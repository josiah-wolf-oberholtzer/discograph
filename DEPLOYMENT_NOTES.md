# DEPLOYMENT NOTES

## Python

Python 3.4, installed manually in /usr/local/.

Linked against manually installed Sqlite3.

    ```
    LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib ./configure \
        LDFLAGS="-L/usr/local/sqlite-3.8.11/lib -Wl,-rpath /usr/local/lib" \
        CPPFLAGS="-I/usr/local/sqlite-3.8.11/include" \
        --prefix=/usr/local \
        --enable-shared

    LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib make altinstall
    ```

## Sqlite

Sqlite 3.8.11, installed manually in /usr/local/sqlite-3.8.11/.

Compiled with FTS3 and FTS4.

## supervisord

It's crucial to set LD_LIBRARY_PATH in the supervisord configuration:

    ```
    [program:discograph]
    directory = /home/mbrsi/subdomains/discograph
    command = /home/mbrsi/subdomains/discograph/bin/gunicorn --conf gunicorn.conf discograph:app
    user = mbrsi
    autostart = true
    autorestart = false
    redirect_stderr = true
    stdout_logfile = /tmp/discograph.log
    environment=HOME=/home/mbrsi,LD_LIBRARY_PATH=/usr/local/sqlite-3.8.11/lib:/usr/local/lib,LD_RUN_PATH=/usr/local/sqlite-3.8.11/lib
    ```