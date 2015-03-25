# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* jobfoldersizes is a python tool that utilizes the scandir python module to calculate the folder sizes of a desired root directory.
* Version: 1.0

## How do I get set up? ##

### Dependencies ###
This relies on [scandir](https://pypi.python.org/pypi/scandir). Scandir you can install via pip, or download as tar directly from the previous link. It is now included in the Python 3.5 trunk(currently in Alpha).

### Set Up ###
1. Check your system that you have at least Python 2.7.6. This is the minimum version that scandir has been tested on.
2. Install scandir either thru pip, manually, or use Python 3.5.x
3. Once installed run the python script `jobsizes.py --root=/path/to/root` and other flags

### Flags ###
* --root=/path/to/sort  This is required. The path must be accessible and you must have permissions. That may require you run as super user or equivalent.
*--sort=[size|name]  How the results should be sorted. The default is size. name sort does a case insensitive sort.
*--filter=regex  This allows you to filter the top dirs to be calculated under your root.
*--output=[terminal]|email  This sets the output format. The default format is terminal which is present a tabbed tabular format. Email is present simple list for easier rendering across a variety of email platforms.
*-d  Will enable debug mode. This will tell you if scandir sees its fast c libraries. It will also output as it calculates each directory before final sorted output. This is helpful is you're not sure if it is rendering or where it is taking long. There is currently no timing.

### Who do I talk to? ###

* Talk to [Anthony Scudese](mail-to:anthony@robottalk.tv)