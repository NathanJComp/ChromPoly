from readFile import readFile

for i in range(4,11):
    file1  = readFile("completeGraphs\\cond"+str(i)+".txt",1)
    file2  = readFile("graphData\\CF_"+str(i)+"_Uniq.txt",1)

    pointer1=0
    pointer2=0
    out_list=[]
    #assuming sorted
    '''
    while pointer1<len(file1) and pointer2<len(file2):
        if file1[pointer1]!=file2[pointer2]:
            pointer1+=1
        else:
            out_list.append(file1[pointer1])
            pointer2+=1'''
    #unsorted
    set1 = set()
    for line in file1:
        #print(line)
        set1.add(str(line[1]))
    for line in file2:
        if str(line[1]) in set1:
            out_list.append(line.split(':'))

    f=open("completeCFintersection\\int"+str(i)+".txt",'w')
    for i,line in enumerate(out_list):
        #print(line)
        #print(line[0])
        #print(line[1])
        f.write(str(line[0]) + " : ")
        for number in line[1].split():
            try:
                f.write(str(int(number))+" ")
            except ValueError:
                print(line)
        if i!=len(out_list)-1:
            f.write("\n")