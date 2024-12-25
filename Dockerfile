FROM frappe/erpnext:v15.46.1

USER root
RUN apt update && \
    apt install libreoffice-writer-nogui -y &&\
    rm -rf /var/lib/apt/lists/* && \
    rm -fr /etc/nginx/sites-enabled/default

USER frappe

RUN cd /home/frappe/frappe-bench && \
    bench remove-app erpnext

ARG CACHEBUST=1

RUN echo "$CACHEBUST" && \
    cd /home/frappe/frappe-bench && \
    bench get-app --resolve-deps https://github.com/abrefael/t_money.git
	
WORKDIR /home/frappe/frappe-bench
	
VOLUME [ \
  "/home/frappe/frappe-bench/sites", \
  "/home/frappe/frappe-bench/sites/assets", \
  "/home/frappe/frappe-bench/logs" \
]

CMD [ \
  "/home/frappe/frappe-bench/env/bin/gunicorn", \
  "--chdir=/home/frappe/frappe-bench/sites", \
  "--bind=0.0.0.0:8000", \
  "--threads=4", \
  "--workers=2", \
  "--worker-class=gthread", \
  "--worker-tmp-dir=/dev/shm", \
  "--timeout=120", \
  "--preload", \
  "frappe.app:application" \
]
