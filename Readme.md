# Idabell
![](idabell.jpg)

## Usage
Start a timer from Terminal:

    mosquitto_pub -h $MQTT_SERVER -t 'timer' -m '{"seconds":5,"title":"chickpeas"}' -u $MQTT_USER -P $MQTT_PASS
