const vscode = require('vscode');

async function activate(context) {
    // 动态加载 open 包
    let open;
    try {
        open = await import('open');
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to load open package: ${error.message}`);
        return;
    }

    let disposable = vscode.commands.registerCommand('coding-cursor2gpt.sendToChatGPT', async () => {
        try {
            // 获取当前编辑器
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage('No active editor found!');
                return;
            }

            // 获取全部代码
            const document = editor.document;
            const code = document.getText();

            // 创建组合内容：代码 + 文案
            const contentToClipboard = `${code}\n\n帮我修复bug 精炼回答`;

            // 复制到剪贴板
            await vscode.env.clipboard.writeText(contentToClipboard);

            // 打开 ChatGPT 网页
            await open.default('https://chatgpt.com/', {
                app: { name: 'chrome' },
                newInstance: true
            });

            vscode.window.showInformationMessage('Code copied to clipboard and ChatGPT opened!');

        } catch (error) {
            vscode.window.showErrorMessage(`Error: ${error.message}`);
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };