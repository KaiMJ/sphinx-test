from typing import Tuple


class UECharacter:
    def __init__(self,
                 name: str,
                 location: Tuple[float, float, float],
                 rotation: float,
                 ):
        """
        Initialize a UECharacter instance.

        :param name: Name of the character.
        :param location: Location of the character as a tuple (x, y, z).
        :param rotation: Rotation of the character as a float in roll direction.
        """
        self.character_id = UECharacter._get_next_id()
        self.name = name
        self.location = location
        self.rotation = rotation

    @classmethod
    def _get_next_id(cls):
        """
        Get the next available ID.

        :return: The next available ID.
        """
        result = cls._id_counter
        cls._id_counter += 1
        return result

    # Interact with pick-up

    def pick_object(self, object_id):
        """
        Pick up object.
        :param object_id: Target object's object id.

        :return: Whether pick up the object successfully as a bool.
        """
        pass

    def drop_down(self):
        """
        Drop down the object character is holding
        Note: Now character can hold an object in right hand so we don't need to specify which hand

        :return: Whether drop down the object successfully as a bool.
        """
        pass

    # Interact with door
    def pass_door(self, object_id):
        """
        Pass the door.
        :param object_id: Target door's object id.

        :return: Whether pass the door successfully as a bool.
        """
        pass

    # Interact with vehicle

    def enter_vehicle(self, vehicle_id):
        """
        Enter the vehicle.
        Note: Currently, character can only enter the front two doors as driver.

        :param vehicle_id: Target vehicle's vehicle id.

        :return: Whether enter the vehicle successfully as a bool.
        """
        pass

    def exit_vehicle(self):
        """
        Exit the vehicle.
        Note: Character are allowed to exit the vehilce only if the car is fully stopped.

        :return: Whether exit the vehicle successfully as a bool.
        """
        pass

    def open_back_trunk(self, vehicle_id):
        """
        Open the back trunk of the vehicle.

        :param vehicle_id: Target vehicle's vehicle id.

        :return: Whether open the trunk successfully as a bool.
        """
        pass

    def close_back_trunk(self, vehicle_id):
        """
        close the back trunk of the vehicle.

        :param vehicle_id: Target vehicle's vehicle id.

        :return: Whether close the trunk successfully as a bool. 
        """
        pass

    def drive_to_location(self, location):
        """
        Drive the car to target location
        :param location: Target location as a tuple (x, y, z) or (x, y).

        :return: character's final location as tuple(x, y, z)
        """
        pass

    # Character's local motion
    def move_character_to_location(self, location):
        """
        Move the character to a specific location. 

        :param location: Target location as a tuple (x, y, z) or (x, y).
        Note: User doesn't have to specify the z location, engine will deal with that value.

        :return: character's final location as tuple(x, y, z)
        """
        pass

    def move_character_to_object(self, object_id):
        """
        Move the character to a specific object. 

        :param object_id: Target object's object id.

        :return: Character's final location as tuple(x, y, z)
        """
        pass

    def move_character_along_direction(self, direction, step_size=150):
        """
        Move the character along direction with one step. 
        Note: If there's an obstacle in the way, character will stop at the obstacle. 

        :param direction: 4 directions are supplied. "forward" , "backward", "left" and "right" 
        represents the forward, backward, left and right direction of the character.
        :param step_size: Step size of this step. In default, it's set as 150.

        :return: Character's final location as tuple(x, y, z)
        """
        pass

    def move_character_towards_location(self, location, step_size=150):
        """
        Move the character towards a specific location with one step. 
        Note: Character will move along the correct path created by navigation system instead of 
        along the direct direction to the location

        :param location: Target location as tuple (x, y, z) or (x, y).
        :param step_size: Step size of this step. In default, it's set as 150.

        :return: Character's final location as tuple(x, y, z)
        """
        pass

    def move_character_towards_object(self, object_id, step_size=150):
        """
        Move the character towards a specific object with one step. 
        Note: the character will move along the correct path created by navigation system instead of 
        along the direct direction to the object.

        :param object_id: Target object's object id.
        :param step_size: Step size of this step. In default, it's set as 150.

        :return: Character's final location as tuple(x, y, z)
        """
        pass
