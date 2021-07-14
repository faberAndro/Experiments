# si puo' ottimizzare con migliori alogiritmi di ricerca e sort, invece che il linear
# ci possono essere duplicati: gestione dei duplicati

p = {'9:00': -30.0, '10:00': 38.2, '11:00': 18.71, '12:00': 14.38, '13:00': 18.22, '14:00': 41.63, '15:00': 116.66, '16:00': 84.86, '17:00': 44.96, '18:00': 8.82, '19:00': 15.67, '20:00': -66.0, '21:00': 27.44, '22:00': -52.0, '23:00': -0.0}

for z in p:
    b = w = float(p[z])
    bh = wh = z
     
for z in p:
    n = float(p[z])
    if n > b:
        b = n
        bh = z
    if n < w:
        w = n
        wh = z

bew = [bh, wh]
print(bew)