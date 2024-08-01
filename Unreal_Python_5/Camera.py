from typing import Tuple, List
from PIL import Image
import time
import json


class UECamera:
    _id_counter = 0  # Class variable to track the next available ID

    def __init__(self,
                 location: Tuple[float, float, float],
                 rotation: Tuple[float, float, float],
                 look_at: Tuple[float, float, float],
                 fov: float):
        """
        Initialize a UECamera instance.

        :param location: A tuple representing the location of the camera (x, y, z).
        :param rotation: A tuple representing the rotation of the camera (pitch, yaw, roll).
        :param look_at: A tuple representing the point the camera is looking at (x, y, z). Overrides rotation.
        :param fov: A float representing the field of view of the camera.
        """
        self.camera_id = UECamera._get_next_id()
        self.camera_id = None
        self.location = location
        self.rotation = rotation
        self.look_at = look_at
        self.fov = fov

    @classmethod
    def _get_next_id(cls):
        """
        Get the next available ID.

        :return: The next available ID.
        """
        result = cls._id_counter
        cls._id_counter += 1
        return result

    # Getters
    def get_id(self):
        """
        Get the ID of the object.

        :return: The ID of the object.
        """
        return self.camera_id

    def get_location(self) -> dict:
        """
        Get the location of the camera.

        :return: The location as a tuple (pitch, yaw, roll).
        """
        return self.location

    def get_rotation(self) -> dict:
        """
        Get the rotation of the camera.

        :return: The rotation as a tuple (pitch, yaw, roll).
        """
        return self.rotation

    def get_look_at(self) -> dict:
        """
        Get the look-at point of the camera.

        :return: The look-at point as a tuple (x, y, z).
        """
        return self.look_at

    def get_fov(self) -> float:
        """
        Get the field of view (FOV) of the camera.

        :return: The field of view.
        """
        return self.fov

    # Setters
    def set_location(self, x: float, y: float, z: float):
        """
        Set the location of the camera.

        :param x: The x-coordinate of the location.
        :param y: The y-coordinate of the location.
        :param z: The z-coordinate of the location.
        """
        self.location = (x, y, z)

    def set_rotation(self, pitch: float, yaw: float, roll: float):
        """
        Set the rotation of the camera.

        :param pitch: The pitch of the rotation.
        :param yaw: The yaw of the rotation.
        :param roll: The roll of the rotation.
        """
        self.rotation = (pitch, yaw, roll)

    def set_look_at(self, x: float, y: float, z: float):
        """
        Set the look-at point of the camera.

        :param x: The x-coordinate of the look-at point.
        :param y: The y-coordinate of the look-at point.
        :param z: The z-coordinate of the look-at point.
        """
        self.look_at = (x, y, z)

    def set_fov(self, fov: float):
        """
        Set the field of view (FOV) of the camera.

        :param fov: The field of view.
        """
        self.fov = fov

    def get_info(self) -> dict:
        """
        Get all the information of the camera.

        :return: A dictionary containing all the information of the camera.
        """
        return {
            "camera_id": self.get_id(),
            "location": self.get_location(),
            "rotation": self.get_rotation(),
            "look_at": self.get_look_at(),
            "fov": self.get_fov()
        }

    # get image / video
    def get_image(self):
        """
        Capture image from this camera

        :return: An Image object of the current camera.
        """
        pass

    def get_segmentation(self) -> Image.Image:
        """
        Capture a segmentation map from a specific camera.

        :return: An Image object of the segmentation map.
        """
        pass

    def get_point_cloud(self) -> dict:
        """
        Capture a point cloud from a specific camera.

        :return: Dictionary containing point cloud data.
        """

    def get_normal_map(self) -> Image.Image:
        """
        Capture a normal map from a specific camera.

        :return: An Image object of the normal map.
        """
        pass

    def get_video(self) -> str:
        """
        Capture a video from a specific camera.

        :return: Path to the captured video.
        """
        pass

    # motion
    def attach_to_object(self, obj, look_at: Tuple[float, float, float]) -> dict:
        """
        Attach a camera to a specific object.

        :param obj: UEObject to attach to.
        :param look_at: The look-at point as a tuple (x, y, z).
        """
        pass

    def move_around(self, look_at: dict, end_xyz: dict, duration: int = 5) -> dict:
        """
        Move the camera around in the scene.

        :param look_at: The look-at point as a tuple (x, y, z).
        :param end_xyz: The end position of the camera as a tuple (pitch, yaw, roll).
        :param duration: Duration of the movement in seconds.
        :return: Response from the server.
        """
        pass

    def zoom_in(self, distance: float) -> dict:
        """
        Zoom in the camera by a certain distance.

        :param distance: Distance to zoom in.
        :return: Response from the server.
        """
        pass

    # json format
    def get_json(self):
        """
        Convert the camera to JSON format for sending to a TCP server.

        :return: JSON string representing the camera.
        """
        data = {
            "type": "camera",
            "id": self.get_id(),
            "location": {
                "x": self.get_location()[0],
                "y": self.get_location()[1],
                "z": self.get_location()[2]
            },
            "rotation": {
                "pitch": self.get_rotation()[0],
                "yaw": self.get_rotation()[1],
                "roll": self.get_rotation()[2]
            },
            "look_at": {
                "x": self.get_look_at()[0],
                "y": self.get_look_at()[1],
                "z": self.get_look_at()[2]
            },
            "fov": self.get_fov()
        }
        return json.dumps(data)
