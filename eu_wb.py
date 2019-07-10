"""
Interactive map of European Union(EU) and West Balcan countries GDP per capita and median GDP.
West Balcan countries inspire to enter the EU and with this map it's obvious that
they need more work with democratisation and advancing their economies to enter EU.
When you run it python/3 eu_wb.py will generate eu_balkans.html. Please open it in your favorite browser
Done with Folium by a Djangonaut/Pythonista :)
Ps: I'm Albanian, which is a West Balcan country
Pps: Shape file(eu_balcans.json) doesn't have great geospatial vector data,
but this is the best one I could find that shows Kosovo as an indipendent country
"""

import folium
import pandas as pd


data = pd.read_csv("GDP_2016.csv")
data = data.set_index("Country")

western_balcan_average_gdp_per_capita = data.ix[0, "WB_2016"] + \
                                        data.ix[3, "WB_2016"] + \
                                        data.ix[17, "WB_2016"] + \
                                        data.ix[21, "WB_2016"] + \
                                        data.ix[23, "WB_2016"] + \
                                        data.ix[28, "WB_2016"]

western_balcan_average_gdp_per_capita = int(western_balcan_average_gdp_per_capita / 6)

eu_gdp_per_capita = list(data["WB_2016"])

# extract the data except of west Balkan countries
indices = 0, 3, 17, 21, 23, 28
df = [i for j, i in enumerate(eu_gdp_per_capita) if j not in indices]

# sum of the data and the average gdp of EU countries
gdp = 1
for x in df:
    gdp += x
eu_average_gdp_per_capita = gdp / 28
eu_average_gdp_per_capita = int(eu_average_gdp_per_capita)


def median_gdp_color(gdp):
    """Median GDP per capita color"""
    if gdp == western_balcan_average_gdp_per_capita:
        return "blue"
    else:
        return "red"


def median_gdp():
    """Median GDP per capita for European Union and West Balcan counties"""
    # list of average GDP of Balcan and EU with relevant coordinates
    avg_gdp = [western_balcan_average_gdp_per_capita, eu_average_gdp_per_capita]
    coordinates = [(43.214764, 19.580932), (50.051477, 10.605102)]

    fg_gdp = folium.FeatureGroup(name="EU & Western Balkan annual GDP per capita")

    for av, coord in zip(avg_gdp, coordinates):
        fg_gdp.add_child(folium.CircleMarker(location=coord,
                                             radius=10,
                                             popup=f"${str(av)}",
                                             fill_color=median_gdp_color(av),
                                             color="grey",
                                             fill_opacity=0.9))
    return fg_gdp


def country_gdp_color(gdp):
    if gdp <= 10000:
        return "green"
    elif 10000 <= gdp <= 20000:
        return "yellow"
    elif 20000 <= gdp <= 30000:
        return "orange"
    else:
        return "red"


def eu_bal_gdp():
    """European Union and West Balcan countries GDP per capita"""
    data_eu = pd.read_csv("GDP_2016.csv")
    country = list(data_eu["Country"])
    lat = tuple(data_eu["latitude"])
    lon = list(data_eu["longitude"])
    gdp = list(data_eu["WB_2016"])

    fg_c = folium.FeatureGroup(name="Countries GDP per capita")

    for c, lt, ln, g in zip(country, lat, lon, gdp):
        fg_c.add_child(folium.CircleMarker(location=[lt, ln],
                                           radius=5,
                                           popup="$" + str(g),
                                           fill_color=country_gdp_color(g),
                                           color="grey",
                                           fill_opacity=0.7))
    return fg_c


def eu_bal_boundaries():
    """Shape file for European Union and West Balcan countries"""
    fg_e = folium.FeatureGroup(name="Europe & Balkan")

    fg_e.add_child(folium.GeoJson(data=open("eu_balkans.json", "r", encoding="utf-8-sig").read(),
                                  style_function=lambda x: {"fillColor": "red"
                                  if x["id"] == "SRB"
                                  or x["id"] == "ALB"
                                  or x["id"] == "MKD"
                                  or x["id"] == "MNE"
                                  or x["id"] == "CS-KM"
                                  or x["id"] == "BIH"
                                  else "blue"}))
    return fg_e


if __name__ == '__main__':
    map = folium.Map(location=(57.006031, 9.374633),
                     tiles='cartodbpositron',
                     zoom_start=4)

    map.add_child(eu_bal_boundaries())
    map.add_child(eu_bal_gdp())
    map.add_child(median_gdp())
    map.add_child(folium.LayerControl())

    map.save("eu_balkans.html")
