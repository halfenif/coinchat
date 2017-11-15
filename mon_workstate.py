import sys
import time
import datetime
import argparse

import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
from itertools import count

def display_workstate(args):
    if args.daystr == None:
        daystr = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        daystr = args.daystr

    print('Collect Count Per Hour [{daystr}]'.format(daystr=daystr))

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT timestr, COUNT(timestr) timestr_cnt FROM ( ',
                                       'SELECT substr(timestr,1,2) timestr FROM tb_chat WHERE daystr = ',
                                       Param(daystr),
                                       ') t GROUP BY timestr ORDER BY timestr DESC'
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)

    for i, row in enumerate(cur.fetchall()):
        print('[ {timestr} ] {timestr_cnt}'.format(timestr=row['timestr'], timestr_cnt=format(row['timestr_cnt'],',')))
    conn.close()

    print('-------------------------------')
    return


def main(args):
    display_workstate(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CoinOne Chat Monitoring')

    parser.add_argument('-d', dest='daystr', action='store',
                       required=False, help='Some day')

    #Parse Argument
    args = parser.parse_args()
    main(args)
