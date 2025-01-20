import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime
from pathlib import Path
import threading

from styles import Styles, COLORS
from settings import Settings
from utils import ChatOrderManager
from llm import LLM

class QuantumChat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quantum Chat AI")
        self.root.geometry("1200x800")
        self.root.minsize(900, 700)
        self.root.configure(bg=COLORS['bg_main'])
        
        # Initialize components
        self.styles = Styles()
        self.style = self.styles.setup_styles(self.root)
        self.settings = Settings.load_settings()
        self.llm = LLM(self.settings)
        self.chat_order = ChatOrderManager()
        self.current_chat_id = None
        self.chats = {}
        self.svg_images = {}
        
        # Setup UI components
        self.load_svgs()
        self.setup_gui()
        self.load_chats()

    def load_svgs(self):
        # Get the absolute path to the assets directory
        base_dir = Path(__file__).parent.parent
        assets_dir = base_dir / 'assets' / 'images'
        
        svg_paths = {
            'delete': ('delete_icon.svg', (20, 20)),
            'edit': ('edit_icon.svg', (20, 20)),
            'favorite': ('favorite_icon.svg', (20, 20)),
            'logo': ('logo.svg', (80, 80)),
            'new_chat': ('new_chat_icon.svg', (24, 24)),
            'quantum_title': ('quantum_title.svg', (300, 60)),
            'robot': ('robot_avatar.svg', (30, 30)),
            'star_empty': ('star_empty.svg', (20, 20)),
            'star': ('star.svg', (20, 20)),
            'user': ('user_avatar.svg', (30, 30))
        }
        
        for key, (filename, size) in svg_paths.items():
            path = assets_dir / filename
            if path.exists():
                self.svg_images[key] = self.styles.load_svg_image(str(path), size)
            else:
                print(f"Warning: SVG file not found: {path}")

    def setup_gui(self):
        # Main container with rounded corners
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create paned window
        self.paned = ttk.PanedWindow(
            self.main_container,
            orient=tk.HORIZONTAL,
            style='Separator.TPanedwindow'
        )
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        self.setup_sidebar()
        self.setup_chat_area()

    def setup_sidebar(self):
        self.sidebar = ttk.Frame(self.paned, style='Sidebar.TFrame')
        self.paned.add(self.sidebar, weight=1)
        
        # Logo and title area with proper spacing
        logo_frame = ttk.Frame(self.sidebar, style='Logo.TFrame')
        logo_frame.pack(fill=tk.X, pady=(20, 30))
        
        logo_label = ttk.Label(
            logo_frame,
            image=self.svg_images['logo'],
            style='Logo.TLabel'
        )
        logo_label.pack(side=tk.LEFT, padx=(20, 10))
        
        title_label = ttk.Label(
            logo_frame,
            image=self.svg_images['quantum_title'],
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)

        # New chat button
        new_chat_btn = ttk.Button(
            self.sidebar,
            text="New Chat",
            image=self.svg_images['new_chat'],
            compound=tk.LEFT,
            command=self.create_new_chat,
            style='NewChat.TButton'
        )
        new_chat_btn.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Chat list container with rounded corners
        self.chat_list_frame = ttk.Frame(self.sidebar, style='ChatList.TFrame')
        self.chat_list_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Settings button (text only)
        settings_btn = ttk.Button(
            self.sidebar,
            text="Settings",
            command=self.show_settings,
            style='Settings.TButton'
        )
        settings_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

    def setup_chat_area(self):
        self.chat_area = ttk.Frame(self.paned, style='ChatArea.TFrame')
        self.paned.add(self.chat_area, weight=3)

        # Current chat label at top
        self.current_chat_label = ttk.Label(
            self.chat_area,
            text="",
            style="CurrentChat.TLabel"
        )
        self.current_chat_label.pack(anchor=tk.W, padx=20, pady=(10,0))
        
        # Messages canvas with rounded corners
        self.messages_canvas = tk.Canvas(
            self.chat_area,
            bg=COLORS['bg_chat'],
            highlightthickness=0,
            bd=0
        )
        self.messages_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.chat_area,
            orient=tk.VERTICAL,
            command=self.messages_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Input area with rounded corners
        self.input_frame = ttk.Frame(self.chat_area, style='Input.TFrame')
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.input = ttk.Entry(
            self.input_frame,
            style='ChatInput.TEntry'
        )
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input.bind('<Return>', lambda e: self.send_message())
        
        send_btn = ttk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            style='Send.TButton'
        )
        send_btn.pack(side=tk.RIGHT)

    def create_new_chat(self):
            chat_id = str(datetime.now().timestamp())
            new_chat = {
                'id': chat_id,
                'name': f'New Chat',
                'messages': [],
                'is_favorite': False,
                'timestamp': datetime.now().isoformat()
            }
            self.chats[chat_id] = new_chat
            self.chat_order.add_chat(chat_id)
            self.save_chat(new_chat)
            self.select_chat(chat_id)
            self.update_chat_list()

    def load_chats(self):
        chat_dir = Path('chats')
        chat_dir.mkdir(exist_ok=True)
        
        for chat_file in chat_dir.glob('*.json'):
            with open(chat_file, 'r') as f:
                chat_data = json.load(f)
                self.chats[chat_data['id']] = chat_data
        
        self.update_chat_list()

    def save_chat(self, chat_data):
        chat_dir = Path('chats')
        chat_dir.mkdir(exist_ok=True)
        
        with open(chat_dir / f"{chat_data['id']}.json", 'w') as f:
            json.dump(chat_data, f, indent=2)

    def update_chat_list(self):
        # Clear existing chat tabs
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        
        # Add chats in order (favorites first)
        ordered_chats = self.chat_order.get_ordered_chats()
        for chat_id in ordered_chats:
            if chat_id in self.chats:
                self.add_chat_tab(self.chats[chat_id])

    def add_chat_tab(self, chat_data):
        commands = {
            'favorite': lambda e: self.toggle_favorite(chat_data['id']),
            'edit': lambda e: self.rename_chat(chat_data['id']),
            'delete': lambda e: self.delete_chat(chat_data['id']),
            'select_chat': lambda e: self.select_chat(chat_data['id'])  # Add this line
        }
        
        frame = self.styles.create_chat_tab(
            self.chat_list_frame,
            chat_data,
            self.svg_images,
            commands
        )
        frame.pack(fill=tk.X, pady=2)
        
        # Bind click event to the entire frame
        frame.bind('<Button-1>', commands['select_chat'])  # Change this line


    def select_chat(self, chat_id):
        self.current_chat_id = chat_id
        self.messages_canvas.delete('all')

        if chat_id in self.chats:
            chat = self.chats[chat_id]
            # Update label to show which chat is loaded
            self.current_chat_label.config(text=f"Chat: {chat['name']}")
            self.update_messages_display()
            
            self.input.focus_set()
            self.messages_canvas.yview_moveto(1.0)

        
        # Clear current messages display
        self.messages_canvas.delete('all')
        
        # Load and display chat messages
        if chat_id in self.chats:
            chat = self.chats[chat_id]
            # Update messages display
            self.update_messages_display()
            
            # Set focus to input field
            self.input.focus_set()
            
            # Scroll to bottom of messages
            self.messages_canvas.yview_moveto(1.0)

    def toggle_favorite(self, chat_id):
        chat = self.chats[chat_id]
        chat['is_favorite'] = not chat['is_favorite']
        self.chat_order.toggle_favorite(chat_id)
        self.save_chat(chat)
        self.update_chat_list()

    def rename_chat(self, chat_id):
        chat = self.chats[chat_id]
        new_name = simpledialog.askstring(
            "Rename Chat",
            "Enter new name:",
            parent=self.root,
            initialvalue=chat['name']
        )
        if new_name:
            chat['name'] = new_name
            self.save_chat(chat)
            self.update_chat_list()

    def delete_chat(self, chat_id):
        if messagebox.askyesno("Delete Chat", "Are you sure you want to delete this chat?"):
            chat_file = Path('chats') / f"{chat_id}.json"
            if chat_file.exists():
                chat_file.unlink()
            
            self.chat_order.remove_chat(chat_id)
            del self.chats[chat_id]
            
            if self.current_chat_id == chat_id:
                self.current_chat_id = None
            
            self.update_chat_list()

    def send_message(self):
        if not self.current_chat_id:
            messagebox.showinfo("Info", "Please select or create a chat first.")
            return

        message = self.input.get().strip()
        if not message:
            return

        self.input.delete(0, tk.END)
        self.add_message('user', message)
        
        # Start AI response in separate thread
        threading.Thread(
            target=self.get_ai_response,
            args=(message,),
            daemon=True
        ).start()

    def get_ai_response(self, user_message):
        try:
            response = self.llm.generate_response(user_message)
            self.root.after(0, lambda: self.add_message('assistant', response))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"Failed to get AI response: {str(e)}"
            ))

    def add_message(self, role, content):
        if not self.current_chat_id:
            return

        chat = self.chats[self.current_chat_id]
        chat['messages'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        self.save_chat(chat)
        self.update_messages_display()

    def update_messages_display(self):
        self.messages_canvas.delete('all')
        if not self.current_chat_id or self.current_chat_id not in self.chats:
            return

        y_pos = 20
        messages = self.chats[self.current_chat_id]['messages']
        
        for msg in messages:
            is_user = msg['role'] == 'user'
            
            # Calculate positions
            canvas_width = self.messages_canvas.winfo_width()
            bubble_width = min(canvas_width * 0.7, 500)
            
            if is_user:
                bubble_x = canvas_width - bubble_width - 60
                avatar_x = canvas_width - 40
            else:
                bubble_x = 60
                avatar_x = 30
            
            # Add avatar
            avatar_img = self.svg_images['user'] if is_user else self.svg_images['robot']
            self.messages_canvas.create_image(
                avatar_x,
                y_pos + 25,
                image=avatar_img
            )
            
            # Create message bubble
            bubble = self.styles.create_rounded_rectangle(
                self.messages_canvas,
                bubble_x,
                y_pos,
                bubble_x + bubble_width,
                y_pos + 50,
                fill=COLORS['message_user'] if is_user else COLORS['message_bot'],
                radius=20
            )
            
            # Add message text
            self.messages_canvas.create_text(
                bubble_x + 20,
                y_pos + 25,
                text=msg['content'],
                fill=COLORS['text_primary'],
                anchor=tk.W,
                width=bubble_width - 40,
                font=('SF Pro Display', 13)
            )
            
            # Add timestamp
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
            self.messages_canvas.create_text(
                bubble_x + bubble_width - 20,
                y_pos + 60,
                text=timestamp,
                fill=COLORS['text_secondary'],
                anchor=tk.E,
                font=('SF Pro Display', 10)
            )
            
            y_pos += 100

        # Update scroll region and scroll to bottom
        self.messages_canvas.configure(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("800x700")
        settings_window.configure(bg=COLORS['bg_settings'])
        
        # Main container with padding
        main_frame = ttk.Frame(settings_window, style='Settings.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Model Connection Section
        connection_section = ttk.Frame(main_frame, style='SettingsSection.TFrame')
        connection_section.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            connection_section,
            text="Model Connection",
            style='SettingsHeader.TLabel'
        ).pack(anchor=tk.W)
        
        # Ollama API URL
        url_frame = ttk.Frame(connection_section, style='Settings.TFrame')
        url_frame.pack(fill=tk.X, pady=(15, 10))
        
        ttk.Label(
            url_frame,
            text="Ollama API URL:",
            style='Settings.TLabel'
        ).pack(side=tk.LEFT)
        
        url_entry = ttk.Entry(
            url_frame,
            style='Settings.TEntry'
        )
        url_entry.insert(0, self.settings.get('api_url', "http://localhost:11434/v1"))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        
        # Model Selection
        model_frame = ttk.Frame(connection_section, style='Settings.TFrame')
        model_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            model_frame,
            text="Model:",
            style='Settings.TLabel'
        ).pack(side=tk.LEFT)
        
        models = ['qwen2.5:14b', 'qwen1.5:14b', 'qwen1.5:7b', 'qwen1.5:4b']
        model_var = tk.StringVar(value=self.settings['model_settings']['model'])
        model_dropdown = ttk.Combobox(
            model_frame,
            textvariable=model_var,
            values=models,
            state='readonly',
            style='Settings.TCombobox'
        )
        model_dropdown.pack(side=tk.LEFT, padx=(15, 0), fill=tk.X, expand=True)
        
        # Model Parameters Section
        params_section = ttk.Frame(main_frame, style='SettingsSection.TFrame')
        params_section.pack(fill=tk.X, pady=20)
        
        ttk.Label(
            params_section,
            text="Model Parameters",
            style='SettingsHeader.TLabel'
        ).pack(anchor=tk.W)
        
        # Parameter sliders
        params = [
            ("Temperature", "temperature", 0.0, 1.0),
            ("Max Tokens", "max_tokens", 100, 4000),
            ("Top P", "top_p", 0.0, 1.0),
            ("Frequency Penalty", "frequency_penalty", 0.0, 2.0),
            ("Presence Penalty", "presence_penalty", 0.0, 2.0)
        ]
        
        for label, key, min_val, max_val in params:
            param_frame = ttk.Frame(params_section, style='Settings.TFrame')
            param_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(
                param_frame,
                text=f"{label}:",
                style='Settings.TLabel'
            ).pack(side=tk.LEFT)
            
            value_var = tk.StringVar(value=f"{self.settings['model_settings'][key]:.2f}")
            value_label = ttk.Label(
                param_frame,
                textvariable=value_var,
                style='Settings.TLabel'
            )
            value_label.pack(side=tk.RIGHT, padx=(10, 0))
            
            scale = ttk.Scale(
                param_frame,
                from_=min_val,
                to=max_val,
                value=self.settings['model_settings'][key],
                command=lambda v, var=value_var: var.set(f"{float(v):.2f}"),
                style='Settings.Horizontal.TScale'
            )
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 15))
            setattr(self, f'scale_{key}', scale)
        
        # Memory Settings Section
        memory_section = ttk.Frame(main_frame, style='SettingsSection.TFrame')
        memory_section.pack(fill=tk.X, pady=20)
        
        ttk.Label(
            memory_section,
            text="Memory Settings",
            style='SettingsHeader.TLabel'
        ).pack(anchor=tk.W)
        
        # Buffer Size
        buffer_frame = ttk.Frame(memory_section, style='Settings.TFrame')
        buffer_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            buffer_frame,
            text="Buffer Size:",
            style='Settings.TLabel'
        ).pack(side=tk.LEFT)
        
        buffer_var = tk.StringVar(value=str(self.settings['memory_settings']['buffer_size']))
        buffer_entry = ttk.Entry(
            buffer_frame,
            textvariable=buffer_var,
            style='Settings.TEntry',
            width=10
        )
        buffer_entry.pack(side=tk.LEFT, padx=(15, 0))
        
        # Summary Settings
        summary_frame = ttk.Frame(memory_section, style='Settings.TFrame')
        summary_frame.pack(fill=tk.X, pady=10)
        
        summary_enabled = tk.BooleanVar(value=self.settings['memory_settings']['summary_enabled'])
        summary_check = ttk.Checkbutton(
            summary_frame,
            text="Enable Summary Memory",
            variable=summary_enabled,
            style='Settings.TCheckbutton'
        )
        summary_check.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Settings.TFrame')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_settings(
                settings_window,
                url_entry.get(),
                model_var.get(),
                {
                    'temperature': float(self.scale_temperature.value_var.get()),
                    'max_tokens': int(float(self.scale_max_tokens.value_var.get())),
                    'top_p': float(self.scale_top_p.value_var.get()),
                    'frequency_penalty': float(self.scale_frequency_penalty.value_var.get()),
                    'presence_penalty': float(self.scale_presence_penalty.value_var.get())
                },
                {
                    'buffer_size': int(buffer_var.get()),
                    'summary_enabled': summary_enabled.get()
                }
            ),
            style='SettingsButton.TButton'
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=settings_window.destroy,
            style='SettingsButton.TButton'
        )
        cancel_btn.pack(side=tk.RIGHT)

        # Center the window on screen
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Calculate position
        x = self.root.winfo_x() + (self.root.winfo_width() - 800) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 700) // 2
        settings_window.geometry(f"+{x}+{y}")

    def save_settings(self, window, api_url, model, model_params, memory_params):
        # Update settings
        self.settings['api_url'] = api_url
        self.settings['model_settings']['model'] = model
        self.settings['model_settings'].update(model_params)
        self.settings['memory_settings'].update(memory_params)
        
        # Save to file
        Settings.save_settings(self.settings)
        
        # Update LLM
        self.llm.update_settings(self.settings)
        
        # Close settings window
        window.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuantumChat()
    app.run()