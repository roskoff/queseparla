#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Este archivo intentan leer el json almacenado en la base de datos, 
# y re-interpletandolo intenta obtener los datos basicos para generar 
# una agenda que pueda ser utilizada.

import requests
import json
import time
import datetime
import re
import hashlib
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="toor",db="queseparla", charset = "utf8", use_unicode = True)
x = db.cursor()

url = requests.get("http://tedic.org/queseparla/preagenda/senado/json/")
data = url.content
print "STATUS: "+str(url.status_code)
meses=[("ENERO","01"),("FEBRERO","02"),("MARZO","03"),("ABRIL","04"),("MAYO","04"),("JUNIO","06"),("JULIO","07"),("AGOSTO","08"),("SETIEMBRE","09"),("SEPTIEMBRE","09"),("OCTUBRE","10"),("NOVIEMBRE","11"),("DICIEMBRE","12")]

js=json.loads(data)
for agendas in js:
	if "AVANCE INFORMATIVO" in agendas["texto"]: # BUSCAMOS TODOS LOS TEXTOS QUE CONTENGAN AVANCES INFORMATIVOS
		print "==================> ID "+agendas["id"]
		texto= agendas["texto"][agendas["texto"].find("AVANCE INFORMATIVO"):agendas["texto"].find("-----")] # LIMPIAMOS EL TEXTO
		texto=texto.replace("AVANCE INFORMATIVO","").replace("-----","") # LIMPIAMOS UN POCO MAS
		match=re.search('\d{1,2}/(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SETIEMBRE|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)/\d{4}',texto) # BUSCAMOS LA FECHA EN QUE OCURRIRA EL EVENTO
		if match:
			fecha_tratara=match.group(0)
			for k, v in meses: 
				fecha_tratara = fecha_tratara.replace(k, v) # REEMPLAZAMOS LOS NOMBRES DE LOS MESES POR SU VARIANTE NUMERICA
			fecha_tratara=datetime.datetime.strptime(fecha_tratara,"%d/%m/%Y") # CONTERTIMOS LA FECHA DE TEXTO A DATE
			fecha_tratara=fecha_tratara.strftime('%Y-%m-%d')
			#print "===> CUANDO SE TRATARA "+fecha_tratara
			
		else:
			print "ERROR: NO SE PUDO ENCONTRAR FECHA CUANDO SE TRATARA"

		match = re.search(r'\d{1,2}/\d{2}/\d{4}',agendas["texto"]) # BUSCO LA FECHA DE PUBLICACION DENTRO DEL TEXTO
		if match:
			fecha_publicacion=match.group(0)
			fecha_publicacion=datetime.datetime.strptime(fecha_publicacion,"%d/%m/%Y")
			fecha_publicacion=fecha_publicacion.strftime('%Y-%m-%d')
			print "===> FECHA PUBLICACION "+fecha_publicacion
		else:
			print "ERROR: NO SE PUDO ENCONTRAR FECHA CUANDO SE PUBLICO"

		txt_agenda=''
		for line in texto.split("\n"): # NAVEGAMOS EL TEXTO LINEA POR LINEA
			hora_evento=''
			match_tratara=re.search('\d{1,2}/(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SETIEMBRE|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)/\d{4}',line) # BUSCAMOS UNA FECHA
			if not match_tratara:
				txt_agenda=txt_agenda+line+"\n" # VAMOS CARGANDO EL TEXTO DE LA AGENDA
				hora=re.search(r'(?:\d{1,2}[:,.]\d{1,2})',txt_agenda) # BUSCAMOS LA HORA EN QUE SE LLEVARA A CABO
				if hora:
					txt_agenda=txt_agenda.replace(r'(?:\d{1,2}[:,.]\d{1,2})','').replace('hs.','').replace(':','').replace('  ','').replace("\t",'') # LIMPIAMOS EL TEXTO DE LA AGENDA
					if(hora_evento!=hora.group(0)): # SI ES UNA HORA NUEVA QUE NO LEI ANTERIORMENTE
						hora_evento=hora.group(0)
						hora_evento=hora_evento.replace('.',':') # FORMATEAMOS CORRECTAMENTE LA HORA
						print "===> CUANDO "+ fecha_tratara + " " + hora_evento
						print "===> TEXTO "+txt_agenda
						

						db_url=agendas["url"]
						db_hash_url=hashlib.md5(db_url).hexdigest()
						db_texto=txt_agenda
						db_hash_texto=hashlib.md5(db_texto.encode('utf8')).hexdigest()
						db_fecha_evento=fecha_tratara + " " + hora_evento
						db_fecha_agregado=time.strftime('%Y-%m-%d %H:%M')
						db_id_preagenda=agendas["id"]
						db_fecha_actualizacion=time.strftime('%Y-%m-%d %H:%M')
						db_fecha_publicacion=fecha_publicacion
						

						x.execute("""INSERT INTO agenda_senado (url,hash_url,texto,hash_texto,fecha_evento,fecha_publicacion,fecha_agregado,id_preagenda) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE fecha_actualizado=%s""",(db_url,db_hash_url,db_texto,db_hash_texto,db_fecha_evento,db_fecha_publicacion,db_fecha_agregado,db_id_preagenda,db_fecha_actualizacion))

						txt_agenda='' # PONEMOS EL TEXTO DE LA AGENDA A CERO Y VOLVEMOS A EMPEZAR


		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"



