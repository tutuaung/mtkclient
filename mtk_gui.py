import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import time
import os

log_errors = True

ascii_art = """
        ******                      ******   **************************  *****     ***
        **** **                    ** ****   **************************  *****    ***
        ****  **                  **  ****   **************************  *****   ***
        ****   **                **   ****             *****             *****  ***
        ****    **              **    ****             *****             ***** ***
        ****     **            **     ****             *****             ********
        ****      **          **      ****             *****             ********
        ****       **        **       ****             *****             ***** ***
        ****        **      **        ****             *****             *****  ***
        ****         **    **         ****             *****             *****   ***
        ****          **  **          ****             *****             *****    ***
        ****           ****           ****             *****             *****     ***
********************************************************************************************
                                                Developed By Tu Tu Aung
                                            ****************************************
"""

def run_command(cmd):
    try:
        output_box.insert(tk.END, f">>> python {cmd}\n")
        result = subprocess.run(["python"] + cmd.split(), capture_output=True, text=True)
        output_box.insert(tk.END, result.stdout + "\n")
        if result.stderr:
            output_box.insert(tk.END, "❌ Error:\n" + result.stderr + "\n")
            if log_errors:
                with open("error.log", "a") as f:
                    f.write(result.stderr + "\n")
        output_box.see(tk.END)
    except Exception as e:
        output_box.insert(tk.END, "❌ Exception: " + str(e) + "\n")
        if log_errors:
            with open("error.log", "a") as f:
                f.write(str(e) + "\n")
        output_box.see(tk.END)

def run_command_threaded(cmd):
    threading.Thread(target=lambda: run_command(cmd)).start()

def check_device_status():
    while True:
        try:
            result = subprocess.run(["python", "mtk", "printgpt"], capture_output=True, text=True)
            if "No device found" in result.stdout or result.stderr:
                status_label.config(text="❌ ဖုန်းမချိတ်ဆက်ရသေးပါ", fg="red")
            else:
                status_label.config(text="✅ ဖုန်းချိတ်ဆက်ပြီးပါပြီ", fg="green")
        except Exception:
            status_label.config(text="❌ စစ်ဆေးမှု Error", fg="orange")
        time.sleep(5)

def reconnect_device():
    status_label.config(text="🔄 Reconnecting...", fg="orange")
    try:
        result = subprocess.run(["python", "mtk", "printgpt"], capture_output=True, text=True)
        if "No device found" in result.stdout or result.stderr:
            status_label.config(text="❌ ဖုန်းမချိတ်ဆက်ရသေးပါ", fg="red")
        else:
            status_label.config(text="✅ ဖုန်းချိတ်ဆက်ပြီးပါပြီ", fg="green")
    except Exception:
        status_label.config(text="❌ စစ်ဆေးမှု Error", fg="orange")

def toggle_logging():
    global log_errors
    log_errors = not log_errors
    status = "ON" if log_errors else "OFF"
    logging_status_label.config(text=f"Error Logging: {status}")
    messagebox.showinfo("Error Logging", f"Error logging is now: {status}")

def show_errors():
    try:
        with open("error.log", "r") as f:
            errors = f.read()
        messagebox.showinfo("Error Log", errors if errors else "No errors logged.")
    except FileNotFoundError:
        messagebox.showinfo("Error Log", "Error log file မရှိသေးပါ")

def show_contact():
    messagebox.showinfo(
        "ဆက်သွယ်ရန်",
        "📞 ဖုန်း: 09954495808\n📧 Gmail: aungtutu83@gmail.com\n\nDeveloped by Tu Tu Aung"
    )

def create_gui():
    root = tk.Tk()
    root.title("MTK Client Tool by Tu Tu Aung")
    root.geometry("1000x650")
    root.configure(bg="#d0f0c0")

    tk.Label(root, text=ascii_art, font=("Courier", 8), fg="green", bg="#d0f0c0", justify="left").pack(pady=(5, 0))

    global status_label
    status_label = tk.Label(root, text="🔄 ဖုန်းချိတ်ဆက်မှု စစ်ဆေးနေသည်...", font=("Helvetica", 12), bg="#d0f0c0")
    status_label.pack(pady=5)

    main_frame = tk.Frame(root, bg="#d0f0c0")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    button_frame_left = tk.Frame(main_frame, bg="#d0f0c0")
    button_frame_left.pack(side="left", fill="y", padx=5)

    button_frame_right = tk.Frame(main_frame, bg="#d0f0c0")
    button_frame_right.pack(side="left", fill="y", padx=5)

    output_frame = tk.Frame(main_frame, bg="#d0f0c0")
    output_frame.pack(side="right", fill="both", expand=True)

    global output_box
    output_box = scrolledtext.ScrolledText(
        output_frame,
        width=60,
        height=20,
        bg="#000000",
        fg="#00ff00",
        font=("Courier", 10),
        wrap="word"
    )
    output_box.pack(fill="both", expand=True)

    global logging_status_label
    logging_status_label = tk.Label(button_frame_right, text="Error Logging: ON", bg="#d0f0c0", font=("Helvetica", 10))
    logging_status_label.pack(pady=3)

    left_buttons = [
        ("GPT ဖတ်မည်", "mtk printgpt"),
        ("Backup nvdata,nvram,nvcfg", "mtk r nvdata,nvram,nvcfg nvdata.img,nvram.img,nvcfg.img"),
        ("Backup All", "mtk r preloader,lk,boot,system,vendor,userdata,nvdata,nvram,nvcfg,nvmetadb,nvcust,nvsec "
         "recovery.img,lk.img,boot.img,system.img,vendor.img,userdata.img,nvdata.img,nvram.img,"
         "nvcfg.img,nvmetadb.img,nvcust.img,nvsec.img"),
        ("Restore nvdata,nvram,nvcfg", "mtk w nvdata,nvram,nvcfg nvdata.img,nvram.img,nvcfg.img"),
        ("Restore All", "mtk w preloader,lk,boot,system,vendor,userdata,nvdata,nvram,nvcfg,nvmetadb,nvcust,nvsec "
         "recovery.img,lk.img,boot.img,system.img,vendor.img,userdata.img,nvdata.img,nvram.img,"
         "nvcfg.img,nvmetadb.img,nvcust.img,nvsec.img"),
        ("Bootloader Unlock", "mtk da seccfg unlock"),
        ("Auth Bypass", "mtk payload"),
        ("Fix dm-verity", "mtk w vbmeta vbmeta.img.empty")
    ]

    right_buttons = [
        ("Format User Data", "mtk e userdata,metadata"),
        ("Format FRP", "mtk e frp"),
        ("Format Para", "mtk w para para.img"),
        ("Reconnect ဖုန်း", reconnect_device),
        ("Error Log ကြည့်မည်", show_errors),
        ("Error Log ON/OFF", toggle_logging),
        ("ဆက်သွယ်ရန်", show_contact),
        ("ထွက်မည်", "exit")
    ]

    for text, cmd in left_buttons:
        action = lambda c=cmd: root.quit() if c == "exit" else run_command_threaded(c)
        tk.Button(button_frame_left, text=text, command=action, width=30, height=2, bg="#ccffcc").pack(pady=3)

    for text, cmd in right_buttons:
        action = lambda c=cmd: root.quit() if c == "exit" else run_command_threaded(c) if isinstance(cmd, str) else cmd
        tk.Button(button_frame_right, text=text, command=action, width=30, height=2, bg="#ccffcc").pack(pady=3)

    threading.Thread(target=check_device_status, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    create_gui()