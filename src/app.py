import pygame
from pygame.pixelarray import PixelArray

from src.camera import AppCamera
from src.surfaceconvertor import SurfaceConvertor


class CaptureChange:
    def __init__(self):
        pygame.init()
        # self._resolution = 640, 480
        # self._resolution = 800, 600
        self._resolution = 1280, 720
        self._convertor = SurfaceConvertor(self._resolution)
        self._screen = pygame.display.set_mode(self._resolution)
        self._surface = pygame.Surface(self._resolution)
        # self._surface.set_alpha(250)
        self._cam = AppCamera(self._resolution)
        self._clock = pygame.time.Clock()

    def draw(self):
        self._surface.fill(pygame.Color('black'))
        _pixel_arr: PixelArray = self.__get_pixel_frame()
        self._convertor.next_frame(_pixel_arr, self._surface)
        self._screen.blit(self._surface, (0, 0))

    def __get_pixel_frame(self) -> PixelArray:
        _image = self._cam.image
        _scaled = pygame.transform.scale(_image, self._resolution)
        return pygame.pixelarray.PixelArray(_scaled)

    def run(self):
        while True:
            self.draw()
            for _event in pygame.event.get():
                if _event.type == pygame.QUIT or (_event.type == pygame.KEYDOWN and _event.key == pygame.K_ESCAPE):
                    self._cam.stop()  # close the camera safely
                    exit()
                elif _event.type == pygame.KEYDOWN and _event.key == pygame.K_q:
                    # self.get_image()
                    pass
            self._clock.tick(30)
            pygame.display.flip()  # Update display surface

