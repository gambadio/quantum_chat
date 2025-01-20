import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cairosvg
import io

COLORS = {
    # Main Background Colors
    'bg_main': '#1A1B3E',          # Rich dark blue
    'bg_sidebar': '#202052',       # Deep purple-blue
    'bg_chat': '#16172E',          # Dark chat background
    'bg_input': '#2C2D7E',         # Input field
    'bg_settings': '#1E1F45',      # Settings background
    
    # Accent Colors (Pastel)
    'accent_primary': '#B4A5FF',    # Soft purple
    'accent_secondary': '#FF9ECD',  # Soft pink
    'accent_tertiary': '#94FBFF',   # Soft cyan
    'accent_quaternary': '#B3FF9D', # Soft green
    
    # Message Colors
    'message_user': '#FF61EF',      # Bright pink for user messages
    'message_bot': '#2D2E8F',       # Brighter purple for bot
    
    # Text Colors
    'text_primary': '#FFFFFF',      # Pure white
    'text_secondary': '#FFFFFF',    # Also white (no grey)
    
    # UI Elements
    'border': '#363794',            # Border color
    'selected': '#3D3E9A',          # Selected state
    'star_active': '#FFD700',       # Yellow for active star
    'slider_track': '#404080',      # Slider track color
    'slider_handle': '#FF9ECD',     # Slider handle color
    
    # Settings Elements
    'settings_section': '#252666',   # Settings section background
    'settings_input': '#343785',     # Settings input background
    'settings_button': '#FF61EF',    # Settings button color
    'settings_slider': '#4A4C9E',    # Settings slider background
    'settings_header': '#FF9ECD',    # Settings header text
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
            background=COLORS['bg_main']
        )

        # Sidebar
        style.configure('Sidebar.TFrame',
            background=COLORS['bg_sidebar']
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
            background=[('active', COLORS['accent_primary'])]
        )

        # Chat List
        style.configure('ChatList.TFrame',
            background=COLORS['bg_sidebar']
        )

        # Chat Tab
        style.configure('ChatTab.TFrame',
            background=COLORS['bg_sidebar'],
            relief="flat",
            padding=(15, 12)
        )

        # Chat Name Labels (Normal and Pressed states)
        style.configure('ChatName.TLabel',
            background=COLORS['bg_sidebar'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 0)
        )
        style.configure('ChatNamePressed.TLabel',
            background=COLORS['selected'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 0)
        )

        # Current Chat Label
        style.configure('CurrentChat.TLabel',
            background=COLORS['bg_chat'],
            foreground=COLORS['accent_primary'],
            font=('SF Pro Display', 14, 'bold'),
            padding=(0, 0)
        )

        # Settings Button
        style.configure('Settings.TButton',
            background=COLORS['bg_sidebar'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=15,
            relief="flat",
            borderwidth=0
        )
        style.map('Settings.TButton',
            background=[('active', COLORS['bg_sidebar'])]
        )

        # Chat Area
        style.configure('ChatArea.TFrame',
            background=COLORS['bg_chat']
        )

        # Message Frame
        style.configure('Message.TFrame',
            background=COLORS['bg_chat'],
            relief="flat",
            padding=15
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
            insertcolor=COLORS['text_primary'],
            font=('SF Pro Display', 14),
            padding=(15, 12)
        )

        # Send Button
        style.configure('Send.TButton',
            background=COLORS['accent_secondary'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13, 'bold'),
            padding=(20, 12),
            relief="flat"
        )

        # Settings Window Styles
        style.configure('Settings.TFrame',
            background=COLORS['bg_settings'],
            relief="flat"
        )

        # Settings Section Frame
        style.configure('SettingsSection.TFrame',
            background=COLORS['settings_section'],
            relief="flat",
            padding=20
        )

        # Settings Headers
        style.configure('SettingsHeader.TLabel',
            background=COLORS['bg_settings'],
            foreground=COLORS['settings_header'],
            font=('SF Pro Display', 16, 'bold'),
            padding=(0, 20, 0, 10)
        )

        # Settings Labels
        style.configure('Settings.TLabel',
            background=COLORS['bg_settings'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(0, 5)
        )

        # Settings Entry
        style.configure('Settings.TEntry',
            fieldbackground=COLORS['settings_input'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 8),
            relief="flat",
            borderwidth=0
        )

        # Settings Combobox
        style.configure('Settings.TCombobox',
            fieldbackground=COLORS['settings_input'],
            background=COLORS['text_primary'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13),
            padding=(10, 8),
            arrowcolor=COLORS['text_primary'],
            relief="flat",
            borderwidth=0
        )
        style.map('Settings.TCombobox',
            fieldbackground=[('readonly', COLORS['settings_input'])],
            selectbackground=[('readonly', COLORS['settings_input'])]
        )

        # Settings Scale (Slider)
        style.configure('Settings.Horizontal.TScale',
            background=COLORS['bg_settings'],
            troughcolor=COLORS['settings_slider'],
            sliderlength=30,
            sliderrelief="flat",
            borderwidth=0,
            sliderthickness=20
        )

        # Settings Checkbutton
        style.configure('Settings.TCheckbutton',
            background=COLORS['bg_settings'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13)
        )

        # Settings Buttons
        style.configure('SettingsButton.TButton',
            background=COLORS['settings_button'],
            foreground=COLORS['text_primary'],
            font=('SF Pro Display', 13, 'bold'),
            padding=(20, 10),
            relief="flat",
            borderwidth=0
        )
        style.map('SettingsButton.TButton',
            background=[('active', COLORS['accent_secondary'])]
        )

        return style

    @staticmethod
    def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
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
        frame = ttk.Frame(parent, style='ChatTab.TFrame')
        
        # Background canvas
        canvas = tk.Canvas(
            frame,
            bg=COLORS['bg_sidebar'],
            highlightthickness=0,
            height=50
        )
        canvas.place(relwidth=1, relheight=1)
        
        # Avatar
        avatar_label = ttk.Label(
            frame,
            image=icons['robot'],
            style='Logo.TLabel'
        )
        avatar_label.pack(side=tk.LEFT, padx=(10, 10))
        
        # Chat name with click handling
        name_label = ttk.Label(
            frame,
            text=chat_data['name'],
            style='ChatName.TLabel'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def on_press(event):
            name_label.configure(style='ChatNamePressed.TLabel')
            
        def on_release(event):
            name_label.configure(style='ChatName.TLabel')
            commands['select_chat'](chat_data['id'])

        # Bind press and release events
        name_label.bind('<ButtonPress-1>', on_press)
        name_label.bind('<ButtonRelease-1>', on_release)
        
        # Action icons container
        actions_frame = ttk.Frame(frame, style='ChatTab.TFrame')
        actions_frame.pack(side=tk.RIGHT, padx=10)
        
        # Star icon (favorite)
        star_icon = 'star' if chat_data.get('is_favorite') else 'star_empty'
        star_label = tk.Label(
            actions_frame,
            image=icons[star_icon],
            bg=COLORS['bg_sidebar'],
            cursor='hand2'
        )
        star_label.pack(side=tk.RIGHT, padx=5)
        star_label.bind('<Button-1>', lambda e: commands['favorite'](chat_data['id']))
        
        # Edit and delete icons
        for icon_name, command in [
            ('edit', 'edit'),
            ('delete', 'delete')
        ]:
            icon_label = tk.Label(
                actions_frame,
                image=icons[icon_name],
                bg=COLORS['bg_sidebar'],
                cursor='hand2'
            )
            icon_label.pack(side=tk.RIGHT, padx=5)
            icon_label.bind('<Button-1>', lambda e, cmd=command: commands[cmd](chat_data['id']))
        
        return frame