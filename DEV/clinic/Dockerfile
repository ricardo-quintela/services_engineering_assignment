FROM python:3.11

# Copying backend files
COPY . .
RUN pip install --no-cache-dir -r requirements.txt &&\
    python manage.py makemigrations clinic authentication &&\
    python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
