import sys
import pygame as pg

from engine import *


class GameWindow:
    def __init__(self, screen_size: tuple[int, int], framerate_limit: int = 0) -> None:
        self.screen_size = screen_size
        self.framerate_limit = framerate_limit
    
    def run(self):
        # Инициализируем библиотеки
        ti.init(arch=ti.cuda)
        pg.init()
        pg.font.init()

        # Создаём окно
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("3D game")

        # Создаём Clock
        self.clock = pg.time.Clock()

        # Создаём шрифт
        font = pg.font.Font(pg.font.get_default_font(), 32)

        # Игровой цикл
        while True:
            # Читаем события окна
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # Очищаем экран
            self.screen.fill((0, 0, 0))

            # Отображаем fps
            self.screen.blit(font.render(f"fps: {int(self.clock.get_fps())}", True, (255, 0, 0)), (10, 10))

            # Обновляем окно
            self.clock.tick(self.framerate_limit)
            pg.display.flip()


def main():
    window = GameWindow((1920, 1080))

    window.run()


if __name__ == "__main__":
    main()
