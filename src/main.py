import numpy as np
import pandas as pd
import plot

versuch = pd.read_csv('streamvergleich720p.csv')
versuch2 = pd.read_csv('streamvergleich144p.csv')

plot.plotten(plot.plt_flow(versuch)[0], plot.plt_flow(versuch)[1],
             plot.plt_flow(versuch)[2], plot.plt_flow(versuch)[3])
'''
versuchsplott = plot.plt_overtime(versuch)
versuchsplott2 = plot.plt_overtime(versuch2)

plot.plottdoppel(versuchsplott[0], versuchsplott[1],
                   versuchsplott2[0], versuchsplott2[1])
'''