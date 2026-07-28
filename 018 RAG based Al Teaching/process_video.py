# converts video to mp3

import os
import subprocess

files=os.listdir("video")
print(files)

for file in files:
    tutorial_num=file.split(" [")[0].split(" #")[1]

    file_name=file.split(" ｜ ")[0]
    print(tutorial_num, file_name)
    subprocess.run(["ffmpeg", "-i" , f"video/{file}", f"audio/{tutorial_num}_{file_name}.mp3"])