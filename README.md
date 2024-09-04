# BoxMaster
根据输入的产品规格和渠道选择，自动生成最佳的货物配货方案。

## 目录

- [BoxMaster](#boxmaster)
  - [目录](#目录)
  - [项目介绍](#项目介绍)
    - [特性](#特性)
    - [项目结构](#项目结构)
  - [版本更新说明](#版本更新说明)
  - [运行环境](#运行环境)
  - [安装与运行](#安装与运行)
    - [1. 克隆项目](#1-克隆项目)
    - [2. 安装依赖](#2-安装依赖)
    - [3. 运行项目](#3-运行项目)
  - [Docker 打包与部署](#docker-打包与部署)
    - [1. 构建 Docker 镜像](#1-构建-docker-镜像)
    - [2. 运行 Docker 容器](#2-运行-docker-容器)
    - [3. 推送到 Docker Hub](#3-推送到-docker-hub)
  - [测试用例](#测试用例)
    - [运行测试](#运行测试)
  - [使用方法](#使用方法)
    - [提交 Issue](#提交-issue)
    - [提交 Pull Request](#提交-pull-request)
  - [许可证](#许可证)

## 项目介绍

优化货物配载、物流方案、Gradio 界面展示等的应用。它可以根据用户输入的数据自动生成最佳方案，并提供便捷的界面交互。

### 特性

- **自动化**：根据输入条件计算最佳方案，简化用户操作。
- **直观界面**：采用 Gradio 提供友好的用户界面。
- **多渠道支持**：支持多种物流渠道的配置和调整。

### 项目结构

```plaintext
Boxmaster/
│
├── src/                       # 源代码目录
│   ├── __init__.py            # 初始化文件
│   ├── config.py              # 配置文件，包含渠道限制等常量
│   ├── utils.py               # 实用工具函数模块
│   ├── packing.py             # 主要的配货优化逻辑
│   └── app.py                 # Gradio 应用程序入口
└── temp
│   └── temp.xlsx              # 模板文件
├── tests/                     # 测试文件目录
│   ├── __init__.py            # 初始化文件
│   └── test_packing.py        # 测试文件
├── requirements.txt           # Python 依赖列表
├── main.py                    # 运行主文件
├── Dockerfile                 # Dockerfile 文件
├── .gitignore                 # git忽略更新文件
├── LICENSE                    # 开源许可证文件
└── README.md                  # 项目说明文件
```

## 版本更新说明

| 时间        | 版本号 | 版本更新说明                               |
|-------------|--------|--------------------------------------------|
| 2024-09-03  | v0.1   | 初始版本，包含基本的货物配货方案生成功能。 |
| 2024-09-04  | v0.2   | 优化项目结构，添加 Docker 支持，改进 UI。  |

## 运行环境

- Python 3.10+
- 必要的依赖列在 `requirements.txt` 中
- Docker (可选)

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/Kizai/BoxMaster.git
cd BoxMaster
```

### 2. 安装依赖

确保你已经安装了 Python 3.10 及以上版本，然后运行：

```bash
pip install -r requirements.txt
```

### 3. 运行项目

运行以下命令启动项目：

```bash
python main.py
```

## Docker 打包与部署

### 1. 构建 Docker 镜像

使用以下命令构建 Docker 镜像：

```bash
docker build -t your_username/boxmaster:tag .
```

例如：

```bash
docker build -t kizai/boxmaster:0.1 .
```

### 2. 运行 Docker 容器

构建完成后，可以使用以下命令启动 Docker 容器：

```bash
docker run -d -p 7860:7860 your_username/boxmaster:tag
```

例如：

```bash
docker run -d -p 7860:7860 kizai/boxmaster:0.1
```

### 3. 推送到 Docker Hub

将镜像推送到 Docker Hub：

```bash
docker push your_username/boxmaster:tag
```

例如：

```bash
docker push kizai/boxmaster:0.1
```

## 测试用例
为了确保项目的稳定性和功能的正确性，我们提供了一些测试用例，覆盖了常见的使用场景和边界条件。测试文件位于 tests/ 目录下，其中包含多个测试用例来验证代码的功能。

### 运行测试
你可以使用以下命令来运行所有测试用例：

```bash
python -m unittest discover -s tests
```
这将自动查找 `tests/` 目录下的所有测试文件，并执行其中的测试用例。

示例测试命令输出：

- 检查单个 SKU 的配货方案是否正确。
- 验证多 SKU 配货方案在尺寸接近限制时的表现。
- 测试超重和超规格的处理逻辑。
- 验证超重费用提示信息的正确性。

## 使用方法

1. 访问应用：在浏览器中打开 `http://localhost:7860`。
2. 根据界面提示输入数据，生成方案或结果。
3. 下载生成的文件或查看结果。

### 提交 Issue

- 请描述清楚问题，并提供必要的重现步骤。

### 提交 Pull Request

- Fork 本仓库并在你的仓库中创建新分支。
- 提交变更并推送到你的仓库。
- 提交 PR 到主仓库并描述变更内容。

## 许可证

该项目采用 [Apache-2.0 许可证](LICENSE) 开源，欢迎自由使用和分发。