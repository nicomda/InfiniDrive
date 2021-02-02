# InfiniDrive
Unlimited Cloud Drive using Amazon Prime Photos

How it's done:
1. The app opens the file you wanna store in RAW binary
2. Bytes of the file are splitted and converted to RGB PNG images
3. Now you are ready to upload all the images to Amazon Prime Photos. As they are images, they are unlimited. You can create an album to download everything at once 
4. Download your album as a zip, then unzip it
5. The app will merge all the images to recreate the original file
6. The magic is done 😎

The recovered file has perfect integrity. Sha256 checksum is passed.

## Installation
Assure that you have python3.8 installed on your system.
```sh
#Clone this repo
git clone https://github.com/nicomda/InfiniDrive

#Install virtualenv if not installed
pip3 install virtualenv

#Creating virtualenv
python3 -m venv InfiniDrive

#Activating venv
source ./bin/activate

#Installing required libraries in the virtual enviroment
pip3 install -r requirements.txt
```
## Quick Start
```bash
#To split a file: 
./InfiniDrive.py -s 'file_to_split'

#To split a file changing size of images. The default size is 2000x2000 (12MB): 
./InfiniDrive.py -s 'file_to_split' --imgpxl=100

#To merge images: 
./InfiniDrive.py -m 'images_folder'
```

### **Available arguments:**

| Argument        | What it does | Optional |
| --------------- |:-------------|:---------:| 
| -s                               |Split mode 
| -m                               |Merge mode 
| -o                               |Change default output folder when splitting |✔
| --outputfile=<out_file_path>     |Path where output file will be created |✔
| --imgpxl='side_size'    |Change the size of the output images |✔
| -h,                            |Extended help |✔

