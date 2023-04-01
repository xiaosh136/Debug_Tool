# -*- coding: utf-8 -*-

import re
import os
import sys
import xml.etree.ElementTree as ET

class Allocinfo(object):

    def __init__(self,):
        pass 

    def Scan(self,XML_File):
        Result = {}
        Size = {}
        Entt = {}
        Tree = ET.ElementTree(file=XML_File)
        Root = Tree.getroot()
        for child in Root:
            for grandson in child:
                if grandson.tag=='item':
                    myFile = ''
                    myLine = ''
                    mySize = ''
                    myEntt = ''
                    for sub_elem in grandson.iter():
                        if sub_elem.tag=='file':
                            myFile = sub_elem.text
                        if sub_elem.tag=='line':
                            myLine = sub_elem.text
                        if sub_elem.tag=='size':
                            mySize = sub_elem.text
                        if sub_elem.tag=='entt':
                            myEntt = sub_elem.text
                    if myFile and myLine:
                        myKey   = myFile + '|' + myLine
                        myValue = Result.get(myKey,0)
                        myValue += 1
                        Result[myKey] = myValue
                        Size[myKey] = mySize
                        Entt[myKey] = myEntt
        Result = [{'Key':key,'Count':Result[key],'Size':Size[key],'Entity':Entt[key]} for key in Result.keys()]
        Result.sort(key=lambda s:s['Count'])
        Result.reverse()
        return Result
        
if __name__=='__main__':
    
    arg_len = len(sys.argv)
    if arg_len==3 or arg_len==4:
        xml_file = sys.argv[1]
        top_n    = sys.argv[2]
        all_flag = 0
        if arg_len==4 and sys.argv[3]=="all":
            all_flag = 1
        if top_n.isdigit():
            top_n = int(top_n)
            if os.path.exists(xml_file):
                a_obj = Allocinfo()
                Data  = a_obj.Scan(xml_file)
                if top_n<1:
                    top_n=1
                if top_n>len(Data):
                    print 'The data is too little!'
                    top_n = len(Data)
                if len(Data)>0:
                    if all_flag==0:
                        myData = Data[top_n-1]
                        # print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ':', myData['Count'], 'allocations'
                        # print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ',', myData['Entity'], ',', myData['Size'], ':', myData['Count'], 'allocations'
                        print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ',', myData['Entity'], ':', myData['Count'], 'allocations'
                    else:
                        for i in range (1, top_n+1):
                            myData = Data[i-1]
                            # print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ':', myData['Count'], 'allocations'
                            # print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ',', myData['Entity'], ',', myData['Size'], ':', myData['Count'], 'allocations'
                            print myData['Key'].split('|')[0],'(', myData['Key'].split('|')[1], ')', ',', myData['Entity'], ':', myData['Count'], 'allocations'
            else:
                print 'XML file does not exist!'
        else:
            print 'The parameter must be a number!'
            print r"Usage: python  ", sys.argv[0], " ./osa_tx_allocinfo_PS.xml 5"
    else:
        print r"Usage: python  ", sys.argv[0], " ./osa_tx_allocinfo_PS.xml 5"

    
    
        
           