FROM python:3.8.1

# Get pipenv
RUN pip install pipenv

# Set working dir
RUN mkdir -p /usr/src/partiguiden-backend
WORKDIR /usr/src/partiguiden-backend

RUN pipenv install

# Copy application code
COPY . /usr/src/partiguiden-backend
