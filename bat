@Echo off

:m1
color 2
echo.
Echo 1 - Entering the Off Time
Echo 2 - Cancel off
echo.
echo.
Set /p choice="Choise: "
if not defined choice goto m1
if "%choice%"=="1" (goto m2)
if "%choice%"=="2" (shutdown -a)
goto m1


:m2
echo.
set /p kolvo_minut="Timer min: "
set/A kolvo_sekund=%kolvo_minut%*60
shutdown -s -f -t "%kolvo_sekund%"
goto m1


