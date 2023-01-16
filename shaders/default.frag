#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture;

void main()
{
    vec3 color = texture(u_texture, uv).rgb;
    fragColor = vec4(color, 1.0);
}