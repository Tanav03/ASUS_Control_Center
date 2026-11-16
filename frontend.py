import tkinter as tk


class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, initial=False, callback=None, bg="#19191b"):
        super().__init__(parent, width=44, height=24, bg=bg, highlightthickness=0, cursor="hand2")
        self.state = initial
        self.callback = callback
        self.bind("<Button-1>", self.toggle)
        self.draw()

    def toggle(self, _=None):
        self.state = not self.state
        self.draw()
        if self.callback:
            self.callback(self.state)

    def draw(self):
        self.delete("all")
        track_color = "#c3f73a" if self.state else "#3c3c42"
        knob_color = "#101012" if self.state else "#d8d8de"
        self.create_oval(2, 2, 22, 22, fill=track_color, outline=track_color)
        self.create_oval(22, 2, 42, 22, fill=track_color, outline=track_color)
        self.create_rectangle(12, 2, 32, 22, fill=track_color, outline=track_color)
        x = 24 if self.state else 4
        self.create_oval(x, 4, x + 16, 20, fill=knob_color, outline=knob_color)


class SystemControlCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASUS Vivobook 15 (M1502YA-BQ703WS) Control Center")
        self.geometry("1160x860")
        self.minsize(980, 740)
        self.configure(bg="#111113")

        self.bg_main = "#111113"
        self.bg_card = "#19191b"
        self.bg_hover = "#232327"
        self.accent = "#c3f73a"
        self.accent_dark = "#111113"
        self.text_primary = "#f3f3f5"
        self.text_muted = "#8b8b93"
        self.border_col = "#2a2a2f"

        self.current_tab = "Dashboard"
        self.power_mode = "Standard"
        self.nav_buttons = {}
        self.mode_buttons = {}
        self.toast_job = None
        self.poll_job = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Control-q>", lambda _: self.on_close())

        self.fan_profile_var = tk.StringVar(value="Standard Mode (15W)")
        self.charge_limit_var = tk.StringVar(value="80")
        self.splendid_var = tk.StringVar(value="Vivid")
        self.ai_mic_var = tk.BooleanVar(value=True)
        self.ai_spk_var = tk.BooleanVar(value=False)
        self.webcam_shutter_var = tk.BooleanVar(value=True)
        self.fn_lock_var = tk.BooleanVar(value=True)
        self.poll_ms_var = tk.StringVar(value="1000")
        self.auto_start_var = tk.BooleanVar(value=True)
        self.osd_var = tk.BooleanVar(value=True)
        self.target_c_var = tk.IntVar(value=85)

        self._build_navbar()
        self.content_area = tk.Frame(self, bg=self.bg_main)
        self.content_area.pack(fill="both", expand=True)

        self.toast_label = tk.Label(
            self,
            text="",
            bg="#26262b",
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=8,
            bd=1,
            relief="solid",
        )

        self.switch_tab("Dashboard")

    def on_close(self):
        if self.toast_job:
            self.after_cancel(self.toast_job)
        if self.poll_job:
            self.after_cancel(self.poll_job)
        self.quit()
        self.destroy()

    def show_toast(self, message):
        if self.toast_job:
            self.after_cancel(self.toast_job)
        self.toast_label.config(text=message)
        self.toast_label.place(relx=0.5, rely=0.95, anchor="center")
        self.toast_job = self.after(2200, self.toast_label.place_forget)

    def _build_navbar(self):
        nav_bar = tk.Frame(self, bg=self.bg_main, height=54)
        nav_bar.pack(fill="x", padx=24, pady=(12, 0))
        nav_bar.pack_propagate(False)

        tabs = [
            "Dashboard",
            "Power & Cooling",
            "Fan Curve",
            "CPU Tuning",
            "Battery",
            "Device",
            "Automation",
            "System",
            "Sensors",
            "Settings",
        ]

        for tab in tabs:
            holder = tk.Frame(nav_bar, bg=self.bg_main)
            holder.pack(side="left", padx=(0, 14), fill="y")

            btn = tk.Label(
                holder,
                text=tab,
                bg=self.bg_main,
                fg=self.text_muted,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                pady=12,
            )
            btn.pack(side="top")

            indicator = tk.Frame(holder, bg=self.bg_main, height=2)
            indicator.pack(side="bottom", fill="x")

            btn.bind("<Button-1>", lambda _, t=tab: self.switch_tab(t))
            self.nav_buttons[tab] = (btn, indicator)

        sep = tk.Frame(self, bg=self.border_col, height=1)
        sep.pack(fill="x", pady=(4, 0))

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        for name, (btn, indicator) in self.nav_buttons.items():
            if name == tab_name:
                btn.config(fg=self.text_primary)
                indicator.config(bg=self.accent)
            else:
                btn.config(fg=self.text_muted)
                indicator.config(bg=self.bg_main)

        for widget in self.content_area.winfo_children():
            widget.destroy()

        builders = {
            "Dashboard": self._build_dashboard,
            "Power & Cooling": self._build_power_cooling,
            "Fan Curve": self._build_fan_curve,
            "CPU Tuning": self._build_cpu_tuning,
            "Battery": self._build_battery,
            "Device": self._build_device,
            "Automation": self._build_automation,
            "System": self._build_system,
            "Sensors": self._build_sensors,
            "Settings": self._build_settings,
        }
        builders[tab_name]()

    def _build_dashboard(self):
        hero = tk.Frame(self.content_area, bg=self.accent, padx=28, pady=22)
        hero.pack(fill="x", padx=24, pady=(20, 18))

        tk.Label(
            hero,
            text="ASUS Intelligent Performance Technology  •  Quiet Blue",
            bg=self.accent,
            fg="#253008",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        self.hero_mode_lbl = tk.Label(
            hero,
            text=self.power_mode,
            bg=self.accent,
            fg=self.accent_dark,
            font=("Segoe UI", 34, "bold"),
        )
        self.hero_mode_lbl.pack(anchor="w", pady=(2, 6))

        tk.Label(
            hero,
            text="ASUS VIVOBOOK 15 (M1502YA-BQ703WS)  •  AMD RYZEN 7 5825U",
            bg=self.accent,
            fg="#253008",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        pill = tk.Button(
            hero,
            text="MyASUS Hardware Diagnostics & ACPI Status  →",
            bg=self.accent,
            fg=self.accent_dark,
            activebackground="#b3e82a",
            activeforeground=self.accent_dark,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=4,
            bd=1,
            relief="solid",
            cursor="hand2",
            command=lambda: self.switch_tab("System"),
        )
        pill.pack(anchor="w")

        body = tk.Frame(self.content_area, bg=self.bg_main)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 22))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        left_col = tk.Frame(body, bg=self.bg_main)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        tk.Label(
            left_col,
            text="Live telemetry",
            bg=self.bg_main,
            fg=self.text_primary,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        readings = [
            ("BAT", "42Wh 3-Cell Battery (80% Cap)", "80%", 80),
            ("CPU", "AMD Ryzen 7 5825U (8C/16T)", "54°C", 54),
            ("FAN", "ASUS IceBlade Cooling Fan", "2400 RPM", 42),
        ]
        for badge, title, val, pct in readings:
            card = tk.Frame(
                left_col,
                bg=self.bg_card,
                padx=18,
                pady=14,
                highlightbackground=self.border_col,
                highlightthickness=1,
            )
            card.pack(fill="x", pady=(0, 12))

            top = tk.Frame(card, bg=self.bg_card)
            top.pack(fill="x")

            tk.Label(
                top,
                text=badge,
                bg=self.bg_card,
                fg=self.text_muted,
                font=("Consolas", 10, "bold"),
                width=4,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                top,
                text=title,
                bg=self.bg_card,
                fg=self.text_primary,
                font=("Segoe UI", 10),
            ).pack(side="left", padx=(6, 0))

            tk.Label(
                top,
                text=val,
                bg=self.bg_card,
                fg=self.text_primary,
                font=("Segoe UI", 16, "bold"),
            ).pack(side="right")

            bar = tk.Canvas(card, height=6, bg="#26262b", highlightthickness=0)
            bar.pack(fill="x", pady=(10, 0))
            bar.update_idletasks()
            bar.create_rectangle(0, 0, int(380 * (pct / 100.0)), 6, fill=self.accent, outline="")

        right_col = tk.Frame(body, bg=self.bg_main)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

        mode_card = tk.Frame(
            right_col,
            bg=self.bg_card,
            padx=20,
            pady=16,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        mode_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            mode_card,
            text="ASUS Fan Profile",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            mode_card,
            text="Cycle modes anytime with Fn + F on Chiclet keyboard",
            bg=self.bg_card,
            fg=self.text_muted,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 12))

        btn_row = tk.Frame(mode_card, bg=self.bg_card)
        btn_row.pack(fill="x")

        self.mode_buttons.clear()
        for idx, mode in enumerate(["Whisper", "Standard", "Performance", "Custom"]):
            btn_row.columnconfigure(idx, weight=1)
            btn = tk.Button(
                btn_row,
                text=mode,
                font=("Segoe UI", 10, "bold"),
                pady=8,
                bd=0,
                cursor="hand2",
                command=lambda m=mode: self.set_power_mode(m),
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=(0 if idx == 0 else 6, 0))
            self.mode_buttons[mode] = btn

        self._refresh_mode_buttons()

        quick_card = tk.Frame(
            right_col,
            bg=self.bg_card,
            padx=20,
            pady=16,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        quick_card.pack(fill="both", expand=True)

        tk.Label(
            quick_card,
            text="MyASUS Quick Controls",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        toggles = [
            ("Battery Health Charging", "Caps 42Wh battery at 80% to extend cell lifespan.", True),
            ("ASUS Splendid Eye Care", "Low blue light filtering for 15.6\" FHD IPS anti-glare panel.", True),
            ("AI Noise-Canceling Array Mic", "Suppresses ambient noise on built-in array microphone.", True),
            ("Fn Lock (Hotkeys)", "Prioritize brightness, volume, and mic mute over F1-F12.", True),
        ]

        for idx, (title, desc, state) in enumerate(toggles):
            if idx > 0:
                tk.Frame(quick_card, bg=self.border_col, height=1).pack(fill="x", pady=9)

            row = tk.Frame(quick_card, bg=self.bg_card)
            row.pack(fill="x")

            txt_box = tk.Frame(row, bg=self.bg_card)
            txt_box.pack(side="left", fill="x", expand=True, padx=(0, 12))

            tk.Label(
                txt_box,
                text=title,
                bg=self.bg_card,
                fg=self.text_primary,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            ).pack(fill="x")

            tk.Label(
                txt_box,
                text=desc,
                bg=self.bg_card,
                fg=self.text_muted,
                font=("Segoe UI", 9),
                anchor="w",
                wraplength=360,
                justify="left",
            ).pack(fill="x", pady=(2, 0))

            ToggleSwitch(
                row,
                initial=state,
                callback=lambda s, t=title: self.show_toast(f"{t} {'enabled' if s else 'disabled'}"),
            ).pack(side="right")

    def set_power_mode(self, mode):
        self.power_mode = mode
        if hasattr(self, "hero_mode_lbl") and self.hero_mode_lbl.winfo_exists():
            self.hero_mode_lbl.config(text=mode)
        self._refresh_mode_buttons()
        self.show_toast(f"ASUS AIPT switched to {mode} mode")

    def _refresh_mode_buttons(self):
        for mode, btn in self.mode_buttons.items():
            if mode == self.power_mode:
                btn.config(bg=self.accent, fg=self.accent_dark, activebackground=self.accent)
            else:
                btn.config(bg="#26262a", fg=self.text_primary, activebackground="#323238")

    def _section_header(self, title, subtitle):
        wrap = tk.Frame(self.content_area, bg=self.bg_main)
        wrap.pack(fill="x", padx=24, pady=(20, 14))
        tk.Label(
            wrap,
            text=title,
            bg=self.bg_main,
            fg=self.text_primary,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            wrap,
            text=subtitle,
            bg=self.bg_main,
            fg=self.text_muted,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

    def _build_power_cooling(self):
        self._section_header(
            "Power & Cooling",
            "AMD Ryzen 7 5825U (15W nominal TDP) STAPM, Fast, and Slow power limits",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        top_row = tk.Frame(card, bg=self.bg_card)
        top_row.pack(fill="x", pady=(0, 12))
        tk.Label(
            top_row,
            text="AIPT Thermal Preset",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        menu = tk.OptionMenu(
            top_row,
            self.fan_profile_var,
            "Whisper Mode (10W)",
            "Standard Mode (15W)",
            "Performance Mode (25W)",
            "Custom Manual",
            command=lambda v: self.show_toast(f"Selected {v}"),
        )
        menu.config(
            bg="#26262a",
            fg=self.text_primary,
            activebackground="#323238",
            activeforeground=self.text_primary,
            highlightthickness=0,
            bd=0,
            font=("Segoe UI", 9, "bold"),
        )
        menu["menu"].config(bg="#26262a", fg=self.text_primary)
        menu.pack(side="right")

        sliders = [
            ("STAPM Sustained Power Limit", "Skin-aware sustained TDP: 10 W - 25 W", 10, 25, 15, "W"),
            ("PPT Fast Boost Power Limit", "Short burst boost TDP: 15 W - 35 W", 15, 35, 25, "W"),
            ("PPT Slow Power Limit", "Medium duration TDP: 12 W - 30 W", 12, 30, 20, "W"),
        ]
        for label, rng, low, high, default, unit in sliders:
            tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)
            self._add_slider_row(card, label, rng, low, high, default, unit)

        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)
        spin_row = tk.Frame(card, bg=self.bg_card)
        spin_row.pack(fill="x")
        tk.Label(
            spin_row,
            text="AMD Tctl Thermal Throttle Limit (°C)",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        spin = tk.Spinbox(
            spin_row,
            from_=65,
            to=95,
            textvariable=self.target_c_var,
            width=6,
            bg="#26262a",
            fg=self.text_primary,
            buttonbackground="#323238",
            font=("Consolas", 10, "bold"),
            bd=0,
        )
        spin.pack(side="right")

    def _build_fan_curve(self):
        self._section_header(
            "Fan Curve",
            "ASUS IceBlade fan duty cycle response for Ryzen 7 5825U",
        )
        wrap = tk.Frame(self.content_area, bg=self.bg_main)
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        wrap.columnconfigure(0, weight=3)
        wrap.columnconfigure(1, weight=2)

        card = tk.Frame(
            wrap,
            bg=self.bg_card,
            padx=20,
            pady=16,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        self.curve_vars = []
        points = [
            ("Point 1 (40°C)", 0),
            ("Point 2 (50°C)", 20),
            ("Point 3 (60°C)", 40),
            ("Point 4 (70°C)", 64),
            ("Point 5 (80°C)", 84),
            ("Point 6 (90°C)", 100),
        ]
        for idx, (pt, pct) in enumerate(points):
            if idx > 0:
                tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=8)
            var = self._add_slider_row(card, pt, "CPU Tdie Temp", 0, 100, pct, "%")
            var.trace_add("write", lambda *_: self._redraw_fan_canvas())
            self.curve_vars.append(var)

        graph_card = tk.Frame(
            wrap,
            bg=self.bg_card,
            padx=18,
            pady=16,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        graph_card.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            graph_card,
            text="Live Duty Cycle Curve",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        self.fan_canvas = tk.Canvas(
            graph_card,
            width=340,
            height=280,
            bg="#141416",
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        self.fan_canvas.pack(fill="both", expand=True)
        self._redraw_fan_canvas()

    def _redraw_fan_canvas(self):
        if not hasattr(self, "fan_canvas") or not self.fan_canvas.winfo_exists():
            return
        c = self.fan_canvas
        c.delete("all")
        w, h = 340, 280
        pad = 32
        for i in range(5):
            y = pad + i * ((h - 2 * pad) / 4)
            c.create_line(pad, y, w - pad, y, fill="#242429")
        coords = []
        vals = [v.get() for v in self.curve_vars]
        for idx, val in enumerate(vals):
            x = pad + idx * ((w - 2 * pad) / (len(vals) - 1))
            y = (h - pad) - (val / 100.0) * (h - 2 * pad)
            coords.extend([x, y])
        c.create_line(*coords, fill=self.accent, width=3, smooth=True)
        for i in range(0, len(coords), 2):
            x, y = coords[i], coords[i + 1]
            c.create_oval(x - 4, y - 4, x + 4, y + 4, fill=self.accent, outline="#111113")

    def _build_cpu_tuning(self):
        self._section_header(
            "CPU & iGPU Tuning",
            "AMD Ryzen 7 5825U (Zen 3, 2.0 - 4.5 GHz) Curve Optimizer & Radeon Graphics",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        self.co_var = self._add_slider_row(
            card, "All-Core Curve Optimizer Offset", "Zen 3 Voltage/Frequency Curve (-30 to 0)", -30, 0, -15, " cnt"
        )
        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)
        self.igpu_var = self._add_slider_row(
            card, "AMD Radeon Graphics Max Clock", "8-Core Vega iGPU (1000 - 2000 MHz)", 1000, 2000, 2000, " MHz"
        )
        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)

        cb_row = tk.Frame(card, bg=self.bg_card)
        cb_row.pack(fill="x", pady=(4, 14))
        self.cpb_enable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            cb_row,
            text="Enable AMD Core Performance Boost (up to 4.5 GHz Max Boost)",
            variable=self.cpb_enable_var,
            bg=self.bg_card,
            fg=self.text_primary,
            selectcolor="#26262a",
            activebackground=self.bg_card,
            activeforeground=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        actions = tk.Frame(card, bg=self.bg_card)
        actions.pack(fill="x")

        tk.Button(
            actions,
            text="Reset Defaults",
            bg="#26262a",
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=6,
            bd=0,
            cursor="hand2",
            command=self._reset_cpu_tuning,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            actions,
            text="Apply Profile",
            bg=self.accent,
            fg=self.accent_dark,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=6,
            bd=0,
            cursor="hand2",
            command=lambda: self.show_toast("Ryzen 7 5825U SMU parameters updated"),
        ).pack(side="right")

    def _reset_cpu_tuning(self):
        self.co_var.set(0)
        self.igpu_var.set(2000)
        self.cpb_enable_var.set(True)
        self.show_toast("Ryzen SMU offsets restored to factory defaults")

    def _add_slider_row(self, parent, title, subtitle, low, high, default, unit):
        row = tk.Frame(parent, bg=self.bg_card)
        row.pack(fill="x")

        left = tk.Frame(row, bg=self.bg_card)
        left.pack(side="left")
        tk.Label(
            left,
            text=title,
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            left,
            text=subtitle,
            bg=self.bg_card,
            fg=self.text_muted,
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(anchor="w")

        val_var = tk.IntVar(value=default)
        val_lbl = tk.Label(
            row,
            text=f"{default}{unit}",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Consolas", 11, "bold"),
            width=9,
            anchor="e",
        )
        val_lbl.pack(side="right")

        scale = tk.Scale(
            row,
            from_=low,
            to=high,
            orient="horizontal",
            variable=val_var,
            showvalue=False,
            bg=self.bg_card,
            fg=self.accent,
            troughcolor="#2d2d33",
            activebackground=self.accent,
            highlightthickness=0,
            bd=0,
            length=250,
            command=lambda v, lbl=val_lbl, u=unit: lbl.config(text=f"{v}{u}"),
        )
        scale.pack(side="right", padx=16)
        return val_var

    def _build_battery(self):
        self._section_header(
            "Battery Health Charging",
            "MyASUS 42Wh 3S1P 3-cell Li-ion protection modes and 45W AC / USB-C PD status",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24, pady=(0, 14))

        modes = [
            ("Full Capacity Mode (100%)", "100", "Charges 42Wh battery to 100% for maximum unplugged travel."),
            ("Balanced Mode (80%)", "80", "Stops charging above 80% — recommended for daily hybrid use."),
            ("Maximum Lifespan Mode (60%)", "60", "Stops charging above 60% — ideal when continuously on AC adapter."),
        ]
        for idx, (label, val, desc) in enumerate(modes):
            if idx > 0:
                tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=10)
            row = tk.Frame(card, bg=self.bg_card)
            row.pack(fill="x")
            tk.Radiobutton(
                row,
                text=label,
                variable=self.charge_limit_var,
                value=val,
                bg=self.bg_card,
                fg=self.text_primary,
                selectcolor="#26262a",
                activebackground=self.bg_card,
                activeforeground=self.text_primary,
                font=("Segoe UI", 10, "bold"),
                command=lambda v=val: self.show_toast(f"Battery charge cap set to {v}%"),
            ).pack(anchor="w")
            tk.Label(
                row,
                text=desc,
                bg=self.bg_card,
                fg=self.text_muted,
                font=("Segoe UI", 9),
            ).pack(anchor="w", padx=(24, 0))

        self._info_grid(
            [
                ("Battery Design Capacity", "42,000 mWh (42WHrs, 3S1P, 3-cell Li-ion)"),
                ("Full Charge Capacity", "41,160 mWh (98.0% Health)"),
                ("Primary Adapter", "45W Barrel AC Adapter (19V DC, 2.37A)"),
                ("USB-C Power Delivery", "USB 3.2 Gen 1 Type-C PD Charging Supported"),
            ]
        )

    def _build_device(self):
        self._section_header(
            "Device & Display",
            "15.6\" FHD Anti-Glare IPS-level display, Chiclet backlight, and SonicMaster Audio",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        splendid_row = tk.Frame(card, bg=self.bg_card)
        splendid_row.pack(fill="x")
        tk.Label(
            splendid_row,
            text="ASUS Splendid Color Mode (45% NTSC)",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        for mode in ["Normal", "Vivid", "Manual", "Eye Care"]:
            tk.Radiobutton(
                splendid_row,
                text=mode,
                variable=self.splendid_var,
                value=mode,
                bg=self.bg_card,
                fg=self.text_primary,
                selectcolor="#26262a",
                activebackground=self.bg_card,
                activeforeground=self.text_primary,
                font=("Segoe UI", 9, "bold"),
                command=lambda m=mode: self.show_toast(f"Splendid profile: {m}"),
            ).pack(side="right", padx=(10, 0))

        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)
        self._add_slider_row(
            card, "Backlit Chiclet Keyboard Brightness", "0 = Off, 3 = Max White Backlight", 0, 3, 2, " lvl"
        )
        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)
        self._add_slider_row(
            card, "Panel Brightness (250 nits Max)", "15.6\" FHD (1920x1080) 60Hz Anti-glare", 10, 100, 75, "%"
        )
        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=12)

        checks = [
            ("Two-Way AI Noise-Canceling Array Microphone", self.ai_mic_var),
            ("SonicMaster Speaker Enhancement & AI Noise Filter", self.ai_spk_var),
            ("720p HD Camera Privacy Status Monitor", self.webcam_shutter_var),
        ]
        for text, var in checks:
            tk.Checkbutton(
                card,
                text=text,
                variable=var,
                bg=self.bg_card,
                fg=self.text_primary,
                selectcolor="#26262a",
                activebackground=self.bg_card,
                activeforeground=self.text_primary,
                font=("Segoe UI", 10),
                command=lambda t=text: self.show_toast(f"Updated: {t}"),
            ).pack(anchor="w", pady=3)

    def _build_automation(self):
        self._section_header(
            "Automation Rules",
            "Event-driven ASUS profile switching rules",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        self.rules_listbox = tk.Listbox(
            card,
            height=6,
            bg="#141416",
            fg=self.text_primary,
            selectbackground=self.accent,
            selectforeground=self.accent_dark,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1,
            highlightbackground=self.border_col,
        )
        self.rules_listbox.pack(fill="x", pady=(0, 12))

        initial_rules = [
            "When 45W AC Adapter Connected  →  Standard Mode (15W) + 80% Brightness",
            "When Running on 42Wh Battery  →  Whisper Mode (10W) + Eye Care",
            "When Battery Drops Below 20%  →  Battery Saver + Keyboard Backlight Off",
            "When Teams / Meet Active  →  Enable Array Mic AI Noise Canceling",
        ]
        for r in initial_rules:
            self.rules_listbox.insert("end", r)

        entry_row = tk.Frame(card, bg=self.bg_card)
        entry_row.pack(fill="x")

        self.new_rule_entry = tk.Entry(
            entry_row,
            bg="#26262a",
            fg=self.text_primary,
            insertbackground=self.text_primary,
            font=("Segoe UI", 10),
            bd=0,
        )
        self.new_rule_entry.insert(0, "When Office / Compile Active  →  Performance Mode (25W)")
        self.new_rule_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))

        tk.Button(
            entry_row,
            text="Add Rule",
            bg=self.accent,
            fg=self.accent_dark,
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=6,
            bd=0,
            cursor="hand2",
            command=self._add_rule,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            entry_row,
            text="Remove Selected",
            bg="#26262a",
            fg=self.text_primary,
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=6,
            bd=0,
            cursor="hand2",
            command=self._remove_rule,
        ).pack(side="left")

    def _add_rule(self):
        rule = self.new_rule_entry.get().strip()
        if rule:
            self.rules_listbox.insert("end", rule)
            self.new_rule_entry.delete(0, "end")
            self.show_toast("Automation rule added")

    def _remove_rule(self):
        sel = self.rules_listbox.curselection()
        if sel:
            self.rules_listbox.delete(sel[0])
            self.show_toast("Automation rule removed")

    def _build_system(self):
        self._section_header(
            "System Inventory",
            "ASUS Vivobook 15 M1502YA-BQ703WS (90NB0X21-M011U0) hardware specification",
        )
        self._info_grid(
            [
                ("Model / Part Number", "ASUS Vivobook 15 M1502YA-BQ703WS  •  90NB0X21-M011U0 (Quiet Blue)"),
                ("Processor", "AMD Ryzen 7 5825U Mobile (8-core/16-thread, 16MB cache, up to 4.5 GHz)"),
                ("Graphics", "AMD Radeon Graphics (Integrated Vega 8)"),
                ("Display", "15.6\" (39.62 cm) FHD (1920x1080) 16:9 IPS-level, 60Hz, 250 nits, 45% NTSC"),
                ("Memory", "16 GB DDR4 (8GB On-board + 8GB SO-DIMM, expandable up to 24GB)"),
                ("Storage", "512 GB M.2 NVMe PCIe 3.0 x4 SSD"),
                ("Connectivity & Ports", "Wi-Fi 6E (1x1) + BT 5.3  •  1x USB-C 3.2 PD  •  2x USB-A 3.2  •  1x USB 2.0  •  HDMI 1.4"),
                ("Chassis & Durability", "1.70 kg  •  1.99 cm thin  •  180° Lay-Flat Hinge  •  US MIL-STD 810H"),
            ]
        )

    def _build_sensors(self):
        self._section_header(
            "Hardware Sensors",
            "Real-time Ryzen 7 5825U thermal, fan tachometer, and 45W rail telemetry",
        )
        self._info_grid(
            [
                ("Ryzen 7 5825U Tdie / Package", "54°C  •  14.8 W STAPM"),
                ("AMD Radeon Graphics Core", "49°C  •  3.2 W"),
                ("M.2 NVMe PCIe 3.0 SSD", "36°C"),
                ("ASUS IceBlade Fan", "2400 RPM"),
                ("42Wh 3S1P Battery Temp", "29.5°C"),
                ("45W AC Adapter Input", "19.0 V DC  •  2.37 A Max"),
            ]
        )

    def _build_settings(self):
        self._section_header(
            "Application Settings",
            "Startup behavior, telemetry polling rate, and OSD alerts",
        )
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=18,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        tk.Checkbutton(
            card,
            text="Launch minimized to system tray at Windows 11 / Linux login",
            variable=self.auto_start_var,
            bg=self.bg_card,
            fg=self.text_primary,
            selectcolor="#26262a",
            activebackground=self.bg_card,
            activeforeground=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Checkbutton(
            card,
            text="Display on-screen OSD overlay when pressing Fn+F or Fn+Esc",
            variable=self.osd_var,
            bg=self.bg_card,
            fg=self.text_primary,
            selectcolor="#26262a",
            activebackground=self.bg_card,
            activeforeground=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 14))

        tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=10)

        poll_row = tk.Frame(card, bg=self.bg_card)
        poll_row.pack(fill="x", pady=(6, 0))
        tk.Label(
            poll_row,
            text="Hardware Sensor Polling Interval (ms)",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        tk.Button(
            poll_row,
            text="Save",
            bg=self.accent,
            fg=self.accent_dark,
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=4,
            bd=0,
            cursor="hand2",
            command=lambda: self.show_toast(f"Polling interval set to {self.poll_ms_var.get()} ms"),
        ).pack(side="right", padx=(8, 0))

        poll_entry = tk.Entry(
            poll_row,
            textvariable=self.poll_ms_var,
            width=8,
            bg="#26262a",
            fg=self.text_primary,
            insertbackground=self.text_primary,
            font=("Consolas", 10, "bold"),
            bd=0,
            justify="right",
        )
        poll_entry.pack(side="right", ipady=4)

    def _info_grid(self, items):
        card = tk.Frame(
            self.content_area,
            bg=self.bg_card,
            padx=22,
            pady=16,
            highlightbackground=self.border_col,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=24)

        for idx, (k, v) in enumerate(items):
            if idx > 0:
                tk.Frame(card, bg=self.border_col, height=1).pack(fill="x", pady=11)
            row = tk.Frame(card, bg=self.bg_card)
            row.pack(fill="x")
            tk.Label(
                row,
                text=k,
                bg=self.bg_card,
                fg=self.text_muted,
                font=("Segoe UI", 10),
            ).pack(side="left")
            tk.Label(
                row,
                text=v,
                bg=self.bg_card,
                fg=self.text_primary,
                font=("Segoe UI", 10, "bold"),
            ).pack(side="right")


if __name__ == "__main__":
    app = SystemControlCenter()
    app.mainloop()