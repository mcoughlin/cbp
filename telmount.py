''' Method to handle connections to TheSkyX
'''
from __future__ import print_function

import logging, optparse, time, datetime
import numpy as np
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, error
import ephem

logger = logging.getLogger(__name__)

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-r","--ra",default=5.0,type=float)
    parser.add_option("-d","--dec",default=10.0,type=float)
    parser.add_option("-a","--alt",default=45.0,type=float)
    parser.add_option("-z","--az",default=0.0,type=float)
    parser.add_option("-c","--coordinates",default="altaz")
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

class SkyxObjectNotFoundError(Exception):
    ''' Exception for objects not found in SkyX.
    '''
    def __init__(self, value):
        ''' init'''
        super(SkyxObjectNotFoundError, self).__init__(value)
        self.value = value

    def __str__(self):
        ''' returns the error string '''
        return repr(self.value)


class SkyxConnectionError(Exception):
    ''' Exception for Failures to Connect to SkyX
    '''
    def __init__(self, value):
        ''' init'''
        super(SkyxConnectionError, self).__init__(value)
        self.value = value

    def __str__(self):
        ''' returns the error string '''
        return repr(self.value)


class SkyXConnection(object):
    ''' Class to handle connections to TheSkyX
    '''
    def __init__(self, host="192.168.1.123", port=3040):
        ''' define host and port for TheSkyX.
        '''
        self.host = host
        self.port = port

    def send(self, command):
        ''' sends a js script to TheSkyX and returns the output.
        '''
        try:
            logger.debug(command)
            sockobj = socket(AF_INET, SOCK_STREAM)
            sockobj.connect((self.host, self.port))
            sockobj.send(bytes('/* Java Script */\n' +
                               '/* Socket Start Packet */\n' + command +
                               '\n/* Socket End Packet */\n'))
            oput = sockobj.recv(2048)
            logger.debug(oput)
            sockobj.shutdown(SHUT_RDWR)
            sockobj.close()
            return oput
        except error as msg:
            raise SkyxConnectionError(msg)

    def closedloopslew(self, target):
        ''' Perform a lcosed loop slew.
            Slew, take image, solve, slew, take image, confirm.
        '''
        # 0 on success
        command = '''
            sky6StarChart.Find("''' + target + '''");
            ClosedLoopSlew.exec();
            '''
        oput = self.send(command)
        for line in oput.splitlines():
            if line == "0":
                return True
            if "5005" in line:
                raise SkyxObjectNotFoundError("Object not found.")
            if "Receive time-out" in line:
                raise SkyxObjectNotFoundError("Time out getting image.")
        # God knows if we are here...
        return True

    def takeimages(self, exposure, nimages):
        ''' Take a given number of images of a specified exposure.
        '''
        command = """
        var Imager = ccdsoftCamera;
        function TakeOnePhoto()
        {
            Imager.Connect();
            Imager.ExposureTime = """+str(exposure)+"""
            Imager.Asynchronous = 0;
            Imager.TakeImage();
        }

        function Main()
        {
            for (i=0; i<"""+str(nimages)+"""; ++i)
            {
                TakeOnePhoto();
            }
        }

        Main();
        """
        # TODO
        oput = self.send(command)
        for line in oput.splitlines():
            pass
        pass

    def sky6ObjectInformation(self, target):
        ''' Method to return basic SkyX position information on a target.
        '''
        command = """
                var Target = \"""" + target + """\";
                var Target56 = 0;
                var Target57 = 0;
                var Target58 = 0;
                var Target59 = 0;
                var Target77 = 0;
                var Target78 = 0;
                var Out = "";
                var err;
                sky6StarChart.LASTCOMERROR = 0;
                sky6StarChart.Find(Target);
                err = sky6StarChart.LASTCOMERROR;
                if (err != 0) {
                            Out = Target + " not found."
                } else {
                            sky6ObjectInformation.Property(56);
                            Target56 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(57);
                            Target57 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(58);
                            Target58 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(59);
                            Target59 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(77);
                            Target77 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(78);
                            Target78 = sky6ObjectInformation.ObjInfoPropOut;
                            Out = "sk6ObjInfoProp_RA_2000:"+String(Target56)+
                            "\\nsk6ObjInfoProp_DEC_2000:"+String(Target57)+
                            "\\nsk6ObjInfoProp_AZM:"+String(Target58)+
                            "\\nsk6ObjInfoProp_ALT:"+String(Target59)+
                            "\\nsk6ObjInfoProp_RA_RATE_ASPERSEC:"+String(Target77)+
                            "\\nsk6ObjInfoProp_DEC_RATE_ASPERSEC:"+String(Target78)+"\\n";

                }
                """
        results = {}
        oput = self.send(command)
        for line in oput.splitlines():
            if "Object not found" in line:
                raise SkyxObjectNotFoundError("Object not found.")
            if ":" in line:
                info = line.split(":")[0]
                val = line.split(":")[1]
                results[info] = val
        return results

    def getcurrentradec(self):
        command = """
            var Out;
            sky6RASCOMTele.Connect()
            if (sky6RASCOMTele.isConnected=0)
            {
                out = "Not connected"
            }
            else
            {
                sky6RASCOMTele.GetRaDec()
                Out  = String(sky6RASCOMTele.dRa);
                Out += " " + String(sky6RASCOMTele.dDec);
            }"""

        oput = self.send(command)
        ra = -1
        dec = -1
        for line in oput.splitlines():
            if "|" in line:
                lineSplit = line.split("|")[0]
                lineSplit = lineSplit.split(" ")
                ra = float(lineSplit[0])
                dec = float(lineSplit[1])
        return ra,dec
    def getcurrentaltaz(self):
        command = """
            var Out;
            sky6RASCOMTele.Connect()
            if (sky6RASCOMTele.isConnected=0)
            {
                out = "Not connected"
            }
            else
            {
                sky6RASCOMTele.GetAzAlt()
                Out  = String(sky6RASCOMTele.dAlt);
                Out += " " + String(sky6RASCOMTele.dAz);
            }"""

        oput = self.send(command)
        ra = -1
        dec = -1
        for line in oput.splitlines():
            if "|" in line:
                lineSplit = line.split("|")[0]
                lineSplit = lineSplit.split(" ")
                alt = float(lineSplit[0])
                az = float(lineSplit[1])
        return alt,az

    def gettargetradec(self,target):
        command = """
            /* Java Script */

            var Target = "%s";/*Parameterize*/
            var TargetRA=0;
            var TargetDec=0;
            var Out="";

            var err;

            sky6StarChart.LASTCOMERROR=0;
            sky6StarChart.Find(Target);
            err = sky6StarChart.LASTCOMERROR;

            if (err != 0)
            {
                Out =Target + " not found."
            }
            else
            {
                sky6ObjectInformation.Property(54);/*RA_NOW*/
                TargetRA = sky6ObjectInformation.ObjInfoPropOut;
                sky6ObjectInformation.Property(55);/*DEC_NOW*/
                TargetDec = sky6ObjectInformation.ObjInfoPropOut;

                Out = String(TargetRA) + " "+ String(TargetDec);
            }"""%(target)

        oput = self.send(command)
        ra = -1
        dec = -1
        for line in oput.splitlines():
            if "|" in line:
                lineSplit = line.split("|")[0]
                lineSplit = lineSplit.split(" ")
                ra = float(lineSplit[0])
                dec = float(lineSplit[1])
        return ra,dec

    def gotoradec(self,ra,dec):
        command = """
            /* Java Script */
            var TargetRA = "%.5f";
            var TargetDec = "%.5f";
            var Out;

            sky6RASCOMTele.Connect();
            if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
            {
                Out = "Not connected"
            }
            else
            {
                sky6RASCOMTele.Asynchronous = true;
                sky6RASCOMTele.SlewToRaDec(TargetRA, TargetDec,"");
                Out  = "OK";
            }"""%(ra,dec)
        oput = self.send(command)
        success = -1
        for line in oput.splitlines():
            if "|" in line:
                lineSplit = line.split("|")[0]
                if lineSplit == "OK":
                    success = 1
        return success

    def gotoaltaz(self,alt,az):
        command = """
            /* Java Script */
            var TargetAlt = "%.5f";
            var TargetAz = "%.5f";
            var Out;

            sky6RASCOMTele.Connect();
            if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
            {
                Out = "Not connected"
            }
            else
            {
                sky6RASCOMTele.Asynchronous = true;
                sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt,"");
                Out  = "OK";
            }"""%(alt,az)
        oput = self.send(command)

        success = -1
        for line in oput.splitlines():
            if "|" in line:
                lineSplit = line.split("|")[0]
                if lineSplit == "OK":
                    success = 1
        return success

    def test1(self):
        ''' basic test
        '''
        command = """
/* Java Script */
var Out;
var PropCnt = 189;
var p;

Out="";
sky6StarChart.Find("Saturn");

for (p=0;p<PropCnt;++p)
{
   if (sky6ObjectInformation.PropertyApplies(p) != 0)
    {
        /*Latch the property into ObjInfoPropOut*/
      sky6ObjectInformation.Property(p)

        /*Append into s*/
      Out += sky6ObjectInformation.ObjInfoPropOut + "|"

        //print(p);
   }
}"""
        print (self.send(command))


