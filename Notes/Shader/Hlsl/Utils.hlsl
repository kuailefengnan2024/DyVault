// fit Value
float fit(float value, float oldMin, float oldMax, float newMin, float newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}

// 添加向量版本的 fit 函数
float2 fit(float2 value, float2 oldMin, float2 oldMax, float2 newMin, float2 newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}

float3 fit(float3 value, float3 oldMin, float3 oldMax, float3 newMin, float3 newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}

float4 fit(float4 value, float4 oldMin, float4 oldMax, float4 newMin, float4 newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}


// 添加重映射函数
float remap(float value, float oldMin, float oldMax, float newMin, float newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}













// 合并同一空间的法线向量
float3 CombineNormals(float3 n1, float3 n2) {
    // 合并 x 和 y 分量
    float3 result;
    result.xy = n1.xy + n2.xy;

    // 归一化向量
    result = normalize(result);

    // 重建 z 分量
    result.z = sqrt(saturate(1.0 - dot(result.xy, result.xy)));

    return result;
}






// 合并不同空间的法线向量
float3 CombineNormalsDifferentSpaces(float3 n1, float3 n2, float3x3 tangentToWorld) {
    // 将切线空间法线转换到世界空间
    float3 n1_world = mul(tangentToWorld, n1);

    // 合并 x 和 y 分量
    float3 result;
    result.xy = n1_world.xy + n2.xy;

    // 归一化向量
    result = normalize(result);

    // 重建 z 分量
    result.z = sqrt(saturate(1.0 - dot(result.xy, result.xy)));

    return result;
}




