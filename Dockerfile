FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY ./ .
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]