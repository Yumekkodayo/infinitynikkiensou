def midi_to_sheet(midi_path, output_path):
    """MIDIを簡易譜面に"""
    mid = mido.MidiFile(midi_path)
    
    with open(output_path, 'w') as f:
        for msg in mid:
            if msg.type == 'note_on' and msg.velocity > 0:
                # 転換
                note_name = mido.note_number_to_name(msg.note)[:-1]
                # 非自然音を除去
                if '#' not in note_name and 48 <= msg.note <= 72:
                    f.write(f"{note_name} {msg.time}\n")

# 例
midi_to_sheet('input.mid', 'output.txt')