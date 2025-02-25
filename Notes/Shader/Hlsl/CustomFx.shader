// 函数:输入一个浮点数 来控制任意向量二维XZ平面旋转函数
float3 RotateDirXZ(float3 dir, float _Rotate)
{
float rad = _Rotate * 3.14159 / 180;
float2x2 rotate_matrix = float2x2(cos(rad), -sin(rad), sin(rad), cos(rad));
float2 dir_rotatexz = mul(rotate_matrix, dir.xz);
float3 dir_rotate = float3(dir_rotatexz.x,dir.y,dir_rotatexz.y);

return dir_rotate;
}


// 函数:输入一个浮点数 来控制任意向量二维XY平面旋转函数
float3 RotateDirXY(float3 dir, float _Rotate)
{
    float rad = _Rotate * 3.14159 / 180;
    float2x2 rotate_matrix = float2x2(cos(rad), -sin(rad), sin(rad), cos(rad));
    float2 dir_rotatexy = mul(rotate_matrix, dir.xy);
    float3 dir_rotate = float3(dir_rotatexy.x,dir_rotatexy.y,dir.z);
    return dir_rotate;
}


// 函数:输入一个浮点数 来控制任意向量三维旋转函数
float3 RotateDirXYZ(float3 dir, float3 axis, float _Rotate)
{
    float rad = _Rotate * 3.14159 / 180;
    float3x3 rotate_matrix = float3x3(cos(rad), -sin(rad), 0, sin(rad), cos(rad), 0, 0, 0, 1);
    float3 dir_rotate = mul(rotate_matrix, dir);
    return dir_rotate;
}


// 函数:将reflect_dir 转换为uv 可以采样非CubeMap的贴图
float2 ReflectDirToUV(float3 reflect_dir)
{
    float3 reflect_dir_normalize = normalize(reflect_dir);
    float latitude = acos(reflect_dir_normalize.y);
    float longitude = atan2(reflect_dir_normalize.z, reflect_dir_normalize.x);
    float2 sphere_uv = float2(longitude,latitude) * float2(0.5 / 3.14159,1.0 / 3.14159);
    float2 uv = float2(0.5,1.0) - sphere_uv;
    
    return uv;
}


// 解码 HDR 立方体贴图颜色的函数 假设_CubeMap_HDR.x存储曝光指数 也就是pow编码而非rgbm编码   平面 HDR和cubemap都可以处理
float3 DecodeDy(float4 color_cubemap, float4 hdr_params)
{
    return color_cubemap.rgb * pow(2.0, hdr_params.x);
}                