import tkinter as tk
from tkinter import messagebox

class VivobookControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASUS Vivobook 15 (M1502YA-BQ703WS)")
        self.geometry("620x680")
        self.configure(bg="#0b120e")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        menubar = tk.Menu(self)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Reset Defaults", command=self.reset_defaults)
        options_menu.add_separator()
        options_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="Options", menu=options_menu)
        self.config(menu=menubar)

        header = tk.Frame(self, bg="#13221a", padx=16, pady=12)
        header.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(
            header,
            text="ASUS Vivobook 15 — M1502YA-BQ703WS",
            bg="#13221a",
            fg="#34d399",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="AMD Ryzen 7 5825U  |  16GB DDR4  |  512GB NVMe  |  42Wh Battery",
            bg="#13221a",
            fg="#a7c4b5",
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 0))

        mode_frame = tk.LabelFrame(
            self, text="Fan Profile (Fn + F)", bg="#0b120e", fg="#ecfdf5", padx=12, pady=8
        )
        mode_frame.pack(fill="x", padx=14, pady=6)

        self.mode_var = tk.StringVar(value="Standard (15W)")
        for mode in ["Whisper (10W)", "Standard (15W)", "Performance (25W)"]:
            tk.Radiobutton(
                mode_frame,
                text=mode,
                variable=self.mode_var,
                value=mode,
                bg="#0b120e",
                fg="#d1fae5",
                selectcolor="#060a08",
                activebackground="#0b120e",
                activeforeground="#34d399",
            ).pack(side="left", padx=(0, 16))

        limits_frame = tk.LabelFrame(
            self, text="Power & Thermal Limits", bg="#0b120e", fg="#ecfdf5", padx=12, pady=8
        )
        limits_frame.pack(fill="x", padx=14, pady=6)

        tk.Label(limits_frame, text="STAPM Power Limit (W):", bg="#0b120e", fg="#d1fae5").grid(
            row=0, column=0, sticky="w"
        )
        self.tdp_scale = tk.Scale(
            limits_frame,
            from_=10,
            to=25,
            orient="horizontal",
            bg="#0b120e",
            fg="#34d399",
            troughcolor="#1e3529",
            highlightthickness=0,
            length=220,
        )
        self.tdp_scale.set(15)
        self.tdp_scale.grid(row=0, column=1, padx=10)

        tk.Label(limits_frame, text="Max Temp (°C):", bg="#0b120e", fg="#d1fae5").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        self.temp_spin = tk.Spinbox(
            limits_frame, from_=65, to=95, width=6, bg="#13221a", fg="#ecfdf5", bd=0
        )
        self.temp_spin.delete(0, "end")
        self.temp_spin.insert(0, "85")
        self.temp_spin.grid(row=1, column=1, sticky="w", padx=10, pady=(8, 0))

        hw_frame = tk.LabelFrame(
            self, text="MyASUS Hardware Features", bg="#0b120e", fg="#ecfdf5", padx=12, pady=8
        )
        hw_frame.pack(fill="x", padx=14, pady=6)

        self.bat_cap_var = tk.BooleanVar(value=True)
        self.ai_mic_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            hw_frame,
            text="Battery Health Charging (80% Cap)",
            variable=self.bat_cap_var,
            bg="#0b120e",
            fg="#d1fae5",
            selectcolor="#060a08",
            activebackground="#0b120e",
        ).pack(anchor="w")

        tk.Checkbutton(
            hw_frame,
            text="AI Noise-Canceling Array Mic",
            variable=self.ai_mic_var,
            bg="#0b120e",
            fg="#d1fae5",
            selectcolor="#060a08",
            activebackground="#0b120e",
        ).pack(anchor="w")

        splendid_row = tk.Frame(hw_frame, bg="#0b120e")
        splendid_row.pack(fill="x", pady=(6, 0))
        tk.Label(splendid_row, text="Splendid Display Mode:", bg="#0b120e", fg="#d1fae5").pack(
            side="left"
        )
        self.splendid_var = tk.StringVar(value="Vivid")
        opt = tk.OptionMenu(splendid_row, self.splendid_var, "Normal", "Vivid", "Eye Care")
        opt.config(bg="#13221a", fg="#ecfdf5", highlightthickness=0, bd=0)
        opt.pack(side="left", padx=10)

        auto_frame = tk.LabelFrame(
            self, text="Automation Rules", bg="#0b120e", fg="#ecfdf5", padx=12, pady=8
        )
        auto_frame.pack(fill="x", padx=14, pady=6)

        self.rules_list = tk.Listbox(
            auto_frame, height=3, bg="#060a08", fg="#d1fae5", selectbackground="#34d399", selectforeground="#060a08", bd=0
        )
        self.rules_list.insert("end", "On 45W AC Adapter -> Standard Mode")
        self.rules_list.insert("end", "On 42Wh Battery -> Whisper Mode")
        self.rules_list.pack(fill="x", pady=(0, 6))

        entry_row = tk.Frame(auto_frame, bg="#0b120e")
        entry_row.pack(fill="x")
        self.rule_entry = tk.Entry(entry_row, bg="#13221a", fg="#ecfdf5", insertbackground="#ecfdf5", bd=0)
        self.rule_entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 6))
        tk.Button(
            entry_row, text="Add Rule", bg="#34d399", fg="#060a08", bd=0, padx=10, command=self.add_rule
        ).pack(side="left")

        self.gauge = tk.Canvas(self, height=22, bg="#13221a", highlightthickness=0)
        self.gauge.pack(fill="x", padx=14, pady=(8, 4))
        self.gauge.create_rectangle(0, 0, 470, 22, fill="#34d399", outline="")
        self.gauge.create_text(295, 11, text="Battery: 80% (42Wh 3S1P)", fill="#060a08", font=("Segoe UI", 9, "bold"))

        footer = tk.Frame(self, bg="#0b120e")
        footer.pack(fill="x", padx=14, pady=10)

        self.status_lbl = tk.Label(footer, text="Ready", bg="#0b120e", fg="#6ee7b7")
        self.status_lbl.pack(side="left")

        tk.Button(
            footer, text="Close", bg="#1e3529", fg="#ecfdf5", bd=0, padx=14, pady=5, command=self.on_close
        ).pack(side="right", padx=(6, 0))
        tk.Button(
            footer, text="Reset", bg="#1e3529", fg="#ecfdf5", bd=0, padx=14, pady=5, command=self.reset_defaults
        ).pack(side="right", padx=(6, 0))
        tk.Button(
            footer, text="Apply", bg="#34d399", fg="#060a08", bd=0, padx=14, pady=5, command=self.apply_settings
        ).pack(side="right")

    def add_rule(self):
        text = self.rule_entry.get().strip()
        if text:
            self.rules_list.insert("end", text)
            self.rule_entry.delete(0, "end")

    def apply_settings(self):
        summary = (
            f"Fan Profile: {self.mode_var.get()}\n"
            f"STAPM Limit: {self.tdp_scale.get()} W\n"
            f"Max Temp: {self.temp_spin.get()} °C\n"
            f"Battery 80% Cap: {'On' if self.bat_cap_var.get() else 'Off'}\n"
            f"AI Array Mic: {'On' if self.ai_mic_var.get() else 'Off'}\n"
            f"Splendid Mode: {self.splendid_var.get()}"
        )
        self.status_lbl.config(
            text=f"Applied: {self.mode_var.get()} | {self.tdp_scale.get()}W | Max {self.temp_spin.get()}°C"
        )
        messagebox.showinfo("Settings Applied", summary)

    def reset_defaults(self):
        self.mode_var.set("Standard (15W)")
        self.tdp_scale.set(15)
        self.temp_spin.delete(0, "end")
        self.temp_spin.insert(0, "85")
        self.bat_cap_var.set(True)
        self.ai_mic_var.set(True)
        self.splendid_var.set("Vivid")
        self.rules_list.delete(0, "end")
        self.rules_list.insert("end", "On 45W AC Adapter -> Standard Mode")
        self.rules_list.insert("end", "On 42Wh Battery -> Whisper Mode")
        self.status_lbl.config(text="Reset to factory defaults")

    def on_close(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = VivobookControlApp()
    app.mainloop()