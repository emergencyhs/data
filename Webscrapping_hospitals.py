"""
This python file scrapes getting hospital data from url 'http://ghanahospitals.org/home/'
"""

#import packages
import urllib2
import urllib
import bs4



def openUrl(url, hdr={'User-Agent': "Magic Browser"}):
    """
    Returns the webpage as text
    :param url: the url of the webpage
    :return:
    """
    req = urllib2.Request(url, headers=hdr)
    source = urllib2.urlopen(req).read()
    return source


def makeSoup(source, type="html.parser"):

    """
    Returns a Beautiful Soup object
    :param source: takes a url as a source
    :param type: takes the format of the webpage as an optional argument
    """
    soup = bs4.BeautifulSoup(source, type)
    return soup


def regions():

    """
    Returns a list of all the regions in Ghana
    """
    regions = ["Ashanti", "Brong", "Central", "Eastern", "G. Accra", "Northern", "ueast", "uwest", "volta", "western"]

    return regions


def encodeName(name):

    """
    Returns an encoded url
    :param name: the string to be encoded
    """

    query = urllib.quote(name)
    url = "http://ghanahospitals.org/regions/opt.php?page=alpha&r=%s" % (query)
    return url

def encodeLink(link):

    """
    Returns an encoded url
    :param link:

    """
    ind = link.find(" ")
    place_holder = ind - 1
    query = urllib.quote(link[place_holder:])
    url = "http://ghanahospitals.org/regions/" + link[:place_holder] + "%s" % (query)
    return url


def getHospitalURLs(regions):

    """
    Returns the urls of all hospitals in the 10 regions of Ghana
    :param regions: list of regions in Ghana as recognized by the website
    """

    links = [] #make a list of the urls of the different hospitals

    for region in regions:

        if " " in region:
            url = encodeName(region)

        else:
            url = "http://ghanahospitals.org/regions/opt.php?page=alpha&r=" + region

        source = openUrl(url)

        soup = makeSoup(source)

        results_td = soup.find_all("div", {"class": "listing"})

        for i in results_td:
            links.append(i.a.get("href"))

    return links




def getDetails(urls):
    """
    Returns the Details of each hospital in a csv file
    :param urls: each hospital's url
    """

    f = open("Hospitals_Ghana.csv", "w")
    headers = "Name, Region, Type, Ownership, Location, Services, NHIS accredited\n"
    f.write(headers)


    for link in urls:

        if " " in link:

            url = encodeLink(link)

        else:
            url = "http://ghanahospitals.org/regions/" + link


        source = openUrl(url)
        soup = makeSoup(source)

        region = soup.find("td", {"height": "100", "class": "subbanner"}).text.strip()

        results_dive = soup.find_all("div", {"class": "fdtails_home"})


        for i in results_dive:
            name = i.strong.text.strip()

            tcases = i.find_all("span", {"class": "Tcase"})

            hospital_type = tcases[0].text.strip()

            ownership = tcases[1].text.strip()[11:]

            location = tcases[2].text.strip()

            services = tcases[4].text.strip()

            NHIS_accredited = tcases[6].text.strip()

        # Write the variables to a csv file to store
        f.write(name.replace(",", " ") + "," + region.replace(",", " ")+ "," + hospital_type.replace(",", " ") + "," + ownership.replace(",", " ") + \
                "," + location.replace(",", " ") + "," + services.replace(",", " ") + "," + NHIS_accredited+ "\n")
    f.close()



def main():

    regions_ = regions()
    urls = getHospitalURLs(regions_)
    getDetails(urls)


if __name__ == "__main__":
    main()