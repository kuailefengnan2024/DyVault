/**
 * 随机分布图案 - Illustrator插件
 * 创建并随机分布线条和圆球组成的图案
 */

// 主要函数
function createDistributedPattern() {
    // 创建对话框UI
    var dialog = new Window("dialog", "随机分布图案生成器");
    dialog.orientation = "column";
    dialog.alignChildren = "fill";
    
    // 图案设置组
    var patternGroup = dialog.add("panel", undefined, "基本图案设置");
    patternGroup.orientation = "column";
    patternGroup.alignChildren = "left";
    
    // 线条长度
    var lineGroup = patternGroup.add("group");
    lineGroup.add("statictext", undefined, "线条长度(pt):");
    var lineLength = lineGroup.add("edittext", undefined, "50");
    lineLength.characters = 5;
    
    // 线条粗细
    var strokeGroup = patternGroup.add("group");
    strokeGroup.add("statictext", undefined, "线条粗细(pt):");
    var strokeWeight = strokeGroup.add("edittext", undefined, "1");
    strokeWeight.characters = 5;
    
    // 圆球大小
    var circleGroup = patternGroup.add("group");
    circleGroup.add("statictext", undefined, "圆球大小(pt):");
    var circleSize = circleGroup.add("edittext", undefined, "5");
    circleSize.characters = 5;
    
    // 分布设置组
    var distributionGroup = dialog.add("panel", undefined, "分布设置");
    distributionGroup.orientation = "column";
    distributionGroup.alignChildren = "left";
    
    // 图案数量
    var countGroup = distributionGroup.add("group");
    countGroup.add("statictext", undefined, "图案数量:");
    var patternCount = countGroup.add("edittext", undefined, "100");
    patternCount.characters = 5;
    
    // 随机长度变化
    var randomGroup = distributionGroup.add("group");
    randomGroup.add("statictext", undefined, "长度随机变化(%):");
    var lengthVariation = randomGroup.add("edittext", undefined, "30");
    lengthVariation.characters = 5;
    
    // 随机旋转角度
    var rotateGroup = distributionGroup.add("group");
    var allowRotation = rotateGroup.add("checkbox", undefined, "允许随机旋转");
    allowRotation.value = false; // 默认不旋转
    
    // 按钮组
    var btnGroup = dialog.add("group");
    btnGroup.alignment = "center";
    var okBtn = btnGroup.add("button", undefined, "确定", {name: "ok"});
    var cancelBtn = btnGroup.add("button", undefined, "取消", {name: "cancel"});
    
    // 显示对话框
    if (dialog.show() == 1) {
        // 用户点击确定，获取输入值
        var baseLineLength = parseFloat(lineLength.text);
        var baseStrokeWeight = parseFloat(strokeWeight.text);
        var baseCircleSize = parseFloat(circleSize.text);
        var count = parseInt(patternCount.text);
        var variation = parseFloat(lengthVariation.text) / 100; // 转换为小数
        var rotate = allowRotation.value;
        
        // 创建图案
        createPatterns(baseLineLength, baseStrokeWeight, baseCircleSize, 
                     count, variation, rotate);
    }
}

// 创建并分布图案
function createPatterns(lineLength, strokeWeight, circleSize, count, variation, allowRotate) {
    // 获取活动文档，如果没有则创建新文档
    var doc;
    if (app.documents.length > 0) {
        doc = app.activeDocument;
    } else {
        doc = app.documents.add(DocumentColorSpace.RGB, 2000, 2000);
    }
    
    // 创建图层
    var patternLayer = doc.layers.add();
    patternLayer.name = "随机图案";
    
    // 创建多个图案
    for (var i = 0; i < count; i++) {
        // 计算随机长度
        var actualLength = lineLength * (1 - variation + Math.random() * 2 * variation);
        
        // 创建组来容纳线条和圆球
        var patternGroup = patternLayer.groupItems.add();
        
        // 创建线条
        var line = patternGroup.pathItems.add();
        line.stroked = true;
        line.strokeWidth = strokeWeight;
        line.strokeColor = new RGBColor();
        line.strokeColor.red = 0;
        line.strokeColor.green = 0;
        line.strokeColor.blue = 0;
        line.filled = false;
        
        // 设置线条点
        line.setEntirePath([
            [0, 0],
            [actualLength, 0]
        ]);
        
        // 创建圆球 - 修复错误部分
        var circle = patternGroup.pathItems.add();
        circle.filled = true;
        circle.stroked = false;
        circle.fillColor = new RGBColor();
        circle.fillColor.red = 0;
        circle.fillColor.green = 0;
        circle.fillColor.blue = 0;
        
        // 在线条末端创建圆球，使用正确的椭圆创建方法
        var radius = circleSize / 2;
        var centerX = actualLength;
        var centerY = 0;
        
        // 创建圆形路径
        var top = centerY + radius;
        var left = centerX - radius;
        var right = centerX + radius;
        var bottom = centerY - radius;
        
        circle.entirePath = [
            [left, top],
            [right, top],
            [right, bottom],
            [left, bottom]
        ];
        
        // 将矩形路径转换为椭圆
        circle.closed = true;
        try {
            circle.roundCorners(radius);
        } catch(e) {
            // 如果roundCorners不可用，我们将使用替代方法创建圆形
            createCircleAlternative(patternGroup, centerX, centerY, radius);
            circle.remove(); // 删除原始路径
        }
        
        // 随机位置
        var posX = Math.random() * (2000 - actualLength - circleSize);
        var posY = Math.random() * (2000 - circleSize);
        
        // 随机旋转（如果允许）
        var angle = 0;
        if (allowRotate) {
            angle = Math.random() * 360;
        }
        
        // 应用变换
        patternGroup.left = posX;
        patternGroup.top = posY;
        patternGroup.rotate(angle);
    }
    
    // 提示完成
    alert("已成功创建 " + count + " 个随机图案!");
}

// 替代方法创建圆形
function createCircleAlternative(parent, centerX, centerY, radius) {
    var circle = parent.pathItems.ellipse(
        centerY + radius,  // top
        centerX - radius,  // left
        radius * 2,        // width
        radius * 2,        // height
        false,             // reversed
        false              // inscribed
    );
    
    circle.filled = true;
    circle.stroked = false;
    circle.fillColor = new RGBColor();
    circle.fillColor.red = 0;
    circle.fillColor.green = 0;
    circle.fillColor.blue = 0;
    
    return circle;
}

// 注册脚本到Illustrator菜单
try {
    // 创建菜单项
    var menuItem = app.scriptMenuActions.add("随机分布图案工具");
    menuItem.addEventListener('onSelect', createDistributedPattern);
    
    // 检查是否是作为扩展运行
    if (typeof module !== 'undefined' && module.constructor.name === 'Object') {
        // 导出主函数以便扩展使用
        module.exports = {
            createDistributedPattern: createDistributedPattern
        };
    }
} catch (e) {
    // 如果直接运行脚本，则直接启动
    createDistributedPattern();
}