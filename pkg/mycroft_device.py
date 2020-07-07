from gateway_addon import Device, Property
import threading
import time


class MycroftDevice(Device):
    """TP-Link smart plug type."""

    def __init__(self, adapter, _id):
        """
        Initialize the object.
        adapter -- the Adapter managing this device
        _id -- ID of this device
        """
        Device.__init__(self, adapter, _id)
        self._type = ["OnOffSwitch"]
        self.poll_interval = 5

        self.description = "Mycroft device"
        self.name = "mycroft"

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

        self.properties["testproperty"] = Property(
            self,
            "testproperty",
            {"@type": "TestCase", "title": "TestMe", "type": "string"},
        )

    def poll(self):
        time.sleep(self.poll_interval)
