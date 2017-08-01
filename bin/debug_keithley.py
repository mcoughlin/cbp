#!/usr/bin/env python
import cbp.cbp_instrument as CBP

def main():
   cbp = CBP.CBP(keithley=True)
   print(cbp.keithley.ins.query('READ?'))

main()
