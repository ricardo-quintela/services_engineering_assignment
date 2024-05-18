FROM python:3.11

ENV EBS_HOST=localhost
ENV S3_BUCKET_URL=http://127.0.0.1:9090
ENV S3_FRONTEND_BUCKET_NAME=frontend.clinic
ENV S3_IMAGE_BUCKET_NAME=image.clinic
ENV RDS_NAME=rds.clinic
ENV RDS_HOST=backend_db
ENV RDS_PORT=5432
ENV RDS_USER=postgres
ENV RDS_PASSWORD=postgres

ENV AWS_ACCESS_KEY_ID=ASIA2UDZ7TAGR2R4BJFW
ENV AWS_SECRET_ACCESS_KEY=3osvMUaeiqwTx4HyQhltdMPAiO3txH7z4PNkmzgP
ENV AWS_DEFAULT_REGION=us-east-1

# Copying backend files
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py makemigrations clinic authentication appointments; python manage.py migrate; python manage.py runserver 0.0.0.0:8000
