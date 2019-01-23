ARG PYTHON_TAG
FROM python:${PYTHON_TAG}-alpine

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && pip install -r /requirements.txt

COPY app/ /app
WORKDIR /app

VOLUME [ "/data" ]

ENTRYPOINT ["python", "app.py"]
CMD ["-h"]
# CMD ["/bin/sh"]
