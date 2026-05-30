@echo off
:: Script de inicialização do app IQESC
:: Executa automaticamente o Streamlit

echo.
echo ========================================
echo   APP IQESC - TCE-SC (AUTOMATICO)
echo ========================================
echo.
echo   NOVIDADES DA VERSAO 2.0:
echo   - Digite qualquer ano desejado
echo   - Download automatico de dados
echo   - Cache inteligente (uso offline)
echo   - Interface 100%% automatica
echo.
echo ========================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python 3.8+ em https://python.org
    pause
    exit /b 1
)

:: Verifica se o Streamlit está instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Streamlit nao encontrado. Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo [OK] Dependencias verificadas
echo.
echo Abrindo interface no navegador...
echo.
echo Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para encerrar
echo ========================================
echo.

:: Inicia o Streamlit
streamlit run app.py

pause
