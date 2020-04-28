FROM python:3.7-alpine AS compile-image

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /bookstore

COPY ./src /bookstore/src

ENV PYTHONPATH=/bookstore/src

CMD ["python", "/bookstore/src/routes.py"]
