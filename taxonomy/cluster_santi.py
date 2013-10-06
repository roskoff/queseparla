from cluster import *
from collections import Counter
from os import listdir

def distance(dic1, dic2):
    totalmente_diferentes = True
    distancia = 0

    claves1 = dic1.keys()
    claves2 = dic2.keys()

    coincidencias = [k for k in claves1 if k in claves2]
    print "Cantidad de claves1: ", len(claves1)
    print "Cantidad de claves2: ", len(claves2)
    print "Longitud de coincidencias: ", len(coincidencias)
    if (len(coincidencias) > 0):
        totalmente_diferentes = False
    #print claves1
    #print claves2


    #iguales = []

    #for c1 in claves1:
    #    for c2 in claves2:
    #        if(c1 != c2):
    #            distancia = distancia + 1
    #        else:
    #            iguales += [c1]

    iguales = coincidencias
# print iguales

    for ci in iguales:
#         print ci
        print "Dic1: ", dic1[ci], "Dic2: ", dic2[ci]
        distancia = distancia + abs( dic1[ci] - dic2[ci] )

    if (totalmente_diferentes):
        distancia = 10000000

    print distancia
    return distancia


def dataset_from_documents():
    stopwords = open("stopwords_es.txt").read().split('\n')
    documents_dir = '../../test2/'
    dataset = []
    for f in listdir(documents_dir):
        content = open(documents_dir + f, "r").read().replace('\n', '').translate(None, "\"'.,-:;()*").split(' ')
        content_lower = [x.lower() for x in content if len(x) > 3]
        content_lower = [y for y in content_lower if y not in stopwords]
        counter = Counter()
        for word in content_lower:
            counter[word] += 1
        # Nombre del archivo
        counter[f] += 10000000

        #content = [y for y in [x for x in content if x != ''] if y.lower() not in stopwords]
        #print("Content:")
        #for sw in stopwords:
            #content = content.replace( ' ' + sw + ' ', '')
        #    content = [x for x in content if x != sw ]
        #print(content)
        #joined_content = " ".join(content)
        #print(joined_content)
        #dataset += [joined_content]
        dataset += [dict(counter.most_common(15))]
    return dataset


#data = [{"casa" : 3, "ambiente" : 2},{"casa" : 1, "pajaro" : 2},{"casa" : 1, "pajaro" : 2}]
data = dataset_from_documents()
cl = HierarchicalClustering(data, lambda x,y: distance(x,y))
print cl.getlevel(10)     # get clusters of items closer than 10
#print cl.getlevel(4)      # get clusters of items closer than 5
