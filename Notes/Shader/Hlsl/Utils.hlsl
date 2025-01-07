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

/* example
float originValue = fit(0.5, 0.0, 1.0, -1.0, 1.0); // 从0.5映射到0
*/

// 添加重映射函数
float remap(float value, float oldMin, float oldMax, float newMin, float newMax) {
    return newMin + (value - oldMin) * (newMax - newMin) / (oldMax - oldMin);
}


// 归一化标量变量
float normalizedValue = (Value - min) / (max - min);