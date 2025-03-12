@echo off
echo confirm=Are you sure you want to shutdown your computer? ( y / s / r  )
echo y: 		shutdown
echo s: 		sleep
echo r: 		restart
echo [other]:	quit script
set /p confirm=Your select: 
if /i "%confirm%" EQU "y" (
   shutdown -s -t 0
) 

if /i "%confirm%" EQU "s" (
   shutdown -h
) 


if /i "%confirm%" EQU "r" (
   shutdown -r -t 0
)