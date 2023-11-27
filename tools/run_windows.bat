@REM Change into project directory
cd /D "%~dp0"

@REM Launch with Python
python3 ..\python\autoclass.py --display --camera_bounds="(150,60)(515,435)" --execute --camera_number=1