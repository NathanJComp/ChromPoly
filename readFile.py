def readFile(file_name,mode=0):
    out_list=[]
    try:
        f=open(file_name,'r')
        for index,line in enumerate(f):
            if mode==1:
                out_list.append(line)
            else:
                line=line.split(':')
                #print(index,line)
                numbers=line[1].split()
                out_list.append([line[0],numbers])
        return out_list
    except IOError:
        print("file name not found")
    


