import socket
import json

class UE5_Engine:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        """
        Start the client
        """
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(3.0)
        except ConnectionRefusedError:
            print("Make sure the TCPServer Actor is loaded in the Unreal Engine Editor")
            print("And game is running!!!")

    def send_data(self, data: dict):
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode('utf-8'))
        response = self.receive_response()
        return response

    def receive_response(self):
        buffer_size = 4096
        response_data = b""

        while True:
            part = self.client_socket.recv(buffer_size)
            response_data += part
            if len(part) < buffer_size:
                break
        
        return response_data.decode("utf-8")
