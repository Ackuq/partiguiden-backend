FROM python:3.10.0rc1

# Get pipenv
RUN pip install pipenv

# Set working dir
RUN mkdir -p /usr/src/partiguiden-backend
WORKDIR /usr/src/partiguiden-backend

# Copy application code
COPY . /usr/src/partiguiden-backend

RUN pipenv install
