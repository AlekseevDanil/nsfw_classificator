import cv2
from keras.models import load_model
import numpy as np
from collections import deque
import warnings
import time

start_time = time.time()
warnings.filterwarnings("ignore")

model = load_model("/home/dn_alekseev/Documents/Projects/AI inspections (Danil) Python/DataBase/Final_weights.h5")
labels = {0: "Neutral", 1: "Porn", 2: "Sexy"}

size = 128
input_vid = "/home/dn_alekseev/Documents/Projects/AI inspections (Danil) Python/Movies/Movie_2.mp4"
Q = deque(maxlen=size)

Neutral, Porn, Sexy, _len = 0, 0, 0, 0

vs = cv2.VideoCapture(input_vid)
print('Loading, it may take some time...')

while True:
    # read the next frame from the file
    (grabbed, frame) = vs.read()

    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    output = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame / 255.0
    frame = cv2.resize(frame, (224, 224)).astype("float32")

    # make predictions on the frame and then update the predictions
    # queue
    preds = model.predict(np.expand_dims(frame, axis=0))[0]
    if preds[0] < 1 and preds[1] < 1 and preds[2] < 1:
        Neutral += (preds[0] * 100)
        Porn += (preds[1] * 100)
        Sexy += (preds[2] * 100)
        _len += 1
    Q.append(preds)

'''
    # perform prediction averaging over the current history of
    # previous predictions

    results = np.array(Q).mean(axis=0)
    i = np.argmax(preds)
    label = labels[i]
    text = "activity: {}:".format(label)
'''

print("[INFO] it's done...")
print("Neutral =", Neutral / _len, "%")
print("Porn =", Porn / _len, "%")
print("Sexy =", Sexy / _len, "%")
print("--- %s seconds ---" % (time.time() - start_time))
vs.release()
