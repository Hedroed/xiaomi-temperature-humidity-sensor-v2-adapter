# WIP
# Requirements

```
sudo apt-get install libglib2.0-dev
```

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo pip3 install git+https://github.com/WebThingsIO/gateway-addon-python.git
```

## Run in docker

```
docker run \
    -d \
    -e TZ=Europe/Paris \
    -v /webthings/data:/home/node/.mozilla-iot \
    --network="host" \
    --log-opt max-size=1m \
    --log-opt max-file=10 \
    --name webthings-gateway \
    mozillaiot/gateway:latest
```
