import io
from PIL import Image

with open("NTPImage.png", "rb") as image:
    readImage = image.read()
    # print(readImage)
    # print(len(readImage))  
    
    # The Same
    # imageByte = bytearray(readImage)
    # print(imageByte) 
    # print(len(imageByte))  
 
    image = Image.open(io.BytesIO(readImage))
    image.show()