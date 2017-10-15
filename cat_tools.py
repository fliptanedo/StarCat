import os, sys
from PIL import Image

import numpy as np

def jpg_image_to_array(image):
    """
    Loads JPEG image into 3D Numpy array of shape 
    (width, height, channels)
    """
    #print(image.size)
    im_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
    #print(im_arr)
    im_arr[im_arr>=0.5] = 255
    #print(im_arr)
    im_arr = im_arr.reshape((image.size[1], image.size[0],4))                                   
    return im_arr

def many_filters(img,nsizes=8,nrotations=8):

    sizes = []
    filter_images = []
    #nsizes = 8
    #nrotations = 8

    nwidth = 128/nsizes


    for i in range(0,nsizes):
        for j in range(0,nrotations):
            a = 128 - (i*int(128/nsizes))

            im_temp = img.copy()

            angle = j*(360/nrotations)
            size = a,a

            im_temp = im_temp.rotate(angle)
            im_temp.thumbnail(size)

            im_temp = jpg_image_to_array(im_temp)
    
            h,w,d = im_temp.shape
            f = np.zeros((h,w))

            for iw in range(w):
                for jh in range(h):
                    tot = im_temp[jh][iw].sum()
                    if tot:
                        f[jh][iw] = 1
            
            filter_images.append(f)

    return filter_images




def fake_sky(size,nstars):

    imsize = size

    data = np.zeros((imsize,imsize))

    vals = np.arange(0,imsize,1)

    np.random.shuffle(vals)
    starx = np.random.randint(0,imsize,nstars)

    np.random.shuffle(vals)
    stary = np.random.randint(0,imsize,nstars)


    for a,b in zip(starx,stary):
        data[a][b] = 1

    return data


def get_real_data(filename,bins):

    vals = np.loadtxt('/home/bellis/Downloads/hygdata_v3.csv',delimiter=',',unpack=True,skiprows=1,dtype=str)
    ra = vals[7].astype(float)
    dec = vals[8].astype(float)
    mag = vals[13].astype(float)

    x = ra[mag<6.5]
    y = dec[mag<6.5]

    xwidth = max(x) - min(x)
    ywidth = max(y) - min(y)

    h = np.histogram2d(y,x,bins=bins)

    x -= min(x)
    x /= xwidth

    y -= min(y)
    y /= ywidth

    x *= bins
    y *= bins

    ret_hist = h[0]
    ret_hist[ret_hist>1] = 1

    return (x,y),h[0]


