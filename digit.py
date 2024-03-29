import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
#Python Imaging Library (PIL) - external library adds support for image processing capabilities
from PIL import Image
import PIL.ImageOps

X, y = fetch_openml('mnist_784', version=1, return_X_y=True)

print(pd.Series(y).value_counts())

classes = ['0', '1', '2','3', '4','5', '6', '7', '8','9']
nclasses = len(classes)

x_train, x_test, y_train, y_test = train_test_split(X,y,random_state = 9, train_size = 7500,test_size = 2500)
x_train_scaled = x_train/255.0
x_test_scaled = x_test/255.0
clf = LogisticRegression(solver = "saga",multi_class = "multinomial").fit(x_train_scaled,y_train)
y_pred = clf.predict(x_test_scaled)
acc = accuracy_score(y_test,y_pred)
print("The accuracy is: ",acc)

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
while(True):
    try:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        height,width = gray.shape
        upper_left = (int(width/2-56), int(height/2-56))
        bottom_right = (int(width/2+56), int(height/2+56))
        cv2.rectangle(gray, upper_left, bottom_right,(0,255,0),2)
        roi = gray[upper_left[1]:bottom_right[1],upper_left[0]:bottom_right[0]]
        im_pil = Image.fromarray(roi)
        # convert() to grayscale image - 'L' format means each pixel represented by a single value from 0 to 255
        image_bw = im_pil.convert("L")
        image_bw_resized = image_bw.resize((28,28),Image.ANTIALIAS)
        img_invert =  PIL.ImageOps.invert(image_bw_resized)
        pixel_filter = 20

        #percentile() converts the values in scalar quantity
        min_pixel = np.percentile(img_invert,pixel_filter)

        #using clip to limit the values betwn 0-255
        img_invert_scale = np.clip(img_invert - min_pixel, 0, 255)
        max_pixel = np.max(img_invert)
        img_invert_scale = np.asarray(img_invert_scale)/max_pixel
        test_sample = np.array(img_invert_scale).reshape(1,784)
        test_pred = clf.predict(test_sample)
        print(f"The predicted digit class is: {test_pred}")
        cv2.imshow("Frame",gray)

        if(cv2.waitKey(1)& 0xFF==ord("q")):
            break

    except Exception as e:
        pass

cap.release()
cv2.destroyAllWindows()

