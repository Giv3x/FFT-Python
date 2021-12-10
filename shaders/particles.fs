#version 430

varying vec4 color_out;

uniform sampler2D img;

void main() {
    gl_FragColor = color_out;
}