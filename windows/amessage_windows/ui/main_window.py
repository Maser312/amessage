"""
AMessage Windows - Main Application Window
"""

import customtkinter as ctk
from typing import Dict, Any

from .contact_list import ContactList
from .chat_view import ChatView
from .debug_panel import DebugPanel
from .settings_dialog import SettingsDialog

class MainWindow(ctk.CTk):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge

        self.title("AMessage — iMessage for Windows (E2EE Native Client)")
        self.geometry("1100x720")
        self.minsize(900, 600)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self._build_ui()
        self._setup_bridge_events()

    def _build_ui(self):
        self.nav_bar = ctk.CTkFrame(self, height=44, corner_radius=0)
        self.nav_bar.pack(fill="x", side="top")

        brand_lbl = ctk.CTkLabel(
            self.nav_bar,
            text="🍏 AMessage",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        brand_lbl.pack(side="left", padx=16)

        self.tab_selector = ctk.CTkSegmentedButton(
            self.nav_bar,
            values=["💬 Messages", "🔬 Protocol Debugger"],
            command=self._switch_view,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.tab_selector.set("💬 Messages")
        self.tab_selector.pack(side="left", padx=20)

        self.status_dot = ctk.CTkLabel(
            self.nav_bar,
            text="● APNs Online",
            font=ctk.CTkFont(size=12),
            text_color="#34C759"
        )
        self.status_dot.pack(side="right", padx=(6, 16))

        settings_btn = ctk.CTkButton(
            self.nav_bar,
            text="⚙ Settings",
            width=80,
            height=28,
            fg_color="transparent",
            hover_color=("#E5E5EA", "#2C2C2E"),
            font=ctk.CTkFont(size=12),
            command=self._open_settings
        )
        settings_btn.pack(side="right", padx=6)

        theme_btn = ctk.CTkButton(
            self.nav_bar,
            text="🌓",
            width=32,
            height=28,
            fg_color="transparent",
            hover_color=("#E5E5EA", "#2C2C2E"),
            command=self._toggle_theme
        )
        theme_btn.pack(side="right", padx=4)

        self.view_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True)

        self.messages_view = ctk.CTkFrame(self.view_container, corner_radius=0, fg_color="transparent")
        
        self.contact_list = ContactList(
            self.messages_view,
            on_select_contact=self._on_contact_selected,
            width=280,
            corner_radius=0
        )
        self.contact_list.pack(side="left", fill="y")

        self.chat_view = ChatView(
            self.messages_view,
            on_send_message=self._on_send_message,
            on_send_tapback=self._on_send_tapback,
            corner_radius=0,
            fg_color="transparent"
        )
        self.chat_view.pack(side="right", fill="both", expand=True)

        self.debug_panel = DebugPanel(
            self.view_container,
            bridge=self.bridge,
            corner_radius=0,
            fg_color="transparent"
        )

        self.messages_view.pack(fill="both", expand=True)

        if self.contact_list.conversations:
            first = self.contact_list.conversations[0]
            self.contact_list._select_conversation(first)

    def _switch_view(self, value: str):
        if "Messages" in value:
            self.debug_panel.pack_forget()
            self.messages_view.pack(fill="both", expand=True)
        else:
            self.messages_view.pack_forget()
            self.debug_panel.pack(fill="both", expand=True)

    def _on_contact_selected(self, contact: Dict[str, Any]):
        self.chat_view.set_contact(contact)

    def _on_send_message(self, recipient: str, text: str):
        self.bridge.send_message(recipient, text)

    def _on_send_tapback(self, recipient: str, target_guid: str, reaction_type: int):
        self.bridge.send_tapback(recipient, target_guid, reaction_type)

    def _open_settings(self):
        SettingsDialog(self, self.bridge, on_save_callback=lambda: None)

    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

    def _setup_bridge_events(self):
        def _handle_incoming_message(msg):
            if self.chat_view.current_contact:
                handle = self.chat_view.current_contact["handle"]
                if handle in msg.sender or msg.sender in handle:
                    self.chat_view.add_message(msg.text, is_from_me=False)

        self.bridge.register_message_callback(_handle_incoming_message)
