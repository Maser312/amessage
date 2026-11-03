"""
AMessage Interactive Command-Line Client
"""

import sys
import os
import json
import logging
import threading
import time
from getpass import getpass
from rich.console import Console
from rich.panel import Panel

from .apns.connection import APNSConnection
from .ids.client import IDSClient
from .anisette.client import AnisetteClient
from .protocol.message import iMessage, TapbackType
from .protocol.session import iMessageSession, normalize_handle

console = Console()

def main():
    console.print("[bold blue]AMessage CLI[/bold blue]")

if __name__ == "__main__":
    main()
