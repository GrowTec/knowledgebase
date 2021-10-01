# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN python -m pip install poetry

# Use poetry to install dependencies
WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app

# Set poetry to NOT create a virtual environment and then install the dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the rest of the files
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
