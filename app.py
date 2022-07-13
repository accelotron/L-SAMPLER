import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.font import Font

import os
import pygame as pg
import soundfile as sf

from audio import PianoSounds
from model import ModelWrapperRave


class CustomScale(ttk.Scale):
    def __init__(self, master, **kw):
        kw.setdefault("orient", "horizontal")
        self.variable = kw.pop('variable', tk.DoubleVar(master))
        ttk.Scale.__init__(self, master, variable=self.variable, **kw)
        self._style_name = f"{self}.custom.{kw['orient'].capitalize()}.TScale"
        self['style'] = self._style_name


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # init sounds
        pg.mixer.init(frequency=16000, channels=1)
        self.piano_sounds = None

        # init model
        self.model = ModelWrapperRave('rave-nsynth-epic.ts', 16000)

        # colors
        self.colors = {
            'background': '#000024',
            'accent': '#3240af',
            'highlight': '#5737f5',
            'veryhighlight': '#785EF7'
        }

        # main window
        self.title('L+SAMPLER')
        self['bg'] = self.colors['background']
        self.geometry('512x720')
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # init styles
        self.style = ttk.Style(self)
        self.btn_font = Font(family="FreeSans", size=16, weight='bold')
        self.cmb_font = Font(family="FreeSans", size=8)
        self.img_trough = ImageTk.PhotoImage(Image.open("imgs/trough.png"))
        self.img_slider = ImageTk.PhotoImage(Image.open("imgs/slider.png"))
        self.init_styles()

        # load logo
        self.logo_frame = ttk.Frame(self)
        self.logo_img = ImageTk.PhotoImage(Image.open("imgs/logo.png"))
        self.logo = ttk.Label(self.logo_frame, image=self.logo_img)
        self.logo.grid(row=0, column=0, sticky='n')
        self.logo_frame.grid(row=0, column=0)

        # generation interface
        self.mash_frame = ttk.Frame(self)

        self.samples = os.listdir('samples')

        self.combobox1 = ttk.Combobox(self.mash_frame)
        self.combobox1.bind("<<ComboboxSelected>>", lambda e, c=self.combobox1: self.combo_play(e, c))
        self.combobox1['values'] = self.samples
        self.combobox1.current(0)
        self.combobox1['state'] = 'readonly'
        self.combobox1['width'] = 16
        self.combobox2 = ttk.Combobox(self.mash_frame)
        self.combobox2.bind("<<ComboboxSelected>>", lambda e, c=self.combobox2: self.combo_play(e, c))
        self.combobox2['values'] = self.samples
        self.combobox2.current(0)
        self.combobox2['state'] = 'readonly'
        self.combobox2['width'] = 16

        self.scale = CustomScale(self.mash_frame, from_=0, to=1)

        self.gen_button = ttk.Button(self.mash_frame, command=self.generate_action, text='Generate', style='P.TButton')
        self.exp_button = ttk.Button(self.mash_frame, command=self.export_action, text='Export', style='P.TButton')
        self.rnd_button = ttk.Button(self.mash_frame, command=self.random_action, text='Random', style='P.TButton')

        self.combobox1.grid(row=0, column=0, padx=5, pady=10)
        self.combobox2.grid(row=0, column=2, padx=5, pady=10)
        self.scale.grid(row=0, column=1, padx=5, pady=10, ipadx=25)
        self.rnd_button.grid(row=1, column=0, padx=10, pady=20)
        self.gen_button.grid(row=1, column=1, padx=10, pady=20)
        self.exp_button.grid(row=1, column=2, padx=10, pady=10)

        self.mash_frame.grid(row=1, column=0, sticky='n')

        # # piano
        self.piano_frame = ttk.Frame(self)

        # # piano roll
        self.piano_roll = ttk.Frame(self.piano_frame)
        self.kids_w = tuple([0, 2, 4, 5, 7, 9, 11])
        self.kids_b = tuple([1, 3, 6, 8, 10])
        self.keys_w = 'qwertyu'
        self.keys_b = '23567'
        self.keymap_w = {self.keys_w[i]: i for i in range(len(self.keys_w))}
        self.keymap_b = {self.keys_b[i]: i for i in range(len(self.keys_b))}
        self.btns_w = []
        self.btns_b = []
        self.pixel = tk.PhotoImage(width=1, height=1)

        for i in range(7):
            self.btns_w.append(
                tk.Button(
                    self.piano_roll,
                    image=self.pixel,
                    width=54,
                    height=180,
                    borderwidth=1,
                    relief=tk.FLAT,
                    background='#ffffff',
                    activebackground=self.colors['veryhighlight']
                ))
            self.btns_w[-1]['command'] = lambda x=self.kids_w[i]: self.play_note(x)
            self.btns_w[-1].grid(row=0, column=i, sticky='n')

        for i in range(6):
            if i == 2:
                continue
            self.btns_b.append(
                tk.Button(
                    self.piano_roll,
                    image=self.pixel,
                    width=39,
                    height=105,
                    borderwidth=1,
                    relief=tk.FLAT,
                    background='#000000',
                    activebackground=self.colors['highlight']
                ))
            self.btns_b[-1]['command'] = lambda x=self.kids_b[i if i < 2 else i - 1]: self.play_note(x)
            self.btns_b[-1].grid(row=0, column=i, sticky='n', columnspan=2)

        # bind keyboard
        for key in self.keys_w + self.keys_b:
            self.bind(key, self.press_key)
        self.bind('<KeyRelease>', self.release_key)

        self.piano_roll.grid(row=0, column=0)
        self.piano_frame.grid(row=2, column=0)

    def init_styles(self):
        self.style.theme_use('default')

        # label styles
        self.style.configure(
            'TLabel',
            borderwidth=0,
            font=Font(family="FreeSans", size=16, weight='bold')
        )

        # frame style
        self.style.configure(
            'TFrame',
            background=self.colors['background'],
        )

        # button styles
        self.style.configure(
            'P.TButton',
            foreground='#ffffff',
            background=self.colors['accent'],
            borderwidth=2,
            bordercolor='#ffffff',
            relief=tk.GROOVE,
            font=self.btn_font
        )
        self.style.map(
            'P.TButton',
            background=[('pressed',  self.colors['veryhighlight']), ('active', self.colors['highlight'])],
            borderwidth=[('pressed', 2), ('active', 2)],
            bordercolor=[('pressed', '#ffffff'), ('active', '#ffffff')],
            relief=[('pressed', tk.GROOVE), ('active', tk.GROOVE)],
        )

        # combobox style
        self.option_add('*TCombobox*Listbox.font', self.cmb_font)

        self.style.configure(
            'TCombobox',
            background=self.colors['highlight'],
            arrowcolor='#ffffff',
            selectbackground=self.colors['veryhighlight'],
        )
        self.style.map(
            'TCombobox',
            fieldbackground=[('readonly', self.colors['veryhighlight'])],
            foreground=[('readonly', "#ffffff")],
            background=[('readonly', self.colors['highlight'])]
        )
        self.style.configure(
            "Vertical.TScrollbar",
            background=self.colors['veryhighlight'],
            bordercolor="#ffffff",
            arrowcolor="#ffffff"
        )

        # slider styles
        self.style.element_create('custom.Scale.trough', 'image', self.img_trough)
        self.style.element_create('custom.Scale.slider', 'image', self.img_slider)
        self.style.layout('custom.Horizontal.TScale', [
            ('custom.Scale.trough', {'sticky': 'ew'}),
            ('custom.Scale.slider', {'side': 'left', 'sticky': '', })
        ])
        self.style.configure(
            'custom.Horizontal.TScale',
            width=10,
            background=self.colors['background'],
        )
        self.style.map(
            'custom.Horizontal.TScale',
            background=[('pressed',  self.colors['background']), ('active', self.colors['background'])]
        )

    def press_key(self, event):
        key = event.keysym.lower()
        print(key, 'pressed')

        if key in self.keys_w:
            btn = self.btns_w[self.keymap_w[key]]
            btn.invoke()
            btn['background'] = self.colors['veryhighlight']

        if key in self.keys_b:
            btn = self.btns_b[self.keymap_b[key]]
            btn.invoke()
            btn['background'] = self.colors['highlight']

    def release_key(self, event):
        key = event.keysym.lower()

        if key in self.keys_w:
            btn = self.btns_w[self.keymap_w[key]]
            btn['background'] = '#ffffff'

        if key in self.keys_b:
            btn = self.btns_b[self.keymap_b[key]]
            btn['background'] = '#000000'

    def play_note(self, note_id):
        print('Note played', note_id)
        if self.piano_sounds:
            self.piano_sounds.play_sound(note_id)

    def combo_play(self, e, combobox):
        print('Sound played', combobox.get())
        pg.mixer.stop()
        pg.mixer.Sound(os.path.join('samples', combobox.get())).play()

    def generate_action(self):
        print('Generate', self.scale.get(), self.combobox1.get(), self.combobox2.get())
        root = self.model.mash_two(
            os.path.join('samples', self.combobox1.get()),
            os.path.join('samples', self.combobox2.get()),
            self.scale.get()
        )
        self.piano_sounds = PianoSounds(root, 16000)
        self.piano_sounds.play_sound(0)

    def export_action(self):
        filename = 'generated.wav'
        c = 1
        while filename in os.listdir('outputs'):
            filename = 'generated_' + str(c) + '.wav'
            c += 1

        sf.write(os.path.join("outputs", filename), self.piano_sounds.root, 16000)
        print('Export', filename)

    def random_action(self):
        print('Random sound')
        root = self.model.random_gen()
        self.piano_sounds = PianoSounds(root, 16000)
        self.piano_sounds.play_sound(0)


if __name__ == "__main__":
    app = App()
    # https://stackoverflow.com/questions/27215326/tkinter-keypress-and-keyrelease-events
    # Prevents bug so <KeyPress> event appears once
    # Works, but user can't use keyboard as usual, needs to be fixed
    os.system('xset r off')
    if not os.path.exists('outputs'):
        os.mkdir('outputs')
    try:
        app.mainloop()
    finally:
        os.system('xset r on')
