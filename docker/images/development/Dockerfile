FROM digitwise/erpnext_china
ENV WORK_DIR=/home/frappe/frappe-bench
RUN bench get-app --branch develop https://github.com/saoxia/erpnext_china_mdm

COPY patches/data/industry_type.txt /home/frappe/frappe-bench/apps/erpnext/erpnext/setup/setup_wizard/data/industry_type.txt
COPY patches/data/lead_source.txt /home/frappe/frappe-bench/apps/erpnext/erpnext/setup/setup_wizard/data/lead_source.txt

CMD ["/bin/bash"]