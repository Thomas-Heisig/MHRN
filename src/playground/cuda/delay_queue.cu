extern "C" __global__ void pan_delay_consume(unsigned n, unsigned slot, double* queue, double* currents) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;if(i>=n)return;
    currents[i]=queue[slot*n+i];queue[slot*n+i]=0.0;
}
// One writer per target, preserving the supplied emission order without atomics on current.
extern "C" __global__ void pan_delay_enqueue(unsigned n, unsigned count, unsigned tick,
    const unsigned* targets,const unsigned* delays,const double* amplitudes,double* queue,unsigned* invalid) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;if(i>=n)return;
    for(unsigned e=0;e<count;++e) if(targets[e]==i) {
        unsigned slot=((tick%65)+delays[e])%65;
        double value=queue[slot*n+i]+amplitudes[e];
        if(!isfinite(value)) atomicExch(invalid,1u);
        queue[slot*n+i]=value;
    }
}
