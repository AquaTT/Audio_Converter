import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from pydub import AudioSegment
import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)

def read_config_section(section_name):
    values = []
    config_path = os.path.join(get_base_path(), "config.txt")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            in_section = False
            for line in f:
                line = line.strip()
                if line.lower() == f"[{section_name.lower()}]":
                    in_section = True
                    continue
                if in_section:
                    if line.startswith("[") and line.lower() != f"[{section_name.lower()}]":
                        break
                    if line and not line.startswith("["):
                        value = line.split("=")[0].strip().lower()
                        values.append(value)
    return values

def convert_audio(input_path, output_directory, format_choice):
    supported_exts = read_config_section("extension")
    supported_outputs = read_config_section("output")

    ext = os.path.splitext(input_path)[1].lower()

    if ext not in supported_exts:
        raise ValueError("このファイル形式は config.txt に記載されていません。")

    if format_choice.lower() not in supported_outputs:
        raise ValueError("その拡張子は config.txt に存在しないか、対応していません。")

    format_hint = ext.replace('.', '')
    try:
        audio = AudioSegment.from_file(input_path, format=format_hint)
    except Exception as e:
        raise ValueError(f"読み込み失敗: {e}")

    base_name = os.path.basename(input_path)
    output_name = os.path.splitext(base_name)[0] + f".{format_choice.lower()}"
    output_path = os.path.join(output_directory, output_name)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        audio.export(output_path, format=format_choice.lower())
    except Exception:
        raise ValueError("その拡張子は存在しないか、ffmpegが対応していません。")

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
    format_choice = format_var.get()

    if format_choice == "未定義":
        result_label.config(text="変換形式が未定義です。config.txt を確認してください。")
        return

    if input_path:
        try:
            convert_audio(input_path, output_directory, format_choice)
            result_label.config(text=f"変換が完了しました\n何か問題があればDiscordに連絡ください。ID:6x00")
        except Exception as e:
            result_label.config(text=f"エラー: {e}")

app = TkinterDnD.Tk()
app.title('Asahara Converter')

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

format_label = tk.Label(button_frame, text="変換形式を選んでください:")
format_label.pack(side=tk.LEFT)

output_formats = read_config_section("output")
format_var = tk.StringVar()
if output_formats:
    format_var.set(output_formats[0])
    format_menu = tk.OptionMenu(button_frame, format_var, *output_formats)
else:
    format_var.set("未定義")
    format_menu = tk.OptionMenu(button_frame, format_var, "未定義")
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
