# DEPLOYMENT NOTES

These are specific to the deployment on a CentOS 6.5 VPS at http://discograph.mbrsi.org.

Disco/graph was designed for Python 3.4+ and (currently) makes use of Sqlite3 with FTS4 support compiled in.

These notes outline some of the build commands used during the process of determining the correct deployment in the above-described environment.

## Python

Python 3.4, installed manually in /usr/local/.

Linked against manually installed Sqlite3.

    LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib ./configure \
        LDFLAGS="-L/usr/local/sqlite-3.8.11/lib -Wl,-rpath /usr/local/lib" \
        CPPFLAGS="-I/usr/local/sqlite-3.8.11/include" \
        --prefix=/usr/local \
        --enable-shared

    LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib make altinstall

## Sqlite

Sqlite 3.8.11, installed manually in /usr/local/sqlite-3.8.11/.

Compiled with FTS3 and FTS4.

## apsw

APSW obviates the need for compiling Sqlite 3.8.11 into Python.

    python setup.py fetch --all build --enable-all-extensions install test

## supervisord

It's crucial to set LD_LIBRARY_PATH in the supervisord configuration:

    [program:discograph]
    directory = /home/mbrsi/subdomains/discograph
    command = /home/mbrsi/subdomains/discograph/bin/gunicorn --conf gunicorn.conf discograph:app
    user = mbrsi
    autostart = true
    autorestart = false
    redirect_stderr = true
    stdout_logfile = /tmp/discograph.log
    environment=HOME=/home/mbrsi,LD_LIBRARY_PATH=/usr/local/sqlite-3.8.11/lib:/usr/local/lib,LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib
