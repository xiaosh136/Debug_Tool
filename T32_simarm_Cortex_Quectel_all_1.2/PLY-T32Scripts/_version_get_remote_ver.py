# -*- coding: utf-8 -*-

import re
import os
import sys
import xml.etree.ElementTree as ET

class SvnLogInfo(object):

    def __init__(self,):
        pass 

    def Scan(self,XML_File):
        Tree = ET.ElementTree(file=XML_File)
        Root = Tree.getroot()
        for LogEntry in Root.iter("logentry"):
            return LogEntry.attrib['revision']
        return ''
        
if __name__=='__main__':
    arg_len = len(sys.argv)
    if arg_len>=4:
        remote_url=sys.argv[1]
        log_xml_file=sys.argv[2]
        output_file=sys.argv[3]
        cmd='svn log '
        cmd+=remote_url
        cmd+=' --limit 1 --xml > '
        cmd+=log_xml_file
        try :
            os.system(cmd)
        except :
            pass
        finally :
            if os.path.exists(log_xml_file):
                a_obj = SvnLogInfo()
                Data  = a_obj.Scan(log_xml_file)
                if Data!="":
                    try :
                        f=open(output_file, 'w')
                        f.write (Data)
                        f.close()
                    except :
                        pass
                    finally :
                        pass
