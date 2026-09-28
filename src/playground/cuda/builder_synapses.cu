// Builder emission algebra; host supplies traversal-ordered random draws.
extern "C" __global__ void pan_synaptic_emit(unsigned count, unsigned stp,
    double gaba, double ratio, const double* input, double* output) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=count) return;
    const double* x=input+5*i;
    double amplitude=x[0], available=x[1];
    if(x[4]!=0.0) amplitude=-fabs(amplitude)*gaba/ratio;
    amplitude*=x[2];
    if(stp) {
        amplitude*=x[3]<fmin(0.95,0.25+0.7*available)?1.0:0.0;
        available=fmax(0.1,available*0.72);
    }
    output[2*i]=amplitude; output[2*i+1]=available;
}
extern "C" __global__ void pan_synaptic_recover(unsigned count, unsigned stp,
    double decay, double maximum, const double* input, double* output) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=count) return;
    double weight=input[5*i], available=input[5*i+1];
    if(stp) available=fmin(1.0,available+0.025);
    if(decay!=0.0) weight*=fmax(0.0,1.0-decay);
    output[2*i]=fmin(maximum,fmax(0.0,weight)); output[2*i+1]=available;
}

// Live target/posture rewards keep the Builder's eligibility-window contract.
extern "C" __global__ void pan_synaptic_reward(unsigned count, unsigned filter_age,
    double scale, double reward, const double* input, double* output) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=count) return;
    const double* x=input+5*i;
    double weight=x[0];
    if(!filter_age || x[2]<=x[3]) weight=fmin(x[4],fmax(0.0,weight+scale*x[1]*reward));
    output[2*i]=weight; output[2*i+1]=x[1];
}
