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

df.plot (style = "ro", legend = False)
plot.hlines (np.array ([-1, 0, 1]) * std[0] + avg[0],
             df.index.min (), 
             df.index.max (),
             colors = ["green", "blue", "green"],
             linestyles = ['dashed', 'solid', 'dashed'])
plot.xticks (np.arange (12) * 365 / 7 / 12, calendar.month_name[1:], 
             rotation = 35)
plot.xlabel ("")
plot.ylabel ("# of NSSI posts")
plot.title ("Unhappiness Index")

subplot = plot.axes ([.2, .2, .3, .3])
df.plot (kind = "hist", ax = subplot, legend = False, fontsize = 10,
         title = "# of Posts", bins = 20)

# plot.tight_layout ()
plot.savefig ("unhappiness.png")
plot.show ()
