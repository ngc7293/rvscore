# rvscore

RVGL self-hosted scoreboard

---

rvscore is composed of two components:

- a Django-based server to display and synchronize times across different machines
- the `rvsync.py` script that reads and writes to RVGL time files

Calling `rvsync.py` will read your local time files and push them to the Django server and then pull the best times for each track/mode/category combination and write them to your local `.times` file.

You can also see the times online by browsing to the webserver url and visiting the page `/<track>/<mode>/<rating>/`. Use rating=Global to see best times for all cars.

Make sure to edit the `rvsync.py` constants `ROOT_FOLDER` and `URL` to mirror the correct values for your deployement.