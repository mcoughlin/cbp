
wavelength=$1
time=$2
cbpshutter=$3
pitmplogfile=$4

ssh pi@139.229.12.11 "cd /home/pi/Code/cbp/bin; python instimage.py -v --doLog -t duration -d $time -s $cbpshutter -w $wavelength -f /tmp/test.dat"
scp pi@139.229.12.11:/tmp/test.dat $pitmplogfile

