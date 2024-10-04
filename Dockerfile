FROM python:3.12.0-slim
WORKDIR /app
COPY . /app
RUN pip install pandas
RUN pip install pygame
RUN pip install -r requirements.txt
EXPOSE 8002

CMD ["python", "main.py"]
~                                                                                                                       ~           
