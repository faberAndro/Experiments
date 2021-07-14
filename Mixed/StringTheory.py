# BISOGNA CERCARE DI RIFARLO USANDO SOLO REGULAR EXPRESSIONS.
# crea una stringa con:
'''
numero di vocali
numero di consonanti
frase invertita sia in lower and uppercase che in ordine delle parole
trattini inseriti tra una parola e l'altra
"pv" inserito prima di ogni vocale.
'''

import re

p = "Non Siamo ANGEls"

RegEx_n_c = "[bcdfhjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]"

letterSet = [x for x in p]
changeCase = []
for y in letterSet:
    if y == y.lower():
        changeCase.append(y.upper())
    elif y == y.upper():
        changeCase.append(y.lower())
invertedCase = ''.join(changeCase)
words = invertedCase.split()
l_w = len(words)
zeta0 = ''
for w in range(l_w):
    zeta0 += words[l_w-1-w]+" "
zeta = zeta0[0:len(zeta0)-1]

s = p.split()

vowels = re.findall("[aeiouAEIOU]",p)
b = []
k = []
i = 0
for v in vowels:
    if i == 0:
        b = p.split(vowels[0],1)
    else:        
        b = b[1].split(v,1)
    k.append(b[0])
    i += 1
k2 = b[1]
i = 0
z = []
for x in vowels:
    z.append(k[i])
    i += 1
    m = 'pv'+x
    z.append(m)
z.append(k2)
soluzione = ''.join(z)

nr_vowels = str(len(re.findall("[aeiouAEIOU]",p)))
nr_consonants = str(len(re.findall(RegEx_n_c,p)))
reversed_p_with_reversed_cases = zeta
every_word_in_p = '-'.join(s)
p_wpvith_inspvertpved_strpving_pv = soluzione

combined_queries = nr_vowels+' '+nr_consonants+'::'+reversed_p_with_reversed_cases+'::'+every_word_in_p+'::'+p_wpvith_inspvertpved_strpving_pv

nr_vowels = str(len(re.findall("[aeiouAEIOU]",p)))
nr_consonants = str(len(re.findall("[[a-z]--[aeiou]]",p)))
reversed_p_with_reversed_cases = re.sub('(\w+), (\w+)', '\\2, \\1', p)
every_word_in_p = re.sub("\s","-",p)
p_wpvith_inspvertpved_strpving_pv = re.sub("([aeiouAEIOU])","pv"+r'\1',p)

combined_queries_RegEx = nr_vowels+' '+nr_consonants+'::'+reversed_p_with_reversed_cases+'::'+every_word_in_p+'::'+p_wpvith_inspvertpved_strpving_pv

print(combined_queries)
print(combined_queries_RegEx)
