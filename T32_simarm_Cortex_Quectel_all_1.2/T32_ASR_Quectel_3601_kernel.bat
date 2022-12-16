@echo off

echo=
echo start to parse com_EE_Hbuf.bin
echo=
eecontext.exe dump/com_EE_Hbuf.bin
echo=
echo Load Trace32

start t32marm.exe -c config.t32, 3601_kernel.cmm &