import customtkinter as ctk
from gui.registration import RegistrationGUI
from gui.voting import VotingGUI
from gui.admin import AdminGUI
from gui.results import ResultsGUI

class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.show_menu()
    
    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", pady=30)
        
        ctk.CTkLabel(header, text="🗳️ ENTERPRISE VOTING SYSTEM", 
                    font=ctk.CTkFont(36, bold=True)).pack()
        
        # Buttons
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=50, pady=20)
        
        buttons = [
            ("👤 Voter Registration", self.show_registration),
            ("🗳️ Cast Vote", self.show_voting),
            ("👨‍💼 Admin Panel", self.show_admin),
            ("📊 Results Dashboard", self.show_results)
        ]
        
        for text, cmd in buttons:
            btn = ctk.CTkButton(container, text=text, command=cmd, height=70, 
                              font=ctk.CTkFont(20, bold=True))
            btn.pack(pady=20, padx=50, fill="x")
    
    def show_registration(self): RegistrationGUI(self.root, self.db, self)
    def show_voting(self): VotingGUI(self.root, self.db, self)
    def show_admin(self): AdminGUI(self.root, self.db, self)
    def show_results(self): ResultsGUI(self.root, self.db, self)