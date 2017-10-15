import folium
import pandas as pd

data = pd.read_csv("GDP_2016.csv")
data = data.set_index("Country")

all_balcan_gdp_per_capita = data.ix[0, "WB_2016"] \
      + data.ix[3, "WB_2016"] \
      + data.ix[17, "WB_2016"] \
      + data.ix[21, "WB_2016"] \
      + data.ix[23, "WB_2016"] \
      + data.ix[28, "WB_2016"]

western_balcan_average_gdp_per_capita = int(all_balcan_gdp_per_capita / 6)

eu_gdp_per_capita = list(data["WB_2016"])

# extract the data except of west Bakan countries
indices = 0, 3, 17, 21, 23, 28
df6 = [i for j, i in enumerate(eu_gdp_per_capita) if j not in indices]

# sum of the data and the average gdp of EU countries
product = 1
for x in df6:
    product += x
eu_average_gdp_per_capita = product / 28
eu_average_gdp_per_capita = int(eu_average_gdp_per_capita)


def color_producer(gdp):
    if gdp == western_balcan_average_gdp_per_capita:
        return "blue"
    else:
        return "red"

# list of average GDP of Balcan and EU with relevant coordinates
avg_gdp = [western_balcan_average_gdp_per_capita, eu_average_gdp_per_capita]
coordinates = ["43.214764, 19.580932", "50.051477, 10.605102"]

map = folium.Map(location=[57.006031, 9.374633],
                 tiles='Mapbox Bright',
                 zoom_start=4)

fg_gdp = folium.FeatureGroup(name="EU & western Balkan annual GDP per capita")

for i, j in zip(avg_gdp, coordinates):
    fg_gdp.add_child(folium.CircleMarker(location=[j],
                                         radius=10,
                                         popup="$ " + str(i),
                                         fill_color=color_producer(i),
                                         color="grey",
                                         fill_opacity=0.9))


data_eu = pd.read_csv("eu_and_balcan.csv")

country = list(data_eu["Country"])
lat = list(data_eu["latitude"])
lon = list(data_eu["longitude"])
gdp = list(data_eu["WB_2016"])


def color_producer(gdp):
    if gdp <= 10000:
        return "green"
    elif 10000 <= gdp <= 20000:
        return "yellow"
    elif 20000 <= gdp <= 30000:
        return "orange"
    else:
        return "red"

fg_c = folium.FeatureGroup(name="Countries GDP per capita")

for c, lt, ln, g in zip(country, lat, lon, gdp):
    fg_c.add_child(folium.CircleMarker(location=[lt, ln],
                                       radius=5,
                                       popup="$ " + str(g),   # c + ", $" + g
                                       fill_color=color_producer(g),
                                       color="grey",
                                       fill_opacity=0.7))


fg_e = folium.FeatureGroup(name="Europe & Balkan")

fg_e.add_child(folium.GeoJson(data=open("eu_balkans.json", "r", encoding="utf-8-sig"),
                              style_function=lambda x: {"fillColor": "red" if x["id"] == "SRB"
                              or x["id"] == "ALB"
                              or x["id"] == "MKD"
                              or x["id"] == "MNE"
                              or x["id"] == "CS-KM"
                              or x["id"] == "BIH"
                              else "blue"}))


map.add_child(fg_e)
map.add_child(fg_c)
map.add_child(fg_gdp)
map.add_child(folium.LayerControl())

map.save("eu_balkans.html")
