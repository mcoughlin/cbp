from asciimatics.screen import *
from asciimatics.scene import *
from asciimatics.widgets import *
from asciimatics.exceptions import *
import logging


class QuitButton(Button):
    def __init__(self):
        super(QuitButton, self).__init__("QUIT", self._quit)
        logging.info("QuitButton Initialized")

    def _quit(self):
        raise StopApplication("User stopped application")


class GoBackButton(Button):
    def __init__(self):
        super(GoBackButton, self).__init__("GO BACK", self._go_back)

    def _go_back(self):
        raise NextScene("Main")


class MainButtonLayout(Layout):
    def __init__(self, frame):
        super(MainButtonLayout, self).__init__([1, 1])
        self._frame = frame
        logging.info("MainButtonLayout Initialized")

    def complete_layout(self):
        self.add_widget(QuitButton(), 1)


class StatusText(Text):
    def __init__(self, item):
        super(StatusText, self).__init__(label=item, name=item, on_change=self.display)
        self.disabled = True

    def display(self):
        self.value = str(1)


class StatusLayout(Layout):
    def __init__(self, frame):
        super(StatusLayout, self).__init__([1, 1])
        self._frame = frame

    def complete_layout(self):
        for idx, item in enumerate(
                ["altaz", "birger", "filter wheel", "keithley", "laser", "lockin", "phidget", "photodiode", "shutter",
                 "spectrograph"]):
            self.add_widget(StatusText("{0}".format(item)), 0 if idx < 5 else 1)


class InstrumentListBox(ListBox):
    def __init__(self):
        height = 4
        options = [("altaz", 0), ("birger", 1), ("filter wheel", 2), ("keithley", 3), ("laser", 4), ("lockin", 5),
                   ("phidget", 6), ("photodiode", 7), ("shutter", 8), ("spectrograph", 9)]
        super(InstrumentListBox, self).__init__(height, options, on_select=self._select)

    def _select(self):
        if self.value == 0:
            raise NextScene("Altaz")


class InstrumentListLayout(Layout):
    def __init__(self, frame):
        super(InstrumentListLayout, self).__init__([1])
        self._frame = frame

    def complete_layout(self):
        self.add_widget(InstrumentListBox())


class MainView(Frame):
    def __init__(self, screen):
        super(MainView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,
                                       title="Main View")
        self._screen = screen
        main_button_layout = MainButtonLayout(self)
        self.add_layout(main_button_layout)
        main_button_layout.complete_layout()
        self.instrument_list_layout = InstrumentListLayout(self)
        self.add_layout(self.instrument_list_layout)
        self.instrument_list_layout.complete_layout()
        status_layout = StatusLayout(self)
        self.add_layout(status_layout)
        status_layout.complete_layout()
        self.fix()


class AltazView(Frame):
    def __init__(self, screen):
        super(AltazView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,
                                        title="Altaz View")
        self._screen = screen
        main_button_layout = MainButtonLayout(self)
        main_button_layout.complete_layout()
        main_button_layout.add_widget(GoBackButton(), 0)
        self.add_layout(main_button_layout)
        self.fix()


def test(screen):
    scene = [Scene([MainView(screen)], -1, name="Main"), Scene([AltazView(screen)], -1, name="Altaz")]
    screen.play(scene)


def main():
    logging.basicConfig(filename='{0}_{1}.log'.format('foo', time.strftime("%m_%d_%Y")), level=logging.DEBUG,
                        format='{0}: {3} in module {2}: {1}'.format('%(asctime)s', '%(message)s', '%(module)s',
                                                                    '%(levelname)s'))
    Screen.wrapper(test)


main()
