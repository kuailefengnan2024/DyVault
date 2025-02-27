const { commands, window, Selection, Clipboard } = require("@raycast/api");

function activate(context) {
  console.log("插件激活成功");

  // 注册命令
  let disposable = commands.registerCommand('cursor-ai-plugin.openChatGPT', async () => {
    console.log("执行 Open ChatGPT with Code 命令");
    const selection = await Selection.get();
    
    if (!selection || !selection.text) {
      window.showErrorMessage("请先选中代码");
      return;
    }

    const defaultText = "\n\n帮我附加中文注释助我理解 并debug 回复仅包含代码即可";
    const textToCopy = selection.text + defaultText;
    
    await Clipboard.copy(textToCopy);
    console.log("已复制到剪贴板:", textToCopy);

    await window.openUrl("https://chatgpt.com");
    console.log("已打开 ChatGPT 页面");
  });

  context.subscriptions.push(disposable);
}

function deactivate() {
  console.log("插件已停用");
}

module.exports = {
  activate,
  deactivate
};