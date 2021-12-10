#version 430

attribute vec3 velocity;
attribute float alpha;
attribute vec3 color;

varying vec4 color_out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
//uniform vec3 gravity;
//uniform float particleLifeTime;

void main() {
    color_out = vec4(0, 0, length(normalize(color)), 1);

    gl_Position = perspective * view * model * vec4(velocity, 1.0);
}

