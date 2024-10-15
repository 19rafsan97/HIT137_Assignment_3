# Github: https://github.com/19rafsan97/HIT137_Assignment_3

import tkinter as tk
from tkinter import messagebox
from transformers import pipeline


# Creating a class for Text Summarization using the facebook/bart-large-cnn model
class Summarizer:
    def __init__(self):
        # Encapsulation: Using a pre-trained summarization model
        self._summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text, max_length=50, min_length=25, do_sample=False):
        # Method that interacts with the encapsulated model to summarize the text
        summary = self._summarizer_model(text, max_length=max_length, min_length=min_length, do_sample=do_sample)
        return summary[0]['summary_text']

# Base class for the application's GUI
class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarizer Application")
        self.root.geometry("500x400")

    def display(self):
        self.root.mainloop()

# Multiple inheritance: App inherits from both Summarizer and AppWindow
class TextSummarizationApp(AppWindow, Summarizer):
    def __init__(self, root):
        # Calling parent constructors: demonstrating polymorphism
        AppWindow.__init__(self, root)
        Summarizer.__init__(self)

        # Main GUI components
        self.input_text = tk.Text(self.root, height=10, width=50)
        self.input_text.pack()

        # Summarize button
        self.summarize_button = tk.Button(self.root, text="Summarize", command=self.summarize_text)
        self.summarize_button.pack(pady=10)

        # Rephrase button
        self.rephrase_button = tk.Button(self.root, text="Rephrase", command=self.rephrase_text)
        self.rephrase_button.pack(pady=5)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text)
        self.clear_button.pack(pady=5)

        self.summary_output = tk.Text(self.root, height=5, width=50)
        self.summary_output.pack()

        # Adding "About" and "How to Use" sections
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        about_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=about_menu)
        about_menu.add_command(label="About", command=self.show_about)
        about_menu.add_command(label="How to Use", command=self.show_how_to_use)

    # Method overriding: Redefining the command functionality for summarize_button
    def summarize_text(self):
        input_text = self.input_text.get("1.0", tk.END)
        if input_text.strip():
            summary = self.summarize(input_text)
            self.summary_output.delete("1.0", tk.END)
            self.summary_output.insert(tk.END, summary)
        else:
            messagebox.showerror("Error", "Input text cannot be empty!")

    def rephrase_text(self):
        input_text = self.input_text.get("1.0", tk.END)
        if input_text.strip():
            # Rephrasing uses do_sample=True for random sampling-based variation
            summary = self.summarize(input_text, max_length=50, min_length=25, do_sample=True)
            self.summary_output.delete("1.0", tk.END)
            self.summary_output.insert(tk.END, summary)
        else:
            messagebox.showerror("Error", "Input text cannot be empty!")

    def clear_text(self):
        # Clear both input and output text areas
        self.input_text.delete("1.0", tk.END)
        self.summary_output.delete("1.0", tk.END)

    @staticmethod
    def show_about():
        # About Section
        messagebox.showinfo("About", "This Text Summarization Application uses the 'facebook/bart-large-cnn' AI model to help you summarize large articles, documents, or news content.")

    @staticmethod
    def show_how_to_use():
        # How to Use Section
        messagebox.showinfo("How to Use", "1. Enter or paste the text into the input field.\n"
                                          "2. Click the 'Summarize' button.\n"
                                          "3. The summarized text will appear in the output area.\n"
                                          "4. Click the 'Rephrase' button to get a different version of the summary.\n"
                                          "5. Use the 'Clear' button to reset everything.")

# Decorator for additional functionality (e.g., logging user input length)
def input_logger(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        input_text = instance.input_text.get("1.0", tk.END)
        print(f"User entered {len(input_text.strip())} characters.")
        return func(*args, **kwargs)
    return wrapper

# Further applying decorators to enhance the summarize_text method
class EnhancedTextSummarizationApp(TextSummarizationApp):
    @input_logger
    def summarize_text(self):
        super().summarize_text()

    @input_logger
    def rephrase_text(self):
        super().rephrase_text()

# Main application start
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedTextSummarizationApp(root)
    app.display()
