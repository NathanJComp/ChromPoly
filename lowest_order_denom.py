import string
import os
import chrompolychunks2

#parses the file into lists of P-type polys, with lists hanging off them containing
#the triples of N, N, D associated with each P
def listify(f):
    list_of_polys=[]
    list_of_factored_polys=[]
    trans_table = {ord("("):None,ord(")"):None}
    d_count=1
    for line in f:
        #after this, the first character will be P, N or D
        line_list = line.split()
        poly_list = [x.translate(trans_table) for x in line_list[1].split(")(")]
        if line_list[0]=="P":
            list_of_polys.append([poly_list])
        else:
            list_of_polys[-1].append(poly_list)

    for item in list_of_polys:
       
        if any(isinstance(el, list) for el in item[1:]):
            list_of_factored_polys.append(item)
    return list_of_factored_polys
        



def main():
    f = open(os.getcwd()+"\\Results\\v2_order_7_lines_1to107.txt")
    list_of_polys= listify(f)
    #print(list_of_polys)
    for item in list_of_polys:
        print("P",item[0])
        for p in item[1:]:
            print(p)

    '''

    #get all files in cwd/results and place them in the list "filenames"
    cwd = os.getcwd()
    filenames = next(os.walk(cwd + "/Results"))[2]

    for file in filenames:
        f = open(file)
        list_of_polys = listify(f)

    '''





if __name__ == "__main__":
    main()