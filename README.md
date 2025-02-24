# python app to correct image persppective

## How to start it

Install python (or confirm you have installed it)

try 

which python 
which py
which python3

to find out if it is installed and which alias, for me it is python3

python3 -m venv venv . - r requirements.txt

source /venv/bin/activate

python app.py

## How to use it

add the path where the images are to source folders.json
add the path where you want the result to the file as well 


all the images that are cropped will be savedf there, once yu open the app it will ask you to ctop all the images until you have the same cropped as not cropped
the cropped are resized to 1000x1000 and the aspect ratio is corrected (sometimes they may look a bit weird but it is the only option to have a common coordinate system in my opinion)

the images are saved in jpg