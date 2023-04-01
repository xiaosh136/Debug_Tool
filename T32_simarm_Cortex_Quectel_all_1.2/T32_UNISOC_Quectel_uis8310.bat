@echo off

echo=
echo start to parse com_EE_Hbuf.bin
echo=
eecontext.exe dump/com_EE_Hbuf.bin
echo=
echo Load Trace32

@REM start t32marm.exe -c config.t32, t117_simulator.cmm &

start t32marm.exe -c config.t32,PLY-T32Scripts/_menu_PLY.cmm &