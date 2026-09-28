#include <cooperative_groups.h>

// Deterministic incoming-edge gather: no floating point atomic accumulation.
// All blocks participate in the barrier, including partial-block inactive lanes.
extern "C" __global__ void pan_recurrent_kernel(
    const unsigned n, const unsigned ticks, const unsigned ring_size,
    const unsigned model, const double dt,
    const unsigned* offsets, const unsigned* sources,
    const unsigned* delays, const double* weights,
    const double* external, const double* parameters,
    double* voltage, double* adaptation, unsigned* ring,
    double* voltage_history, double* adaptation_history, unsigned* spikes) {
    auto grid = cooperative_groups::this_grid();
    const unsigned neuron = blockIdx.x * blockDim.x + threadIdx.x;
    for (unsigned tick = 0; tick < ticks; ++tick) {
        if (neuron < n) {
            double current = external[tick * n + neuron];
            for (unsigned edge = offsets[neuron]; edge < offsets[neuron + 1]; ++edge) {
                if (tick >= delays[edge]) {
                    const unsigned slot = (tick - delays[edge]) % ring_size;
                    current += weights[edge] * ring[slot * n + sources[edge]];
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
    }
}
