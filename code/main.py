from keras.models import load_model
from collections import deque
import numpy as np
import warnings
import time
import cv2
warnings.filterwarnings("ignore")


def start_classification(input_vid, model=load_model("../model/inspector_model.h5")):
    size = 128
    Q = deque(maxlen=size)

    Neutral, Porn, Sexy, _len = 0, 0, 0, 0

    vs = cv2.VideoCapture(input_vid)

    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame / 255.0
        frame = cv2.resize(frame, (224, 224)).astype("float32")

        preds = model.predict(np.expand_dims(frame, axis=0))[0]

        if preds[0] < 1 and preds[1] < 1 and preds[2] < 1:
            Neutral += (preds[0])
            Porn += (preds[1])
            Sexy += (preds[2])
            _len += 1

        Q.append(preds)

    vs.release()
    return [(Neutral / _len), (Porn / _len), (Sexy / _len)]


if __name__ == "__main__":
    start_time = time.time()

    input_vid = "../movies/porn_15s.mp4"
    model = load_model("../model/inspector_model.h5")

    Neutral_percent, Porn_percent, Sexy_percent = start_classification(input_vid, model)

    print("[INFO] it's done...\n")
    print("Neutral =", Neutral_percent, "%")
    print("Porn =", Porn_percent, "%")
    print("Sexy =", Sexy_percent, "%")
    print("\n--- %s seconds ---" % (time.time() - start_time))
