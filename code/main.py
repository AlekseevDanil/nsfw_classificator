from keras.models import load_model
import numpy as np
import warnings
import time
import cv2
warnings.filterwarnings("ignore")


def start_classification(input_vid, model_path="../model/inspector_model.h5"):
    model = load_model(model_path)
    Neutral, Porn, Sexy, marks_len = 0, 0, 0, 0

    vs = cv2.VideoCapture(input_vid)

    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame / 255.0
        frame = cv2.resize(frame, (224, 224)).astype("float32")

        # preds = [Neutral Porn Sexy]
        preds = model.predict(np.expand_dims(frame, axis=0))[0]

        if preds[0] < 1 and preds[1] < 1 and preds[2] < 1:
            Neutral += (preds[0])
            Porn += (preds[1])
            Sexy += (preds[2])
            marks_len += 1

    vs.release()
    return [float(str(Neutral / marks_len)[:4]),
            float(str(Porn / marks_len)[:4]),
            float(str(Sexy / marks_len)[:4])]


if __name__ == "__main__":
    start_time = time.time()

    input_vid = "../movies/porn_15s.mp4"
    Neutral_percent, Porn_percent, Sexy_percent = start_classification(input_vid)

    print("[INFO] it's done! Result is:\n")
    print("Neutral =", Neutral_percent, "%")
    print("Porn =", Porn_percent, "%")
    print("Sexy =", Sexy_percent, "%")
    print("\n--- %s seconds ---" % (time.time() - start_time))
