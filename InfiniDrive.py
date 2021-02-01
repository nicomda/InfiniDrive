#!bin/python3
import os, sys, io, math, getopt
from pathlib import Path 
import PIL.Image as Image
from PIL.PngImagePlugin import PngInfo

MB_IMG_DATA=36000000 #12MB IMG's
split_counter=0
split_parts=0
operation_mode="None"
filepath=sys.argv[1]
outfolder=Path(filepath).resolve().stem
def printQuickHelp():
    print("***Quick Usage steps***")
    print("----------------------------------------")
    print("To split & encode file as RGB images: InfiniDrive.py -s <file_to_encrypt>")
    print("To merge RGB images folder to the original file: InfiniDrive.py -m <imgs_folder> ")
def getArgsOptions():
    global filepath, size, operation_mode
    if len(sys.argv) == 1:
        printQuickHelp()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'hs:m:', ["help","imgsize=","merge","split"])
    except getopt.GetoptError:
        print('Arguments error, just use as below or -h for more options.')
        printQuickHelp()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printExtendedHelp()
            sys.exit()
        elif opt in ('-s', '--split'):
            operation_mode="split"
        elif opt in ('-m', '--merge'):
            operation_mode="merge"
        elif opt in ('--imagesize'):
            #var=int(arg)
def guessSplittedParts(path):
    return math.ceil(Path(path).stat().st_size/MB_IMG_DATA)

def generateImg(bytearray, width, height):
    global filepath, split_counter, outfolder
    if(not Path.exists(Path(outfolder))):
        os.mkdir(outfolder)
    #Adding metadata
    filename, file_extension = os.path.splitext(filepath)    
    infinidata = PngInfo()
    infinidata.add_text("Extension", file_extension)
    infinidata.add_text("Name", filename)
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
        print(im.text) #Printing metadata
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
#mergeImages(outfolder)
print(filename)
print(file_extension)


           
