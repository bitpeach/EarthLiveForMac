# EarthLiveForMac

## Thanks
EarthLive using Python has been made to perform on Mac by @bitpeach. Note that two guys who name @bitdust and @xyangk are the important helpers of my codes.

## What is the EarthLive
* EartLive is a kind of pragrams or softwares to set your wallpaper of PC or phones by the real-time earth living images. That is amazing of nearly using and watching the 24-hour or real-time earth pictures captured by the satellite.

* Here is an example. Please note that this wallpaper can be real-time changed by the earth real-time changing. Excited!

![](https://github.com/bitpeach/EarthLiveForMac/blob/master/Example%201%20%5BEarthLive%20is%20used%20in%20Wallpaper%5D.png) 

* The real-time pictures of 24-hour earth come from the [Himawari-8](http://himawari8.nict.go.jp), the wiki or introduction of Himawari-8 is this [link](https://en.wikipedia.org/wiki/Himawari_8). Thanks to Himawari-8 of Japan satellite. And we will wait for the COMPASS satellite and hope to communicate with both two satellites. :-)


## Different Versions of EarthLive
* C# Version (see this [link](https://github.com/bitdust/EarthLiveSharp), the author is @bitdust, this version is the most famous one that can be performed on Windows PC.)

* Android Version (see this [link](https://github.com/oxoooo/earth), the author is @XiNGRZ or @oxoooo, this app is called mantou_earth or 馒头地球 as well that can be performed on the Android Mobile Phone.)

* Ruby Version (see this [link](https://gist.github.com/pepsin/2332ef243e3285ca68c6), the author is @pepsin.)

* Golang or Ruby Version (see this [link](https://github.com/oxoooo/mantou_earth), the author is @XiNGRZ or @oxoooo.)

* Python Version (see this [link](https://github.com/xyangk/EarthLiveSharp), the author is @xyangk.)


## EathLive For Mac(What I have done)
* What I have done: This version of mine revised based on @xyangk is designed with Mac and Python.

* Why did I do this: The Golang or Ruby version is not open-source, then I learned the Python version from @xyangk and found that may have some errors when running on Mac. So I tried to horizon my eyes and made some revisions.

* What are the contributions of this version:
>* I want the more accurate pictures when using the 4k or large size of computer screen. Therefore, I try to tailor the multiple pictures into the whole one. The codes from @xyangk did not include the higher accurate picture processing.
>* I found the codes from @xyangk may contains some error such as two places. The first is that those codes need AppKit to be running. However, AppKit is a problem to be linked with 3-rd Python. I tried to use the command "pip install PyObjc" and still got failed on the code building. The second is that those codes may use the wrong picture interface linked to the Himawari-8 web and I have fixed these.


## How Does my Codes work
* Brief Procedure:
>* (1) You should download or get the picture that contains the real-time earth. It's lucky that Himawari-8 satellite provides those pictures in each 10 minutes. During you download those pictures, you should know the web interface.
>* (2) Then when you have already got the pictures, you need to tailor them because the pictures may be not suitable for PC wallpaper. The other reason is that some pictures are not the intact for the accurate control so you should combine those images by yourself. 

* Program Procedure:
>* (1) We try to learn the formal file name of pictures, search the original download link and call for them.
>* (2) Then, we use the website `Cloudinary` to let it automatically fetch the pictures from the original link instead of downloading the pictures from the original link by ourselves. Using `Cloudinary` to download them may avoid the network failure or shield and computer overload.
>* (3) Finally, after we get the pictures, we find that the pictures have the only earth and no stripes. That may be not nice watched on the PC wallpaper. So we should resize the pictures. Meantime, some pictures comprise of one earth, so we should combine them. 

* What is the picture interface by Himawari-8:
  * Json format: If you want to know how to download the pictures captured by Himawari-8, you should firstly know the data format of picture names. The json file name is obeyed this [format](http://himawari8.nict.go.jp/img/D531106/latest.json). The return data format is like this `{"date":"2016-05-15 10:00:00","file":"PI_H08_20160515_1000_TRC_FLDK_R10_PGPFD.png"}`.
  
  * Web interface about pictures: According to the format of json data, we can construct an `interface URL` like this `http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/2016/05/15/100000_0_0.png` and we can open this URL by any web broswer. So we consider the regulatory format can be writed as follow.
  </br>Format:`http://himawari8-dl.nict.go.jp/himawari8/img/D531106/[%accuracy]/550/[%year]/[%month]/[%day]/[%hour%min%sec]_[%row position]_[%column position].png`
  
  * [%accuracy]: It can be set as `1d` which means that the picture is the whole one and also set as `2d` which means that the pictures consists of `2 x 2 = 4` pictures. If the `2d` is set, the sub-pictures can be pointed by four kinds of positions using `(0,0) (0,1) (1,0) and (1,1)`. Generally, this parameter should be set and controlled by yourself.

  * [%year]/[%month]/[%day]/[%hour%min%sec]: Generally, this parameter can be derived from the JSON file automatically.
  
  * [%row position],[%column position]: These two parameters can be set both zero if the [%accuracy] is set as `1d`. If the [%accuracy] is set as `2d`, `2d` pictures consist of 4 sub-pictures and the whole earth is obtained by combining those 4 sub-pictures. So we should download 4 pictures through accessing the 4 kinds of `interface URL` generated by row or column positions changing. For instance, [%row position] is set as `0` with [%column position] set as `1` and it means the top-right corner sub-pictures.

  * Here is an example: If [%accuracy] is set as `2d`, we should download the pictures using those 4 URLS as follows.
  [%Four interface URLs]</br>
  ` http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2015/11/25/002000_0_0.png
    http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2015/11/25/002000_0_1.png
    http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2015/11/25/002000_1_0.png
    http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2015/11/25/002000_1_1.png`</br>
  It means that the complete picture consists of the four pictures above and the time of pictures captured by Himawari-8 is 00:20:00 am, Nov. 25th, 2015.

* What is the fetch interface by Cloudinary:
  * Fetch format:
  `http://res.cloudinary.com/[%Your_Cloud_Account_Name]/image/fetch/[%interface URL]`
  So you may register an account on this [website](http://cloudinary.com).

* How to combine the picture and set wallpaper:
  * PIL (`Pillow` Python Module): We build a new canvas and paste the 4 sub-pictures into the new canvas. The function may be involved by `Imaga.new`, `Imaga.open` or `Image.paste(Image, [row position * base size, column position * base size])`.
  * OS X shell: `tell an application "Finder"` or `tell application "System Events"`

### The Limitation of EarthLiveForMac
* The strict permission of OS X: I cannot set it as the self-starting process. However, this problem has been discussed by this [place](https://github.com/xyangk/EarthLiveSharp) or [here](http://stackoverflow.com/questions/6442364/running-script-upon-login-mac).

* The gap of this pragmatized tool: I still consider that coding is for fun. Therefore, this script or tool is just a beginning and we wait for more friends to help polishing this code. Thank you.


## License
[GNU General Public License, version 3](LICENSE)

## Finally
` It's not bright.`

` I'm magnetised.`

` To somebody that don't feel it, love paralyzed just never gonna need me.`

As it said, sure if the world keeps the moon in the sky. So please keep us hanging on the earth.
By @bitpeach
