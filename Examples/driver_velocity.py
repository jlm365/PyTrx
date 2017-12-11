'''
PYTRX EXAMPLE VELOCITY DRIVER

This script is part of PyTrx, an object-oriented programme created for the 
purpose of calculating real-world measurements from oblique images and 
time-lapse image series.

This driver calculates surface velocities using modules in PyTrx at Kronebreen,
Svalbard, for a subset of the images collected during the 2014 melt season. 
Specifically this script performs feature-tracking through sequential daily 
images of the glacier to derive surface velocities (spatial average, 
individual point displacements and interpolated velocity maps) which have been 
corrected for image distortion and motion in the camera platform (i.e. image
registration).

@author: Penny How (p.how@ed.ac.uk)
         Nick Hulton (nick.hulton@ed.ac.uk)
'''

#Import packages
import sys
import os


#Import PyTrx packages
sys.path.append('../')
from CamEnv import CamEnv
from Measure import Velocity
from FileHandler import writeHomographyFile, writeVelocityFile
from Utilities import plotPX, plotXYZ, interpolateHelper, plotInterpolate


#-------------------------   Map data sources   -------------------------------

#Get data needed for processing
camdata = '../Examples/camenv_data/camenvs/CameraEnvironmentData_KR2_2014.txt'
camvmask = '../Examples/camenv_data/masks/KR2_2014_vmask.JPG'
caminvmask = '../Examples/camenv_data/invmasks/KR2_2014_inv.JPG'
camimgs = '../Examples/images/KR2_2014_subset/demo/*.JPG'


#Define data output directory
destination = '../Examples/results/velocity/'
if not os.path.exists(destination):
    os.makedirs(destination)


#-----------------------   Create camera object   -----------------------------

#Define camera environment
cameraenvironment = CamEnv(camdata, quiet=2)


#----------------------   Calculate velocities   ------------------------------

#Set up Velocity object
velo=Velocity(camimgs, cameraenvironment, camvmask, caminvmask, image0=0, 
            band='L', quiet=2) 


#Calculate homography and velocities    
xyz, uv = velo.calcVelocities()


print '\n\nVelocities calculated for ' + str(len(xyz[0])) + ' image pairs'  
 
  
#----------------------------   Plot Results   --------------------------------

print '\n\nPLOTTING DATA'


method='linear'
cr1 = [446000, 451000, 8754000, 8760000]


for i in range(velo.getLength()-1):
    imn=velo._imageSet[i].getImagePath().split('\\')[1]  
    
    print '\nPlotting image plane output'
    plotPX(velo, i, (destination + 'imgoutput_' + imn), crop=None, show=True)
    
    print 'Plotting XYZ output'
    plotXYZ(velo, i, (destination + 'xyzoutput_' + imn), crop=cr1, 
            show=True, dem=True)

    grid, pointsextent = interpolateHelper(velo,i,method,filt=False)
    fgrid, fpointsextent = interpolateHelper(velo,i,method,filt=True)
        
    print 'Plotting interpolation map (unfiltered)'
    plotInterpolate(velo, i, grid, pointsextent, show=True, 
                    save=destination+'interpunfilter_'+imn, crop=cr1)                      
                        
    print 'Plotting interpolation map (filtered)'
    plotInterpolate(velo, i, fgrid, fpointsextent, show=True, 
                    save=destination+'interpfilter_'+imn, crop=cr1)    


#---------------------------  Export data   -----------------------------------

print '\n\nWRITING DATA TO FILE'

#Write homography data to .csv file
target1 = destination + 'homography.csv'
writeHomographyFile(velo, target1)

#Write out velocity data to .csv file
target2 = destination + 'velo_output.csv'
writeVelocityFile(velo, target2) 


#------------------------------------------------------------------------------

print '\nFinished'