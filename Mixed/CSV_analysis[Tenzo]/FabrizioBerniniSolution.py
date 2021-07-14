"""
Please write you name here: Fabrizio Bernini
"""

"""
-- ABOUT THIS CODE (by Fabrizio) --

CAPABILITIES AND EXCEPTIONS:
- it can work with any number of rows (data) in the excel files, provided that they are in the correct format
- it runs a consistency check on the excel data format and raise error messages in case of incorrect formats 
- it manages simple exceptions on opening files
(see function "exceptions(e)" in the code for more details)
- parameter "verbose" can be set to TRUE within "main", to show the software processing internal outputs (current value is FALSE)
- The implemented algorithm calculate the hourly costs considering the fraction of hours worked too (BOTH AT THE BEGINNING AND AT THE END OF THE SHIFTS) - in the present case, we have only 22.30 as non-integer hour - .

ASSUMPTIONS and CRITERIA: 
- within the break notes, dates (full days) are not considered (the are just skipped) and rather interpreted as no break on normal days.
- wages to employees are payed in any fraction of hour.
- payrates are always > 0

LIMITATIONS:
- In the unlikely case that BEST and/or WORST hours (the output) have duplicates, these are not managed by the program, as it returns only one of the values for each of them.
- The algorithm does not actually consider final working hours after 23:59.

* Note 1: Note on the percentage algorithm. The algorithm to calculated the percentage is approximate as:
the hourly cost is calculated on a hourly basis and not on fraction of hours. So, for example, the cost/income at 22.00pm does not account that in the second half of the hour there is a person less (the one working until 22.30pm), instead the income from 22.30 would appear to be linked to the cost of that person, even if the cash is received at 22.45.
A better algorith should consider this aspect

* Note 2: it is to be noted that, in this particular case, the result does not change considering or omitting the lunch breaks
"""

import csv
import datetime


def exceptions(e): # additional function with printed text list depending on the exception raised
    
    print("\n ******** ERROR ******** \n")
    if e==1:        
        print(" At least one of the following source files:\n\n","shifts data file -> ",path_to_shifts,"\n","sales data file -> ",path_to_sales,"\n")
        print(""" could not be opened.
              
            Please check that:
            - both files exist
            - both files are in the right location
            - the path you specified is correct
            - to have replaced the single slash '\' in the paths with the double one '\\', in order the path to be readable by python
                
            Then try again.
            Good luck! :))
        
            """)
    
    if e==2:
        print("""Please check the break notes:\n
        hours and times must be in one of the following formats:\n
        15.00
        15
        3PM
        
        Each note must contain only 2No. different times, separated by a dash '-'
        
        Please amend the source file and try again
        """)
    
    if e==3:
        print("""Please check the data format and consistency in the source files.\n
        Ensure that:\n
        - ALL TIMES (except for break notes) ARE IN THE FORMAT : HH:MM
        - EACH SHIFT END TIME IS MAJOR THAN ITS START TIME
        - EACH PAY RATE IS > 0 AND IN THE RIGHT FORMAT

        Then try again

        Thank you
        """)
        
    exit()



