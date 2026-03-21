import tkinter as tk
import random
class GuessTheWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Word")
        self.root.geometry("500x450")
        self.root.configure(bg="#f0f4f8") # Light grayish-blue background
        self.root.resizable(False, False)

        # Game Data
        self.word_list = [
            "COMPUTER", "PROGRAMMING", "PYTHON", "VARIABLE", 
            "ALGORITHM", "DATABASE", "NETWORK", "DEVELOPER", 
            "SOFTWARE", "INTERFACE", "TKINTER", "WIDGET"
        ]
        self.max_tries = 6
        
        # State variables
        self.secret_word = ""
        self.guessed_letters = set()
        self.attempts_left = 0
        self.game_over = False

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        """Creates and places all the GUI widgets."""
        # Title
        title_label = tk.Label(self.root, text="Guess the Word!", font=("Helvetica", 24, "bold"), bg="#f0f4f8", fg="#2c3e50")
        title_label.pack(pady=(20, 10))

        # Word Display (e.g., _ _ P P L _)
        self.word_label = tk.Label(self.root, text="", font=("Courier New", 28, "bold"), bg="#f0f4f8", fg="#34495e")
        self.word_label.pack(pady=20)

        # Status/Feedback Message
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f0f4f8")
        self.status_label.pack(pady=5)

        # Attempts Remaining
        self.attempts_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"), bg="#f0f4f8", fg="#e74c3c")
        self.attempts_label.pack(pady=5)

        # Input Frame (Entry + Button)
        input_frame = tk.Frame(self.root, bg="#f0f4f8")
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Enter a letter:", font=("Helvetica", 12), bg="#f0f4f8").grid(row=0, column=0, padx=5)
        
        self.entry_var = tk.StringVar()
        self.guess_entry = tk.Entry(input_frame, textvariable=self.entry_var, font=("Helvetica", 14), width=5, justify="center")
        self.guess_entry.grid(row=0, column=1, padx=5)
        
        # Bind the Enter key to the guess function
        self.root.bind('<Return>', self.make_guess)

        self.guess_btn = tk.Button(input_frame, text="Guess", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", 
                                   activebackground="#2980b9", activeforeground="white", command=self.make_guess)
        self.guess_btn.grid(row=0, column=2, padx=10)

        # Play Again Button (Hidden by default)
        self.play_again_btn = tk.Button(self.root, text="Play Again", font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white",
                                        activebackground="#27ae60", activeforeground="white", command=self.start_new_game)
        # We don't pack it here; we pack it when the game ends.

    def start_new_game(self):
        """Initializes or resets the game state."""
        self.secret_word = random.choice(self.word_list)
        self.guessed_letters.clear()
        self.attempts_left = self.max_tries
        self.game_over = False

        # Reset UI elements
        self.update_word_display()
        self.set_status("Game started! Good luck.", "#34495e")
        self.update_attempts_display()
        
        self.guess_entry.config(state="normal")
        self.guess_btn.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus() # Put text cursor in the entry box
        
        self.play_again_btn.pack_forget() # Hide play again button

    def update_word_display(self):
        """Updates the _ _ _ visual based on guessed letters."""
        display = [char if char in self.guessed_letters else '_' for char in self.secret_word]
        self.word_label.config(text=" ".join(display))

    def update_attempts_display(self):
        self.attempts_label.config(text=f"Attempts remaining: {self.attempts_left}")

    def set_status(self, message, color):
        """Helper to update the feedback text and color."""
        self.status_label.config(text=message, fg=color)

    def make_guess(self, event=None):
        """Handles the logic when the user submits a guess."""
        if self.game_over:
            return

        guess = self.entry_var.get().upper().strip()
        self.guess_entry.delete(0, tk.END) # Clear entry box

        # 1. Input Validation
        if len(guess) != 1 or not guess.isalpha():
            self.set_status("Invalid input! Please enter a single letter.", "#e67e22") # Orange
            return
        
        if guess in self.guessed_letters:
            self.set_status(f"You already guessed '{guess}'. Try another.", "#e67e22")
            return

        # 2. Process Guess
        self.guessed_letters.add(guess)

        if guess in self.secret_word:
            self.set_status(f"Good job! '{guess}' is in the word.", "#27ae60") # Green
        else:
            self.set_status(f"Sorry, '{guess}' is not in the word.", "#e74c3c") # Red
            self.attempts_left -= 1

        # 3. Update Displays
        self.update_word_display()
        self.update_attempts_display()

        # 4. Check Win/Loss Conditions
        self.check_game_over()

    def check_game_over(self):
        """Checks if the player has won or lost."""
        # Win condition: No underscores left in the display
        current_display = self.word_label.cget("text").replace(" ", "")
        
        if current_display == self.secret_word:
            self.set_status("🎉 CONGRATULATIONS! You won! 🎉", "#27ae60")
            self.end_game()
        elif self.attempts_left <= 0:
            self.set_status(f"💀 GAME OVER! The word was: {self.secret_word}", "#c0392b")
            self.word_label.config(text=" ".join(list(self.secret_word)), fg="#e74c3c") # Reveal word in red
            self.end_game()

    def end_game(self):
        """Disables inputs and shows the Play Again button."""
        self.game_over = True
        self.guess_entry.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self.play_again_btn.pack(pady=20)


if __name__ == "__main__":
    # Create the main window and start the application
    root = tk.Tk()
    app = GuessTheWordApp(root)
    
    # Ensures the window appears on top of other windows when launched
    root.attributes('-topmost', True) 
    root.update()
    root.attributes('-topmost', False)
    
    root.mainloop()