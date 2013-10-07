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

url = requests.get("http://tedic.org/queseparla/preagenda/senado/json/")
data = url.content
print "STATUS: "+str(url.status_code)
meses=[("ENERO","01"),("FEBRERO","02"),("MARZO","03"),("ABRIL","04"),("MAYO","04"),("JUNIO","06"),("JULIO","07"),("AGOSTO","08"),("SETIEMBRE","09"),("SEPTIEMBRE","09"),("OCTUBRE","10"),("NOVIEMBRE","11"),("DICIEMBRE","12")]

js=json.loads(data)
for agendas in js:
	if "AVANCE INFORMATIVO" in agendas["texto"]:
		print "==================> ID "+agendas["id"]
		texto= agendas["texto"][agendas["texto"].find("AVANCE INFORMATIVO"):agendas["texto"].find("-----")]
		print texto
		match = re.search(r'\d{1,2}/\d{2}/\d{4}',agendas["texto"])
		if match:
			fecha_publicacion=match.group(0)
			fecha_publicacion=datetime.datetime.strptime(fecha_publicacion,"%d/%m/%Y")
			fecha_publicacion=fecha_publicacion.strftime('%Y-%m-%d')
			print "===> FECHA PUBLICACION "+fecha_publicacion
		else:
			print "ERROR: NO SE PUDO ENCONTRAR FECHA CUANDO SE PUBLICO"

		match=re.search('\d{1,2}/(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SETIEMBRE|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)/\d{4}',texto)
		if match:
			fecha_tratara=match.group(0)
			for k, v in meses:
				fecha_tratara = fecha_tratara.replace(k, v)
			fecha_tratara=datetime.datetime.strptime(fecha_tratara,"%d/%m/%Y")
			fecha_tratara=fecha_tratara.strftime('%Y-%m-%d')
			print "===> CUANDO SE TRATARA "+fecha_tratara
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		else:
			print "ERROR: NO SE PUDO ENCONTRAR FECHA CUANDO SE TRATARA"

