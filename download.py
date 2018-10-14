# coding=UTF-8
import sys, os


def main():
  lines, title, curr, ctr = None, None, None, 0
  HOME_URL = sys.argv[2]
  with open(sys.argv[1],'r') as f:
      lines = f.readlines()

  for line in lines:
      line = line.rstrip()
      if 'Title' in line:
          title = line.split(':')[1]
          os.system('mkdir -p "'+title+'"')
      if 'Ep' in line:
          ctr = 0
          ep = line.split(':')[1]
          curr = title+'/'+ep
          os.system('mkdir -p "'+ curr+'"')
          print '[INFO] Create Folder: ' + ep
      if 'CH' in line:
          ctr += 1
          _, url = line.split(';UR')
          url = HOME_URL + url.split(':')[1]
          print '[INFO] Download: ' + _.split(':')[1]
          cmd = 'curl -ks ' + url + '  | iconv -f gbk -t utf-8 > "' + \
                  curr + '/' + str(ctr) + '.txt"'
          os.system(cmd)


if __name__=='__main__':
    main()
