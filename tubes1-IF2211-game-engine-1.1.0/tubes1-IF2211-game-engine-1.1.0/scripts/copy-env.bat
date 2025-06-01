@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

for /d %%p in ("%SCRIPT_DIR%\..\packages\*") do (
  if exist "%%p\.env.defaults" (
    copy /y "%%p\.env.defaults" "%%p\.env"
    echo Copied "%%p\.env.defaults" to "%%p\.env"
  )
)

endlocal
