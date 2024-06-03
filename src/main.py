import cProfile
import pstats
import datei_import as di
import numpy as np
import pandasplot

'''
daten_laenge = 10000
daten_anzahl = np.arange(daten_laenge + 1)
zahl_liste = daten_anzahl.tolist()
'''

#di.plotueberordner_downloadrate('/home/david/mobile_yt_dataset/dataset/')
di.plotueberordner_downloadrate('/home/david/Testmobile_yt_dataset/')




'''''
with cProfile.Profile() as profile:
    normal = pandasplot.plt_normal('streamvergleich720p.csv')
    pandasplot.plotten(normal)

results = pstats.Stats(profile)
results.sort_stats(pstats.SortKey.TIME)
results.print_stats()
results.dump_stats("results.prof")
'''

'''
versuchsplott = plot.plt_overtime(versuch)
versuchsplott2 = plot.plt_overtime(versuch2)

plot.plottdoppel(versuchsplott[0], versuchsplott[1],
                   versuchsplott2[0], versuchsplott2[1])
'''
