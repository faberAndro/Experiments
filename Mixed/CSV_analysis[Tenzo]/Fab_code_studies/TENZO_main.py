# eliminare i print e i commenti inutili. Eliminare le parole in italiano.
# RIFARE LA FUNZIONE BEST AND WORST
import csv
import datetime

"""
Please write you name here: Fabrizio Bernini
"""
# PARSE THE BREAK INTERVAL NOTES
def calculate_breaks(row):
       
            pml = pmr = d = 0
            s0 = "".join(row[0].split()) # erase all whitespaces
            print(s0)
            sp = s0.split("-")
            s1l = sp[0]
            s1r = sp[1]         
            if s1l.find("PM")!=-1:
                s1l = s1l.replace("PM","")
                pml = 1
                print("replacement: "+s1l)
            if s1r.find("PM")!=-1:
                s1r = s1r.replace("PM","")
                pmr = 1
                print("replacement: "+s1r)
            if (s1l.isalpha() or s1r.isalpha()): # CHECK IF THERE IS A DAY
                d=True
            else:
                d=False
                print("whole day")
            # CONVERT EACH TIME IN HH:MM FORMAT
            if (s1l.isdigit()):
                s1l += ".00"
            if (s1r.isdigit()):
                s1r += ".00"
            
            if not(d):
                s2l = s1l.split(".")
                s3l = int(s2l[0])
                s2r = s1r.split(".")
                s3r = int(s2r[0])
                if (pml==1 or ((pmr==1) and (s3r<=s3l))):
                    s4l = s3l+12
                    s1l = s1l.replace(str(s3l),str(s4l))
                if (pmr==1):
                    s4r = s3r+12
                    s1r = s1r.replace(str(s3r),str(s4r))
    
            values = [d, s1l, s1r]
            return values


def process_shifts(path_to_csv):
    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """
    # 1. CALCULATE EARLIEST AND LATEST WORKING HOURS
    csv1 = path_to_csv
    f1 = open(csv1)
    with f1 as csv_file:   
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
           
    hi = int(earliest.strftime("%H")) # INITIAL NUMERIC WORKING HOUR
    hf = int(latest.strftime("%H"))   # FINAL NUMERIC WORKING HOUR
#   print("earliest start: ",earliest,  " latest finish: ",latest)

    # 2. CALCULATE HOURLY COSTS WITHOUT CONSIDERING BREAKS 
    working_hours = []
    hourly_costs  = []
    dict_costs    = {}

    for j in range(hi, hf+1, 1):
        working_hours.append(j)
        hourly_costs.append(0)
    print(working_hours,hourly_costs)
    
    f1 = open(csv1)
    with f1 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if i==0:
                i=1
            else:
                costo_inizio_fraz = 0
                costo_fine_fraz = 0
                
                costo =  int(row[2][0:2])
                
                inizio = int(row[3][0:2])
                minuti_inizio = int(row[3][4:6])
                if minuti_inizio > 0:
                    costo_inizio_fraz = costo*(minuti_inizio/60) 
                
                fine =   int(row[1][0:2])
                minuti_fine = int(row[1][4:6])
                if minuti_fine > 0:
                    fine +=1
                    costo_fine_fraz = costo*(minuti_fine/60) 
                
               # print(inizio," ",fine," ",costo)
                hourly_costs[inizio-working_hours[0]] = -costo_inizio_fraz
                for k in range(inizio, fine, 1):
                    r = k - working_hours[0] 
                    hourly_costs[r] += costo
                hourly_costs[r] += costo_fine_fraz

                i +=1
    f1.close()
    print(working_hours,hourly_costs)

    # 3. SUBTRACT BREAKS' COSTS
    f1 = open(csv1)
    with f1 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i=0
        for row in csv_reader:
             if i==0:
                i=1
             else:
                pause = calculate_breaks(row)
                if not(pause[0]):
                    costo_inizio_fraz = 0
                    costo_fine_fraz = 0
                    costo =  int(row[2][0:2])                
                    inizio = int(pause[1][0:2])
                    minuti_inizio = int(pause[1][4:6])
                    if minuti_inizio > 0:
                        costo_inizio_fraz = costo*(minuti_inizio/60)                 
                    fine =   int(pause[2][0:2])
                    minuti_fine = int(pause[2][4:6])
                    if minuti_fine > 0:
                        fine +=1
                        costo_fine_fraz = costo*(minuti_fine/60) 
                    # print(inizio," ",fine," ",costo)
                    hourly_costs[inizio-working_hours[0]] += +costo_inizio_fraz
                    for k in range(inizio, fine, 1):
                        r = k - working_hours[0] 
                        hourly_costs[r] -= costo
                    hourly_costs[r] -= costo_fine_fraz
                i +=1
    f1.close()
    
    # 4. BUILD THE COST DICTIONARY
    for n in range(len(working_hours)):
        y = str(working_hours[n])+":00"
        dict_costs[y] = float(hourly_costs[n])
    
    print("COSTI: ------")
    for pp1 in dict_costs:
        print(pp1, " ", dict_costs[pp1])

    return dict_costs


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """
    csv2 = path_to_csv
    f2 = open(csv2)
    with f2 as csv_file:   
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

    # potrei includere tutte le working hours invece delle ore in cui si e' venduto

    hi = int(earliest.strftime("%H"))
    hf = int(latest.strftime("%H"))

    working_hours = []
    hourly_sales  = []
    dict_sales    = {}

    for j in range(hi, hf+1, 1):
        working_hours.append(j)
        hourly_sales.append(float(0))
    print(working_hours,hourly_sales)
    
    f2 = open(csv2)
    with f2 as csv_file:   
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
    
    print("VENDITE! -----")
    for pp2 in dict_sales:
        print(pp2, " ", dict_sales[pp2]) 
    f2.close()
    return dict_sales

