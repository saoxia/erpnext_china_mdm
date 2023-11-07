FROM digitwise/erpnext_china
ENV WORK_DIR=/home/frappe/frappe-bench
RUN bench get-app --branch develop https://github.com/saoxia/erpnext_china_mdm

COPY patches/workspace/buying/buying.json ${WORK_DIR}/apps/erpnext/erpnext/buying/workspace/buying/buying.json
COPY patches/workspace/crm/crm.json ${WORK_DIR}/apps/erpnext/erpnext/crm/workspace/crm/crm.json
COPY patches/workspace/manufacturing/manufacturing.json ${WORK_DIR}/apps/erpnext/erpnext/manufacturing/workspace/manufacturing/manufacturing.json
COPY patches/workspace/selling/selling.json ${WORK_DIR}/apps/erpnext/erpnext/selling/workspace/selling/selling.json

COPY patches/data/industry_type.txt /home/frappe/frappe-bench/apps/erpnext/erpnext/setup/setup_wizard/data/industry_type.txt
COPY patches/data/lead_source.txt /home/frappe/frappe-bench/apps/erpnext/erpnext/setup/setup_wizard/data/lead_source.txt

RUN chmod -R 777 .

COPY frappe-bench.conf /etc/nginx/conf.d/frappe-bench.conf


CMD ["/bin/bash"]