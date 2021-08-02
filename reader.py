import cv2 as cv
from pyzbar.pyzbar import decode
import imutils

def scan (img):
    img = cv.imread(img)
    detectedBarcodes = decode(img)
    imgH, imgW, imgC = img.shape
    img = imutils.resize(img, width = 1280)
    newImgH, newImgW, newImgC = img.shape
    orgImg = img.copy()

    xMult = (newImgW/imgW)
    yMult = (newImgH/imgH)

    if detectedBarcodes:
        count = 0

        for barcode in detectedBarcodes:
            with open('readCodes.txt', "r") as codeFile:
                prevCodes = codeFile.readlines()
            count += 1
            print(f"\n-----------------------------\n{count}:")
            highlightColour = (0, 255, 0)
            type = barcode.type
            info = barcode.data.decode("utf-8")
            
            savedInfo = (type, info)

            if (str(savedInfo)+"\n") in prevCodes:
                print("Already Scanned. Invalid Barcode found")
                highlightColour = (0, 0, 255)
            
            else:
                with open("readCodes.txt", "a") as codeFile:
                    codeFile.write(str(savedInfo) + "\n")

            (x, y, w, h) = barcode.rect
            x = int(x * xMult)
            y = int(y * yMult)
            w = int(w * xMult)
            h = int(h * yMult)

            print(x,y)
            cropped = orgImg[y: y + h, x: x + w]

            try:
                cropped = imutils.resize(cropped, width = 400)
                
                print(f"Successful scan\nType: {type}\nInfo: {info}")

                cv.rectangle(img, (x, y), (x + w, y + h), highlightColour, 2)

                txt = f"{count}: {type}: {info}"
                cv.putText(img, txt, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7, (highlightColour), 2)

                cv.imshow(f"Cropped: {txt}", cropped)

            except:
                print("An error occured displaying the code")
                count -= 1
            
            

        cv.imshow("Barcode", img)
        print("-----------------------------\n")
        print("Press \"W\" on any window to end program.")
        if cv.waitKey(0) == ord("w"):            
            cv.destroyAllWindows()

    else:
        print("Unsuccessful attempt")

def getInput():
    imgFile = input("File name: ")
    imgType = input("File extension: ")
    
    return f"{imgFile}.{imgType}"

scan(getInput())
