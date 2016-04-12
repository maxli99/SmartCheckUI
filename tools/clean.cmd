@echo off
@echo ...............................................

@set script_path=%~dp0
@cd %script_path%\..
call tools\pre_clean.py .
del /s /q SmartCheckUI.spec
del /s /q dist build
rd /s /q dist build
