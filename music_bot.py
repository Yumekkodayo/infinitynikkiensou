import pyautogui
import time
import random

# キーマッピング
NOTE_MAP = {
    # 低音域（C3-B3）
    'C3': 'a', 'D3': 's', 'E3': 'd', 'F3': 'f',
    'G3': 'g', 'A3': 'h', 'B3': 'j',
    
    # 高音域（C4-B4）
    'C4': 'q', 'D4': 'w', 'E4': 'e', 'F4': 'r',
    'G4': 't', 'A4': 'y', 'B4': 'u'
}

def play_note(note, duration, tie=False):
    """音符または休符を演奏する"""
    if note == 'R':
        print(f"休符，持続時間 {duration} 拍")
        time.sleep(duration)
    elif ',' in note:  # 連符を処理
        notes = note.split(',')
        for n in notes:
            if n in NOTE_MAP:
                key = NOTE_MAP[n]
                print(f"キーを押す：{key} (音符：{n})")
                pyautogui.keyDown(key)
        time.sleep(duration * 0.9)
        for n in notes:
            if n in NOTE_MAP:
                key = NOTE_MAP[n]
                pyautogui.keyUp(key)
        time.sleep(duration * 0.1)
    elif note in NOTE_MAP:
        key = NOTE_MAP[note]
        print(f"キーを押す：{key} (音符：{note})")
        pyautogui.keyDown(key)
        time.sleep(duration * 0.9)
        if not tie:  # 連音でない場合、キーを離す
            pyautogui.keyUp(key)
        time.sleep(duration * 0.1)

def parse_simple_sheet(sheet_path):
    """楽譜を解析する"""
    with open(sheet_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) == 2:
                    yield parts[0], float(parts[1])

def play_song(sheet_path, bpm=60):
    """メインの演奏関数"""
    pyautogui.PAUSE = 0  # pyautogui のデフォルト遅延を無効にする
    
    print(f"5秒後に演奏を開始します {sheet_path} (BPM: {bpm})")
    print("ゲームウィンドウがアクティブであることを確認してください！")
    time.sleep(5)
    
    beat_duration = 60 / bpm
    total_notes = 0
    
    for note, beat in parse_simple_sheet(sheet_path):
        play_note(note, beat * beat_duration)
        total_notes += 1
    
    print(f"演奏が完了しました！合計 {total_notes} 個の音符を演奏しました")

if __name__ == "__main__":
    play_song('demo_sheet.txt', bpm=120)  # デフォルトの楽譜と BPM