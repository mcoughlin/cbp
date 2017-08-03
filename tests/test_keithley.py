import visa
import cbp.keithley
import pytest

@pytest.fixture(scope='module')
def keithley_1():
    keithley_1 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=0,do_reset=True)
    return keithley_1

@pytest.fixture(scope='module')
def keithley_2():
    keithley_2 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=1,do_reset=True)
    return keithley_2

def test_connection_1(keithley_1):
    assert(keithley_1.status[0]=="connected")

def test_connection_2(keithley_2):
    assert(keithley_2.status[1]=="connected")

def test_reading_1(keithley_1):
    assert(keithley_1.get_photodiode_reading() != None)

def test_reading_2(keithley_2):
    assert(keithley_2.get_photodiode_reading() != None)