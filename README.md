#  Idiom Solver

## 项目简介
一个基于 Tkinter 的图形界面工具，用于辅助解答 Handle 游戏。用户可以输入猜测的成语，每个汉字的声母、韵母、声调均以可点击变色的格子显示，通过颜色标注反馈，系统将自动筛选并返回剩余的候选成语，同时为你推荐下一次猜测。

试试 [Handle](https://handle.antfu.me/)!

## 项目功能
- 每个成语汉字分解为：
  - 汉字
  - 声母
  - 韵母
  - 声调
- 每部分均可手动点击变色（绿色：正确；橙色：位置错误；灰色：不存在）
- 提交后智能更新推荐猜测成语（最多显示5个）
- 提交后智能更新候选成语（最多显示10个）

## 安装与运行

### 依赖
请先安装以下依赖库：

```bash
pip install pypinyin
```

### 运行方式

在主目录中，运行

```bash
python main.py
```

## 使用方法

1. 输入你猜测的成语，每个字填写在对应格子
2. 程序会自动显示拼音、声调
3. 根据 Handle 的反馈规则点击对应部分设置颜色
4. 点击“提交”，左侧会更新推荐猜测和当前可能的候选成语

## 数据来源

- data/idiom.json 来源于[chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua)
- data/idiom.txt 及 data/polypolyphones.json 来源于[handle](https://github.com/antfu/handle)

## 灵感来源

本项目的设计灵感来自 3Blue1Brown 的视频：[用信息论解 Wordle 谜题](https://www.bilibili.com/video/BV1zZ4y1k7Jw)。该视频深入浅出地讲解了如何通过信息熵最大化策略优化猜词过程，对本项目的策略实现与交互设计均提供了重要启发。
