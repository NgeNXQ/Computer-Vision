import pygame

class Application:

    _VIEWPORT_WIDTH = 800
    _VIEWPORT_HEIGHT = 600

    _MAX_FPS = 60

    width, height = 800, 600

    white = (255, 255, 255)

    # Pyramid parameters
    pyramid_height = 200
    pyramid_base = 300

    # Pyramid calculation
    half_base = pyramid_base // 2
    pyramid_vertices = [(width // 2, height - 50),
                        (width // 2 - half_base, height - 50 - pyramid_height),
                        (width // 2 + half_base, height - 50 - pyramid_height)]

    def __init__(self) -> None:
        self._start()
        self._update()


    def _start(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Лабораторна робота № 1. ІП-14 Бабіч Денис")
        self._screen = pygame.display.set_mode((self._VIEWPORT_WIDTH, self._VIEWPORT_HEIGHT))
    

    def _update(self) -> None:

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self._destroy()

            pygame.draw.polygon(self._screen, self.white, self.pyramid_vertices)

            pygame.display.flip()
            self._clock.tick(self._MAX_FPS)
        
        self._destroy()


    def _destroy(self) -> None:
        pygame.quit()
