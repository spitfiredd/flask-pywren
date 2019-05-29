FROM python:3.7-slim
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
ENV FLASK_APP='app.run' \
    FLASK_ENV='development'

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--no-reload"]
