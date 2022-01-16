"""
This scripts computes the number of goals made from each team within the English Premier Leaugue 2014/15,
using a json file as a source of information.
"""

import json

file = 'football_matches_list.json'
f = open(file)
matches = f.read()
data = json.loads(matches)
teams = {}
check = 0
r = data["rounds"]

for i in r:
    rI = i
    m_rI = rI["matches"]
    for j in m_rI:
        mI_rJ = j
        t1 = mI_rJ["team1"]
        k_t1 = t1["key"]
        n_t1 = t1["name"]
        s1 = mI_rJ["score1"]
        if teams.get(k_t1):
            score1 = [n_t1, teams[k_t1][1] + s1]
        # IN THE FOLLOWING CASE: FIRST TIME A TEAM IS ENCOUNTERED AND A NEW RECORD IS GENERATED 
        else:
            score1 = [n_t1, s1]
        teams.update({k_t1: score1})
        t2 = mI_rJ["team2"]
        k_t2 = t2["key"]
        n_t2 = t2["name"]
        s2 = mI_rJ["score2"]
        if teams.get(k_t2):
            score2 = [n_t2, teams[k_t2][1] + s2]
        # IN THE FOLLOWING CASE: FIRST TIME A TEAM IS ENCOUNTERED AND A NEW RECORD IS GENERATED 
        else:
            score2 = [n_t2, s2]
        teams.update({k_t2: score2})
        check += s1 + s2
print(teams)
print(check)

# Output provided in column form
c = 0
for s in teams:
    spaces1 = spaces2 = ""
    for spaces_o in range(1, 20 - len(s)):
        spaces1 += " "
    for spaces_o in range(1, 30 - len(teams[s][0])):
        spaces2 += " "
    c += 1
    print(c, "\t", s, spaces1, teams[s][0], spaces2, "Goals: ", teams[s][1])
