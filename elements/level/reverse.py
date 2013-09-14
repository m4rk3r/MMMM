
txt = open('0_1_1.txt').readlines()

tmp = []
for line in txt:
    tmp.append(list(line.replace('\n','')))
    
print tmp
print
for x in range(len(tmp)):
    tmp[x].reverse()
    tmp[x] = ''.join(tmp[x])+'\n'

test = open('test.txt','a')
test.writelines(tmp)