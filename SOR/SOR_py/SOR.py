import sys
from SORm import SOread

sarg = sys.argv[1].split(".")

if sarg[len(sarg)-1] in [ "sorf", "sordf" ]:
    ocont = open(sys.argv[1], 'r').read()
    tsplitter = "/"
    if "\\" in sys.argv[1]: tsplitter  = "\\"
    objsname = (sys.argv[1].split(tsplitter)[len(sys.argv[1].split(tsplitter))-1]).split(".")[0]
    objs = SOread(objsname, ocont)
    try:
        if sys.argv[2] == "print":
            strobjs = str(objs).replace("{", "{\n").replace("}", "\n}\n").replace(", ", ",\n")
            while "{\n{" in strobjs or "}\n\n}" in strobjs or "{\n\n}" in strobjs or "}\n," in strobjs:
                strobjs = strobjs.replace("{\n{", "{{").replace("}\n\n}", "}}").replace("{\n\n}", "{}").replace("}\n,", "},")
            print(objsname + " = " + strobjs)
        elif sys.argv[2] == "tk":
            import tkinter as tk
            import tkinter.messagebox.showinfo as msg
            root = tk.Tk()
            def openobj(obj):
                for i, j in obj.items():
                    if i != "@FORM":
                        try:
                            print(obj)
                            print(j)
                            el = tk.Button( root, text = j["@FORM"]["display_name"], command = lambda j = j : openobj(j) )
                            try:
                                el["bg"] = j["@FORM"]["bg_color"]
                                el["fg"] = j["@FORM"]["fg_color"]
                            except:
                                try:
                                    el["bg"] = obj["@FORM"]["bg_color"]
                                    el["fg"] = obj["@FORM"]["fg_color"]
                                except:
                                    {}
                        except:
                            el = tk.Button( root, text = i, command = lambda i = i, j = j : msg( title=i, text=j ) )
                            try:
                                el["bg"] = obj["@FORM"]["bg_color"]
                                el["fg"] = obj["@FORM"]["fg_color"]
                            except:
                                {}
                        el.pack()
            openobj(obj)
            root.mainloop()
        elif sys.argv[2] == "test":
            for i, j in objs.items():
                print(j["@FORM"]["display_name"])
    except Exception as e:
        print(e)
if sarg[len(sarg)-1] in [ "nsorf", "sor2f" ]:
    print("NSOR is not ready")
