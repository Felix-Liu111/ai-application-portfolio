FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# 使用阿里云 PyPI 镜像（稳定不超时）
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]