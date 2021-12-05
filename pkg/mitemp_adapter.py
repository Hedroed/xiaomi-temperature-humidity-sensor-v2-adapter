"""Xiaomi adapter for WebThings Gateway."""

from gateway_addon import Adapter, Database

from .mitemp_device import MiTempSensorDevice
from .util import print

_TIMEOUT = 3


class MiTempAdapter(Adapter):
    """Adapter for Xiaomi temperature and humidity sensor devices."""

    def __init__(self, loop=None, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'xiaomi-temperature-humidity-sensor-v2-adapter',
                         'xiaomi-temperature-humidity-sensor-v2-adapter',
                         verbose=verbose)

        self.loop = loop

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def _add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('xiaomi-temperature-humidity-sensor-v2-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        print(f'WIP: loading config {config}')

        if config.get('devices') is None:
            return

        for dev in config['devices']:

            # bluepy stuff
            print(f'WIP: {dev} can be added')

            _id = f"mitemp-{dev['mac'].replace(':', '-')}"
            if _id not in self.devices:
                device = MiTempSensorDevice(self, _id, dev['mac'], loop=self.loop)

                self.handle_device_added(device)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.pairing:
            return

        self.pairing = True

        self._add_from_config()

        self.pairing = False

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
