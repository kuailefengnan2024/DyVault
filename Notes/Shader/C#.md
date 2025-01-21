### C# 基础速通（Shader技术美术相关）

| 内容                 | 描述                                                                                               |
|----------------------|----------------------------------------------------------------------------------------------------|
| **C#的角色**         | 在Shader和渲染管线中负责控制和管理，设置Shader参数、处理材质逻辑、调用渲染命令，并整合后处理效果。 |
| **为何用C#而非Shader**| Shader专注GPU计算和图像处理，C#运行在CPU上，负责逻辑控制、资源管理和动态交互，实现功能灵活性。       |

以下是C#中与Shader开发和Unity引擎相关的基础内容，帮助你快速理解代码结构和常用功能：

---

### **1. 基础语法**
- **命名空间**：
  - `using`：引入命名空间，类似于包含库。例如：
    ```csharp
    using UnityEngine; // Unity的核心引擎功能
    using UnityEngine.Rendering.PostProcessing; // 后处理相关
    ```

- **类与继承**：
  - `class`：定义类。
  - `: BaseClass`：表示继承。例如：
    ```csharp
    public class MyEffect : PostProcessEffectSettings { } // 继承后处理效果基类
    ```

- **方法与函数**：
  - `public` / `private`：访问修饰符，决定方法或变量的可见性。
    ```csharp
    public void MyFunction() { } // 公共方法
    private void HelperFunction() { } // 私有方法
    ```

- **属性与变量**：
  - `public Type Name`：定义变量或属性。例如：
    ```csharp
    public float intensity = 1.0f; // 公共浮点变量
    ```

---

### **2. Unity常用类和方法**
#### **2.1 MonoBehaviour（脚本组件基类）**
- **生命周期函数**：
  - `Start()`：脚本启用时运行一次。
  - `Update()`：每帧运行一次，用于逻辑更新。
  - `OnRenderImage()`：后处理相关，处理屏幕渲染图像。

#### **2.2 PostProcessing相关**
- **PostProcessEffectSettings**：
  - 定义后处理效果的参数。
  - 常用类型：
    ```csharp
    public FloatParameter blend; // 浮点参数
    public ColorParameter color; // 颜色参数
    ```

- **PostProcessEffectRenderer<T>**：
  - 实现后处理效果的具体渲染逻辑。
  - 核心方法：
    ```csharp
    public override void Render(PostProcessRenderContext context) { } // 渲染逻辑
    ```

- **PostProcessRenderContext**：
  - 提供渲染上下文数据，如输入源纹理、目标纹理等。
    ```csharp
    context.source; // 源纹理
    context.destination; // 目标纹理
    ```

---

### **3. Shader与C#交互方法**
#### **3.1 设置Shader参数**
- **常用方法（Material类）**：
  ```csharp
  Material.SetFloat("_ParamName", value); // 设置浮点数参数
  Material.SetColor("_Color", colorValue); // 设置颜色参数
  Material.SetTexture("_MainTex", texture); // 设置纹理参数
  ```

#### **3.2 渲染相关**
- `BlitFullscreenTriangle`（PostProcessing专用）：
  - 将屏幕图像从源纹理渲染到目标纹理。
    ```csharp
    context.command.BlitFullscreenTriangle(source, destination, sheet, 0);
    ```

---

### **4. 常用Unity内置类**
- **CommandBuffer**：
  - 用于存储渲染命令。
    ```csharp
    CommandBuffer cmd = context.command; // 获取命令缓冲区
    cmd.BeginSample("SampleName"); // 开始性能分析采样
    cmd.EndSample("SampleName"); // 结束采样
    ```

- **PropertySheet**：
  - 管理Shader的属性。
    ```csharp
    PropertySheet sheet = context.propertySheets.Get(Shader.Find("ShaderName"));
    sheet.properties.SetFloat("_MyParam", value); // 设置Shader参数
    ```

- **Color**：
  - Unity的颜色类型。
    ```csharp
    Color color = new Color(1f, 0f, 0f, 1f); // 红色，带Alpha通道
    ```

---

### **5. C#基础工具**
- **属性修饰**：
  - `[Serializable]`：允许类或字段可被序列化。
  - `[Tooltip("TooltipText")]`：在Inspector中显示提示文字。
  - `[Range(min, max)]`：限制参数范围。

- **泛型**：
  - 用于定义灵活的数据类型。
    ```csharp
    public List<float> values = new List<float>(); // 泛型列表
    ```

- **常见关键词**：
  - `var`：自动推断变量类型。
  - `new`：创建对象实例。
  - `override`：重写基类方法。

---

