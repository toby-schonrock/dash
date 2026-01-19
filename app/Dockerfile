FROM python:3-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

RUN chmod +x entrypoint.sh

RUN useradd app
USER app

CMD ["./entrypoint.sh"]