#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# DEFINIMOS VARIABLES GENERALES
delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
path='/var/www/parlamento_abierto.tedic.org/'

# DEFINIMOS CUALES SON LAS COMISIONES EXISTENTES PARA CADA CAMARA

#COMISIONES CON ACENTOS
#comisiones_diputados=['Asuntos Constitucionales','Comision Especial','Asuntos Economicos y Financieros','Legislacion y Codificacion','Relaciones Exteriores','Justicia, Trabajo y Prevision Social','Derechos Humanos','Educacion, Cultura y Culto','Obras, Servicios Publicos y Comunicaciones','Prensa y Comunicacion Social','Agricultura y Ganaderia','Defensa Nacional, Seguridad y Orden Interno','Industria, Comercio y Turismo','Salud Publica','Asuntos Municipales y Departamentales','Desarrollo Social, Poblacion y Vivienda','Presupuesto','Cuentas y Control de Ejecucion Presupuestaria','Peticiones, Poderes, Reglamento y Redaccion','Lucha contra el Narcotrafico','Ciencia y Tecnologia','Energia, Minas e Hidrocarburos','Ecologia, Recursos Naturales y Medio Ambiente','Bienestar Rural','Equidad Social y Genero','Deportes','Pueblos Indigenas','Entes Binacionales']
#comisiones_senadores=['Asuntos Constitucionales, Defensa Nacional y Fuerza Publica','Legislacion, Codificacion, Justicia y Trabajo','Hacienda y Presupuesto','Relaciones Exteriores y Asuntos Internacionales','Peticiones, Poderes y Reglamentos','Cultura, Educacion, Culto y Deportes','Derechos Humanos','Economia, Cooperativismo, Desarrollo e Integracion Economica Latinoamericana','Reforma Agraria y Bienestar Rural','Salud Publica y Seguridad Social','Asuntos Departamentales, Municipales, Distritales y Regionales','Obras Publicas y Comunicaciones','Energia, Recursos Naturales, Poblacion, Ambiente, Produccion y Desarrollo Sostenible','Equidad y Genero','Estilo','Cuentas y Control de la Adminstracion Financiera del Estado','Industria, Comercio y Turismo','Prevencion y Lucha contra el Narcotrafico y Delitos Conexos','Desarrollo Social']

#COMISIONES SIN ACENTO
comisiones_diputados=['Asuntos Constitucionales','Comision Especial','Asuntos Economicos y Financieros','Legislacion y Codificacion','Relaciones Exteriores','Justicia, Trabajo y Prevision Social','Derechos Humanos','Educacion, Cultura y Culto','Obras, Servicios Publicos y Comunicaciones','Prensa y Comunicacion Social','Agricultura y Ganaderia','Defensa Nacional, Seguridad y Orden Interno','Industria, Comercio y Turismo','Salud Publica','Asuntos Municipales y Departamentales','Desarrollo Social, Poblacion y Vivienda','Presupuesto','Cuentas y Control de Ejecucion Presupuestaria','Peticiones, Poderes, Reglamento y Redaccion','Lucha contra el Narcotrafico','Ciencia y Tecnologia','Energia, Minas e Hidrocarburos','Ecologia, Recursos Naturales y Medio Ambiente','Bienestar Rural','Equidad Social y Genero','Deportes','Pueblos Indigenas','Entes Binacionales']
comisiones_senadores=['Asuntos Constitucionales, Defensa Nacional y Fuerza Publica','Legislacion, Codificacion, Justicia y Trabajo','Hacienda y Presupuesto','Relaciones Exteriores y Asuntos Internacionales','Peticiones, Poderes y Reglamentos','Cultura, Educacion, Culto y Deportes','Derechos Humanos','Economia, Cooperativismo, Desarrollo e Integracion Economica Latinoamericana','Reforma Agraria y Bienestar Rural','Salud Publica y Seguridad Social','Asuntos Departamentales, Municipales, Distritales y Regionales','Obras Publicas y Comunicaciones','Energia, Recursos Naturales, Poblacion, Ambiente, Produccion y Desarrollo Sostenible','Equidad y Genero','Estilo','Cuentas y Control de la Adminstracion Financiera del Estado','Industria, Comercio y Turismo','Prevencion y Lucha contra el Narcotrafico y Delitos Conexos','Desarrollo Social']


# REALIZAMOS LA COPIA DE TODOS LOS DOCUMENTOS A UNA CARPETA TEMPORAL DE TRABAJO
#os.system('find /var/www/tesa-sil.tedic.org/tesa-sil.tedic.org/documentos/ -name "*.txt"  -exec cp {} /var/www/parlamento_abierto.tedic.org/txts/ \;')

print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ DIPUTADOS +++++++++++++++ "
for indice,comision in enumerate(comisiones_diputados):
	str_comision="D_"+comision.translate(None,delchars)
	print "====> TRABAJANDO "+str(indice+1)+" DE "+str(len(comisiones_diputados))
	print " BUSCANDO "+comision+" para guardar en "+path+"comisiones/"+str_comision
	os.system("mkdir "+path+"comisiones/"+str_comision)
	if comision.find("comision"):
		os.system('find '+path+'txts/ -name "*.txt" -exec grep -l  "'+comision+'" {} \; | sort | uniq | xargs -I {}  cp {} '+path+'comisiones/'+str_comision)
	else:
		os.system('find '+path+'txts/ -name "*.txt" -exec grep -l  "Comision de '+comision+'" {} \; | sort | uniq | xargs -I {}  cp {} '+path+'comisiones/'+str_comision)
	print " EXTRAYENDO PALABRAS CLAVES PARA "+comision
	os.system("find "+path+"comisiones/"+str_comision+" -name '*.txt' -exec cat {} \; | sed 's/\s/\\n/g' | sed -e 's/^[ \\t]*//' | sed 's/[^a-zA-Z0-9]//g' | sed 's/[0-9]*//g' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -b -g -r > "+path+"diccionarios/"+str_comision+".txt")
	print "-----------------------------------------------------------"



print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ SENADORES ++++++++++++++ "
for indice,comision in enumerate(comisiones_senadores):
	str_comision="S_"+comision.translate(None,delchars)
	print "====> TRABAJANDO "+str(indice+1)+" DE "+str(len(comisiones_senadores))
	print " BUSCANDO "+comision+" para guardar en "+path+"comisiones/"+str_comision
	os.system("mkdir "+path+"comisiones/"+str_comision)
	if comision.find("comision"):
		os.system('find '+path+'txts/ -name "*.txt" -exec grep -l  "'+comision+'" {} \; | sort | uniq | xargs -I {}  cp {} '+path+'comisiones/'+str_comision)
	else:
		os.system('find '+path+'txts/ -name "*.txt" -exec grep -l  "Comision de '+comision+'" {} \; | sort | uniq | xargs -I {}  cp {} '+path+'comisiones/'+str_comision)
	print " EXTRAYENDO PALABRAS CLAVES PARA "+comision
	os.system("find "+path+"comisiones/"+str_comision+" -name '*.txt' -exec cat {} \; | sed 's/\s/\\n/g' | sed -e 's/^[ \\t]*//' | sed 's/[^a-zA-Z0-9]//g' | sed 's/[0-9]*//g' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -b -g -r > "+path+"diccionarios/"+str_comision+".txt")
	print "-----------------------------------------------------------"
