FROM python:3.10-slim as build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    build-essential gcc 

WORKDIR /app
RUN python -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.10-slim as app

WORKDIR /usr/app

# Copy build dependencies
COPY --from=build /app/venv ./venv
ENV PATH="/usr/app/venv/bin:$PATH"

WORKDIR /app
# Copy Application
COPY . .

CMD [ "python", "main.py" ]