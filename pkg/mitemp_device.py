"""Xiaomi adapter for WebThings Gateway."""

from gateway_addon import Device, Property
import asyncio
import time
import bluepy.btle
import struct
from typing import List

from .util import print


_POLL_INTERVAL = 120


class MiTempSensorDevice(Device):
    """Xiaomi smart bulb type."""

    def __init__(self, adapter, _id, mac: str, loop: asyncio.BaseEventLoop = None):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        """
        self.properties: List[Property]

        super().__init__(adapter, _id)

        self._type = ['TemperatureSensor', 'HumiditySensor']
        self.name = 'Mi Temp Sensor'
        self.description = 'Xiaomi Bluetooth Temperature and Humidity Sensor'

        self.mac = mac

        # # bluepy stuff
        print(f'WIP: new {self.mac} device')

        try:
            pp = bluepy.btle.Peripheral(self.mac)

            # read battery level
            battery, = struct.unpack('<B', pp.readCharacteristic(27))

            # read sensor data
            temperature, humidity, voltage = struct.unpack('<HBH', pp.readCharacteristic(54))

        except bluepy.btle.BTLEDisconnectError as err:
            print(f'Error during poll: {err}')
            self.name = 'Invalid MiTemp'
            return

        finally:
            if pp:
                pp.disconnect()
            time.sleep(5)

        print(f'get Temperature {temperature / 100} C')
        print(f'get Humidity {humidity}%')
        print(f'get Voltage {voltage / 1000} V')
        print(f'get Battery {battery}%')

        self.properties['temperature'] = Property(
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
                'description': 'The ambient temperature'
            },
        )
        self.properties['temperature'].set_cached_value(temperature / 100)

        self.properties['humidity'] = Property(
            self,
            'humidity',
            {
                'type': 'integer',
                '@type': 'HumidityProperty',
                'minimum': 0,
                'maximum': 100,
                'unit': 'percent',
                'title': 'Humidity',
                'description': 'The relative humidity',
                'readOnly': True
            }
        )
        self.properties['humidity'].set_cached_value(humidity)

        self.properties['voltage'] = Property(
            self,
            'voltage',
            {
                '@type': 'VoltageProperty',
                'title': 'Voltage',
                'type': 'number',
                'unit': 'volt',
                'multipleOf': 0.001,
            },
        )
        self.properties['voltage'].set_cached_value(voltage / 1000)

        self.properties['battery'] = Property(
            self,
            'battery',
            {
                'type': 'integer',
                'unit': 'percent',
                'title': 'Battery',
                'description': 'Current battery level',
                'readOnly': True
            },
        )
        self.properties['battery'].set_cached_value(battery)

        if loop:
            self.update_task = asyncio.run_coroutine_threadsafe(self.poll(), loop)

    def _fix_and_set_property_value(self, _property: str, value: str) -> None:
        """
        Set the current value of a property.

        property -- the property name
        value -- the value to set
        """
        prop = self.properties[_property]

        if prop.description.get('minimum'):
            value = max(prop.description.get('minimum'), value)

        if prop.description.get('maximum'):
            value = min(prop.description.get('maximum'), value)

        if 'enum' in prop.description and len(prop.description['enum']) > 0 and value not in prop.description['enum']:
            raise PropertyError('Invalid enum value')

        prop.set_cached_value_and_notify(value)

    async def poll(self):
        """Poll the device for changes."""
        while True:
            print(f'MITEMP: wait 120s and update {self.mac} properties')
            await asyncio.sleep(_POLL_INTERVAL)

            pp = None
            try:
                # # bluepy stuff
                pp = bluepy.btle.Peripheral(self.mac)

                # read battery level
                handle = 27
                print(f'handle {handle} {self.mac}')
                pp._writeCmd("rd %X\n" % handle)
                resp = pp._getResp('rd', timeout=60)
                if resp is None:
                    print(f'timeout {handle} {self.mac}')
                    continue
                battery, = struct.unpack('<B', resp['d'][0])
                print(f'done {handle} {self.mac}')

                # read sensor data
                handle = 54
                print(f'handle {handle} {self.mac}')
                pp._writeCmd("rd %X\n" % handle)
                resp = pp._getResp('rd', timeout=60)
                if resp is None:
                    print(f'timeout {handle} {self.mac}')
                    continue
                temperature, humidity, voltage = struct.unpack('<HBH', resp['d'][0])
                print(f'done {handle} {self.mac}')

                print(f'get Temperature {temperature / 100} C')
                self._fix_and_set_property_value('temperature', temperature / 100)

                print(f'get Humidity {humidity}%')
                self._fix_and_set_property_value('humidity', humidity)

                print(f'get Voltage {voltage / 1000} V')
                self._fix_and_set_property_value('voltage', voltage / 1000)

                print(f'get Battery {battery} %')
                self._fix_and_set_property_value('battery', battery)

            except bluepy.btle.BTLEDisconnectError as err:
                print(f'Error during poll: {err}')
                time.sleep(15)

            except Exception as err:
                print(f'Unknown Error during poll: {err}')

            finally:
                if pp:
                    pp.disconnect()
                time.sleep(5)
