// Two phases preserve Builder ordering: decay before plasticity, commit after emission.
extern "C" __global__ void pan_neuron_traces(unsigned n, unsigned commit, unsigned tick,
    const unsigned* spikes, double* traces, long long* last_spike) {
    unsigned i=blockIdx.x*blockDim.x+threadIdx.x;if(i>=n)return;
    if(!commit) {
        traces[i]*=0.95;traces[n+i]*=0.95;
    } else if(spikes[i]) {
        traces[i]+=1.0;traces[n+i]+=1.0;last_spike[i]=(long long)tick;
    }
}
