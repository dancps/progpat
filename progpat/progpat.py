#!/usr/bin/env python
'''
Programing Pattern

Author: Danilo C. P. dos Santos
'''
import os
import argparse
# Handle no termcolor
try:
    from termcolor import colored
except ImportError:
    def colored(a,*b,**c):
        return str(a)

def calls(msg_type):
    if(msg_type=="warning"): return "["+colored("!","yellow")+"]"
    elif(msg_type=="error"): return "["+colored("x","red")+"]"
    elif(msg_type=="message"): return "["+colored("~","cyan")+"]"
    elif(msg_type=="item"): return "["+colored("•","blue")+"]"

class PatternManager(object):
    def __init__(self):
        self.__patterns=None#self.load_patterns() #list of dicts dict with "path":"o path", "pattern_name","patern_object":self.Pattern type
        self.__main_pattern_path=os.path.realpath(os.path.join(os.path.dirname(__file__),"../patterns"))
        self.__pattern_path=[self.__main_pattern_path]
        self.__configs_path=os.path.realpath(os.path.join(os.path.dirname(__file__),"../.config"))
        self.__config()
        self.__update_patterns()

    def __update_patterns(self):
        self.__patterns = self.get_patterns()
        
    def __config(self): # checks if default config files are available
        if not os.path.isdir(self.__main_pattern_path):
            os.makedirs(self.__main_pattern_path)
            print(calls('warning'), "Pattern folder created.")
        if not os.path.isdir(self.__configs_path):
            os.makedirs(self.__configs_path)
            print(calls('warning'), "Config folder created.")
        if not os.path.isfile(os.path.join(self.__configs_path,"paths.cfg")):
            with open(os.path.join(self.__configs_path,"paths.cfg"), 'w') as fl:
                print(calls('warning'), "Config file created.")
        with open(os.path.join(self.__configs_path,"paths.cfg"), 'r') as fl:
            for p in fl.readlines():
                if os.path.isdir(p.strip()) and p.strip() not in self.__pattern_path:
                    self.__pattern_path.append(p.strip()) 

            
    def add_pattern_path(self,path):
        if(os.path.isdir(path)):
            if path in self.__pattern_path:
                print(calls('error'),"The folder {} was already added.".format(colored(path,"red")))
            else:
                self.__pattern_path.append(path)
                with open(os.path.join(self.__configs_path,"paths.cfg"), 'a') as fl:
                    fl.write(path+"\n")
                self.__update_patterns()
        else:
            print(calls('error'),"This path doesn\'t exist.")

    def remove_pattern_path(self,path):
        if(os.path.isdir(path)):
            if path in self.__pattern_path:
                if path!=self.__main_pattern_path:
                    print(calls("message"),"Removing {} from cfg.".format(colored(path,attrs=["bold"])))
                    lines = []
                    with open(os.path.join(self.__configs_path,"paths.cfg"), 'r') as fl:
                        lines = [li.strip() for li in fl.readlines()]
                    lines.remove(path)
                    with open(os.path.join(self.__configs_path,"paths.cfg"), 'w') as fl:
                        for li in lines:
                            fl.write(li+"\n")
                else:
                    print(calls("error"),"Cannot remove {} from cfg.".format(colored(path,attrs=["bold"])))
        else:
            print(calls("error"),"The folder {} doesn't exists.".format(colored(path,attrs=["bold"])))


    def show_pattern_path(self):
        print("{}".format(colored("Pattern Paths:",attrs=["bold"])))
        for idx, path in enumerate(self.__pattern_path):
            print("  {}. {}".format(colored(idx,attrs=["bold"]),path))

    def get_patterns(self):
        pats = {}
        for path in self.__pattern_path:
            for file in sorted(os.listdir(path)):
                if file.endswith(".pat"):
                    file_p = os.path.join(path,file)
                    pat = Pattern(file_p)
                    pat_dict = {'path':file_p,
                                "pattern_name":pat.get_header(),
                                "pattern":pat,
                                "obs":""}
                    pat_name = os.path.splitext(file)[0]
                    if pat_name in pats:
                        count = 1
                        while not "_".join([pat_name,str(count)]) in pats:
                            pat_dict["obs"] = "({})".format(file_p)
                            pats["_".join([pat_name,str(count)])] = pat_dict
                    else:
                        pats[os.path.splitext(file)[0]] = pat_dict
        return pats

    def list_patterns(self):
        print(calls("message"),"{}".format(colored("Available patterns:",attrs=["bold"])))
        for idx,pat in enumerate(self.__patterns):
            print("  {}. {} {}".format(colored(idx,attrs=["bold"]),pat,self.__patterns[pat]["obs"]))

    def show_pattern(self,pattern):
        if pattern in self.__patterns:
            self.__patterns[pattern]["pattern"].print()
        else:
            print(calls("error"),"This pattern doesn\'t exists.")
            raise ValueError("This pattern doesn\'t exists.")

class Pattern(object):
    def __init__(self,file_path):
        self.__header = None#TODO: "# tmux" e "#tmux" devem ser iguais
        self.__subheader_delimiter = "%" # mesmo da acima
        self.__text_ident = 4
        self.__lines = None
        self.__process_file(file_path)

    def __process_file(self,path):
        with open(path,'r') as fl:
            first_line = fl.readline()
            if(first_line.startswith("#")):
                self.__header = first_line[1:].lstrip().strip("\n")
            else:
                self.__header = "Untitled pattern"
            self.__lines = [self.__process_line(line,delimiter=self.__subheader_delimiter) for line in fl.readlines()]

    def __process_line(self,line,delimiter):
        if line.startswith(delimiter):
            return " "+calls("item")+" "+colored(line[1:].lstrip().strip("\n"),attrs=["bold"])
        else:
            return " "*self.__text_ident+line.strip("\n")

    def get_header(self):
        return self.__header
    
    def get_subheaders(self): #TODO
        pass

    def print(self):
        print(calls("message"),colored(self.__header,"cyan",attrs=["bold"])+":")
        for line in self.__lines:
            print(line)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some snippets.')
    parser.add_argument('command', type=str, nargs='*',help='chooses which command to use.(show,list,add-path,list-path,rm-path)')
    args = parser.parse_args()
    if(args.command==[]): 
        parser.parse_args(["-h"])
    
    pmg = PatternManager()
    if(args.command[0]=="add-path"):
        for add in args.command[1:]:
            pmg.add_pattern_path(os.path.abspath(add))
    elif(args.command[0]=="list-path"):
        pmg.show_pattern_path()
    elif(args.command[0]=="rm-path"):
        for rm in args.command[1:]:
            pmg.remove_pattern_path(os.path.abspath(rm))
    elif(args.command[0]=="list"):
        pmg.list_patterns()
    elif(args.command[0]=="show"):
        for show_f in args.command[1:]:
            try:
                pmg.show_pattern(show_f)
            except ValueError:
                pass
    else:
        for show_f in args.command[0:]:
            try:
                pmg.show_pattern(show_f)
            except ValueError:
                print(calls("error"),"Wrong command")

    # For argparsing https://stackoverflow.com/questions/9729919/gem-git-style-command-line-arguments-in-python
if(__name__=="__main__"):
    main()
    