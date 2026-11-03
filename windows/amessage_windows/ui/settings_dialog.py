"""
AMessage Windows - Settings & Apple ID Manager
"""

import customtkinter as ctk

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, master, bridge, on_save_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.bridge = bridge
        self.on_save = on_save_callback

        self.title("AMessage Settings & Apple ID")
        self.geometry("460x380")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        title_lbl = ctk.CTkLabel(
            container,
            text="Account & Relay Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_lbl.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(container, text="Apple ID (Email or Phone):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.apple_id_entry = ctk.CTkEntry(container, placeholder_text="user@icloud.com", height=34)
        self.apple_id_entry.pack(fill="x", pady=(2, 10))
        if self.bridge.ids.user_id:
            self.apple_id_entry.insert(0, self.bridge.ids.user_id)

        ctk.CTkLabel(container, text="Apple ID Password (Optional in test mode):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.pwd_entry = ctk.CTkEntry(container, placeholder_text="••••••••••••", show="*", height=34)
        self.pwd_entry.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(container, text="Validation Relay Server URL (Leave blank for built-in SMBIOS):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.relay_entry = ctk.CTkEntry(container, placeholder_text="http://localhost:8080", height=34)
        self.relay_entry.pack(fill="x", pady=(2, 15))
        if self.bridge.relay_url:
            self.relay_entry.insert(0, self.bridge.relay_url)

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save & Reconnect",
            fg_color="#007AFF",
            hover_color="#0B84FE",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save
        )
        save_btn.pack(side="right")

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="transparent",
            text_color="#8E8E93",
            hover_color=("#E5E5EA", "#2C2C2E"),
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def _save(self):
        apple_id = self.apple_id_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        relay = self.relay_entry.get().strip()

        if apple_id:
            self.bridge.ids.authenticate_apple_id(apple_id, pwd)
        if relay:
            self.bridge.relay_url = relay
            self.bridge.anisette.relay_url = relay

        self.bridge.connect()
        self.on_save()
        self.destroy()
