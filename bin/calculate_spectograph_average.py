import cbp.cbp_class as cbp_instrument

def main():
    output_dir = '/home/pi/CBP/lightsource/7_17_2017/'
    n_averages = 10
    duration = 10000000
    dark = False
    collimated_beam_projector = cbp_instrument.CBP(spectrograph=True)
    collimated_beam_projector.get_spectograph_average(output_dir=output_dir, n_averages=n_averages, duration=duration, dark=dark)

main()
