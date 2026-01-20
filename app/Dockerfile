FROM python:3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8050

COPY . .

RUN chmod +x entrypoint.sh

RUN useradd app
USER app

CMD ["./entrypoint.sh"]