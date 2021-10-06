# sqleye
<h1>SqlEYE a simple python3 sql injection spider with file output</h1>


use: 
* sqleye.py host.ip
* sqleye.py -f servers.txt


This will scan a site and all links in that site, there is a blacklist which blacklists out site like google,facebook,youtube, and other big sites to prevent from a rabit hole scanning those site. 
It works by getting all the href's and checking for the "id=" string then pushing a sqli input and checking for a error. it appends every site to a temp list to prevent inf. looping of scanning the same site
