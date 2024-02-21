'''
№ 9

Графічна фігура: Піраміда з чотирикутною основою.

Технічні умови: Динаміка фігури: графічна фігура з’являється та гасне, змінює колір контуру та заливки.
'''

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from datetime import datetime
from typing import Callable, ForwardRef

class Transform:

    _VECTOR3_X_INDEX = 0
    _VECTOR3_Y_INDEX = 1
    _VECTOR3_Z_INDEX = 2

    @property
    def position(self) -> list[float]:
        return self._position

    @position.setter
    def position(self, value: list[float]) -> None:
        self._position = value

    @property
    def rotation(self) -> list[float]:
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: list[float]) -> None:
        self._rotation = value

    @property
    def scale(self) -> list[float]:
        return self._scale
    
    @scale.setter
    def scale(self, value: list[float]) -> None:
        self._scale = value

    def __init__(self, position: list[float], rotation: list[float], scale: list[float]) -> None:
        self._scale = scale
        self._position = position
        self._rotation = rotation

    def apply_scale(self) -> None:
        glScalef(self.scale[Transform._VECTOR3_X_INDEX], self.scale[Transform._VECTOR3_Y_INDEX], self.scale[Transform._VECTOR3_Z_INDEX])

    def apply_position(self) -> None:
        glTranslatef(self.position[Transform._VECTOR3_X_INDEX], self.position[Transform._VECTOR3_Y_INDEX], self.position[Transform._VECTOR3_Z_INDEX])

    def apply_rotation(self) -> None:
        PRECISION = 3
        ANGLE_THRESHOLD = 360.0

        glMultMatrixf(self._get_rotation_matrix_x(np.radians(np.round(self._rotation[Transform._VECTOR3_X_INDEX] % ANGLE_THRESHOLD, decimals = PRECISION))))
        glMultMatrixf(self._get_rotation_matrix_y(np.radians(np.round(self._rotation[Transform._VECTOR3_Y_INDEX] % ANGLE_THRESHOLD, decimals = PRECISION))))
        glMultMatrixf(self._get_rotation_matrix_z(np.radians(np.round(self._rotation[Transform._VECTOR3_Z_INDEX] % ANGLE_THRESHOLD, decimals = PRECISION))))

    def _get_rotation_matrix_x(self, angle: float) -> np.array:
        return np.array([[1, 0, 0, 0],
                         [0, np.cos(angle), -np.sin(angle), 0],
                         [0, np.sin(angle), np.cos(angle), 0],
                         [0, 0, 0, 1]], dtype = np.float32)

    def _get_rotation_matrix_y(self, angle: float) -> np.array:
        return np.array([[np.cos(angle), 0, np.sin(angle), 0],
                         [0, 1, 0, 0],
                         [-np.sin(angle), 0, np.cos(angle), 0],
                         [0, 0, 0, 1]], dtype = np.float32)

    def _get_rotation_matrix_z(self, angle: float) -> np.array:
        return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                         [np.sin(angle), np.cos(angle), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]], dtype = np.float32)

class Mesh:

    _VERTICES_IN_TRIANGLE = 3
    _VERTICES_IN_QUAD = 4

    def __init__(self, vertices: list[list[float]], faces: list[list[float]]) -> None:
        self._faces = faces
        self._vertices = vertices

    def draw_base(self) -> None:
        for face in self._faces:
            if len(face) == Mesh._VERTICES_IN_TRIANGLE:
                glBegin(GL_TRIANGLES)
            elif len(face) == Mesh._VERTICES_IN_QUAD:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_POLYGON)

            for vertex in face:
                glVertex3fv(self._vertices[vertex - 1])

            glEnd()

    def draw_outline(self) -> None:
        glBegin(GL_LINES)

        for face in self._faces:
            for i in range(len(face)):
                vertex_start = self._vertices[face[i] - 1]
                vertex_end = self._vertices[face[(i + 1) % len(face)] - 1]

                glVertex3fv(vertex_start)
                glVertex3fv(vertex_end)

        glEnd()

