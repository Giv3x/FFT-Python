#version 430 core

layout (local_size_x=16, local_size_y=16) in;
layout (rgba32f, binding=0) writeonly uniform image2D tilde_h0k;
layout (rgba32f, binding=1) writeonly uniform image2D tilde_h0minusk;

uniform sampler2D noise;

uniform int N = 256;
uniform int L = 1000;
uniform float A = 20;
uniform vec2 w = vec2(1, 1);
uniform float wind_speed = 15;

const float g = 9.8;
const float M_PI = 3.1415926535897932384626433832795;

vec4 gaussRND() {
    vec2 texCoord = vec2(gl_GlobalInvocationID.xy)/float(N);

	float noise00 = clamp(texture(noise, texCoord).r, 0.001, 1.0);
	float noise01 = clamp(texture(noise, texCoord).g, 0.001, 1.0);
	float noise02 = clamp(texture(noise, texCoord).b, 0.001, 1.0);
	float noise03 = clamp(texture(noise, texCoord).a, 0.001, 1.0);

	float u0 = 8.0*M_PI*noise00;
	float v0 = sqrt(-2.0 * log(noise01));
	float u1 = 8.0*M_PI*noise02;
	float v1 = sqrt(-2.0 * log(noise03));

	vec4 rnd = vec4(v0 * cos(u0), v0 * sin(u0), v1 * cos(u1), v1 * sin(u1));

	return rnd;
}

void main() {
    vec2 x = vec2(gl_GlobalInvocationID.xy) - float(N)/2;

    vec2 k = vec2(2 * M_PI * x.x/L, 2 * M_PI * x.y/L);

    float L_ = (wind_speed * wind_speed) / g;
    float mag = length(k);
    if(mag < 0.00001) mag = 0.00001;
    float magSq = mag * mag;

    float h0k = clamp(sqrt((A/(magSq*magSq)) * pow(dot(normalize(k),normalize(w)), 2) * exp(-(1/(magSq*L_*L_))) * exp(-magSq*pow(L/2000.0,2)))/sqrt(2.0), -4000, 4000);
    float h0minusk = clamp(sqrt((A/(magSq*magSq)) * pow(dot(normalize(-k),normalize(w)), 2) * exp(-(1/(magSq*L_*L_))) * exp(-magSq*pow(L/2000.0,2)))/sqrt(2.0), -4000, 4000);

    vec4 gauss_random = gaussRND();

    imageStore(tilde_h0k, ivec2(gl_GlobalInvocationID.xy), vec4(gauss_random.xy * h0k, 0, 1));
    imageStore(tilde_h0minusk, ivec2(gl_GlobalInvocationID.xy), vec4(gauss_random.zw * h0minusk, 0, 1));
}