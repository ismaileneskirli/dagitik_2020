import csv
import operator
import numpy as np
import matplotlib.pyplot as plt

#csvfile = open("data\lab8_0.30-6.13-1.53.mbd","r")
filename =  "data\lab8_0.30-6.13-1.53.mbd"
w=100
rssi_counter=1
counter=0
counter2=0
counter3=0
counter4=0
counter5=0
counter6=0
counter7=0
counter8=0
sensor1 = []
sensor2 = []
sensor3 = []
sensor4 = []
sensor5 = []
sensor6 = []
sensor7 = []
sensor8 = []
rssi1 =[]
rssi2 =[]
rssi3 =[]
rssi4 =[]
rssi5 =[]
rssi6 =[]
rssi7 =[]
rssi8 =[]
timestamp1 = []
frekans1 =[]
frekans=0
j=0

with open(filename, 'r') as csvfile:
    reader = csv.reader(open("data\lab8_0.30-6.13-1.53.mbd"), delimiter=",")
    for row in csvfile: 
        fields = row.strip().split(",")
        if fields[2] == "f963ea9bb3ea"  and fields[1] == "001583e5b269":
            counter  += 1
            sensor1.append(fields[3])
            timestamp1.append(fields[0])
            if len(timestamp1) == 100:
                frekans = w/(float(timestamp1[-1]) - float(timestamp1[0]))
                frekans1.append(frekans)
                timestamp1.pop(0)
        if fields[2] == "f963ea9bb3ea"  and fields[1] == "001583e5a3c0":
            counter2  += 1
            sensor2.append(fields[3])
        if fields[2] == "f963ea9bb3ea"  and fields[1] == "001a7dda710b":
            counter3  += 1
            sensor3.append(fields[3])
        if fields[2] == "f963ea9bb3ea"  and fields[1] == "001583e5a5bd":
            counter4  += 1
            sensor4.append(fields[3]) ## ilk verici bitti
        if fields[2] == "e78f135624ce"  and fields[1] == "001583e5b269":
            counter5  += 1
            sensor5.append(fields[3])
        if fields[2] == "e78f135624ce"  and fields[1] == "001583e5a3c0":
            counter6  += 1
            sensor6.append(fields[3])
        if fields[2] == "e78f135624ce"  and fields[1] == "001a7dda710b":
            counter7  += 1
            sensor7.append(fields[3])
        if fields[2] == "e78f135624ce"  and fields[1] == "001583e5a5bd":
            counter8  += 1
            sensor8.append(fields[3])        
############################################### 1.ikili
print(str(counter) + " tane veri vardır")
x=sorted(sensor1)
#print(x)
print("En büyük ve en küçük veriler sırasıyla: "+ str(x[0]) +" "+ str(x[-1]))

for i in range(0,counter-1):
    if x[i] == x[i+1]:  
        rssi_counter +=1
        if i== counter-2:
            rssi1.append(rssi_counter)
    else:
        rssi1.append(rssi_counter)
        rssi_counter=1
        
       
temp=[]

for i in range(0,counter-1):
    if x[i] != x[i+1]:
        temp.append(int(x[i]))
        j += 1

temp.append(int(x[counter-1]))
j += 1

for i in range(0, j): 
    x.clear()
    x.append(temp[i])    
    
x= temp
print(frekans1)
print("1.Graph")
print(rssi1) 
print (x)  # (f963ea9bb3ea, 001583e5b269) sonu.

################################### 2.ikili
j=0

print(str(counter2) + " tane veri vardır")
x2=sorted(sensor2)
print("En büyük ve en küçük veriler sırasıyla: "+ str(x2[0]) +" "+ str(x2[-1]))

for i in range(0,counter2-1):
    if x2[i] == x2[i+1]:
        rssi_counter +=1
        if i== counter-2:
            rssi2.append(rssi_counter)
    else:
        rssi2.append(rssi_counter)
        rssi_counter=1
        
print(rssi2)        

temp2=[]

for i in range(0,counter2-1):
    if x2[i] != x2[i+1]:
        temp2.append(int(x2[i]))
        j += 1

