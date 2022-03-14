# doc = open('file1.docx', 'rb').read()
# open('file2.docx', 'wb').write(doc)

# with open('NTPDoc.docx', "rb") as doc:
#     readDoc = doc.read()
#     docByte = bytearray(readDoc)
#     print(readDoc[10000])  

import docx
import os.path

def getTextFromDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

print(getTextFromDoc('NTPDoc.docx'))