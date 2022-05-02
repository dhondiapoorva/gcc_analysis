from subprocess import PIPE, run
import subprocess
import os
import json
import pandas as pd

filename="reports/overall_analysis.txt"
proddebugfile="data/production_debug_statements.json"
prodassertfiles="data/production_assert_statements.json"
prodfilename="reports/overall_prod_analysis.txt"
testassertfile="data/test_assert_statements.json"
loctestassertfile="data/loc_assert_statements.json"


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout
	
def clone_repository():
    directories = os.listdir('./')
    
    if 'gcc' not in directories:
        print("Repo doesnot exist. Cloning GCC repo now ...")
        os.system('git clone https://github.com/gcc-mirror/gcc.git')
        print("Cloning repo done")

class TestFiles():
    
    def __init__(self):
        global total_testfiles,total_assertstmts
        #os.system("echo \"\nTotal Number of Test Files = \" >> ./reports/overall_analysis.txt")
        total_testfiles=out("find ./gcc/testsuite/ -type f | wc -l")
        total_assertstmts=out("grep -ER \"^[^#--/*//].*Assert.*\(.*\)\" ./gcc/testsuite/* | wc -l")
        # test_files_depth=out('find ./gcc/testsuite/ -maxdepth 1 -type d | while read -r dir; do printf "%s:\t" "$dir"; find "$dir" -type f | wc -l; done')
        # print(test_files_depth)
        self.testFilesAssert()
        
    def testFilesAssert(self):
        #global assert_statements
        #total_assert_statements=out('grep -EcoR "^[^#--/*//\"].*Assert.*\(.*\)" ./gcc/testsuite/* | grep -v :0 | wc -l')
        os.system('grep -EcoR \"^[^#--/*//].*Assert.*\(.*\)\" ./gcc/testsuite/* | grep -v :0 >> ./reports/assert_statements.txt');
        os.system('grep -EiRn \"^[^#--/*//].*Assert.*\(.*\)\" ./gcc/testsuite/* | cut -f1,2 -d: >> ./reports/loc_assert_statements.txt')
		#assert_statements=open('./reports/assert_statements.txt', 'r').read()
        self.generateReport()
        self.generate_json_data()

    def generate_json_data(self):
        dict1={}
        with open('./reports/assert_statements.txt','r') as fh:
            for line in fh:
                filename,count=line.strip().split(":")
                dict1[filename]=count
        os.makedirs(os.path.dirname(testassertfile), exist_ok=True)
        with open("./data/test_assert_statements.json", "w+") as fp:
              json.dump(dict1, fp,indent = 3, sort_keys = False)
              fp.close()
        dict2={}
        l2=[]
        with open('./reports/loc_assert_statements.txt','r') as fh:
            for l in fh:
                filename,linenumber=l.strip().split(":")
                if filename in dict2:
                   dict2[filename].append(linenumber)
                else:
                   dict2[filename]=[linenumber]
        with open("./data/loc_assert_statements.json", "w+") as fp:
              json.dump(dict2, fp,indent = 3, sort_keys = False)
              fp.close()
    		
    def generateReport(self):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open('./reports/overall_analysis.txt', "w+") as f:
            f.write("\nTotal Number of Test Files = " + str(total_testfiles))
            #f.write("\nTotal Test Files in each Module = " )
            #f.write(str(out('find ./gcc/testsuite/ -maxdepth 6 -type d | while read -r dir; do printf "%s:\t" "$dir"; find "$dir" -type f | wc -l; done')))
            f.write("\nTotal Number of Assert Statements in Test Files = " + str(total_assertstmts))
            #f.write("\nTotal Number of Test Files with Assert Statements = " +  str(assert_statements))       
            f.close()
    
class ProdFiles():
    def __init__(self):
        global total_prodfiles,total_prodassertstmts,total_proddebugstmts
        total_prodfiles=out("find ./ -not -path \"testsuite\" -type f | wc -l")
        total_prodassertstmts=out("grep -EiR --exclude-dir={testsuite,reports} \"^[^#--/*//].*Assert.*\(.*\)\" ./* | wc -l")
        total_proddebugstmts=out("grep -EiR --exclude-dir={testsuite,reports} \"^[^#--/*//].*debug.*\(.*\)\" ./* | wc -l")
        os.system('grep -EicoR --exclude-dir={testsuite,reports} \"^[^#--/*//].*Assert.*\(.*\)\" ./* | grep -v -e ":0" >> ./reports/prod_assert_statements.txt')
        os.system('grep -EicoR --exclude-dir={testsuite,reports} \"^[^#--/*//].*debug.*\(.*\)\" ./* | grep -v -e ":0" >> ./reports/prod_debug_statements.txt')
        os.system('grep -EiRn --exclude-dir={testsuite,reports} \"^[^#--/*//].*Assert.*\(.*\)\" ./* | cut -f1,2 -d: >> ./reports/loc_prod_assert_statements.txt')
        os.system('grep -EiRn --exclude-dir={testsuite,reports} \"^[^#--/*//].*debug.*\(.*\)\" ./* | cut -f1,2 -d: >> ./reports/loc_prod_debug_statements.txt')
        os.makedirs(os.path.dirname(prodfilename), exist_ok=True)
        os.makedirs(os.path.dirname(prodassertfiles), exist_ok=True)
        os.makedirs(os.path.dirname(proddebugfile), exist_ok=True)
        self.generateProdReport()
        self.generate_json_data()


    def generateProdReport(self):
        
        with open('./reports/overall_prod_analysis.txt', "w+") as fp:
            fp.write("\nTotal Number of Prod Files = " + str(total_prodfiles))
            fp.write("\nTotal Number of Assert Statements in Prod Files = " + str(total_prodassertstmts))
            fp.write("\nTotal Number of Debug Statements in Prod Files = " + str(total_proddebugstmts))
            fp.close()
            
    def generate_json_data(self):
        dict1={}
        with open('./reports/prod_assert_statements.txt','r') as fh:
            for line in fh:
                filename,count=line.strip().split(":")
                dict1[filename]=count
        with open("./data/production_assert_statements.json", "w+") as fp:
              json.dump(dict1, fp,indent = 3, sort_keys = False)
              fp.close()
        dict2={}
        with open('./reports/prod_debug_statements.txt','r') as fh:
            for line in fh:
                filename,count=line.strip().split(":")
                dict2[filename]=count
        with open("./data/production_debug_statements.json", "w+") as fp:
              json.dump(dict2, fp,indent = 3, sort_keys = False)
              fp.close()
        dict3={}
        l1=[]
        with open('./reports/loc_prod_assert_statements.txt','r') as fh:
            for l in fh:
                filename,linenumber=l.strip().split(":")
                if filename in dict3:
                   dict3[filename].append(linenumber)
                else:
                   dict3[filename]=[linenumber]
        with open("./data/loc_production_assert_statements.json", "w+") as fp:
              json.dump(dict3, fp,indent = 3, sort_keys = False)
              fp.close()
        dict4={}
        l2=[]
        with open('./reports/loc_prod_debug_statements.txt','r') as fh:
            for l in fh:
                filename,linenumber=l.strip().split(":")
                if filename in dict4:
                   dict4[filename].append(linenumber)
                else:
                   dict4[filename]=[linenumber]
        with open("./data/loc_production_debug_statements.json", "w+") as fp:
              json.dump(dict4, fp,indent = 3, sort_keys = False)
              fp.close()
        


if __name__=="__main__":
    #clone_repository()
    TestFiles()
    ProdFiles()
    exec(open("gen-figures.py").read())
        