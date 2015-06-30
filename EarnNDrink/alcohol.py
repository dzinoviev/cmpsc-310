from bs4 import BeautifulSoup
import numpy as np
import urllib.request
import pandas as pd
import sklearn.cluster
import matplotlib.pyplot as plt

ALCO_SOURCE = "https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"
GDP_SOURCE = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita"

# Cook the soup and find sortable tables
soup1 = BeautifulSoup (urllib.request.urlopen (ALCO_SOURCE))
tabs1 = soup1.findAll ("table", {"class" : "wikitable sortable"})

# Extract the rows, the headers, and the rest of the data
rows1 = tabs1[1].findAll ('tr')
headers1 = ['.'.join (x.text.split ()) for x in rows1[0].findAll ('th')]
body1 = [[x.text.strip () for x in r.findAll ('td')] for r in rows1[1:]]

# Create a data frame
alc = pd.DataFrame (body1, columns = headers1)
alc.set_index (headers1[0], inplace = True)

# Process NAs and convert strings to doubles
alc[alc == ''] = np.nan
alc[alc == '-'] = np.nan
alc = alc.astype (float, copy = False)

print (alc.describe ())

# Cook the soup and find sortable tables
soup2 = BeautifulSoup (urllib.request.urlopen (GDP_SOURCE))
tabs2 = soup2.findAll ("table", {"class" : "wikitable sortable"})

# Extract the rows, the headers, and the rest of the data
rows2 = tabs2[0].findAll ('tr')
headers2 = ['.'.join (x.text.split ()) for x in rows2[0].findAll ('th')]
body2 = [[x.text.strip () for x in r.findAll ('td')] for r in rows2[1:]]

# Create a data frame
gdp = pd.DataFrame (body2, columns = headers2)
gdp.set_index (headers2[1], inplace = True)

# Process NAs and convert strings to doubles
gdp[gdp == '—'] = np.nan
gdp[gdp == '-'] = np.nan
gdp[gdp == ''] = np.nan
gdp['Int$'] = gdp['Int$'].str.replace (',', '').astype (float)

print (gdp.describe ())

# Join the data frames by index, remove NA rows
combined = gdp.join (alc)[['Total', 'Int$']].dropna ()

# Is there any correlation?
print (combined.corr ())

# Scale the numbers to be in the range [0..1]
minTotal = combined["Total"].min ()
rangeTotal = combined["Total"].max () - combined["Total"].min ()
minIntD = combined["Int$"].min ()
rangeIntD = combined["Int$"].max () - combined["Int$"].min ()

combined["Total.n"] = (combined["Total"] - minTotal) / rangeTotal
combined["Int$.n"] = (combined["Int$"] - minIntD) / rangeIntD

# I want 9 clusters
NC = 9
kmeans = sklearn.cluster.KMeans (n_clusters = NC) 
combined["Cluster"] = kmeans.fit_predict (combined[["Total.n","Int$.n"]])
combined.sort (["Cluster", "Int$"], ascending = [True, False], inplace = True)

# Unscale the cluster centers
centersDF = pd.DataFrame (kmeans.cluster_centers_, columns = ["Total", "Int$"])
centers = centersDF * np.array ((rangeTotal, rangeIntD)) \
    + np.array ((minTotal, minIntD))
                        
# List the clusters
print ('\n\n'.join([', '.join (combined[combined["Cluster"] == i].index.values)
                    for i in combined["Cluster"].unique ()]))

# Plot the clustered data
ax = combined.plot (x = "Total", y = "Int$", kind = "scatter",
                    c = "Cluster", colormap = plt.cm.get_cmap ('gist_ncar', NC),
                    colorbar = False,
                    s = 80, alpha = 0.75, xlim = 0, ylim = 0,
                    title = "Rich get richer, Drunk get... drunker")

# Plot the cluster centers
centers.plot (x = "Total", y = "Int$", kind = "scatter",
              s = 300, marker = "s", ax = ax, c = "r", alpha = 0.4)
plt.xlabel ("Yearly alcohol consumption per capita, l")
plt.ylabel ("GDP (PPP) per capita, Int$")

# Voila!
plt.savefig ("earn-and-drink.png")
plt.show ()