temp2.append(int(x2[counter2-1]))
j += 1

for i in range(0, j): 
    x2.clear()
    x2.append(temp2[i])    
    
x2= temp2
print (x2)  # (f963ea9bb3ea, 001583e5a3c0) sonu.

############################ 3.ikili
j=0

print(str(counter3) + " tane veri vardır")
x3=sorted(sensor3)
print("En büyük ve en küçük veriler sırasıyla: "+ str(x3[0]) +" "+ str(x3[-1]))

for i in range(0,counter3-1):
    if x3[i] == x3[i+1]:
        rssi_counter +=1
        if i== counter3-2:
            rssi3.append(rssi_counter)
    else:
        rssi3.append(rssi_counter)
        rssi_counter=1
        
      

temp3=[]

for i in range(0,counter3-1):
    if x3[i] != x3[i+1]:
        temp3.append(int(x3[i]))
        j += 1

temp3.append(int(x3[counter3-1]))
j += 1

for i in range(0, j): 
    x3.clear()
    x3.append(temp3[i])    
    
x3= temp3
print("3.Graph")
print(rssi3) 
print (x3) 
#(f963ea9bb3ea, 001583e5a5bd) sonu.

############################################### 4.ikili

x4=sorted(sensor4)
j=0
for i in range(0,counter4-1):
    if x4[i] == x4[i+1]:
        rssi_counter +=1
        if i== counter4-2:
            rssi4.append(rssi_counter)
    else:
        rssi4.append(rssi_counter)
        rssi_counter=1   
                   
temp4=[]
for i in range(0,counter4-1):
    if x4[i] != x4[i+1]:
        temp4.append(int(x4[i]))
        j += 1
        
temp4.append(int(x4[counter4-1]))
j += 1

for i in range(0, j): 
    x4.clear()
    x4.append(temp4[i])    
    
x4= temp4
print("4.Graph")
print(rssi4) 
print (x4) 
# (f963ea9bb3ea, 001583e5b269) sonu.

############################################### 5.ikili

x5=sorted(sensor5)
j=0
for i in range(0,counter5-1):
    if x5[i] == x5[i+1]:
        rssi_counter +=1
        if i== counter5-2:
            rssi5.append(rssi_counter)
    else:
        rssi5.append(rssi_counter)
        rssi_counter=1   
                   
temp5=[]
for i in range(0,counter5-1):
    if x5[i] != x5[i+1]:
        temp5.append(int(x5[i]))
        j += 1
        
temp5.append(int(x5[counter5-1]))
j += 1

for i in range(0, j): 
    x5.clear()
    x5.append(temp5[i])    
    
x5= temp5
# (e78f135624ce, 001583e5b269) sonu

############################################### 6.ikili

x6=sorted(sensor6)
j=0
for i in range(0,counter6-1):
    if x6[i] == x6[i+1]:
        rssi_counter +=1
        if i== counter6-2:
            rssi6.append(rssi_counter)
    else:
        rssi6.append(rssi_counter)
        rssi_counter=1   
                   
temp6=[]
for i in range(0,counter6-1):
    if x6[i] != x6[i+1]:
        temp6.append(int(x6[i]))
        j += 1
        
temp6.append(int(x6[counter6-1]))
j += 1

for i in range(0, j): 
    x6.clear()
    x6.append(temp6[i])    
    
x6= temp6
# (e78f135624ce, 001583e5a3c0) sonu

############################################### 7.ikili

x7=sorted(sensor7)
j=0
for i in range(0,counter7-1):
    if x7[i] == x7[i+1]:
        rssi_counter +=1
        if i== counter7-2:
            rssi7.append(rssi_counter)
    else:
        rssi7.append(rssi_counter)
        rssi_counter=1   
                   
temp7=[]
for i in range(0,counter7-1):
    if x7[i] != x7[i+1]:
        temp7.append(int(x7[i]))
        j += 1
        
temp7.append(int(x7[counter7-1]))
j += 1

for i in range(0, j): 
    x7.clear()
    x7.append(temp7[i])    
    
