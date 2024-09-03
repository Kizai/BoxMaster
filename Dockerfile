# 使用官方 Python 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY main.py .
COPY temp /app/temp
COPY temp/temp.xlsx /app/temp
COPY requirements.txt .

# 更换软件源为阿里云镜像源
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*


# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Gradio 的默认端口
EXPOSE 7860

# 运行 Gradio 应用
CMD ["python", "main.py"]

