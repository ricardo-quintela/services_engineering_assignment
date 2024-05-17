FROM python:3.11

ENV EBS_HOST=localhost
ENV S3_BUCKET_URL=http://127.0.0.1:9090
ENV S3_BUCKET_NAME=frontend

# Copying backend files
COPY . .
RUN pip install --no-cache-dir -r requirements.txt &&\
    python manage.py makemigrations clinic authentication &&\
    python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
