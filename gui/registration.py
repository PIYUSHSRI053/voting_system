import customtkinter as ctk
from tkinter import messagebox
from services.face_service import FaceService
from database.mongodb_client import MongoDBClient

class RegistrationGUI:
    def __init__(self, root, db, main_window):
        self.root = root
        self.db = db
        self.main = main_window
        self.face_service = FaceService()
        self.setup_ui()
    
    def setup_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = ctk.CTkLabel(frame, text="👤 VOTER REGISTRATION", font=ctk.CTkFont(28, bold=True))
        title.pack(pady=30)
        
        # Form
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        self.entries = {}
        fields = [("Name", "name"), ("Email", "email"), ("Phone", "phone"), 
                 ("National ID", "national_id"), ("Address", "address"), ("Password", "password")]
        
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=f"{label}:").grid(row=i//2, column=(i%2)*2, padx=20, pady=15, sticky="w")
            entry = ctk.CTkEntry(form_frame, width=250)
            entry.grid(row=i//2, column=(i%2)*2+1, padx=20, pady=15)
            self.entries[key] = entry
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=40)
        
        ctk.CTkButton(btn_frame, text="📸 Capture Face", command=self.capture_face, width=200).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="✅ Register", command=self.register, width=200).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="🔙 Back", command=self.main.show_menu, width=200).pack(side="left", padx=20)
    
    def capture_face(self):
        encoding, path = self.face_service.capture_and_encode()
        if encoding:
            self.face_encoding = encoding
            self.photo_path = path
            messagebox.showinfo("Success", f"Photo saved: {path}")
    
    def register(self):
        try:
            data = {k: v.get() for k, v in self.entries.items()}
            data.update({
                'face_encoding': self.face_encoding,
                'photo_path': self.photo_path
            })
            
            voter_id = self.db.register_voter(data)
            messagebox.showinfo("Success", f"Registered! ID: {voter_id}")
            self.main.show_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))