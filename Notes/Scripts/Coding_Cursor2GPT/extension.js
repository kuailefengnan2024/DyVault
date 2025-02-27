const vscode = require('vscode');
const open = require('open'); // 假设 open 包已经正确安装

async function activate(context) {
    // 定义功能函数
    async function sendToChatGPT() {
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
            const contentToClipboard = `${code}\n\n帮我修复bug 你给我的回复不需要包含任何其他内容 只给出修复后的代码,解释应该包含在代码注释中`;

            // 复制到剪贴板
            await vscode.env.clipboard.writeText(contentToClipboard);

            // 打开 ChatGPT 网页
            // await open('https://chatgpt.com/', {
            //     app: { name: 'chrome' },
            //     newInstance: true
            // });
            // 打开 https://grok.com/ 网页
            await open('https://grok.com/', {
                app: { name: 'chrome' },
                newInstance: true
            });

            vscode.window.showInformationMessage('Code copied to clipboard and ChatGPT opened!');
        } catch (error) {
            vscode.window.showErrorMessage(`Error: ${error.message}`);
        }
    }

    // 注册命令
    let disposable = vscode.commands.registerCommand('coding-cursor2gpt.sendToChatGPT', sendToChatGPT);
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
