import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from pydub import AudioSegment
import os

def convert_audio(input_path, output_directory, format_choice):
    if input_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(input_path)
    elif input_path.lower().endswith('.wav'):
        audio = AudioSegment.from_wav(input_path)
    elif input_path.lower().endswith('.ogg'):
        audio = AudioSegment.from_ogg(input_path)
    elif input_path.lower().endswith('.mp4'):
        audio = AudioSegment.from_file(input_path, format="mp4")
    elif input_path.lower().endswith('.avi'):
        audio = AudioSegment.from_file(input_path, format="avi")
    elif input_path.lower().endswith('.mov'):
        audio = AudioSegment.from_file(input_path, format="mov")
    elif input_path.lower().endswith('.webm'):
        audio = AudioSegment.from_file(input_path, format="webm")
    else:
        raise ValueError("次のファイル形式しかサポートしていません 'mp3','wav','ogg','mp4','avi','mov','webm'.")

    base_name = os.path.basename(input_path)
    if format_choice.lower() == 'wav':
        output_name = os.path.splitext(base_name)[0] + ".wav"
        output_format = "wav"
    elif format_choice.lower() == 'ogg':
        output_name = os.path.splitext(base_name)[0] + ".ogg"
        output_format = "ogg"
    elif format_choice.lower() == 'mp3':
        output_name = os.path.splitext(base_name)[0] + ".mp3"
        output_format = "mp3"
    else:
        raise ValueError("次のファイル形式しかサポートしていません 'mp3','wav','ogg'.")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_path = os.path.join(output_directory, output_name)

    print(f"Saving to: {output_path}")

    audio.export(output_path, format=output_format)

def drop(event):
    input_path = event.data.strip('{}')
    entry.delete(1.0, tk.END)
    entry.insert(tk.END, input_path)

def browse_file():
    input_path = filedialog.askopenfilename()
    if input_path:
        entry.delete(1.0, tk.END)
        entry.insert(tk.END, input_path)

def choose_output_directory():
    global output_directory
    output_directory = filedialog.askdirectory()
    if output_directory:
        output_dir_entry.config(state=tk.NORMAL)
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_directory)
        output_dir_entry.config(state=tk.DISABLED)

def convert_button_click():
    input_path = entry.get("1.0", tk.END).strip()
    if input_path:
        format_choice = format_var.get()
        convert_audio(input_path, output_directory, format_choice)
        result_label.config(text=f"変換が完了しました\n何か問題があればDiscordに連絡ください。ID:6x00")

app = TkinterDnD.Tk()
app.title('Audio Converter')

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="変換したいファイルを青い枠にドロップするか、参照してください")
label.pack()

browse_button = tk.Button(frame, text="ファイルを参照", command=browse_file)
browse_button.pack(pady=5)

entry = tk.Text(frame, width=50, height=5, bg="blue", fg="white")
entry.pack(pady=5)

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)

entry.bind("<Key>", lambda e: "break")

button_frame = tk.Frame(frame)
button_frame.pack(pady=5)

format_var = tk.StringVar(value="mp3")
format_label = tk.Label(button_frame, text="変換形式を選んでください:")
format_label.pack(side=tk.LEFT)

format_choices = ["mp3", "wav", "ogg"]
format_menu = tk.OptionMenu(button_frame, format_var, *format_choices)
format_menu.pack(side=tk.LEFT)

output_dir_frame = tk.Frame(frame)
output_dir_frame.pack(pady=5)

output_dir_button = tk.Button(output_dir_frame, text="出力ディレクトリを選択", command=choose_output_directory)
output_dir_button.pack(side=tk.LEFT)

output_dir_entry = tk.Entry(output_dir_frame, width=50, state=tk.DISABLED)
output_dir_entry.pack(side=tk.LEFT)

convert_button = tk.Button(frame, text="変換", command=convert_button_click)
convert_button.pack(pady=5)

output_directory = ""

result_label = tk.Label(app, text="")
result_label.pack(pady=5)

app.mainloop()
