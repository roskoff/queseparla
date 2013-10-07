from bs4 import BeautifulSoup
import requests
from pyquery import PyQuery as pq
from lxml import etree
import bleach
import re
import HTMLParser
import time
import hashlib
import MySQLdb



db = MySQLdb.connect(host="localhost", user="root", passwd="toor",db="queseparla", charset = "utf8", use_unicode = True)

def guardarBD(texto,hora):
	x = db.cursor()

	hash_texto=hashlib.md5(texto.encode('utf8')).hexdigest()
	fecha_agregado=time.strftime('%Y-%m-%d %H:%M')
	x.execute("""INSERT INTO agenda_diputados ( texto, hash_texto, fecha_agregado, hora) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE fecha_actualizado=%s""",(texto,hash_texto,fecha_agregado,hora,fecha_agregado))


#DIPUTADOS
url = requests.get("http://www.diputados.gov.py/ww2/?pagina=agenda-parlamentaria")
data = url.text

soup = BeautifulSoup(data)
tabla = soup.find_all('table' , {'class' : 'tex'})
data = tabla[1].prettify()
trs = BeautifulSoup(data)
tds = trs.find_all('td', {'class' : 'borderU'})

rowcount = 0
for fila in tds:
	rowcount += 1
	clean = bleach.clean(fila, tags=[], strip=True)
	
	#print clean
	#cadena = clean
	cadena = re.sub('\s+',' ',clean.strip())
	#Fecha
	if (rowcount == 1):
		fecha = cadena

	#Presidencia
	if(rowcount == 2):
		horas_presidencia = re.findall(r"[0-9][0-9]\:[0-9][0-9] Hs\. ",cadena)

		lista_presidencia = []
		
		for x in range(len(horas_presidencia)):
			
			inicio = cadena.find(horas_presidencia[x]) + len(horas_presidencia[x])
			
			if x < len(horas_presidencia)-1: 
				fin = cadena.find(horas_presidencia[x+1])
				lista_presidencia += [cadena[inicio:fin]]
			else:
				lista_presidencia += [cadena[inicio:]]
			
		presidencia = []
		print "--------->>"
		print len(lista_presidencia)
		print lista_presidencia
		for p in lista_presidencia:
			presidencia += [re.sub(r"[0-9][0-9]\:[0-9][0-9] Hs\. ",'',p)]
		
	
	#Comisiones
	if(rowcount == 3):

		horas_comision = re.findall(r"[0-9][0-9]\:[0-9][0-9] Hs\. ",cadena)
		
		lista_comision = []
		
		for x in range(len(horas_comision)):
			
			inicio = cadena.find(horas_comision[x]) + len(horas_comision[x])
			
			if x < len(horas_comision)-1: 
				fin = cadena.find(horas_comision[x+1])
				lista_comision += [cadena[inicio:fin]]
			else:
				lista_comision += [cadena[inicio:]]
		comisiones = []
		for c in lista_comision:
			comisiones += [re.sub(r"[0-9][0-9]\:[0-9][0-9] Hs\. ",'',c)]
		


print "FECHA : " + fecha

print "PRESIDENCIA : "
for i in range(len(horas_presidencia)):
	print "HORA : " + horas_presidencia[i]
	print "TITULO : " + presidencia[i]
	guardarBD(presidencia[i],horas_presidencia[i].replace("Hs. ",""))


print "COMISIONES : " 
for i in range(len(horas_comision)):
	print "HORA : " + horas_comision[i]
	print "TITULO : " + comisiones[i]
	guardarBD(comisiones[i],horas_comision[i].replace("Hs. ",""))



