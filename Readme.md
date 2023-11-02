# RFID tag reader

```
sudo pigpiod
sudo python3 read-rfid-tags.py 
```

# Install services

## Tag reader

    sudo cp tag-reader.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable tag-reader
    sudo systemctl start tag-reader

## MQTT tag listener

    sudo cp mqtt-tag-listener.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable mqtt-tag-listener
    sudo systemctl start mqtt-tag-listener

