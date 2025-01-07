Shader "Custom/RandomStarWithColorAndEmission"
{
    Properties
    {
        _Scale ("Scale", Float) = 10.0       // 控制星点分布密度
        _Threshold ("Threshold", Float) = 0.1 // 控制星点基础大小
        _Blur ("Blur", Float) = 0.05        // 控制模糊程度
        _Color1 ("Star Color 1", Color) = (1, 0, 0, 1) // 星星颜色1
        _Color2 ("Star Color 2", Color) = (0, 1, 0, 1) // 星星颜色2
        _Color3 ("Star Color 3", Color) = (0, 0, 1, 1) // 星星颜色3
        _EmissionIntensity ("Emission Intensity", Float) = 1.0 // 自发光强度
        _Seed ("Random Seed", Float) = 43758.5453 // 随机种子
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            float _Scale;
            float _Threshold;
            float _Blur;
            float4 _Color1;
            float4 _Color2;
            float4 _Color3;
            float _EmissionIntensity;
            float _Seed;
            
            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            
            float hash(float p)
            {
                p = frac(sin(p) * _Seed);
                return p;
            }

            float2 hash21(float2 p)
            {
                p = frac(sin(dot(p, float2(12.9898, 78.233))) * _Seed);
                return frac(float2(p.x * p.y, p.x + p.y));
            }

            float voronoi(float2 uv, float scale, out float intensity, out int colorIndex)
            {
                uv *= scale;
                float2 g = floor(uv);
                float2 f = frac(uv);

                float minDist = 1.0;
                intensity = 0.0;
                colorIndex = 0;

                for (int y = -1; y <= 1; y++)
                {
                    for (int x = -1; x <= 1; x++)
                    {
                        float2 lattice = float2(x, y);
                        float2 randomOffset = hash21(g + lattice);
                        float2 neighbor = g + lattice + randomOffset;
                        float dist = length(f - (neighbor - g));

                        if (dist < minDist)
                        {
                            minDist = dist;
                            intensity = 0.2 + 0.8 * hash(dot(neighbor, float2(7.0, 3.0)));
                            
                            // 生成随机颜色索引（1-3）
                            colorIndex = int(floor(hash(dot(neighbor, float2(13.0, 17.0))) * 3.0)) + 1;
                        }
                    }
                }
                return minDist;
            }

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float intensity;
                int colorIndex;
                float noise = voronoi(i.uv, _Scale, intensity, colorIndex);

                // 模糊处理
                float star = smoothstep(_Threshold * 0.01 + _Blur * 0.01, _Threshold * 0.01 - _Blur * 0.01, noise * intensity);

                // 根据颜色索引选择颜色
                float4 color = (colorIndex == 1) ? _Color1 :
                               (colorIndex == 2) ? _Color2 : _Color3;

                // 将星点颜色用于自发光，应用自发光强度
                float4 emission = color * star * intensity * _EmissionIntensity;

                // 输出颜色（可以叠加到其他材质输出中，如果需要）
                return fixed4(emission.rgb, 1); // Alpha 通道保持为 1
            }
            ENDCG
        }
    }
    FallBack "Diffuse"
}