from bs4 import BeautifulSoup
import numpy as np
import urllib.request
import pandas as pd
import sklearn.cluster
import matplotlib.pyplot as plt

soup1 = BeautifulSoup (urllib.request.urlopen ("https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"))

tabs1 = soup1.findAll ("table", {"class" : "wikitable sortable"})

rows1 = tabs1[1].findAll ('tr')
headers1 = ['.'.join (x.text.split ()) for x in rows1[0].findAll ('th')]
body1 = [[x.text.strip () for x in r.findAll ('td')] for r in rows1[1:]]
alc = pd.DataFrame (body1, columns = headers1)
alc.set_index (headers1[0], inplace = True)
alc[alc == ''] = np.nan
alc[alc == '-'] = np.nan
alc = alc.astype (float, copy = False)

print (alc.describe ())

soup2 = BeautifulSoup (urllib.request.urlopen ("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita"))
tabs2 = soup2.findAll ("table", {"class" : "wikitable sortable"})
rows2 = tabs2[0].findAll ('tr')
headers2 = ['.'.join (x.text.split ()) for x in rows2[0].findAll ('th')]
body2 = [[x.text.strip () for x in r.findAll ('td')] for r in rows2[1:]]
gdp = pd.DataFrame (body2, columns = headers2)
gdp.set_index (headers2[1], inplace = True)
gdp[gdp == '—'] = np.nan
gdp[gdp == '-'] = np.nan
gdp[gdp == ''] = np.nan
gdp['Int$'] = gdp['Int$'].str.replace (',', '').astype (float)
print (gdp.describe ())

combined = gdp.join (alc)[['Total', 'Int$']].dropna ()
print (combined.corr ())

minTotal = combined["Total"].min ()
rangeTotal = combined["Total"].max () - combined["Total"].min ()
minIntD = combined["Int$"].min ()
rangeIntD = combined["Int$"].max () - combined["Int$"].min ()

combined["Total.n"] = (combined["Total"] - minTotal) / rangeTotal
combined["Int$.n"] = (combined["Int$"] - minIntD) / rangeIntD

NC = 9
kmeans = sklearn.cluster.KMeans (n_clusters = NC) 
combined["Cluster"] = kmeans.fit_predict (combined[["Total.n","Int$.n"]])
combined.sort (["Cluster", "Int$"], ascending = [True, False], inplace = True)
centers = pd.DataFrame (kmeans.cluster_centers_,
                        columns = ["Total", "Int$"]) \
                        * np.array ((rangeTotal, rangeIntD)) \
                        + np.array (minTotal, minIntD)
                        
print ('\n\n'.join([', '.join (combined[combined["Cluster"] == i].index.values)
                    for i in combined["Cluster"].unique ()]))

ax = combined.plot (x = "Total", y = "Int$", kind = "scatter",
                    c = "Cluster", colormap = plt.cm.get_cmap ('gist_ncar', NC),
                    colorbar = False,
                    s = 80, alpha = 0.75, xlim = 0, ylim = 0,
                    title = "Rich get richer, Drunk get... drunker")
centers.plot (x = "Total", y = "Int$", kind = "scatter",
              s = 300, marker = "s", ax = ax, c = "r", alpha = 0.4)
plt.xlabel ("Yearly alcohol consumption per capita, l")
plt.ylabel ("GDP (PPP) per capita, Int$")
plt.savefig ("earn-and-drink.png")
plt.show ()