### **6. 示例总结**
以下是一段完整的代码示例，结合了上述内容：
```csharp
uusing UnityEngine; // 引入Unity核心命名空间，用于访问游戏对象、组件等功能。
using UnityEngine.Rendering.PostProcessing; // 引入Unity后处理(PostProcessing)的命名空间，用于创建后处理效果。

[Serializable] // 表示这个类可以序列化，让其属性可以在Inspector中显示并被保存。
[PostProcess(typeof(MyEffectRenderer), PostProcessEvent.AfterStack, "MyEffect")]
// 注册一个自定义后处理效果：
// - typeof(MyEffectRenderer): 指定渲染器类。
// - PostProcessEvent.AfterStack: 效果执行顺序，所有后处理效果处理完后执行。
// - "MyEffect": 在PostProcessing Volume下拉菜单中显示的名字。
public class MyEffect : PostProcessEffectSettings // 定义一个后处理效果设置类，继承自PostProcessEffectSettings。
{
    public ColorParameter color = new ColorParameter { value = Color.white }; 
    // 定义一个颜色参数，类型为ColorParameter，值默认为白色。

    public FloatParameter intensity = new FloatParameter { value = 1.0f }; 
    // 定义一个浮点参数，类型为FloatParameter，值默认为1.0。
}

public sealed class MyEffectRenderer : PostProcessEffectRenderer<MyEffect> 
// 定义一个渲染器类，用于实现具体的渲染逻辑，绑定到MyEffect类。
{
    public override void Render(PostProcessRenderContext context) 
    // 重写Render方法（PostProcessEffectRenderer的核心方法），负责实现后处理效果的渲染逻辑。
    {
        var cmd = context.command; 
        // 获取CommandBuffer（命令缓冲区），用于存储并执行渲染命令。

        cmd.BeginSample("MyEffect"); 
        // 标记采样区域，方便性能分析和调试（Profiler中显示为"MyEffect"）。

        var sheet = context.propertySheets.Get(Shader.Find("Hidden/MyEffect")); 
        // 获取PropertySheet（属性表），用于管理Shader和其属性。
        // Shader.Find("Hidden/MyEffect") 用于加载名为"Hidden/MyEffect"的隐藏Shader。

        sheet.properties.SetColor("_Color", settings.color); 
        // 将用户在Inspector中设置的颜色参数传递到Shader中的"_Color"变量。

        sheet.properties.SetFloat("_Intensity", settings.intensity); 
        // 将用户设置的强度参数传递到Shader中的"_Intensity"变量。

        context.command.BlitFullscreenTriangle(context.source, context.destination, sheet, 0); 
        // 执行全屏渲染：
        // - context.source: 当前屏幕的渲染输入纹理。
        // - context.destination: 渲染后的目标纹理。
        // - sheet: 包含了Shader和参数的PropertySheet。
        // - 0: 指定Shader中使用的第一个Pass。

        cmd.EndSample("MyEffect"); 
        // 结束采样区域，方便Profiler中查看性能数据。
    }
}
 ```

---

### 快速解释这些词：

- **命名空间**：代码的分类容器，用来组织类和方法，防止命名冲突。  
  _例：`using UnityEngine;` 引入Unity核心功能。_

- **类**：代码的模板，定义对象的属性和行为。  
  _例：`public class MyEffect {}` 定义一个效果类。_

- **修饰符**：控制变量、方法、类的访问权限或特性。  
  _例：`public` 公共，`private` 私有，`static` 静态。_

- **脚本组件基类**：Unity中脚本的基础类，比如`MonoBehaviour`。  
  _例：`public class MyScript : MonoBehaviour` 是一个组件脚本。_

- **属性**：类中定义的变量，用于存储对象的数据。  
  _例：`public float intensity;` 定义一个强度变量。_

- **方法**：类中定义的功能或动作。  
  _例：`void Update()` 每帧执行一次的方法。_

- **字段**：类中的变量或成员，存储对象的状态。  
  _例：`private int value;` 是一个字段。_

- **接口**：定义行为的契约，类可以实现接口来提供具体功能。  
  _例：`public interface IDamageable { void TakeDamage(); }`_

- **继承**：一个类继承另一个类的属性和行为。  
  _例：`class MyEffect : PostProcessEffectSettings`_

- **泛型**：定义数据结构或方法时允许使用任意数据类型。  
  _例：`List<T> values = new List<int>();`_

- **序列化**：将数据保存到文件或Inspector中可编辑。  
  _例：`[Serializable]` 让类能显示在Inspector中。_

一句话总结：这些是C#中组织代码、定义功能和与Unity协作的基础概念，非常重要！

### **速通总结**
1. **基础语法**：理解命名空间、类、变量、方法、修饰符。
2. **Unity专用**：熟悉`PostProcessEffectSettings`、`PostProcessEffectRenderer`等类。
3. **Shader交互**：重点掌握`Material.SetXXX`、`BlitFullscreenTriangle`。
4. **工具和修饰**：清楚`[Serializable]`、`[Range]`等属性的作用。

