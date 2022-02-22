# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import cv2 as cv
import os, sys, glob
import matplotlib.pyplot as plt
from scipy import signal


# %%
"""
imgs = []
for img_file in os.listdir('/Users/estepark/Documents/week1_tues/White/1_20200328_150422_White_Reg'):
    imgs.append(cv.imread('/Users/estepark/Documents/week1_tues/White/1_20200328_150422_White_Reg/1_20200328_150422_White_Reg.csv'))
# need to know how the csv file is formated to conver the pixel array
"""

imgs = []
for img_file in os.listdir('/Users/estepark/Documents/week1_tues/LeftEdge/'):
    imgs.append(cv.imread('/Users/estepark/Documents/week1_tues/LeftEdge/5_20181126_102335_White_Reg.Png'))
# need to know how the csv file is formated to conver the pixel array
print(imgs)


# %%
# remove the first sublist in the list, bc it's a NoneType for some odd reason
imgs.pop(0)
type(imgs)
print(imgs)# remove the first sublist in the list, bc it's a NoneType for some odd reason


# %%
for x in imgs:
    plt.figure()
    plt.imshow(x)
    plt.show()


# %%
print("Low pass fitler and dramatize contours:")
for img in imgs: 
    im = img.copy()
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    print(imgray)
    imgray = cv.bilateralFilter(imgray, 15, 75, 75)
    ret, thresh = cv.threshold(imgray, 10, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    im_with_contours = cv.drawContours(im.copy(), contours, -1, (0,255,0), 6)
    plt.figure()
    plt.imshow(im_with_contours ,cmap='gray')
    plt.show()

# define scharr kernal to convolve along diagonals
print("identify a pattern:")
kern = [[0, 1,  0], [1, 0, -1],[ 0, -1 ,0]]
diag_img = signal.convolve2d(imgray, np.array(kern), boundary='symm', mode='same')
plt.figure()
#plt.imshow(diag_img+101, cmap="gray")
plt.imshow(diag_img, cmap="gray")

print('where')
plt.show()

# sliced image 
plt.figure()
plt.imshow(diag_img[:,0:100], cmap="gray") # diag_img[start_vertical:end_vertical, start_horizontal:end_horizontal]; 
plt.title('sliced image')
plt.show()

# histogram
plt.figure()
plt.hist(im[:,0:100].ravel())
plt.show()

# magic RGB
plt.figure()
#plt.plot(diag_img[:,25]+100)
#plt.plot(im[:,25]+100)
plt.plot(im[:,25])
plt.xlabel('pixel location along y')
plt.ylabel('intensity in RGB')
plt.title('intensity in RGB vs. pixel location along y axis (# columns)')
plt.show()

# Graph FFT of the array
samplingFrequency = 2*600 # how many time points are needed (ie, sampling frequency this is arbitrary, tune later)
samplingInterval = 1/samplingFrequency
#amplitude1 = im[0:600,25][:,1]
amplitude1 = im[0:600,25][:,0]
#time1 = np.arange(0,10,samplingInterval)
time1 = np.linspace(0,600,600)
print('length o time is ' + str(len(amplitude1)))
print('amptlitude1 length is : ' + str(len(time1) ))
# spatial/time domain representation for sine wave1
figure , axis = plt.subplots(3,1)
plt.subplots_adjust(hspace=1)
axis[0].set_title('Sine wave with unknown time period of Left Edge defect')
axis[0].plot(time1, amplitude1)
axis[0].set_xlabel('length of Columns along y pixel mat')
axis[0].set_ylabel('Pixel intesity')
# frequency domain reqpresentation
#fourierTrans = np.fft.fft(amplitude1)/len(amplitude1) # normalize amplitude
fourierTrans = np.fft.fft(amplitude1) # unnormalize amplitude
print('four unnormalized' + str(len(fourierTrans)))
fourierTrans = fourierTrans[range(int(len(amplitude1)/2   ))]
print('fourTrans ' + str(len(fourierTrans)))
tpCount = len(amplitude1)
values = np.arange(int(tpCount/2))
timePeriod = tpCount/samplingFrequency
freq1 = values / timePeriod
axis[1].set_title('frequency spectrum of Left Edge defect')
axis[1].plot(freq1, abs(fourierTrans))
axis[1].set_xlabel('frequency of Columns along y pixel mat')
axis[1].set_ylabel('Pixel intesity')
axis[1].set_xlim(-5,600)
# stem plot
axis[2].set_title('frequency spectrum of Left Edge defect')
axis[2].stem(freq1, abs(fourierTrans))
axis[2].set_xlabel('frequency of Columns along y pixel mat')
axis[2].set_ylabel('Pixel intesity')
axis[2].set_xlim(-5,5)
axis[2].set_ylim(0,100)


# %%
gray_filtered = cv.bilateralFilter(imgray, 50, 25, 25)
can = cv.Canny(gray_filtered, 5, 6)
plt.figure(figsize=(10,10))
plt.imshow(can, cmap="gray")
plt.show()
plt.figure(figsize=(10,10))
plt.imshow(imgray, cmap="gray")


# %%
from scipy import fftpack
f_s=10 # sampling rate weirdness, lower the rate --> more points resolve, vice versa, but how?
x= amplitude1
X = fftpack.fft(x)
freqs = fftpack.fftfreq(len(x)) * f_s

fig, ax = plt.subplots()

ax.stem(freqs, np.abs(X))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
#ax.set_xlim(-f_s / 2, f_s / 2)
ax.set_xlim(-5,5)
ax.set_ylim(-5, 500)


# %%



# %%


