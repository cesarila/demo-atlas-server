FROM cesarila/python:sha-cdeef3e

USER root
RUN apt-get update && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*
USER nobody

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /opt/demo-atlas

# Install production dependencies.
COPY --chown=nobody requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY --chown=nobody app app
COPY --chown=nobody migrations migrations
COPY --chown=nobody demoAtlas.py config.py boot.sh dbUtils.py globals.py setup.cfg setup.py /opt/demo-atlas/
RUN chmod +x boot.sh

EXPOSE 5000
ENTRYPOINT ["/opt/demo-atlas/boot.sh"]