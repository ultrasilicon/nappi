FROM alpine
COPY . /app
RUN apk add python3 py3-pip \
    && pip install rpi_backlight
CMD python3 /app/src/nappi-server.py
