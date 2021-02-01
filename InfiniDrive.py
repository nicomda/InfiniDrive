#!bin/python3
import os
import io
import sys
import math
from pathlib import Path 
import PIL.Image as Image
from PIL.PngImagePlugin import PngInfo

MB_IMG_DATA=36000000 #12MB IMG's
split_counter=0
split_parts=0
filepath=sys.argv[1]
outfolder=Path(filepath).resolve().stem

def guessSplittedParts(path):
    return math.ceil(Path(path).stat().st_size/MB_IMG_DATA)

def generateImg(bytearray, width, height):
    global filepath, split_counter, outfolder
    if(not Path.exists(Path(outfolder))):
        os.mkdir(outfolder)
    #Adding metadata    
    infinidata = PngInfo()
    infinidata.add_text("Extension", "EXAMPLE")
    img=Image.frombytes("RGB", (width,height), bytes(bytearray))
    img_name=f'{outfolder}_{str(split_counter).zfill(len(str(guessSplittedParts(filepath))))}.png'
    img.save(f'{outfolder}/{img_name}',"PNG", pnginfo=infinidata)
    print(f'Image {split_counter} created')
    split_counter+=1
        
def openFileBinary(path):
    with open(path, "rb") as bf:
        raw_data=bytearray()
        print('Start processing. It may take a while...')
        while (byte := bf.read(1)):
            raw_data+=byte
            if(len(raw_data) == MB_IMG_DATA): 
                generateImg(raw_data,3000,4000)
                raw_data.clear()    
        raw_data+=bytearray(bytes(MB_IMG_DATA - len(raw_data))) #Padding 0's till completed
        generateImg(raw_data,3000,4000) #Generating last img

def mergeImages(path):
    file_list = os.listdir(path)
    file_list.sort()
    print(file_list)
    raw_buffer=bytearray()
    for file in range(len(file_list)):
        im = Image.open(f'{path}/{file_list[file]}', mode='r')
        im_width, im_height = im.size
        list(im.getdata())
        pixel_list = bytearray([pixel for tuple in list(im.getdata()) for pixel in tuple])
        print(im.text)
        raw_buffer+=pixel_list
        pixel_list.clear()
    print(len(raw_buffer))
    while raw_buffer[-1] == 0 :
        del raw_buffer[-1]
    print(len(raw_buffer))
    with open("prueba_recovered", "wb") as recovered:
        recovered.write(raw_buffer)
split_parts = guessSplittedParts(filepath)
if split_parts == 1:
    print(f'File will be splitted in 1 image ')
else:
    print(f'File will be splitted in {split_parts} images ')
#print(guessSplittedParts)
#openFileBinary(filepath)
mergeImages(outfolder)



           
