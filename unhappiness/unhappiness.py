import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import calendar
import scipy.stats as stats

df = pd.read_table ("postsbyweek.dat", index_col = 0, names = ["count"])
df.drop (53, inplace = True)

corr, pvalue = stats.pearsonr (df.index.values, df["count"])
print ("Correlation:", corr, "P-value:", pvalue)

avg = df.mean ()
std = df.std ()

df.plot (style = "ro-", legend = False, fontsize = 11)
plot.hlines (np.array ([-1, 0, 1]) * std[0] + avg[0],
             df.index.min (), 
             df.index.max (),
             colors = ["green", "blue", "green"],
             linestyles = ['dashed', 'solid', 'dashed'])
plot.xticks (np.arange (12) * 365 / 7 / 12, calendar.month_name[1:], 
             rotation = 30)
plot.xlabel ("")
plot.ylabel ("# of NSSI posts")
plot.title ("Unhappiness Index")

plot.annotate (s = "rho=%.3f" % corr, xy = (35, 700))
plot.annotate (s = "p-value=%.3f" % pvalue, xy = (35, 650))

subplot = plot.axes ([.25, .2, .3, .25])
df.plot (kind = "hist", ax = subplot, legend = False, fontsize = 10,
         title = "Posts", bins = 20, orientation = "horizontal")

# plot.tight_layout ()
plot.savefig ("unhappiness.png")
plot.show ()
