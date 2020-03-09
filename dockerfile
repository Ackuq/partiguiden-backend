FROM python:3.8.1

# Get pipenv
RUN pip install pipenv

# Set working dir
RUN mkdir -p /usr/src/partiguiden-backend
WORKDIR /usr/src/partiguiden-backend

# Install dependencies listed in requirements.txt before copying
# the entire app for better Docker caching
COPY Pipfile* /usr/src/partiguiden-backend/
RUN pipenv lock --requirements > requirements.txt && \
  pipenv lock --requirements --dev >> requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /usr/src/partiguiden-backend

# Start Django application
CMD python manage.py runserver 0.0.0.0:8000
