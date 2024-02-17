'''
№ 9

Графічна фігура: Піраміда з чотирикутною основою.

Технічні умови: Динаміка фігури: графічна фігура з’являється та гасне, змінює колір контуру та заливки.
'''

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

class Transform:

    def __init__(self) -> None:
        print("init")

class Mesh:

    _VERTEX_X_INDEX = 0
    _VERTEX_Y_INDEX = 1
    _VERTEX_Z_INDEX = 2

    def __init__(self, vertices: list[list[float]]) -> None:
        self._vertices = vertices

    def draw_base(self) -> None:
        glBegin(GL_TRIANGLES)

        for vertex in self._vertices:
            glVertex3f(vertex[self._VERTEX_X_INDEX], vertex[self._VERTEX_Y_INDEX], vertex[self._VERTEX_Z_INDEX])

        glEnd()

    def draw_outline(self) -> None:
        vertices_count = len(self._vertices)

        glBegin(GL_LINES)

        for i in range(vertices_count):
            vertex_start = self._vertices[i]
            vertex_end = self._vertices[(i + 1) % vertices_count]
            glVertex3f(vertex_start[Mesh._VERTEX_X_INDEX], vertex_start[Mesh._VERTEX_Y_INDEX], vertex_start[Mesh._VERTEX_Z_INDEX])
            glVertex3f(vertex_end[Mesh._VERTEX_X_INDEX], vertex_end[Mesh._VERTEX_Y_INDEX], vertex_end[Mesh._VERTEX_Z_INDEX])

        glEnd()

class Material:

    _COLOR_RED_CHANNEL = 0
    _COLOR_GREEN_CHANNEL = 1
    _COLOR_BLUE_CHANNEL = 2
    _COLOR_ALPHA_CHANNEL = 3

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

class GameObject:

    def __init__(self, transform: Transform, mesh: Mesh, material: Material) -> None:
        self._mesh = mesh
        self._material = material
        self._transform = transform

    def update(self) -> None:
        self._material.apply_base_color()
        self._mesh.draw_base()

        self._material.apply_outline_color()
        self._mesh.draw_outline()

    def get_transform(self) -> Transform:
        return self._transform

    def set_transform(self, transform: Transform) -> None:
        self._transform = transform

    def get_material(self) -> Material:
        return self._material

    def set_material(self, material: Material) -> None:
        self._material = material


class Application:

    _VIEWPORT_WIDTH = 800
    _VIEWPORT_HEIGHT = 600
    
    ANTI_ALIASING_SAMPLE_COUNT = 5
    
    def __init__(self) -> None:
        glfw.init()
        glfw.window_hint(glfw.SAMPLES, self.ANTI_ALIASING_SAMPLE_COUNT)
        self._window = glfw.create_window(self._VIEWPORT_WIDTH, self._VIEWPORT_HEIGHT, "Лабораторна робота № 1. ІП-14 Бабіч Денис", None, None)
        glfw.make_context_current(self._window)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        self._start()

        while not glfw.window_should_close(self._window):
            self._update()
            glfw.poll_events()

        self._destroy()

    def _start(self) -> None:

        self._game_objects = list()

        pyramid_transform = Transform()

        pyramid_mesh = Mesh([ [0.0, 1.0, 0.0],
                              [1.0, -1.0, 0.0],
                              [-1.0, -1.0, 0.0] ])

        pyramid_material = Material([1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], 10)
        
        pyramid = GameObject(pyramid_transform, pyramid_mesh, pyramid_material)

        self._game_objects.append(pyramid)

    def _update(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for game_object in self._game_objects:
            game_object.update()

        glfw.swap_buffers(self._window)
        
    def _destroy(self) -> None:
        glfw.terminate()


if __name__ == "__main__":
    instance = Application()