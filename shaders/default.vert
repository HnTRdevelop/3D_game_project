#version 330 core

layout (location = 0) in  vec2 in_texture_coord;
layout (location = 1) in vec3 in_position;

out vec2 uv;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

void main()
{
    uv = in_texture_coord;
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}