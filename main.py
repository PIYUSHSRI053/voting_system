import customtkinter as ctk
from database.mongodb_client import MongoDBClient
from gui.main_window import MainWindow
import os

def main():
    # Create directories
    os.makedirs("proof_images", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("🗳️ SECURE VOTING SYSTEM v2.0")
    root.geometry("1400x900")
    
    mongo = MongoDBClient()
    app = MainWindow(root, mongo)
    
    root.protocol("WM_DELETE_WINDOW", lambda: (mongo.client.close(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()