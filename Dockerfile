FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "--app", "app","run",  "--host=0.0.0.0"]

