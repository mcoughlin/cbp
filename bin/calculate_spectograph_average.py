import cbp.cbp_class as cbp_instrument

def main():
    output_dir = '/home/pi/CBP/keithley'
    num_averages = 3
    duration = 1000000
    collimated_beam_projector = cbp_instrument.CBP()
    collimated_beam_projector.get_spectograph_average(output_dir=output_dir, num_averages=num_averages, duration=duration)