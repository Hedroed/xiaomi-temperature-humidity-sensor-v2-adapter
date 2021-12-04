"""Xiaomi adapter for WebThings Gateway."""

from gateway_addon import Device
import threading
import time

from .mitemp_property import MiTempProperty
from .util import print


_POLL_INTERVAL = 5


class MiTempSensorDevice(Device):
    """Xiaomi smart bulb type."""

    def __init__(self, adapter, _id, mac: str):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        """
        MiTempDevice.__init__(self, adapter, _id)

        self._type = ['TemperatureSensor', 'HumiditySensor']
        self.name = 'Mi Temp Sensor'
        self.description = 'Xiaomi Bluetooth Temperature and Humidity Sensor'

        self.mac = mac

        # # bluepy stuff
        print(f'WIP: new {self.mac} device')


        self.properties['temperature'] = MiTempProperty(
            self,
            'temperature',
            {
                '@type': 'TemperatureProperty',
                'title': 'Temperature',
                'type': 'number',
                'minimum': -127.99,
                'maximum': 127.99,
                'multipleOf': 0.01,
                'unit': 'degree celsius',
                'description': 'The ambient temperature',
                'readOnly': True
            },
            0.0
        )

        self.properties['humidity'] = MiTempProperty(
            self,
            'temperature',
            {
                'type': 'number',
                '@type': 'HumidityProperty',
                'minimum': 0,
                'maximum': 100,
                'multipleOf': 0.1,
                'unit': '%',
                'title': 'Humidity',
                'description': 'The relative humidity',
                'readOnly': True
            },
            0.0
        )

        self.properties['voltage'] = MiTempProperty(
            self,
            'voltage',
            {
                '@type': 'VoltageProperty',
                'title': 'Voltage',
                'type': 'number',
                'unit': 'volt',
                'multipleOf': 0.001,
            },
            0.0
        )

        self.properties['battery'] = MiTempProperty(
            self,
            'battery',
            {
                'type': 'integer',
                'minimum': 0,
                'maximum': 100,
                'multipleOf': 1,
                'unit': 'percent',
                'title': 'Battery',
                'description': 'Current battery level',
                'readOnly': True
            },
            100
        )

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)

            try:

                # # bluepy stuff
                print(f'WIP: update {self.mac} properties ')

            except Exception:  #TODO: better change exception catching
                continue

    @staticmethod
    def brightness(light_state):
        """
        Determine the current brightness of the light.

        light_state -- current state of the light
        """
        return int(light_state['brightness'])
