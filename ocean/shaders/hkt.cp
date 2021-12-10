#version 430 core

layout (local_size_x = 16, local_size_y = 16) in;

layout (rgba32f, binding=0) uniform image2D tilde_h0k;
layout (rgba32f, binding=1) uniform image2D tilde_h0minusk;
layout (rgba32f, binding=2) uniform image2D tilde_hkt;

uniform int N = 256;
uniform int L = 1000;
uniform float t = 0;

const float g = 9.8;
const float PI = 3.1415926535897932384626433832795;

struct complex {
    float real;
    float im ;
};

complex mul(complex c0, complex c1) {
    complex c;
    c.real = c0.real * c1.real - c0.im * c1.im;
    c.im = c0.real * c1.im + c0.im * c1.real;

    return c;
}

complex add(complex c0, complex c1) {
    complex c;
    c.real = c0.real + c1.real;
    c.im = c0.im + c1.im;

    return c;
}

complex conj(complex c) {
    return complex(c.real, -c.im);
}

void main() {
    vec2 x = ivec2(gl_GlobalInvocationID.xy) - float(N)/2;
    vec2 k = vec2(2 * PI * x.x/L, 2 * PI * x.y/L);

    float mag = length(k);
    if(mag < 0.00001) mag = 0.00001;

    float w = sqrt(g * mag);

    vec2 h0k_values = imageLoad(tilde_h0k, ivec2(gl_GlobalInvocationID.xy)).rg;
    vec2 h0minusk_values = imageLoad(tilde_h0minusk, ivec2(gl_GlobalInvocationID.xy)).rg;
    complex fourier_cmp = complex(h0k_values.x, h0k_values.y);
    complex fourier_cmp_conj = conj(complex(h0minusk_values.x, h0minusk_values.y));

    float cos_w_t = cos(w*t);
    float sin_w_t = sin(w*t);

    complex exp_iwt = complex(cos_w_t, sin_w_t);
    complex exp_iwt_inv = complex(cos_w_t, -sin_w_t);

    complex hkt_dy = add(mul(fourier_cmp,exp_iwt), mul(fourier_cmp_conj,exp_iwt_inv));

    imageStore(tilde_hkt, ivec2(gl_GlobalInvocationID.xy), vec4(hkt_dy.real, hkt_dy.im, 0, 1));
}