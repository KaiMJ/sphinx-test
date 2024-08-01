from typing import Union, List
from .Object import UEObject
from .Camera import UECamera
# from Unreal_Python_5.SceneGraph import SceneGraph
import socket
import json
from PIL import Image
import time

class UE5_Engine:
    def __init__(self, host="127.0.0.1", port=12345):
        """
        Initialize the UE5_Engine client.

        :param host: The host address of the server (default is "127.0.0.1").
        :param port: The port number of the server (default is 12345).
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        """
        Start the client and connect to the server.

        Raises:
            ConnectionRefusedError: If the server is not available.
        """
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(3.0)
        except ConnectionRefusedError:
            print("Make sure the TCPServer Actor is loaded in the Unreal Engine Editor")
            print("And game is running!!!")

    def send_data(self, data: dict) -> str:
        """
        Send data to the server.

        :param data: A dictionary containing the data to be sent.
        :return: The response from the server.
        """
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode('utf-8'))
        response = self.receive_response()
        return response

    def receive_response(self) -> str:
        """
        Receive response from the server.

        :return: The response data as a string.
        """
        buffer_size = 4096
        response_data = b""

        while True:
            part = self.client_socket.recv(buffer_size)
            response_data += part
            if len(part) < buffer_size:
                break

        return response_data.decode("utf-8")

    # def _render(self, object: Union[UEObject, UECamera, SceneGraph]):
    def _render(self, object: UEObject):
        """
        Internal method to send an object's JSON data to the server.

        :param object: An instance of UEObject, UECamera, or SceneGraph.
        """
        self.send_data(object.get_json())

    # def render(self, object: Union[List[Union[UEObject, UECamera, SceneGraph]], UEObject, UECamera, SceneGraph]):
    def render(self, object):
        """
        Render the object(s) by sending their data to the server.

        :param object: A single instance or a list of instances of UEObject, UECamera, or SceneGraph.
        """
        if type(object) == list:
            for obj in object:
                self._render(obj)
        else:
            self._render(object)

    def take_screenshot(self) -> Image.Image:
        """
        Capture a screenshot from the scene as seen in the Unreal Editor.

        :return: An Image object of the captured screenshot.
        """
        data = {"action": "capture_screenshot"}
        img_path = self.send_data(data)
        formatted_path = "/" + img_path.replace('../', '')

        while True:
            try:
                return Image.open(formatted_path)
            except FileNotFoundError:
                time.sleep(0.1)  # Wait for 0.1 second before retrying
            except Exception as e:
                print(f"An error occurred: {e}")
                break