
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


def coord_x(longitude, image):
    h, l, _ = image.shape
    x = l*longitude/360 + l/2
    return x

def coord_y(latitude, image):
    h, l, _ = image.shape
    y = - h*latitude/180 + h/2
    return y

def coord(longitude,latitude, image) :
    return (coord_x(longitude,image),coord_y(latitude,image))

def meridiens(deg, image):
    for longitude in range(0, 180, deg):
        A = coord(longitude,-90, image)
        B = coord(longitude,90, image)
        plt.plot([A[0], B[0]], [A[1], B[1]], 'black', alpha = 0.2)
    for longitude in range(0, -180, -deg):
        A= coord(longitude,-90, image)
        B= coord(longitude,90, image)
        plt.plot([A[0], B[0]], [A[1], B[1]], 'black', alpha = 0.2)
    
def paralleles(deg, image) :
    for latitude in range(0, 90, deg):
        A = coord(-180, latitude, image)
        B = coord(180, latitude, image)
        plt.plot([A[0], B[0]], [A[1], B[1]], 'black', alpha = 0.2)
    for latitude in range(0, -90, -deg):
        A = coord(-180, latitude, image)
        B = coord(180, latitude, image)
        plt.plot([A[0], B[0]], [A[1], B[1]], 'black', alpha = 0.2)

def init_carte(nom_image) :
    image  = plt.imread(nom_image, format=None)
    plt.imshow(image)
    plt.xlim(0, image.shape[1])
    plt.ylim(image.shape[0], 0)
    #meridiens(15, image)  # decommenter
    #paralleles(15, image) # decommenter
    return image


conn = sqlite3.connect("flights.db")
airports = pd.read_sql("select * from airports", conn)
airlines = pd.read_sql("select * from airlines", conn)
routes = pd.read_sql("select * from routes", conn)
airports['latitude'] = pd.to_numeric((airports['latitude']))
airports['longitude'] = pd.to_numeric((airports['longitude']))

def affiche_aeroports(aeroports,image):
    X = coord_x( aeroports['longitude'], image)
    Y = coord_y( aeroports['latitude'], image)
    plt.scatter(X,Y,1)


### Exercie 1 : Listons les 15 villes ayant le plus d’aéroports dans la base

aeroports_par_ville = airports[['code','city']].groupby('city').count().sort_values('code',ascending=False)

aeroports_par_ville = aeroports_par_ville[0:15]


print(aeroports_par_ville)


### Exercice 2

""" Partie 1 : Construisons et affichons le nombre de compagnies (airlines) par pays """


airlines_par_pays = airlines[['id','country']].groupby('country').count()

print(airlines_par_pays)


""" Partie 2 : Tracons sur la carte des points proportionnels au nombre de compagnies par pays """

par_pays =  airports[['country', 'longitude', 'latitude']].groupby('country').agg({'longitude':'mean','latitude':'mean'})

par_pays['total_airlines'] = airlines_par_pays

image = init_carte("Equirectangular-projection-topographic-world.jpg")

plt.scatter(coord_x(par_pays['longitude'],image),coord_y(par_pays['latitude'],image),par_pays['total_airlines']/10)

plt.show() 



 
### Exercie 3 :

# Fonction de l'itineraire 

 
def itineraire(xA, yA, xB, yB, image):
    plt.plot([coord_x(xA,image),coord_x(xB,image)],
             [coord_y(yA,image),coord_y(yB,image)], linewidth=0.5,color = 'r')


""" 1 - Affichage de l'ensemble des liaisons qui partent de France en destination des Etats-Unis """

base_donnes = airports.merge(routes,left_on = 'code',right_on='source' )

base_donnes = base_donnes[base_donnes['country']== 'France']


base_donnes = base_donnes.merge(airports[airports['country']== 'United States'],left_on= 'dest', right_on='code')


image = init_carte("Equirectangular-projection-topographic-world.jpg")

itineraire(base_donnes['longitude_x'],base_donnes['latitude_x'],base_donnes['longitude_y'],base_donnes['latitude_y'],image)

plt.show() 

    
""" 2 - Affichage de l'ensemble des liaisons effectues par les compagnies aeriennes du Royaume-Uni et des Etats-Unis """ 

Uk_Us = airlines[airlines['country']=='United Kingdom'].merge(airlines[airlines['country']=='United States'],how='outer')

routes_airlines = routes.merge(Uk_Us,how='inner')

base_donnes = airports.merge(routes_airlines,left_on='code',right_on='source')

base_donnes = base_donnes.merge(airports,left_on= 'dest', right_on='code')

image = init_carte("Equirectangular-projection-topographic-world.jpg")

itineraire(base_donnes['longitude_x'],base_donnes['latitude_x'],base_donnes['longitude_y'],base_donnes['latitude_y'],image)

plt.show() 

 
""" 3 - Affichage de l'ensemble des liaisons effectuees par toutes les compagnies aeriennes en destination de l'Australie et de la Chine """ 

base_donnes = airports.merge(routes,left_on = 'code',right_on='source' )


China_Australia = airports[airports['country']=='Australia'].merge(airports[airports['country']=='China'],how='outer')


base_donnes = base_donnes.merge(China_Australia,left_on= 'dest', right_on='code')


image = init_carte("Equirectangular-projection-topographic-world.jpg")


itineraire(base_donnes['longitude_x'],base_donnes['latitude_x'],base_donnes['longitude_y'],base_donnes['latitude_y'],image)


plt.show() 












































