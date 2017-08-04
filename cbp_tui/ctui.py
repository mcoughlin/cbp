test = False
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Layout, ListBox, Button, Frame, Text, Label
from asciimatics.exceptions import NextScene, StopApplication
if not test:
    import cbp.cbp_instrument as CBP
import logging
import time
from cbp._version import get_versions
import thorlabs
import ConfigParser
import cbp.shutter as shutter


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
        if self.instrument_list_box.value == 3:
            raise NextScene("Keithley")
        if self.instrument_list_box.value == 4:
            raise NextScene("Laser")
        if self.instrument_list_box.value == 9:
            raise NextScene("Shutter")


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
        self.steps_text = Text("Steps")
        self.layout2.add_widget(self.alt_angle_text,0)
        self.layout2.add_widget(self.az_angle_text,0)
        self.layout2.add_widget(self.steps_text)
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
            steps = abs(int(self.steps_text.value))
            cbp.altaz.do_steps(1,-steps)
            logging.info(cbp.altaz.azangle)
            self.az_angle_text.value = str(cbp.altaz.azangle)

    def _right(self):
        if test:
            pass
        else:
            steps = abs(int(self.steps_text.value))
            cbp.altaz.do_steps(1,steps)
            logging.info(cbp.altaz.azangle)
            self.az_angle_text.value = str(cbp.altaz.azangle)

    def _up(self):
        if test:
            pass
        else:
            steps = abs(int(self.steps_text.value))
            cbp.altaz.do_steps(2,steps)
            logging.info(cbp.altaz.altangle)
            self.alt_angle_text.value = str(cbp.altaz.altangle)

    def _down(self):
        if test:
            pass
        else:
            steps = abs(int(self.steps_text.value))
            cbp.altaz.do_steps(2,-steps)
            logging.info(cbp.altaz.altangle)
            self.alt_angle_text.value = str(cbp.altaz.altangle)

    def _display_alt_angle(self):
        if test:
            pass
        else:
            self.alt_angle_text.value = str(cbp.altaz.altangle)

    def _display_az_angle(self):
        if test:
            pass
        else:
            self.az_angle_text.value = str(cbp.altaz.azangle)

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class BirgerView(Frame):
    def __init__(self,screen):
        super(BirgerView, self).__init__(screen,height=screen.height * 2 // 3, width=screen.width * 3 // 3, hover_focus=True,title="Birger View")
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
        self.set_focus_text = Text("Set Focus")
        self.set_aperture_text = Text("Set Birger")
        self.layout2.add_widget(self.focus_text,0)
        self.layout2.add_widget(Label(""),0)
        self.layout2.add_widget(Label(""),0)
        self.layout2.add_widget(self.aperture_text,0)
        self.layout2.add_widget(self.set_focus_text,1)
        self.layout2.add_widget(Button("SET FOCUS",self._focus_up),1)
        self.layout2.add_widget(Label(""),1)
        self.layout2.add_widget(self.set_aperture_text,1)
        self.layout2.add_widget(Button("SET APERTURE",self._aperture_up),1)
        self.fix()

    def _focus_up(self):
        if test:
            pass
        else:
            val = int(self.set_focus_text.value)
            cbp.birger.do_focus(val)
            self.focus_text.value = str(val)

    def _aperture_up(self):
        if test:
            pass
        else:
            val = int(self.set_aperture_text.value)
            cbp.birger.do_aperture(val)
            self.aperture_text.value = str(val)

    def _display_focus(self):
        if test:
            pass
        else:
            focus = cbp.birger.focus
            self.focus_text.value = str(focus)

    def _display_aperture(self):
        if test:
            pass
        else:
            aperture = cbp.birger.aperture
            self.aperture_text.value = str(aperture)

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class FilterWheelView(Frame):
    def __init__(self,screen):
        super(FilterWheelView, self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Filter Wheel View")
        self._screen = screen
        self.filters_dictionary = {None:"None",0:"568 nm inteference",1:"700 nm (10 nm)",2:"671 nm (10 nm)",3:"DECam (2.2 deg)",4:"680 nm (10 nm)"}
        self.masks_dictionary = {None:"None",0:"200 micron slit",1:"20 micron pinhole",2:"ronchi grating",3:"20 micron pinhole decam",4:"USAF target"}
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
        self.set_mask_text = Text("Set Mask")
        self.set_mask_text.disabled = True
        self.set_filter_text = Text("Set Filter")
        self.set_filter_text.disabled = True
        self.set_filter = None
        self.set_mask = None
        self.layout2.add_widget(self.mask_text)
        self.layout2.add_widget(self.filter_text)
        self.layout2.add_widget(Label(""))
        self.layout2.add_widget(self.set_mask_text)
        self.layout2.add_widget(self.set_filter_text)
        self.layout2.add_widget(self.mask_options_list_box,1)
        self.layout2.add_widget(Label(""),1)
        self.layout2.add_widget(self.filter_options_list_box,1)
        self.layout2.add_widget(Button("SET FILTER AND MASK",self._set_filter_and_mask),1)
        self.fix()

    def _set_filter_and_mask(self):
        filter = self.set_filter
        mask = self.set_mask
        cbp.filter_wheel.do_position(mask=mask,filter=filter)
        self.mask_text.value = None
        self.filter_text.value = None

    def _select_filter(self):
        if self.filter_options_list_box.value == 0:
            self.set_filter_text.value = self.filters_dictionary[0]
            self.set_filter = 0
        if self.filter_options_list_box.value == 1:
            self.set_filter_text.value = self.filters_dictionary[1]
            self.set_filter = 1
        if self.filter_options_list_box.value == 2:
            self.set_filter_text.value = self.filters_dictionary[2]
            self.set_filter = 2
        if self.filter_options_list_box.value == 3:
            self.set_filter_text.value = self.filters_dictionary[3]
            self.set_filter = 3
        if self.filter_options_list_box.value == 4:
            self.set_filter_text.value = self.filters_dictionary[4]
            self.set_filter = 4

    def _select_mask(self):
        if self.mask_options_list_box.value == 0:
            self.set_mask_text.value = self.masks_dictionary[0]
            self.set_mask = 0
        if self.mask_options_list_box.value == 1:
            self.set_mask_text.value = self.masks_dictionary[1]
            self.set_mask = 1
        if self.mask_options_list_box.value == 2:
            self.set_mask_text.value = self.masks_dictionary[2]
            self.set_mask = 2
        if self.mask_options_list_box.value == 3:
            self.set_mask_text.value = self.masks_dictionary[3]
            self.set_mask = 3
        if self.mask_options_list_box.value == 4:
            self.set_mask_text.value = self.masks_dictionary[4]
            self.set_mask = 4

    def _display_mask(self):
        if test:
            pass
        else:
            mask = cbp.filter_wheel.mask
            self.mask_text.value = self.masks_dictionary[mask]

    def _display_filter(self):
        if test:
            pass
        else:
            filter = cbp.filter_wheel.filter
            self.filter_text.value = self.filters_dictionary[filter]

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class KeithleyView(Frame):
    def __init__(self,screen):
        super(KeithleyView, self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Keithley View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        self.keithley_text = Text("Keithley 1: ",on_change=self._display_keithley_1)
        self.keithley_text.disabled = True
        # TODO add in keithley 2 text <>
        # TODO disable keithley 2 text <>
        self.duration_text = Text("Duration")
        self.timeseries_text = Text("Timeseries Last Value:")
        self.timeseries_text.disabled = True
        self.layout2.add_widget(self.keithley_text)
        # TODO attach keithley 2 text to layout <>
        self.layout2.add_widget(Button("GET READING",self._get_photodiode_reading))
        # TODO attach keithley 2 get photodiode reading to layout <>
        self.layout2.add_widget(self.duration_text,1)
        self.layout2.add_widget(self.timeseries_text,1)
        self.layout2.add_widget(Button("Get Timeseries",self._get_timeseries),1)
        self.fix()

    # TODO add in keithley 2 display function <>

    def _get_timeseries(self):
        duration = int(self.duration_text.value)
        cbp.keithley.selectmode('char',1)
        times, photosl = cbp.keithley.get_charge_timeseries(duration=duration)
        self.timeseries_text.value = str(photosl[-1])

    def _get_photodiode_reading(self):
        cbp.keithley.selectmode('curr',1)
        cbp.keithley.get_photodiode_reading()
        self.keithley_text.value = None

    # TODO add in keithley 2 photodiode reading function <>

    def _display_keithley_1(self):
        if test:
            pass
        else:
            k = cbp.keithley.photodiode_reading_1
            self.keithley_text.value = str(k)

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class LaserView(Frame):
    def __init__(self,screen):
        super(LaserView, self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Laser View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        self.wavelength_text = Text("Wavelength",on_change=self._display_wavelength)
        self.wavelength_text.disabled = True
        self.set_wavelength_text = Text("Wavelength Set")
        self.layout2.add_widget(self.wavelength_text)
        self.layout2.add_widget(self.set_wavelength_text)
        self.layout2.add_widget(Button("SET WAVELENGTH",self._set_wavelength))
        self.fix()

    def _display_wavelength(self):
        wavelength = str(cbp.laser.wavelength)
        self.wavelength_text.value = wavelength

    def _set_wavelength(self):
        set_wavelength = int(self.set_wavelength_text.value)
        cbp.laser.change_wavelength(set_wavelength)
        self.wavelength_text.value = None
        self.set_wavelength_text.value = ""

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class LockinView(Frame):
    def __init__(self,screen):
        # REVIEW is this view necessary <>
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

class ShutterView(Frame):
    def __init__(self,screen):
        super(ShutterView, self).__init__(screen,screen.height * 2 // 3, screen.width * 3 // 3, hover_focus=True,title="Shutter View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        self.shutter_status_text = Text("Shutter Status",on_change=self._display_shutter_status)
        self.shutter_status_text.disabled = True
        self.flipper_status_text = Text("Flipper Status",on_change=None)
        self.flipper_status_text.disabled = True
        self.shutter_duration_text = Text("duration")
        self.layout2.add_widget(self.shutter_status_text)
        self.layout2.add_widget(self.flipper_status_text)
        self.layout2.add_widget(self.shutter_duration_text)
        self.layout2.add_widget(Button("Shutter OPEN DURATION in milliseconds:",self._open_shutter_duration))
        self.layout2.add_widget(Button("SHUTTER OPEN",self._open_shutter),1)
        self.layout2.add_widget(Button("SHUTTER CLOSE",self._close_shutter),1)
        self.layout2.add_widget(Button("FLIPPER OPEN",self._open_flipper),1)
        self.layout2.add_widget(Button("FLIPPER CLOSE",self._close_flipper),1)
        self.fix()

    def _display_shutter_status(self):
        pass

    def _display_flipper_status(self):
        # FIXME flipper status is not changing <>
        pos, flipper_status = thorlabs.thorlabs.get_flipper()
        logging.info(pos)
        if pos == 1:
            self.flipper_status_text.value = "closed"
        else:
            self.flipper_status_text.value = "open"

    def _open_shutter(self):
        val = -1
        shutter.main(runtype='shutter',val=-1)
        self.shutter_status_text.value = "open"

    def _close_shutter(self):
        val = 0
        shutter.main(runtype='shutter',val=0)
        self.shutter_status_text.value = "closed"

    def _close_flipper(self):
        val = 1
        thorlabs.thorlabs.run_flipper(val)
        self.flipper_status_text.value = "closed"

    def _open_flipper(self):
        val = 2
        thorlabs.thorlabs.run_flipper(val)
        self.flipper_status_text.value = "open"
   
    def _open_shutter_duration(self):
        val = int(self.shutter_duration_text.value)
        shutter.main(runtype='shutter',val=val)

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")

class SpectrographView(Frame):
    # REVIEW is this view necessary <>
    def __init__(self,screen):
        super(SpectrographView, self).__init__(screen,screen.height * 2 // 3, screen.width * 2 // 3, hover_focus=True,title="Spectrograph View")
        self._screen = screen
        self.layout = Layout([1])
        self.add_layout(self.layout)
        self.layout.add_widget(Button("QUIT", self._quit))
        self.layout.add_widget(Button("GO BACK", self._go_back))
        self.layout2 = Layout([1,1])
        self.add_layout(self.layout2)
        # TODO add in duration display <>
        # TODO add in get spectrograph button <>
        self.fix()

    # TODO add in duration display function <>

    # TODO add in get spectrograph button function <>

    def _go_back(self):
        raise NextScene("Main")

    def _quit(self):
        raise StopApplication("User stopped application")


def launch(screen):
    scene = [Scene([MainView(screen)],-1,name="Main"),Scene([AltazView(screen)],-1,name="Altaz"),Scene([BirgerView(screen)],-1,name="Birger"),Scene([FilterWheelView(screen)],-1,name="Filter Wheel"),Scene([KeithleyView(screen)],-1,name="Keithley"),Scene([LaserView(screen)],-1,name="Laser"),Scene([LockinView(screen)],-1,name="Lockin"),Scene([SpectrographView(screen)],-1,name="Spectrograph"),Scene([ShutterView(screen)],-1,name="Shutter")]
    screen.play(scene)


def main():
    logging.basicConfig(filename='{0}_{1}.log'.format('ctui', time.strftime("%m_%d_%Y_%H_%M")), level=logging.DEBUG,format='{0}: {3} in module {2}: {1}'.format('%(asctime)s', '%(message)s', '%(module)s','%(levelname)s'))
    Screen.wrapper(launch)

if not test:
    cbp = CBP.CBP(everything=True)
    config = ConfigParser.RawConfigParser()
    config.read('/home/pi/Code/cbp_2/cbp_tui/ctui.cfg')
    cbp.birger.do_aperture(int(config.get('birger', 'aperture')))
    cbp.birger.do_focus(int(config.get('birger', 'focus')))
    cbp.filter_wheel.do_position(int(config.get('filter wheel', 'mask')), int(config.get('filter wheel', 'filter')))
cbp_instrument_options = [("altaz", 0), ("birger", 1), ("filter wheel", 2), ("keithley", 3), ("laser", 4), ("shutter", 9)]
cbp_instrument_list = ["altaz","birger","filter wheel","keithley","laser","lockin","phidget","photodiode","potentiometer","shutter","spectrograph","temperature","lamp"]
main()
