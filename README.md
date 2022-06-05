Работа выполнена студентами группы РИ-571227:

Иванов Р.С.
Токарева В.М.
Худякова Е.А.

Был реализован следующий функционал:
- Сконфигурирован master сервер;
- Сконфигурирован stanby сервер;
- Настроена репликация кластера БД;
- Сконфигурирован Арбитр;
- Написана программа-агент Replication.py на языке python, которая мониторит статус подключенных серверов и поднимает slave сервер до master при проблеме с подключением master-сервера;
- Программа-агент запущена на всех серверах;
- Работоспобность схемы доказана и зафиксирована на приложенной видеозаписи.

Подготовительный этап:
- Созданы 3 ВМ - Master-сервер: 192.168.200.100,  Standby-сервер: 192.168.200.101, Арбитр: 192.168.200.102;
- Сгенерированы и распространены RSA ключи для пользователей postgres для всех виртуальных машин для возможности безпарольного ssh подключения;\
- На Master и Standby настроен postgres и запущена репликация;


Настройка конфигурации Master-сервера:
  Файл postgresql.conf:
  
      listen_addresses = '*'
      wal_level = hot_standby
      archive_mode = on
      archive_command = 'cd .'
      max_wal_senders = 16
      hot_standby = on
      
  Файл pg_hba.conf:
    
      host    replication    postgres    192.168.200.101/24    trust




Настройка конфигурации Standby-сервера:
  Файл postgresql.conf:
  
      listen_addresses = '*'
      wal_level = hot_standby
      archive_mode = on
      archive_command = 'cd .'
      max_wal_senders = 16
      hot_standby = on
      
      
  Файл pg_hba.conf:
    
      host    replication    postgres    192.168.200.100/24    trust
      
Выполнена команда для начала репликации:
pg_basebackup -P -R -X stream -c fast -h 192.168.200.100 P -U postgres -D ./main
