ARG FRAPPE_BRANCH=version-15
ARG FRAPPE_PATH=https://github.com/frappe/frappe

FROM frappe/build:${FRAPPE_BRANCH} AS builder

USER root
RUN apt update && \
    apt install libreoffice-writer-nogui -y &&\
    rm -rf /var/lib/apt/lists/*

USER frappe

RUN bench init \
    --frappe-branch=${FRAPPE_BRANCH} \
    --frappe-path=${FRAPPE_PATH} \
    --no-procfile \
    --no-backups \
    --skip-redis-config-generation \
    --verbose \
    /home/frappe/frappe-bench && \
    cd /home/frappe/frappe-bench && \
    echo "{}" > sites/common_site_config.json

FROM frappe/base:${FRAPPE_BRANCH} AS backend

USER frappe

COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

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
