#version 430

attribute vec3 position;
attribute vec2 texCoord;

varying vec4 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;

uniform sampler2D img;

void main() {
    float h = texture(img, vec2(texCoord.x, texCoord.y)).r;
    gl_Position = perspective * view * model * vec4(vec3(position.x,position.y+h*15, position.z), 1.0);
        //perspective * view * model * vec4(position, 1.0);
    //color = abs(perspective[0]);
}