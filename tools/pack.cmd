@echo off
@echo ...............................................

@set script_path=%~dp0
@cd %script_path%\..
call ..\tools\pre_check.py
call pyinstaller --icon="nokia.ico" -p libs -w SmartCheckUI.py
@md dist\SmartCheckUI\templates
md dist\SmartCheckUI\static
@md dist\SmartCheckUI\tmp
@md dist\SmartCheckUI\config
@xcopy /E /y templates dist\SmartCheckUI\templates
@xcopy /E /y static dist\SmartCheckUI\static
@xcopy /E /y tmp dist\SmartCheckUI\tmp
@copy /y config\config.ini.sample dist\SmartCheckUI\config\config.ini
@copy /y config\boot.json.sample dist\SmartCheckUI\config\boot.json
