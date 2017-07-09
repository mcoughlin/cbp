import cbp.cbp_class as cbp_instrument

def main():
    output_dir = '/home/pi/CBP/lightsource/'
    Naverages = 3
    duration = 300000000
    dark = False
    collimated_beam_projector = cbp_instrument.CBP()
    collimated_beam_projector.get_spectograph_average(output_dir=output_dir, Naverages=Naverages, duration=duration, dark=dark)

main()
