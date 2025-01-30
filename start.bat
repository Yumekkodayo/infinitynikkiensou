@echo off
:: 管理者権限で実行されているか確認
net session >nul 2>&1
if %errorlevel% == 0 (
    echo 管理者権限で実行中
) else (
    echo 管理者権限をリクエスト中...
    :: 管理者権限で再起動
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

title 音楽演奏ボット
color 0a

:: Python がインストールされているか確認
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python が見つかりません。Python 3.x をインストールしてください！
    pause
    exit /b
)

:: 依存関係をインストール
echo Python 依存関係をインストール中...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% neq 0 (
    echo pip インストールに失敗しました。修復を試みます...
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip install --upgrade pip >nul 2>&1
)

python -m pip install pyautogui mido >nul 2>&1
if %errorlevel% neq 0 (
    echo 依存関係のインストールに失敗しました。以下のコマンドを手動で実行してください：
    echo python -m pip install pyautogui mido
    pause
    exit /b
)

:: サンプル楽譜を確認
if not exist "demo_sheet.txt" (
    echo サンプル楽譜を作成中...
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

:: プログラムを起動
echo 音楽ボットを起動中...
python music_bot.py

:: ウィンドウを開いたままにする
pause