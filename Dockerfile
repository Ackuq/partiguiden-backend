FROM python:3.11.0

# Set working dir
RUN mkdir -p /usr/src/partiguiden-backend
WORKDIR /usr/src/partiguiden-backend

# Copy application code
COPY . /usr/src/partiguiden-backend

# Project initialization:
RUN pip install -r requirements.txt