def compute_percentage(shifts, sales):
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """

    costi = shifts.copy()
    vendite = sales.copy()

    percentuali = {}
    for x in costi:
        if (float(costi[x])!= 0):
            if (x in vendite):
                if (float(vendite[x])!= 0):
                    o = round(100*(float(costi[x]) / float(vendite[x])),2)
                else:
                    o = - float(costi[x])
            else:
                o = - float(costi[x])
            percentuali[x] = o
        
    print("PERCENTUALI! ---")
    for pp3 in percentuali:
        print(pp3, " ", percentuali[pp3])
    return percentuali


def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """
    p = percentages.copy()
    # 1No. dictionary -> 4No. lists
    # NOTE: THIS OUTPUT DOES NOT MANAGE DUPLICATES
    hlist_p = []
    plist_p = []
    hlist_n = []
    plist_n = []
    for z in p:
        n = float(p[z])
        if n>0:
            plist_p.append(n)
            hlist_p.append(z)
        else:
            plist_n.append(n)
            hlist_n.append(z)
   
   
    if (len(plist_p)!=0):    # the list is not empty -> there is at least one hour where sth has been sold
        best = min(plist_p)
        bh = hlist_p[plist_p.index(best)]
    else:                    # no sales at all during the day
        best = max(plist_n)
        bh = hlist_n[plist_n.index(best)]

    if (len(plist_n)!=0):    # there are hours with no sales
        worst = min(plist_n) 
        wh = hlist_n[plist_n.index(worst)]
    else:
        worst = max(plist_p) # every hours there is at least one sale
        wh = hlist_n[plist_n.index(worst)]
                   
    
    """
    # TRANSFORM THAT IN A LIST!! OTHERWISE WILL BE DIFFICULT!!
    # "0" CANNOT EXIST FOR COSTS
    first_n = first_p = b = w = 0
    # FIND FIRST POSITIVE AND NEGATIVE VALUE
    for z in p:
        n = float(p[z])
        if (n>0):
            first_p = n
            bh = z   
        if (n<0):
            first_n = n
            wh = z
    b = first_p
    w = first_n
    # BEST HOUR CALCS
    # BEST case 1: NO SALES FOR THE WHOLE DAY (= no positive values = no sales at all)
    if (b == 0):
        for z in p:
            n = float(p[z])
                if (n < 0):
                    if (abs(n) > b):
                        b = n
                        bh = z
    # BEST case 2: MIN OF POSITIVE VALUES
    elif (b > 0):
        for z in p:
            n = float(p[z])
                if (n>0):
                    if n < b:
                        b = n
                        bh = z
    # WORST HOUR CALCS
    # WORST case 1: MAX OF POSITIVE VALUES (= sales every single hour)
    if (w == 0):
        for z in p:
            n = float(p[z])
                if (n>0):
                    if n < w:
                        w = n
                        bh = z
    # WORST case 2: MIN OF NEGATIVE VALUES
    elif (w < 0):
        for z in p:
            n = float(p[z])
                if (n<0):
                    if n < w:
                        w = n
                        bh = z    
    """
    bew = [bh, wh]
    print(bew)
    return bew

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)

    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "c:\\Users\\FABBA\\Desktop\\Tenzo\\transactions.csv"
    path_to_shifts = "c:\\Users\\FABBA\\Desktop\\Tenzo\\work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)
    print(best_hour," ",worst_hour)

# Please write you name here: Fabrizio Bernini

