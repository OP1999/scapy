import io
from PIL import Image

with open("NTPImage.png", "rb") as image:
    readImage = image.read()
    imageByte = bytearray(readImage)
    print(imageByte[0])  
    image = Image.open(io.BytesIO(imageByte))
    image.show()