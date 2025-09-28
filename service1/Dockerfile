FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV VSTORAGE_PATH=/data/vstorage
ENV STORAGE_URL=http://storage:8080

EXPOSE 8199
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8199"]
