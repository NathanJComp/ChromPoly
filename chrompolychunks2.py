__author__ = 'Nathan'

#from sympy import *
from collections import Counter
from readFile import readFile
import re
import unittest
import time
#x = Symbol('x')

#takes a line from kerri's input .txt
#breaks a polynomial down into its factors, splits bracketed things, converts ^ to **
#also converts the strings into a format which can be "sympified", once sympyFormat() is run
def breakIntoFactors(poly):
    poly_list=re.findall("\((.*?)\)", poly)
    #for i in range(len(poly_list)):
        #poly_list[i]=poly_list[i].replace("^","**")
        #find all isntances of numbers followed by an x, insert a *
        #poly_list[i]=re.sub("(?<=\d)(?=x)","*",poly_list[i])
    return poly_list

#needs a list of factors
#joins a list of factors into a single poly which can be sympified
def sympyFormat(polyList):
    polyList=['('+x+')' for x in polyList]
    poly=''.join(polyList)
    return poly



#needs a list of factors
#takes a poly list (strings) and returns a list of all the non x-a factors
def get_interesting_factors(poly_list):
    interesting_factors=[]
    for factor in poly_list:
        #print(factor)
        if not re.match("^x(-\d+)?$",factor):
            interesting_factors.append(factor)
    return interesting_factors

#needs a sympy object
#returns the degree of the largest complete polynomial which divides poly
'''def hasComplete(poly):
    divides=True
    order=0
    while(divides):
        q,r=div(poly,x-order)
        if r!=0:
            divides=False
        else:
            order+=1
    return order'''
#returns a dictionary of the interesting factors,the polynomials with those factors
#polynomials are indexed by their order and then position in poly_list which is the same as their line number-1
#so a polynomial of degree 9 from line 1084 would be given the value of 91084

'''#takes lists of factors
#takes as input 3 polynomails and the set of all poly. The current "p", and a prospective H1 and H2. Determines if H1*H2/p is in the set
def existsDivisor(p,h1,h2,poly_dict):
    mult=poly_mult(h1,h2)
    denominator=poly_div(mult,p)
    denominator=sympyFormat(denominator)
    if denominator in poly_dict:
        pass'''



def poly_mult(h1,h2):
    mult=Counter()
    for factor in h1+h2:

        if factor in mult:
            mult[factor]+=1
        else:
            mult[factor]=1
    return mult
#note that numerator is a Counter, while d is simply a list of factors

def poly_div(numerator,d):
    for factor in d:
        if factor in numerator:
            if numerator[factor]>0:
                numerator[factor]-=1
            else:
                return False
        else:
            return False

    for factor,freq in list(numerator.items()):
        if freq==0:
            del numerator[factor]
    #makes a frozenSet out of factor:freq pairs
    dividend=frozenset(numerator.items())
    return dividend

def update_dict_of_interesting_factors(order,poly_list,factor_dict):

    for index,poly in enumerate(poly_list):
        if index%10000==0:
            print("updatingDict:",order,index)
        #get a list of the interesting factors of the current polynomial
        #print("d",poly[0])
        intersesting_factors=get_interesting_factors(poly[0])
        #print("i",intersesting_factors)
        for factor in intersesting_factors:
            if factor in factor_dict:
                current_associated_polys=factor_dict[factor]
                current_associated_polys.append(str(order)+':'+str(index+1))

                factor_dict[factor]=current_associated_polys
            else:
                factor_dict[factor]=[str(order)+':'+str(index+1)]

def backTrackMakeboringPolys(n,partialSol,factors,poly_list):
    if len(partialSol)==n-1:
        poly_list.append([n-1,partialSol])
        return poly_list
    else:
        next_factors=getNextFactors(partialSol,factors)
        for item in next_factors:
            partialSol.insert(-2,item)
            poly_list=backTrackMakeboringPolys(n,partialSol[::],factors,poly_list)
            partialSol.pop(-2)
    return poly_list

def getNextFactors(partialSol,poly_list):
    last=partialSol[-1]
    if last=='x':
        return ['x-1']

    last_constant=int(last[-1])
    return poly_list[last_constant-1:last_constant+1]

#makes all boring polynomials of degree n-1
def makeBoringPolys(n):
    factors=[]
    for i in range(1,n):
        factors.append('x-{0}'.format(i))
    #print(factors)
    partialSol=['x']
    poly_list=[]
    backTrackMakeboringPolys(n,partialSol,factors,poly_list)
    return poly_list

#returns the boring and interesting poly lists
def get_poly_lists(p,p_id,order,factor_dict,poly_lists):
    boring_polys=[]
    p_boring=False
    for i in range(2,order):
        boring_polys+=makeBoringPolys(i)
    #will store polynomials which share interesting factors with p
    interesting_polys=[]
    interesting_p_factors=get_interesting_factors(p)
    if len(interesting_p_factors)==0:
        p_boring=True
    '''print("all:")
    for x in poly_lists:
        print("list")
        for y in x:
            print("\t",y)'''

    for factor in interesting_p_factors:
        #look up polys which share that factor
        common_factor_list=factor_dict[factor]
        for poly_id in common_factor_list:
            #print("id of current:",p_id, "id of candidate:", poly_id)
            if str(poly_id) != str(p_id):
                #print(poly_id)
                poly_id=poly_id.split(':')
                degree=int(poly_id[0])
                if degree<order:

                    line_num=int(poly_id[1])
                    #print(degree)
                    poly=poly_lists[degree-1][line_num-1]
                    interesting_polys.append([degree,poly])
    return boring_polys,interesting_polys,p_boring

