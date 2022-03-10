# doc = open('file1.docx', 'rb').read()
# open('file2.docx', 'wb').write(doc)

with open('NTPDoc.docx', "rb") as doc:
    readDoc = doc.read()
    docByte = bytearray(readDoc)
    print(readDoc[10000])  