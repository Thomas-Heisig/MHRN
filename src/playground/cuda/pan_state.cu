// Exploratory PAN per-neuron state and ordered population reduction.
__device__ double pan_bound(double x, double lo=0.0, double hi=1.0) {
    return fmax(lo, fmin(hi, x));
}
extern "C" __global__ void pan_state_step(
    unsigned n, unsigned dimensions, unsigned tick, unsigned plastic,
    double dt, double decay, double death_threshold,
    const double* voltage, const double* threshold, const double* position,
    const double* coupling, const unsigned* spikes, unsigned* alive,
    double* state, double* vectors) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i>=n || !alive[i]) return;
    // health, amplitude, energy, activity EMA, consolidation, information proxy
    double* s=state+6*i;
    bool spike=spikes[i]!=0;
    double activity=0.97*s[3]+0.03*(spike?1.0:0.0);
    double energy=s[2]; energy+=0.015*(1.0-energy);
    if(spike) energy-=0.035;
    energy=pan_bound(energy);
    double p=pan_bound(activity,1e-6,1.0-1e-6);
    double information=pan_bound(-log2(spike?p:(1.0-p))/8.0);
    double stress=fabs(activity-0.02)+fmax(0.0,0.35-energy);
    double health=s[0]; health-=decay*(dt/1000.0);
    health-=0.0015*stress; health+=0.0005*fmax(0.0,1.0-stress);
    health=pan_bound(health);
    double consolidation=pan_bound(0.995*s[4]+(spike?0.005:0.0));
    s[0]=health; s[1]=pan_bound(0.2+0.8*health,0.2,1.0); s[2]=energy;
    s[3]=activity; s[4]=consolidation; s[5]=information;
    double exponent=pan_bound((voltage[i]-threshold[i])/5.0,-40.0,40.0);
    double values[10]={(tick+1)*(dt/1000.0),1.0/(1.0+exp(-exponent)),
      plastic?health:0.0,information,health,
      0.5+0.5*sin(2.0*3.141592653589793*(tick%64)/64.0),energy,
      position[i],consolidation,coupling[i]};
    for(unsigned d=0;d<dimensions;++d) vectors[i*dimensions+d]=d<10?values[d]:0.0;
    if(health<=death_threshold) alive[i]=0;
}

// One ordered writer per axis, retaining dead-neuron vectors as the CPU does.
extern "C" __global__ void pan_population_mean(unsigned n, unsigned dimensions, unsigned slot,
    const double* vectors, double* population, double* history) {
    unsigned d=threadIdx.x;if(d>=dimensions)return;
    double total=0.0;
    for(unsigned i=0;i<n;++i) total+=vectors[i*dimensions+d];
    population[d]=total/(double)n;
    history[slot*dimensions+d]=population[d];
}

// History availability is bounded by the same retention window as the CPU.
extern "C" __global__ void pan_feedback_source(unsigned dimensions, unsigned source,
    unsigned delay, unsigned count, unsigned next_slot,
    const double* population, const double* history, double* vector) {
    unsigned d=threadIdx.x;if(d>=dimensions)return;
    double value=delay==0?population[d]:(count>delay?history[((next_slot+66-1-delay)%66)*dimensions+d]:0.0);
    if(source==1 && d>=dimensions/2) value=0.0;
    else if(source==2 && d%2) value=0.0;
    else if(source==3) value=tanh(value);
    vector[d]=value;
}

// Ordered projection of the selected device source.
extern "C" __global__ void pan_feedback_step(
    unsigned n, unsigned dimensions, unsigned nonlinearity,
    double gain, double threshold, double saturation,
    const double* weights, const double* vector, const unsigned* enabled,
    double* currents) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i>=n) return;
    double raw=0.0;
    for(unsigned d=0;d<dimensions;++d) raw+=weights[i*dimensions+d]*vector[d];
    double shaped=raw;
    if(nonlinearity==1) shaped=tanh(raw);
    else if(nonlinearity==2) shaped=raw>0.0?1.0:(raw<0.0?-1.0:0.0);
    else if(nonlinearity==3) shaped=pan_bound(raw,-1.0,1.0);
    if(fabs(shaped)<threshold) shaped=0.0;
    currents[i]=pan_bound(enabled[i]?gain*shaped:0.0,-saturation,saturation);
}
