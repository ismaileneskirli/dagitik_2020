    #ismail Enes KIRLI 16401728  odev02
import sys
new_dict = {} #dictionary'i init ediyorum.
file = open("airlines.txt","r")

def isPath(new_dict, start, end, path=[]):  # 2 düğüm arasında yol olup olmadığını gösteren boolean fonksiyon.
    for point in new_dict[start]:
        if point not in path:
            newpath = findPath(new_dict, point, end, path)
            if newpath:
                return True            
            else:
                return False

def findPath(new_dict, start, end, path=[]): # 2 düğüm arasındaki en kısa olası yolu döndüren recursive fonksiyon.
    path = path + [start]
    shortest_path =None
    if start == end: #recursive fonksiyonun bitiş kondisyonu.
        return path
    
    for point in new_dict[start]:
        if point not in path:
            newpath = findPath(new_dict, point, end, path)
            if newpath:
                if not shortest_path or len(newpath) < len(shortest_path):  # bulduğu yolları en kısa olan ile sürekli karşılaştırarak  en sonunda en kısa olanı döndürüyorum.
                    shortest_path=newpath
    return shortest_path
            

            
for line in file:  # okuma işlemini burada yapıp dict'e atamaları yapıyorum.
    fields = line.strip().split(",")
    new_dict[fields[0]]=fields[1:]

#print(new_dict)
if isPath(new_dict,sys.argv[1],sys.argv[2]): #yol var mı kontrolü
    print("Partnerlik ilişkisi vardır ve yol şu şekildedir ->"+ str(findPath(new_dict,sys.argv[1],sys.argv[2])))
else:
    print("Partnerlik ilişkisi yoktur.")
    
    
file.close()