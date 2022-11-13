# Lyrics Data Collector

## Overview

- A simple data collector cli api for collecting lyrics of various artists.

 
## How to Run Locally
The application was able to run on Ubuntu 20.04 machines (one with 2GB and another with 8GB RAM) with the default settings by following the instructions below. Python version 3.9 was used. Install the packages provided in requirements.txt file using `pip install -r requirements.txt`
The command line application can be run by running python script `LyricsDataCollector/cli_app.py`.
An example for collecting artists lyrics from lyrics.com and storing it in seperate csv file for each artist in relative directory `data` is as follows:
```
  python cli_app.py --artists Linkin-Park Imagine-Dragons
```
