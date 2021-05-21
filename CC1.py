

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
    meridiens(15, image)      # décommentez cette ligne si vous avez fait meridiens
    paralleles(15, image)     # décommentez cette ligne si vous avez fait paralleles
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



### Question 1 :





### Question 2
par_pays =  airports[['country', 'longitude', 'latitude']].groupby('country').agg({'longitude':'mean','latitude':'mean'})





### Question 3 :



