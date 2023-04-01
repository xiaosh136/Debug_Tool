@echo off
if exist C:\Python27 (C:\Python27\python.exe %1 %2 %3 > %4) else (python %1 %2 %3 > %4)