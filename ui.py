import pygame as pg
import random
import os
import shutil


# https://pastebin.com/GtUzre96
pg.font.init()
FONT_TEXT_NORMAL = pg.font.Font("SyneMono-Regular.ttf", 15)
FONT_TEXT_BIG = pg.font.Font("SyneMono-Regular.ttf", 40)
FONT_TEXT_LOGO = pg.font.Font("SyneMono-Regular.ttf", 90)


class Logo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, surface):
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 470, 110))
        surface.blit(FONT_TEXT_LOGO.render("L+SAMPLER", False, (255, 255, 255)), [15, 5])


class RectGrey:
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def render(self, surface):
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, self.h, self.w))


class PianoRoll:
    def __init__(self, x, y, ps):
        self.x = x
        self.y = y
        self.sounds = ps

        # key ids
        self.kids_white = tuple([0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23])
        self.kids_black = tuple([1, 3, 6, 8, 10, 13, 15, 18, 20, 22])
        self.kid_map = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 2, 7: 4, 8: 3, 9: 5, 10: 4, 11: 6, 12: 7,
                        13: 5, 14: 8, 15: 6, 16: 9, 17: 10, 18: 7, 19: 11, 20: 8, 21: 12, 22: 9, 23: 13}
        self.key_buttons = 'q2w3er5t6y7uzsxdcvgbhnjm'
        self.key_map = {self.key_buttons[i]: i for i in range(24)}

        # top left corner of every key
        self.tl_white = [[self.x + i * 70 + i * 2 + 20, self.y + 20] for i in range(14)]
        self.tl_black = [[self.x + i * 40 + i * 32 + 71, self.y + 20] for i in range(13)]
        del self.tl_black[9]
        del self.tl_black[6]
        del self.tl_black[2]

        self.pressed_keys = [False for _ in range(24)]
        self.mouse_kid = None

    def render(self, surface):
        # draw board
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 1046, 240))

        # draw keys
        for tl in self.tl_white:
            pg.draw.rect(surface, (255, 255, 255), pg.Rect(tl, (70, 200)))

        for tl in self.tl_black:
            pg.draw.rect(surface, (0, 0, 0), pg.Rect(tl, (40, 140)))

    def get_keyboard_kid(self, key):
        if key in self.key_buttons and key != '':
            return self.key_map[key]
        else:
            return None

    def get_mouse_kid(self, pos):
        # check black
        for i in range(10):
            tl = self.tl_black[i]
            if tl[0] <= pos[0] <= tl[0] + 40 and tl[1] <= pos[1] <= tl[1] + 140:
                self.mouse_kid = self.kids_black[i]
                return self.kids_black[i]

        # check white
        for i in range(14):
            tl = self.tl_white[i]
            if tl[0] <= pos[0] <= tl[0] + 70 and tl[1] <= pos[1] <= tl[1] + 200:
                self.mouse_kid = self.kids_white[i]
                return self.kids_white[i]

        return None

    def key_down(self, event, surface):
        kid = None

        if event.type == pg.KEYDOWN:
            kid = self.get_keyboard_kid(str(event.unicode))

        if event.type == pg.MOUSEBUTTONDOWN:
            kid = self.get_mouse_kid(event.pos)

        if kid in self.kids_white:
            self.pressed_keys[kid] = True
            pg.mixer.stop()
            try:
                self.sounds.sound_play(kid)
            except AttributeError:
                print("Piano roll doesn't have any sounds to play!")
            pg.draw.rect(surface, (95, 123, 159), pg.Rect(self.tl_white[self.kid_map[kid]], (70, 200)))
            self.regenerate_black(kid, surface)

        if kid in self.kids_black:
            self.pressed_keys[kid] = True
            pg.mixer.stop()
            try:
                self.sounds.sound_play(kid)
            except AttributeError:
                print("Piano roll doesn't have any sounds to play!")
            pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_black[self.kid_map[kid]], (40, 140)))

    def key_up(self, event, surface):
        kid = None

        if event.type == pg.KEYUP:
            kid = self.get_keyboard_kid(str(event.unicode))

        if event.type == pg.MOUSEBUTTONUP:
            kid = self.mouse_kid
            self.mouse_kid = None

        if kid in self.kids_white:
            self.pressed_keys[kid] = False
            pg.draw.rect(surface, (255, 255, 255), pg.Rect(self.tl_white[self.kid_map[kid]], (70, 200)))
            self.regenerate_black(kid, surface)

        if kid in self.kids_black:
            self.pressed_keys[kid] = False
            pg.draw.rect(surface, (0, 0, 0), pg.Rect(self.tl_black[self.kid_map[kid]], (40, 140)))

    def regenerate_black(self, kid, surface):
        # regenerate black keys
        if kid - 1 in self.kids_black:
            if self.pressed_keys[kid - 1]:
                pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_black[self.kid_map[kid - 1]], (40, 140)))
            else:
                pg.draw.rect(surface, (0, 0, 0), pg.Rect(self.tl_black[self.kid_map[kid - 1]], (40, 140)))

        if kid + 1 in self.kids_black:
            if self.pressed_keys[kid + 1]:
                pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_black[self.kid_map[kid + 1]], (40, 140)))
            else:
                pg.draw.rect(surface, (0, 0, 0), pg.Rect(self.tl_black[self.kid_map[kid + 1]], (40, 140)))

    def keys_update(self, event, surface):
        if event.type == pg.MOUSEBUTTONUP:
            self.key_up(event, surface)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.key_down(event, surface)


