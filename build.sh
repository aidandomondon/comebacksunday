#!/bin/bash

export MYSQL_HOME=/usr/local/mysql-9.3.0-macos15-arm64/include;
export MYSQLCLIENT_CFLAGS="-I/usr/local/mysql-9.3.0-macos15-arm64/include";
export MYSQLCLIENT_LDFLAGS="-L/usr/local/mysql-9.3.0-macos15-arm64/lib -lmysqlclient";

source venv/bin/activate && pip3 install -r requirements.txt;