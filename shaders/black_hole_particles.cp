#version 430
layout (local_size_x = 1024) in;

layout(std430, binding=0) buffer vel {
    vec4 velocity[];
};

layout(std430, binding=1) buffer pos {
    vec4 position[];
};

uniform float gravity1 = 1000;
uniform vec3 blackHolePos1 = vec3(-3, -2, -2);
uniform float gravity2 = 500;
uniform vec3 blackHolePos2 = vec3(2, 2, -2);

uniform float particleInvMass = 1.0/20;
uniform float deltaT = 0.0005;

float gravity = -0.01;
float particleLifeTime = 20;

void main() {
     uint idx = gl_GlobalInvocationID.x;
     vec3 v = velocity[idx].xyz;
     vec3 p = position[idx].xyz;

     vec3 d = blackHolePos1 - p;
     vec3 force = (gravity1 / length(d) ) * normalize(d);

     d = blackHolePos2 - p;
     force += (gravity2 / length(d) ) * normalize(d);

     vec3 a = force * particleInvMass;

     position[idx] = vec4(p + v*deltaT + 0.5*a*deltaT*deltaT, 1.0);
     velocity[idx] = vec4(v + a*deltaT, 0);
}