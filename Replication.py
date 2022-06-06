import psycopg2
import sys
import time
import os, platform
from psycopg2 import Error


def Connect(ip_addr):
    try:
        connection = psycopg2.connect(user="postgres", password="12345", host=ip_addr, port="5432", database="postgres")
        cursor = connection.cursor()
        sql_query = 'select 1;'
        cursor.execute(sql_query)
        connection.commit()
        print("База данных доступна")
    except (Exception, Error) as error:
        print("База данных не доступна")


def Availability(host):
    response = os.system("ping -c 1 " + host + " > /dev/null")
    if response == 0:
        Status = True
    else:
        Status = False
    return Status


def Replication(ip_addr_m, ip_addr_s):
    id = 1
    flag_promote = False
    flag_master_drop = False
    while (True):
     if (Availability(ip_addr_m) and flag_master_drop == False):
        print(f"[{id}] Основная база данных подключена")
        Connect(ip_addr_m)
    if (not Availability(ip_addr_m) and Availability(ip_addr_s)):
        print(f"[{id}] [Основная база данных не доступна, переключено на резервную]")
        Connect(ip_addr_s)
        flag_master_drop = True
        if (flag_promote == False):
            os.system(f"ssh postgres@{ip_addr_s} '/usr/lib/postgresql/14/bin/pg_ctl promote -D /var/lib/postgresql/14/main > /dev/null'")
            flag_promote = True
            print("[Резервная база данных сейчас является основной].")
    if (Availability(ip_addr_m) and flag_master_drop):
        print((f"[{id}] Подключение к основной базе данных восстановлено"))
        Connect(ip_addr_m)
        try:
             os.system(f"ssh postgres@{ip_addr_m} 'rm -rf /var/lib/postgresql/14/main && mkdir /var/lib/postgresql/14/main && chmod go-rwx /var/lib/postgresql/14/main && pg_basebackup -P -X stream -c fast -h 192.168.200.101 -U postgres -D /var/lib/postgresql/14/main && sudo systemctl restart postgresql'")
             os.system(f"ssh postgres@{ip_addr_s} 'rm -rf /var/lib/postgresql/14/main && mkdir /var/lib/postgresql/14/main && chmod go-rwx /var/lib/postgresql/14/main && pg_basebackup -P -R -X stream -c fast -h 192.168.200.100 -U postgres -D /var/lib/postgresql/14/main && sudo systemctl restart postgresql'")
             flag_master_drop = False
             flag_promote = False
             print("Репликация прошла успешно")
        except (Exception, Error) as error:
            print(f"Ошибка репликации")
    id += 1
    time.sleep(2)


def main():
    ip_addr_m = '192.168.200.100'
    ip_addr_s = '192.168.200.101'

    Replication(ip_addr_m, ip_addr_s)

if __name__ == "__main__":
    main()

