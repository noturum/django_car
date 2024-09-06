FROM python:3.12-slim
LABEL authors="nik"
EXPOSE 8000
WORKDIR /app
COPY . .
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
CMD ["/bin/sh","entrypoint.sh"]
