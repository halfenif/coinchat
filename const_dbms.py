import dbms

def get_conn():
    return dbms.connect.postgres('coinchat', 'coinchat', 'coinchat', host="192.168.0.104")
