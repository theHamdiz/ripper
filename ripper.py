#!/usr/bin/env python3

""" Tumbrl downloader
This program will download
all the images from a Tumblr blog """

__author__ = "a7madx7"
__license__ = "BSD"
__version__ = "0.3"
__email__ = "ahmad.hamdi.emara@gmail.com"
__status__ = "Beta"

class RColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from urllib.request import urlopen, urlretrieve

import os, sys, re

def check_url(url):
  # Test if url is ok
  url_parsed = re.findall(".tumblr.com", url)
  if len(url_parsed) < 1:
    # if not a full tumblr url, we should check if its not tumblr
    url_parsed = re.findall(".com", url)
    # if it contains another domain and not tumblr.com then its another website
    if len(url_parsed) > 0:
      return ""
    else:
      print(str(RColors.BLUE) + "Tumblr blog name only detected")
      print(str(RColors.GREEN))
      return "https://" + url + ".tumblr.com/"
  else:
    return url

def get_images_page(html_code):

  images =re.findall("src=\"(?:.[^\"]*)_(?:[0-9]*).(?:jpg|png|gif|jpeg|jpg-large|jpeg-large|mp4|wmv|flv|webm|mpeg|mkv|avi|bmp|tiff|raw|jbig|svg|bpg|webp|exif|jiff|heif)\"", html_code)

  forbidden = ["avatar"]

  images = list(set(images))
  #for im in images:
  #  print(im)
  images_http = []
  for im in images:
    for word in forbidden:
      if word not in im:
        images_http.append(im[5:-1])

  print(str(RColors.BLUE) +"Number of images: " + str(RColors.BOLD) + str(len(images_http)))
  print(str(RColors.GREEN) + ("=-" * 20 ) + '+')
  #for im in images_http:
  #  print(im)
  return images_http

def check_end(html1, html2, num):
  h1 = html1
  h2 = html2
  for n in range(-2,1):
    h1 = h1.replace(str(num+n),"")
    h2 = h2.replace(str(num+n),"")

  return (h1 == h2)

def download_images(images, path):
  for im in images:
    print(str(RColors.BLUE) + im)

    extension = os.path.splitext(im)[1]

    im_big = im.replace("250", "1280")
    im_big = im_big.replace("500", "1280")

    filename = re.findall("([^/]*).(?:jpg|png|gif|jpeg|jpg-large|jpeg-large|mp4|wmv|flv|webm|mpeg|mkv|avi|bmp|tiff|raw|jbig|svg|bpg|webp|exif|jiff|heif)",im)[0]
    filename = os.path.join(path,filename)
    filename = filename + extension

    filename_big = re.findall("([^/]*).(?:jpg|png|gif|jpeg|jpg-large|jpeg-large|mp4|wmv|flv|webm|mpeg|mkv|avi|bmp|tiff|raw|jbig|svg|bpg|webp|exif|jiff|heif)",im_big)[0]
    filename_big = os.path.join(path,filename_big)
    filename_big = filename_big + extension

    try:
      urlretrieve(im_big, filename_big)
    except:
      try:
        urlretrieve(im, filename)
      except:
        print(str(RColors.WARNING) + "Failed to download " + im)

def main():

  # Check input arguments
  if len(sys.argv) < 2:
    print("usage: ./tumblr.py url[starting page]")
    sys.exit(1)

  url = sys.argv[1]
  if len(sys.argv) == 3:
    pagenum = int(sys.argv[2])
  else:
    pagenum = 1

  url = check_url(url)  
  print(url)
  if (url == ""):
    print(str(RColors.FAIL) + "Error: Malformed url")
    print(str(RColors.GREEN))
    sys.exit(1)

  if (url[-1] != "/"):
    url += "/"

  blog_name = url.replace("https://", "")
  blog_name = re.findall("(?:.[^\.]*)", blog_name)[0]
  current_path = os.getcwd()
  path = os.path.join(current_path, blog_name)
  #Create blog directory
  if not os.path.isdir(path):
    os.mkdir(path)

  html_code_old = ""
  while(True):
    #fetch html from url
    print(str(RColors.HEADER) + "\nFetching images from page " + str(RColors.BOLD) + str(pagenum) + "\n")
    f = urlopen(url + "page/" + str(pagenum))
    html_code = f.read()
    html_code = str(html_code)
    if(check_end(html_code, html_code_old, pagenum)):
      break

    images = get_images_page(html_code)
    download_images(images, path)

    html_code_old = html_code
    pagenum += 1


  print("Done downloading all images from " + url)


if __name__ == '__main__':
  main()
