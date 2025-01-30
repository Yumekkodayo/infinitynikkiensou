import pyautogui
import time
import mido
import random

# キーバインド
NOTE_MAP = {
    # 低音（C3-B3）
    'C3': 'a', 'D3': 's', 'E3': 'd', 'F3': 'f',
    'G3': 'g', 'A3': 'h', 'B3': 'j',
    
    # 高音（C4-B4）
    'C4': 'q', 'D4': 'w', 'E4': 'e', 'F4': 'r',
    'G4': 't', 'A4': 'y', 'B4': 'u'
}

def play_note(note, duration):
    """ランダムラグ"""
    if note in NOTE_MAP:
        key = NOTE_MAP[note]
        pyautogui.keyDown(key)
        time.sleep(duration * 0.85 + random.uniform(0, 0.05))
        pyautogui.keyUp(key)
        time.sleep(duration * 0.15 + random.uniform(0, 0.02))

def parse_simple_sheet(sheet_path):
    """楽譜解析"""
    with open(sheet_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) == 2:
                    yield parts[0], float(parts[1])

def play_song(sheet_path, bpm=120):
    """playnote"""
    pyautogui.PAUSE = 0  # 禁用pyautogui的默认延迟
    
    print(f"5秒内に演奏開始 {sheet_path} (BPM: {bpm})")
    print("ゲームのウィンドウを一番前にしてください")
    time.sleep(5)
    
    beat_duration = 60 / bpm
    total_notes = 0
    
    for note, beat in parse_simple_sheet(sheet_path):
        play_note(note, beat * beat_duration)
        total_notes += 1
    
    print(f"演奏終了 {total_notes} 個の音符を演奏しました")

if __name__ == "__main__":
    # デフォルト値
    play_song('demo_sheet.txt', bpm=120)