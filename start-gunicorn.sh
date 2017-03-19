#!/bin/sh
# here is path to gunicorn run file
export PATH=PATH:/Library/Frameworks/Python.framework/Versions/3.4/bin/
# environment - development, staging and production
export APP_ENV=production
mkdir .log 2> /dev/null
export DEBUG=0
#gunicorn -w3 -b 10.10.0.14:443 --certfile=swap3g.crt --keyfile=swap3g.key app:app --access-logfile .log/access.log --error-logfile .log/general.log
/usr/local/bin/gunicorn -w3 -b 10.10.0.14:81 app:app --access-logfile glog/access.log --error-logfile glog/general.log
