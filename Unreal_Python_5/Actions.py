from PIL import Image
import time

class ObjectActions:
    def add_object(self, name, location, rotation, scale, properties, 
                mesh_path=None, material_path=None, physics=False):
        """
        Add an object to the scene.

        :param name: Name of the object.
        :param location: Location of the object as a dictionary {'x': value, 'y': value, 'z': value}.
        :param rotation: Rotation of the object as a dictionary {'pitch': value, 'yaw': value, 'roll': value}.
        :param scale: Scale of the object as a dictionary {'x': value, 'y': value, 'z': value}.
        :param properties: Dictionary of properties to set on the object.
        :param mesh_path: Optional path to the mesh asset.
        :param material_path: Optional path to the material asset.
        :param physics: Boolean indicating whether physics should be enabled.
        :return: ID of the added object.
        """
        data = {
            "action": "add_object",
            "name": name,
            "location": {
                "x": location['x'],
                "y": location['y'],
                "z": location['z']
            },
            "rotation": {
                "pitch": rotation['pitch'],
                "yaw": rotation['yaw'],
                "roll": rotation['roll']
            },
            "scale": {
                "x": scale['x'],
                "y": scale['y'],
                "z": scale['z']
            },
            "properties": properties,
            "mesh_path": mesh_path,
            "material_path": material_path,
            "physics": physics
        }

        object_id = self.send_data(data)
        return object_id  # Example return {'object_id': 1}

    def delete_object(self, object_id):
        """
        Delete an object from the scene.

        :param object_id: ID of the object to delete.
        :return: Response message from the server.
        """
        data = {
            "action": "delete_object",
            "object_id": str(object_id)
        }
        message = self.send_data(data)
        return message  # Example return {'status': 'success'}


    def change_object(self, object_id, properties):
        """
        Change properties of an object in the scene.

        :param object_id: ID of the object to change.
        :param properties: Dictionary of properties to update on the object.
        :return: Response message from the server.
        """
        data = {
            "action": "change_object",
            "object_id": str(object_id),
            "properties": properties
        }
        message = self.send_data(data)
        return message  # Example return {'status': 'success'}

    def add_lighting(self, name: str, location: tuple, properties: dict) -> None:
        """
        Add lighting to the scene.

        :param name: Name of the lighting.
        :param location: Location of the lighting as a tuple (x, y, z).
        :param properties: Dictionary of properties to set on the lighting.
        :return: Response message from the server.
        """
        data = {
            "action": "add_lighting",
            "name": name,
            "location": {
                "x": location[0],
                "y": location[1],
                "z": location[2]
            },
            "properties": properties
        }
        message = self.send_data(data)
        return message  # Example return {'lighting_id': 1}


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

# llm.genetae("what should the agent do now?") 
# output --> move_foward(1, x, y, z)

# def move_forward(self, character_id, x, y, z):
#     data = {'action': 'forward', ...}
#     # data = openai.gpt("write a string for move forward")
#     return self.send_data(data)
