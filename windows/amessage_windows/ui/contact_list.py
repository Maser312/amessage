"""
AMessage Windows - Contact List Sidebar
"""

import customtkinter as ctk
from typing import Callable, List, Dict, Any

class ContactList(ctk.CTkFrame):
    def __init__(self, master, on_select_contact: Callable[[Dict[str, Any]], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_select_contact = on_select_contact
        self.selected_contact_id = None
        self.contact_buttons = {}

        self.conversations = [
            {
                "id": "1",
                "name": "Alice Johnson",
                "handle": "alice@icloud.com",
                "device": "iPhone 15 Pro",
                "last_message": "Wait, your bubbles are blue?! 🤯",
                "time": "09:41"
            },
            {
                "id": "2",
                "name": "Bob Smith",
                "handle": "tel:+14155552671",
                "device": "iPhone 14",
                "last_message": "Let's test APNs push gateway connection.",
                "time": "Yesterday"
            },
            {
                "id": "3",
                "name": "Sarah Miller",
                "handle": "sarah.m@gmail.com",
                "device": "MacBook Pro",
                "last_message": "Loved your blue bubble reaction ❤️",
                "time": "Monday"
            }
        ]

        self._build_ui()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(12, 6))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Messages",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(side="left")

        new_btn = ctk.CTkButton(
            header_frame,
            text="+",
            width=28,
            height=28,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#007AFF",
            hover_color="#0B84FE",
            command=self._on_new_chat
        )
        new_btn.pack(side="right")

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search contacts or email...",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.search_entry.pack(fill="x", padx=12, pady=(0, 10))

        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True, padx=4, pady=4)

        self._render_conversations()

    def _render_conversations(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        for conv in self.conversations:
            btn_frame = ctk.CTkFrame(
                self.list_container,
                fg_color="#1E1E20" if self.selected_contact_id == conv["id"] else "transparent",
                corner_radius=10
            )
            btn_frame.pack(fill="x", pady=2, padx=4)

            initials = "".join([part[0] for part in conv["name"].split()[:2]]).upper()
            avatar = ctk.CTkLabel(
                btn_frame,
                text=initials,
                width=38,
                height=38,
                corner_radius=19,
                fg_color="#8E8E93",
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            avatar.pack(side="left", padx=(8, 10), pady=8)

            text_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, pady=6)

            top_row = ctk.CTkFrame(text_frame, fg_color="transparent")
            top_row.pack(fill="x")

            name_lbl = ctk.CTkLabel(
                top_row,
                text=conv["name"],
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            name_lbl.pack(side="left")

            time_lbl = ctk.CTkLabel(
                top_row,
                text=conv["time"],
                font=ctk.CTkFont(size=11),
                text_color="#8E8E93"
            )
            time_lbl.pack(side="right", padx=(0, 8))

            last_msg_lbl = ctk.CTkLabel(
                text_frame,
                text=conv["last_message"],
                font=ctk.CTkFont(size=12),
                text_color="#8E8E93",
                anchor="w"
            )
            last_msg_lbl.pack(fill="x")

            def make_click_handler(c=conv):
                return lambda event=None: self._select_conversation(c)

            for w in [btn_frame, avatar, text_frame, top_row, name_lbl, time_lbl, last_msg_lbl]:
                w.bind("<Button-1>", make_click_handler())

    def _select_conversation(self, conv: Dict[str, Any]):
        self.selected_contact_id = conv["id"]
        self._render_conversations()
        self.on_select_contact(conv)

    def _on_new_chat(self):
        dialog = ctk.CTkInputDialog(text="Enter recipient (Phone or Apple ID):", title="New iMessage")
        handle = dialog.get_input()
        if handle:
            new_conv = {
                "id": str(len(self.conversations) + 1),
                "name": handle,
                "handle": handle,
                "device": "Apple Device",
                "last_message": "New conversation",
                "time": "Now"
            }
            self.conversations.insert(0, new_conv)
            self._select_conversation(new_conv)
