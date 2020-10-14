    #ismail Enes KIRLI 16401728  ödev01
import sys
tuple_list={}
for i in range(int(sys.argv[1])):
    x=input("ID, isim, soyisim ve yaş giriniz")
    user=x.split()
    ID= user[0]
    isim= user[1:-2][0]
    soyisim=user[-2]
    yas=user[-1]
    stringAd="".join(isim)
    if ID.isdigit() and stringAd.isalpha() and soyisim.isalpha() and yas.isdigit() :
        if ID not in tuple_list:
            tup = (stringAd,soyisim,yas)
            tuple_list[ID] = tup
        elif ID in tuple_list:
            ID=input("Girmiş olduğunuz id mevcut Yeni bir ıd giriniz")
            tup = (stringAd,soyisim,yas)
            tuple_list[ID] = tup

sortedTupleList = sorted(tuple_list.items() ,  key=lambda x: x[0])
print(sortedTupleList)