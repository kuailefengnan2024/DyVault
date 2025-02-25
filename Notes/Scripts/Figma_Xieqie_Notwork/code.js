// code.js
figma.showUI(__html__, { width: 300, height: 200 });

// 存储当前选中的文本图层和相关蒙版
let selectedTextNodes = [];

figma.ui.onmessage = async (msg) => {
  const selectedNodes = figma.currentPage.selection;

  // 如果没有选中任何图层，提示用户
  if (selectedNodes.length === 0) {
    figma.notify("请先选择一个文本图层！");
    console.error("No selection found.");
    return;
  }

  // 确保只处理文本图层
  const textNodes = selectedNodes.filter(node => node.type === 'TEXT');
  if (textNodes.length === 0) {
    figma.notify("请选择一个文本图层！当前选择的对象不是文本。");
    console.error("Selected nodes are not TEXT type:", selectedNodes.map(n => n.type));
    return;
  }

  try {
    if (msg.pluginMessage.type === 'update-skew') {
      const { horizontal } = msg.pluginMessage;

      for (const node of textNodes) {
        // 提示用户：使用蒙版模拟倾斜，原始文本保持可编辑
        figma.notify("即将使用蒙版模拟倾斜，原始文本保持可编辑。");

        // 获取文本的边界框
        const bounds = node.absoluteRenderBounds;
        if (!bounds) {
          figma.notify("无法获取文本边界，请重试！");
          console.error("Failed to get bounds for text node:", node);
          return;
        }

        // 创建一个矩形作为蒙版
        const mask = figma.createRectangle();
        mask.x = bounds.x;
        mask.y = bounds.y;
        mask.resize(bounds.width, bounds.height);

        // 应用水平倾斜到矩形蒙版
        const transform = [
          1, 0, // 垂直保持不变（b = 0）
          Math.tan(horizontal * Math.PI / 180), 1, // 水平倾斜（c）
          0, 0 // 平移
        ];
        mask.relativeTransform = transform;

        // 将文本设置为蒙版的填充（裁剪模式）
        mask.fills = [{ type: 'IMAGE', imageHash: '', scaleMode: 'FIT' }]; // 占位，避免报错
        node.clipsContent = true; // 启用裁剪
        mask.clipsContent = true; // 确保蒙版裁剪文本

        // 创建组，将文本和蒙版组合
        const group = figma.group([node, mask], figma.currentPage);
        group.name = `${node.name} (倾斜组)`;

        // 保持原始文本选中
        figma.currentPage.selection = [node];
        console.log("Applied mask transform:", mask.relativeTransform);
      }
    } else if (msg.pluginMessage.type === 'reset-skew') {
      for (const node of textNodes) {
        // 查找并重置所有以 "(倾斜组)" 结尾的组
        const groups = figma.currentPage.children.filter(child => child.name.endsWith("(倾斜组)"));
        for (const group of groups) {
          if (group.type === 'GROUP') {
            // 重置蒙版的变换
            const mask = group.children.find(child => child.type === 'RECTANGLE');
            if (mask) {
              mask.relativeTransform = [
                1, 0,
                0, 1,
                0, 0
              ];
            }
          }
        }
      }
      figma.notify("倾斜已重置。");
    } else if (msg.pluginMessage.type === 'apply-skew') {
      // 确认当前是否有倾斜组
      const skewedGroups = figma.currentPage.children.filter(child => child.name.endsWith("(倾斜组)") && child.type === 'GROUP');
      for (const group of skewedGroups) {
        const mask = group.children.find(child => child.type === 'RECTANGLE');
        if (mask && mask.relativeTransform[2] !== 0) {
          figma.notify("倾斜效果已成功应用！");
        } else {
          figma.notify("当前无倾斜效果，请先调整角度！");
          return;
        }
      }
      // 关闭插件
      figma.closePlugin();
    }
  } catch (error) {
    figma.notify("插件运行出错，请检查控制台日志。");
    console.error("Plugin error:", error);
  }
};

// 插件加载时初始化选中的文本图层
selectedTextNodes = figma.currentPage.selection.filter(node => node.type === 'TEXT');