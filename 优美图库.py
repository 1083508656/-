
import requests
import re
import os
import time

'''
1.通过链接获取详情页url，标题名字
创建功能，获取详情页地址：
XXXX

2.获取详情页获取图片下载地址，翻页的url
3.通过下载地址下载图片
'''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
def download_img(img_url,i,k,title):
        
    img_page = requests.get(img_url, headers=headers)
    img_page.encoding = img_page.apparent_encoding
    img_1 = re.findall(r'https://(.*?).jpg', img_page.text)[0]
    
    img = 'https://' + img_1 + '.jpg'
    img_name = f"{title}/" + i + "/" + str(k) + ".jpg"
    with open (img_name, 'wb') as f:
        f.write(requests.get(img).content)
    f.close()
    print('第' + str(k) + '张图片下载完成')

def get_img_url(url):
    l = 0
    
    while True:
        l += 1
        print('正在获取第' + str(l) + '页图片')
        r = requests.get(url +str(l)+'.htm', headers=headers)
        if r.status_code != 200:
            print('下载完成')
            break
        else:
            time.sleep(1)
        r.encoding = r.apparent_encoding
        con = re.findall(r'<span>(.*?)</span></a>', r.text)
        
        img_num = re.findall(rf'a href="{url}(.*?).htm"', r.text)
        title = re.findall(r'<title>【(.*?)】.*?</title>', r.text)
        title = title[0]
        if not os.path.exists(title):
            os.mkdir(title)
        k = 0
        for j in img_num:
            page_url = url + j + '.htm'
            page = requests.get(page_url, headers=headers)
            page.encoding = page.apparent_encoding
            page_num = re.findall(r'共(.*?)页:', page.text)
            if len(page_num) == 0:
                page_num = 1
            else:
                page_num = page_num[0]
            i = con[k]
            
            if not os.path.exists(f"{title}/" + i):
                os.mkdir(f"{title}/" +i)
            print('正在下载图片：' + i,'共' + str(page_num) + '张')
            
            for k in range(1， int(page_num)+1):
                if k == 1:
                    download_img(page_url,i,k,title)
                else:
                    img_url2 = page_url[:-4] + '_' + str(k) + '.htm'
                    download_img(img_url2,i,k,title)
            k += 1 
            
if __name__ == '__main__':
    url = 'http://www.umeituku.com/bizhitupian/shoujibizhi/'#修改url
    get_img_url(url)

