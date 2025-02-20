figma.showUI(__html__, { width: 400, height: 300 });

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'convert') {
    const markdown = msg.markdown;
    createTableFromMarkdown(markdown);
  }
};

function createTableFromMarkdown(markdown) {
  // 清空当前页面上的临时节点
  figma.currentPage.children.forEach(node => {
    if (node.name === 'Markdown Table') {
      node.remove();
    }
  });

  // 分割 Markdown 为行，并过滤掉空行
  const lines = markdown.trim().split('\n').map(line => line.trim()).filter(line => line.length > 0);
  const headers = lines[0].split('|').map(h => h.trim()).filter(h => h.length > 0);
  // 只处理非空的数据行
  const rows = lines.slice(2)
    .map(row => row.split('|').map(cell => cell.trim()).filter(cell => cell.length > 0))
    .filter(row => row.length > 0); // 过滤掉空行或无效行

  const cellHeight = 89; // 每个单元格的高度
  const rowSpacing = 0; // 行间距
  const tableWidth = 630; // 主表格固定宽度

  // 创建主表格 Frame 作为容器
  const tableFrame = figma.createFrame();
  tableFrame.name = 'Markdown Table by Donyan ^_^';
  tableFrame.layoutMode = 'VERTICAL';
  tableFrame.itemSpacing = rowSpacing;
  tableFrame.paddingLeft = 0;
  tableFrame.paddingRight = 0;
  tableFrame.paddingTop = 0;
  tableFrame.paddingBottom = 0;
  tableFrame.fills = [{
    type: 'SOLID',
    color: { r: 226 / 255, g: 226 / 255, b: 226 / 255 } // #E2E2E2
  }];
  tableFrame.cornerRadius = 20; // 设置圆角

  // 计算每列的宽度（均匀分配）
  const numColumns = Math.max(headers.length, ...rows.map(row => row.length));
  const cellWidth = (tableWidth - 20 - (numColumns - 1) * 5) / numColumns; // 减去 padding 和间距

  // 创建表头行，设置背景色为 #C9C9C9
  const headerRow = createRowFrame(headers, cellWidth, cellHeight, true, numColumns, tableWidth, 20, { r: 201 / 255, g: 201 / 255, b: 201 / 255 }); // 表头背景色 #C9C9C9
  tableFrame.appendChild(headerRow);

  // 创建内容行，设置背景色为 #E2E2E2
  rows.forEach((row, rowIndex) => {
    const rowFrame = createRowFrame(row, cellWidth, cellHeight, false, numColumns, tableWidth, 16, { r: 226 / 255, g: 226 / 255, b: 226 / 255 }); // 内容行背景色 #E2E2E2
    tableFrame.appendChild(rowFrame);
  });

  // 设置主表格宽度和高度
  tableFrame.resize(
    tableWidth,
    (cellHeight + rowSpacing) * (rows.length + 1)  // 包括 padding
  );

  // 将表格添加到画布
  figma.currentPage.appendChild(tableFrame);
  figma.viewport.scrollAndZoomIntoView([tableFrame]);
}

function createRowFrame(cells, cellWidth, cellHeight, isHeader, numColumns, tableWidth, fontSize, bgColor) {
  const rowFrame = figma.createFrame();
  rowFrame.name = isHeader ? 'Header' : '';
  rowFrame.resize(tableWidth, cellHeight); // 固定宽度为 630，高度为 89
  rowFrame.fills = [{
    type: 'SOLID',
    color: bgColor // 设置背景色
  }];

  cells.forEach((cellText, colIndex) => {
    const xPosition = colIndex * (cellWidth + 5); // 手动定位
    const textNode = createTextNode(cellText, xPosition, 0, cellWidth, cellHeight, isHeader, fontSize);
    rowFrame.appendChild(textNode);
  });

  return rowFrame;
}

function createTextNode(text, x, y, width, height, isHeader, fontSize) {
  const textNode = figma.createText();
  figma.loadFontAsync({ family: 'Inter', style: 'Regular' }).then(() => {
    textNode.fontName = { family: 'Inter', style: 'Regular' };
    textNode.characters = text || '';
    textNode.resize(width - 10, height - 10); // 留出内边距
    textNode.x = x + 5; // 内边距
    textNode.y = y + 5;
    textNode.textAlignHorizontal = 'CENTER';
    textNode.textAlignVertical = 'CENTER';
    textNode.fills = [{ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }];
    textNode.fontSize = fontSize; // 根据传入的字体大小设置
  });

  return textNode;
}
