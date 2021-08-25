import requests 
from bs4 import BeautifulSoup
from lxml import html, etree
import sys
import re
#use ./sqleye.py website (or ip)
#will add multi threading and reading from a list of servers
def presentation():

    print("[+] # #############################################")
    print("[+] #                                             #")
    print("[+] #          'Hurt,,, feelings,,,'  -Mac Mille  #")
    print("[+] #                                             #")
    print("[+] #      ~00xZ-                                 #")
    print("[+] #                                             #")
    print("[+] # #############################################")

def gethref(ip):
    url = ("http://" + ip)
    print("[x] ~ SCAN: " + url + " ~ [x]")
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    for link in soup.select('a[href*=".php?id="]'):
        okay = (link["href"])
        serv = (url + "/" + okay + "'")
        reeqee = requests.get(serv)
        souper = BeautifulSoup(reeqee.text, "html.parser")
        if souper(text=lambda t: "SQL syntax" in t):
            print(serv + " :  [!] VULN [!]")
            fo = open("vulnSQLi.txt", "a+")
            fo.write(serv + "\n")
            fo.close
        else:
            print("[x] found sqli but no pass [x] : " + serv )
			
			
def main():
	presentation()
	ip = str(sys.argv[1])
	print("sent")
	gethref(ip)
main()
