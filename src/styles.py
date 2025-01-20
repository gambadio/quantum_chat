import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cairosvg
import io

COLORS = {
    # Main Background Colors
    'bg_main': '#1A1B2E',          # Deep blue main background
    'bg_sidebar': '#20214A',        # Lighter sidebar
    'bg_chat': '#16172A',          # Darker chat area
    'bg_input': '#2C2D6E',         # Input field background
    
    # Accent Colors (Pastel)
    'accent_primary': '#B4A5FF',    # Soft purple for new chat
    'accent_secondary': '#FF9ECD',  # Soft pink
    'accent_tertiary': '#94FBFF',   # Soft cyan
    'accent_quaternary': '#B3FF9D', # Soft green
    
    # Message Colors
    'message_user': '#FF61EF',      # Pastel pink for user messages
    'message_bot': '#2D2E77',       # Deep purple for bot messages
    
    # Text Colors
    'text_primary': '#FFFFFF',      # Pure white text
    'text_secondary': '#E0E0FF',    # Very light purple
    
    # UI Elements
    'border': '#363794',            # Border color
    'selected': '#3D3E9A'           # Selected state
}

class Styles:
    @staticmethod
    def load_svg_image(path, size=(24, 24)):
        """Load and resize SVG images"""
        try:
            png_data = cairosvg.svg2png(
                url=path,
                output_width=size[0],
                output_height=size[1]
            )
            image = Image.open(io.BytesIO(png_data))
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading SVG {path}: {e}")
            return None

    @staticmethod
    def setup_styles(root):
        style = ttk.Style()
        style.theme_use('default')

        # Main Window
        style.configure('Main.TFrame',
            background=COLORS['bg_main'],
            relief="flat"
        )

        # Sidebar
        style.configure('Sidebar.TFrame',
            background=COLORS['bg_sidebar'],
            relief="flat"
        )

        # Logo Area
        style.configure('Logo.TFrame',
            background=COLORS['bg_sidebar'],
            padding=(20, 15)
        )
        
        style.configure('Logo.TLabel',
            background=COLORS['bg_sidebar'],
            padding=(0, 0)
        )
        
        style.configure('Title.TLabel',
            background=COLORS['bg_sidebar'],
            padding=(0, 0)
        )

        # New Chat Button
        style.configure('NewChat.TButton',
            background=COLORS['accent_primary'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 14, 'bold'),
            padding=(20, 15),
            relief="flat",
            borderwidth=0
        )
        style.map('NewChat.TButton',
            background=[('active', COLORS['accent_tertiary'])]
        )

        # Chat List
        style.configure('ChatList.TFrame',
            background=COLORS['bg_sidebar'],
            relief="flat"
        )

        # Chat Tab
        style.configure('ChatTab.TFrame',
            background=COLORS['bg_sidebar'],
            relief="flat",
            padding=(15, 12)
        )

        # Chat Name
        style.configure('ChatName.TLabel',
            background=COLORS['bg_sidebar'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 0)
        )

        # Chat Area
        style.configure('ChatArea.TFrame',
            background=COLORS['bg_chat'],
            relief="flat"
        )

        # Message Canvas
        style.configure('MessageCanvas.TFrame',
            background=COLORS['bg_chat'],
            relief="flat"
        )

        # Input Area
        style.configure('Input.TFrame',
            background=COLORS['bg_chat'],
            relief="flat",
            padding=(20, 15)
        )

        # Chat Input
        style.configure('ChatInput.TEntry',
            fieldbackground=COLORS['bg_input'],
            foreground=COLORS['text_primary'],
            insertcolor=COLORS['accent_secondary'],
            font=('SF Pro Display', 14),
            padding=(15, 12),
            relief="flat"
        )

        # Send Button
        style.configure('Send.TButton',
            background=COLORS['accent_secondary'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13, 'bold'),
            padding=(20, 12),
            relief="flat"
        )

        # Settings Button
        style.configure('Settings.TButton',
            background=COLORS['bg_sidebar'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=15,
            relief="flat"
        )

        # Settings Window
        style.configure('Settings.TFrame',
            background=COLORS['bg_main'],
            relief="flat"
        )

        style.configure('Settings.TLabelframe',
            background=COLORS['bg_main'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 14, 'bold'),
            relief="flat",
            borderwidth=2,
            bordercolor=COLORS['border']
        )

        style.configure('Settings.TLabel',
            background=COLORS['bg_main'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 5)
        )

        style.configure('Settings.TEntry',
            fieldbackground=COLORS['bg_input'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 5)
        )

        style.configure('Settings.TScale',
            background=COLORS['bg_main'],
            troughcolor=COLORS['bg_input'],
            slidercolor=COLORS['accent_secondary']
        )

        return style

    @staticmethod
    def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=15, **kwargs):
        """Create a rounded rectangle on a canvas"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    @staticmethod
    def create_chat_tab(parent, chat_data, icons, commands):
        """Create a chat tab with integrated action icons"""
        frame = ttk.Frame(parent, style='ChatTab.TFrame')
        
        # Avatar
        avatar_label = ttk.Label(
            frame,
            image=icons['robot'],
            style='Logo.TLabel'
        )
        avatar_label.pack(side=tk.LEFT, padx=(5, 10))
        
        # Chat name
        name_label = ttk.Label(
            frame,
            text=chat_data['name'],
            style='ChatName.TLabel'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Action icons container
        actions_frame = ttk.Frame(frame, style='ChatTab.TFrame')
        actions_frame.pack(side=tk.RIGHT, padx=5)
        
        # Add action icons (without button borders)
        for icon_name, command in [
            ('star', commands['favorite']),
            ('edit', commands['edit']),
            ('delete', commands['delete'])
        ]:
            icon_label = tk.Label(
                actions_frame,
                image=icons[icon_name],
                bg=COLORS['bg_sidebar'],
                cursor='hand2'
            )
            icon_label.pack(side=tk.RIGHT, padx=2)
            icon_label.bind('<Button-1>', command)
        
        return frame