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
        self._font = pygame.font.Font('./font/ms mincho.ttf', font_size)
        self._font.set_bold(True)
        self.__pixel_matrix = np.random.choice(self.__pixel_variants, self.__matrix_size)
        self.char_intervals = np.random.randint(25, 50, size=self.__matrix_size)
        self.cols_speed = np.random.randint(1, 500, size=self.__matrix_size)
        self.__pixel_colors = self.__render_color_palette()

        print('Convertor details')
        print('\tMatrix size:'.ljust(14) + f'cols - {self.__matrix_size[1]}, rows - {self.__matrix_size[0]}')
        print('\tPx variants:'.ljust(14) + f'{len(self.__pixel_variants)}')
        print('\tRendered px:'.ljust(14) + f'{len(self.__pixel_colors)}')

    def next_frame(self, pixel_arr, surface):
        """ Convert picture to new one with changed pixels """
        _frames = pygame.time.get_ticks()
        self.change_chars(_frames)
        self.shift_column(_frames)
        self.__convert_and_draw(pixel_arr, surface)

    def __render_color_palette(self) -> dict[tuple[str, int], any]:
        """ Pre render pixels variants with color scheme """
        _color_palette = [(0, green, 0) for green in range(256)]
        # _color_palette = [(0, 0, blue) for blue in range(256)]
        # _color_palette = [(red, 0, 0) for red in range(256)]
        # _color_palette = [(gray, gray, gray) for gray in range(256)]
        _pixels: dict[tuple[str, int], any] = {}
        for _px in self.__pixel_variants:
            _color_pixel = {(_px, idx): self._font.render(_px, True, color) for idx, color in enumerate(_color_palette)}
            _pixels.update(_color_pixel)
        return _pixels

    def shift_column(self, frames):
        _num_cols = np.argwhere(frames % self.cols_speed == 0)
        _num_cols = _num_cols[:, 1]
        _num_cols = np.unique(_num_cols)
        self.__pixel_matrix[:, _num_cols] = np.roll(self.__pixel_matrix[:, _num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.__pixel_variants, mask.shape[0])
        self.__pixel_matrix[mask[:, 0], mask[:, 1]] = new_chars

    def __convert_and_draw(self, pixel_arr, surface):
        for y, row in enumerate(self.__pixel_matrix):
            for x, _pixel in enumerate(row):
                if _pixel:
                    pos = x * self.__pixel_size, y * self.__pixel_size
                    _, red, green, blue = pygame.Color(pixel_arr[pos])
                    if red and green and blue:
                        _color = self.__color_to_int(red, green, blue)
                        # _color = self.__color_correction(_color)
                        _pixel = self.__pixel_colors[(_pixel, _color)]
                        # _pixel.set_alpha(_color + 80)
                        surface.blit(_pixel, pos)

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
