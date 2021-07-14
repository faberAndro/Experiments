# parsing json

import json
file = r'C:\Users\FABBA\Desktop\IT Projects\zzz. Job Exercises\en.1.json'
f = open(file)
partite = f.read()
dati = json.loads(partite)
squadre = {}
check = 0
r = dati["rounds"]

for i in r:
    
    rI = i
    m_rI = rI["matches"]
    
    for j in m_rI:
    
        mI_rJ = j
    
        t1 = mI_rJ["team1"]
        k_t1 = t1["key"]
        n_t1 = t1["name"]
        s1 = mI_rJ["score1"]
        if squadre.get(k_t1):   
            score1 = [n_t1,squadre[k_t1][1]+s1]
        # CASO IN CUI E' LA PRIMA VOLTA CHE VIENE INCONTRATA LA SQUADRA E IL RECORD VIENE CREATO
        else:
            score1 = [n_t1,s1]
        squadre.update({k_t1:score1})
        
        t2 = mI_rJ["team2"]
        k_t2 = t2["key"]
        n_t2 = t2["name"]
        s2 = mI_rJ["score2"] 
        if squadre.get(k_t2):
            score2 = [n_t2,squadre[k_t2][1]+s2]
        # CASO IN CUI E' LA PRIMA VOLTA CHE VIENE INCONTRATA LA SQUADRA E IL RECORD VIENE CREATO
        else:
            score2 = [n_t2,s2]
        squadre.update({k_t2:score2})
        
        check += s1+s2
        
print(squadre)
print(check)


# OUTPUT IN COLONNE
c = 0
for s in squadre:
    spazi1 = spazi2 = ""
    for spazio in range(1,20-len(s)): spazi1 += " " 
    for spazio in range(1,30-len(squadre[s][0])): spazi2 += " " 
    c +=1    
    print(c,"\t",s,spazi1,squadre[s][0],spazi2,"Goals: ",squadre[s][1])