def frozenlist_to_normal_list(d):
    out=[]
    for factor in d:
        for i in range(factor[1]):
            out.append(factor[0])
    return out


def display_results(h1,h2,d,out_f,list_of_lists_of_input_lines,poly_dict):
    #print("h1",h1)
    #print("h2",h2)
    out_f.write(" N ")
    h1_lookup=frozenset(Counter(h1).items())
    h1_printable=sympyFormat(h1)
    if h1_lookup in poly_dict:
        h1_graph_numbers=poly_dict[h1_lookup]
        out_f.write(h1_printable+" : " + " ".join(h1_graph_numbers)+"\n")
    else:
        out_f.write(h1_printable+" : " + "boring\n")

    out_f.write(" N ")

    h2_lookup=frozenset(Counter(h2).items())

    h2_printable=sympyFormat(h2)

    if h2_lookup in poly_dict:
        h2_graph_numbers=poly_dict[h2_lookup]
        #print("h2",h2_graph_numbers)
        out_f.write(h2_printable+" : " + " ".join(h2_graph_numbers)+"\n")
    else:
        out_f.write(h2_printable+" : " + "boring\n")


    out_f.write("  D ")
    list_d=list(d)

    convertable_d=frozenlist_to_normal_list(d)

    printable_d=sympyFormat(convertable_d)
    #figure out how to sort these into the right format
    d_graph_numbers=poly_dict[d]
    out_f.write(printable_d + " : " + " ".join(d_graph_numbers)+"\n")
    #d_printable=sympyFormat(list_d)
    #out_f.write(d_printable)

#determins if a polynomial is complete
def is_complete(p):
    #print(p)
    p=frozenlist_to_normal_list(p)
    #print(p)
    if not "x" in p:
        return False
    for i in range(1,len(p)):
        if not "x-{0}".format(i) in p:
            return False
    return True


def look_through_pairs(list1,list2,p_degree,same_list,p,poly_dict,out_f,list_of_lists_of_input_lines,found_factorisation,p_string):
    if same_list:
        for i in range(len(list1)):
            for j in range(i,len(list2)):
                
                if list2[j][0]>p_degree-list1[i][0] :
                    numerator=poly_mult(list1[i][1],list2[j][1])
                    candidate=poly_div(numerator,p)
                    if candidate:
                        #print("a",candidate)
                        if not is_complete(candidate):
                            if candidate in poly_dict:
                                if not found_factorisation:
                                    #out_f.write(p_string)
                                    found_factorisation=True
                                display_results(list1[i][1],list2[j][1],candidate,out_f,list_of_lists_of_input_lines,poly_dict)
    else:
        for poly1 in list1:
            for poly2 in list2:
                if poly1[0]>p_degree-poly2[0]:
                    numerator=poly_mult(poly1[1],poly2[1])
                    candidate=poly_div(numerator,p)
                    if candidate:
                        #print("b",candidate)
                        if not is_complete(candidate):

                            if candidate in poly_dict:
                                if not found_factorisation:
                                    #out_f.write(p_string)
                                    found_factorisation=True
                                display_results(poly1[1],poly2[1],candidate,out_f,list_of_lists_of_input_lines,poly_dict)



