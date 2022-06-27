import paddlers as pdrs
import cv2
import numpy as np


class Predict_extract: # 地物提取

    def __init__(self, img_path,save_path):
        img = cv2.imread(img_path)
        self.img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)  # 将数据强制转换成256 * 256尺寸
        self.predictor = pdrs.deploy.Predictor('aipro/inference_model_extract')
        self.save_path = save_path

    def Predict(self):
        result = self.predictor.predict(self.img)
        self.output = result['label_map'] * 255

    def Save(self):
        cv2.imwrite(self.save_path, self.output)

'''
if __name__ == '__main__':

    img_path = 'img-40.png'
    #model_path = 
    save_path = "result2.png"

    run = Predict_extract(img_path,save_path)
    run.Predict()
    run.Save()
'''
