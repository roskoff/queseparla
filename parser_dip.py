#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PARSEA LA AGENDA DE DIPUTADOS Y LO GUARDA EN LA DB ONLINE.
# OBTIENE TEXTO CRUDO QUE DEBE SER TRATADO PARA GENERAR LA AGENDA

from bs4 import BeautifulSoup
import requests
import time
import hashlib
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="toor",db="queseparla", charset = "utf8", use_unicode = True)

href="http://www.diputados.gov.py/ww2/?pagina=agenda-parlamentaria"
url = requests.get(href)
data = url.content

soup = BeautifulSoup(data,"html5lib")
# $('table[height="100%"]')
latabla = soup.find_all('table', attrs = {'class':'tex','align':'left'})

x = db.cursor()

for h in latabla:
	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	#texto_agenda= (h.get_text()).strip(' \n\t').replace('  ','').replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")
	texto_agenda=h.prettify()
	print texto_agenda
	hash_texto=hashlib.md5(texto_agenda.encode('utf8')).hexdigest()
	fecha_agregado=time.strftime('%Y-%m-%d %H:%M')
	x.execute("""INSERT INTO preagenda_diputados (url, html, hash_html, fecha_agregado) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE fecha_actualizado=%s""",(href,texto_agenda,hash_texto,fecha_agregado,fecha_agregado))
	print "/////////////////////////////////////////////////////////////////////////////////"
	time.sleep(1)
