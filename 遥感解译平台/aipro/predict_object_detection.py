import paddlers as pdrs
import numpy as np
import cv2
from paddlers.tasks.utils.visualize import visualize_detection


class Predict_object_detection:

    def __init__(self, img_path,save_path):
        img = cv2.imread(img_path)
        self.img = cv2.resize(img, (608, 608), interpolation=cv2.INTER_LINEAR)
        self.predictor = pdrs.deploy.Predictor('aipro\inference_model_object_detection')
        self.save_path = save_path

    def Predict(self):
        result = self.predictor.predict(self.img)
        vis = self.img
        self.vis = visualize_detection(
            np.array(vis), result,
            color=np.asarray([[0, 255, 0]], dtype=np.uint8),
            save_dir=None
        )

    def Save(self):
        cv2.imwrite(self.save_path, self.vis)

'''
if __name__ == '__main__':
    img_path = 'C:\\Users\\Administrator\\Desktop\\RS_model_data\\RSOD-Dataset\\RSOD-Dataset\\playground\\playground\\JPEGImages\\playground_8.jpg'
    model_path = 'C:\\Users\\Administrator\\Desktop\\RS_model_data\\object_detection\\inference_model_object_detection'
    save_path = 'C:\\Users\\Administrator\\Desktop\\test.png'
    run = Predict_object_detection(img_path, model_path, save_path)
    run.Predict()
    run.Save()

'''