def parse_lunch_breaks(row):
# PARSE THE BREAK INTERVAL NOTES (additional function, to make the "process_shifts" lighter)
       
    try:
        pml = pmr = d = 0
        s0 = "".join(row[0].split()) # ERASE ALL WHITESPACES
        sp = s0.split("-")
        s1l = sp[0]
        s1r = sp[1]         
        if s1l.find("PM")!=-1:
            s1l = s1l.replace("PM","")
            pml = 1
        if s1r.find("PM")!=-1:
            s1r = s1r.replace("PM","")
            pmr = 1
        if (s1l.isalpha() or s1r.isalpha()): # CHECK IF THERE IS A DAY
            d=True
        else:
            d=False
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
    except:
        exceptions(2)
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
    csv1 = path_to_csv # variable added to grant future flexibility
    try:
        f1 = open(csv1)
    except:
        exceptions(1)
    
    # CHECK CONSISTENCY OF DATA:
    with f1 as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if (i>0): 
                try:
                    datetime.datetime.strptime(row[1], '%H:%M')
                    datetime.datetime.strptime(row[3], '%H:%M')
                    test = float(row[2])
                    if row[3] > row[1]: exceptions(3)
                    if (test <= 0): exceptions(3)
                except:
                    exceptions(3)
            i +=1
    f1.close()        
    # 1. CALCULATE EARLIEST AND LATEST WORKING HOURS        
    f1 = open(csv1)
    all_hours = []
    with f1 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        if verbose: print("SHIFTS ---")        
        for row in csv_reader:
            if (i>0):
                h1 = datetime.datetime.strptime(row[3],'%H:%M')
                h2 = datetime.datetime.strptime(row[1],'%H:%M')
                all_hours.extend([h1,h2])
                if verbose: print(row[3]," ",row[1])                
                
            i +=1
            
    earliest = min(all_hours)
    latest = max(all_hours)
    hi = int(earliest.strftime("%H")) # INITIAL NUMERIC WORKING HOUR
    hf = int(latest.strftime("%H"))   # FINAL NUMERIC WORKING HOUR

    # 2. CALCULATE HOURLY CUMULATIVE COSTS IN A FIRST INSTANCE WITHOUT CONSIDERING BREAKS 
    working_hours = []
    hourly_costs  = []
    dict_costs    = {}

    for j in range(hi, hf+1, 1):
        working_hours.append(j)
        hourly_costs.append(0)
    
    f1 = open(csv1)
    with f1 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if i>0:
                
                cost_init_frac = 0
                cost_end_frac = 0
                cost =  int(row[2][0:2])
                
                init = int(row[3][0:2])
                minutes_init = int(row[3][4:6])
                if minutes_init > 0:
                    cost_init_frac = cost*(minutes_init/60) 
                
                end = int(row[1][0:2])
                minutes_end = int(row[1][4:6])
                if minutes_end > 0:
                    end +=1
                    cost_end_frac = cost*(minutes_end/60) 
                
                hourly_costs[init-working_hours[0]] = -cost_init_frac
                for k in range(init, end, 1):
                    r = k - working_hours[0] 
                    hourly_costs[r] += cost
                hourly_costs[r] += cost_end_frac

            i +=1
    
    f1.close()
    if verbose: print("working hours vs. hourly costs: \n",working_hours,hourly_costs)

    # 3. SUBTRACT BREAKS' COSTS
    f1 = open(csv1)
    with f1 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i=0
        for row in csv_reader:
             if i>0:              
                pause = parse_lunch_breaks(row)
                if not(pause[0]):       # discards the annual leaves
                    
                    cost_init_frac = 0
                    cost_end_frac = 0
                    cost =  int(row[2][0:2])                
                    init = int(pause[1][0:2])
                    minutes_init = int(pause[1][4:6])
                    
                    if minutes_init > 0:
                        cost_init_frac = costo*(minutes_init/60)                 
                    end = int(pause[2][0:2])
                    minutes_end = int(pause[2][4:6])
                    
                    if minutes_end > 0:
                        end +=1
                        cost_end_frac = cost*(minutes_end/60) 
                    hourly_costs[init-working_hours[0]] += +cost_init_frac
                    
                    for k in range(init, end, 1):
                        r = k - working_hours[0] 
                        hourly_costs[r] -= cost
                    hourly_costs[r] -= cost_end_frac
             i +=1
    
    f1.close()
    
    # 4. BUILD THE COST DICTIONARY
    for n in range(len(working_hours)):
        y = str(working_hours[n])+":00"
        dict_costs[y] = float(hourly_costs[n])
    
    if verbose: 
        print("HOURLY COSTS: ------")
        for pp1 in dict_costs:
            if verbose: print(pp1, " ", dict_costs[pp1])

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
    # 1. CALCULATE MIN & MAX TIME
    all_times = []
    if verbose: print("SALES TIME!")
    csv2 = path_to_csv
    try:
        f2 = open(csv2)
    except:
        exceptions(1)
        
    # CHECK CONSISTENCY OF DATA:   
    with f2 as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if (i>0): 
                try:
                    datetime.datetime.strptime(row[1], '%H:%M')
                    test = float(row[0])
                    if (test <= 0): exceptions(3)
                except:
                    exceptions(3)
            i +=1
    f2.close()
    
    f2 = open(csv2)
    with f2 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if (i>0):
                h = datetime.datetime.strptime(row[1],'%H:%M')
                all_times.append(h)
            i +=1
    earliest = min(all_times)
    latest = max(all_times)   
    hi = int(earliest.strftime("%H"))
    hf = int(latest.strftime("%H"))
    if verbose: print("earliest start: ",earliest,  " latest finish: ",latest)
    
    # 2. CALCULATE THE CUMULATIVE HOURLY SALES
    working_hours = []
    hourly_sales  = []
    dict_sales    = {}

    for j in range(hi, hf+1, 1):
        working_hours.append(j)
        hourly_sales.append(float(0))
    
    f2 = open(csv2)
    with f2 as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if i==0:
                i=1
            else:
                ora = int(row[1][0:2])
                money =  float(row[0])            
                r = ora - working_hours[0] 
                hourly_sales[r] += money            
                i +=1

    # 3. BUILD THE "SALES" DICTIONARY
    for n in range(len(working_hours)):
        y = str(working_hours[n])+":00"
        dict_sales[y] = round(float(hourly_sales[n]),2)
    
    if verbose: print("SALES! -----")
    for pp2 in dict_sales:
        if verbose: print(pp2, " ", dict_sales[pp2]) 
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
    
    costs = shifts.copy()
    sales = sales.copy()

    percentages = {}
    for x in costs:
        if (float(costs[x])!= 0):
            if (x in sales):
                if (float(sales[x])!= 0):
                    o = round(100*(float(costs[x]) / float(sales[x])),2)
                else:
                    o = - float(costs[x])
            else:
                o = - float(costs[x])
            percentages[x] = o
        
    if verbose: 
        print("PERCENTAGES (c/s)! ---")
        for pp3 in percentages:
            print(pp3, " ", percentages[pp3])
    
    return percentages



def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """
    p = percentages.copy() # added variable 'p' for future flexibility
    # 1No. dictionary -> 4No. lists (: positive numbers,their hours,negative numbers,their hours)
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
                   
    bew = [bh, wh]
    if verbose: print("best and worst hours: ",bew)
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
    verbose = False
    path_to_sales = "c:\\Users\\FABBA\\Desktop\\Tenzo\\transactions.csv"
    path_to_shifts = "c:\\Users\\FABBA\\Desktop\\Tenzo\\work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)
    print(best_hour," ",worst_hour)

# Please write you name here: Fabrizio Bernini

