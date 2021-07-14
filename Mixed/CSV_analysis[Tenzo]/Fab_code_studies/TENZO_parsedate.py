import csv
import datetime

csv1 = 'c:\\Users\\FABBA\\Desktop\\Tenzo\\work_shifts.csv'
f = open(csv1)
with f as csv_file:   
    csv_reader = csv.reader(csv_file, delimiter=',')
        
    i = 0
    bh_i = []
    bh_f = []
    day =  []
    for row in csv_reader:
        if i==0:
            i=1
        else:    
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
                d=1
                day.append(True)
            else:
                day.append(False)
                print("whole day")
            # CONVERT EACH TIME IN HH:MM FORMAT
            if (s1l.isdigit()):
                s1l += ".00"
            if (s1r.isdigit()):
                s1r += ".00"
            
            if d==0:
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

                
            bh_i.append(s1l)
            bh_f.append(s1r)
            i +=1
            
k=0            
for j in bh_i:
    print(day[k],"  ",bh_i[k],"  ",bh_f[k])
    k +=1

        