# 使用官方的 Python 镜像
#FROM python:3.9    build result >=1 GB
#buld result >=86 MB
FROM python:3.9-alpine
LABEL org.opencontainers.image.source="https://github.com/ZongL/makepdf"
# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用程序端口
EXPOSE 5000

# 定义启动命令
CMD ["python", "pdf_dev.py"]
