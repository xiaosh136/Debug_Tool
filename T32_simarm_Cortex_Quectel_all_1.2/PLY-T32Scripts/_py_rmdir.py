# -*- coding: utf-8 -*-

import re
import os
import sys
import shutil

if __name__=='__main__':
    arg_len = len(sys.argv)
    if arg_len>=2:
        dir=sys.argv[1]
        if os.path.exists(dir):
            del_list=os.listdir(dir)
            for f in del_list:
                file_path=os.path.join(dir,f)
                try :
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path, True)
                except :
                    pass
                finally :
                    pass
            try :
                shutil.rmtree(dir, True)
            except :
                pass
            finally :
                pass

