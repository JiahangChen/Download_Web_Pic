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


def download_pic(url_list, name_list, currentVideoPath):
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
    for i in range(len(url_list)):
        url = url_list[i]
        name = name_list[i]
        urllib.request.urlretrieve(url=url, filename=os.path.join(currentVideoPath, r'{}'.format(name)), reporthook=Schedule_cmd)
        print(i)
      #  print(name + 'Success')

def get_play_list(url_page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': 'PHPSESSID=nricelqdmjsu6counkrm12640atabab0vle3t3h3mdoio6gmfbo1vktcdm3hmn1hn748kcinkcm4ujg643j6ok6ole6v1eip0up3nfhioshfd86a713u9lafa2nob9da', # SESSDATA here, validate 30 days. 
        'Host': 'www.cardland-kamata.com',
    }
    html_get_pagemun = requests.get(url_page, headers=headers).text
    pagenum_list = re.findall('pager_btn">(\d+)', html_get_pagemun)
    pagenum_list = ['1'] + pagenum_list[: int(len(pagenum_list)/2)]
    object_url_list = []
    object_name_list = []
    for page in pagenum_list:
        url_api = url_page + '?page=' + page
        all_object_page_link = []
        html_all = requests.get(url_api, headers=headers).text
        raw_links = re.findall(r'https://www.cardland-kamata.com/product/(\d+)', html_all)
        for link in raw_links:
            all_object_page_link.append('https://www.cardland-kamata.com/product/' + link)
        for link in all_object_page_link:
            html_specific = requests.get(link).text
            span_num = re.search(r'https://www.cardland-kamata.com/data/cardland/product/(.)+"', html_specific).span()
            pic_url = html_specific[span_num[0]:span_num[1] - 1]
            object_url_list.append(pic_url)
            name_org = re.findall(r't/.*$', pic_url)[0][2:]
            # name1 = name_org[:-8]
            name1 = re.findall( '(^.*?-.*?)0', name_org)[0]
            if name1[0] == '2':
                colour_code = 'G'
            elif name1[0] == '3':
                colour_code = 'B'
            elif name1[0] == '4':
                colour_code = 'R'
            elif name1[0] == '1':
                colour_code = 'U'
            elif name1[0] == '5':
                colour_code = 'Y'
            elif name1[0] == '6':
                colour_code = 'W'
            elif name1[0] == '7':
                colour_code = 'P'
            elif name1[0] == '8':
                colour_code = 'P'
            elif name1[0] == '0':
                colour_code = 'Q'

            name2 = re.findall('^.*?-.*?0+(.*)', name_org)[0][:-4]
            #name2 = re.findall( '0*(.+)', name_org[-8:-4] )[0]
            
            name3 = re.findall('<span class="goods_name">(.+)</span>', html_specific)[0]

            name3 = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', name3)

            name = colour_code + ' ' + name1[2:] + name2 + ' ' + name3 + '.jpg'
            object_name_list.append(name)
            print(name)
    
    return object_url_list, object_name_list



if __name__ == '__main__':
    start_time = time.time()
    folderlist = readfolder()     # Don't forget to renew this list after the update
    print('readfolder success')
#    for page_number in range(467, 491):  # From 21 to 24
    for page_number in range(487, 488):
        print(str(page_number - 466) + 'start')
        currentVideoPath = os.path.join(sys.path[0], 'Pic', folderlist[page_number - 467])
        url_page = 'https://www.cardland-kamata.com/product-list/' + str(page_number)
        url_list, name_list = get_play_list(url_page)
        download_pic(url_list, name_list, currentVideoPath)