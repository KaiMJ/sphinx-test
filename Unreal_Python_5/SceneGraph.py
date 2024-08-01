from .Object import UEObject

class SceneGraph:
    def __init__(self, prompt:str = None):
        pass
        if prompt is not None:
            self.prompt_to_scene_graph()

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.objs):
            result = self.objs[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def prompt_to_scene_graph(self):
        self.objs =  [UEObject(), UEObject(), UEObject()]
        return self.objs

    def prompt_to_scene_component(self):
        pass

    def get_scene_info(self):
        pass

    def save_scene(self, save_path):
        pass

    def load_scene(self, load_path):
        pass


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
