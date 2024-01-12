#!/bin/bash

bench new-site \
	--db-host=test.ebc.zhushigroup.cn --db-port=3306  \
	--db-name=ebc_test \
	--admin-password=Bi12345678!  \
	--db-root-password=Bi12345678! \
	ebc.zhushigroup.cn
bench --site ebc.zhushigroup.cn install-app  erpnext erpnext_china erpnext_china_mdm
echo Y | bench set-nginx-port ebc.zhushigroup.cn 443
bench set-mariadb-host test.ebc.zhushigroup.cn
bench --site ebc.zhushigroup.cn migrate
bench build --app erpnext_china --force
bench set-config -g maintenance_mode 0
echo Bi12345678! | sudo -S service nginx restart
sudo service ssh restart
/home/frappe/frappe-bench/env/bin/gunicorn \
  --chdir=/home/frappe/frappe-bench/sites \
  --bind=0.0.0.0:8000 \
  --threads=10 \
  --workers=3 \
  --worker-class=gthread \
  --timeout=120 \
  --preload \
  frappe.app:application

