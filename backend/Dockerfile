FROM python:3.11-slim

WORKDIR /backend

COPY backend/ .

RUN pip install --no-cache-dir -r requirements.txt

COPY run.py /run.py

EXPOSE 8000

CMD ["python", "/run.py"]
