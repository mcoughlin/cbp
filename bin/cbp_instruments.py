import cbp.cbp_instrument
import cbp_interpretator.initialize_cbp

def main():
    cb = cbp.cbp_instrument.CBP()
    cb_parser = cbp_interpretator.initialize_cbp.CbpParser(cbp=cb)
    parser = cb_parser.create_parser()
    args = parser.parse_args()

if __name__ == '__main__':
    main()