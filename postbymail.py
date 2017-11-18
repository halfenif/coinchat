import argparse
import datetime
import time

import smtplib
from email.mime.text import MIMEText

import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import psycopg2

def get_post(args):
    if args.daystr == None:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        daystr = yesterday.strftime('%Y-%m-%d')
    else:
        daystr = args.daystr

    post_title = []
    post_content = []
    i = 0
    while i < 6:
        begin = format(int(i*4), "02d")
        end   = format(int((i+1)*4)-1, "02d")
        post_title.append('{daystr} [{begin}~{end}]'.format(daystr=daystr, begin=begin, end=end))
        post_content.append('')
        i = i + 1

    #print(post_title)

    rows = sqlSelect(daystr)
    for row in rows:
        i = int(int(row['reghour'])/4)
        post_content[i] = post_content[i] + '[{timestr} {uid}]\t{msg}\n'.format(timestr=row['timestr'], uid=row['uid'], msg=row['msg'])

    return post_title, post_content

#---------------------------------
# SQL Select
def sqlSelect(daystr):
    rows = []

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT daystr, timestr, uid, msg, ',
                                       "to_char(regdate,'hh24') reghour " ,
                                       "FROM tb_chat WHERE to_char(regdate, 'yyyy-mm-dd') = ",
                                       Param(daystr), ' ',
                                       'ORDER BY regdate asc'
                                       ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
        for i, row in enumerate(cur.fetchall()):
            rows.append(row)

        print('Rows {count}'.format(count=i))
    except Exception as err:
        print("sqlSelect.Other Exception:{}".format(err))
        print(err)
    finally:
        conn.close()

    return rows

def send(args):
    post_title, post_content = get_post(args)

    i = 0
    while i < 6:
        if post_content[i] == '':
            i = i + 1
            continue

        # 텍스트를 MIME 형식으로 바꾼다.
        msg = MIMEText(post_content[i])

        msg['Subject'] = post_title[i]
        msg['From'] = args.from_addr
        msg['To'] = args.to_addr

        # 로컬 SMTP 서버가 없을 경우 계정이 있는 다른 서버를 사용하면 된다.
        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login(args.from_addr, args.passwd)
        s.sendmail(args.from_addr, args.to_addr, msg.as_string())
        s.quit()
        print('Send', post_title[i])

        i = i + 1
        time.sleep(10)
    return

if __name__   == "__main__":
    parser = argparse.ArgumentParser(description='CoinOne Chat Send Mail')

    parser.add_argument('-f', dest='from_addr', action='store',
                       required=True, help='From Email Address')

    parser.add_argument('-t', dest='to_addr', action='store',
                       required=True, help='To Email Address')

    parser.add_argument('-p', dest='passwd', action='store',
                       required=True, help='Send Email Password')

    parser.add_argument('-d', dest='daystr', action='store',
                       required=False, help='Some day')

    #Parse Argument
    args = parser.parse_args()

    send(args)
