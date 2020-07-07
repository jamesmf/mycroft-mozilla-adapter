"""TP-Link adapter for Mozilla WebThings Gateway."""
import socket
from gateway_addon import Adapter, Database
from .mycroft_device import MycroftDevice

_TIMEOUT = 3


class MycroftAdapter(Adapter):
    """Adapter for the Mycroft Assistant. For more information, visit mycroft.ai"""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self, "mycroft-adapter", "mycroft-adapter", verbose=verbose)

        self.pairing = False
        self.device_ip = None
        self.start_pairing(_TIMEOUT)

    def _add_from_config(self):
        """Attempt to get the ip of the Mycroft."""
        database = Database("mycroft-adapter")
        if not database.open():
            return

        config = database.load_config()
        database.close()

        if not config or "devicename" not in config:
            return

        try:
            mycroft_device_name = config["devicename"]
            print(mycroft_device_name)
            mycroft_ip = socket.gethostbyname(mycroft_device_name)
            self.device_ip = mycroft_ip
        except (OSError, UnboundLocalError, socket.gaierror) as e:
            print("Failed to connect to {}: {}".format(str(mycroft_device_name), e))

        if self.device_ip:
            self.device_ref = MycroftDevice(self, "mycroft-id123")

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

        self.handle_device_added(self.device_ref)

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
