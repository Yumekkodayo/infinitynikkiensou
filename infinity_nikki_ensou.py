import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyautogui
import time
import random
import mido
from ttkthemes import ThemedTk
import tkinter.ttk as ttk

# キーマッピング
NOTE_MAP = {
    'C3': 'a', 'D3': 's', 'E3': 'd', 'F3': 'f',
    'G3': 'g', 'A3': 'h', 'B3': 'j',
    'C4': 'q', 'D4': 'w', 'E4': 'e', 'F4': 'r',
    'G4': 't', 'A4': 'y', 'B4': 'u'
}

def play_note(note, duration, tie=False, feedback_text=None):
    """音符または休符を演奏する"""
    if note == 'R':
        feedback_text.insert(tk.END, f"休符，持続時間 {duration} 拍\n")
        feedback_text.see(tk.END)  # 最新の内容に自動スクロール
        time.sleep(duration)
    elif ',' in note:  # 連符を処理
        notes = note.split(',')
        for n in notes:
            if n in NOTE_MAP:
                key = NOTE_MAP[n]
                feedback_text.insert(tk.END, f"キーを押す：{key} (音符：{n})\n")
                feedback_text.see(tk.END)
                pyautogui.keyDown(key)
        time.sleep(duration * 0.9)
        for n in notes:
            if n in NOTE_MAP:
                key = NOTE_MAP[n]
                pyautogui.keyUp(key)
        time.sleep(duration * 0.1)
    elif note in NOTE_MAP:
        key = NOTE_MAP[note]
        feedback_text.insert(tk.END, f"キーを押す：{key} (音符：{note})\n")
        feedback_text.see(tk.END)
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

def play_song(sheet_path, bpm=60, feedback_text=None):
    """メインの演奏関数"""
    pyautogui.PAUSE = 0  # pyautogui のデフォルト遅延を無効にする
    
    feedback_text.insert(tk.END, f"5秒後に演奏を開始します {sheet_path} (BPM: {bpm})\n")
    feedback_text.see(tk.END)
    for i in range(5, 0, -1):
        feedback_text.insert(tk.END, f"{i}...\n")
        feedback_text.see(tk.END)
        time.sleep(1)
    
    beat_duration = 60 / bpm
    total_notes = 0
    
    for note, beat in parse_simple_sheet(sheet_path):
        play_note(note, beat * beat_duration, feedback_text=feedback_text)
        total_notes += 1
    
    feedback_text.insert(tk.END, f"演奏が完了しました！合計 {total_notes} 個の音符を演奏しました\n")
    feedback_text.see(tk.END)

def midi_to_sheet(midi_path, output_path):
    """MIDI ファイルを楽譜に変換する"""
    mid = mido.MidiFile(midi_path)
    ticks_per_beat = mid.ticks_per_beat  # MIDI ファイルのタイムベースを取得

    with open(output_path, 'w') as f:
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    # MIDIノート番号を音符名に変換
                    note_number = msg.note
                    octave = (note_number // 12) - 1
                    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
                    note_name = note_names[note_number % 12]

                    # 自然音のみをフィルタリング（C3-B4）
                    if '#' not in note_name and 48 <= note_number <= 72:
                        # タイムスタンプを拍に変換
                        beat = msg.time / ticks_per_beat
                        if beat > 0:  # 時値が 0 の音符を無視
                            f.write(f"{note_name}{octave} {beat}\n")

class InfinityNikkiEnsouUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InfinityNikkiEnsou")
        self.root.geometry("500x400")

        # ウィンドウアイコンを設定
        try:
            self.root.iconbitmap("nikki.ico")
        except tk.TclError:
            messagebox.showerror("エラー", "アイコンファイル 'nikki.ico' が見つかりません。")

        # ピンクのテーマを適用
        self.root.set_theme("scidpink")  # ピンクのテーマを使用

        # 楽譜ファイルパス
        self.sheet_path = tk.StringVar()
        self.sheet_path.set("demo_sheet.txt")  # デフォルト楽譜

        # BPM
        self.bpm = tk.IntVar()
        self.bpm.set(120)  # デフォルト BPM

        # UI コンポーネントを作成
        self.create_widgets()

    def create_widgets(self):
        # 楽譜ファイル選択
        ttk.Label(self.root, text="楽譜ファイル:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.sheet_path, width=30).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="選択", command=self.select_sheet).grid(row=0, column=2, padx=10, pady=10)

        # MIDI ファイル変換
        ttk.Button(self.root, text="MIDI を楽譜に変換", command=self.convert_midi).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # BPM 調整
        ttk.Label(self.root, text="BPM:").grid(row=2, column=0, padx=10, pady=10)
        ttk.Scale(self.root, from_=60, to=200, orient=tk.HORIZONTAL, variable=self.bpm).grid(row=2, column=1, padx=10, pady=10)

        # 開始/停止ボタン
        ttk.Button(self.root, text="演奏開始", command=self.start_playing).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="停止", command=self.stop_playing).grid(row=3, column=1, padx=10, pady=10)

        # フィードバックテキストボックス
        self.feedback_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.feedback_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def select_sheet(self):
        """楽譜ファイルを選択"""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.sheet_path.set(file_path)

    def convert_midi(self):
        """MIDI ファイルを楽譜に変換"""
        midi_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if midi_path:
            output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if output_path:
                midi_to_sheet(midi_path, output_path)
                messagebox.showinfo("成功", f"楽譜が保存されました: {output_path}")

    def start_playing(self):
        """演奏を開始"""
        sheet_path = self.sheet_path.get()
        bpm = self.bpm.get()
        self.feedback_text.insert(tk.END, f"演奏を開始します: {sheet_path} (BPM: {bpm})\n")
        self.feedback_text.see(tk.END)
        play_song(sheet_path, bpm, feedback_text=self.feedback_text)

    def stop_playing(self):
        """演奏を停止"""
        # ここに停止ロジックを追加（必要であれば）
        self.feedback_text.insert(tk.END, "演奏を停止しました\n")
        self.feedback_text.see(tk.END)

if __name__ == "__main__":
    root = ThemedTk(theme="scidpink")  # ピンクのテーマを使用
    app = InfinityNikkiEnsouUI(root)
    root.mainloop()