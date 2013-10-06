#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://www.senado.gov.py/ordendeldia
#http://www.senado.gov.py/agendas

# PARSEA LA AGENDA DEL SENADO Y LO GUARDA EN LA DB ONLINE.
# OBTIENE TEXTO CRUDO QUE DEBE SER TRATADO PARA GENERAR LA AGENDA

from bs4 import BeautifulSoup
import requests
import time
import hashlib
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="toor",db="queseparla", charset = "utf8", use_unicode = True)


url = requests.get("http://www.senado.gov.py/agendas")
data = url.content

soup = BeautifulSoup(data,"html5lib")
# $('table[height="100%"]')
latabla = soup.find_all('table', attrs = {'height':'100%'})

x = db.cursor()

for h in latabla:
	print "--------------------------"
	soup_href= BeautifulSoup(h.prettify(),"html5lib")
	links=soup_href.find_all('a')
	for link in links:
		href=str("http://www.senado.gov.py/"+link.get("href"))
		if (href.find('\:')==-1):
			print href
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			url_agenda=requests.get(href)
			print "==> STATUS: "+str(url_agenda.status_code)
			if(url_agenda.status_code==200):
				soup_agenda=BeautifulSoup(url_agenda.content,"html5lib")
				texto_agenda=soup_agenda.find_all('td', {'height':'100%','align':'left'})
				soup_agenda=BeautifulSoup(texto_agenda[0].prettify())
				texto_agenda=soup_agenda('td',{'align':'left'})
				texto_agenda= (soup_agenda.get_text()).strip(' \n\t').replace('  ','').replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")
				print texto_agenda
				hash_url=hashlib.md5(href).hexdigest()
				hash_texto=hashlib.md5(texto_agenda.encode('utf8')).hexdigest()
				fecha_agregado=time.strftime('%Y-%m-%d %H:%M')
				x.execute("""INSERT INTO preagenda_senado ( hash_url, url, texto, hash_texto, fecha_agregado) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE fecha_actualizado=%s""",(hash_url,href,texto_agenda,hash_texto,fecha_agregado,fecha_agregado))

				print "/////////////////////////////////////////////////////////////////////////////////"
				time.sleep(1)
