#version 330

attribute vec3 position;
attribute vec2 texCoords;

varying vec2 texCoord;
varying vec4 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;

void main() {
    gl_Position = perspective * view * model * vec4(position, 1.0);
    texCoord = vec2(texCoords.x, 1-texCoords.y);
    //color = abs(perspective[0]);
}