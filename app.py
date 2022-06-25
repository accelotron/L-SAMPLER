from ui import *
import pygame as pg
import os
from audio import PianoSounds


if __name__ == "__main__":
    pg.init()
    pg.mixer.init(frequency=16000)

    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    if not os.path.exists('piano_cache'):
        os.makedirs('piano_cache')

    if not os.path.exists('samples'):
        os.makedirs('samples')

    logo = pg.image.load("32by32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("L + SAMPLER")

    screen = pg.display.set_mode((1280, 720))
    screen.fill((39, 41, 45))

    logo = Logo(5, 5)
    logo.render(screen)

    pg.display.update()

    rect_list = [RectGrey(1056, 475, 219, 240), RectGrey(480, 5, 795, 110), RectGrey(5, 120, 1270, 120),
                 RectGrey(5, 360, 420, 110), RectGrey(855, 360, 420, 110)]

    for rect in rect_list:
        rect.render(screen)

    preset_load_1 = PresetLoader(5, 245, 'samples', 'Base File 1')
    preset_load_1.render(screen)

    preset_load_2 = PresetLoader(855, 245, 'samples', 'Base File 2')
    preset_load_2.render(screen)

    gen_btn = GenButton(430, 245)
    gen_btn.render(screen)

    exp_btn = ExportButton(430, 360, 'piano_cache', 'outputs')
    exp_btn.render(screen)

    ps = PianoSounds(
        'piano_cache',
        'rave_nsynth.ts',
        16000)

    piano = PianoRoll(5, 475, ps)
    piano.render(screen)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                piano.key_down(event, screen)

            if event.type == pg.KEYUP:
                piano.key_up(event, screen)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                piano.keys_update(event, screen)
                preset_load_1.update(event, screen)
                preset_load_2.update(event, screen)
                exp_btn.update(event, screen)

                # Я панк, мне тутутутуту.....
                # И да, оно будет висеть на цикле. Вопросы?
                gen_btn.update(event, preset_load_1.get_file(), preset_load_2.get_file(), piano, exp_btn, screen)

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                piano.keys_update(event, screen)

            pg.display.update()
