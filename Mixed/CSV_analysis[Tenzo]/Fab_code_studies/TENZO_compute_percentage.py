

costi   = {'9:00': 30.0, '10:00': 50.0, '11:00': 60.0, '12:00': 74.0, '13:00': 74.0, '14:00': 74.0, '15:00': 74.0, '16:00': 64.0, '17:00': 64.0, '18:00': 66.0, '19:00': 66.0, '20:00': 66.0, '21:00': 66.0, '22:00': 52.0, '23:00': 0.0}
vendite = {'10:00': 130.88, '11:00': 320.65, '12:00': 514.65, '13:00': 406.08, '14:00': 177.77, '15:00': 63.43, '16:00': 75.42, '17:00': 142.34, '18:00': 748.62, '19:00': 421.08, '20:00': 0.0, '21:00': 240.54}

percentuali = {}
for x in costi:
    if (x in vendite and float(vendite[x] != 0)):
        o = round(100*(float(costi[x]) / float(vendite[x])),2)
    else:
        o = - float(costi[x])
    
    percentuali[x] = o
    
print(percentuali)
    #print(x,int(round(o,2)*100));
    
