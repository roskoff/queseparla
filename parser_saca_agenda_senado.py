#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Este archivo intentan leer el json almacenado en la base de datos, 
# y re-interpletandolo intenta obtener los datos basicos para generar 
# una agenda que pueda ser utilizada.

import requests
import json
import time
import re

url = requests.get("http://tedic.org/queseparla/preagenda/senado/json/")
data = url.content
print "STATUS: "+str(url.status_code)

js=json.loads(data)
for agendas in js:
	if "AVANCE INFORMATIVO" in agendas["texto"]:
		print "==================> ID "+agendas["id"]
		texto= agendas["texto"][agendas["texto"].find("AVANCE INFORMATIVO"):agendas["texto"].find("-----")]
		print texto
		match = re.search(r'\d{1,2}/\d{2}/\d{4}',agendas["texto"])
		print "===> FECHA PUBLICACION "+match.group(0)
		match=re.search('\d{1,2}/(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SETIEMBRE|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)/\d{4}',texto)
		print "===> CUANDO SE TRATARA "+match.group(0)
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		

