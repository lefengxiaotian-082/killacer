markdown
# Acer 鸿基学生端进程杀手
> 一款轻量、便捷的 Windows 进程管理工具，专为快速挂起/恢复指定进程（SduEdu.exe）设计，支持热键操作和单实例运行。

## 项目介绍
### 核心功能
- 🎯 精准管理指定进程（默认：SduEdu.exe），一键挂起/恢复
- ⌨️ 全局热键支持：F1挂起、F2恢复、F3隐藏/显示窗口、F4退出
- 🔒 单实例运行保护，避免重复启动
- 🪟 置顶窗口 + 美化界面，支持深色模式
- 🚀 轻量化设计，运行无负担

### 技术栈
- 编程语言：Python 3.x
- 核心库：
  - `customtkinter`：现代化 GUI 界面
  - `psutil`：进程管理核心
  - `keyboard`：全局热键监听
  - `socket`：单实例锁实现
  - `ctypes`：Windows 窗口美化/置顶
  - `Pillow (PIL)`：图标加载（可选）

## 快速开始
### 环境要求
- 操作系统：Windows 7/10/11（仅支持 Windows）
- Python 版本：3.7 及以上
- 管理员权限（进程挂起/恢复需要）

### 安装步骤
```bash
# 1. 克隆/下载项目到本地
git clone <你的仓库地址>
cd acer-process-manager

# 2. 安装依赖包
pip install customtkinter psutil keyboard pillow
运行程序
bash
运行
# 直接运行源码
python main.py

# （可选）打包成 exe 可执行文件
pip install pyinstaller
pyinstaller -F -w -i acer.ico main.py --add-data "acer.ico;."
使用说明
基础操作
启动程序后，窗口默认置顶显示
「控制中心」标签页：
点击「挂起进程 (F1)」：暂停 SduEdu.exe 运行
点击「恢复进程 (F2)」：恢复 SduEdu.exe 运行
「关于」标签页：查看版本和热键说明
全局热键
表格
热键	功能
F1	挂起目标进程
F2	恢复目标进程
F3	隐藏 / 显示窗口
F4	强制退出程序
自定义修改
修改目标进程：修改代码中 self.target_name = "SduEdu.exe" 为你需要管理的进程名
修改热键：调整 setup_hotkeys() 方法中的热键绑定
修改端口：修改 PORT = 47201 可更改单实例锁的监听端口
注意事项
运行程序需要管理员权限，否则会提示「权限不足」
若提示 PIL 导入失败，执行 pip install pillow 即可
单实例保护：重复启动会唤醒已运行的窗口，而非新建实例
隐藏窗口后（F3），再次按 F3 或重新启动程序可恢复窗口
许可证
本项目仅供学习交流使用，请勿用于商业或非法用途。
