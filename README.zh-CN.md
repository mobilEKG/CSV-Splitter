# CSV Splitter：Windows 开源大文件 CSV 拆分工具

CSV Splitter 是一个免费开源的 Windows 桌面应用，可以把大型 CSV、TXT、XML 和日志文件拆分成更小的文件，方便在 Excel 和其他工具中打开、检查和分享。

[CNB 主仓库](https://cnb.cool/CodeAnt-2026/CSV-Splitter) | [GitHub 备份](https://github.com/mobilEKG/CSV-Splitter) | [English README](README.md)

[下载最新版本（CNB 主仓库）](https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest) 或使用 Python 从源代码运行。CNB 是主仓库，GitHub 仅作为备份。

## 为什么需要 CSV Splitter

Microsoft Excel 工作表最多支持 1,048,576 行。如果源文件超过这个限制，CSV Splitter 可以让你设置合适的行数，并生成带编号的输出文件。

适合以下场景：

- 在大型 CSV 文件超过 Excel 的 1,048,576 行限制前进行拆分。
- 把大型文本导出文件拆成多个带编号的小文件。
- 在每个输出文件的开头保留原始表头。
- 使用简单的 Windows 桌面界面，不必编写命令行脚本。

## 截图

![CSV Splitter 主窗口，显示文件选择、行数设置、表头选项和拆分控制](images/Screenshot.png)

## 功能

- 将 CSV、TXT、XML、日志和其他文本文件拆分成带编号的多个部分。
- 设置每个输出文件包含的数据行数。
- 选择是否将源文件表头复制到每个输出文件。
- 防止意外覆盖已有的输出文件。
- 取消耗时的行数统计或文件拆分任务。
- 使用 PyInstaller 构建独立的 Windows 可执行文件。

## Windows 下载

1. 打开 [CNB 最新版本](https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest)。
2. 下载 `CSV_Splitter_windows.exe`。
3. 运行程序并选择要拆分的文件。

## 从源代码运行

安装 Python 依赖：

```bash
pip install -r requirements.txt
```

启动图形界面：

```bash
python csv-splitter.py
```

将“每个文件的行数”设置为低于目标行数上限的值。启用“在每个部分中包含表头”后，表头会额外写入每个输出文件，不计入设置的数据行数。

## 构建 Windows 可执行文件

```bash
pyinstaller csv-splitter.py --clean --noupx --noconsole --noconfirm --onefile --windowed --icon=app_icon.ico --add-data "app_icon.ico;."
```

## 测试

安装 pytest，然后运行测试套件：

```bash
pip install pytest
pytest -q
```

## 许可证

本项目使用 MIT 许可证发布。