def main():
    #mult=poly_mult(['x-3','x-1'],['x-2','x**2-4*x+5','x','x-7'])
    #print(mult)
    #mult_after_div = poly_div(mult,['x-7'])
    #print(mult_after_div)
    list_of_lists_of_input_lines=[]

    start_time=time.time()
    poly_dict={}
    factor_dict={}
    poly_lists=[]
    order=int(input("please enter the order"))
    #get all the polynomials of order < the given order we are looking at
    for i in range(1,order):
        file_name="graphData\\cf_"+str(i)+"_uniq.txt"
        list_of_input_lines = readFile(file_name)
        list_of_lists_of_input_lines.append(list_of_input_lines)
        #print(list_of_lists_of_input_lines)
        for j in range(len(list_of_input_lines)):
            if j%10000==0:
                print("file:",i,"line:",j)
            list_of_input_lines[j][0] = breakIntoFactors(list_of_input_lines[j][0])
            current_poly=list_of_input_lines[j][0]
            # we need to assocaite the polys with thier graph numbers for output purposes
            proper_poly_graphs=list_of_input_lines[j][1]
            proper_poly_graphs=tuple(proper_poly_graphs)
            #makes a frozenSet out of factor:freq pairs
            proper_poly=frozenset(Counter(current_poly).items())
            poly_dict[proper_poly]=proper_poly_graphs
        #updates the factor dictionary with all the polys of this order

        poly_lists.append([line[0] for line in list_of_input_lines])
        update_dict_of_interesting_factors(i,list_of_input_lines,factor_dict)

    #get the polynomials of the order we want to factorise
    file_name="completeCfIntersection\\int"+str(order)+".txt"
    list_of_input_lines = readFile(file_name)
    list_of_lists_of_input_lines.append(list_of_input_lines)
    #print(list_of_lists_of_input_lines)
    for j in range(len(list_of_input_lines)):
        if j%10000==0:
            print("file:",order,"line:",j)
        list_of_input_lines[j][0] = breakIntoFactors(list_of_input_lines[j][0])
        current_poly=list_of_input_lines[j][0]
        # we need to assocaite the polys with thier graph numbers for output purposes
        proper_poly_graphs=list_of_input_lines[j][1]
        proper_poly_graphs=tuple(proper_poly_graphs)
        #makes a frozenSet out of factor:freq pairs
        proper_poly=frozenset(Counter(current_poly).items())
        poly_dict[proper_poly]=proper_poly_graphs
    poly_lists.append([line[0] for line in list_of_input_lines])
    update_dict_of_interesting_factors(order,list_of_input_lines,factor_dict)
    #gets all the polynomials from the file, makes them into frozensets and puts them in a big set for lookup

    #makes a dictionary of the non (x-a) factors from the input polynomials

    '''for x in factor_dict:
        if len(factor_dict[x])>1:
            print(factor_dict[x])'''
    '''for poly in poly_dict:
        print(poly)'''
    
    print(time.time()-start_time)
    #start=0
    #stop=999
    valid_inputs=False
    while not valid_inputs:
        try:
            start=int(input("please enter a start value\n"))
            stop=input("please enter an end value (press enter for all)\n")
            chunk_len = input("please enter a chunk length (enter for unlimited) \n")
            if stop == "":
                stop = int(len(list_of_input_lines))
            else:
                stop=int(stop)
            if chunk_len == "":
                chukn_len=False
            else:
                chunk_len=int(chunk_len)
            
            if start>=1 and start<=stop:
                valid_inputs=True
            else:
                print("ensure start>=0 and start>=stop")
        except ValueError:
            print("please ensure you enter integers")

    #go through all the polynomials from start to stop in the input file
    #print([line[0] for line in list_of_input_lines[start:stop]])
    #just loop through the polynomials from line start to line stop of input lines
    if chunk_len:
        chunks = (stop-(start-1))//chunk_len+1
    else:  
        chunks=1
        chunk_len=stop-(start-1)
    for i in range(chunks):
        out_f=open("Results//v2_order_"+str(order)+"_lines_"+str(start+i*chunk_len)+"to"+str(min(start+(i+1)*chunk_len-1,stop))+".txt",'w')
        #note that stop is not included
        
        
        #for index in range(len([line[0] for line in list_of_input_lines[start:stop]])):
        for index in range(start-1+i*chunk_len,min(start-1+(i+1)*chunk_len,stop)):
            #print(index)
            found_factorisation=False
            if index%10==0:
                print(index)
            line_num=index+1
            p_id=str(order)+':'+str(line_num)
            #print(p_id)
            p=list_of_input_lines[index][0]
            p_graph_numbers=list_of_input_lines[index][1]
            #out_f.write("$\n")
            #out_f.write("P ")
            printable_p=sympyFormat(p)
            #out_f.write(printable_p+ " : " + " ".join(p_graph_numbers))
            #out_f.write("\n")
            p_string="P "+printable_p + " : " + " ".join(p_graph_numbers)+"\n"
            out_f.write(p_string)
            #get the two lists of polynomials which could be h1 and h2
            # item in interesting_list and boring_list is a list.
            #first element is the degree, second is the poly
            boring_list,interesting_list,p_boring=get_poly_lists(p,p_id,order,factor_dict,poly_lists)
            #print("b",boring_list)
            #print("i",interesting_list)

            if p_boring:
                look_through_pairs(boring_list,boring_list,order,True,p,poly_dict,out_f,list_of_lists_of_input_lines,found_factorisation,p_string)
                #look through all pairs in the boring list
            else:
                #if there is nothing in interesting list, there are no polys with the same factors that p
                #had so we should not look for a factorisation
                if len(interesting_list)>0:
                    #look through boring/interesting pairs, and interesting interesting pairs

                    look_through_pairs(boring_list,interesting_list,order,False,p,poly_dict,out_f,list_of_lists_of_input_lines,found_factorisation,p_string)
                    look_through_pairs(interesting_list,interesting_list,order,True,p,poly_dict,out_f,list_of_lists_of_input_lines,found_factorisation,p_string)
            '''print("current p:",p)
            print("boring list:",boring_list)
            print("interesting list:" ,interesting_list)'''
    print(time.time()-start_time)

if __name__== "__main__":
    #p1="(x)(x-1)(x-2)(x-3)"
    #p2="(x)(x-1)(x-2)(x-3)(x-1)"
    #p1=breakIntoFactors(p1)
    #p2=breakIntoFactors(p2)
    #print(is_complete(p1))
    #print(is_complete(p2))
    main()
    close=input("press any key to close")