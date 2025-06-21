"""
Tkinter GUI interface for the Password Strength Analyzer & Wordlist Generator.

Features:
- Password strength analysis with color-coded meter
- Wordlist generation with personal information input
- Wordlist export to text file
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Dict, Any, List, Optional

# Import local modules
from pass_tool.analyzer import PasswordAnalyzer
from pass_tool.wordlist import WordlistGenerator


class PasswordToolGUI:
    """
    Main GUI application for the Password Strength Analyzer & Wordlist Generator.
    """

    def __init__(self, master: tk.Tk):
        """
        Initialize the GUI.

        Args:
            master: Root Tkinter window
        """
        self.master = master
        self.master.title("Password Strength Analyzer & Wordlist Generator")
        self.master.geometry("700x600")
        self.master.minsize(650, 550)

        # Set application icon if available
        self._set_icon()

        # Initialize analyzers
        self.password_analyzer = PasswordAnalyzer()
        self.wordlist_generator = WordlistGenerator()

        # Create main notebook with tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.analyzer_tab = ttk.Frame(self.notebook)
        self.wordlist_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.analyzer_tab, text="Analyze Password")
        self.notebook.add(self.wordlist_tab, text="Generate Wordlist")

        # Initialize tabs
        self._init_analyzer_tab()
        self._init_wordlist_tab()

        # Create footer
        self._create_footer()

    def _set_icon(self):
        """Set the application icon if available."""
        icon_path = None

        # Look for icon in possible locations
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png"),
            os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico"),
            os.path.join(os.path.dirname(sys.argv[0]), "assets", "icon.png"),
            os.path.join(os.path.dirname(sys.argv[0]), "assets", "icon.ico"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                icon_path = path
                break

        if icon_path:
            try:
                self.master.iconphoto(True, tk.PhotoImage(file=icon_path))
            except Exception:
                # Fall back to iconbitmap for Windows if PhotoImage fails
                try:
                    if icon_path.endswith('.ico'):
                        self.master.iconbitmap(icon_path)
                except Exception:
                    pass  # Ignore if icon setting fails

    def _init_analyzer_tab(self):
        """Initialize the password analyzer tab."""
        # Password entry frame
        entry_frame = ttk.Frame(self.analyzer_tab)
        entry_frame.pack(fill="x", padx=20, pady=20)

        # Password label and entry
        ttk.Label(entry_frame, text="Enter Password:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(entry_frame, textvariable=self.password_var, width=40, show="•")
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)

        # Toggle password visibility
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(
            entry_frame, 
            text="Show Password", 
            variable=self.show_password_var, 
            command=self._toggle_password_visibility
        )
        self.show_password_check.grid(row=0, column=2, padx=5, pady=5)

        # Analyze button
        self.analyze_button = ttk.Button(
            entry_frame, 
            text="Analyze Password", 
            command=self._analyze_password
        )
        self.analyze_button.grid(row=1, column=1, padx=5, pady=10)

        # Real-time analysis option
        self.realtime_var = tk.BooleanVar(value=True)
        self.realtime_check = ttk.Checkbutton(
            entry_frame, 
            text="Analyze as I type", 
            variable=self.realtime_var
        )
        self.realtime_check.grid(row=1, column=2, padx=5, pady=10, sticky="w")

        # Results frame
        results_frame = ttk.LabelFrame(self.analyzer_tab, text="Analysis Results")
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Strength meter frame
        meter_frame = ttk.Frame(results_frame)
        meter_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(meter_frame, text="Password Strength:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.strength_var = tk.StringVar(value="N/A")
        self.strength_label = ttk.Label(meter_frame, textvariable=self.strength_var, font=("Arial", 12, "bold"))
        self.strength_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Strength meter progress bar
        self.meter_var = tk.IntVar(value=0)
        self.strength_meter = ttk.Progressbar(
            meter_frame, 
            variable=self.meter_var, 
            maximum=4, 
            mode="determinate",
            length=300
        )
        self.strength_meter.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Detailed results frame
        details_frame = ttk.Frame(results_frame)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Entropy and crack time
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill="x", pady=5)

        ttk.Label(info_frame, text="Entropy:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entropy_var = tk.StringVar(value="N/A")
        ttk.Label(info_frame, textvariable=self.entropy_var).grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(info_frame, text="Estimated Crack Time:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.crack_time_var = tk.StringVar(value="N/A")
        ttk.Label(info_frame, textvariable=self.crack_time_var).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Feedback text area
        ttk.Label(details_frame, text="Feedback:").pack(anchor="w", padx=5, pady=(10, 0))
        self.feedback_text = ScrolledText(
            details_frame, 
            wrap=tk.WORD, 
            height=5, 
            state="disabled"
        )
        self.feedback_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Bind password changes for real-time analysis
        self.password_var.trace("w", self._on_password_change)

    def _init_wordlist_tab(self):
        """Initialize the wordlist generator tab."""
        # Main container with scrolling
        container = ttk.Frame(self.wordlist_tab)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Personal information frame
        personal_frame = ttk.LabelFrame(scrollable_frame, text="Personal Information (Optional)")
        personal_frame.pack(fill="x", padx=20, pady=(10, 5), ipadx=5, ipady=5)

        # Create entry fields for personal info
        self.personal_entries = {}
        personal_fields = [
            ("name", "Full Name"),
            ("birth_date", "Birth Date (YYYY-MM-DD)"),
            ("pet_name", "Pet Name"),
            ("favorite_team", "Favorite Team"),
            ("phone", "Phone Number"),
            ("company", "Company/School"),
            ("street", "Street Address"),
            ("city", "City"),
        ]

        for i, (field, label) in enumerate(personal_fields):
            row, col = divmod(i, 2)
            ttk.Label(personal_frame, text=label).grid(row=row, column=col*2, sticky="w", padx=5, pady=5)
            self.personal_entries[field] = ttk.Entry(personal_frame, width=25)
            self.personal_entries[field].grid(row=row, column=col*2+1, sticky="ew", padx=5, pady=5)

        # Custom words frame
        custom_frame = ttk.LabelFrame(scrollable_frame, text="Custom Words (Optional)")
        custom_frame.pack(fill="x", padx=20, pady=5, ipadx=5, ipady=5)

        ttk.Label(custom_frame, text="Enter additional words (one per line):").pack(anchor="w", padx=5, pady=5)

        self.custom_words_text = ScrolledText(custom_frame, wrap=tk.WORD, height=5)
        self.custom_words_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Options frame
        options_frame = ttk.LabelFrame(scrollable_frame, text="Generation Options")
        options_frame.pack(fill="x", padx=20, pady=5, ipadx=5, ipady=5)

        # Checkboxes for options
        self.option_vars = {
            "leetspeak": tk.BooleanVar(value=True),
            "case_variations": tk.BooleanVar(value=True),
            "years": tk.BooleanVar(value=True),
            "prefixes_suffixes": tk.BooleanVar(value=True)
        }

        option_labels = {
            "leetspeak": "Include Leetspeak (a→@, e→3, i→1, o→0, s→$, t→7)",
            "case_variations": "Include Case Variations (lower/upper/mixed case)",
            "years": "Include Year Appendages (e.g. 1990, 22)",
            "prefixes_suffixes": "Include Prefixes/Suffixes"
        }

        for i, (option, var) in enumerate(self.option_vars.items()):
            ttk.Checkbutton(
                options_frame, 
                text=option_labels[option], 
                variable=var
            ).pack(anchor="w", padx=5, pady=2)

        # Word limit option
        limit_frame = ttk.Frame(options_frame)
        limit_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(limit_frame, text="Maximum words to generate:").pack(side="left", padx=5)
        self.word_limit_var = tk.StringVar(value="10000")
        ttk.Entry(limit_frame, textvariable=self.word_limit_var, width=10).pack(side="left", padx=5)

        # Generate button
        generate_frame = ttk.Frame(scrollable_frame)
        generate_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.generate_button = ttk.Button(
            generate_frame, 
            text="Generate Wordlist", 
            command=self._generate_wordlist
        )
        self.generate_button.pack(pady=10)

        # Results frame
        results_frame = ttk.LabelFrame(scrollable_frame, text="Generated Wordlist")
        results_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Stats frame
        self.stats_frame = ttk.Frame(results_frame)
        self.stats_frame.pack(fill="x", padx=5, pady=5)

        self.stats_label = ttk.Label(self.stats_frame, text="No wordlist generated yet.")
        self.stats_label.pack(anchor="w", padx=5, pady=5)

        # Wordlist preview
        self.wordlist_preview = ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            height=8, 
            state="disabled"
        )
        self.wordlist_preview.pack(fill="both", expand=True, padx=5, pady=5)

        # Save button
        self.save_button = ttk.Button(
            results_frame, 
            text="Save Wordlist", 
            command=self._save_wordlist,
            state="disabled"
        )
        self.save_button.pack(pady=10)

    def _create_footer(self):
        """Create the application footer."""
        footer_frame = ttk.Frame(self.master)
        footer_frame.pack(fill="x", padx=10, pady=5)

        footer_label = ttk.Label(
            footer_frame, 
            text="© 2025 Sridhar S",
            font=("Arial", 9)
        )
        footer_label.pack(side="right", padx=10)

    def _toggle_password_visibility(self):
        """Toggle password visibility in the entry field."""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def _on_password_change(self, *args):
        """Handle password changes for real-time analysis."""
        if self.realtime_var.get():
            self._analyze_password()

    def _analyze_password(self):
        """Analyze the entered password and display results."""
        password = self.password_var.get()

        # Get analysis results
        result = self.password_analyzer.analyze_password(password)

        # Update strength meter
        self.meter_var.set(result['score'])
        self.strength_var.set(result['strength'])
        self.strength_label.config(foreground=result['color'])

        # Update detailed results
        self.entropy_var.set(f"{result['entropy']:.1f} bits")
        self.crack_time_var.set(result['crack_time'])

        # Update feedback text
        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, result['feedback'])
        self.feedback_text.config(state="disabled")

    def _get_personal_data(self) -> Dict[str, str]:
        """Get personal data from entry fields."""
        personal_data = {}
        for field, entry in self.personal_entries.items():
            personal_data[field] = entry.get().strip()
        return personal_data

    def _get_custom_words(self) -> List[str]:
        """Get custom words from text area."""
        text = self.custom_words_text.get(1.0, tk.END).strip()
        if not text:
            return []

        # Split by lines and filter empty lines
        words = [line.strip() for line in text.split('\n') if line.strip()]
        return words

    def _generate_wordlist(self):
        """Generate the wordlist based on user inputs."""
        # Get personal data and custom words
        personal_data = self._get_personal_data()
        custom_words = self._get_custom_words()

        if not personal_data and not custom_words:
            messagebox.showwarning(
                "No Input", 
                "Please enter some personal information or custom words to generate a wordlist."
            )
            return

        # Get options
        options = {
            'personal_data': personal_data,
            'custom_words': custom_words,
            'include_leetspeak': self.option_vars['leetspeak'].get(),
            'include_case_variations': self.option_vars['case_variations'].get(),
            'include_years': self.option_vars['years'].get(),
            'include_prefixes_suffixes': self.option_vars['prefixes_suffixes'].get()
        }

        # Get word limit
        try:
            word_limit = int(self.word_limit_var.get())
            if word_limit <= 0:
                word_limit = 10000
        except ValueError:
            word_limit = 10000

        options['max_words'] = word_limit

        # Show loading cursor
        self.master.config(cursor="watch")
        self.generate_button.config(state="disabled")
        self.master.update()

        try:
            # Generate wordlist
            wordlist = self.wordlist_generator.generate_wordlist(**options)

            # Get statistics
            stats = self.wordlist_generator.get_wordlist_stats()

            # Update stats label
            stats_text = (
                f"Generated {stats['total_words']} words from {stats['base_words']} base words. "
                f"Average length: {stats['average_length']:.1f} characters."
            )
            self.stats_label.config(text=stats_text)

            # Update preview
            self.wordlist_preview.config(state="normal")
            self.wordlist_preview.delete(1.0, tk.END)

            # Show first 100 words
            preview_words = wordlist[:100]
            preview_text = '\n'.join(preview_words)

            if len(wordlist) > 100:
                preview_text += f"\n\n... and {len(wordlist) - 100} more words"

            self.wordlist_preview.insert(tk.END, preview_text)
            self.wordlist_preview.config(state="disabled")

            # Enable save button
            self.save_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate wordlist: {e}")
        finally:
            # Restore cursor
            self.master.config(cursor="")
            self.generate_button.config(state="normal")

    def _save_wordlist(self):
        """Save the generated wordlist to a file."""
        if not self.wordlist_generator.final_wordlist:
            messagebox.showwarning("No Wordlist", "Please generate a wordlist first.")
            return

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Wordlist"
        )

        if not filename:
            return  # User cancelled

        # Show loading cursor
        self.master.config(cursor="watch")
        self.save_button.config(state="disabled")
        self.master.update()

        try:
            # Save wordlist
            success = self.wordlist_generator.save_wordlist(filename)

            if success:
                messagebox.showinfo(
                    "Success", 
                    f"Wordlist saved to {filename}\n"
                    f"({len(self.wordlist_generator.final_wordlist)} words)"
                )
            else:
                messagebox.showerror("Error", "Failed to save wordlist.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wordlist: {e}")
        finally:
            # Restore cursor
            self.master.config(cursor="")
            self.save_button.config(state="normal")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PasswordToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
