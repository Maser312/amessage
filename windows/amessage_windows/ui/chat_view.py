"""
AMessage Windows - Chat View with Blue Bubbles & Tapbacks
"""

import customtkinter as ctk
import time
from typing import Callable, Optional, Dict, Any, List

class ChatView(ctk.CTkFrame):
    def __init__(self, master, on_send_message: Callable[[str, str], None], on_send_tapback: Callable[[str, str, int], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_send_message = on_send_message
        self.on_send_tapback = on_send_tapback
        self.current_contact: Optional[Dict[str, Any]] = None
        self.messages: List[Dict[str, Any]] = []

        self._build_ui()

    def _build_ui(self):
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("#F2F2F7", "#1A1A1C"))
        self.header_frame.pack(fill="x", side="top")

        self.contact_name_lbl = ctk.CTkLabel(
            self.header_frame,
            text="Select a conversation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.contact_name_lbl.pack(pady=(8, 0))

        self.contact_sub_lbl = ctk.CTkLabel(
            self.header_frame,
            text="iMessage • End-to-End Encrypted",
            font=ctk.CTkFont(size=11),
            text_color="#8E8E93"
        )
        self.contact_sub_lbl.pack(pady=(0, 6))

        self.input_frame = ctk.CTkFrame(self, height=54, corner_radius=0, fg_color=("#F7F7F7", "#161618"))
        self.input_frame.pack(fill="x", side="bottom", padx=10, pady=8)

        self.react_btn = ctk.CTkButton(
            self.input_frame,
            text="❤️",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="transparent",
            hover_color=("#E5E5EA", "#2C2C2E"),
            font=ctk.CTkFont(size=16),
            command=self._show_tapback_menu
        )
        self.react_btn.pack(side="left", padx=(4, 6))

        self.msg_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="iMessage",
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(size=14)
        )
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.msg_entry.bind("<Return>", lambda event: self._send_current())

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="↑",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="#007AFF",
            hover_color="#0B84FE",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self._send_current
        )
        self.send_btn.pack(side="right", padx=(0, 4))

        self.messages_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.messages_scroll.pack(fill="both", expand=True, padx=12, pady=8)

    def set_contact(self, contact: Dict[str, Any]):
        self.current_contact = contact
        self.contact_name_lbl.configure(text=f"{contact['name']} ({contact.get('device', 'iPhone')})")
        self.contact_sub_lbl.configure(text=f"iMessage ({contact['handle']}) • E2EE Active")

        self.messages = [
            {
                "id": "1",
                "text": "Hey! You're showing up with blue bubbles from Windows?! 🍏",
                "is_from_me": False,
                "time": "09:30",
                "tapback": None
            },
            {
                "id": "2",
                "text": "Yes! Running AMessage Windows with direct APNs push socket & P-256 encryption. Zero Mac required!",
                "is_from_me": True,
                "time": "09:31",
                "tapback": "❤️"
            },
            {
                "id": "3",
                "text": "That's insane. Do Tapbacks and delivery receipts sync seamlessly?",
                "is_from_me": False,
                "time": "09:32",
                "tapback": None
            }
        ]
        self._render_messages()

    def add_message(self, text: str, is_from_me: bool = True, tapback: Optional[str] = None):
        msg = {
            "id": str(len(self.messages) + 1),
            "text": text,
            "is_from_me": is_from_me,
            "time": time.strftime("%H:%M"),
            "tapback": tapback
        }
        self.messages.append(msg)
        self._render_messages()

    def _render_messages(self):
        for widget in self.messages_scroll.winfo_children():
            widget.destroy()

        for msg in self.messages:
            row_frame = ctk.CTkFrame(self.messages_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            align = "right" if msg["is_from_me"] else "left"
            bubble_color = "#007AFF" if msg["is_from_me"] else ("#E9E9EB", "#26252A")
            text_color = "white" if (msg["is_from_me"] or ctk.get_appearance_mode() == "Dark") else "black"

            bubble_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            bubble_container.pack(side=align, padx=10)

            bubble = ctk.CTkLabel(
                bubble_container,
                text=msg["text"],
                corner_radius=16,
                fg_color=bubble_color,
                text_color=text_color,
                font=ctk.CTkFont(size=14),
                wraplength=480,
                justify="left",
                padx=14,
                pady=10
            )
            bubble.pack(side="top", anchor="e" if msg["is_from_me"] else "w")

            if msg.get("tapback"):
                badge = ctk.CTkLabel(
                    bubble_container,
                    text=msg["tapback"],
                    width=24,
                    height=24,
                    corner_radius=12,
                    fg_color=("#F2F2F7", "#333336"),
                    font=ctk.CTkFont(size=13)
                )
                badge.pack(side="top", anchor="e" if msg["is_from_me"] else "w", pady=(0, 2))

            if msg["is_from_me"]:
                status_lbl = ctk.CTkLabel(
                    bubble_container,
                    text="Delivered",
                    font=ctk.CTkFont(size=10),
                    text_color="#8E8E93"
                )
                status_lbl.pack(side="top", anchor="e")

        self.messages_scroll._parent_canvas.yview_moveto(1.0)

    def _send_current(self):
        text = self.msg_entry.get().strip()
        if not text:
            return
        if not self.current_contact:
            return

        self.add_message(text, is_from_me=True)
        self.msg_entry.delete(0, "end")
        self.on_send_message(self.current_contact["handle"], text)

    def _show_tapback_menu(self):
        if not self.current_contact or not self.messages:
            return
        last_msg = self.messages[-1]
        last_msg["tapback"] = "❤️" if last_msg.get("tapback") != "❤️" else None
        self._render_messages()
        self.on_send_tapback(self.current_contact["handle"], last_msg["id"], 2000)
