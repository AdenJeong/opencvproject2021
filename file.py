f1= open('target1.txt','r')
f2=open('target2.txt','r')
f3=open('target3.txt','r')
f4=open('target4.txt','r')
final = open('final_target.txt','w')

list1 = []
a=f1.readlines()
b=f2.readlines()
c=f3.readlines()
d=f4.readlines()

list1=a+b+c+d
list2 = set(list1)
list1 = list(list2)
print(list1)

final.writelines(list1)