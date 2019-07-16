apt-get update && apt-get install -y libaio1
wget https://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.56-linux-glibc2.5-x86_64.tar.gz
groupadd mysql
useradd -g mysql mysql
tar -xvf mysql-5.5.56-linux-glibc2.5-x86_64.tar.gz
mv mysql-5.5.56-linux-glibc2.5-x86_64 /usr/local/
cd /usr/local
mv mysql-5.5.56-linux-glibc2.5-x86_64 mysql
cd mysql
chown -R mysql:mysql *
scripts/mysql_install_db --user=mysql
chown -R root .
chown -R mysql data
cp support-files/my-medium.cnf /etc/my.cnf
bin/mysqld_safe --user=mysql &
cp support-files/mysql.server /etc/init.d/mysql.server
bin/mysqladmin -u root password 'root'
ln -s /usr/local/mysql/bin/mysql /usr/local/bin/mysql