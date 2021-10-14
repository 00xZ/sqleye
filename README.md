# sqleye
<h1>SqlEYE a deep web scanner that checks for sql injections</h1>


use: 
* python3 sqleye.py 1.3.3.7
* python3 sqleye.py -f servers.txt
* Proxy mode with -p
* python3 sqleye.py 1.3.3.7 -p 6.9.4.20
* python3 sqleye.py -f servers.txt -p 4.20.6.9


requires :
* requests, bs4, lxml, sys, fnmatch, re

This will scan a site and all links in that site, there is a blacklist which blacklists out site like google,facebook,youtube, and other big sites to prevent from a rabit hole scanning those site. 
It works by getting all the href's and checking for the "id=" string then pushing a sqli input and checking for a error. it appends every site to a temp list to prevent inf. looping of scanning the same site

! TODO:
* scan for js files and check publicly known js programs for CVE's
