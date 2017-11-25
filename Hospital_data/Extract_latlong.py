import pandas as pd
import googlemaps
import os

def openFile(filename):
    """
    Returns a csv file as a dataframe
    :param filename: csv file
    """
    df = pd.read_csv(filename)
    df.columns = ['Name', 'Region', 'Type', 'Ownership', 'Location',
       'Services', 'NHIS accredited']

    return df


def getName(df):
    """
    Returns the name column of a dataframe
    :param df: dataframe object
    """
    return df.Name

def getRegion(df):

    """
    Returns the region column of a dataframe
    :param df: dataframe object
    """

    return df.Region

def createColumns(df, name):

    """
    Makes a new column in a dataframe with the specified name
    :param df: dataframe object
    :param name: name of the column to be added to the dataframe

    """
    df[name] = None



api_token = os.environ.get('api_token', None)

maps = googlemaps.Client(key=api_token)



def getLatLong(df, country = "GHANA"):
    """
    Returns a dataframe with the latitude and longitude coordinates
    of all the hospitals addded
    :param df: dataframe object
    :param country: default country is Ghana
    """
    counter = 0

    #iterate through the name and region column of the dataframe
    for i,j in zip(getName(df), getRegion(df)):

        address = str(i) + ", " + str(j) + ", " + country

        data = maps.geocode(address)

        if len(data) == 0:
            continue
        else:
            latitude = data[0]["geometry"]["location"]["lat"]
            longitude = data[0]["geometry"]["location"]["lng"]
            df.Latitude[counter] = latitude
            df.Longitude[counter] = longitude

        counter += 1


    return df


def main():

    #Takes the name of the csv file
    filename = "Hospitals_Ghana.csv"

    #Opens the csv file as a Pandas dataframe
    df = openFile(filename)

    #Creates new columns, Latitude and Longitude
    createColumns(df, "Latitude")
    createColumns(df, "Longitude")

    #Finds the latitude and longitude coordinates of the respective hospitals
    updated_df = getLatLong(df)

    #Saves the modified dataframe as a csv file
    updated_df.to_csv("Full_hospital_list_1.csv")


if __name__ == "__main__":

	main()













