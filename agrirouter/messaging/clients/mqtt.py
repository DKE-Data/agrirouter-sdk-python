from typing import Any, List, Tuple

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv31, MQTTMessageInfo


class MqttClient:

    def __init__(self,
                 client_id: str = "",
                 on_message_callback: callable = None,
                 userdata: Any = None,
                 clean_session: bool = True
                 ):
        # TODO: Implement on_message_callback parameter validation:
        #  must take params as described at https://pypi.org/project/paho-mqtt/#callbacks

        self.mqtt_client = mqtt_client.Client(
            client_id=client_id,
            clean_session=clean_session,
            userdata=userdata,
            protocol=MQTTv31,
            transport="tcp"
        )
        self.mqtt_client.on_message = on_message_callback if on_message_callback else self._get_on_message_callback()
        self.mqtt_client.on_connect = self._get_on_connect_callback()
        self.mqtt_client.on_disconnect = self._get_on_disconnect_callback()
        self.mqtt_client.on_subscribe = self._get_on_subscribe_callback()
        self.mqtt_client.on_unsubscribe = self._get_on_unsubscribe_callback()

    def connect(self, host: str, port: str) -> None:
        self.mqtt_client.connect_async(
            host=host,
            port=port
        )
        self.mqtt_client.loop_start()

    def disconnect(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def publish(self, topic, payload, qos=0) -> MQTTMessageInfo:
        """

        :param topic: str representing unique name of the topic that the message should be published on
        :param payload: The actual message to send
        :param qos: int representing the quality of service level to use. May be [0, 1, 2]
        :return: MQTTMessageInfo
        """
        message_info = self.mqtt_client.publish(
            topic=topic,
            payload=payload,
            qos=qos
        )
        return message_info

    def subscribe(self, topics: List[Tuple[str, int]]) -> tuple:
        """

        :param topics: list of tuples [(topic, qos),] containing topic to subscribe on
          and desired quality of service

        topic: str representing unique name of the topic to subscribe on
        qos: int representing the quality of service level to use. May be [0, 1, 2]

        Example: topics=[('my/topic/1', 0), ('my/topic/2', 1), ('my/topic/3', 2)]

        :return: tuple
        """
        result, mid = self.mqtt_client.subscribe(topics)
        return result, mid

    def unsubscribe(self, topics: List[str]) -> tuple:
        """

        :param topics: list of strings [topic, topic] containing topic to unsubscribe from

        topic: str representing unique name of the topic to unsubscribe from

        Example: topics=['my/topic/1', 'my/topic/2', 'my/topic/3']

        :return: tuple
        """
        result, mid = self.mqtt_client.unsubscribe(topics)
        return result, mid

    @staticmethod
    def _get_on_connect_callback() -> callable:

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code: {rc}")

            return client, userdata, flags, rc, properties

        return on_connect

    @staticmethod
    def _get_on_message_callback() -> callable:

        def on_message(client, userdata, msg):
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            return client, userdata, msg

        return on_message

    @staticmethod
    def _get_on_subscribe_callback() -> callable:

        def on_subscribe(client, userdata, mid, granted_qos, properties=None):
            # print(f"Subscribed {userdata} to `{properties}`")

            return client, userdata, mid, granted_qos, properties

        return on_subscribe

    @staticmethod
    def _get_on_disconnect_callback() -> callable:

        def on_disconnect(client, userdata, rc):
            # print(f"Disconnected from from `{properties}`")

            return client, userdata, rc

        return on_disconnect

    @staticmethod
    def _get_on_unsubscribe_callback() -> callable:

        def on_unsubscribe(client, userdata, mid):
            # print(f"Unsubscribed `{userdata}` from `{properties}`")

            return client, userdata, mid

        return on_unsubscribe
