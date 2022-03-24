import io
from PIL import Image

# with open("NTPImage.png", "rb") as image:
with open("NTP1KbImage.jpg", "rb") as image:
    readImage = image.read()
    # print(readImage)
    # print(len(readImage))  
    
    # The Same
    imageByte = bytearray(readImage)

    # print(imageByte) 
    print(len(imageByte))  

    with open("NTPImageByteArray.txt", "w") as text_file:
        print(f"{imageByte}", file=text_file)
 
    image = Image.open(io.BytesIO(imageByte))
    image.save("NTP1KbImg.jpg")
    image.show()