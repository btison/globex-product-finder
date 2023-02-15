FROM registry.access.redhat.com/ubi8/python-39:1-97

USER 0

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app-src /app
COPY ./models /models
RUN chown -R 1001:0 /app && \
    chown -R 1001:0 /models

WORKDIR /app/

ENV PYTHONPATH=/app

USER 1001

CMD gunicorn -w 1 --threads 4 -b 0.0.0.0 'wsgi:application'