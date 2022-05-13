import numpy as np
import pygame


class SurfaceConvertor:
    """ Create matrix for new pixel_size and control converting surface """

    def __init__(self, resolution=(640, 480), font_size=8):
        _width, _height = resolution
        self.__pixel_size = font_size
        self.__matrix_size = _height // font_size, _width // font_size
        # katakana
        self.__pixel_variants = np.array([chr(int('0x30a0', 16) + i) for i in range(96)])
        self.__matrix = np.random.choice(self.__pixel_variants, self.__matrix_size)
        self.__pixels_switch = np.random.randint(low=25, high=50, size=self.__matrix_size)
        self.__cols_speed = np.random.randint(low=1, high=50, size=(3, self.__matrix_size[1]))
        self.__pixels = self.__render_color_palette(font_size)

        print('Convertor details')
        print('\tMatrix size:'.ljust(14) + f'{self.__matrix_size[1]} x {self.__matrix_size[0]}')
        print('\tPx variants:'.ljust(14) + f'{len(self.__pixel_variants)}')
        print('\tRendered px:'.ljust(14) + f'{len(self.__pixels)}')

    def next_frame(self, pixel_arr, surface) -> None:
        """ Draw converted picture on surface """
        _frames = pygame.time.get_ticks()
        self.__change_pixels(_frames)
        self.__shift_column(_frames)
        self.__convert_and_draw(pixel_arr, surface)

    def __render_color_palette(self, font_size: int) -> dict[tuple[str, int], any]:
        """ Pre render pixels variants with color scheme """
        _font = pygame.font.Font('./font/ms mincho.ttf', font_size)
        _font.set_bold(True)
        _color_palette = [(0, green, 0) for green in range(256)]
        # _color_palette = [(0, 0, blue) for blue in range(256)]
        # _color_palette = [(red, 0, 0) for red in range(256)]
        # _color_palette = [(gray, gray, gray) for gray in range(256)]
        _pixels: dict[tuple[str, int], any] = {}
        for _px in self.__pixel_variants:
            _color_pixel = {(_px, idx): _font.render(_px, True, color) for idx, color in enumerate(_color_palette)}
            _pixels.update(_color_pixel)
        return _pixels

    def __shift_column(self, frames: int) -> None:
        _num_cols = np.argwhere(frames % self.__cols_speed == 0)
        _num_cols = _num_cols[:, 1]
        _num_cols = np.unique(_num_cols)
        self.__matrix[:, _num_cols] = np.roll(self.__matrix[:, _num_cols], shift=1, axis=0)

    def __change_pixels(self, frames: int) -> None:
        _mask = np.argwhere(frames % self.__pixels_switch == 0)
        _new_pixels = np.random.choice(self.__pixel_variants, _mask.shape[0])
        self.__matrix[_mask[:, 0], _mask[:, 1]] = _new_pixels

    def __convert_and_draw(self, pixel_arr, surface) -> None:
        for _y, _row in enumerate(self.__matrix):
            for _x, _pixel in enumerate(_row):
                if _pixel:
                    _position = _x * self.__pixel_size, _y * self.__pixel_size
                    _, _red, _green, _blue = pygame.Color(pixel_arr[_position])
                    if _red and _green and _blue:
                        _color = self.__color_to_int(_red, _green, _blue)
                        _color = self.__color_correction(_color)
                        _pixel = self.__pixels[(_pixel, _color)]
                        # _pixel.set_alpha(_color + 80)
                        surface.blit(_pixel, _position)

    @staticmethod
    def __color_to_int(red: int, green: int, blue: int) -> int:
        _color = (red + green + blue) // 3
        return _color if _color > 0 else 0

    @staticmethod
    def __color_correction(color: int) -> int:
        if color > 200:
            return color - 5
        if color > 150:
            return color
        if color > 100:
            return color + 5
        if color > 50:
            return color + 10
        return color + 15
