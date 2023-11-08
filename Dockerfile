FROM python:3.9-slim
ADD dl_image.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./dl_image.py"] 