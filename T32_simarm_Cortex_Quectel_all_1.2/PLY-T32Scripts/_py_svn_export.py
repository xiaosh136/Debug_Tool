# -*- coding: utf-8 -*-

import re
import os
import sys

if __name__=='__main__':
    arg_len = len(sys.argv)
    if arg_len>=3:
        remote_url=sys.argv[1]
        upgrade_dir=sys.argv[2]
        cmd='svn export '
        cmd+=remote_url
        cmd+=' '
        cmd+=upgrade_dir
        try :
            os.system(cmd)
        except :
            pass
        finally :
            pass
           