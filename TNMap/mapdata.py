# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:53:39 2019
@author: ashwa
"""

# importing libraries
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns

# initialozing visualization set
sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10, 6))

# opening the vector map
shp_path = "D:\\MEGA\\Core CS\\Projects\\TNWaterMap\\resources\\tamilnadu_district.shp"
# reading the shape file by using reader function of the shape lib
sf = shp.Reader(shp_path)

# number of different shapes which were imported by shp.reader
len(sf.shapes())

# exploring the records from the shape file
sf.records()


# converting shapefile data in pandas dataframe
def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords'
    column holding the geometry information. This uses the pyshp
    package
    """
    # fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]
    # fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    # converting shapefile data into pandas dataframe
    df = pd.DataFrame(columns=fields, data=records)
    # assigning the coordinates
    df = df.assign(coords=shps)
    return df


# visualization of data after being converted into dataframes where it refers to rows and columns
df = read_shapefile(sf)
df.shape

# seeing the sample of a data representation the last point has the coordinates of the data lat and long which will be used to create a specific map shape
df.sample(5)

# we can access the diff columns by only its column name
print(df.DIST_NAME)


# plotting the map of a small city in rajasthan or a specific shape with the help of matplotlib
# a) Plot the shape (polygon) based on the city's coordinates and,
# b) calculate and return the medium point of that specific shape (x0, y0).
# This medium point was also used to define where to print the city's name
def plot_shape(id, s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    # plotting the graphical axes where map ploting will be done
    ax = plt.axes()
    ax.set_aspect('equal')
    # storing the id number to be worked upon
    shape_ex = sf.shape(id)
    # NP.ZERO initializes an array of rows and column with 0 in place of each elements
    # an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    x_lon = np.zeros((len(shape_ex.points), 1))
    # an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    # plotting using the derived coordinated stored in array created by numpy
    plt.plot(x_lon, y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
    return x0, y0


# setting the city name whose map to be printed
DIST_NAME = 'JAIPUR'
# to get the id of the city map to be plotted
com_id = df[df.DIST_NAME == 'JAIPUR'].index.get_values()[0]
plot_shape(com_id, DIST_NAME)

sf.shape(com_id)


# plotting the full map of rajasthan
def plot_map(sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''
    plt.figure(figsize=figsize)
    id = 0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id + 1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


# calling the function and passing required parameters
plot_map(sf)

# plotting a zoomed map
y_lim = (2900000, 3000000)  # latitude
x_lim = (200000, 400000)  # longitude

plot_map(sf, x_lim, y_lim)


# plotting a single shape over a map

def plot_map2(id, sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon, y_lat, 'r', linewidth=3)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


# plotting the city with particular id
plot_map2(26, sf)


# to darken the color
def plot_map_fill(id, sf, x_lim=None,
                  y_lim=None,
                  figsize=(11, 9),
                  color='r'):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    ax.fill(x_lon, y_lat, color)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


# plot_map_fill(0, sf, x_lim, y_lim, color='g')

plot_map_fill(13, sf, color='g')


# plotting multiple shapes on a map with the help of ID
def plot_map_fill_multiples_ids(title, city, sf,
                                x_lim=None,
                                y_lim=None,
                                figsize=(11, 9),
                                color='r'):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    for id in city:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color)

        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, id, fontsize=10)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


# naming the id number of the cities to be coloured
city_id = [0, 1, 2, 3, 4, 5, 6]
plot_map_fill_multiples_ids("Multiple Shapes",
                            city_id, sf, color='g')


# plotting the city on the map to be coloured by using the dist_name
def plot_cities_2(sf, title, cities, color):
    '''
    Plot map with selected comunes, using specific color
    '''

    df = read_shapefile(sf)
    city_id = []
    for i in cities:
        city_id.append(df[df.DIST_NAME == i.upper()]
                       .index.get_values()[0])
    plot_map_fill_multiples_ids(title, city_id, sf,
                                x_lim=None,
                                y_lim=None,
                                figsize=(11, 9),
                                color=color);


south = ['jaipur', 'churu', 'bikaner']
plot_cities_2(sf, 'North', south, 'c')
plt.show()


# heat mapping

def calc_color(data, color=None):
    if color == 1:
        color_sq = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0', '#807dbaF0', '#6a51a3F0', '#54278fF0'];
        colors = 'Purples';
    elif color == 2:
        color_sq = ['#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494'];
        colors = 'YlGnBu';
    elif color == 3:
        color_sq = ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#636363', '#252525'];
        colors = 'Greys';
    elif color == 9:
        color_sq = ['#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000'];

    else:
        color_sq = ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#d95f0e', '#993404'];
        colors = 'YlOrBr';
    new_data, bins = pd.qcut(data, 6, retbins=True,
                             labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val])
    if color != 9:
        colors = sns.color_palette(colors, n_colors=6)
        sns.palplot(colors, 0.6);
        for i in range(6):
            print("\n" + str(i + 1) + ': ' + str(int(bins[i])) +
                  " => " + str(int(bins[i + 1]) - 1))
        print("\n\n   1   2   3   4   5   6")
    return color_ton, bins;


def plot_cities_data(sf, title, cities, data=None, color=None, print_id=False):
    '''
    Plot map with selected comunes, using specific color
    '''

    color_ton, bins = calc_color(data, color)
    df = read_shapefile(sf)
    city_id = []
    for i in cities:
        city_id.append(df[df.DIST_NAME ==
                          i.upper()].index.get_values()[0])
    plot_map_fill_multiples_ids_tone(sf, title, city_id,
                                     print_id,
                                     color_ton,
                                     bins,
                                     x_lim=None,
                                     y_lim=None,
                                     figsize=(11, 9));


def plot_map_fill_multiples_ids_tone(sf, title, city,
                                     print_id, color_ton,
                                     bins,
                                     x_lim=None,
                                     y_lim=None,
                                     figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    for id in city:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color_ton[city.index(id)])
        if print_id != False:
            x0 = np.mean(x_lon)
            y0 = np.mean(y_lat)
            plt.text(x0, y0, id, fontsize=10)
    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


south = ['jaipur', 'bikaner', 'churu', 'bhilwara', 'udaipur']
data = [100, 2000, 300, 400000, 500, 600, 100, 2000, 300, 400, 500, 600, 100, 2000, 300, 400, 500, 600]
print_id = True  # The shape id will be printed
color_pallete = 1  # 'Purples'
plot_cities_data(sf, 'South', south, data, color_pallete, print_id)

# plotting real data
census_17 = df.POPULATION
census_17.shape

title = 'Population Distrubution on Rajasthan Region'
data = census_17
names = df.DIST_NAME
plot_cities_data(sf, title, names, data, 4, True)