from imageai.Classification.Custom import CustomImageClassification
import os
from PIL import Image, ImageEnhance
from tensorflow import keras
import cv2
import numpy as np

classNames = ['apple', 'banana', 'chip', 'coin', 'dragon scale', 'epic coin', 'epic fish', 'fish', 'golden fish', 'life potion', 'mermaid hair', 'ruby', 'unicorn horn', 'wolf skin', 'zombie eye']

model = keras.models.load_model('mymodel')

def solveCaptcha():
    img = Image.open("captcha.png")
    imgGray = img.convert('L')

    width, height = imgGray.size
    imgGrayCrop = imgGray.crop((0, 10, 220, height - 10))
    width, height = imgGrayCrop.size

    new_size = (246, 236)
    new_im = Image.new("L", new_size)   ## luckily, this is already black!
    new_im.paste(imgGrayCrop)
    imgGrayCrop = new_im
    width, height = imgGrayCrop.size
    
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = imgGrayCrop.getpixel((i,j))
            if (data>245):
                for k in range(i-10, i+10):
                    for m in range(j-10, j+10):
                        imgGrayCrop.putpixel((k,m),(36))
            elif (data==0):
                imgGrayCrop.putpixel((i,j),(36))
    imgGrayCrop = imgGrayCrop.crop((0, 0, width-10, height))

    enhancer = ImageEnhance.Contrast(imgGrayCrop)
    factor = 2 #increase contrast
    imgGrayCrop = enhancer.enhance(factor)
    newsize = (100, 100)
    imgGrayCrop = imgGrayCrop.resize(newsize)

    imgGrayCrop.save("captcha_bw.png")

    image=cv2.imread("captcha_bw.png")
    image=np.expand_dims(image,axis=0)
    pred=model.predict(image)

    return [classNames[idx] for idx in np.flip(np.argpartition(pred[0], -3)[-3:])]