# rvscore

RVGL self-hosted scoreboard

---

rvscore is composed of two components:

- a Django-based server to display and synchronize times across different machines
- the `rvsync.py` script that reads and writes to RVGL time files

Calling `rvsync.py` from inside your `rvgl` folder will read your local time files and push them to the Django server and then pull the best times for each track/mode/category combination and write them to your local `.times` file.

You can also see the times online by browsing to the webserver url. The keybindings the same as in RVGL.

Configuration is done by creating a file name `rvsync.ini` in `rvgl/profiles/`:

```ini
[sync]
url="http://localhost/"
count=X
```

Change the URL to your server's URL, and count to the number of best times you want to download from the server *per track*.