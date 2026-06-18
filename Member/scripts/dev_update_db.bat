set localpath=%~dp0
cd /d %localpath%

if exist "..\data\*.db" del "..\data\*.db"
if exist "..\data\run.log" del "..\data\run.log"
if exist "config.json" del "config.json"

python init.py

python info_enter.py 103494770 醒刃拂尘
python info_modify.py 103494770 --time 2025-07-08 --landforce C --airforce C --navy U

python info_enter.py 186714697 MirageStar
python info_modify.py 186714697 --time 2026-05-23 --landforce C --airforce U --navy U

python info_enter.py 155534136 Nedisk

python info_lookup.py --all