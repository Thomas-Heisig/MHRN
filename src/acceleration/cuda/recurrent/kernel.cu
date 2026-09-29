#include <cooperative_groups.h>

#ifdef PAN_PLASTIC
__device__ double release_uniform(unsigned seed, unsigned tick, unsigned edge) {
    unsigned bits = seed ^ (tick * 0x9E3779B9u) ^ (edge * 0x85EBCA6Bu);
    bits ^= bits >> 16; bits *= 0x7FEB352Du;
    bits ^= bits >> 15; bits *= 0x846CA68Bu; bits ^= bits >> 16;
    return (bits >> 8) / 16777216.0;
}
#endif

// Deterministic incoming-edge gather: no floating point atomic accumulation.
// All blocks participate in the barrier, including partial-block inactive lanes.
extern "C" __global__ void pan_recurrent_kernel(
    const unsigned n, const unsigned ticks, const unsigned ring_size,
    const unsigned model, const double dt,
    const unsigned* offsets, const unsigned* sources,
    const unsigned* delays, double* weights,
    const double* external, const double* parameters,
    double* voltage, double* adaptation, unsigned* ring,
    double* voltage_history, double* adaptation_history, unsigned* spikes
#ifdef PAN_PLASTIC
    , const double* config, const double* rewards, double* eligibility,
    double* available, int* last_event, int* last_spike, double* emitted
#endif
    ) {
    auto grid = cooperative_groups::this_grid();
    const unsigned neuron = blockIdx.x * blockDim.x + threadIdx.x;
    for (unsigned tick = 0; tick < ticks; ++tick) {
        if (neuron < n) {
            double current = external[tick * n + neuron];
            for (unsigned edge = offsets[neuron]; edge < offsets[neuron + 1]; ++edge) {
                if (tick >= delays[edge]) {
                    const unsigned slot = (tick - delays[edge]) % ring_size;
#ifdef PAN_PLASTIC
                    current += emitted[slot * offsets[n] + edge];
#else
                    current += weights[edge] * ring[slot * n + sources[edge]];
#endif
                }
            }
            const double* p = parameters + neuron * 10;
            double v = voltage[neuron];
            double w = adaptation[neuron];
            if (model == 0) {
                v += dt * ((p[0] - v + p[9] * current) / p[3]);
            } else {
                const double exponent = fmin(20.0, (v - p[1]) / p[2]);
                const double dv = (-(v - p[0]) + p[2] * exp(exponent) - w + current) / p[3];
                const double dw = (p[5] * (v - p[0]) - w) / p[4];
                v += dt * dv;
                w += dt * dw;
            }
            const unsigned spike = v >= p[7];
            if (spike) {
                v = p[8];
                if (model != 0) w += p[6];
            }
            voltage[neuron] = v;
            adaptation[neuron] = w;
            voltage_history[tick * n + neuron] = v;
            adaptation_history[tick * n + neuron] = w;
            spikes[tick * n + neuron] = spike;
            ring[(tick % ring_size) * n + neuron] = spike;
        }
        grid.sync();
#ifdef PAN_PLASTIC
        if (neuron < n) {
            const unsigned post = spikes[tick * n + neuron];
            for (unsigned edge = offsets[neuron]; edge < offsets[neuron + 1]; ++edge) {
                const unsigned source = sources[edge];
                const unsigned pre = spikes[tick * n + source];
                double weight = weights[edge];
                double trace = eligibility[edge] * exp(-dt / config[7]);
                const int since_pre = (int)tick - last_spike[source];
                const int since_post = (int)tick - last_spike[neuron];
                for (unsigned phase = 0; phase < 2; ++phase) {
                    const bool pre_phase = source <= neuron ? phase == 0 : phase == 1;
                    if (pre_phase && pre) {
                        if (config[0] && since_post > 0 && since_post <= 20)
                            weight = fmax(0.0, weight - 0.08);
                        trace -= 0.5;
                    }
                    if (!pre_phase && post) {
                        if (config[0] && since_pre > 0 && since_pre <= 20)
                            weight = fmin(100.0, weight + 0.1);
                        trace += 1.0;
                    }
                }
                if (pre || post) last_event[edge] = tick;
                if (config[2] && (int)tick - last_event[edge] <= config[8])
                    weight = fmin(100.0, fmax(0.0, weight + config[4] * config[9] * config[10] * trace * rewards[tick]));
                double amplitude = pre ? weight : 0.0;
                double resource = available[edge];
                if (config[1]) {
                    if (pre) {
                        amplitude *= release_uniform((unsigned)config[3], tick, edge) < fmin(0.95, 0.25 + 0.7 * resource);
                        resource = fmax(0.1, resource * 0.72);
                    }
                    resource = fmin(1.0, resource + 0.025);
                }
                available[edge] = resource;
                emitted[(tick % ring_size) * offsets[n] + edge] = amplitude;
                weights[edge] = fmin(config[6], fmax(0.0, weight * (1.0 - config[5])));
                eligibility[edge] = trace;
            }
        }
        grid.sync();
        if (neuron < n && spikes[tick * n + neuron]) last_spike[neuron] = tick;
        grid.sync();
#endif
    }
}
