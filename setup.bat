@echo off
echo ======================================================================
echo BEYOND HUMAN PERCEPTION AUDIO ANALYZER
echo Automated Setup Script
echo ======================================================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo Step 2: Checking current setup...
python check_setup.py
if errorlevel 1 (
    echo.
    echo Step 3: Installing dependencies...
    echo This may take a few minutes...
    echo.
    
    choice /C YN /M "Install full dependencies (Y) or minimal only (N)"
    if errorlevel 2 goto minimal
    if errorlevel 1 goto full
    
    :full
    echo Installing full dependencies...
    pip install -r requirements.txt
    goto verify
    
    :minimal
    echo Installing minimal dependencies...
    pip install numpy scipy matplotlib pyyaml
    goto verify
    
    :verify
    echo.
    echo Step 4: Verifying installation...
    python check_setup.py
    if errorlevel 1 (
        echo [WARNING] Some dependencies may not have installed correctly
        echo Try running: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo ======================================================================
echo SETUP COMPLETE!
echo ======================================================================
echo.
echo You can now run:
echo   1. python demo.py              - Quick demonstration
echo   2. python test_suite.py        - Comprehensive tests
echo   3. python src/analyzer.py      - Main analyzer
echo.
echo ======================================================================
echo.

choice /C YN /M "Run quick demo now"
if errorlevel 2 goto end
if errorlevel 1 (
    echo.
    echo Running demo...
    python demo.py
)

:end
echo.
echo Setup script finished.
pause
