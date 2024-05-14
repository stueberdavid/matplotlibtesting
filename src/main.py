import numpy as np
import pandas as pd
import plot

versuch = pd.read_csv('streamvergleich720p.csv')
versuch2 = pd.read_csv('streamvergleich144p.csv')

plot.plotten(plot.plt_frametopayload(versuch)[0], plot.plt_frametopayload(versuch)[1])
'''
versuchsplott = plot.plt_overtime(versuch)
versuchsplott2 = plot.plt_overtime(versuch2)

plot.plottendoppel(versuchsplott[0], versuchsplott[1],
                   versuchsplott2[0], versuchsplott2[1])
'''