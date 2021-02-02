#!bin/python3
import os, sys, io, math, getopt
from pathlib import Path 
import PIL.Image as Image
from PIL.PngImagePlugin import PngInfo

split_counter=0 #Stores which image is gonna be stored. It will help to set the img title
split_parts=0 #Stores the number of images needed
imgsize=2000 #Default img size 2000x2000
MB_IMG_DATA=imgsize*imgsize*3 #Width * height * RGB. The image will be an square to get things easier.
operation_mode="None" #Whether the app is gonna split or merge 
filepath="." #Name of the file to be splitted
outfolder=Path(filepath).resolve().stem #By default, the folder where the images are saved
origname="" #Name of the file before being splitted. Will be extracted from PNG's EXIF.
outputpath="" #Just if you want to modify the default output file path


def printQuickHelp():
    print("***Quick Usage steps***")
    print("----------------------------------------")
    print("To split & encode file as RGB images: InfiniDrive.py -s <file_to_split>")
    print("To merge RGB images folder to the original file: InfiniDrive.py -m <imgs_folder> ")
    print("If you need more info, just call me with -h or --help")

def printExtendedHelp():
    print('Available arguments')
    print('-s <file_to_split>               Split mode')
    print('-m <folder_with_img_to_merge>    Merge mode')
    print('-o, <path_to_img_folder>         To change the default output folder when splitting')
    print('--outputfile=out_file_path       Path where output file will be created')
    print('--imgpxl=side_pixels             To set a different splitting size')

def getArgsOptions(): #Will handle the necessary params from argv
    global filepath, imgsize, operation_mode, outfolder, MB_IMG_DATA, outputpath
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'hs:m:o:', ["help","imgpxl=","outputfile="])
    except getopt.GetoptError:
        print('Arguments error, just use as below or -h for more options.')
        printQuickHelp()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printExtendedHelp()
            sys.exit()
        elif opt in ('-s'):
            operation_mode = "split"
            filepath=arg
            outfolder=Path(arg).resolve().stem
        elif opt in ('-m'):
            operation_mode="merge"
            outfolder=Path(arg).resolve().stem
        elif opt in ('--imgpxl'): #Will be the pixels of a side (Width or height doesn't matter cause it will be treated as a square)
            imgsize=int(arg)
            MB_IMG_DATA=imgsize*imgsize*3
        elif opt in ('--outputfile'):
            outputpath=arg
        elif opt in ('-o'):
            outfolder=arg

def guessSplittedParts(path):
    return math.ceil(Path(path).stat().st_size/MB_IMG_DATA)

def generateImg(bytearray, size): #Will generate images of given size with the raw bytes of a bytearray. It uses RGB bytes to do that (That's the trick.)
    global filepath, split_counter, outfolder, split_parts
    if(not Path.exists(Path(outfolder))):
        os.mkdir(outfolder)
    #Adding metadata
    filename, file_extension = os.path.splitext(filepath)    
    infinidata = PngInfo()
    infinidata.add_text("OrigName", f'{filename}{file_extension}')
    img=Image.frombytes("RGB", (size,size), bytes(bytearray))
    img_name=f'{outfolder}_{str(split_counter).zfill(len(str(guessSplittedParts(filepath))))}.png'
    img.save(f'{outfolder}/{img_name}',"PNG", pnginfo=infinidata)
    print(f'Creating Image {split_counter+1}/{split_parts}', end = "\r")
    split_counter+=1
        
def openFileBinary(path): #Will open a file in raw mode and then generate as much as needed images to store the file.
    global imgsize, split_parts
    with open(path, "rb") as bf:
        raw_data=bytearray()
        print('Start processing. It may take a while...')
        if split_parts == 1:
            print(f'File will be splitted in 1 image ')
        else:
            print(f'File will be splitted in {split_parts} images ')
        while (byte := bf.read(1)):
            raw_data+=byte
            if(len(raw_data) == MB_IMG_DATA): 
                generateImg(raw_data,imgsize)
                raw_data.clear()    
        raw_data+=bytearray(bytes(MB_IMG_DATA - len(raw_data))) #Padding \x00's till completed
        generateImg(raw_data,imgsize) #Generating last img

def mergeImages(path):
    global origname, outputpath
    file_list = os.listdir(path)
    file_list.sort()
    im = Image.open(f'{path}/{file_list[0]}', mode='r') #Opening first image to get filename before entering the loop
    origname=im.text.get('OrigName') #Extracting metadata
    print(f"RAW bytes in images gonna be merged as the original file '{origname}'")
    if(outputpath == ""):
        outputpath=origname
    else:
        outputpath=f'{outputpath}/{origname}'
    if(os.path.isfile(f'{outputpath}')):
        print(f"There's already a file called {origname}. Do you want to overwrite it?")
        isOverwritten=input('(y/N)')
        if(isOverwritten == 'y' or isOverwritten=='Y'):
            os.remove(outputpath)
        else:
            print("In order to protect your files, nothing will be removed.")
            sys.exit()
    with open(outputpath, "ab") as recovered:
        file_counter=1
        for file in range(len(file_list)):
            print(f'Processing {file_list[file]} ({file_counter}/{len(file_list)})', end = "\r")
            im = Image.open(f'{path}/{file_list[file]}', mode='r')
            im_width, im_height = im.size
            list(im.getdata())
            pixel_list = bytearray([pixel for tuple in list(im.getdata()) for pixel in tuple])
            if(file_list[file] == file_list[-1]): #Deleting EOF padding from the last img
                print("Deleting last image null bytes")
                while pixel_list[-1] == 0 :
                    del pixel_list[-1]
            recovered.write(pixel_list)
            pixel_list.clear()
            file_counter=file_counter+1
        

#Here's where the magic starts ¯\_(ツ)_/¯
getArgsOptions() #Get options from argv
if(operation_mode == 'split'):
    if(os.path.isfile(filepath)):
        split_parts = guessSplittedParts(filepath)
        openFileBinary(filepath)
        print(f"The file has been splitted. You've got the images in folder '{outfolder}'")
    else:
        print("A file with that name does not exists here.")    
elif(operation_mode == 'merge'):
    if(os.path.exists(outfolder)):
        mergeImages(outfolder)
        print(f'The file has been recovered as {origname} ')
    else:
        print("Can't find folder with that name. Try again.")
else:
    print('No operation mode was selected. Maybe you need help?')
    printQuickHelp()


           
