#version 330

varying vec2 texCoord;
varying vec4 color;

uniform sampler2D img;

void main() {
    gl_FragColor = texture(img, texCoord);
}