class StepDisplay:
    def __init__(self, x, y, values, init_i, max_v_len):
        self.x = x
        self.y = y

        self.tl_add = [self.x + 370, self.y + 5]
        self.tl_disp = [self.x + 60, self.y + 5]
        self.tl_dim = [self.x + 20, self.y + 5]

        self.values_d = [v if len(v) <= max_v_len else v[:max_v_len:] + '...' for v in values]
        self.values = values
        self.value_i = init_i

    def render(self, surface):
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 420, 40))

        # draw add btn
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_add, (30, 30)))
        pg.draw.rect(surface, (95, 123, 159), pg.Rect([self.tl_add[0] + 2, self.tl_add[1] + 11], (26, 8)))
        pg.draw.rect(surface, (95, 123, 159), pg.Rect([self.tl_add[0] + 11, self.tl_add[1] + 2], (8, 26)))

        # draw text field
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_disp, (300, 30)))
        surface.blit(FONT_TEXT_NORMAL.render(str(self.values_d[self.value_i]), False, (255, 255, 255)),
                     [self.tl_disp[0] + 5, self.tl_disp[1] + 5])

        # draw dim btn
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.tl_dim, (30, 30)))
        pg.draw.rect(surface, (95, 123, 159), pg.Rect([self.tl_dim[0] + 2, self.tl_dim[1] + 11], (26, 8)))

    def press(self, pos, surface):
        if self.tl_add[0] <= pos[0] <= self.tl_add[0] + 30 and self.tl_add[1] <= pos[1] <= self.tl_add[1] + 30:
            if self.value_i + 1 > len(self.values) - 1:
                self.value_i = 0
            else:
                self.value_i += 1
            self.render(surface)
            return True
        elif self.tl_dim[0] <= pos[0] <= self.tl_dim[0] + 30 and self.tl_dim[1] <= pos[1] <= self.tl_dim[1] + 30:
            if self.value_i - 1 < 0:
                self.value_i = len(self.values) - 1
            else:
                self.value_i -= 1
            self.render(surface)
            return True
        return False

    def disp_press(self, pos):
        if self.tl_disp[0] <= pos[0] <= self.tl_disp[0] + 300 and self.tl_disp[1] <= pos[1] <= self.tl_disp[1] + 30:
            return True
        return False

    def get_value(self):
        return self.values[self.value_i]


class PresetLoader:
    def __init__(self, x, y, path, header):
        self.x = x
        self.y = y

        self.header = header
        self.path = path
        self.files = list(os.listdir(path))
        self.step_disp = StepDisplay(self.x, self.y + 40, self.files, random.randint(0, len(self.files) - 1), 30)

    def render(self, surface):
        # draw board
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 420, 110))
        surface.blit(FONT_TEXT_NORMAL.render(self.header, False, (255, 255, 255)),
                     [self.x + 20, self.y + 10])
        self.step_disp.render(surface)

    def update(self, event, screen):
        self.step_disp.press(event.pos, screen)

        if self.step_disp.disp_press(event.pos):
            self.sound_preview()

    def sound_preview(self):
        pg.mixer.stop()
        pg.mixer.Sound(self.get_file()).play()

    def get_file(self):
        return os.path.join(self.path, self.step_disp.get_value())


class ExportButton:
    def __init__(self, x, y, path_s, path_o):
        self.x = x
        self.y = y
        self.path_s = path_s
        self.path_o = path_o
        self.pressed = False

    def render(self, surface):
        # draw board
        self.pressed = False
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 420, 110))
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.x + 20, self.y + 20, 380, 70))
        surface.blit(FONT_TEXT_BIG.render("EXPORT", False, (255, 255, 255)),
                     [self.x + 110, self.y + 30])

    def render_pressed(self, surface):
        self.pressed = True
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.x + 20, self.y + 20, 380, 70))
        surface.blit(FONT_TEXT_BIG.render("EXPORTED", False, (255, 255, 255)),
                     [self.x + 110, self.y + 30])

    def export_12(self):
        files = [str(_) for _ in os.listdir(self.path_o)]

        filename = 'generated.wav'
        c = 1
        while filename in files:
            filename = 'generated_' + str(c) + '.wav'
            c += 1

        shutil.copy(
            os.path.join(self.path_s, '12.wav'),
            os.path.join(self.path_o, filename)
        )

    def update(self, event, surface):
        pos = event.pos

        if not self.pressed and self.x + 20 <= pos[0] <= self.x + 400 and self.y + 20 <= pos[1] <= self.y + 90:
            self.render_pressed(surface)
            self.export_12()


class GenButton:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, surface):
        # draw board
        pg.draw.rect(surface, (48, 50, 53), pg.Rect(self.x, self.y, 420, 110))
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.x + 20, self.y + 20, 380, 70))
        surface.blit(FONT_TEXT_BIG.render("GENERATE!", False, (255, 255, 255)),
                     [self.x + 110, self.y + 30])

    def render_pressed(self, surface):
        pg.draw.rect(surface, (45, 58, 89), pg.Rect(self.x + 20, self.y + 20, 380, 70))
        surface.blit(FONT_TEXT_BIG.render("GENERATING...", False, (255, 255, 255)),
                     [self.x + 110, self.y + 30])

    def update(self, event, file_1, file_2, piano, exp_btn, surface):
        pos = event.pos

        if self.x + 20 <= pos[0] <= self.x + 400 and self.y + 20 <= pos[1] <= self.y + 90:
            self.render_pressed(surface)
            pg.display.update()
            piano.sounds.sounds = piano.sounds.generate_sounds(file_1, file_2)
            self.render(surface)
            exp_btn.render(surface)

