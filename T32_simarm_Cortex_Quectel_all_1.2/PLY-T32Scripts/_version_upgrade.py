# -*- coding: utf-8 -*-

import re
import os
import sys
import shutil

if __name__=='__main__':
    arg_len = len(sys.argv)
    if arg_len>=4:
        remote_url=sys.argv[1]
        download_dir=sys.argv[2]
        script_dir=sys.argv[3]
        
        # delete files in the download dir
        if os.path.exists(download_dir):
            del_list=os.listdir(download_dir)
            for f in del_list:
                file_path=os.path.join(download_dir,f)
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
                shutil.rmtree(download_dir, True)
            except :
                pass
            finally :
                pass
        
        # download
        cmd='svn export '
        cmd+=remote_url
        cmd+=' '
        cmd+=download_dir
        try :
            os.system(cmd)
        except :
            pass
        finally :
            pass
        
        # copy
        copy_list=os.listdir(download_dir)
        for f in copy_list:
            src_file_path=os.path.join(download_dir,f)
            dst_file_path=os.path.join(script_dir,f)
            try :
                if os.path.isfile(src_file_path):
                    shutil.copyfile(src_file_path, dst_file_path)
                elif os.path.isdir(src_file_path):
                    shutil.copytree(src_file_path, dst_file_path)
            except :
                pass
           
        # delete files in the download dir
        if os.path.exists(download_dir):
            del_list=os.listdir(download_dir)
            for f in del_list:
                file_path=os.path.join(download_dir,f)
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
                shutil.rmtree(download_dir, True)
            except :
                pass
            finally :
                pass