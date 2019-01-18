FROM opencv:4.0.0

RUN pip install imutils paho-mqtt

WORKDIR /app
