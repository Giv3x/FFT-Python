#version 430
layout (local_size_x = 1024) in;

layout(std430, binding=0) buffer vel {
    vec4 velocity[];
};

layout(std430, binding=1) buffer pos {
    vec4 position[];
};

uniform float time;

float gravity = -0.01;
float particleLifeTime = 20;

void main() {
     uint idx = gl_GlobalInvocationID.x;
     vec4 v = velocity[idx];
     position[idx] = vec4(0);

     if(time > v.a) {
        float t = time - v.a;

        if(t < particleLifeTime) {
            position[idx] = vec4(v.xyz*t + gravity*t*t, 1 - t/particleLifeTime);
        }
    }
}