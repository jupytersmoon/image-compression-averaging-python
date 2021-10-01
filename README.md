# image-compression-averaging-python
This is a program to compress .jpg/.jpeg and .png images using python. Only uses numpy and PIL library. The method used to compress is averaging the pixel values.

<br>This program was made for a college project
<br>There are restrictions in writing the codes for this program, to name some:
<br>1. Only PIL and numpy is allowed
<br>2. PIL library is only allowed to be used for reading the image and converting arrays back to an image
<br>3. Numpy library is only allowed to be used for converting the image into an array, doing math calculations, and converting array's data type
<br>4. Any other Python libraries/modules are NOT ALLOWED to be used, unless it does not impact the main logic of the program

<br>The comments in the image_compressing.py file are in Indonesian.

## How To Use
<br>You can choose to compress your image by changing the image's dimension or compressing without changing the image's dimension. The program will ask you, in this order:
<br>1. The image file you want to compress (accepting colour and grayscale image, .jpg/.jpeg and .png)
<br>2. The ratio of dimension compression, choose between 1 - 4. 1 means no image dimension change, 4 means your image's dimension will be 4 times smaller.
<br>3. The ratio of colour compression, choose between 1 - 4. 1 means no colour averaging, 4 means your image will be more pixelated.
<br>4. Wait for around 60 - 75 seconds, depending on your image size it can be faster or longer.
<br>5. The file type you want your compressed image to be. 1 means saving in .JPG, 2 means saving in .PNG.
<br>6. File name and file path to save your compressed image.
