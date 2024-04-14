FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "unstructured[md]"

EXPOSE 8080

ENV NAME World

CMD ["python", "main.py"]
