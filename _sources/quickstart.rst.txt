Quickstart
==========

1. Ensure that Unreal Engine is in gameplay and connect to the engine

.. code-block:: python
    
    from Unreal_Python_5 import UE5_Engine
    
    engine = UE5_engine(host="127.0.0.1", port=12345)
    # make sure ATCPServer is inside the Unreal Engine and the game is running!!!
    engine.start_client()

2. Add Object.

.. code-block:: python

    from Unreal_Python_5 import UEObject

    obj = UEObject(name="chair",
            location=(0, 0, 0),
            rotation=(0, 0, 0),
            scale=(1, 1, 1),
            mesh_path="/path/to/mesh",
            material_path="/path/to/material",
            physics=True
        )

    # call engine.render    
    engine.render(obj)

    obj.get_id() # int: id
    obj.get_name() # str: name
    obj.get_location() # tuple: (x, y, z)
    obj.get_rotation() # tuple: (yaw, roll, pitch)
    obj.get_scale() # tuple: (x, y, z)
    obj.get_mesh_path() # str: mesh path
    obj.get_material_path() # str: material path
    obj.get_physics() # bool: True / False
    obj.get_info() # JSON dict of all the info

    obj.set_name("blue chair")
    obj.set_location(x=100, y=100, z=100)
    obj.set_rotation(pitch=90, yaw=90, roll=90)
    obj.set_scale(x=2, y=2, z=2)
    obj.set_mesh_path("/path/to/new/mesh")
    obj.set_material_path("/path/to/new/material")
    obj.set_physics(False)

    # call engine.render again to make changes    
    engine.render(obj)

3. Add Camera

.. code-block:: python

    from Unreal_Python_5 import UECamera

    camera = UECamera(name="chair",
            location=(0, 0, 0),
            rotation=(0, 0, 0),
            look_at=(10, 10, 10),
            fov=10
        )

    # call engine.render   
    engine.render(camera)

    camera.get_id() # int: id
    camera.get_location() # tuple: (x, y, z)
    camera.get_rotation() # tuple: (yaw, roll, pitch)
    camera.get_look_at() # tuple: (x, y, z)
    camera.get_fov() # float: fov
    camera.get_info() # JSON dict of all the info

    camera.set_location(x=100, y=100, z=100)
    camera.set_rotation(pitch=90, yaw=90, roll=90)
    camera.set_look_at(x=0, y=0, z=0)
    camera.set_fov(False)

    # call engine.render again to make changes    
    engine.render(camera)

    camera.get_image() # returns Image object of the current camera
    # TODO:
    camera.get_segmentation()
    camera.get_point_cloud()
    camera.get_normal_map()
    camera.get_video()
    camera.attach_to_object(obj, look_at=(0, 0, 0))
    camera.move_around(look_at=(0, 0, 0), end_xyz=(100, 100, 100), duration=10)
    camera.zoom_in()
    engine.render(camera)



4. #TODO: Add SceneGraph

.. code-block:: python

    from Unreal_Python_5 import SceneGraph
    cigar_room_scene = SceneGraph("Create a cigar room scene.")

    cigar_room_scene.save_scene("cigar_room.json")

    cigar_room_scene.load_scene("cigar_room.json")

    engine.render(cigar_room_scene)