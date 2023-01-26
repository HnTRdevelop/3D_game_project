#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;
in vec3 normal;
in vec3 frag_pos;

uniform sampler2D u_texture;
uniform vec3 view_pos;
uniform int light_count;
uniform vec3 light_sources[128];
uniform vec3 light_colors[128];

void main()
{
    vec3 color = texture(u_texture, uv).rgb;

    float ambientStrength = 0.1;
    vec3 ambient = vec3(0);

    vec3 diffuse = vec3(0);

    float specular_streangth = 0.5;
    vec3 specular = vec3(0);

    for(int i = 0; i < light_count; i++){
        vec3 light_pos = light_sources[i];
        vec3 light_color = light_colors[i];

        ambient += ambientStrength * light_color;

        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_pos - frag_pos);
        float diff = max(dot(norm, light_dir), 0.0);
        diffuse += diff * light_color;

        vec3 view_dir = normalize(view_pos - frag_pos);
        vec3 reflect_dir = reflect(-light_dir, norm);
        float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32.0);
        specular += specular_streangth * spec * light_color;
    }

    color = (ambient + diffuse + specular) * color;

    float gamma = 2.2;
    color = pow(color, vec3(gamma));
    color = pow(color, 1 / vec3(gamma));

    fragColor = vec4(color, 1.0);
}