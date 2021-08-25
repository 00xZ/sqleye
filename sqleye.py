#python3.9
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
    try:
        req = requests.get(url, timeout=6)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.select('a[href*=".php?id="]'):
            okay = (link["href"])
            serv = (url + "/" + okay + "'")
            reeqee = requests.get(serv, timeout=6)
            souper = BeautifulSoup(reeqee.text, "html.parser")
            if souper(text=lambda t: "SQL syntax" in t):
                print(serv + " :  [!] VULN [!]")
                fo = open("vulnSQLi.txt", "a+")
                fo.write(serv + "\n")
                fo.close
            else:
                print("[x] found sqli but no pass [x] : " + serv )
			    pass
    except:
        pass
        
			

def main():
	presentation()
	count = 0
	if len(sys.argv) < 3:
		print("use -f for file")
		ip = str(sys.argv[1])
		gethref(ip)
	else:
		input_file = open(sys.argv[2])
		#threads = (sys.argv[3])
		for i in input_file.readlines():
			ip = i.strip("\n")
			gethref(ip)

main()
