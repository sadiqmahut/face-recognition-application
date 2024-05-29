import threading
import cv2
import pickle
from .predict import predict

class CameraWidget(threading.Thread):
    def __init__(self, dept, div, path_model, src = 0) -> None:
        threading.Thread.__init__(self)
        self.dept = dept
        self.div = div
        self.model = self.open_model(path_model)
        self.src = src

    def open_model(self, path):
        file = open(path, 'rb')
        model = pickle.load(file)
        file.close()
        return model

    def run(self):
        self.gen_frames()

    def gen_frames(self):
        cam = cv2.VideoCapture(self.src)
        while (cam.isOpened()):
            _, frame = cam.read()
            print(predict(frame, self.model))
            frame = cv2.imencode('.jpeg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if cv2.waitKey(1) == 13:
                cam.release()
                cv2.destroyAllWindows()
                break

