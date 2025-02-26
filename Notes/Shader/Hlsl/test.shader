// 渐变映射函数 - 类似PS中的渐变映射
// 输入颜色将被映射到由四个控制点定义的渐变上

// 定义渐变控制点结构 (为四个均匀分布的颜色点)
float4 _GradientColor1; // 对应亮度 0.0
float4 _GradientColor2; // 对应亮度 0.333
float4 _GradientColor3; // 对应亮度 0.667
float4 _GradientColor4; // 对应亮度 1.0

// 计算输入颜色的亮度
float CalculateLuminance(float3 color)
{
    // 使用标准亮度系数
    return dot(color, float3(0.299, 0.587, 0.114));
}

// 在两个颜色之间插值
float4 LerpColor(float4 colorA, float4 colorB, float t)
{
    return lerp(colorA, colorB, t);
}

// 主渐变映射函数
float4 ApplyGradientMapping(float4 inputColor)
{
    // 计算输入颜色的亮度值 (0-1范围)
    float luminance = CalculateLuminance(inputColor.rgb);
    
    // 根据亮度确定在渐变中的位置
    float4 mappedColor;
    
    if (luminance < 0.333)
    {
        // 在第一段渐变中
        float t = luminance / 0.333;
        mappedColor = LerpColor(_GradientColor1, _GradientColor2, t);
    }
    else if (luminance < 0.667)
    {
        // 在第二段渐变中
        float t = (luminance - 0.333) / 0.334;
        mappedColor = LerpColor(_GradientColor2, _GradientColor3, t);
    }
    else
    {
        // 在第三段渐变中
        float t = (luminance - 0.667) / 0.333;
        mappedColor = LerpColor(_GradientColor3, _GradientColor4, t);
    }
    
    // 可选：保留原始的Alpha值
    mappedColor.a = inputColor.a;
    
    return mappedColor;
}

// 更灵活的版本 - 支持自定义颜色在梯度中的位置
float4 _CustomGradientColors[4]; // 颜色数组
float _CustomGradientPositions[4]; // 位置数组 (0-1范围)

float4 ApplyCustomGradientMapping(float4 inputColor)
{
    float luminance = CalculateLuminance(inputColor.rgb);
    float4 mappedColor = float4(0, 0, 0, inputColor.a);
    
    // 找到luminance所在的区间
    for (int i = 0; i < 3; i++)
    {
        if (luminance >= _CustomGradientPositions[i] && luminance <= _CustomGradientPositions[i+1])
        {
            float t = (luminance - _CustomGradientPositions[i]) / 
                     (_CustomGradientPositions[i+1] - _CustomGradientPositions[i]);
            
            mappedColor = LerpColor(_CustomGradientColors[i], _CustomGradientColors[i+1], t);
            break;
        }
    }
    
    return mappedColor;
}