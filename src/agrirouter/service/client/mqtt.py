import logging
import ssl
import time
from typing import Any, List, Tuple

import paho.mqtt.client as mqtt_client
from paho.mqtt.client import MQTTv31, MQTTMessageInfo

from agrirouter.api.constants import SYNC, ASYNC
from agrirouter.service.certification import CertificationService


class MqttClient:
    _log = logging.getLogger(__name__)

    def __init__(self,
                 onboard_response,
                 client_id: str,
                 on_message_callback: callable = None,
                 userdata: Any = None,
                 clean_session: bool = False
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
        self.mqtt_client.on_connect = self._get_on_connect_callback(onboard_response)
        self.mqtt_client.on_disconnect = self._get_on_disconnect_callback()
        self.mqtt_client.on_subscribe = self._get_on_subscribe_callback()
        self.mqtt_client.on_unsubscribe = self._get_on_unsubscribe_callback()

        certificate_file_path = CertificationService.create_certificate_file_from_pen(onboard_response)
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(
            certfile=certificate_file_path,
            keyfile=certificate_file_path,
            password=onboard_response.get_authentication().get_secret(),
        )
        self.mqtt_client.tls_set_context(context)

        self._mode = None

    def connect(self, host: str, port: str) -> None:
        self._log.debug(f"Connecting client to MQTT broker at {host}:{port}")
        self.mqtt_client.connect(
            host=host,
            port=int(port)
        )
        self.mqtt_client.loop()

        self._mode = SYNC

    def connect_async(self, host: str, port: str):
        self._log.debug(f"Connecting async client to MQTT broker at {host}:{port}")
        self.mqtt_client.connect_async(
            host=host,
            port=int(port)
        )
        self.mqtt_client.loop_start()

        self._mode = ASYNC

        while self.mqtt_client._state == 0:
            time.sleep(1)

    def disconnect(self):
        self._log.debug("Disconnecting client from MQTT broker")
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def receive_outbox_messages(self):
        self.mqtt_client.loop()

    def publish(self, topic, payload, qos=2) -> MQTTMessageInfo:
        """
        :param topic: str representing unique name of the topic that the message should be published on
        :param payload: The actual message to send
        :param qos: int representing the quality of service level to use. May be [0, 1, 2]
        :return: MQTTMessageInfo
        """
        self._log.debug(f"Publishing message on topic {topic} with payload {payload}")
        message_info = self.mqtt_client.publish(
            topic=topic,
            payload=payload,
            qos=qos
        )
        if self._mode == SYNC:
            self.mqtt_client.loop()
            time.sleep(3)  # TODO: Check / Remove this sleep?
            self.mqtt_client.loop()
        self._log.debug(f"Message published with message info: {message_info}")
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
        self._log.debug(f"Subscribing to topics {topics}")
        result, mid = self.mqtt_client.subscribe(topics, qos=2)
        return result, mid

    def unsubscribe(self, topics: List[str]) -> tuple:
        """

        :param topics: list of strings [topic, topic] containing topic to unsubscribe from

        topic: str representing unique name of the topic to unsubscribe from

        Example: topics=['my/topic/1', 'my/topic/2', 'my/topic/3']

        :return: tuple
        """
        self._log.debug(f"Unsubscribing from topics {topics}")
        result, mid = self.mqtt_client.unsubscribe(topics)
        return result, mid

    @staticmethod
    def _get_on_connect_callback(onboard_response) -> callable:

        def on_connect(client: mqtt_client.Client, userdata, flags, rc, properties=None):
            if rc == 0:
                client.subscribe(topic=onboard_response.connection_criteria.commands)
                time.sleep(3)

        return on_connect

    @staticmethod
    def _get_on_message_callback() -> callable:

        def on_message(client, userdata, msg):
            return client, userdata, msg

        return on_message

    @staticmethod
    def _get_on_subscribe_callback() -> callable:

        def on_subscribe(*args, **kwargs):
            return args, kwargs

        return on_subscribe

    @staticmethod
    def _get_on_disconnect_callback() -> callable:

        def on_disconnect(*args, **kwargs):
            return args, kwargs

        return on_disconnect

    @staticmethod
    def _get_on_unsubscribe_callback() -> callable:

        def on_unsubscribe(*args, **kwargs):
            return args, kwargs

        return on_unsubscribe
