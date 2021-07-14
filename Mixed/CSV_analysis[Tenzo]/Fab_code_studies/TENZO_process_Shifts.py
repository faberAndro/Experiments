import csv
import datetime

csv1 = 'c:\\Users\\FABBA\\Desktop\\Tenzo\\work_shifts.csv'

"""
print(f'Dataset is: {", ".join(row)}')
print(f'\t break interval: {row[0]} , during the shift from {row[3]} to {row[1]} , payrate: £{row[2]}/hr.')
print(f'Processed {line_count} lines.')
"""
# FATTO --- aggiungere la correzione con i break times.
# FATTO --- trasformarlo in una funzione con "def" e "return"
# correggere l'input path per il format "\\" o "\". Fare due casi
# gestione degli errori

# trova massimo e minimo degli orari di lavoro SOSTITUIRE CON UNA FUNZIONE CHE CARICA IN UNA TUPLA I VALORI CONVERTITI E POI NE TROVA IL MASSIMO
# risoluzione dei bug
# prova con altri IDE's e/o shell

#csv1 = path_to_csv
f = open(csv1)
with f as csv_file:   
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i==0:
            i=1
        elif i==1:
                earliest = datetime.datetime.strptime(row[3],'%H:%M') 
                latest   = datetime.datetime.strptime(row[1],'%H:%M')
                print(row[3]+" "+row[1])
                i +=1
        else:
                begin = datetime.datetime.strptime(row[3],'%H:%M') 
                end   = datetime.datetime.strptime(row[1],'%H:%M')
                print(row[3]+" "+row[1])
                if begin < earliest:
                   earliest = begin
                if end > latest:
                   latest = end
                i +=1
       
print("earliest start: ",earliest,  " latest finish: ",latest)

# costruisce il dizionario
# CALCOLARE GLI ORARI FRAZIONARI (FRAZIONI DI COSTO!!) EX.: 22.30. correggere sia per l'incipit che per la fine

hi = int(earliest.strftime("%H"))
hf = int(latest.strftime("%H"))

working_hours = []
hourly_costs  = []
dict_costs    = {}

for j in range(hi, hf+1, 1):
    working_hours.append(j)
    hourly_costs.append(0)
print(working_hours,hourly_costs)

with open(csv1) as csv_file:   
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i==0:
            i=1
        else:
            inizio = int(row[3][0:2])
            costo =  int(row[2][0:2])
            fine =   int(row[1][0:2])
            print(inizio," ",fine," ",costo)
            
            for k in range(inizio, fine, 1):
                r = k - working_hours[0] 
                hourly_costs[r] += costo
                
            i +=1

print(working_hours,hourly_costs)
for n in range(len(working_hours)):
    y = str(working_hours[n])+":00"
    dict_costs[y] = float(hourly_costs[n])
print(dict_costs)

f.close()