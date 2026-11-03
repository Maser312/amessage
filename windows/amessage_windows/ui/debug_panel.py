"""
AMessage Windows - Protocol Debugger & Inspector Panel
"""

import customtkinter as ctk
import time
import socket
import ssl

class DebugPanel(ctk.CTkFrame):
    def __init__(self, master, bridge, **kwargs):
        super().__init__(master, **kwargs)
        self.bridge = bridge

        self._build_ui()
        self._start_event_listener()

    def _build_ui(self):
        toolbar = ctk.CTkFrame(self, height=44, fg_color="transparent")
        toolbar.pack(fill="x", padx=12, pady=8)

        lbl = ctk.CTkLabel(
            toolbar,
            text="iMessage Protocol Debugger",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl.pack(side="left")

        ping_btn = ctk.CTkButton(
            toolbar,
            text="Test APNs Socket",
            width=130,
            height=30,
            fg_color="#34C759",
            hover_color="#30B753",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._test_apns_socket
        )
        ping_btn.pack(side="right", padx=(6, 0))

        sim_btn = ctk.CTkButton(
            toolbar,
            text="Simulate Incoming Push",
            width=160,
            height=30,
            fg_color="#5856D6",
            hover_color="#4F4DC7",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._simulate_incoming_push
        )
        sim_btn.pack(side="right", padx=(6, 0))

        clear_btn = ctk.CTkButton(
            toolbar,
            text="Clear",
            width=60,
            height=30,
            fg_color="#8E8E93",
            hover_color="#636366",
            font=ctk.CTkFont(size=12),
            command=self._clear_logs
        )
        clear_btn.pack(side="right", padx=(6, 0))

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.left_col = ctk.CTkFrame(content_frame, width=320, corner_radius=10)
        self.left_col.pack(side="left", fill="y", padx=(0, 8))

        hw_title = ctk.CTkLabel(
            self.left_col,
            text="Hardware & SMBIOS Spoof",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        hw_title.pack(anchor="w", padx=12, pady=(12, 6))

        self.hw_info_text = ctk.CTkTextbox(
            self.left_col,
            width=300,
            font=ctk.CTkFont(family="Consolas", size=11),
            activate_scrollbars=True
        )
        self.hw_info_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._update_hw_info()

        self.right_col = ctk.CTkFrame(content_frame, corner_radius=10)
        self.right_col.pack(side="right", fill="both", expand=True)

        log_title = ctk.CTkLabel(
            self.right_col,
            text="Live Protocol Packet & Cryptographic Stream",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        log_title.pack(anchor="w", padx=12, pady=(12, 6))

        self.log_text = ctk.CTkTextbox(
            self.right_col,
            font=ctk.CTkFont(family="Consolas", size=12),
            activate_scrollbars=True
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text.tag_config("TIME", foreground="#8E8E93")
        self.log_text.tag_config("APNS", foreground="#007AFF")
        self.log_text.tag_config("IDS", foreground="#34C759")
        self.log_text.tag_config("CRYPTO", foreground="#AF52DE")
        self.log_text.tag_config("PROTO", foreground="#FF9500")
        self.log_text.tag_config("SUCCESS", foreground="#34C759")
        self.log_text.tag_config("WARNING", foreground="#FFCC00")
        self.log_text.tag_config("ERROR", foreground="#FF3B30")

    def _update_hw_info(self):
        profile = self.bridge.anisette.profile
        lines = [
            f"Model       : {profile.model}",
            f"Serial No   : {profile.serial_number}",
            f"Board-ID    : {profile.board_id}",
            f"MLB         : {profile.mlb}",
            f"ROM (MAC)   : {profile.rom.hex()}",
            f"PlatformUUID: {profile.platform_uuid[:18]}...",
            f"Relay Mode  : {'Self-Hosted' if self.bridge.relay_url else 'Local Synthesizer'}",
            f"APNs Socket : courier.push.apple.com:5223",
            f"Topic       : com.apple.madrid (iMessage)",
            f"E2EE Cipher : NIST P-256 + AES-128-GCM"
        ]
        self.hw_info_text.delete("0.0", "end")
        self.hw_info_text.insert("end", "\n".join(lines))

    def _start_event_listener(self):
        def _poll():
            while not self.bridge.event_queue.empty():
                evt = self.bridge.event_queue.get_nowait()
                self._append_log_event(evt)
            self.after(100, _poll)

        self.after(100, _poll)

    def _append_log_event(self, evt):
        tag_map = {
            "APNs": "APNS",
            "IDS": "IDS",
            "Crypto": "CRYPTO",
            "Protocol": "PROTO",
            "Anisette": "PROTO"
        }
        category_tag = tag_map.get(evt.category, "PROTO")
        level_tag = evt.level if evt.level in ["SUCCESS", "WARNING", "ERROR"] else "PROTO"

        self.log_text.insert("end", f"[{evt.timestamp}] ", "TIME")
        self.log_text.insert("end", f"[{evt.category}] ", category_tag)
        self.log_text.insert("end", f"{evt.message}\n", level_tag)
        self.log_text.see("end")

    def _test_apns_socket(self):
        self.bridge.log_event("APNs", "Executing live socket diagnostic to courier.push.apple.com:5223...", "INFO")
        
        def _worker():
            start = time.time()
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                s = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname="courier.push.apple.com")
                s.settimeout(5.0)
                s.connect(("courier.push.apple.com", 5223))
                elapsed = (time.time() - start) * 1000
                cert = s.getpeercert(binary_form=True)
                s.close()
                self.bridge.log_event("APNs", f"Live ping SUCCESS! RTT: {elapsed:.1f}ms | Apple cert: {len(cert)} bytes", "SUCCESS")
            except Exception as e:
                self.bridge.log_event("APNs", f"Diagnostic failed: {e}", "ERROR")

        import threading
        threading.Thread(target=_worker, daemon=True).start()

    def _simulate_incoming_push(self):
        self.bridge.log_event("APNs", "Triggering simulated incoming push frame on com.apple.madrid...", "INFO")
        time.sleep(0.2)
        self.bridge.log_event("IDS", "Encapsulated session key decrypted via NIST P-256 ECDH.", "SUCCESS")
        time.sleep(0.2)
        self.bridge.log_event("Protocol", "Incoming Madrid payload unpacked: 'Testing live debug stream from iPhone 15 Pro!'", "SUCCESS")

    def _clear_logs(self):
        self.log_text.delete("0.0", "end")
