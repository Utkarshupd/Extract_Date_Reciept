# import the necessary packages

import numpy as np
import cv2
from PIL import Image
import datefinder

import pytesseract
import flask
import sys
import os



# initialize our Flask application and the Keras model
app = flask.Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)

@app.route('/')
@app.route('/home')
def upload_image():
    return flask.render_template('index.html')


def crp1(image):
    crp_size=[]
    try:

        frame = cv2.imread(image)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        Lchannel = img[:, :, 1]
        mask = cv2.inRange(Lchannel, 100, 255)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        ## find the non-zero min-max coords of canny
        pts = np.argwhere(mask > 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        crp_size =[[y1,x1],[y2,x2]]
    except:
        crp_size=-1

    return crp_size

def crp2(image):
    crp_size = []
    try:

        frame = cv2.imread(image)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        Lchannel = img[:, :, 1]
        mask = cv2.inRange(Lchannel, 130, 255)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        ## find the non-zero min-max coords of canny
        pts = np.argwhere(mask > 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        crp_size = [[y1, x1], [y2, x2]]
    except:
        crp_size = -1

    return crp_size


def crp3(image):
    crp_size = []
    try:

        frame = cv2.imread(image)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        Lchannel = img[:, :, 1]
        mask = cv2.inRange(Lchannel, 170, 255)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        ## find the non-zero min-max coords of canny
        pts = np.argwhere(mask > 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        crp_size = [[y1, x1], [y2, x2]]
    except:
        crp_size = -1

    return crp_size

def crp4(image):
    crp_size = []
    try:

        frame = cv2.imread(image)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        Lchannel = img[:, :, 1]
        mask = cv2.inRange(Lchannel, 200, 255)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        ## find the non-zero min-max coords of canny
        pts = np.argwhere(mask > 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        crp_size = [[y1, x1], [y2, x2]]
    except:
        crp_size = -1

    return crp_size

def crp5(image):
    crp_size = []
    try:

        img1 = cv2.imread(image)
        img=cv2.GaussianBlur(img1,(11,11),0)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,100,200)

        # find the non-zero min-max coords of canny
        pts = np.argwhere(edges>0)
        y1,x1 = pts.min(axis=0)
        y2,x2 = pts.max(axis=0)
        crp_size = [[y1, x1], [y2, x2]]
    except:
        crp_size = -1

    return crp_size


@app.route('/upload', methods=['POST']) #POST will get the data and perform operatins
def post_image():

    target=os.path.join(APP_ROOT, 'static/')
    print(target)
    print(flask.request.files.getlist('file'))
    for upload in flask.request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename1 = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename1)[1]
        if (ext == ".jpeg") or (ext == ".jpg"):
            print("File supported moving on...")
        else:
            return 'Image Not Uploaded'
        destination = "/".join([target, filename1])
        print("Accept incoming file:", filename1)
        print("Save it to:", destination)
        upload.save(destination)


        final_crp={}
        num = 0
        for fun in (crp1,crp2,crp3,crp4,crp5):
            final_crp[num]=fun(destination)
            num=num+1

        for i in range(5):
            if final_crp[i] is -1:
                del final_crp[i]
        final_list=[]
        for i in final_crp.keys():
            final_list.append(final_crp[i])

        print(final_list)
        y1, x1 = 0, 0
        y2, x2 = 0, 0
        for i in range(len(final_list)):
            y1 = y1 + final_list[i][0][0]
            x1 = x1 + final_list[i][0][1]

            y2 = y2 + final_list[i][1][0]
            x2 = x2 + final_list[i][1][1]
        leng = len(final_list)
        y1 = y1 // leng
        y2 = y2 // leng
        x1 = x1 // leng
        x2 = x2 // leng
        print(x1, x2)
        print(y1, y2)
        # crop the region
        img1=cv2.imread(destination)
        cropped = img1[y1:y2, x1:x2]
        tess = "/".join([APP_ROOT, '.apt/usr/bin/tess'])
        filenaam='tesseract.exe'
        teese = "/".join([tess, filenaam])

        pat='/app/.apt/usr/bin/tesseract'
        #pytesseract.pytesseract.tesseract_cmd = pat

        text = pytesseract.image_to_string(cropped)

        datefinder.ValueError = ValueError, OverflowError
        input_string = text
        yes = datefinder.find_dates(input_string)
        matches = list(yes)

        def dat(val):
            return val.minute

        print(matches)
        date_l = []
        for i in matches:
            if (2000 < i.year < 2020):
                date_l.append(i)

        date_l.sort(key=dat, reverse=True)
        try:
            date = date_l[0]
        except:
            date = "Null"

        return flask.render_template('index.html', pred="The Date is {}".format(date))


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    app.run(debug=True)
