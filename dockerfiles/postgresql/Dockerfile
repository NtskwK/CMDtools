FROM ubuntu:20.04
LABEL maintainer="kuron <natsukawa247@outlook.com>"
LABEL description="PostgreSQL 9.5.25 with PostGIS 2.3.2"
LABEL version="2.3.2"

ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_HOST_AUTH_METHOD trust
ENV POSTGRES_ALLOW_HOST all
ENV GOSU_VERSION 1.12
ENV PG_MAJOR 9.5
ENV PG_VERSION 9.5.25
ENV POSTGIS_VERSION 2.3.2
ENV PATH $PATH:/usr/local/pgsql/bin
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG en_US.utf8
ENV PGDATA /var/lib/postgresql/data

# RUN mkdir /docker-entrypoint-initdb.d
# COPY init.sql /docker-entrypoint-initdb.d/init-db.sql
# RUN chmod 644 /docker-entrypoint-initdb.d/init-db.sql

# COPY docker-entrypoint.sh /usr/local/bin/
# RUN ln -s /usr/local/bin/docker-entrypoint.sh / # backwards compat

# Setup system
RUN apt-get update; \
    set -eux; \
	groupadd -r postgres --gid=999; \
	useradd -r -g postgres --uid=999 --home-dir=/var/lib/postgresql --shell=/bin/bash postgres; \
	mkdir -p /var/lib/postgresql; \
	chown -R postgres:postgres /var/lib/postgresql; \
    # grab gosu for easy step-down from root
    # https://github.com/tianon/gosu/releases
	apt-get update; \
	apt-get install -y --no-install-recommends wget; \
	rm -rf /var/lib/apt/lists/*; \
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	# wget --no-check-certificate -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget --no-check-certificate -O /usr/local/bin/gosu "https://gh-proxy.natsuu.top/https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	chmod +x /usr/local/bin/gosu; \
	gosu --version; \
	gosu nobody true; \
    # make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
	apt-get update; \
	apt-get install -y --no-install-recommends locales; \
	localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    # Build Postgres from source
	mkdir /staging; \
	apt-get install -y --no-install-recommends python3 python3-dev libpython3-dev gcc build-essential libproj-dev libgeos-dev libxml2-dev zlib1g-dev libreadline-dev libpq-dev; \ 
	cd /staging; \
	# wget --no-check-certificate -q https://github.com/OpenDroneMap/WebODM/releases/download/v1.9.2/postgresql-$PG_VERSION.tar.gz; \
	wget --no-check-certificate -q https://mirrors.huaweicloud.com/postgresql/source/v$PG_VERSION/postgresql-$PG_VERSION.tar.gz; \
	cd /staging; \
	tar -zxf postgresql-$PG_VERSION.tar.gz; \
	cd postgresql-$PG_VERSION; \
	find / -name "Python.h";\
	./configure --with-python --includedir=/usr/include/python3.8/ ; \
	make -j$(nproc); \
	make install; \
	postgres --version; \
  sed -ri "s/#autovacuum_max_workers = 3/autovacuum_max_workers = 6/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_naptime = 1min/autovacuum_naptime = 15s/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_vacuum_threshold = 50/autovacuum_vacuum_threshold = 25/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_vacuum_scale_factor = 0.2/autovacuum_vacuum_scale_factor = 0.1/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_analyze_threshold = 50/autovacuum_analyze_threshold = 10/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_analyze_scale_factor = 0.1/autovacuum_analyze_scale_factor = 0.05/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_analyze_threshold = 50/autovacuum_analyze_threshold = 10/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_vacuum_cost_delay = 20ms/autovacuum_vacuum_cost_delay = 10ms/" /usr/local/pgsql/share/postgresql.conf.sample; \
  sed -ri "s/#autovacuum_vacuum_cost_limit = -1/autovacuum_vacuum_cost_limit = 1000/" /usr/local/pgsql/share/postgresql.conf.sample; \
	sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" /usr/local/pgsql/share/postgresql.conf.sample; \
	grep -F "listen_addresses = '*'" /usr/local/pgsql/share/postgresql.conf.sample; \
    mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod 2777 /var/run/postgresql; \
    # this 777 will be replaced by 700 at runtime (allows semi-arbitrary "--user" values)
    mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 777 "$PGDATA"; \
    # Build PostGIS from source
	apt-get update; \
	apt-get install -y --no-install-recommends libgdal-dev libjson-c-dev; \
	cd /staging; \
	# wget --no-check-certificate -q https://github.com/OpenDroneMap/WebODM/releases/download/v1.9.2/postgis-$POSTGIS_VERSION.tar.gz; \
	# wget --no-check-certificate -q https://gh-proxy.natsuu.top/https://github.com/OpenDroneMap/WebODM/releases/download/v1.9.2/postgis-$POSTGIS_VERSION.tar.gz; \
	wget --no-check-certificate -q https://mirrors.huaweicloud.com/postgresql/source/v$PG_MAJOR/postgresql-$PG_MAJOR.tar.gz; \
	# wget --no-check-certificate -q -O /usr/include/json-c/json_object_private.h https://gh-proxy.natsuu.top/https://raw.githubusercontent.com/json-c/json-c/json-c-0.13/json_object_private.h; \
	# tar -zxf postgis-$POSTGIS_VERSION.tar.gz; \
	tar -zxf postgis-$PG_MAJOR.tar.gz; \
	sed -i 's/#error.*/#define ACCEPT_USE_OF_DEPRECATED_PROJ_API_H 1/' /usr/include/proj_api.h; \
	cd /staging/postgis-$PG_MAJOR; \
	./configure --with-pgconfig=/usr/local/pgsql/bin/pg_config; \
	make; \
	make install; \
	sed -i '1d' /usr/local/pgsql/share/extension/postgis--$POSTGIS_VERSION.sql; \
	# apt-get remove -y gcc build-essential wget; \
	# apt-get autoremove -y; \
	# apt-get clean; \
	# rm -fr /var/lib/apt/lists/* /staging /usr/include;

VOLUME /var/lib/postgresql/data
ENTRYPOINT ["docker-entrypoint.sh"]
STOPSIGNAL SIGINT
EXPOSE 5432
CMD ["postgres"]