FROM python:3.12
ENV APPLICATION_SERVICE=/app


RUN apt-get update && apt-get install -y libgl1-mesa-glx


# set work directory
RUN mkdir -p $APPLICATION_SERVICE

# where the code lives
WORKDIR $APPLICATION_SERVICE

# set environment variabless
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# copy project
COPY . $APPLICATION_SERVICE
WORKDIR $APPLICATION_SERVICE

# Expose port 8000 for the Django app
EXPOSE 8000

# Copy the entrypoint script into the container
COPY run.sh .

# Ensure the entrypoint script is executable
RUN chmod +x run.sh

# Run the entrypoint script
ENTRYPOINT ["./run.sh"]
