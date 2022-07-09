FROM python:3.10.5

ENV POETRY_VERSION=1.1.13

# Get pipenv
RUN pip install "poetry==$POETRY_VERSION"

# Set working dir
RUN mkdir -p /usr/src/partiguiden-backend
WORKDIR /usr/src/partiguiden-backend

# Copy application code
COPY . /usr/src/partiguiden-backend

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
