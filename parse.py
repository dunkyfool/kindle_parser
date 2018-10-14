# coding=UTF-8
import sys, re
from hanziconv import HanziConv

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_content():
  lines = None
  flag = False
  with open(sys.argv[2],'r') as f:
      lines = f.readlines()

  with open('TMP','a') as f:
    for line in lines:
        line = line.rstrip()
        if '<title>' in line:
            line = re.sub(r"<title>", "", line)
            line = re.sub(r"</title>", "", line)
            line = "# "+line+"#\n"
            #print line
            #f.write(HanziConv.toTraditional(line))
            f.write(line)
        if '<div id="content">' in line:
            flag = True
        if flag:
            line = re.sub(r"<div.+", "", line)
            line = re.sub(r"\&nbsp;", "", line)
            line = re.sub(r"<br />", "", line)
            line = re.sub(r"<ul.+ul>", "", line)
            if '</div>' in line:
                break
            line = line+"\n"
            #print line
            #f.write(HanziConv.toTraditional(line))
            f.write(line)


def parse_table():
  lines = None
  episode = 1
  with open(sys.argv[2],'r') as f:
      lines = f.readlines()

  with open('table.json', 'a') as f:
    for line in lines:
        line = line.rstrip()
        if 'title' in line:
            line = re.sub(r"<div id=\"title\">", "", line)
            line = re.sub(r"</div>", "", line)
            line = re.sub(r"\(.+\)", "", line)
            line = 'Title:' + line + '\n'
            #print line
            #f.write(HanziConv.toTraditional(line))
            f.write(line)
        elif 'colspan' in line:
            line = re.sub(r"    <td class=\"vcss\" colspan=\"4\">", "", line)
            line = re.sub(r"</td>", "", line)
            line = line.split(' ',2)[0]
            line = 'Ep:' + line + '\n'
            #print line
            #f.write(HanziConv.toTraditional(line))
            f.write(line)
        elif 'href' in line and '插图' not in line :
            line = re.sub(r"    <td class=\"ccss\"><a href=\"", "", line)
            line = re.sub(r"</a></td>", "", line)
            line = re.sub(r"\">", ",", line)
            url, name = line.split(',')
            line = 'CH:' + name + ';URL:' + url + '\n'
            #print line 
            #f.write(HanziConv.toTraditional(line))
            f.write(line)


def main():
  print '[INFO] Command: '+' '.join(sys.argv)
  if sys.argv[1] == 'content':
      print '[INFO] Parse Content'
      parse_content()
  elif sys.argv[1] == 'table':
      print '[INFO] Parse Table'
      parse_table()


if __name__=='__main__':
    main()
