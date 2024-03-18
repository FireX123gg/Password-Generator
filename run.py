import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
from PIL import Image, ImageTk
import requests
import io


class PasswordGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Password Generator")
        self.geometry("800x400")
        self.configure(bg="#5c3c92")

        # Set app icon
        try:
            response_icon = requests.get(
                "https://thumbs.dreamstime.com/b/passwords-icon-trendy-design-style-isolated-white-background-vector-simple-modern-flat-symbol-web-site-mobile-logo-135734914.jpg")
            icon_data = io.BytesIO(response_icon.content)
            self.icon_img = Image.open(icon_data)
            self.icon_img = self.icon_img.resize((32, 32))
            self.icon_img = ImageTk.PhotoImage(self.icon_img)
            self.iconphoto(True, self.icon_img)
        except Exception as e:
            messagebox.showerror(
                "Error", "Failed to set app icon: " + str(e))

        # Heading
        self.heading_label = tk.Label(
            self, text="Password Generator", bg="#5c3c92", fg="white", font=("Helvetica", 24))
        self.heading_label.pack(pady=10)

        # Password frame
        self.password_frame = tk.Text(
            self, height=15, width=50, bg="white", fg="black", font=("Helvetica", 12), state=tk.DISABLED)
        self.password_frame.pack(pady=10, side=tk.LEFT, padx=10)

        # Configuration panel
        self.config_panel = tk.Frame(self, bg="#5c3c92")
        self.config_panel.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Number of passwords label and entry
        self.num_label = tk.Label(
            self.config_panel, text="Number of Passwords:", bg="#5c3c92", fg="white", font=("Helvetica", 12))
        self.num_label.pack(pady=5, anchor="w")
        self.num_entry = tk.Entry(
            self.config_panel, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.num_entry.pack(pady=5)

        # Length label and entry
        self.length_label = tk.Label(
            self.config_panel, text="Length of Passwords:", bg="#5c3c92", fg="white", font=("Helvetica", 12))
        self.length_label.pack(pady=5, anchor="w")
        self.length_entry = tk.Entry(
            self.config_panel, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.length_entry.pack(pady=5)

        # Uppercase
        self.upper_var = tk.BooleanVar()
        self.upper_switch_frame = tk.Frame(self.config_panel, bg="#5c3c92")
        self.upper_switch_frame.pack(pady=5, anchor="w")
        self.upper_switch_label = tk.Label(
            self.upper_switch_frame, text="Uppercase", bg="#5c3c92", fg="white", font=("Helvetica", 12))
        self.upper_switch_label.pack(side=tk.LEFT, padx=(0, 5))
        self.upper_switch = tk.Checkbutton(
            self.upper_switch_frame, variable=self.upper_var, onvalue=True, offvalue=False, bg="#5c3c92")
        self.upper_switch.pack(side=tk.LEFT)

        # Special
        self.special_var = tk.BooleanVar()
        self.special_switch_frame = tk.Frame(self.config_panel, bg="#5c3c92")
        self.special_switch_frame.pack(pady=5, anchor="w")
        self.special_switch_label = tk.Label(
            self.special_switch_frame, text="Special", bg="#5c3c92", fg="white", font=("Helvetica", 12))
        self.special_switch_label.pack(side=tk.LEFT, padx=(0, 5))
        self.special_switch = tk.Checkbutton(
            self.special_switch_frame, variable=self.special_var, onvalue=True, offvalue=False, bg="#5c3c92")
        self.special_switch.pack(side=tk.LEFT)

        # Lowercase
        self.lower_var = tk.BooleanVar()
        self.lower_switch_frame = tk.Frame(self.config_panel, bg="#5c3c92")
        self.lower_switch_frame.pack(pady=5, anchor="w")
        self.lower_switch_label = tk.Label(
            self.lower_switch_frame, text="Lowercase", bg="#5c3c92", fg="white", font=("Helvetica", 12))
        self.lower_switch_label.pack(side=tk.LEFT, padx=(0, 5))
        self.lower_switch = tk.Checkbutton(
            self.lower_switch_frame, variable=self.lower_var, onvalue=True, offvalue=False, bg="#5c3c92")
        self.lower_switch.pack(side=tk.LEFT)

        # Generate button
        self.generate_button = tk.Button(
            self.config_panel, text="Generate Passwords", command=self.generate_passwords, bg="#8a8a8a", fg="black", font=("Helvetica", 12))
        self.generate_button.pack(pady=10)

        # Copy button
        try:
            response_copy = requests.get(
                "https://static.vecteezy.com/system/resources/previews/000/423/039/original/copy-icon-vector-illustration.jpg")
            copy_icon_data = io.BytesIO(response_copy.content)
            img_copy = Image.open(copy_icon_data)
            img_copy = img_copy.resize((25, 25))
            self.img_copy = ImageTk.PhotoImage(img_copy)
        except Exception as e:
            messagebox.showerror(
                "Error", "Failed to load Copy icon: " + str(e))
            self.img_copy = None

        self.copy_button = tk.Button(
            self.password_frame, image=self.img_copy, command=self.copy_passwords, bg="#5c3c92", bd=0, activebackground="#5c3c92")
        self.copy_button.image = self.img_copy
        self.copy_button.place(relx=0.98, rely=0.0, anchor="ne")

        # Clear button
        try:
            response_clear = requests.get(
                "https://clipart-library.com/new_gallery/55030_red-cross-png.png")
            clear_icon_data = io.BytesIO(response_clear.content)
            img_clear = Image.open(clear_icon_data)
            img_clear = img_clear.resize((25, 25))
            self.img_clear = ImageTk.PhotoImage(img_clear)
        except Exception as e:
            messagebox.showerror(
                "Error", "Failed to load Clear icon: " + str(e))
            self.img_clear = None

        self.clear_button = tk.Button(
            self.password_frame, image=self.img_clear, command=self.clear_passwords, bg="#5c3c92", bd=0, activebackground="#5c3c92")
        self.clear_button.image = self.img_clear
        self.clear_button.place(relx=0.92, rely=0.0, anchor="ne")

    def generate_password(self, length, use_uppercase, use_special, use_lowercase):
        chars = ''
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_special:
            chars += string.punctuation
        if use_lowercase:
            chars += string.ascii_lowercase

        if not chars:
            messagebox.showerror(
                "Error", "Please select at least one character type.")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    def generate_passwords(self):
        try:
            num_passwords = int(self.num_entry.get())
            length_passwords = int(self.length_entry.get())
            use_uppercase = self.upper_var.get()
            use_special = self.special_var.get()
            use_lowercase = self.lower_var.get()
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter valid numbers for number and length of passwords.")
            return

        if num_passwords > 100:
            messagebox.showerror(
                "Error", "Number of passwords cannot exceed 100.")
            return

        if length_passwords > 30:
            messagebox.showerror(
                "Error", "Password length cannot exceed 30 characters.")
            return

        passwords_generated = []
        for _ in range(num_passwords):
            password = self.generate_password(
                length_passwords, use_uppercase, use_special, use_lowercase)
            passwords_generated.append(password)

        self.password_frame.config(state=tk.NORMAL)
        self.password_frame.delete("1.0", tk.END)
        self.password_frame.insert(tk.END, "\n".join(passwords_generated))
        self.password_frame.config(state=tk.DISABLED)

    def clear_passwords(self):
        self.password_frame.config(state=tk.NORMAL)
        self.password_frame.delete("1.0", tk.END)
        self.password_frame.config(state=tk.DISABLED)

    def copy_passwords(self):
        passwords_text = self.password_frame.get("1.0", tk.END).strip()
        pyperclip.copy(passwords_text)
        messagebox.showinfo("Copied", "Passwords copied to clipboard!")


if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()
