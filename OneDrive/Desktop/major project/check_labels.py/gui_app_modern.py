import customtkinter as ctk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import threading
import os
import subprocess
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageTk
import time
from detect_files import detect_files
from train_model import train_model
from utils import extract_features

# Set appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Cyber-purple accent

class HarmfulFileDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Harmful File Detector")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.folder_path = ctk.StringVar(value="")
        self.model_path = ctk.StringVar(value="model.pkl")
        self.scan_results = []
        self.model_accuracy = "N/A"
        self.is_scanning = False
        self.loading_window = None
        self.pie_canvas = None
        self.button_colors = {}
        self.current_tab = "Scan"

        # Animations
        self.title_alpha = 0.0
        self.footer_alpha = 0.0
        self.scanning_dots = 0
        self.animating = True
        self.rotation_angle = 0

        # Fixed theme
        self.current_theme = {
            "bg": "#0f1419",
            "fg": "#1a1a2e",
            "accent": "#00d4ff",
            "text": "#ffffff",
            "secondary_text": "#b0b0b0",
            "button_bg": "#8e44ad",
            "button_hover": "#9b59b6",
            "card_bg": "#16213e",
            "progress_color": "#00d4ff",
            "sidebar_bg": "#0d1117",
            "sidebar_hover": "#161b22"
        }
        self.current_color_theme = {
            "primary": "#8e44ad",
            "secondary": "#9b59b6",
            "accent": "#00d4ff",
            "danger": "#e74c3c",
            "success": "#27ae60",
            "warning": "#f39c12",
            "pie_safe": "#27ae60",
            "pie_harmful": "#e74c3c"
        }

        # Main layout: Sidebar + Content
        self.sidebar_frame = ctk.CTkFrame(self.root, fg_color=self.current_theme["sidebar_bg"], width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self.root, fg_color=self.current_theme["bg"], corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.content_frame.pack_propagate(False)

        # Sidebar buttons
        self.scan_tab_button = ctk.CTkButton(self.sidebar_frame, text="🧠 Scan", command=lambda: self.switch_tab("Scan"),
                                             fg_color="transparent", hover_color=self.current_theme["sidebar_hover"],
                                             corner_radius=0, font=ctk.CTkFont(size=14, weight="bold"))
        self.scan_tab_button.pack(fill="x", pady=(20, 5), padx=10)

        self.training_tab_button = ctk.CTkButton(self.sidebar_frame, text="🔄 Training", command=lambda: self.switch_tab("Training"),
                                                 fg_color="transparent", hover_color=self.current_theme["sidebar_hover"],
                                                 corner_radius=0, font=ctk.CTkFont(size=14, weight="bold"))
        self.training_tab_button.pack(fill="x", pady=5, padx=10)

        self.logs_tab_button = ctk.CTkButton(self.sidebar_frame, text="📋 Logs", command=lambda: self.switch_tab("Logs"),
                                             fg_color="transparent", hover_color=self.current_theme["sidebar_hover"],
                                             corner_radius=0, font=ctk.CTkFont(size=14, weight="bold"))
        self.logs_tab_button.pack(fill="x", pady=5, padx=10)

        # Content areas
        self.scan_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.training_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.logs_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")

        self.build_scan_tab()
        self.build_training_tab()
        self.build_logs_tab()

        self.switch_tab("Scan")

        # Start animations
        self.animate_title()
        self.animate_footer()

    def build_scan_tab(self):
        # Header
        self.header_frame = ctk.CTkFrame(self.scan_frame, fg_color=self.current_theme["fg"], corner_radius=25)
        self.header_frame.pack(pady=20, padx=20, fill="x")

        self.logo_label = ctk.CTkLabel(self.header_frame, text="🛡️", font=ctk.CTkFont(size=48, weight="bold"))
        self.logo_label.pack(side="left", padx=(25, 15), pady=15)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Harmful File Detector",
                                        font=ctk.CTkFont(size=36, weight="bold"), text_color=self.current_theme["accent"])
        self.title_label.pack(side="left", pady=15)
        self.title_label.bind("<Enter>", self.title_hover_enter)
        self.title_label.bind("<Leave>", self.title_hover_leave)

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="AI-powered malicious file scanner",
                                           font=ctk.CTkFont(size=18), text_color=self.current_theme["secondary_text"])
        self.subtitle_label.pack(side="left", padx=(15, 0), pady=15)

        # Folder & Model Controls
        self.controls_frame = ctk.CTkFrame(self.scan_frame, fg_color=self.current_theme["card_bg"], corner_radius=20)
        self.controls_frame.pack(pady=15, padx=20, fill="x")

        self.folder_label = ctk.CTkLabel(self.controls_frame, text="Select Folder to Scan:",
                                         font=ctk.CTkFont(size=16, weight="bold"), text_color=self.current_theme["text"])
        self.folder_label.pack(anchor="w", padx=25, pady=(20, 8))

        self.folder_entry = ctk.CTkEntry(self.controls_frame, textvariable=self.folder_path, width=700,
                                         corner_radius=12, font=ctk.CTkFont(size=14))
        self.folder_entry.pack(side="left", padx=(25, 10), pady=8)

        self.browse_button = ctk.CTkButton(self.controls_frame, text="📁 Browse Folder", command=self.browse_folder,
                                           fg_color=self.current_color_theme["primary"], hover_color=self.current_color_theme["secondary"],
                                           corner_radius=12, font=ctk.CTkFont(size=14, weight="bold"))
        self.browse_button.pack(side="left", padx=(0, 25), pady=8)
        self.browse_button.bind("<Enter>", lambda e: self.button_glow_enter(e, self.browse_button))
        self.browse_button.bind("<Leave>", lambda e: self.button_glow_leave(e, self.browse_button))

        self.model_label = ctk.CTkLabel(self.controls_frame, text="Model Path:",
                                        font=ctk.CTkFont(size=16, weight="bold"), text_color=self.current_theme["text"])
        self.model_label.pack(anchor="w", padx=25, pady=(15, 8))

        self.model_entry = ctk.CTkEntry(self.controls_frame, textvariable=self.model_path, width=700,
                                        corner_radius=12, font=ctk.CTkFont(size=14))
        self.model_entry.pack(side="left", padx=(25, 10), pady=8)

        self.model_note = ctk.CTkLabel(self.controls_frame, text="Using Pre-Trained Model",
                                       font=ctk.CTkFont(size=14, slant="italic"), text_color=self.current_theme["secondary_text"])
        self.model_note.pack(anchor="w", padx=25, pady=(8, 20))

        # Buttons
        self.buttons_frame = ctk.CTkFrame(self.scan_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=15, padx=20, fill="x")

        self.scan_button = ctk.CTkButton(self.buttons_frame, text="🧠 Start Scan", command=self.start_scan_thread,
                                         fg_color=self.current_color_theme["primary"], hover_color=self.current_color_theme["secondary"],
                                         corner_radius=18, font=ctk.CTkFont(size=16, weight="bold"))
        self.scan_button.pack(side="left", padx=(0, 15), pady=8)
        self.scan_button.bind("<Button-1>", lambda e: self.button_pulse(e, self.scan_button))
        self.scan_button.bind("<Enter>", lambda e: self.button_glow_enter(e, self.scan_button))
        self.scan_button.bind("<Leave>", lambda e: self.button_glow_leave(e, self.scan_button))

        self.quarantine_button = ctk.CTkButton(self.buttons_frame, text="🧹 Open Quarantine", command=self.open_quarantine,
                                               fg_color=self.current_color_theme["success"], hover_color="#229954",
                                               corner_radius=18, font=ctk.CTkFont(size=16, weight="bold"))
        self.quarantine_button.pack(side="left", padx=(0, 15), pady=8)
        self.quarantine_button.bind("<Button-1>", lambda e: self.button_pulse(e, self.quarantine_button))
        self.quarantine_button.bind("<Enter>", lambda e: self.button_glow_enter(e, self.quarantine_button))
        self.quarantine_button.bind("<Leave>", lambda e: self.button_glow_leave(e, self.quarantine_button))

        self.export_button = ctk.CTkButton(self.buttons_frame, text="💾 Export CSV", command=self.export_csv,
                                           fg_color=self.current_color_theme["warning"], hover_color="#e67e22",
                                           corner_radius=18, font=ctk.CTkFont(size=16, weight="bold"))
        self.export_button.pack(side="left", padx=(0, 15), pady=8)
        self.export_button.bind("<Button-1>", lambda e: self.button_pulse(e, self.export_button))
        self.export_button.bind("<Enter>", lambda e: self.button_glow_enter(e, self.export_button))
        self.export_button.bind("<Leave>", lambda e: self.button_glow_leave(e, self.export_button))

        # Progress & Logs
        self.progress_frame = ctk.CTkFrame(self.scan_frame, fg_color=self.current_theme["bg"], corner_radius=18)
        self.progress_frame.pack(pady=15, padx=20, fill="x")

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Progress:",
                                           font=ctk.CTkFont(size=16, weight="bold"), text_color=self.current_theme["text"])
        self.progress_label.pack(anchor="w", padx=25, pady=(20, 8))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=850, progress_color=self.current_theme["progress_color"])
        self.progress_bar.pack(pady=(0, 12), padx=25)
        self.progress_bar.set(0)

        self.scanning_label = ctk.CTkLabel(self.progress_frame, text="", font=ctk.CTkFont(size=14),
                                           text_color=self.current_theme["accent"])
        self.scanning_label.pack(anchor="w", padx=25, pady=(0, 12))

        self.logs_label = ctk.CTkLabel(self.progress_frame, text="Scan Logs:",
                                       font=ctk.CTkFont(size=16, weight="bold"), text_color=self.current_theme["text"])
        self.logs_label.pack(anchor="w", padx=25, pady=(12, 8))

        self.logs_textbox = ctk.CTkTextbox(self.progress_frame, width=850, height=160, wrap="word",
                                           fg_color=self.current_theme["fg"], corner_radius=12, font=ctk.CTkFont(size=12))
        self.logs_textbox.pack(pady=(0, 20), padx=25)

        # Stats Section
        self.stats_frame = ctk.CTkFrame(self.scan_frame, fg_color=self.current_theme["card_bg"], corner_radius=18)
        self.stats_frame.pack(pady=15, padx=20, fill="x")
        self.stats_frame.bind("<Enter>", lambda e: self.card_hover_enter(e, self.stats_frame))
        self.stats_frame.bind("<Leave>", lambda e: self.card_hover_leave(e, self.stats_frame))

        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Scan Summary",
                                        font=ctk.CTkFont(size=20, weight="bold"), text_color=self.current_theme["text"])
        self.stats_title.pack(pady=(20, 12))

        self.stats_inner_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        self.stats_inner_frame.pack(pady=(0, 12), padx=25, fill="x")

        # Stat cards
        self.files_scanned_card = ctk.CTkFrame(self.stats_inner_frame, fg_color=self.current_color_theme["primary"], corner_radius=12)
        self.files_scanned_card.pack(side="left", padx=(0, 12), pady=8, fill="y", expand=True)
        self.files_scanned_card.bind("<Enter>", lambda e: self.card_hover_enter(e, self.files_scanned_card))
        self.files_scanned_card.bind("<Leave>", lambda e: self.card_hover_leave(e, self.files_scanned_card))
        self.files_scanned_label = ctk.CTkLabel(self.files_scanned_card, text="Files Scanned: 0",
                                                font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        self.files_scanned_label.pack(pady=12)

        self.harmful_detected_card = ctk.CTkFrame(self.stats_inner_frame, fg_color=self.current_color_theme["danger"], corner_radius=12)
        self.harmful_detected_card.pack(side="left", padx=(0, 12), pady=8, fill="y", expand=True)
        self.harmful_detected_card.bind("<Enter>", lambda e: self.card_hover_enter(e, self.harmful_detected_card))
        self.harmful_detected_card.bind("<Leave>", lambda e: self.card_hover_leave(e, self.harmful_detected_card))
        self.harmful_detected_label = ctk.CTkLabel(self.harmful_detected_card, text="Harmful Detected: 0",
                                                   font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        self.harmful_detected_label.pack(pady=12)

        self.quarantined_card = ctk.CTkFrame(self.stats_inner_frame, fg_color=self.current_color_theme["success"], corner_radius=12)
        self.quarantined_card.pack(side="left", padx=(0, 12), pady=8, fill="y", expand=True)
        self.quarantined_card.bind("<Enter>", lambda e: self.card_hover_enter(e, self.quarantined_card))
        self.quarantined_card.bind("<Leave>", lambda e: self.card_hover_leave(e, self.quarantined_card))
        self.quarantined_label = ctk.CTkLabel(self.quarantined_card, text="Quarantined: 0",
                                              font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        self.quarantined_label.pack(pady=12)

        self.accuracy_card = ctk.CTkFrame(self.stats_inner_frame, fg_color=self.current_color_theme["warning"], corner_radius=12)
        self.accuracy_card.pack(side="left", padx=0, pady=8, fill="y", expand=True)
        self.accuracy_card.bind("<Enter>", lambda e: self.card_hover_enter(e, self.accuracy_card))
        self.accuracy_card.bind("<Leave>", lambda e: self.card_hover_leave(e, self.accuracy_card))
        self.accuracy_label = ctk.CTkLabel(self.accuracy_card, text=f"Model Accuracy: {self.model_accuracy}",
                                           font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        self.accuracy_label.pack(pady=12)

        # Pie chart frame
        self.pie_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        self.pie_frame.pack(pady=(12, 20), padx=25, fill="x")
        self.create_pie_chart()

        # Footer
        self.footer_label = ctk.CTkLabel(self.scan_frame, text="Developed by B5 — 2025",
                                         font=ctk.CTkFont(size=12), text_color=self.current_theme["secondary_text"])
        self.footer_label.pack(pady=10, anchor="e", padx=20)

    def build_training_tab(self):
        self.training_title = ctk.CTkLabel(self.training_frame, text="Model Training",
                                           font=ctk.CTkFont(size=36, weight="bold"), text_color=self.current_theme["accent"])
        self.training_title.pack(pady=(50, 20))

        self.retrain_button = ctk.CTkButton(self.training_frame, text="🔄 Retrain Model",
                                            command=self.retrain_thread, fg_color=self.current_color_theme["danger"], hover_color="#c0392b",
                                            corner_radius=18, font=ctk.CTkFont(size=16, weight="bold"))
        self.retrain_button.pack(pady=20)
        self.retrain_button.bind("<Button-1>", lambda e: self.button_pulse(e, self.retrain_button))
        self.retrain_button.bind("<Enter>", lambda e: self.button_glow_enter(e, self.retrain_button))
        self.retrain_button.bind("<Leave>", lambda e: self.button_glow_leave(e, self.retrain_button))

        self.training_logs_textbox = ctk.CTkTextbox(self.training_frame, width=800, height=400, wrap="word",
                                                    fg_color=self.current_theme["fg"], corner_radius=12, font=ctk.CTkFont(size=12))
        self.training_logs_textbox.pack(pady=20, padx=20)

    def build_logs_tab(self):
        self.logs_tab_title = ctk.CTkLabel(self.logs_frame, text="Application Logs",
                                           font=ctk.CTkFont(size=36, weight="bold"), text_color=self.current_theme["accent"])
        self.logs_tab_title.pack(pady=(50, 20))

        self.full_logs_textbox = ctk.CTkTextbox(self.logs_frame, width=800, height=500, wrap="word",
                                                fg_color=self.current_theme["fg"], corner_radius=12, font=ctk.CTkFont(size=12))
        self.full_logs_textbox.pack(pady=20, padx=20)

    def switch_tab(self, tab):
        self.current_tab = tab
        if tab == "Scan":
            self.scan_frame.pack(fill="both", expand=True)
            self.training_frame.pack_forget()
            self.logs_frame.pack_forget()
        elif tab == "Training":
            self.scan_frame.pack_forget()
            self.training_frame.pack(fill="both", expand=True)
            self.logs_frame.pack_forget()
        elif tab == "Logs":
            self.scan_frame.pack_forget()
            self.training_frame.pack_forget()
            self.logs_frame.pack(fill="both", expand=True)

    def create_pie_chart(self):
        fig, ax = plt.subplots(figsize=(4, 4), facecolor=self.current_theme["bg"])
        ax.pie([1, 1], labels=['Safe', 'Harmful'], autopct='%1.1f%%', colors=[self.current_color_theme["pie_safe"], self.current_color_theme["pie_harmful"]],
               textprops={'color': 'white'})
        ax.set_title('Scan Results', color='white')
        fig.patch.set_facecolor(self.current_theme["bg"])
        self.pie_canvas = FigureCanvasTkAgg(fig, master=self.pie_frame)
        self.pie_canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_pie_chart(self):
        try:
            if self.pie_canvas:
                safe = len(self.scan_results) - sum(1 for r in self.scan_results if r['prediction'] == 'Harmful')
                harmful = sum(1 for r in self.scan_results if r['prediction'] == 'Harmful')
                if safe + harmful > 0:
                    self.pie_canvas.figure.clear()
                    ax = self.pie_canvas.figure.add_subplot(111)
                    wedges, texts, autotexts = ax.pie([safe, harmful], labels=['Safe', 'Harmful'], autopct='%1.1f%%',
                                                       colors=[self.current_color_theme["pie_safe"], self.current_color_theme["pie_harmful"]], textprops={'color': 'white'})
                    ax.set_title('Scan Results', color='white')
                    self.pie_canvas.figure.patch.set_facecolor(self.current_theme["bg"])
                    # Animate
                    def animate(frame):
                        for wedge in wedges:
                            wedge.set_alpha(frame / 10)
                        return wedges
                    self.anim = FuncAnimation(self.pie_canvas.figure, animate, frames=10, interval=50, repeat=False)
                    self.pie_canvas.draw()
        except Exception as e:
            print(f"Error updating pie chart: {e}")

    def animate_title(self):
        if self.animating and self.title_alpha < 1.0:
            self.title_alpha += 0.05
            color = f"#{int(255 * self.title_alpha):02x}{int(212 * self.title_alpha):02x}{int(255 * self.title_alpha):02x}"
            self.title_label.configure(text_color=color)
            self.root.after(50, self.animate_title)

    def animate_footer(self):
        if self.animating and self.footer_alpha < 1.0:
            self.footer_alpha += 0.05
            color = f"#{int(102 * self.footer_alpha):02x}{int(102 * self.footer_alpha):02x}{int(102 * self.footer_alpha):02x}"
            self.footer_label.configure(text_color=color)
            self.root.after(50, self.animate_footer)

    def title_hover_enter(self, event):
        self.title_label.configure(text_color="#00ffff")

    def title_hover_leave(self, event):
        self.title_label.configure(text_color="#00d4ff")

    def button_pulse(self, event, button):
        # Store original fg_color if not already stored
        if not hasattr(button, '_original_fg_color'):
            button._original_fg_color = button.cget('fg_color')
        original_fg_color = button._original_fg_color
        button.configure(fg_color="#ffffff")
        self.root.after(100, lambda: button.configure(fg_color=original_fg_color))

    def button_glow_enter(self, event, button):
        button.configure(border_width=2, border_color=self.current_color_theme["accent"])

    def button_glow_leave(self, event, button):
        button.configure(border_width=0)

    def card_hover_enter(self, event, card):
        card.configure(corner_radius=15)  # Slight scale effect

    def card_hover_leave(self, event, card):
        card.configure(corner_radius=12)

    def toggle_theme_smooth(self):
        if self.theme_transitioning:
            return
        self.theme_transitioning = True
        mode = self.appearance_var.get()
        ctk.set_appearance_mode(mode)
        self.fade_theme_transition()

    def fade_theme_transition(self):
        # Simple fade by updating colors gradually
        steps = 10
        for i in range(steps):
            alpha = (i + 1) / steps
            self.root.after(i * 50, lambda a=alpha: self.update_theme_partial(a))
        self.root.after(steps * 50, self.finalize_theme_transition)

    def update_theme_partial(self, alpha):
        # Interpolate colors
        pass  # For simplicity, just update at end

    def finalize_theme_transition(self):
        self.update_theme_colors()
        self.theme_transitioning = False

    def change_color_theme(self, theme):
        self.current_color_theme = self.color_themes[theme]
        self.update_color_theme_colors()

    def update_theme_colors(self):
        mode = self.appearance_var.get()
        self.current_theme = self.themes[mode]
        # Update all components
        self.sidebar_frame.configure(fg_color=self.current_theme["sidebar_bg"])
        self.content_frame.configure(fg_color=self.current_theme["bg"])
        self.header_frame.configure(fg_color=self.current_theme["fg"])
        self.title_label.configure(text_color=self.current_theme["accent"])
        self.subtitle_label.configure(text_color=self.current_theme["secondary_text"])
        self.controls_frame.configure(fg_color=self.current_theme["card_bg"])
        self.folder_label.configure(text_color=self.current_theme["text"])
        self.model_label.configure(text_color=self.current_theme["text"])
        self.model_note.configure(text_color=self.current_theme["secondary_text"])
        self.progress_frame.configure(fg_color=self.current_theme["bg"])
        self.progress_label.configure(text_color=self.current_theme["text"])
        self.progress_bar.configure(progress_color=self.current_theme["progress_color"])
        self.scanning_label.configure(text_color=self.current_theme["accent"])
        self.logs_label.configure(text_color=self.current_theme["text"])
        self.logs_textbox.configure(fg_color=self.current_theme["fg"])
        self.stats_frame.configure(fg_color=self.current_theme["card_bg"])
        self.stats_title.configure(text_color=self.current_theme["text"])
        self.footer_label.configure(text_color=self.current_theme["secondary_text"])
        self.training_title.configure(text_color=self.current_theme["accent"])
        self.training_logs_textbox.configure(fg_color=self.current_theme["fg"])
        self.logs_tab_title.configure(text_color=self.current_theme["accent"])
        self.full_logs_textbox.configure(fg_color=self.current_theme["fg"])
        if self.pie_canvas:
            self.pie_canvas.figure.patch.set_facecolor(self.current_theme["bg"])
            self.pie_canvas.draw()
        self.update_color_theme_colors()

    def update_color_theme_colors(self):
        self.scan_button.configure(fg_color=self.current_color_theme["primary"], hover_color=self.current_color_theme["secondary"])
        self.retrain_button.configure(fg_color=self.current_color_theme["danger"], hover_color="#c0392b")
        self.quarantine_button.configure(fg_color=self.current_color_theme["success"], hover_color="#229954")
        self.export_button.configure(fg_color=self.current_color_theme["warning"], hover_color="#e67e22")
        self.browse_button.configure(fg_color=self.current_color_theme["primary"], hover_color=self.current_color_theme["secondary"])
        self.files_scanned_card.configure(fg_color=self.current_color_theme["primary"])
        self.harmful_detected_card.configure(fg_color=self.current_color_theme["danger"])
        self.quarantined_card.configure(fg_color=self.current_color_theme["success"])
        self.accuracy_card.configure(fg_color=self.current_color_theme["warning"])
        self.color_dropdown.configure(fg_color=self.current_color_theme["primary"], button_color=self.current_color_theme["secondary"])
        self.update_pie_chart()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_scan_thread(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder to scan.")
            return
        if not os.path.exists(self.model_path.get()):
            messagebox.showerror("Error", "Model file not found.")
            return
        self.scan_button.configure(state="disabled")
        self.logs_textbox.delete("0.0", "end")
        self.progress_bar.set(0)
        self.scan_results = []
        self.is_scanning = True
        self.show_loading_overlay()
        self.animate_scanning_dots()
        thread = threading.Thread(target=self.start_scan)
        thread.start()

    def show_loading_overlay(self):
        self.loading_window = ctk.CTkToplevel(self.root)
        self.loading_window.geometry("400x300")
        self.loading_window.title("")
        self.loading_window.resizable(False, False)
        self.loading_window.attributes("-topmost", True)
        self.loading_window.overrideredirect(True)
        self.loading_window.geometry(f"+{self.root.winfo_x() + 500}+{self.root.winfo_y() + 300}")

        loading_frame = ctk.CTkFrame(self.loading_window, fg_color="#1a1a2e", corner_radius=20)
        loading_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.loading_canvas = ctk.CTkCanvas(loading_frame, width=100, height=100, bg="#1a1a2e", highlightthickness=0)
        self.loading_canvas.pack(pady=(20, 10))
        self.shield_image = Image.open("shield.png") if os.path.exists("shield.png") else None  # Assume shield image exists
        self.shield_photo = None
        if self.shield_image:
            self.shield_photo = ImageTk.PhotoImage(self.shield_image.resize((80, 80)))
            self.loading_canvas.create_image(50, 50, image=self.shield_photo)
        self.animate_rotation()

        self.loading_text = ctk.CTkLabel(loading_frame, text="Scanning...", font=ctk.CTkFont(size=16))
        self.loading_text.pack(pady=(0, 20))

    def animate_rotation(self):
        if self.is_scanning and self.loading_canvas:
            self.rotation_angle += 10
            if self.shield_photo:
                rotated = self.shield_image.rotate(self.rotation_angle).resize((80, 80))
                self.shield_photo = ImageTk.PhotoImage(rotated)
                self.loading_canvas.create_image(50, 50, image=self.shield_photo)
            self.root.after(100, self.animate_rotation)

    def animate_scanning_dots(self):
        if self.is_scanning:
            dots = "." * ((self.scanning_dots % 3) + 1)
            self.scanning_label.configure(text=f"Scanning{dots}")
            self.scanning_dots += 1
            self.root.after(500, self.animate_scanning_dots)

    def start_scan(self):
        # Same logic as original
        folder = self.folder_path.get()
        model = self.model_path.get()
        quarantine_path = os.path.join(folder, 'quarantine')

        if not os.path.exists(model):
            self.update_logs("Model not found. Please train the model first.\n")
            self.root.after(0, lambda: self.scan_button.configure(state="normal"))
            self.is_scanning = False
            self.hide_loading_overlay()
            return

        artifact = joblib.load(model)
        if isinstance(artifact, dict) and 'model' in artifact and 'columns' in artifact:
            model_obj = artifact['model']
            trained_columns = artifact['columns']
        else:
            model_obj = artifact
            trained_columns = None

        os.makedirs(quarantine_path, exist_ok=True)

        results = []
        file_count = 0
        total_files = sum([len(files) for r, d, files in os.walk(folder) if not r.startswith(quarantine_path)])

        for root, dirs, files in os.walk(folder):
            if os.path.abspath(root).startswith(os.path.abspath(quarantine_path)):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                file_count += 1
                timestamp = time.strftime("%H:%M:%S")
                self.update_logs(f"[{timestamp}] Processing file {file_count}: {file_path}\n")
                self.update_progress(file_count / total_files)
                try:
                    features = extract_features(file_path)
                    df = pd.DataFrame([features])

                    if 'file_extension' in df.columns:
                        df = pd.get_dummies(df, columns=['file_extension'])

                    df = df.fillna(0)

                    if trained_columns is not None:
                        df = df.reindex(columns=trained_columns, fill_value=0)
                    else:
                        expected = getattr(model_obj, "n_features_in_", None)
                        if expected and df.shape[1] < expected:
                            for i in range(expected - df.shape[1]):
                                df[f'extra_{i}'] = 0
                        if expected and df.shape[1] > expected:
                            df = df.iloc[:, :expected]

                    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

                    prediction = model_obj.predict(df)[0]

                    probability = 0.0
                    try:
                        proba = model_obj.predict_proba(df)[0]
                        classes = list(model_obj.classes_)
                        if 1 in classes:
                            idx = classes.index(1)
                            probability = float(proba[idx])
                        else:
                            probability = float(max(proba))
                    except Exception:
                        pass

                    if int(prediction) == 1:
                        dest = os.path.join(quarantine_path, os.path.basename(file_path))
                        try:
                            import shutil
                            shutil.move(file_path, dest)
                            status = "Quarantined"
                        except Exception as e:
                            status = f"QuarantineFailed: {str(e)}"
                    else:
                        status = "Safe"

                    result = {
                        'file': file_path,
                        'prediction': 'Harmful' if int(prediction) == 1 else 'Safe',
                        'probability': probability,
                        'status': status
                    }
                    results.append(result)
                    self.update_logs(f"[{timestamp}] {result['file']}: {result['prediction']} (Prob: {result['probability']:.2f}) - {result['status']}\n")

                except Exception as e:
                    self.update_logs(f"[{timestamp}] Error processing {file_path}: {str(e)}\n")
                    results.append({
                        'file': file_path,
                        'prediction': 'Error',
                        'probability': 0.0,
                        'status': f'Error: {str(e)}'
                    })

        self.scan_results = results
        self.root.after(0, lambda: self.update_stats())
        self.root.after(0, lambda: self.update_pie_chart())
        timestamp = time.strftime("%H:%M:%S")
        self.update_logs(f"[{timestamp}] Scan complete: {len(results)} files scanned, {sum(1 for r in results if r['prediction'] == 'Harmful')} harmful quarantined.\n")
        self.show_toast("Scan Complete", f"Scan complete: {len(results)} files scanned, {sum(1 for r in results if r['prediction'] == 'Harmful')} harmful quarantined.")
        self.root.after(0, lambda: self.scan_button.configure(state="normal"))
        self.is_scanning = False
        self.hide_loading_overlay()

    def retrain_thread(self):
        self.retrain_button.configure(state="disabled")
        thread = threading.Thread(target=self.retrain_model)
        thread.start()

    def retrain_model(self):
        try:
            ember_path = 'train_ember_2018_v2_features.parquet'
            if os.path.exists(ember_path):
                train_model(ember_path=ember_path)
            else:
                messagebox.showerror("Error", "EMBER dataset not found.")
                self.root.after(0, lambda: self.retrain_button.configure(state="normal"))
                return
            self.update_logs_training("Model retrained successfully.\n")
            self.show_toast("Success", "Model retrained and saved as model.pkl.")
        except Exception as e:
            self.update_logs_training(f"Error retraining model: {str(e)}\n")
            self.show_toast("Error", f"Error retraining model: {str(e)}")
        self.root.after(0, lambda: self.retrain_button.configure(state="normal"))

    def open_quarantine(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return
        quarantine_path = os.path.join(folder, 'quarantine')
        if os.path.exists(quarantine_path):
            try:
                if os.name == 'nt':
                    os.startfile(quarantine_path)
                else:
                    subprocess.run(['xdg-open', quarantine_path])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open quarantine folder: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Quarantine folder does not exist yet.")

    def export_csv(self):
        if not self.scan_results:
            messagebox.showwarning("Warning", "No scan results to export.")
            return
        try:
            df = pd.DataFrame(self.scan_results)
            df.to_csv('scan_results.csv', index=False)
            self.show_toast("Success", "Scan results saved to scan_results.csv")
        except Exception as e:
            self.show_toast("Error", f"Error exporting CSV: {str(e)}")

    def update_logs(self, text):
        self.root.after(0, lambda: self.logs_textbox.insert("end", text))
        self.root.after(0, lambda: self.logs_textbox.see("end"))

    def update_logs_training(self, text):
        self.root.after(0, lambda: self.training_logs_textbox.insert("end", text))
        self.root.after(0, lambda: self.training_logs_textbox.see("end"))

    def update_progress(self, value):
        self.root.after(0, lambda: self.progress_bar.set(value))

    def update_stats(self):
        files_scanned = len(self.scan_results)
        harmful_detected = sum(1 for r in self.scan_results if r['prediction'] == 'Harmful')
        quarantined = sum(1 for r in self.scan_results if r['status'] == 'Quarantined')
        self.root.after(0, lambda: self.files_scanned_label.configure(text=f"Files Scanned: {files_scanned}"))
        self.root.after(0, lambda: self.harmful_detected_label.configure(text=f"Harmful Detected: {harmful_detected}"))
        self.root.after(0, lambda: self.quarantined_label.configure(text=f"Quarantined: {quarantined}"))
        try:
            artifact = joblib.load(self.model_path.get())
            if isinstance(artifact, dict) and 'model' in artifact:
                model = artifact['model']
            else:
                model = artifact
            self.model_accuracy = "N/A"
        except:
            self.model_accuracy = "N/A"
        self.root.after(0, lambda: self.accuracy_label.configure(text=f"Model Accuracy: {self.model_accuracy}"))

    def hide_loading_overlay(self):
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None
        self.scanning_label.configure(text="")

    def show_toast(self, title, message):
        toast = ctk.CTkToplevel(self.root)
        toast.geometry("350x120")
        toast.title("")
        toast.resizable(False, False)
        toast.attributes("-topmost", True)
        toast.overrideredirect(True)
        # Center the toast
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 60
        toast.geometry(f"+{x}+{y}")

        # Frosted glass effect with semi-transparent background
        bg_color = "#27ae60" if title == "Success" else "#e74c3c"
        toast_frame = ctk.CTkFrame(toast, fg_color=bg_color, corner_radius=20)
        toast_frame.pack(fill="both", expand=True, padx=10, pady=10)

        toast_title = ctk.CTkLabel(toast_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        toast_title.pack(pady=(15, 5))

        toast_message = ctk.CTkLabel(toast_frame, text=message, font=ctk.CTkFont(size=14))
        toast_message.pack(pady=(0, 15))

        # Fade in animation
        self.fade_in_toast(toast_frame)
        # Auto disappear after 3s with fade out
        self.root.after(3000, lambda: self.fade_out_toast(toast))

    def fade_in_toast(self, frame):
        # Simple fade in by gradually increasing opacity (not perfect, but for demo)
        pass  # CustomTkinter doesn't support alpha easily, so skip for now

    def fade_out_toast(self, toast):
        # Fade out
        toast.destroy()

    def on_closing(self):
        self.animating = False
        self.root.quit()

if __name__ == "__main__":
    root = ctk.CTk()
    app = HarmfulFileDetectorApp(root)
    root.mainloop()
