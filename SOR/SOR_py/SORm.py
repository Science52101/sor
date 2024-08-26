def SOread(objsname, ocont):
    ocont = (ocont.replace("-OBJ-", "-OBJ- ").replace("-FRM- <<", "-FRM- @FORM <<").replace("\n", " ")).strip()
    socont = ocont.split("** ")
    objs = {}
    for i in range(len(socont)):
        l, in_quotes, slice = [], False, ""
        for socontchar in socont[i]:
            if socontchar == '"': in_quotes = not in_quotes
            elif socontchar == ' ' and ( not in_quotes ) and slice: l.append(slice); slice = ""
            else: slice += socontchar
        if slice: l.append(slice)
        if l[0] == "OBJ":
            if l[2] == "<<":
                pf = "-"
                obj = objs[l[1]] = {}
                def aobjv(obj, l, pf):
                    for i in range(3, len(l)):
                        if str(pf+"----") in l[i] and not( str(pf+"-----") in l[i] ):
                            ovl = l[i].replace(pf+"----", "")
                            if l[i+1] in ["<-", "<-n", "<-num", "<-txt", "<-t", "<<"]:
                                i += 2
                                try:
                                    if l[i-1] in ["<-", "<-n", "<-num"]: obj[ovl] = eval(l[i])
                                except:
                                    obj[ovl] = str(l[i])
                                if l[i-1] in ["<-t", "<-txt"]: obj[ovl] = str(l[i])
                            else:
                                obj[ovl] = None
                        elif pf+"OBJ-" == l[i] and l[i+2] == "<<":
                            son = l[i+1]
                            sobj = obj[son] = {}
                            nl = []
                            for j in range(i, len(l)):
                                nl.append(l[j])
                            sobj = aobjv(sobj, nl, pf + "-----")
                        elif pf+"FRM-" == l[i] and l[i+2] == "<<":
                            ofn = l[i+1]
                            form = obj[ofn] = {}
                            nl = []
                            for j in range(i, len(l)):
                                nl.append(l[j])
                            form = aobjv(form, nl, pf + "-----")
                        elif str(pf+"-----") in l[i] or str(pf+"-OBJ-") in l[i] or str(pf+"-FRM-") in l[i]:
                            {}
                        elif "----" in l[i] or "-OBJ-" in l[i] or "-FRM-" in l[i]:
                            break
                    return obj
                obj = aobjv(obj, l, pf)
                if l[1] == objsname: objs = obj
            else:
                objs[l[1]] = {}
    return objs

