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

namelist_buffer = []
namelist = []

def download_pic(url, currentVideoPath, name):
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
    try:
        urllib.request.urlretrieve(url=url, filename=os.path.join(currentVideoPath, r'{}'.format(name)), reporthook=Schedule_cmd)
        print(name + 'success')
        return 
    except urllib.error.HTTPError as e:
        print(str(e.reason) + str(e.code) + name)
        return


if __name__ == '__main__':
    name_org = ['1-U-0245.jpg', '1-U-0252.jpg', '1-U-0276.jpg', '1-U-0297.jpg', '1-U-0313.jpg', '1-U-0337.jpg', '1-U-0355.jpg', '1-U-0366.jpg', '1-U-0381.jpg', '1-U-0395.jpg', '1-U-0412.jpg', '1-U-0424.jpg', '2-U-0226.jpg', 
'2-U-0247.jpg', '2-U-0254.jpg', '2-U-0266.jpg', '2-U-0287.jpg', '2-U-0302.jpg', '2-U-0311.jpg', '2-U-0320.jpg', '2-U-OO0012.jpg', '2-U-OO0023.jpg', '2-U-OO0032.jpg', '2-U-OO0040.jpg', '2-U-OO0050.jpg', '2-O-OO0007.jpg', '3-U-0121.jpg', '3-U-0129.jpg', '3-U-0139.jpg', '3-U-0146.jpg', '3-U-0162.jpg', '3-U-0170.jpg', '3-U-0181.jpg', '3-U-0191.jpg', '3-U-0201.jpg', '3-U-OO0001.jpg', '3-U-OO0013.jpg', '3-U-OO0020.jpg', 
'3-C-OO0004.jpg', '3-C-Z0055.jpg', '4-U-0139.jpg', '4-U-0170.jpg', '4-U-0194.jpg', '4-U-C0062.jpg', '4-U-C0067.jpg', '4-U-C0082.jpg', '4-U-C0087.jpg', '4-U-C0092.jpg', '4-U-C0103.jpg', '4-U-C0109.jpg', '4-U-C0122.jpg', '4-U-C0129.jpg', '5-U-G0001.jpg', '5-U-G0014.jpg', '5-U-G0025.jpg', '5-U-G0035.jpg', '5-U-G0045.jpg', '5-U-G0057.jpg', '5-U-G0062.jpg', '5-U-G0074.jpg', '5-U-G0083.jpg', '5-U-G0092.jpg', '5-U-X0069.jpg', '5-U-X0077.jpg', '6-U-0120.jpg', '6-U-0127.jpg', '6-U-S0007.jpg', '6-U-S0079.jpg', '6-U-S0110.jpg', '6-U-S0120.jpg', '6-U-S0138.jpg', '6-U-S0155.jpg', '6-U-S0178.jpg', '6-U-S0182.jpg', '6-U-S0189.jpg', '6-U-S0202.jpg', '6-U-S0227.jpg', '6-U-S0235.jpg', '8-U-OO0003.jpg', '8-U-OO0004.jpg', '8-U-OO0010.jpg', '8-U-OO0015.jpg', '8-U-OO0019.jpg']
    name1 = [chr(i) for i in range(65,91)]
    start_time = time.time()
    currentVideoPath = os.path.join(sys.path[0], 'test', 'test')
    for first_index in name_org:
        for second_index in name1:
            name = first_index[:-4] + str(second_index) + '.jpg'
            url = 'https://www.cardland-kamata.com/data/cardland/product/' + name
            download_pic(url, currentVideoPath, name)

    pass
