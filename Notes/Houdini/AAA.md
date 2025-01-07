>编辑资产参数思路:主电缆 副电缆 模拟(优化)
![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-12-09-13-50-12.png)


![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-12-05-13-16-56.png)
![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-12-05-13-17-28.png)

>螺旋线制作方法 扭转扫描
![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-12-05-12-38-02.png)


叉乘前normalize记得


>程序化切割平面(xz平面)
![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-10-06-14-20-40.png)
>addprim使用过程:
![](d:/BaiduSyncdisk/DyVault/Notes/Houdini/images/2024-10-06-01-15-02.png)


>用循环: 逐个处理、复杂逻辑、动态生成。
不用循环: 统一操作、内置函数批量处理。



| 属性  | 数据类型 | 单位         | 特点                          |
|-------|----------|--------------|-------------------------------|
| Age   | float    | 秒（seconds）| 表示粒子当前生命时间，随时间增加。 |
| Life  | float    | 秒（seconds）| 表示粒子的最大生命期，决定粒子存活时间。 |
| Time  | float    | 秒（seconds）| 表示场景的全局时间，从开始到当前帧的时间。 |

>粒子life experiency默认以秒为单位
popvop需要手动选取input

fields ≈ attribute

>![alt text](./images/image-18.png)
*使用popfluid将粒子转换为流体    **粒子流→液态粒子流**


>![alt text](./images/image-19.png)
*接上图  **液态粒子流→液态网格**




>![alt text](./images/image-17.png)
 *这里的星号是乘（）是判断*


>![alt text](./images/image-16.png)
*dop网络最核心的结构



houdini导出给引擎需要**transform*50**


![alt text](img_v3_02el_06f1c127-b65e-40f4-8416-82db671bca0g.jpg)


![alt text](./images/image-15.png)
*blender导入houdini设置*


![alt text](./images/image-1.png)
*sdf自带surface属性，fog自带density属性，polygon构成了mesh*

> ### houdini的大体思路：加减法控制变量➡乘法控制强度➡循环条件控制生长
> #### fit 中的src max一般就是控制range的（spread）

![alt text](./images/image-3.png)
*vdb需要是封闭的网格否则出错*

>![alt text](./images/image-4.png)
*sdf可理解为距离vdb 而密度vdb就是云*

![alt text](./images/image-5.png)
![alt text](./images/image-6.png)
![alt text](./images/image-7.png)
*方向覆盖（雪花，尘土等）原理如此简单：通过筛选法线角度 来指定Group*

set()用来定义向量（可以是二维或者三维）
类似python中的元组和列表（列表可变，元组不可变）

>![alt text](./images/image-8.png)
*属性随机化 和法定变量搭配使用*

![alt text](./images/image-9.png)
*vertex和point的区别，前者更加底层*


>![alt text](./images/image-10.png)
*捕捉顶点组区域*

顶点组原理就是通过emu给了几何数据一个新的属性（布尔值属性）
#### 用houdini做粒子一定要做的立体，否则不如直接用材质解决

![alt text](./images/image-11.png)

![alt text](./images/image-12.png)
*注：Scatter只能读取面组，所以需要搭配grouppromote（转换点组为面组）来使用*

>![alt text](./images/image-13.png)
attribute属性就是编程中的变量如：p（xyz）index等等
enumerat遍历（也有说枚举的）总之就是可以给点添加编号

>![alt text](./images/image-14.png)
绿色为重点

