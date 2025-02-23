#target illustrator

function exportSelectedToSVG() {
    var doc = app.activeDocument;
    var selection = doc.selection;

    // 检查是否有选中的对象
    if (selection.length === 0) {
        alert("请先选择要导出的图案。");
        return;
    }

    // 创建一个文件夹以保存SVG文件
    var exportFolder = Folder.selectDialog("选择保存SVG文件的文件夹");
    if (exportFolder == null) {
        return; // 用户取消
    }

    // 导出每个选定的对象
    for (var i = 0; i < selection.length; i++) {
        var item = selection[i];
        var fileName = item.name ? item.name : "svg_" + (i + 1); // 使用对象名称或默认名称
        var svgFile = new File(exportFolder + "/" + fileName + ".svg");

        // 设置SVG导出选项
        var options = new ExportOptionsSVG();
        options.embedRasterImages = true; // 嵌入位图图像
        options.fontType = SVGFontType.OUTLINEFONT; // 字体类型

        // 创建一个新文档，并将选定的对象复制到新文档中
        var tempDoc = app.documents.add();
        item.duplicate(tempDoc, ElementPlacement.PLACEATEND);

        // 导出SVG
        tempDoc.exportFile(svgFile, ExportType.SVG, options);
        tempDoc.close(SaveOptions.DONOTSAVECHANGES); // 关闭临时文档
    }

    alert("导出完成！");
}

exportSelectedToSVG();