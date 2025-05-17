FROM python:3.13.1-slim

WORKDIR /app

COPY . .

RUN python -m venv venv \
    && venv/bin/pip install -r req.txt

CMD ["sh", "-c", ". venv/bin/activate && python -m src.run"]