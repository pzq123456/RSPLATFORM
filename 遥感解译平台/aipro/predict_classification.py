import paddlers as pdrs
import cv2
import numpy as np

# 此模型输入图片必须为256 * 256
class Predict_classification:

    def __init__(self, img_path,save_path):

        img = cv2.imread(img_path)
        self.img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_LINEAR)  # 将数据强制转换成256 * 256尺寸
        self.predictor = pdrs.deploy.Predictor('aipro/inference_model_classification' ) # 直接导入模型
        self.save_path = save_path
        self.lut = np.zeros((256, 3), dtype=np.uint8)
        self.lut[0] = [255, 0, 0]
        self.lut[1] = [30, 255, 142]
        self.lut[2] = [60, 0, 255]
        self.lut[3] = [255, 222, 0]
        self.lut[4] = [0, 0, 0]

    def Predict(self):
        result = self.predictor.predict(self.img)
        output = result['label_map']
        self.im = self.lut[output]

    def Save(self):
        cv2.imwrite(self.save_path, self.im)

'''
if __name__ == '__main__':
    img_path = './T000036.jpg'  # 遥感影像
    model_file = 'inference_model_classification'  # 模型文件 # 改为相对路径
    save_path = './test_img.png'  # 保存路径
    run = Predict_classification(img_path, model_file, save_path)
    run.Predict()
    run.Save()

'''
