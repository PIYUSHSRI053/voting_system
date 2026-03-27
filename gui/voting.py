import customtkinter as ctk
from tkinter import messagebox
import cv2

class VotingGUI:
    def __init__(self, root, db, main_window):
        self.root = root
        self.db = db
        self.main = main_window
        self.current_voter = None
        self.setup_ui()
    
    def setup_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(frame, text="🗳️ VOTER LOGIN", font=ctk.CTkFont(28, bold=True))
        title.pack(pady=50)
        
        login_frame = ctk.CTkFrame(frame)
        login_frame.pack(pady=30)
        
        self.email = ctk.CTkEntry(login_frame, placeholder_text="Email", width=300)
        self.email.pack(pady=10)
        self.password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=300)
        self.password.pack(pady=10)
        
        ctk.CTkButton(login_frame, text="🔐 Login", command=self.login, width=200, height=40).pack(pady=20)
        ctk.CTkButton(frame, text="🔙 Back", command=self.main.show_menu).pack(pady=20)
    
    def login(self):
        voter = self.db.login_voter(self.email.get(), self.password.get())
        if voter:
            self.current_voter = voter
            self.show_voting_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def show_voting_screen(self):
        # Simplified voting - show candidates
        candidates = self.db.get_candidates()
        
        for w in self.root.winfo_children():
            w.destroy()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"Welcome {self.current_voter['name']}", 
                    font=ctk.CTkFont(24, bold=True)).pack(pady=30)
        
        # Capture face for verification
        self.cap = cv2.VideoCapture(0)
        self.label = ctk.CTkLabel(frame, text="Face verification...", width=400, height=300)
        self.label.pack(pady=20)
        
        self.update_camera()
        
        vote_frame = ctk.CTkFrame(frame)
        vote_frame.pack(pady=30)
        
        self.selected = ctk.StringVar()
        for cand in candidates:
            ctk.CTkRadioButton(vote_frame, text=f"{cand['name']} ({cand['party']})", 
                             variable=self.selected, value=str(cand['_id'])).pack(pady=10)
        
        ctk.CTkButton(vote_frame, text="✅ Vote", command=self.submit_vote).pack(pady=20)
    
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ctk.CTkImage(image=rgb_frame, size=(400, 300))
            self.label.configure(image=img)
        