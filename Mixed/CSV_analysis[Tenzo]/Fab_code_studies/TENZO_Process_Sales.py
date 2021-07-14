import csv
import datetime

csv1 = 'c:\\Users\\FABBA\\Desktop\\Tenzo\\transactions.csv'

"""
print(f'Dataset is: {", ".join(row)}')
print(f'\t break interval: {row[0]} , during the shift from {row[3]} to {row[1]} , payrate: £{row[2]}/hr.')
print(f'Processed {line_count} lines.')
"""
# FATTO: aggiungere la correzione con i break times.
# trasformarlo in una funzione con "def" e "return"
# correggere l'input path per il format "\\" o "\". Fare due casi
# trova massimo e minimo degli orari di lavoro SOSTITUIRE CON UNA FINZIONE CHE CARICA IN UNA TUPLA I VALORI CONVERTITI E POI NE TROVA IL MASSIMO
# eliminare il bug delle ore 13.00

csv1 = path_to_csv
with open(csv1) as csv_file:   
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i==0:
            i=1
        elif i==1:
                earliest = datetime.datetime.strptime(row[1],'%H:%M') 
                latest   = datetime.datetime.strptime(row[1],'%H:%M')
                print(row[1])
                i +=1
        else:
                begin = datetime.datetime.strptime(row[1],'%H:%M') 
                end   = datetime.datetime.strptime(row[1],'%H:%M')
                print(row[1])
                if begin < earliest:
                   earliest = begin
                if end > latest:
                   latest = end
                i +=1
       
print("earliest start: ",earliest,  " latest finish: ",latest)

# costruisce il dizionario
# CALCOLARE GLI ORARI FRAZIONARI (FRAZIONI DI COSTO!!) EX.: 22.30. correggere sia per l'incipit che per la fine
# potrei includere tutte le vorking hours invece delle ore in cui si e' venduto

hi = int(earliest.strftime("%H"))
hf = int(latest.strftime("%H"))

working_hours = []
hourly_sales  = []
dict_sales    = {}

for j in range(hi, hf+1, 1):
    working_hours.append(j)
    hourly_sales.append(float(0))
print(working_hours,hourly_sales)

with open(csv1) as csv_file:   
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i==0:
            i=1
        else:
            ora = int(row[1][0:2])
            incasso =  float(row[0])            
            r = ora - working_hours[0] 
            hourly_sales[r] += incasso            
            i +=1

print(working_hours,hourly_sales)

for n in range(len(working_hours)):
    y = str(working_hours[n])+":00"
    dict_sales[y] = round(float(hourly_sales[n]),2)
print(dict_sales)
