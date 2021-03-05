import gpxpy
import gpxpy.gpx
from rdflib import URIRef,Literal,Graph,Namespace,RDF
from math import sin, cos, sqrt, atan2,radians
import xml.etree.ElementTree as ET
import rdflib


## Fonction qui permet de parcourir le fichier gpx et d'obtenir les latitudes et longitudes de tout les waypoints et trackpoint
def obtainLatLongMinMax(filename):
    filename = 'GPX_Tracks/'+filename
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    lat = [waypoint.latitude for waypoint in gpx.waypoints]
    long = [waypoint.longitude for waypoint in gpx.waypoints]
    return [min(long),min(lat),max(long),max(lat)]

def coordTometer(lat1,lon1,lat2,lon2): #En entrant deux pair de longitude/latitue on obtient la distance en métres
    R = 6373.0 #Rayon de la terre
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c *1000

bbox1 = obtainLatLongMinMax("4sDDFdd4cjA.gpx")  #une bbox contient la latitude et longitude min et max
bbox2 = obtainLatLongMinMax("btSeByOExEc.gpx")
bbox3 = obtainLatLongMinMax("kmrcRbHcMpg.gpx")
bbox4 = obtainLatLongMinMax("PO21QxqG2co.gpx")

bbox5 = obtainLatLongMinMax("pRAjjKqHwzQ.gpx")
bbox6 = obtainLatLongMinMax("rx1-4gf5lts.gpx")
bbox7 = obtainLatLongMinMax("tIRn_qJSB5s.gpx")
bbox8 = obtainLatLongMinMax("UAQjXL9WRKY.gpx")

# print(bbox1)    En les printants nous pouvons télécharger les fichiers osm associés
# print(bbox2)
# print(bbox3)
# print(bbox4)
# print("     ")
# print(bbox5)
# print(bbox6)
# print(bbox7)
# print(bbox8)

## On veut maintenant retourner les noeuds avec les tags intéressant

def takeAllPoints(filename): # Recupere les nodes possédants des tags
    filename = 'Osm/' + filename
    root = ET.parse(filename).getroot()
    pointsOfInterest = []
    for node in root.findall("node"):
            lat = node.get('lat')
            lon = node.get('lon')
            tagKeyValue = [[tag.get('k'),tag.get('v')] for tag in node]
            if not tagKeyValue == []:
                pointsOfInterest.append([lat]+[lon]+tagKeyValue)
    return pointsOfInterest




# Creer noeud graphe rdf avec trackpoint

def rdfGraphe(filename,d):

    filename = 'GPX_Tracks/'+filename # On redefini le cheminement au fichier
    gpx_file = open(filename, 'r') # On ouvre et on parse le fichier gpx
    gpx = gpxpy.parse(gpx_file)
    g=Graph()
    filename = filename[11:-1]
    filename = filename[0:-3]
    filename = filename +'.osm'
    allPoints = takeAllPoints(filename)
    trk = Namespace("http://trackpoint/") # On définit nos namespace afin de faciliter la definition de notre graphe
    osm = Namespace("http://osmInfo/")
    #neighbour = Namespace("http://link/")
    for track in gpx.tracks: # On crée des noeuds du graphe correspondant à chaque trackpoint dans le fichier gpx en donnant comme litéraux leur latitude et longitude
        for segment in track.segments:
            for i in range(len(segment.points)):
                g.add((URIRef("http://trackpoint/"+str(i)), RDF.type, trk.point))
                g.add((URIRef("http://trackpoint/"+str(i)),trk.latitude,Literal(str(segment.points[i].latitude))))
                g.add((URIRef("http://trackpoint/"+str(i)), trk.longitude, Literal(str(segment.points[i].longitude))))


    # Ici, après avoir filtre notre fichier osm on crée des noeuds en affectant leur longitude, latitude et chacun des autres tag présent de le node.

    for i in range(len(allPoints)):
        g.add((URIRef("http://osmInfo/" + str(i)), RDF.type, osm.node))
        g.add((URIRef("http://osmInfo/" + str(i)), osm.latitude, Literal(allPoints[i][0])))
        g.add((URIRef("http://osmInfo/" + str(i)), osm.longitude, Literal(allPoints[i][1])))
        n = len(allPoints[i])
        for j in range(2,n):
            g.add((URIRef("http://osmInfo/" + str(i)),URIRef("http://osmInfo/"+allPoints[i][j][0]), Literal(allPoints[i][j][1])))


    # Il reste plus qu'a lier nos noeuds, pour cela nous avons decidé de faire appel à une fct qui convertie deux paire de latitude/longitude en metre.
    # Selon la valeur distance rentré, on lie les point d'interet du fichier osm au trackpoint le plus proche.
    tabu = []
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(len(segment.points)):
                for j in range(len(allPoints)):
                    if coordTometer(segment.points[i].latitude,segment.points[i].longitude,float(allPoints[j][0]),float(allPoints[j][1])) < d and allPoints[j] not in tabu:
                        g.add((URIRef("http://trackpoint/"+str(i)),trk.HasPointOfInterest, URIRef("http://osmInfo/" + str(j))))
                        tabu.append(allPoints[j])
    return g







def QuerySparsql(filename,d): # fct qui

    graphe = rdfGraphe(filename,d)
    filename = filename[0:-4]
    filename = 'turtle/'+filename+'.ttl'

    ## Sparql:
    g = rdflib.Graph()
    result = g.parse(filename, format='ttl')
    query = """ PREFIX ns2: <http://trackpoint/>
                PREFIX ns1: <http://osmInfo/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                select ?x ?o where { 
                    ?s1 ns2:HasPointOfInterest ?s .
                    ?s rdf:type ns1:node .
                    ?s ns1:name ?o .
                    ?s ns1:amenity ?x .
                } ORDER BY ?x ASC(?s1) """

    resultat = g.query(query)





    return resultat



def GPS_INFO(filename,d):
    filename = filename
    resultat = QuerySparsql(filename,d)
    resultat = list(resultat)
    pointsOfInterest = []
    for element in resultat:
        pointsOfInterest.append([str(element[0]),str(element[1])])

    categories = []
    for point in pointsOfInterest:
        if point[0] not in categories:
            categories.append(point[0])


    dictionaire = dict()
    for element in categories:
        dictionaire[element] = []

    for element in pointsOfInterest:
        dictionaire[element[0]].append(element[1])

    return dictionaire



#dic = GPS_INFO("4sDDFdd4cjA.gpx",500)
#print(dic)



