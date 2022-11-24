#version 440
#define PI 3.1415926535897932384626433832795

in vec3 outCol;
out vec4 fragCol;

void main()
{
    fragCol = vec4(outCol, 1);
}