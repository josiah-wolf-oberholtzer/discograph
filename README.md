# discograph

[Discograph](http://discograph.mbrsi.org/) - Social Graphing for the Discogs Database

#### What?

Disco/graph is an interactive visualization of the relationships between musicians, bands and labels. :notes:

All of Disco/graph's data is derived from the [Discogs](http://www.discogs.com) discography database: nearly 4 million artists, 1 million labels, and 7 million releases creating a network of nearly 70 million different relationships.

What do all of these symbols mean?

* Small circles represent artists.
* Large circles represent bands.
* Solid lines show band membership.
* Dotted lines show pseudonyms.

The graph only shows 100 entities at a time, so double-click on any circle containing a plus-sign to reveal more connections.

![The "Morris Day" Network](/discograph.png)

# DEPLOYMENT NOTES :construction:

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
