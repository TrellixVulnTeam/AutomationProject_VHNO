# coding = utf8

import os
import time

os.path.abspath(".")

"""
    测试opencv python从摄像头获取视频、帧率、分辨率、码率等属性设置和使用
    获取实时帧率不准
"""
import cv2

capture = cv2.VideoCapture(0)
# capture.set(6, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
capture.set(6, cv2.VideoWriter.fourcc("Y", "U", "Y", "2"))
capture.set(3, 960)
capture.set(4, 540)
while True:
    start_time = time.time()
    rval, frame = capture.read()
    if rval:
        cv2.imshow("video", frame)
        end_time = time.time()
        whole_time = end_time - start_time
        current_fps = 1 / whole_time
        print("Current fps is {}".format(current_fps))
        cur_fps = capture.get(cv2.CAP_PROP_FPS)
        print("Current video fps is : {}".format(cur_fps))
        total_frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count is:{}".format(total_frame_count))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

capture.release()
cv2.destroyAllWindows()
