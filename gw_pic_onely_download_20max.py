import requests, time, urllib.request, re
from moviepy.editor import *
import os, sys

import imageio
imageio.plugins.ffmpeg.download()

def readfolder():
    f = open('./folder_builder.txt', encoding="utf8")
    lines = f.readlines()
    folderlist = []
    for line in lines:
        if 'nav_label"' in line:
            folder_name = re.findall('>(.+)</span>', line)[0]
            folderlist.append(folder_name)
    f.close()
    return folderlist

def Schedule_cmd(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # Set Download Process Line
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # Set Download Process Line
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    print(percent_str.ljust(6, ' ') + '-' + speed_str)
    f.flush()
    time.sleep(2)
    # print('\r')


    # Format Change
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("Wrong Type")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)


def download_pic(url, currentVideoPath, name):
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
    try:
        urllib.request.urlretrieve(url=url, filename=os.path.join(currentVideoPath, r'{}'.format(name)), reporthook=Schedule_cmd)
        return 0
    except urllib.error.HTTPError as e:
        print(str(e.reason) + str(e.code) + name)
        return 1


if __name__ == '__main__':
    start_time = time.time()
    currentVideoPath = os.path.join(sys.path[0], 'test', 'test')
    first_index_list = ['1','2','3','4','5','6','7','8']
    second_index_list = ['VU', 'VCH', 'VC', 'VO']
#    third_index_list = ['', 'OO', 'C', 'Z', 'G', 'X', 'S']
    third_index_list = ['']
    for first_index in first_index_list:
        for second_index in second_index_list:
            for third_index in third_index_list:
                stop_index = 0
                for number in range(500):
                    if stop_index > 20:
                        break
                    name = first_index + '-' + second_index + '-' + third_index + str(number).zfill(4) + '.jpg'
                    url = 'https://www.cardland-kamata.com/data/cardland/product/' + name
                    stop_index = stop_index + download_pic(url, currentVideoPath, name)
