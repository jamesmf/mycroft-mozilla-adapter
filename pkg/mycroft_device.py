from gateway_addon import Device, Property
import threading
import time
import json
import websocket


class MycroftDevice(Device):
    """Mycroft Device"""

    msg_template = '"type": "{msg_type}", "data": {msg_data_str}'

    def __init__(self, adapter, _id, message_types, device_ip):
        """
        Initialize the object.
        adapter -- the Adapter managing this device
        _id -- ID of this device,
        device_ip -- ip of the mycroft on your gateway's local network
        """
        Device.__init__(self, adapter, _id)
        self.message_types = message_types
        self._type = ["SmartSpeaker"]
        self.message = self.format_message("mozilla-iot.initialized", {})

        self.description = "Mycroft device"
        self.name = "mycroft"
        self.queue = []

        self.ws_reader = websocket.create_connection(f"ws://{device_ip}:8181/core")
        self.ws_sender = websocket.create_connection(f"ws://{device_ip}:8181/core")

        send_thread = threading.Thread(target=self.send)
        send_thread.daemon = True
        send_thread.start()

        read_thread = threading.Thread(target=self.read)
        read_thread.daemon = True
        read_thread.start()

        self.properties["testproperty"] = Property(
            self,
            "testproperty",
            {"@type": "TestCase", "title": "TestMe", "type": "string"},
        )

    def send(self):
        if self.message is not None:
            self.ws_sender.send(self.message)
            self.message = None

    def read(self):
        r = self.ws_reader.recv()
        if r in self.message_types:
            self.handle_message(r)
            self.queue.append(r)
        if len(self.queue) > 100:
            self.queue = self.queue[:100]

    def format_message(self, type_, data):
        data = json.dumps(data)
        return "{" + self.msg_template.format(msg_type=type_, msg_data_str=data) + "}"

    def handle_message(self, msg):
        print(msg)