x7= temp7
print("7.Graph")
print(rssi7) 
print (x7) 
# (f963ea9bb3ea, 001583e5b269) sonu.

############################################### 8.ikili

x8=sorted(sensor8)
j=0
for i in range(0,counter8-1):
    if x8[i] == x8[i+1]:
        rssi_counter +=1
        if i== counter8-2:
            rssi8.append(rssi_counter)
    else:
        rssi8.append(rssi_counter)
        rssi_counter=1   
                   
temp8=[]
for i in range(0,counter8-1):
    if x8[i] != x8[i+1]:
        temp8.append(int(x8[i]))
        j += 1
        
temp8.append(int(x8[counter8-1]))
j += 1

for i in range(0, j): 
    x8.clear()
    x8.append(temp8[i])    
    
x8= temp8
# (e78f135624ce, 001583e5a5bd) sonu

#1. figure burada oluşturuluyor 8 tane subplot alacak şekilde.
figure1 = plt.figure()
ax1= figure1.add_subplot(2,4,1)
ax2= figure1.add_subplot(2,4,2)
ax3= figure1.add_subplot(2,4,3)
ax4= figure1.add_subplot(2,4,4)
ax5= figure1.add_subplot(2,4,5)
ax6= figure1.add_subplot(2,4,6)
ax7= figure1.add_subplot(2,4,7)
ax8= figure1.add_subplot(2,4,8)
#1. subplot
ypos1 = np.arange(len(x))
ax1.bar(ypos1,rssi1)
ax1.set_title("(f963ea9bb3ea, 001583e5b269)")
ax1.set_xticks(ypos1, minor=False)
ax1.set_xticklabels(x, fontdict=None, minor=False)
#2. subplot.
ypos2 = np.arange(len(x2))
ax2.bar(ypos2,rssi2)
ax2.set_title("(f963ea9bb3ea, 001583e5a3c0)")
ax2.set_xticks(ypos2, minor=False)
ax2.set_xticklabels(x2, fontdict=None, minor=False)
#3. subplot
ypos3 = np.arange(len(x3))
ax3.bar(ypos3,rssi3)
ax3.set_title("(f963ea9bb3ea, 001a7dda710b)")
ax3.set_xticks(ypos3, minor=False)
ax3.set_xticklabels(x3, fontdict=None, minor=False)
#4. subplot
ypos4 = np.arange(len(x4))
ax4.bar(ypos4,rssi4)
ax4.set_title("(f963ea9bb3ea, 001583e5a5bd)")
ax4.set_xticks(ypos4, minor=False)
ax4.set_xticklabels(x4, fontdict=None, minor=False)
#5. subplot
ypos5 = np.arange(len(x5))
ax5.bar(ypos5,rssi5)
ax5.set_title("(e78f135624ce, 001583e5b269)")
ax5.set_xticks(ypos5, minor=False)
ax5.set_xticklabels(x5, fontdict=None, minor=False)

#6. subplot
ypos6 = np.arange(len(x6))
ax6.bar(ypos6,rssi6)
ax6.set_title("(e78f135624ce, 001583e5a3c0)")
ax6.set_xticks(ypos6, minor=False)
ax6.set_xticklabels(x6, fontdict=None, minor=False)
"""
#7. subplot
## BURADA BİR SIKINTI oldu total sayıları tutmasına rağmen  listelerdeki eleman sayısı nedense hep farklı çıktı.
ypos7 = np.arange(len(x7))
ax7.bar(ypos7,rssi7)
ax7.set_title("(e78f135624ce, 001a7dda710b)")
ax7.set_xticks(ypos7, minor=False)
ax7.set_xticklabels(x7, fontdict=None, minor=False)
"""
#8. subplot
ypos8 = np.arange(len(x8))
ax8.bar(ypos8,rssi8)
ax8.set_title("(e78f135624ce, 001583e5a5bd)")
ax8.set_xticks(ypos8, minor=False)
ax8.set_xticklabels(x8, fontdict=None, minor=False)


#1. figürün bastırılması. Rssi kısmı sonu
plt.show()

figure2 = plt.figure()
ypos9 = np.arange(len(frekans1))