class Material:

    _COLOR_RED_CHANNEL = 0
    _COLOR_GREEN_CHANNEL = 1
    _COLOR_BLUE_CHANNEL = 2
    _COLOR_ALPHA_CHANNEL = 3

    @property
    def base_color(self) -> list[float]:
        return self._base_color
    
    @base_color.setter
    def base_color(self, value: list[float]) -> None:
        self._base_color = value

    @property
    def outline_color(self) -> list[float]:
        return self._outline_color
    
    @outline_color.setter
    def outline_color(self, value: list[float]) -> None:
        self._outline_color = value

    def __init__(self, base_color: list[float], outline_color: list[float], outline_thickness: float = 1.0) -> None:
        self._base_color = base_color
        self._outline_color = outline_color
        self._outline_thickness = outline_thickness

    def apply_base_color(self) -> None:
        self._apply_color(self._base_color)
    
    def apply_outline_color(self) -> None:
        glLineWidth(self._outline_thickness)
        self._apply_color(self._outline_color)

    def _apply_color(self, color: list[float]) -> None:
        glColor4f(color[self._COLOR_RED_CHANNEL], color[self._COLOR_GREEN_CHANNEL], color[self._COLOR_BLUE_CHANNEL], color[self._COLOR_ALPHA_CHANNEL])

class SceneObject:

    @property
    def transform(self) -> Transform:
        return self._transform
    
    @property
    def material(self) -> Material:
        return self._material

    def __init__(self, transform: Transform, mesh: Mesh, material: Material, update_delegate: Callable[[ForwardRef("SceneObject"), float], None]) -> None:
        self._mesh = mesh
        self._material = material
        self._transform = transform
        self._update_delegate = update_delegate

    def render(self) -> None:
        glPushMatrix()
        
        self._transform.apply_scale()
        self._transform.apply_rotation()
        self._transform.apply_position()

        self._material.apply_base_color()
        self._mesh.draw_base()

        self._material.apply_outline_color()
        self._mesh.draw_outline()

        glFlush()

        glPopMatrix()

    def update(self, delta_time: float) -> None:
        self._update_delegate(self, delta_time)

class Application:

    _VIEWPORT_WIDTH = 1920
    _VIEWPORT_HEIGHT = 1080
    
    _ANTI_ALIASING_SAMPLE_COUNT = 5

    _CAMERA_FOV = 45.0
    _CAMERA_ASPECT_RATIO = _VIEWPORT_WIDTH / _VIEWPORT_HEIGHT
    _CAMERA_NEAR_CLIPPING_PLANE = 0.01
    _CAMERA_FAR_CLIPPING_PLANE = 100.0
    _CAMERA_OFFSET = -5.0

    _MIN_DELTA_TIME = 0.005
    
    def __init__(self) -> None:
        glfw.init()
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        glfw.window_hint(glfw.SAMPLES, self._ANTI_ALIASING_SAMPLE_COUNT)
        self._window = glfw.create_window(self._VIEWPORT_WIDTH, self._VIEWPORT_HEIGHT, "Лабораторна робота № 1. ІП-14 Бабіч Денис", None, None)
        glfw.make_context_current(self._window)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        self._start()

        while not glfw.window_should_close(self._window):
            self._update()
            glfw.poll_events()

        self._destroy()

    def _apply_isometric_projection(self) -> None:
        ANGLE_ISOMETRIC_X = 45.0
        ANGLE_ISOMETRIC_Y = 45.0

        glLoadIdentity()

        glMatrixMode(GL_PROJECTION)

        angle_x = np.radians(ANGLE_ISOMETRIC_X)
        angle_y = np.radians(ANGLE_ISOMETRIC_Y)

        rotation_matrix_x = np.array([ [1, 0, 0, 0],
                                       [0, np.cos(angle_x), -np.sin(angle_x), 0],
                                       [0, np.sin(angle_x), np.cos(angle_x), 0],
                                       [0, 0, 0, 1] ], dtype = np.float32)

        rotation_matrix_y = np.array([ [np.cos(angle_y), 0, np.sin(angle_y), 0],
                                       [0, 1, 0, 0],
                                       [-np.sin(angle_y), 0, np.cos(angle_y), 0],
                                       [0, 0, 0, 1] ], dtype = np.float32)

        glMultMatrixf(rotation_matrix_x)
        glMultMatrixf(rotation_matrix_y)

    def _start(self) -> None:
        self._game_objects = list()

        pyramid_transform = Transform([-0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0])

        pyramid_vertices = [ [1, -1, -1],   # A
                             [1, -1, 1],    # B
                             [-1, -1, 1],   # C
                             [-1, -1, -1],  # D
                             [0, 1, 0] ]    # E (apex)

        pyramid_faces = [ [1, 2, 3, 4],  # Base (ABCD)
                          [1, 2, 5],     # Side (ABE)
                          [2, 3, 5],     # Side (BCE)
                          [3, 4, 5],     # Side (CDE)
                          [4, 1, 5] ]    # Side (DAE)

        pyramid_mesh = Mesh(pyramid_vertices, pyramid_faces)

        pyramid_material = Material([1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 1.0], 5)

        pyramid = SceneObject(pyramid_transform, pyramid_mesh, pyramid_material, pyramid_update)

        self._game_objects.append(pyramid)

    def _update(self) -> None:
        start_time = glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Pespective projection

        #glLoadIdentity()

        #glMatrixMode(GL_MODELVIEW)

        #gluPerspective(Application._CAMERA_FOV, Application._CAMERA_ASPECT_RATIO, Application._CAMERA_NEAR_CLIPPING_PLANE, Application._CAMERA_FAR_CLIPPING_PLANE)
        #glTranslate(0.0, 0.0, Application._CAMERA_OFFSET)

        #Isometric projection

        self._apply_isometric_projection()
        glTranslate(0.6, -1.25, 0.6)

        #glLoadIdentity()
        #glTranslate(0.0, 0.25, 1.35)
        #glRotatef(-45.0, 1.0, 0.0, 0.0)
        #glRotatef(-45.0, 0.0, 1.0, 0.0)

        glClearColor(0.0, 0.0, 0.0, 1.0)

        for game_object in self._game_objects:
            game_object.render()

        delta_time = (glfw.get_time() - start_time)

        if delta_time < Application._MIN_DELTA_TIME:
            delta_time = Application._MIN_DELTA_TIME

        for game_object in self._game_objects:
            game_object.update(delta_time)

        glfw.swap_buffers(self._window)
        
    def _destroy(self) -> None:
        glfw.terminate()

