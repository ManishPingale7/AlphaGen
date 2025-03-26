FROM python:3.11-slim

WORKDIR /app

# Create a writable temporary directory
RUN mkdir -p /writable-tmp && chmod 777 /writable-tmp
ENV TMPDIR=/writable-tmp

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