if __name__ == "__main__":
    HOST, PORT = "localhost", 3040
    xconn = SkyXConnection(host=HOST,port=PORT)
    #print(xconn.sky6ObjectInformation("Saturn"))

    # Parse command line
    opts = parse_commandline()

    target = "Sun"
    #target = "Moon"
    #ra_target, dec_target = xconn.gettargetradec(target)

    if opts.doPosition:
        if opts.coordinates == "altaz":
            alt_target = opts.alt
            az_target = opts.az
            print("Target Altitude: %.5f Azimuth: %.5f\n"%(alt_target,az_target))
            success = xconn.gotoaltaz(alt_target,az_target)
            print("Success: %d\n"%success) 
        else:
            ra_target = opts.ra
            dec_target = opts.dec
            print("Target RA: %.5f Declination: %.5f\n"%(ra_target,dec_target)) 
            success = xconn.gotoradec(ra_target,dec_target)
            print("Success: %d\n"%success)

    if opts.doGetPosition:
        if opts.coordinates == "altaz":
            alt,az = xconn.getcurrentaltaz()
            print("Current Altitude: %.5f Azimuth: %.5f"%(alt,az))
        else:
            ra,dec = xconn.getcurrentradec()
            print("Current RA: %.5f Declination: %.5f"%(ra,dec))

        #utc = time.time()
        #utc_timestamp = datetime.datetime.utcfromtimestamp(utc)
        #utc_date = utc_timestamp.strftime('%Y/%m/%d %H:%M:%S')
        
        #telescope = ephem.Observer()
        # Reversed longitude and latitude for Mauna Kea
        #telescope.lat = '-30:15:06.37' # from Wikipedia
        #telescope.long = '-70:44:17.50'
        #telescope.elevation = 2552.0
        #telescope.date = utc_date
        #star = ephem.FixedBody()
        #star._ra  = ra
        #star._dec = dec
        #star.compute(telescope)
        #alt = float(repr(star.alt)) * (360/(2*np.pi))
        #az = float(repr(star.az)) * (360/(2*np.pi))

    #xconn.test1()   
    #xconn.closedloopslew("Saturn")


