#!/usr/bin/env python

import os, serial, sys, time, glob, struct
import numpy as np
import optparse
import FLI

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--xmin",default=34.0,type=float)
    parser.add_option("--xmax",default=36.0,type=float)
    parser.add_option("--dx",default=1.0,type=float)

    parser.add_option("--ymin",default=34.0,type=float)
    parser.add_option("--ymax",default=36.0,type=float)
    parser.add_option("--dy",default=1.0,type=float)

    parser.add_option("--zmin",default=0,type=int)
    parser.add_option("--zmax",default=100000,type=int)
    parser.add_option("--dz",default=10000,type=float)

    parser.add_option("--thetamin",default=-1.0,type=float)
    parser.add_option("--thetamax",default=1.0,type=float)
    parser.add_option("--dtheta",default=1.0,type=float)
    
    parser.add_option("--phimin",default=-1.0,type=float)
    parser.add_option("--phimax",default=1.0,type=float)
    parser.add_option("--dphi",default=1.0,type=float)

    parser.add_option("--altmin",default=45.0,type=float)
    parser.add_option("--altmax",default=55.0,type=float)
    parser.add_option("--dalt",default=5.0,type=float)

    parser.add_option("--azmin",default=0.0,type=float)
    parser.add_option("--azmax",default=5.0,type=float)
    parser.add_option("--daz",default=10.0,type=float)

    parser.add_option("--doRaster", action="store_true",default=False)
    parser.add_option("-r","--rasterType",default="XY")

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()

if opts.doRaster:
    if opts.rasterType == "XY":
        xs = np.arange(opts.xmin,opts.xmax+opts.dx,opts.dx)
        ys = np.arange(opts.ymin,opts.ymax+opts.dy,opts.dy)
        
        for x in xs:
            for y in ys: 
                print "Current Position: %.5f, %.5f"%(x,y)
                sys_command = "python zaber.py --doPosition -d 1 -p %.5f"%(x)
                os.system(sys_command)
                sys_command = "python zaber.py --doPosition -d 2 -p %.5f"%(y)
                os.system(sys_command)
                raw_input("Press enter when ready.")

    elif opts.rasterType == "Focuser":
        zs = np.arange(opts.zmin,opts.zmax+opts.dz,opts.dz)

        for z in zs:
            print "Current Position: %.5f"%(z)
            sys_command = "python focuser.py --doPosition -p %d"%z
            os.system(sys_command)
            raw_input("Press enter when ready.")

    elif opts.rasterType == "TipTilt":
        thetas = np.arange(opts.thetamin,opts.thetamax+opts.dtheta,opts.dtheta)
        phis = np.arange(opts.phimin,opts.phimax+opts.dphi,opts.dphi)

        for phi in phis:
            for theta in thetas:
                print "Current Position (phi,theta): %.5f, %.5f"%(phi,theta)
                sys_command = "python tiptilt.py --doAngle -t %.5f -p %.5f"%(theta,phi)
                os.system(sys_command)
                raw_input("Press enter when ready.")
 
    elif opts.rasterType == "AltAz":
        alts = np.arange(opts.altmin,opts.altmax+opts.dalt,opts.dalt)
        azs = np.arange(opts.azmin,opts.azmax+opts.daz,opts.daz)
        
        for alt in alts:
            for az in azs:
                print "Current Position (alt,az): %.5f, %.5f"%(alt,az)
                sys_command = "python telmount.py --doSSH --doPosition -a %.5f -z %.5f"%(alt,az)
                os.system(sys_command)
                raw_input("Press enter when ready.")

