FROM python:3.10

WORKDIR /chat_with_ollama

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 7088

CMD ["python", "app.py"]