import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import datetime

# Supported formats
SUPPORTED_IMAGE_FORMATS = [".png", ".bmp", ".jpg", ".jpeg"]

# History data
history = []
session_results = []

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SteganographyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("1100x850")

        self.setup_ui()

    def setup_ui(self):
        title = ctk.CTkLabel(self.root, text="Steganography Tool", font=ctk.CTkFont(size=30, weight="bold"))
        title.pack(pady=15)

        tabview = ctk.CTkTabview(self.root, width=1000, height=650)
        tabview.pack(pady=10)

        self.encode_tab = tabview.add("Encode")
        self.decode_tab = tabview.add("Decode")
        self.history_tab = tabview.add("History")

        self.setup_encode_tab()
        self.setup_decode_tab()
        self.setup_history_tab()

        quit_button = ctk.CTkButton(self.root, text="Exit Application", command=self.root.quit, fg_color="red", font=ctk.CTkFont(size=18))
        quit_button.pack(pady=10)

    def setup_encode_tab(self):
        self.encode_image_path = ctk.StringVar()
        ctk.CTkLabel(self.encode_tab, text="Select Image", font=("Segoe UI", 20)).pack(pady=10)
        path_entry = ctk.CTkEntry(self.encode_tab, textvariable=self.encode_image_path, width=700, font=ctk.CTkFont(size=16))
        path_entry.pack()
        ctk.CTkButton(self.encode_tab, text="Browse", command=self.browse_image_encode, font=ctk.CTkFont(size=16)).pack(pady=5)

        ctk.CTkLabel(self.encode_tab, text="Enter Message", font=("Segoe UI", 20)).pack(pady=10)
        self.message_text = ctk.CTkTextbox(self.encode_tab, height=150, width=800, font=ctk.CTkFont(size=16))
        self.message_text.pack()

        ctk.CTkButton(self.encode_tab, text="Encode", command=self.encode_message, font=ctk.CTkFont(size=18)).pack(pady=20)

        self.encode_new_session_button = ctk.CTkButton(self.encode_tab, text="Start New Session", command=self.clear_session, font=ctk.CTkFont(size=16))
        self.encode_new_session_button.pack(pady=5)
        self.encode_new_session_button.pack_forget()

    def setup_decode_tab(self):
        self.decode_image_path = ctk.StringVar()
        ctk.CTkLabel(self.decode_tab, text="Select Image", font=("Segoe UI", 20)).pack(pady=10)
        path_entry = ctk.CTkEntry(self.decode_tab, textvariable=self.decode_image_path, width=700, font=ctk.CTkFont(size=16))
        path_entry.pack()
        ctk.CTkButton(self.decode_tab, text="Browse", command=self.browse_image_decode, font=ctk.CTkFont(size=16)).pack(pady=5)

        ctk.CTkButton(self.decode_tab, text="Decode", command=self.decode_message, font=ctk.CTkFont(size=18)).pack(pady=10)

        self.decode_result_box = ctk.CTkTextbox(self.decode_tab, height=200, width=850, font=ctk.CTkFont(size=16))
        self.decode_result_box.configure(state="disabled")
        self.decode_result_box.pack(pady=10)

        self.save_decode_button = ctk.CTkButton(self.decode_tab, text="Save Output", command=self.save_last_result, font=ctk.CTkFont(size=16))
        self.save_decode_button.pack(pady=5)
        self.save_decode_button.pack_forget()

        self.new_session_button = ctk.CTkButton(self.decode_tab, text="Start New Session", command=self.clear_session, font=ctk.CTkFont(size=16))
        self.new_session_button.pack(pady=5)
        self.new_session_button.pack_forget()

    def setup_history_tab(self):
        self.history_box = ctk.CTkTextbox(self.history_tab, height=500, width=900, font=ctk.CTkFont(size=16))
        self.history_box.pack(pady=20)
        self.history_box.bind("<Double-1>", self.load_result_from_history)

    def update_history_box(self):
        self.history_box.delete("1.0", "end")
        for entry in history:
            self.history_box.insert("end", entry + "\n")

    def clear_session(self):
        self.encode_image_path.set("")
        self.decode_image_path.set("")
        self.message_text.delete("1.0", "end")
        self.decode_result_box.configure(state="normal")
        self.decode_result_box.delete("1.0", "end")
        self.decode_result_box.configure(state="disabled")
        self.save_decode_button.pack_forget()
        self.new_session_button.pack_forget()
        self.encode_new_session_button.pack_forget()

    def browse_image_encode(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp *.jpg *.jpeg")])
        if path:
            self.encode_image_path.set(path)

    def browse_image_decode(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp *.jpg *.jpeg")])
        if path:
            self.decode_image_path.set(path)

    def encode_message(self):
        img_path = self.encode_image_path.get()
        message = self.message_text.get("1.0", "end").strip()

        if not img_path or not message:
            messagebox.showerror("Error", "Both image and message are required.")
            return

        ext = os.path.splitext(img_path)[1].lower()
        if ext not in SUPPORTED_IMAGE_FORMATS:
            messagebox.showerror("Error", "Only PNG, BMP, JPG, and JPEG formats are supported.")
            return

        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        encoded = img.copy()
        binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'

        pixels = list(encoded.getdata())
        new_pixels = []
        bit_idx = 0

        for pixel in pixels:
            if bit_idx < len(binary_message):
                r, g, b = pixel[:3]
                r = (r & ~1) | int(binary_message[bit_idx])
                bit_idx += 1
                new_pixels.append((r, g, b))
            else:
                new_pixels.append(pixel)

        encoded.putdata(new_pixels)
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            encoded.save(output_path)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history.append(f"[ENCODE] {timestamp} -> {output_path}")
            session_results.append(("Encoded", message))
            self.update_history_box()
            messagebox.showinfo("Success", "Message encoded and saved successfully.")
            self.encode_new_session_button.pack(pady=5)

    def decode_message(self):
        img_path = self.decode_image_path.get()
        if not img_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        ext = os.path.splitext(img_path)[1].lower()
        if ext not in SUPPORTED_IMAGE_FORMATS:
            messagebox.showerror("Error", "Only PNG, BMP, JPG, and JPEG formats are supported.")
            return

        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        pixels = list(img.getdata())
        binary_message = ""

        for pixel in pixels:
            r = pixel[0]
            binary_message += str(r & 1)

        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        message = ""
        for char in chars:
            if char == '11111110':
                break
            message += chr(int(char, 2))

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append(f"[DECODE] {timestamp} <- {img_path}")
        session_results.append(("Decoded", message))
        self.update_history_box()
        self.decode_result_box.configure(state="normal")
        self.decode_result_box.delete("1.0", "end")
        self.decode_result_box.insert("1.0", message)
        self.decode_result_box.configure(state="disabled")
        self.save_decode_button.pack(pady=5)
        self.new_session_button.pack(pady=5)

    def save_last_result(self):
        if not session_results:
            messagebox.showinfo("Info", "No result to save.")
            return
        result_type, message = session_results[-1]
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w') as f:
                f.write(message)
            messagebox.showinfo("Success", f"{result_type} message saved at: {save_path}")

    def load_result_from_history(self, event):
        line_index = self.history_box.index("@%s,%s linestart" % (event.x, event.y))
        line = self.history_box.get(line_index, f"{line_index} lineend").strip()
        for tag, msg in session_results:
            if tag in line:
                self.decode_result_box.configure(state="normal")
                self.decode_result_box.delete("1.0", "end")
                self.decode_result_box.insert("1.0", msg)
                self.decode_result_box.configure(state="disabled")
                break

if __name__ == '__main__':
    root = ctk.CTk()
    app = SteganographyTool(root)
    root.mainloop()
