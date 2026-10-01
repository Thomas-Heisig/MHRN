// One real Builder membrane step. Host owns the full PAN/environment loop.
extern "C" __global__ void pan_membrane_step(
    unsigned n, unsigned model, double dt, const double* parameters,
    const double* currents, const unsigned* active,
    double* voltage, double* adaptation, unsigned* spikes) {
    const unsigned i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    spikes[i] = 0;
    if (!active[i]) return;
    const double* p = parameters + 10 * i;
    double v = voltage[i], w = adaptation[i];
    if (model == 0) {
        v += dt * ((p[0] - v + p[9] * currents[i]) / p[3]);
    } else {
        const double exponent = fmin(20.0, (v - p[1]) / p[2]);
        const double dv = (-(v - p[0]) + p[2] * exp(exponent) - w + currents[i]) / p[3];
        const double dw = (p[5] * (v - p[0]) - w) / p[4];
        v += dt * dv;
        w += dt * dw;
    }
    const unsigned spike = v >= p[7];
    if (spike) { v = p[8]; if (model != 0) w += p[6]; }
    voltage[i] = v; adaptation[i] = w; spikes[i] = spike;
}
