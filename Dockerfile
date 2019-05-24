FROM python:3.6
RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends \
    apt-utils \
  && rm -r /var/lib/apt/lists/*

ENV APP_HOME=/app

WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/. $APP_HOME/app
COPY tests/. $APP_HOME/tests

ENTRYPOINT ["python"]
