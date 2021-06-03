
SET dbhost=127.0.0.1 
SET dbuser=root
SET dbpasswd=xzkdbtest

cd E:\Program Files\mysql\bin

::执行SQL脚本 alter user 'root'@'localhost' identified by 'xzkdbtest';

mysql -h%dbhost% -u%dbuser% -p%dbpasswd% 

ECHO OK!
PAUSE