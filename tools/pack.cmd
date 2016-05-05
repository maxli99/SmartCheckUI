@echo off
@echo ...............................................

@set script_path=%~dp0
@cd %script_path%\..
call .\tools\pre_check.py
call pyinstaller --icon="nokia.ico" --hiddenimport _socket --hiddenimport flask_sqlalchemy  --exclude-module configparser -p libs -y --clean -d -c SmartCheckUI.py

del /s /q config\config.db
call .\tools\dbinit.py

@md dist\SmartCheckUI\templates
@md dist\SmartCheckUI\static
@md dist\SmartCheckUI\tmp
@md dist\SmartCheckUI\config
@md dist\SmartCheckUI\sc
@md dist\SmartCheckUI\extra_libs
@xcopy /E /y templates dist\SmartCheckUI\templates
@xcopy /E /y static dist\SmartCheckUI\static
@xcopy /E /y tmp dist\SmartCheckUI\tmp
@copy /y config\config.db dist\SmartCheckUI\config\config.db
@copy /y config\boot.json.sample dist\SmartCheckUI\config\boot.json
@xcopy /E /y sc dist\SmartCheckUI\sc
@xcopy /E /y extra_libs dist\SmartCheckUI\extra_libs
