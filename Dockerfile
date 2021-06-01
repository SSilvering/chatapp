# first stage
FROM python:3.8-slim AS builder
COPY requirements.txt .

# install dependencies to the local user directory (/root/.local)
RUN pip install --user -r requirements.txt

# second stage
FROM python:3.8-alpine3.11
WORKDIR /app

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /usr/local
COPY . .
RUN rm requirements.txt

# mount point for local db file
VOLUME [ "/app/app/db" ]
ENV DB_URL='sqlite:///db/app.db'

# unless otherwise noted, creates a local database
ENV SECRET_KEY="my-very-strong-secret-key"
ENV TRACK_MODIFICATIONS="False"

EXPOSE 5000

ENTRYPOINT [ "python", "./run.py" ]