



def table(d) :
    header = ["param", "value"]
    a = max([len("param")]+[len(k) for k in d.keys()])+1
    b = max([len("value")]+[len(d[k]) for k in d.keys()])+1
    displaycol = lambda colname : str(colname).center( a," ")
    displayval = lambda v : str(v).ljust(b, " ")
    fillcol = lambda x : a*"-"
    fillval=  lambda x : b*"-"
    rows = []
    rows.append("|".join([ displaycol("param"), displayval("value")]))
    rows.append("+".join([ fillcol(""), fillval("")]))
    for k in d.keys() :
        rows.append("|".join([displaycol(k),displayval(d[k])]))

    return "\n"+"\n".join(["| "+r+" |" for r in rows])


if __name__=="__main__":
    print table({"a" : "xxx","c" : "ssssssssssss"})
