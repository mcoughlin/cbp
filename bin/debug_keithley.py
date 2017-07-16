import cbp.cbp_class as CBP

def main():
   cbp = CBP.CBP(keithley=True)
   print(cbp.keithley.ins.query('READ?'))

main()
