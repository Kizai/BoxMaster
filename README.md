# BoxMaster
根据输入的产品规格和渠道选择，自动生成最佳的货物配货方案。

## 目录

- [BoxMaster](#boxmaster)
  - [目录](#目录)
  - [项目介绍](#项目介绍)
    - [特性](#特性)
    - [项目结构](#项目结构)
  - [运行环境](#运行环境)
  - [安装与运行](#安装与运行)
    - [1. 克隆项目](#1-克隆项目)
    - [2. 安装依赖](#2-安装依赖)
    - [3. 运行项目](#3-运行项目)
  - [Docker 打包与部署](#docker-打包与部署)
    - [1. 构建 Docker 镜像](#1-构建-docker-镜像)
    - [2. 运行 Docker 容器](#2-运行-docker-容器)
    - [3. 推送到 Docker Hub](#3-推送到-docker-hub)
  - [使用方法](#使用方法)
    - [提交 Issue](#提交-issue)
    - [提交 Pull Request](#提交-pull-request)
  - [许可证](#许可证)

## 项目介绍

优化货物配载、物流方案、Gradio 界面展示等] 的应用。它可以根据用户输入的数据自动生成最佳方案，并提供便捷的界面交互。

### 特性

- **自动化**：根据输入条件计算最佳方案，简化用户操作。
- **直观界面**：采用 Gradio 提供友好的用户界面。
- **多渠道支持**：支持多种物流渠道的配置和调整。

### 项目结构

```plaintext
/Boxmaster
│
├── main.py        # 主程序文件
├── requirements.txt      # Python 依赖列表
├── Dockerfile            # Dockerfile 文件
└── temp
    └── temp.xlsx         # 模板文件
```

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
docker build -t john_doe/boxmaster:v1.0 .
```

### 2. 运行 Docker 容器

构建完成后，可以使用以下命令启动 Docker 容器：

```bash
docker run -d -p 7860:7860 your_username/boxmaster:tag
```

例如：

```bash
docker run -d -p 7860:7860 kizai/boxmaster:v1.0
```

### 3. 推送到 Docker Hub

将镜像推送到 Docker Hub：

```bash
docker push your_username/boxmaster:tag
```

例如：

```bash
docker push kizai/boxmaster:v1.0
```

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

该项目采用 [MIT 许可证](LICENSE) 开源，欢迎自由使用和分发。
```