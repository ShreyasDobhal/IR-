import tkinter as tk
from values import TOAST_SIZE

def show_toast(root, message, timeout=2000, on_close=None):
    toast = tk.Toplevel(root)
    
    # Calculate the center coordinates of the screen
    screen_width = toast.winfo_screenwidth()
    screen_height = toast.winfo_screenheight()
    # Adjust the height and width as needed
    toast_width, toast_height = TOAST_SIZE.split('x')
    toast_width = int(toast_width)
    toast_height = int(toast_height)
    x = (screen_width - toast_width) // 2
    y = (screen_height - toast_height) // 2
    
    # Center the toast
    toast.geometry(f"{TOAST_SIZE}+{x}+{y}")
    # Make it topmost
    toast.wm_attributes("-topmost", 1)
    # Add transparency (0.0 to 1.0)
    toast.attributes("-alpha", 0.9)
    # Remove window decorations (title bar, borders)
    toast.overrideredirect(True)
    
    # Create a custom style for the label
    label = tk.Label(toast, text=message, bg="black", fg="white", font=("Helvetica", 14), wraplength=280)
    label.pack(fill=tk.BOTH, expand=True)
    
    def close_toast():
        toast.destroy()
        if on_close is not None:
            on_close()

    # Automatically close the toast after a few seconds (adjust as needed)
    toast.after(timeout, close_toast)
    
    toast.mainloop()
