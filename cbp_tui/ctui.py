test = True
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Layout, ListBox, Button, Frame, Text, Label
from asciimatics.exceptions import NextScene, StopApplication
if not test:
    import cbp.cbp_instrument as CBP
import logging
import time
from cbp._version import get_versions


class MainView(Frame):
    def __init__(self,screen):
        super(MainView,self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Main View")
        self._screen = screen
        self.main_button_layout = Layout([1])
        self.add_layout(self.main_button_layout)
        self.main_button_layout.add_widget(Label('Version:{0}'.format(get_versions()['version'])))
        self.main_button_layout.add_widget(Button("QUIT",self._quit))
        self.instrument_list_layout = Layout([1])
        height = 4
        options = cbp_instrument_options
        self.instrument_list_box = ListBox(height=height,options=options,on_select=self._instrument_select)
        self.add_layout(self.instrument_list_layout)
        self.instrument_list_layout.add_widget(self.instrument_list_box)
        self.status_layout = Layout([1,1])
        self.add_layout(self.status_layout)
        self.instument_text_dictionary = {}
        for idx, item in enumerate(cbp_instrument_list):
            instrument_text = Text("{0}".format(item),name=item,on_change=self._display_status)
            instrument_text.disabled = True
            self.instument_text_dictionary[item] = instrument_text
            self.status_layout.add_widget(instrument_text,0 if idx < 5 else 1)
        self.fix()

    def _display_status(self):
        if test:
            pass
        else:
            for key, item in cbp.instrument_dictionary.iteritems():
                self.instument_text_dictionary[key].value = cbp.instrument_dictionary[key].status

    def _quit(self):
        raise StopApplication("User stopped application")

    def _instrument_select(self):
        if self.instrument_list_box.value == 0:
            raise NextScene("Altaz")
        if self.instrument_list_box.value == 1:
            raise NextScene("Birger")
        if self.instrument_list_box.value == 2:
            raise NextScene("Filter Wheel")


class AltazView(Frame):
    def __init__(self,screen):
        super(AltazView, self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Altaz View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT",self._quit))
        self.layout.add_widget(Button("GO BACK",self._go_back))
        self.layout2 = Layout([1,1,1,1])
        self.add_layout(self.layout2)
        self.alt_angle_text = Text("Alt Angle",on_change=self._display_alt_angle)
        self.alt_angle_text.disabled = True
        self.az_angle_text = Text("Az Angle",on_change=self._display_az_angle)
        self.az_angle_text.disabled = True
        self.layout2.add_widget(self.alt_angle_text,0)
        self.layout2.add_widget(self.az_angle_text,0)
        self.layout2.add_widget(Button(u"\u2191",self._up),2)
        self.layout2.add_widget(Label(""),2)
        self.layout2.add_widget(Button(u"\u2193",self._down),2)
        self.layout2.add_widget(Label(""),1)
        self.layout2.add_widget(Button(u"\u2190",self._left),1)
        self.layout2.add_widget(Label(""),3)
        self.layout2.add_widget(Button(u"\u2192",self._right),3)
        self.fix()

    def _left(self):
        if test:
            pass
        else:
            cbp.altaz.do_steps(1,-100)

    def _right(self):
        if test:
            pass
        else:
            cbp.altaz.do_steps(1,100)

    def _up(self):
        if test:
            pass
        else:
            cbp.altaz.do_steps(2,100)

    def _down(self):
        if test:
            pass
        else:
            cbp.altaz.do_steps(2,-100)

    def _display_alt_angle(self):
        if test:
            pass
        else:
            self.az_angle_text.value = str(cbp.altaz.do_azangle())

    def _display_az_angle(self):
        if test:
            pass
        else:
            self.alt_angle_text.value = str(cbp.altaz.do_altangle())

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class BirgerView(Frame):
    def __init__(self,screen):
        super(BirgerView, self).__init__(screen,height=screen.height * 2 // 3, width=screen.width * 2 // 3, hover_focus=True,title="Birger View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        self.focus_text = Text("Focus",on_change=self._display_focus)
        self.focus_text.disabled = True
        self.aperture_text = Text("Aperture",on_change=self._display_aperture)
        self.aperture_text.disabled = True
        self.layout2.add_widget(self.focus_text,0)
        self.layout2.add_widget(Label(""),0)
        self.layout2.add_widget(Label(""),0)
        self.layout2.add_widget(self.aperture_text,0)
        self.layout2.add_widget(Button(u"\u2191",self._focus_up),1)
        self.layout2.add_widget(Button(u"\u2193",self._focus_down),1)
        self.layout2.add_widget(Label(""),1)
        self.layout2.add_widget(Button(u"\u2191",self._aperture_up),1)
        self.layout2.add_widget(Button(u"\u2193",self._aperture_down),1)
        self.fix()

    def _focus_up(self):
        if test:
            pass
        else:
            cf = cbp.birger.do_status()
            cbp.birger.do_focus(cf[0]+1)

    def _focus_down(self):
        if test:
            pass
        else:
            cf = cbp.birger.do_status()
            cbp.birger.do_focus(cf[0]-1)

    def _aperture_up(self):
        if test:
            pass
        else:
            ca = cbp.birger.do_status()
            cbp.birger.do_aperture(ca[1]+10)

    def _aperture_down(self):
        if test:
            pass
        else:
            ca = cbp.birger.do_status()
            cbp.birger.do_aperture(ca[1]-10)

    def _display_focus(self):
        if test:
            pass
        else:
            focus = cbp.birger.do_status()
            self.focus_text.value = str(focus[0])

    def _display_aperture(self):
        if test:
            pass
        else:
            aperture = cbp.birger.do_status()
            self.aperture_text.value = str(aperture[1])

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class FilterWheelView(Frame):
    def __init__(self,screen):
        super(FilterWheelView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Filter Wheel View")
        self._screen = screen
        self.filters_dictionary = {0:"568 nm inteference",1:"700 nm (10 nm)",2:"671 nm (10 nm)",3:"DECam (2.2 deg)",4:"680 nm (10 nm)"}
        self.masks_dictionary = {0:"200 micron slit",1:"20 micron pinhole",2:"ronchi grating",3:"20 micron pinhole decam",4:"USAF target"}
        self.filter_options = [("568 nm inteference",0),("700 nm (10 nm)",1),("671 nm (10 nm)",2),("DECam (2.2 deg)",3),("680 nm (10 nm)",4)]
        self.mask_options = [("200 micron slit",0),("20 micron pinhole",1),("ronchi grating",2),("20 micron pinhole decam",3),("USAF target",4)]
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        self.mask_text = Text("Mask",on_change=self._display_mask)
        self.mask_text.disabled = True
        self.filter_text = Text("Filter", on_change=self._display_filter)
        self.filter_text.disabled = True
        self.filter_options_list_box = ListBox(label="Filter Options",height=len(self.filter_options),options=self.filter_options,on_select=self._select_filter)
        self.mask_options_list_box = ListBox(label="Mask Options",height=len(self.mask_options),options=self.mask_options,on_select=self._select_mask)
        self.layout2.add_widget(self.mask_text)
        self.layout2.add_widget(self.filter_text)
        self.layout2.add_widget(self.mask_options_list_box,1)
        self.layout2.add_widget(Label(""),1)
        self.layout2.add_widget(self.filter_options_list_box,1)
        self.fix()

    def _select_filter(self):
        if self.filter_options_list_box.value == 0:
            cbp.filter_wheel.filter = 0
        if self.filter_options_list_box.value == 1:
            cbp.filter_wheel.filter = 1
        if self.filter_options_list_box.value == 2:
            cbp.filter_wheel.filter = 2
        if self.filter_options_list_box.value == 3:
            cbp.filter_wheel.filter = 3
        if self.filter_options_list_box.value == 4:
            cbp.filter_wheel.filter = 4

    def _select_mask(self):
        if self.mask_options_list_box.value == 0:
            cbp.filter_wheel.mask = 0
        if self.mask_options_list_box.value == 1:
            cbp.filter_wheel.mask = 1
        if self.mask_options_list_box.value == 2:
            cbp.filter_wheel.mask = 2
        if self.mask_options_list_box.value == 3:
            cbp.filter_wheel.mask = 3
        if self.mask_options_list_box.value == 4:
            cbp.filter_wheel.mask = 4

    def _display_mask(self):
        if test:
            pass
        else:
            mask, filter = cbp.filter_wheel.get_position()
            self.mask_text.value = self.masks_dictionary[mask]

    def _display_filter(self):
        if test:
            pass
        else:
            mask, filter = cbp.filter_wheel.get_position()
            self.filter_text.value = self.filters_dictionary[filter]

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class KeithleyView(Frame):
    def __init__(self,screen):
        super(KeithleyView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Keithley View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.fix()

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class LaserView(Frame):
    def __init__(self,screen):
        super(LaserView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Laser View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.fix()

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class LockinView(Frame):
    def __init__(self,screen):
        super(LockinView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Lockin View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.fix()

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class PhidgetView(Frame):
    def __init__(self,screen):
        super(PhidgetView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Phidget View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.fix()

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class SpectrographView(Frame):
    def __init__(self,screen):
        super(SpectrographView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Spectrograph View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.fix()

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")


def launch(screen):
    scene = [Scene([MainView(screen)],-1,name="Main"),Scene([AltazView(screen)],-1,name="Altaz"),Scene([BirgerView(screen)],-1,name="Birger"),Scene([FilterWheelView(screen)],-1,name="Filter Wheel"),Scene([KeithleyView(screen)],-1,name="Keithley"),Scene([LaserView(screen)],-1,name="Laser"),Scene([LockinView(screen)],-1,name="Lockin"),Scene([PhidgetView(screen)],-1,name="Phidget"),Scene([SpectrographView(screen)],-1,name="Spectrograph")]
    screen.play(scene)


def main():
    logging.basicConfig(filename='{0}_{1}.log'.format('foo', time.strftime("%m_%d_%Y")), level=logging.DEBUG,format='{0}: {3} in module {2}: {1}'.format('%(asctime)s', '%(message)s', '%(module)s','%(levelname)s'))
    Screen.wrapper(launch)

if not test:
    cbp = CBP.CBP(everything=True)
cbp_instrument_options = [("altaz", 0), ("birger", 1), ("filter wheel", 2), ("keithley", 3), ("laser", 4), ("lockin", 5),("phidget", 6), ("photodiode", 7), ("shutter", 8), ("spectrograph", 9)]
cbp_instrument_list = ["altaz","birger","filter wheel","keithley","laser","lockin","phidget","photodiode","shutter","spectrograph"]
main()
