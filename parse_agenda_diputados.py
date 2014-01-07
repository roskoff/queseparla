#!/usr/bin/env python
# -*- coding: utf-8 -*-

	#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Este archivo intentan leer el json almacenado en la base de datos, 
# y re-interpletandolo intenta obtener los datos basicos para generar 
# una agenda que pueda ser utilizada.

from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
import re
import hashlib
import MySQLdb


db = MySQLdb.connect(host="mysql.tedic.org", user="root", passwd="toor",db="queseparla", charset = "utf8", use_unicode = True)
x = db.cursor()

url = requests.get("http://tedic.org/queseparla/preagenda/diputados/json/")
data = url.content
print "STATUS: "+str(url.status_code)

js=json.loads(data)
for agendas in js:
	html= agendas['html']
	fecha=re.search('(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d',html)
	if fecha:
		fecha_agenda=fecha.group(0)
		print "FECHA ENCONTRADA: "+str(fecha_agenda)
		soup = BeautifulSoup(html,"html5lib")
		#losp = soup.find_all('p', attrs = {'style':'text-align: justify;'})
		losp = soup.find_all('p')
		for p in losp:
			lap=p.get_text()
			horas_presidencia = re.search(r"([0-9]{1,2}\:[0-9]{1,2}) hs\.",lap,re.IGNORECASE)
			print lap
			if horas_presidencia:
				horas_presidencia=horas_presidencia.group(0)
				print "HORAS PRESIDENCIA: "+horas_presidencia

				if horas_presidencia.lower().find("hs"):
					texto_agenda=(lap).strip(' \n\t').replace('  ','').replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n").replace(horas_presidencia,'')
					horas_presidencia=horas_presidencia[0:horas_presidencia.lower().find("hs")].strip()
					fecha_evento=datetime.datetime.strptime(str(fecha_agenda+" "+horas_presidencia),"%d/%m/%Y %H:%M")
					print "FECHA EVENTO: "+str(fecha_evento)
					print "TEXTO: "+texto_agenda
					id_preagenda=agendas['id']
					texto=texto_agenda.strip()
					hash_texto=hashlib.md5(texto.encode('utf8')).hexdigest()
					fecha_agregado=time.strftime('%Y-%m-%d %H:%M')
					fecha_evento=fecha_evento
					fecha_actualizado=time.strftime('%Y-%m-%d %H:%M')

					x.execute("""INSERT INTO agenda_diputados (id_preagenda,texto,hash_texto,fecha_agregado,fecha_evento) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE fecha_actualizado=%s""",(id_preagenda,texto,hash_texto,fecha_agregado,fecha_evento,fecha_actualizado))
				else:
					print "NO ENCONTRE LA HORA GILUN"
			else:
				print "NO HAY HORA NDEE"

	else:
		print "Y LA FECHA? NO HAY :("

	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"



