@echo off
:: �����ߘ��ޤǌg�Ф���Ƥ��뤫�_�J
net session >nul 2>&1
if %errorlevel% == 0 (
    echo �����ߘ��ޤǌg����
) else (
    echo �����ߘ��ޤ�ꥯ��������...
    :: �����ߘ��ޤ�������
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

title ���S����ܥå�
color 0a

:: Python �����󥹥ȩ`�뤵��Ƥ��뤫�_�J
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python ��Ҋ�Ĥ���ޤ���Python 3.x �򥤥󥹥ȩ`�뤷�Ƥ���������
    pause
    exit /b
)

:: �����v�S�򥤥󥹥ȩ`��
echo Python �����v�S�򥤥󥹥ȩ`����...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% neq 0 (
    echo pip ���󥹥ȩ`���ʧ�����ޤ������ޏͤ�ԇ�ߤޤ�...
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip install --upgrade pip >nul 2>&1
)

python -m pip install pyautogui mido >nul 2>&1
if %errorlevel% neq 0 (
    echo �����v�S�Υ��󥹥ȩ`���ʧ�����ޤ��������¤Υ��ޥ�ɤ��քӤǌg�Ф��Ƥ���������
    echo python -m pip install pyautogui mido
    pause
    exit /b
)

:: ����ץ�S�V��_�J
if not exist "demo_sheet.txt" (
    echo ����ץ�S�V��������...
    echo C4 0.5 > demo_sheet.txt
    echo D4 0.5 >> demo_sheet.txt
    echo E4 1 >> demo_sheet.txt
    echo C4 0.5 >> demo_sheet.txt
    echo D4 0.5 >> demo_sheet.txt
    echo E4 1 >> demo_sheet.txt
    echo E4 0.5 >> demo_sheet.txt
    echo F4 0.5 >> demo_sheet.txt
    echo G4 2 >> demo_sheet.txt
)

:: �ץ���������
echo ���S�ܥåȤ�������...
python music_bot.py

:: ������ɥ����_�����ޤޤˤ���
pause