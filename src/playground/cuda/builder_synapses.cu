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

// Independent edges reproduce the original ascending-neuron event order.
extern "C" __global__ void pan_synaptic_plasticity(unsigned count, unsigned flags,
    double decay, double learning, const double* input, double* output) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=count) return;
    // weight, eligibility, eligibility time, pre/post deltas, decayed traces,
    // spike flags, source/target IDs, current tick.
    const double* x=input+12*i;
    double weight=x[0], eligibility=x[1]*decay, last=x[2];
    bool pre=x[7]!=0.0, post=x[8]!=0.0, pre_first=x[9]<x[10];
    for(unsigned event=0;event<2;++event) {
        bool source_event=(event==0)==pre_first;
        if(source_event && pre) {
            if((flags&1) && x[4]>0.0 && x[4]<=20.0) weight=fmax(0.0,weight-0.08*learning);
            if(flags&2) weight=fmax(0.0,weight-0.04*(x[6]+((!pre_first && post)?1.0:0.0)));
            if(flags&4) {eligibility-=0.5;last=x[11];}
        } else if(!source_event && post) {
            if((flags&1) && x[3]>0.0 && x[3]<=20.0) weight=fmin(100.0,weight+0.1*learning);
            if(flags&2) weight=fmin(100.0,fmax(0.0,weight+0.06*(x[5]+((pre_first && pre)?1.0:0.0))+0.025*x[6]));
            if(flags&4) {eligibility+=1.0;last=x[11];}
        }
    }
    output[3*i]=weight;output[3*i+1]=eligibility;output[3*i+2]=last;
}

extern "C" __global__ void pan_synaptic_scale(unsigned count, unsigned unused,
    double factor, double maximum, const double* input, double* output) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;if(i>=count)return;
    output[2*i]=fmax(0.0,fmin(maximum,input[5*i]*factor));output[2*i+1]=0.0;
}
