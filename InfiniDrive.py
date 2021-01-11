#!bin/python3
import os
import io
import sys
from pathlib import Path 
import PIL.Image as Image

MB_IMG_DATA=12000000 #12MB IMG's
split_counter=0

def generateImg(bytearray, width, height, split_counter):
    filepath=sys.argv[1]
    outfolder=Path(filepath).resolve().stem
    if(not Path.exists(outfolder)):
        os.mkdir(outfolder)
    img=Image.frombytes("RGB", (width,height), bytes(bytearray))
    img_name=f'{split_counter.zfill(5)}.png'
    os.chdir(outfolder)
    img.save(img_name,"PNG")
        
def openFileBinary(path):
    with open(path, "rb") as bf:
        raw_data=bytearray()
        while (byte := bf.read(1)):
            raw_data.append(byte)
            if(len(raw_data) == MB_IMG_DATA):    
                generateImg(raw_data,3000,4000)
                raw_data.clear()    
            raw_data.append(bytes(MB_IMG_DATA - len(raw_data))) #Padding 0's till completed
            generateImg(raw_data,3000,4000) #Generating last img
            



           
