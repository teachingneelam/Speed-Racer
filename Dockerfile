FROM python:3.12.5
WORKDIR D:\vs workspace\car-racing\Speed-Racer
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["python", "main.py"]

