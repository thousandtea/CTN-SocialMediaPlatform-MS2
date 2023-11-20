# 使用官方 Python 镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器中
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 安装 gunicorn
RUN pip install gunicorn

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