def pyramid_update(scene_object: SceneObject, delta_time: float) -> None:
    Y = 1
    COLOR_ALPHA_CHANNEL = 1.0
    COLOR_MAX_INTENSITY = 255

    ANGLE_FULL_CIRCLE = 360
    ANGLE_ROTATION_SPEED = 45

    timestamp = datetime.now().timestamp()

    previous_rotation = scene_object.transform.rotation
    scene_object.transform.rotation = [0, (previous_rotation[Y] + (ANGLE_ROTATION_SPEED * delta_time)) % ANGLE_FULL_CIRCLE, 0]

    COLOR_BASE_SHIFT_SPEED = 1

    gradient_black_white = np.interp((np.sin(timestamp * COLOR_BASE_SHIFT_SPEED)), [-1, 1], [0, 1])
    scene_object.material.base_color = [gradient_black_white, gradient_black_white, gradient_black_white, COLOR_ALPHA_CHANNEL]

    COLOR_OUTLINE_SHIFT_SPEED = 1

    COLOR_RED_CHANNEL_OFFSET = 0
    COLOR_GREEN_CHANNEL_OFFSET = 2 * np.pi / 3
    COLOR_BLUE_CHANNEL_OFFSET = 4 * np.pi / 3

    color_red_channel = int(np.interp(np.sin((timestamp * COLOR_OUTLINE_SHIFT_SPEED) + COLOR_RED_CHANNEL_OFFSET), [-1, 1], [0, 255])) / COLOR_MAX_INTENSITY
    color_green_channel = int(np.interp(np.sin((timestamp * COLOR_OUTLINE_SHIFT_SPEED) + COLOR_GREEN_CHANNEL_OFFSET), [-1, 1], [0, 255])) / COLOR_MAX_INTENSITY
    color_blue_channel = int(np.interp(np.sin((timestamp * COLOR_OUTLINE_SHIFT_SPEED) + COLOR_BLUE_CHANNEL_OFFSET), [-1, 1], [0, 255])) / COLOR_MAX_INTENSITY

    scene_object.material.outline_color = [color_red_channel, color_green_channel, color_blue_channel, COLOR_ALPHA_CHANNEL]

if __name__ == "__main__":
    instance = Application()