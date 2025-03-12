@echo off

echo Try to reboot explorer.exe to  slove Windows GUI crashed

taskkill /f /im explorer.exe

start explorer.exe