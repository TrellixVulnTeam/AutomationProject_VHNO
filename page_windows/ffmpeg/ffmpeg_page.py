# coding = utf8
import os
import subprocess

from toolsbar.common import create_folder

os.path.abspath(".")


class Ffmpeg_Page:

    def __init__(self, case_saved_folder, case_picture_saved_folder):
        """
            {}分别代表：
                1、视频存放根目录（自定义好Ev录屏存放地址）
                2、case几（1~28）
                3、当前case的第几次测试视频
                4、存放的帧图片根目录
                5、case几（1~28）
                6、第几次（1~10）
                如：
                ffmpeg -i D:\\For_Work\\PandaOs性能测试_study\\temp\\case1_testVideo_1_times.mp4 -q:v 1 -f image2 D:\\For_Work\\PandaOs性能测试_study\\test_result_temp\\case1_and_1_times_frame_picture\\xxx_%05d.jpg
        """
        # self.cut_command = r"ffmpeg -i {}case{}_testVideo_{}.mp4 -q:v 1 -f image2 {}case{}_and_{}_times_frame_picture\\xxx_%05d.jpg"
        # case固定录屏存放path和ev recorder录制存放地址一致
        # self.case_saved_folder = "D:\\For_Work\\PandaOs性能测试_study\\temp\\"
        self.case_saved_folder = case_saved_folder
        # # case号随测试变动（1~28）
        # self.case_number = "1"
        # # case第几次随测试变动（1~10）
        # self.case_count = "1"
        # # 总case固定存放图片path
        # self.case_picture_saved_folder = "D:\\For_Work\\PandaOs性能测试_study\\test_result_temp\\"
        self.case_picture_saved_folder = case_picture_saved_folder

    def cut_video_into_pieces_frame_picture(self, case_number, case_count):
        video_path = "{}case{}_testVideo_{}.mp4".format(self.case_saved_folder, case_number, case_count)
        picture_path = "{}case{}_and_{}_times_frame_picture".format(self.case_picture_saved_folder,
                                                                    case_number, case_count)
        command = "ffmpeg -i {} -q:v 1 -f image2 {}\\测试图片_%05d.jpg".format(video_path, picture_path)
        # 如无文件夹就创建，有就删除再创建
        if create_folder(picture_path):
            cut_result = \
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1]
            if cut_result and "failed" not in str(cut_result):
                print("Cut success!")
            else:
                print(cut_result)
                print("FAILED cut:\n" + str(cut_result))


if __name__ == '__main__':
    ffmpeg_page = Ffmpeg_Page()
    ffmpeg_page.cut_video_into_pieces_frame_picture("1", "1")
