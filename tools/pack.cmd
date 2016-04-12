@echo off
@echo ...............................................

@set script_path=%~dp0
@cd %script_path%\..
call ..\tools\pre_check.py
call pyinstaller --icon="nokia.ico" -p libs -w SmartCheckUI.py
@md dist\SmartCheckUI\templates
md dist\SmartCheckUI\static
@md dist\SmartCheckUI\tmp
@xcopy /E /y templates dist\SmartCheckUI\templates
@xcopy /E /y static dist\SmartCheckUI\static
@xcopy /E /y tmp dist\SmartCheckUI\tmp
