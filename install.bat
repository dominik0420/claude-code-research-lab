@echo off
REM This script is no longer needed.
REM Setup is now: mv lab .claude (Mac/Linux) or Move-Item lab .claude (PowerShell)
REM See README.md for the full setup instructions.
echo See README.md -- setup is now a single rename: Move-Item lab .claude
exit /b 0
REM ---- old content below, kept for reference ----
REM This copies lab/ into .claude/ for Claude Code to recognize agents and commands.

echo ============================================
echo  Claude Code Research Lab — Install
echo ============================================

REM Create .claude directory structure
mkdir .claude 2>nul
mkdir .claude\agents 2>nul
mkdir .claude\commands 2>nul
mkdir .claude\docs 2>nul
mkdir .claude\docs\templates 2>nul
mkdir .claude\rules 2>nul

echo Copying agents...
copy /Y lab\agents\*.md .claude\agents\

echo Copying commands...
copy /Y lab\commands\*.md .claude\commands\

echo Copying docs...
copy /Y lab\docs\*.md .claude\docs\
copy /Y lab\docs\templates\*.md .claude\docs\templates\

echo Copying rules...
copy /Y lab\rules\*.md .claude\rules\

echo.
echo Creating project directory structure...

REM Research documents
mkdir research 2>nul
mkdir literature 2>nul
mkdir literature\papers 2>nul

REM Experiments
mkdir experiments 2>nul
mkdir experiments\specs 2>nul
mkdir experiments\configs 2>nul
mkdir experiments\results 2>nul

REM Code
mkdir src 2>nul
mkdir src\models 2>nul
mkdir src\data 2>nul
mkdir src\training 2>nul
mkdir src\evaluation 2>nul
mkdir src\utils 2>nul

REM Scripts
mkdir scripts 2>nul

REM Tests
mkdir tests 2>nul

REM Data
mkdir data 2>nul
mkdir data\raw 2>nul
mkdir data\processed 2>nul

REM Baselines
mkdir baselines 2>nul

REM Analysis
mkdir analysis 2>nul
mkdir analysis\outputs 2>nul
mkdir analysis\outputs\figures 2>nul
mkdir analysis\figures 2>nul

REM Papers
mkdir papers 2>nul
mkdir papers\drafts 2>nul

REM Production
mkdir production 2>nul
mkdir production\milestones 2>nul
mkdir production\sprints 2>nul
mkdir production\session-state 2>nul

echo.
echo Creating starter files...

REM research-log.md
if not exist research\research-log.md (
    echo # Research Log > research\research-log.md
    echo. >> research\research-log.md
    echo All significant decisions and pivots are logged here. >> research\research-log.md
    echo Use the template in .claude\docs\templates\research-log-entry.md >> research\research-log.md
)

REM session state
if not exist production\session-state\active.md (
    echo ## Current Focus > production\session-state\active.md
    echo New project — run /start to begin. >> production\session-state\active.md
)

echo.
echo ============================================
echo  Installation complete!
echo ============================================
echo.
echo Next steps:
echo   1. Open this folder in Claude Code (claude command from this directory)
echo   2. Run /start to begin your research project
echo   3. See .claude\docs\quick-start.md for the full guide
echo.
