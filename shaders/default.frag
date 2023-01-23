#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture;

void main()
{
    float gamma = 2.2;

    vec3 color = texture(u_texture, uv).rgb;
    color = pow(color, vec3(gamma));

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}