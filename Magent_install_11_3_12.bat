ECHO OFF
IF EXIST "C:\Program Files (x86)\Mandiant\fireeyeagent.exe" goto 1
IF EXIST "C:\Program Files (x86)\FireEye Agent\fireeyeagent.exe" goto 1
IF EXIST "C:\Program Files\Mandiant\fireeyeagent.exe" goto 1
IF EXIST "C:\Program Files\FireEyeAgent\fireeyeagent.exe" goto 1
msiexec /i C:\Windows\AgentSetup_11.3.12_universal.msi /quiet TARGETDIR="%PROGRAMFILES%\FireEye Agent\" EXENAME="fireeyeagent.exe"
:1
EXIT
