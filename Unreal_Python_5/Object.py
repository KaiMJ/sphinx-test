from typing import Tuple
import json


class UEObject:
    _id_counter = 0  # Class variable to track the next available ID

    def __init__(self,
                 name: str,
                 location: Tuple[float, float, float],
                 rotation: Tuple[float, float, float],
                 scale: Tuple[float, float, float],
                 mesh_path: str,
                 material_path: str,
                 physics: bool
                 ):
        """
        Initialize a UEObject instance.

        :param name: Name of the object.
        :param location: Location of the object as a tuple (x, y, z).
        :param rotation: Rotation of the object as a tuple (pitch, yaw, roll).
        :param scale: Scale of the object as a tuple (x, y, z).
        :param mesh_path: Path to the mesh asset.
        :param material_path: Path to the material asset.
        :param physics: Boolean indicating whether physics should be enabled.
        """
        self.object_id = UEObject._get_next_id()
        self.name = name
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.mesh_path = mesh_path
        self.material_path = material_path
        self.physics = physics

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
        return self.object_id

    def get_name(self):
        """
        Get the name of the object.

        :return: The name of the object.
        """
        return self.name

    def get_location(self):
        """
        Get the location of the object.

        :return: The location of the object as a tuple (x, y, z).
        """
        return self.location

    def get_rotation(self):
        """
        Get the rotation of the object.

        :return: The rotation of the object as a tuple (pitch, yaw, roll).
        """
        return self.rotation

    def get_scale(self):
        """
        Get the scale of the object.

        :return: The scale of the object as a tuple (x, y, z).
        """
        return self.scale

    def get_mesh_path(self):
        """
        Get the mesh path of the object.

        :return: The mesh path of the object.
        """
        return self.mesh_path

    def get_material_path(self):
        """
        Get the material path of the object.

        :return: The material path of the object.
        """
        return self.material_path

    def get_physics(self):
        """
        Get the physics status of the object.

        :return: The physics status of the object (True/False).
        """
        return self.physics

    def get_info(self):
        """
        Get all the information of the object.

        :return: A dictionary containing all the information of the object.
        """
        return {
            'id': self.get_id(),
            "name": self.get_name(),
            'location': self.get_location(),
            'rotation': self.get_rotation(),
            'scale': self.get_scale(),
            'mesh_path': self.get_mesh_path(),
            'material_path': self.get_material_path(),
            'physics': self.get_physics()
        }

    # Setters
    def set_name(self, name):
        """
        Set the name of the object.

        :param name: The new name of the object.
        """
        self.name = name

    def set_location(self, x: float, y: float, z: float):
        """
        Set the location of the object.

        :param x: The x-coordinate of the location.
        :param y: The y-coordinate of the location.
        :param z: The z-coordinate of the location.
        """
        self.location = (x, y, z)

    def set_rotation(self, pitch: float, yaw: float, roll: float):
        """
        Set the rotation of the object.

        :param pitch: The pitch of the rotation.
        :param yaw: The yaw of the rotation.
        :param roll: The roll of the rotation.
        """
        self.rotation = (pitch, yaw, roll)

    def set_scale(self, x: float, y: float, z: float):
        """
        Set the scale of the object.

        :param x: The x-scale of the object.
        :param y: The y-scale of the object.
        :param z: The z-scale of the object.
        """
        self.scale = (x, y, z)

    def set_mesh_path(self, mesh_path: str):
        """
        Set the mesh path of the object.

        :param mesh_path: The new mesh path of the object.
        """
        self.mesh_path = mesh_path

    def set_material_path(self, material_path: str):
        """
        Set the material path of the object.

        :param material_path: The new material path of the object.
        """
        self.material_path = material_path

    def set_physics(self, physics: bool):
        """
        Set the physics status of the object.

        :param physics: The new physics status of the object (True/False).
        """
        self.physics = physics

    # Motion
    def move(self, location: Tuple[float, float, float], duration: float):
        """
        TODO: how to implement this.
        obj.move()
        engine.move(obj) ?
        """
        pass

    # json format
    def get_json(self):
        """
        Convert the object to JSON format for sending to a TCP server.

        :return: JSON string representing the object.
        """
        data = {
            "type": "object",
            "id": self.get_id(),
            "name": self.name,
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
            "scale": {
                "x": self.get_scale()[0],
                "y": self.get_scale()[1],
                "z": self.get_scale()[2]
            },
            "mesh_path": self.get_mesh_path(),
            "material_path": self.get_material_path(),
            "physics": self.get_physics()
        }
        return json.dumps(data)
