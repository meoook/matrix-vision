import pygame.camera


class AppCamera(object):
    __DEFAULT_RESOLUTION: tuple[int, int] = 640, 480

    def __init__(self, resolution: tuple[int, int] = None):
        _resolution = resolution or self.__DEFAULT_RESOLUTION

        _backends = pygame.camera.get_backends()
        pygame.camera.init(_backends[0])

        _cameras = pygame.camera.list_cameras()
        if _cameras:
            self.__cam = pygame.camera.Camera(_cameras[0], _resolution)
            self.__cam.start()
        else:
            raise SystemExit("No cameras detected")

        self.__snapshot = pygame.surface.Surface(_resolution)

    @property
    def image(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.__cam.query_image():
            self.__snapshot = self.__cam.get_image(self.__snapshot)
        return self.__snapshot

    def stop(self) -> None:
        print('Safe stop camera')
        self.__cam.stop()  # close the camera safely
