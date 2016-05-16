#!/usr/bin/env python
#__auther_of 1st_version___ = ('xiao yang / xyangk','Feb 18th','2016')
#__auther_of 2nd_version___ = ('bitpeach','May 16th','2016')

from __future__ import division
import re
import urllib2
import time
import json
import subprocess
import os
from PIL import Image

ORIGINAL_IMG_WIDTH      = 550 # Please do not revise this.
ORIGINAL_IMG_HEIGHT     = 550 # Please do not revise this.
DESKTOP_LONG            = 1920 # It is your size of desktop. if HOW_MANY_D is set as 1, the size of 1280 * 800 maybe enough.
DESKTOP_SHORT           = 1200 # Please remeber that if HOW_MANY_D is set as 2, the size of 1920 * 1200 maybe suitable for Macbook Pro.
Your_Cloud_Account_Name = "XXXX" # Here is your real cloud account name.
HOW_MANY_D = 2 # If the pictures from Himawari-8 satellite consist 2 sub-parts, so the HOW_MANY_D is set as 2. 
AUTO_REMOVE = True # If you want to delete the old version pictures automatically, you can set AUTO_REMOVE as True.



def download_img():
    url_temp = 'http://himawari8.nict.go.jp/img/D531106/latest.json'
    request_temp = urllib2.Request(url_temp)
    response_temp = urllib2.urlopen(request_temp)
    data_temp = response_temp.read()

    #decode json
    json_dec = json.JSONDecoder()
    json_result = json_dec.decode(data_temp)
    date_ = str(json_result['date'])

    #get date
    pattern = re.compile(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')
    result = re.search(pattern, str(date_))
    if result:
        year = result.group(1)
        month = result.group(2)
        day = result.group(3)
        hour = result.group(4)
        minute = result.group(5)
        second = result.group(6)
    else:
        pass



    #Download picture that just has the earth
    url_half = "http://res.cloudinary.com/" + Your_Cloud_Account_Name + "/image/fetch/http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/%s/%s/%s/%s%s%s_" % (year, month, day, hour, minute, second)

    Fusion_2d_Image = Image.new('RGBA',(ORIGINAL_IMG_WIDTH * 2, ORIGINAL_IMG_HEIGHT * 2))
    
    for row in range(HOW_MANY_D):
        for column in range(HOW_MANY_D):
            url_rest_half = "%s_%s.png" % (row, column)
            request_img = urllib2.Request(url_half + url_rest_half)
            response_img = urllib2.urlopen(request_img)
            data_img = Image.open(response_img)
            Fusion_2d_Image.paste(data_img, (row * ORIGINAL_IMG_WIDTH, column * ORIGINAL_IMG_HEIGHT))

    #Re-tailor picture
    scaled_img = scale_original_wallpaper(Fusion_2d_Image, HOW_MANY_D)
    picture_save_name = os.path.join(os.environ['HOME'], "Pictures/%s_%s_%s_%s_%s_%s_%s_%s_EarthLiveForMac.png" % (year, month, day, hour, minute, second, row, column))  # pic path under the script dir
    scaled_img.save(picture_save_name)

    return picture_save_name

def scale_original_wallpaper(img, how_many_d):
    # Make a picture including the Earth and the black canvas
    size = (DESKTOP_LONG, DESKTOP_SHORT)
    bg_img = Image.new('RGB', size, 'black')

    # calculate the paste origin
    o_x = (size[0] - ORIGINAL_IMG_WIDTH * how_many_d) // 2
    o_y = (size[1] - ORIGINAL_IMG_HEIGHT * how_many_d) // 2
    bg_img.paste(img, (o_x, o_y))
    return bg_img


def set_wallpaper():
    # Using shell to set wallpaper
    picpath = download_img()

    script = """/usr/bin/osascript << END
                tell application "Finder" to set desktop picture to POSIX file "%s"
END"""

    subprocess.call(script%picpath, shell=True)
    time.sleep(3)
    if os.path.isfile(picpath) and AUTO_REMOVE is True:
        os.remove(picpath)# delete it after wallpaper set.
    print 'Done.'

if __name__ == '__main__':
    while True:
        print "waiting..."
        set_wallpaper()
        time.sleep(600)
