f = open("D:\\work\\trainc\\get_off_all.txt", 'r')
f2 = open("D:\\work\\trainc\\get_off_notframe.txt", 'w')
notframe=set()
while True:
    line = f.readline()
    if not line: break
    # line
    # print(line)
    # print()
    a = line.split("\\")[:-1]
    notframe.add("\\".join(a))

f.close()

print(len(notframe))

for i in notframe:
    label_one_path = i +"\n"
    f2.write(label_one_path)

f2.close()