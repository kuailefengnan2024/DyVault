nvidia-smi 检查cuda版本
cursor中的mcp是client --- mcp Protocol协议 --- mcp server(访问本地或者远程)

### 资产库
* 新建catalog，在具体的资产库文件中，以创建目录实体文件
* 打开具体的资产文件，将它移动到创建的目录中，保存即可
### Hardsurface
shift Q吊用randomflow
f调用fluent

### Rig
1.选择模型，autorig选择各个点
2.go生成骨骼后，调整对上模型
3.点击Match to rig生成控制器骨骼
4.绑定控制器和网格（选择体素方式绑定
### Sculpture
分块进行，头部，头发，胸腹，四肢，手指

使用subd方式起大型到六成
使用雕刻抓起，调整中型（调整到五千面左右）
加上多级细分两级，使用显示锐边标记，然后黏条塑造，最后刮削
细分的原理，面的中点连接各边，细分后，三边极点是吸引极点，五边以上都是排斥极点

极点可能导致着色问题，尽量放在平滩表面（3和5边的都叫极点，4不是极点，因为不影响流向）

流向就是头尾四边面的对边中点连线


硬表面建模，先用大块面铺，然后细分即可

做贴纸，可以把所有的贴图画在一张图上，调节uv位置即可
可以把伽马值当做一个选取某一个亮度空间作为画面主色调的东西

摄像机~空物体
标准跟随

矫正平滑修改器可以根据顶点组修复关节破损
我理解这个修改器就是形态键变体，
而且可以用作模型的平滑，这样比雕刻貌似要好

两个纹理混用：
纹理总是需要用向量（蓝色输入）来驱动，在前边的纹理将起到决定性的作用，另外前边的输出往往是黑白的渐变的，这样才能给第二个纹理发挥空间
物体编号在物体bar
材质编号在材质bar

材质置换尽量少用（性能消耗最大），尽量用法向和凹凸去实现

烘焙
1.展好uv，不要重叠
2.选择相应通道，选择模型，选择图像纹理节点，点击烘焙（法线选择noncolor）
3.展uv尽量充满，不浪费像素

凹凸和法线贴图都是连接到法向口上的，可用deepbump插件来图片转法线


### sp插件相关：
1.尽量不要用透明的因为容易与黑白混淆
2.尽量分开模型，分开材质来做，别在图层分，最大程度避免卡顿
3.选用32位浮点格式（柔滑渐变
4.镂板就是sp的映射功能，毛糙边缘可以通过颜渐解决
避免卡顿：设置两个pix材质，其中一个的图层均只保留bc，来画色块
另一个pix材质负责上具体材质
法向通道比较特殊，导出要用rgb使用要用非彩色
bl 3.3以下版本才不会出现保存后再打开丢节点bug

高烘低流程
1.分别导出1和6细分模型
2.sp打开低，纹理集选择高模烘焙
SP通过绘制影响AO的方法
绘制完成后，单独导出法线，替换掉原来的法线贴图即可，烘焙

### UE5相关
三者均可以导出UV和选区
Obj最简单，abc带点动画,fbx带骨骼动画，贴图
UE 命令profilegpu查看gpu占用情况

导入UE之前：
1.展好UV，检查模型破面
2.转换为pbr材质，ue无法识别bl金属度
3.bl导出fbx右侧设置,路径模式选择复制，并点击内嵌纹理，面平滑
3.ue作为关卡导入

快捷键统一
blender~shift alt 触控圈
ue5~shift alt 触控圈

另外需要把数位板设置F3 F4，并且把bl内f3f4设为视图缩放快捷键
数位笔拇指按键为中键

### 设置软连接
来达到各版本同一套插件（addon）和快捷键
win r cmd
mklink /J "D:\BaiduSyncdisk\Blender Foundation\Blender\3.1" "D:\BaiduSyncdisk\Blender Foundation\Blender\3.6"
*上述意思就是用3.1文件夹骗自己电脑是3.6
mklink /J "C:\Users\Administrator\AppData\Roaming\Blender Foundation" "E:\BaiduSyncdisk\Blender Foundation"
mklink /J "C:\Users\Admin\AppData\Roaming\Blender Foundation" "D:\BaiduSyncdisk\Blender Foundation"
 
mklink /J "D:\BaiduSyncdisk\Blender Foundation\Blender\4.0" "D:\BaiduSyncdisk\Blender Foundation\Blender\4.1"
两台电脑同步同理（需要网盘）
##### 3系列以3.6为准，4系列以4.1为准
家里的电脑 c盘admin是专为bl的软链接，administrator里也有一个（有时候admin和adminstrator搞混了所以这样


### MD（一切柔体模拟
善用布料穿插和缝线，简单的操作好的效果

把md当做模型布料渲染器,前提是uv必须展好
1.Autorig比较简单，应用缩放后点击go，然后到蒙皮点击绑定即可
2.调好动作，存好姿态资产
3.分别以obj格式导出为动作0和1
4.MD导入动作0（作为虚拟模特导入），导入动作1（作为morph target导入）

md可以选择边，然后右键对称联动板片，也可以选择边右键取消联动
同时可以选择两个面片，右键设为联动板片
冷冻功能适合多层衣服，本质就是把衣服变成网格，很常用，可以避免出错（但无法完全避免
导出之前右键 重置网格 或者 四边面 都可以

不想要衣服之间的互相影响的时候：可以选择影响别人的板片，反激活它们
想要衣服之间互相影响：选择板片（上层的），在属性中设置为层2

拓扑分面
5＞3＞1＞2＞4

Cursor安装插件命令
cursor --install-extension D:\BaiduSyncdisk\DyVault\Notes\Scripts\Coding_Cursor2GPT\coding-cursor2gpt-0.0.1.vsix
Vscode安装插件命令
code --install-extension D:\BaiduSyncdisk\DyVault\Notes\Scripts\Coding_Cursor2GPT\coding-cursor2gpt-0.0.1.vsix