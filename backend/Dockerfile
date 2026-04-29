FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 拷贝依赖清单
COPY llama_cpp_python-0.3.4-cp310-cp310-linux_x86_64.whl .
# COPY zh_core_web_sm-3.8.0-py3-none-any.whl .
RUN pip install ./llama_cpp_python-0.3.4-cp310-cp310-linux_x86_64.whl
# RUN pip install ./zh_core_web_sm-3.8.0-py3-none-any.whl
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 拷贝所有代码
COPY . .

# 暴露FastAPI端口
EXPOSE 8000

# 启动神经总线
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "main.py"]