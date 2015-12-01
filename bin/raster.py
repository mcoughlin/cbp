#!/usr/bin/env python

import os, serial, sys, time, glob, struct, warnings
import numpy as np
import optparse

import matplotlib
#matplotlib.rc('text', usetex=True)
hostname = os.uname()[1]
if not hostname == "raspberrypi":
    matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 16})
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib import cm as cmx
from matplotlib import colors

try:
    import FLI
except:
    warnings.warn('FLI import failed... cannot use filter wheel or focuser...\n')

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--xmin",default=30.0,type=float)
    parser.add_option("--xmax",default=230.0,type=float)
    parser.add_option("--dx",default=10.0,type=float)

    parser.add_option("--ymin",default=30.0,type=float)
    parser.add_option("--ymax",default=230.0,type=float)
    parser.add_option("--dy",default=20.0,type=float)

    parser.add_option("--x0",default=130.0,type=float)
    parser.add_option("--y0",default=130.0,type=float)
    parser.add_option("--rmin",default=0.0,type=float)
    parser.add_option("--rmax",default=120.0,type=float)

    parser.add_option("--zmin",default=0,type=int)
    parser.add_option("--zmax",default=100000,type=int)
    parser.add_option("--dz",default=10000,type=float)

    parser.add_option("--thetamin",default=-0.00001,type=float)
    parser.add_option("--thetamax",default=0.00001,type=float)
    parser.add_option("--dtheta",default=0.00001,type=float)
    
    parser.add_option("--phimin",default=-0.00001,type=float)
    parser.add_option("--phimax",default=0.00001,type=float)
    parser.add_option("--dphi",default=0.00001,type=float)

    parser.add_option("--altmin",default=29.0,type=float)
    parser.add_option("--altmax",default=31.0,type=float)
    parser.add_option("--dalt",default=1.0,type=float)

    parser.add_option("--azmin",default=299.0,type=float)
    parser.add_option("--azmax",default=301.0,type=float)
    parser.add_option("--daz",default=1.0,type=float)

    parser.add_option("--doRaster", action="store_true",default=False)
    parser.add_option("-r","--rasterType",default="XY")
    parser.add_option("--doLog", action="store_true",default=False)
    parser.add_option("--doPlots", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()

types = ["XY","Radial","Focuser","TipTilt","AltAz"]
if not opts.rasterType in types:
    raise Exception("%s is not a valid raster type... please choose from %s..."%(opts.rasterType,",".join(types)))

if opts.doLog:
    if not hostname == "raspberrypi":
        baseDir = '/Users/allsky/Desktop/CBP'
    else:
        baseDir = '/home/pi/CBP'

    if not os.path.isdir(baseDir):
        os.mkdir(baseDir)
    logDir = os.path.join(baseDir,'logs')
    if not os.path.isdir(logDir):
        os.mkdir(logDir)
    plotDir = os.path.join(baseDir,'plots')
    if not os.path.isdir(plotDir):
        os.mkdir(plotDir)

    logNumber = len(glob.glob(os.path.join(logDir,'raster_log_*')))
    #logNumber = 5
    logFile = os.path.join(os.path.join(logDir,'raster_log_%d.txt'%logNumber))

if opts.doRaster:
    if opts.doLog:
        fid = open(logFile,'w')

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

    elif opts.rasterType == "Radial":
        xs = np.arange(opts.xmin,opts.xmax+opts.dx,opts.dx)
        ys = np.arange(opts.ymin,opts.ymax+opts.dy,opts.dy)

        for x in xs:
            for y in ys:

                r = np.sqrt((x-opts.x0)**2 + (y-opts.y0)**2) 
                if (r >= opts.rmin) and (r <= opts.rmax):
                    print "Current Position: %.5f, %.5f"%(x,y)
                    sys_command = "python zaber_daisy.py --doPosition -d 1 -p %.5f"%(x)
                    os.system(sys_command)
                    sys_command = "python zaber_daisy.py --doPosition -d 2 -p %.5f"%(y)
                    os.system(sys_command)

                    if opts.doLog:
                        try:
                            val = float(raw_input('Value? '))
                        except:
                            val = 0.0

                        fid.write('%.5f,%.5f,%.5f\n'%(x,y,val))

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

        theta0 = 0.0
        phi0 = 0.0
        for phi in phis:
            for theta in thetas:
                print "Current Position (phi,theta): %.5f, %.5f"%(phi,theta)
                sys_command = "python tiptilt.py --doAngle -t %.5f -p %.5f"%(theta-theta0,phi-phi0)
                os.system(sys_command)
                raw_input("Press enter when ready.")
                theta0 = theta
                phi0 = phi 
 
    elif opts.rasterType == "AltAz":
        alts = np.arange(opts.altmin,opts.altmax+opts.dalt,opts.dalt)
        azs = np.arange(opts.azmin,opts.azmax+opts.daz,opts.daz)
        
        for alt in alts:
            for az in azs:
                print "Current Position (alt,az): %.5f, %.5f"%(alt,az)
                sys_command = "python telmount.py --doSSH --doPosition -a %.5f -z %.5f"%(alt,az)
                os.system(sys_command)
                raw_input("Press enter when ready.")

    if opts.doLog:
        fid.close()

if opts.doLog and opts.doPlots:
    data = np.loadtxt(logFile,delimiter=',')

    plotName = os.path.join(os.path.join(plotDir,'scatter_%d.png'%logNumber)) 
    plt.figure()
    plt.scatter(data[:,0],data[:,1],s=20,c=data[:,2], alpha = 0.5)
    plt.xlabel("X [mm]")
    plt.ylabel("y [mm]")
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Photodiode Current [nA]')
    plt.savefig(plotName)
    plt.close()
   
    r = np.sqrt((data[:,0]-130.0)**2 + (data[:,1]-130.0)**2)
    plotName = os.path.join(os.path.join(plotDir,'radial_%d.png'%logNumber))
    plt.figure()
    plt.plot(r,data[:,2], 'kx')
    plt.xlabel("Radius [mm]")
    plt.ylabel("Photodiode Current [nA]")
    plt.savefig(plotName)
    plt.close() 
