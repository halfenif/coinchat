import argparse
import datetime
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import psycopg2

url = 'https://coinone.co.kr/chat/'

def call_loop(args):

    try:
        profile = webdriver.FirefoxProfile()
        driver = webdriver.Firefox(firefox_profile=profile)
        if not args.showwindow:
            driver.minimize_window()

        driver.get(url)
        time.sleep(60)

        items_time = driver.find_elements_by_class_name('time')
        items_msg = driver.find_elements_by_class_name('message_wrapper')

        i = 0
        while i < len(items_time):
            item_time = items_time[i].text
            item_temp = items_msg[i].text.split()
            item_id = item_temp[0]
            item_msg = " ".join(item_temp[1:])

            i = i + 1

            item = {}
            item['daystr']  = datetime.datetime.now().strftime('%Y-%m-%d')
            item['timestr'] = item_time
            item['uid']     = item_id
            item['msg']     = item_msg
            sqlInsert(item)
        print('--------------------------------------------------------------')
    except NoSuchElementException:
        print('NoSuchElementException')

    finally:
        driver.quit()

#---------------------------------
# SQL Insert
def sqlInsert(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_chat ',
                                       '(daystr, timestr, uid, msg ) VALUES (',
                                       Param(item['daystr']),              ',',
                                       Param(item['timestr']),            ',',
                                       Param(item['uid']),                ',',
                                       Param(item['msg']),
                                       ')'
                                       ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        if err.pgcode == '23505':
            #Exist Data
            print('Exist Data', item['timestr'], item['uid'], item['msg'])
            return
        print("sqlInsert.psycopg2.IntegrityError:{}".format(err.pgcode))
        print(err)
    except Exception as err:
        print("sqlInsert.Other Exception:{}".format(err))
        print(err)
    else:
        #print('New Data')
        conn.commit()
    finally:
        conn.close()
    return


if __name__   == "__main__":
    parser = argparse.ArgumentParser(description='CoinOne Chat Archive')

    parser.add_argument('-s', dest='showwindow', action='store_true',
                       required=False, help='Show Window')

    #Parse Argument
    args = parser.parse_args()

    while(1):
        try:
            call_loop(args)
        except Exception as err:
            print("Exception:{}".format(err))
