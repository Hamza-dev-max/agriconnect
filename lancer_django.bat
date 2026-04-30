@echo off
REM Script de lancement de l'application Django
REM Application de Recommandation Agricole v3.0
REM Auteur: Hamza Marzaq

echo ============================================================
echo   Application de Recommandation Agricole - Django Web App
echo   Version 3.0
echo   Auteur : Hamza Marzaq
echo ============================================================
echo.

REM Vérifier que Python est installé
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.12+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Vérifier que Django est installé
py -c "import django" >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Django n'est pas installe
    echo.
    echo Installation de Django...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERREUR] Echec de l'installation
        pause
        exit /b 1
    )
)

echo [OK] Django installe
echo.

REM Vérifier que MySQL est démarré
echo Verification de MySQL...
mysql --version >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] MySQL n'est pas detecte
    echo Assurez-vous que MySQL est installe et demarre
    echo.
)

echo.
echo ============================================================
echo   Lancement du serveur Django...
echo ============================================================
echo.
echo Acces a l'application :
echo   - Application : http://127.0.0.1:8000/
echo   - Administration : http://127.0.0.1:8000/admin/
echo.
echo Appuyez sur CTRL+C pour arreter le serveur
echo ============================================================
echo.

REM Lancer le serveur Django
py manage.py runserver

REM Si le serveur se termine avec une erreur
if errorlevel 1 (
    echo.
    echo ============================================================
    echo [ERREUR] Le serveur s'est termine avec une erreur
    echo.
    echo Solutions possibles :
    echo   1. Verifier que MySQL est demarre : net start MySQL80
    echo   2. Verifier le fichier .env
    echo   3. Faire les migrations : py manage.py migrate
    echo   4. Consulter DJANGO_READY.md
    echo ============================================================
    echo.
)

pause
