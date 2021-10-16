#!/usr/bin/python python3
# coding=utf-8
'''
Author: WhaleFall
Date: 2021-10-10 03:28:54
LastEditTime: 2021-10-10 03:42:55
Description: 利用opencv拍照文件
'''
import cv2
from datetime import datetime
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
flag = cap.isOpened()


while (flag):
    ret, frame = cap.read()
    font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
    def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    imgzi = cv2.putText(frame, now(), (50, 50), font,
                        1.2, (255, 255, 255), 2)
    # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度

    cv2.imshow("Rpi-Photo", frame)  # 显示摄像头
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):  # 按下s键，进入下面的保存图片操作
        cv2.imwrite("E:/PyCharm Workspaces/" + "test" + ".jpg", frame)
        print("save" + "test" + ".jpg successfuly!")
        print("-------------------------")
        
    elif k == ord('q'):  # 按下q键，程序退出
        break

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 释放并销毁窗口
