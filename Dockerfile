FROM python:latest

WORKDIR /app
COPY . /app
EXPOSE 8000

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /static
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]