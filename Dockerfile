FROM python:3.12.5
WORKDIR /D/workspace/car-app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y
EXPOSE 8002
ENV carenv
CMD ["python", "main.py"]

