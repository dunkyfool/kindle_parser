#!/bin/bash

# 哥布林殺手
HOME_URL='https://www.wenku8.net/novel/2/2084/'
# 灰與幻想的格林姆迦爾
HOME_URL='https://www.wenku8.net/novel/1/1546/'


TABLE=TABLE
JSON=table.json
DIFF=DIFF
BAK=BAK


# get all novel url
function getURL {
  rm -f ${JSON}
  rm -f ${TABLE}
  curl -ks ${HOME_URL}  | iconv -f gbk -t utf-8 | grep -E 'id="title"|colspan|href="[0-9].+.htm"' > ${TABLE}
  python parse.py table ${TABLE}
  #cat ${TABLE}
  #cat ${JSON}
}


# check whether there are new novels or not
function checkUpdate {
  TITLE=$(grep Title ${JSON}| cut -d':' -f2)
  if [ -e ${TITLE}/${JSON} ]; then
    touch ${TITLE}/${JSON}
  fi
  comm -3 ${JSON} ${TITLE}/${JSON} > ${DIFF}
  if [ -s ${DIFF} ]; then
    echo "[INFO] Find New Novel"
    cp ${JSON} ${BAK}
    echo "Title:${TITLE}" > ${JSON}
    cat ${DIFF} >> ${JSON}
  else
    echo "[INFO] No Update"
    exit 0
  fi
}


# download all chapters
function download {
  python download.py ${JSON} ${HOME_URL}
}


# parse content & change to utf-8
function parse {
  TITLE=$(grep Title ${JSON}| cut -d':' -f2)
  CH_arr=$(grep Ep ${JSON}| cut -d':' -f2| cut -d';' -f1)
  for CH in ${CH_arr[@]}; do
    COLLECTION=${TITLE}/${CH}
    NAME="${TITLE} ${CH}.txt"

    echo "[INFO] Parse ${NAME}"
    rm -f TMP
    rm -f "${COLLECTION}/${NAME}"
    for file in `ls ${COLLECTION} | sort -n`;
    do
      python parse.py content ${COLLECTION}/${file}
    done
    mv TMP "${COLLECTION}/${NAME}"
  done
}


# send to kindle
function send {
  echo "[INFO] Send TXT File to Kindle"
  TITLE=$(grep Title ${JSON}| cut -d':' -f2)
  CH_arr=$(grep Ep ${JSON}| cut -d':' -f2| cut -d';' -f1)
  for CH in ${CH_arr[@]}; do
    COLLECTION=${TITLE}/${CH}
    NAME="${TITLE} ${CH}.txt"

    echo "[INFO] Send ${NAME}"
    python send.py "${COLLECTION}/${NAME}"
  done
}


function archive {
  TITLE=$(grep Title ${JSON}| cut -d':' -f2)
  mv ${BAK} ${JSON}
  cp ${TABLE} ${TITLE}
  cp ${JSON} ${TITLE}
}


# main
function main {
  getURL
  checkUpdate
  download
  parse
  send
  archive
}


main
