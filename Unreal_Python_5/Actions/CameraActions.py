from PIL import Image
import time

class CameraActions:
    def add_camera(self, name: str, location: dict, properties: dict) -> dict:
        """
        Add a camera to the scene.

        :param name: Name of the camera.
        :param location: Location of the camera as a dictionary {'x': value, 'y': value, 'z': value}.
        :param properties: Dictionary of properties to set on the camera.
        :return: Response from the server.
        """
        data = {
            "action": "add_camera",
            "name": name,
            "location": location,
            "properties": properties
        }
        response = self.send_data(data)
        return response  # Example return {'camera_id': 1}

    def take_screenshot(self) -> Image.Image:
        """
        Capture a screenshot from the scene.

        :return: An Image object of the captured screenshot.
        """
        data = {"action": "capture_screenshot"}
        img_path = self.send_data(data)
        formatted_path = "/" + img_path.replace('../', '')

        while True:
            try:
                return Image.open(formatted_path)
            except FileNotFoundError:
                time.sleep(1)  # Wait for 1 second before retrying
            except Exception as e:
                print(f"An error occurred: {e}")
                break
