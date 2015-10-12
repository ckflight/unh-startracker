# rewriting the center pixel method for use in python
# eliminates the need to do any kind of "circular hough transform" etc.
# 
from __future__ import division
from PIL import Image
import client
import time
import sys
import os
import subprocess
import json
# brittle code. need a way to do relative path idk why the relative path
# isn't working 
sys.path.append('/home/newmy/research/exp/unh-startracker/unh-startracker/analysisAndPlots/maps/')
# print sys.path
import re
import glob
import ST

def extractTimeFromImage(img):
    img = Image.open(img)
    imgTime = img._getexif()
    imgTime = imgTime[36868].split()
    imgTime = imgTime[1].split(':')

    # imgTime is an array of [hr, min, sec] in UTC from the image file
    imgTime =  [float(x) for x in imgTime] 
    return imgTime

def populateImageList():
    imageList = glob.glob('./*.jpg')
    return imageList

def populateWcsList():
    wcsList = glob.glob('./*.wcs')
    return wcsList

def apiGetCalibrationAndStarList(image):
    apiKey = 'lmrqojqbcjrzxkzx'
    c = client.Client()
    c.login(apiKey) 

    # the reason we set equal c.upload to a variable is because it returns a
    # dictionary with the image id in it
    uploadedImage = c.upload(image)
    
    #print "ul image == %s" %uploadedImage
    # time.sleep(30)
    # try to minimize 
    while True: # look forever
        subId =  uploadedImage['subid']
        if subId == None:
            time.sleep(5)
        elif subId != None:
            break
    # print subId
    while True:
        blah = c.sub_status(subId, justdict=True) #NEED TO ACTIVATE THE JUSTDICT = TRUE FLAG 
        try:
            # print "blah =========== %s" %type(blah['jobs'][0])
            if type(blah['jobs'][0]) == int:
                print "TYEP OF blah =========== %s" %type(blah['jobs'])
                jobId = blah['jobs'][0]
                print "jobId =============== %s" % jobId
                break
        except:
            time.sleep(5) 
            pass

    
    print" fuckkk %s" % blah 
    
    # this time.sleep call will need to be more bulletproof
    time.sleep(60) 
    calibration = c.send_request('jobs/%s/calibration' % jobId)
    starList = c.send_request('jobs/%s/annotations' % jobId)
    #while True:
    #    try:
    #        if calibration[''
    #while True:
     #   calibration = c.send_request('jobs/%s/calibration' % jobId)
     #   starList = c.send_request('jobs/%s/annotations' % jobId)
     #   try:
     #       if exists(calibration['parity']):
     #           return [calibration, starList]
     #   except:
     #       time.sleep(5)
     #       pass


# define center pixel constants, pitch calibration and stuff

def makeWcsFiles(image):
    # this function calls astrometry with certain options and puts a .wcs file
    # in the directory specified after '-D'
    subprocess.call(['solve-field', '-p', '--overwrite', '--scale-units',
                    'degwidth', '--scale-low', '25', '--scale-high', '35',
                    '--downsample', '2', '-D', '.', image])

def getStarDictionary(wcsFile):
    # start a star dictionary object (kind of)
    command = ['/usr/local/astrometry/bin/plotann.py', '--brightcat','/home/newmy/research/exp/unh-startracker/astrometry.net-0.50/catalogs/brightstars.fits', 'DSC_0058_NEF_embedded.wcs']#%wcsFile
    print 'command is %s' %command
    sdProc = subprocess.Popen(command, stdout=subprocess.PIPE)
    #sdProc = os.popen(command).read() 
    starDict = sdProc.stdout.read()
    
    # put the dictionary in dictionary (instead of string) form
    starDict = json.loads(starDict)
    print "star dictionary == %s"%type(starDict)
    print starDict[0]
    #return starDict
def computeHcFromImage(calibration, starList):
    rightAscension = calibration['ra']
    declination = calibration['dec']
    pixScale = calibration['pixscale'] # arcsec/pixel
    pixDegrees = pixScale/3600

    imageWidth = 3872 # pix
    imageHeight = 2592 # pix
    xc = imageWidth/2
    yc = imageHeight/2

    #PITCH CALIBRATION SUPER IMPORTANT
    pitch = 62.6 # deg

    # strip 'annotations'
    starList = starList['annotations']

    shortList = [] # make a short list of the stars we're really interested in
    for star in starList:

        # if the star has an alternate name its probably big or bright or both
        if len(star['names'])>1:

            # pixel offsets
            star['xOff'] = star['pixelx'] - xc
            star['yOff'] = yc - star['pixely']
            # rotation will go here

            # Hc (unrolled)
            star['hcu'] = pitch + star['yOff']*pixDegrees
            shortList.append(star)
            print star 
    return star
def doImageProcessing():
    imageList = populateImageList()
    print imageList 
    for image in imageList:
        print image
        makeWcsFiles(image)
    wcsList = populateWcsList()
    #print "wcs list is %s" %wcsList
    for wcs in wcsList:
        aaa = getStarDictionary(wcs)
        print aaa


if __name__ == "__main__":
    
     doImageProcessing()
#    imageList = populateImageList()
#    data = getCalibrationAndStarList(imageList)
#    cal = data[0]
#    sl = data[1]
#    print "cal == %s" %cal
#    print "sl == %s" %sl
#    computeHcFromImage(calibration,starList) 
