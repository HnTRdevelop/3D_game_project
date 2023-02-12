from engine import GameWindow
import pygame as pg


def main():
    window = GameWindow((1920, 1080), max_fps=0)
    pg.display.toggle_fullscreen()

    window.run()


if __name__ == "__main__":
    main()
