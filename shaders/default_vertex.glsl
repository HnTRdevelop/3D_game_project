#version 440
#define PI 3.14159265359

#define FAR 1000
#define NEAR 0.001
#define FOV PI / 2


layout(location=0) in vec3 vertPos;
layout(location=1) in vec3 inCol;
out vec3 outCol;

void main()
{
    float f = 1 / tan(FOV / 2);
    float a = 800 / 600;
    float q = FAR / (FAR - NEAR);

    float posx = (a * f * vertPos.x) / vertPos.z;
    float posy = (f * vertPos.y) / vertPos.z;
    float posz = vertPos.z * q - NEAR * q;

    gl_Position = vec4(posx / vertPos.z, posy / vertPos.z, posz / vertPos.z, 1);

	outCol = inCol;
}