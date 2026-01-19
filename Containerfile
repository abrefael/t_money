FROM debian:bookworm-slim AS bench

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    # For frappe framework
    git \
    mariadb-client \
    gettext-base \
    wget \
    ca-certificates \
    # for PDF
    libssl-dev \
    fonts-cantarell \
    xfonts-75dpi \
    xfonts-base \
    # weasyprint dependencies
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    # to work inside the container
    locales \
    build-essential \
    cron \
    curl \
    less \
    # Other
    libffi-dev \
    liblcms2-dev \
    libldap2-dev \
    libmariadb-dev \
    libsasl2-dev \
    libtiff5-dev \
    libwebp-dev \
    pkg-config \
    redis-tools \
    rlwrap \
    tk8.6-dev \
    ssh-client \
    # For pandas
    libbz2-dev \
    # For bench execute
    libsqlite3-dev \
    # For other dependencies
    zlib1g-dev \
    libreadline-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    liblzma-dev \
    file \
    nginx \
    jq \
    wait-for-it \
    # For MIME type detection
    media-types \
    shared-mime-info \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales

# Detect arch and install wkhtmltopdf
ARG WKHTMLTOPDF_VERSION=0.12.6.1-3
ARG WKHTMLTOPDF_DISTRO=bookworm
RUN if [ "$(uname -m)" = "aarch64" ]; then export ARCH=arm64; fi \
    && if [ "$(uname -m)" = "x86_64" ]; then export ARCH=amd64; fi \
    && downloaded_file=wkhtmltox_${WKHTMLTOPDF_VERSION}.${WKHTMLTOPDF_DISTRO}_${ARCH}.deb \
    && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/$WKHTMLTOPDF_VERSION/$downloaded_file \
    && dpkg -i $downloaded_file \
    && rm $downloaded_file

# Create new user with home directory, improve docker compatibility with UID/GID 1000,
# add user to sudo group, allow passwordless sudo, switch to that user
# and change directory to user home directory
RUN groupadd -g 1000 frappe \
    && useradd --no-log-init -r -m -u 1000 -g 1000 -G sudo frappe \
    && echo "frappe ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN sed -i '/user www-data/d' /etc/nginx/nginx.conf \
    && ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log \
    && touch /run/nginx.pid \
    && chown -R frappe:frappe /etc/nginx/conf.d \
    && chown -R frappe:frappe /etc/nginx/nginx.conf \
    && chown -R frappe:frappe /var/log/nginx \
    && chown -R frappe:frappe /var/lib/nginx \
    && chown -R frappe:frappe /run/nginx.pid \
    && chown -R frappe:frappe /etc/nginx/conf.d \
    && chown -R frappe:frappe /etc/nginx/nginx.conf \
    && chown -R frappe:frappe /var/log/nginx \
    && chown -R frappe:frappe /var/lib/nginx \
    && chown -R frappe:frappe /run/nginx.pid





RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash && \
    \. "$HOME/.nvm/nvm.sh" && \
    nvm install 24 && \
    npm install -g yarn && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    . "$HOME/.local/bin/env" && \
    uv python install 3.14 --default && \
    . "$HOME/.bashrc" && \
    uv tool install frappe-bench && \
    echo $(which bench)

RUN cp -r "$HOME/.local" /home/frappe/ && \
    chown -R frappe:frappe /home/frappe

COPY resources/nginx-template.conf /templates/nginx/frappe.conf.template
COPY resources/nginx-entrypoint.sh /usr/local/bin/nginx-entrypoint.sh


FROM bench AS builder
USER frappe
WORKDIR /home/frappe

ARG FRAPPE_BRANCH=version-16
ARG FRAPPE_PATH=https://github.com/frappe/frappe
RUN /home/frappe/.local/bin/bench init \
    --frappe-branch=${FRAPPE_BRANCH} \
    --frappe-path=${FRAPPE_PATH} \
    --no-procfile \
    --no-backups \
    --skip-redis-config-generation \
    --verbose \
    --python /home/frappe/python3.14 \
    /home/frappe/frappe-bench && \
    /home/frappe/.local/share/uv/tools/frappe-bench/bin/python -m ensurepip && \
    cd /home/frappe/frappe-bench && \
    echo "{}" > sites/common_site_config.json && \
    find apps -mindepth 1 -path "*/.git" | xargs rm -fr

FROM builder AS backend

USER frappe

RUN echo "echo \"Commands restricted in prodution container, Read FAQ before you proceed: https://frappe.io/ctr-faq\"" >> ~/.bashrc

COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench
#COPY --chown=frappe:frappe backups /home/frappe/frappe-bench/backups
USER root

RUN apt-get update && apt-get install --no-install-recommends file libreoffice-writer -y && \
    rm -rf /var/lib/apt/lists 


USER frappe
ARG CACHEBUST=1

RUN echo "$CACHEBUST" && \
    cd /home/frappe/frappe-bench && \
    bench get-app --resolve-deps --branch V1.16 https://github.com/abrefael/t_money.git

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
