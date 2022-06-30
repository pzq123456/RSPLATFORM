import paddlers as pdrs
import cv2
import numpy as np


class Predict_buiding_change:

    # 读取两时相影像
    def __init__(self, img_path1, img_path2, save_path_1,save_path_2):
        img1 = cv2.imread(img_path1)
        img2 = cv2.imread(img_path2)
        self.img1 = cv2.resize(img1, (1024, 1024), interpolation=cv2.INTER_LINEAR)  # 将数据强制转换成1024 * 1024尺寸
        self.img2 = cv2.resize(img2, (1024, 1024), interpolation=cv2.INTER_LINEAR)
        self.img2 = cv2.imread(img_path2)
        self.predictor = pdrs.deploy.Predictor('aipro/inference_model_building') # 直接加载模型 相对路径
        self.save_path_1 = save_path_1
        self.save_path_2 = save_path_2

    # 将1024 * 1024的影像进行裁剪，得到一个包含16个256 * 256影像的列表
    def Crop_img(self, w, h):
        # 切割第一时相影像
        self.img_list1 = ['0' for j in range(0, 16, 1)]
        self.img_list1[0] = self.img1[0:int(h / 4), 0:int(w / 4), :]
        self.img_list1[1] = self.img1[0:int(h / 4), int(w / 4):int((w / 4) * 2), :]
        self.img_list1[2] = self.img1[0:int(h / 4), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list1[3] = self.img1[0:int(h / 4), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list1[4] = self.img1[int(h / 4):int((h / 4) * 2), 0:int(w / 4), :]
        self.img_list1[5] = self.img1[int(h / 4):int((h / 4) * 2), int(w / 4):int((w / 4) * 2), :]
        self.img_list1[6] = self.img1[int(h / 4):int((h / 4) * 2), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list1[7] = self.img1[int(h / 4):int((h / 4) * 2), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list1[8] = self.img1[int((h / 4) * 2):int((h / 4) * 3), 0:int(w / 4), :]
        self.img_list1[9] = self.img1[int((h / 4) * 2):int((h / 4) * 3), int(w / 4):int((w / 4) * 2), :]
        self.img_list1[10] = self.img1[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list1[11] = self.img1[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list1[12] = self.img1[int((h / 4) * 3):int((h / 4) * 4), 0:int(w / 4), :]
        self.img_list1[13] = self.img1[int((h / 4) * 3):int((h / 4) * 4), int(w / 4):int((w / 4) * 2), :]
        self.img_list1[14] = self.img1[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list1[15] = self.img1[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 3):int((w / 4) * 4), :]

        # 切割第二时相影像
        self.img_list2 = ['0' for j in range(0, 16, 1)]
        self.img_list2[0] = self.img2[0:int(h / 4), 0:int(w / 4), :]
        self.img_list2[1] = self.img2[0:int(h / 4), int(w / 4):int((w / 4) * 2), :]
        self.img_list2[2] = self.img2[0:int(h / 4), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list2[3] = self.img2[0:int(h / 4), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list2[4] = self.img2[int(h / 4):int((h / 4) * 2), 0:int(w / 4), :]
        self.img_list2[5] = self.img2[int(h / 4):int((h / 4) * 2), int(w / 4):int((w / 4) * 2), :]
        self.img_list2[6] = self.img2[int(h / 4):int((h / 4) * 2), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list2[7] = self.img2[int(h / 4):int((h / 4) * 2), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list2[8] = self.img2[int((h / 4) * 2):int((h / 4) * 3), 0:int(w / 4), :]
        self.img_list2[9] = self.img2[int((h / 4) * 2):int((h / 4) * 3), int(w / 4):int((w / 4) * 2), :]
        self.img_list2[10] = self.img2[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list2[11] = self.img2[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 3):int((w / 4) * 4), :]

        self.img_list2[12] = self.img2[int((h / 4) * 3):int((h / 4) * 4), 0:int(w / 4), :]
        self.img_list2[13] = self.img2[int((h / 4) * 3):int((h / 4) * 4), int(w / 4):int((w / 4) * 2), :]
        self.img_list2[14] = self.img2[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 2):int((w / 4) * 3), :]
        self.img_list2[15] = self.img2[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 3):int((w / 4) * 4), :]

    def Predict(self):
        self.pre_list = ['0' for j in range(0, 16, 1)]
        for i in range(0, 16, 1):
            img_b = np.array(self.img_list1[i])
            img_a = np.array(self.img_list2[i])
            result = self.predictor.predict((img_b, img_a))
            output = np.where(result[0]['label_map'] == 1, 255, 0)
            self.pre_list[i] = output

    # 将预测的影像进行拼接
    def Splicing_method(self, h, w):
        self.img_prob = np.zeros((h, w), np.uint8)

        self.img_prob[0:int(h / 4), 0:int(w / 4)] = self.pre_list[0]
        self.img_prob[0:int(h / 4), int(w / 4):int((w / 4) * 2)] = self.pre_list[1]
        self.img_prob[0:int(h / 4), int((w / 4) * 2):int((w / 4) * 3)] = self.pre_list[2]
        self.img_prob[0:int(h / 4), int((w / 4) * 3):int((w / 4) * 4)] = self.pre_list[3]

        self.img_prob[int(h / 4):int((h / 4) * 2), 0:int(w / 4)] = self.pre_list[4]
        self.img_prob[int(h / 4):int((h / 4) * 2), int(w / 4):int((w / 4) * 2)] = self.pre_list[5]
        self.img_prob[int(h / 4):int((h / 4) * 2), int((w / 4) * 2):int((w / 4) * 3)] = self.pre_list[6]
        self.img_prob[int(h / 4):int((h / 4) * 2), int((w / 4) * 3):int((w / 4) * 4)] = self.pre_list[7]

        self.img_prob[int((h / 4) * 2):int((h / 4) * 3), 0:int(w / 4)] = self.pre_list[8]
        self.img_prob[int((h / 4) * 2):int((h / 4) * 3), int(w / 4):int((w / 4) * 2)] = self.pre_list[9]
        self.img_prob[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 2):int((w / 4) * 3)] = self.pre_list[10]
        self.img_prob[int((h / 4) * 2):int((h / 4) * 3), int((w / 4) * 3):int((w / 4) * 4)] = self.pre_list[11]

        self.img_prob[int((h / 4) * 3):int((h / 4) * 4), 0:int(w / 4)] = self.pre_list[12]
        self.img_prob[int((h / 4) * 3):int((h / 4) * 4), int(w / 4):int((w / 4) * 2)] = self.pre_list[13]
        self.img_prob[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 2):int((w / 4) * 3)] = self.pre_list[14]
        self.img_prob[int((h / 4) * 3):int((h / 4) * 4), int((w / 4) * 3):int((w / 4) * 4)] = self.pre_list[15]

    def Save_img(self):
        # 改 运行一次算法把结果存到两个地方
        cv2.imwrite(self.save_path_1, self.img_prob)
        cv2.imwrite(self.save_path_2, self.img_prob)

'''
if __name__ == '__main__':

    img_path1 = 'train_1.png'  # 第一时相影像
    img_path2 = 'train_2.png'  # 第二时相影像
    model_file = 'building_change\inference_model_building'  # 模型文件
    save_path = './result.png'  # 保存路径
    # 预测
    run = Predict_buiding_change(img_path1, img_path2, model_file, save_path)
    run.Crop_img(1024, 1024)
    run.Predict()
    run.Splicing_method(1024, 1024)
    run.Save_img()


'''

