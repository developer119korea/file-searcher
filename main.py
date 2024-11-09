import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import subprocess
import platform  # For OS detection

class FileSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Searcher")

        # Get screen width and height for center positioning
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size
        window_width = 800
        window_height = 600

        # Calculate position to center the window on the screen
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        style = ttk.Style()
        style.configure("TButton", foreground="black", background="lightgrey")
        style.map("TButton",
                  foreground=[('disabled', 'grey')],
                  background=[('disabled', 'lightgrey')])

        # Regex input field and preset dropdown with label in the same row
        self.regex_frame = tk.Frame(root)
        self.regex_frame.pack(pady=(10, 0))

        # Label for Regex input
        self.regex_label = tk.Label(self.regex_frame, text="Regex:")
        self.regex_label.pack(side="left", padx=(0, 10))

        # Regex input field
        self.regex_var = tk.StringVar(value=r'[\u4e00-\u9fff]')
        self.regex_entry = tk.Entry(self.regex_frame, textvariable=self.regex_var, width=50)
        self.regex_entry.pack(side="left")

        # Preset dropdown with label
        self.preset_label = tk.Label(self.regex_frame, text="Preset:")
        self.preset_label.pack(side="left", padx=(10, 0))

        # Dropdown menu for preset
        self.preset_var = tk.StringVar(value="Chinese")
        self.preset_dropdown = ttk.Combobox(self.regex_frame, textvariable=self.preset_var, state="readonly")
        self.preset_dropdown['values'] = ("None", "Chinese")
        self.preset_dropdown.pack(side="left")
        self.preset_dropdown.bind("<<ComboboxSelected>>", self.update_regex_from_preset)

        # Folder selection button
        self.select_folder_button = ttk.Button(root, text="Select Folder", command=self.select_folder, state="normal")
        self.select_folder_button.pack(pady=10)

        # Folder path label
        self.folder_path_label = tk.Label(root, text="Selected Folder: None")
        self.folder_path_label.pack(pady=5)

        # File list table (Treeview)
        self.columns = ("File Path", "Size (MB)", "Creation Date")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")

        # Header with sort arrow icon
        self.sort_order = {col: False for col in self.columns}
        for col in self.columns:  # All columns
            self.tree.heading(col, text=f"{col}", command=lambda _col=col: self.sort_column(_col))

        # Set column widths
        self.tree.column("File Path", width=400)
        self.tree.column("Size (MB)", width=100, anchor="center")
        self.tree.column("Creation Date", width=150, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Add "Delete Selected Files" button above "Rescan" button
        self.delete_button = ttk.Button(root, text="Delete Selected Files", command=self.delete_selected_files, state="disabled")
        self.delete_button.pack(pady=(5, 0))

        # Rescan button (Search button)
        self.rescan_button = ttk.Button(root, text="Rescan", command=self.search_files, state="disabled")
        self.rescan_button.pack(pady=10)

        # File info label (Total file count and selected files info)
        self.file_info_label = tk.Label(root, text="Total files found: 0, Selected files: 0, Total selected size: 0 MB")
        self.file_info_label.pack(pady=10)

        self.found_files = []  # List of files containing matched regex
        self.selected_folder = None
        self.previous_regex = self.regex_var.get()

        # Bind selection change event
        self.tree.bind("<<TreeviewSelect>>", self.update_selection_info)

        # Right-click context menu for "View in Finder"
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="View in Finder", command=self.view_in_finder)

        # Bind right-click event on treeview
        self.tree.bind("<Button-2>", self.show_context_menu)

    def update_regex_from_preset(self, event):
        # Update regex input field based on selected preset
        selected_preset = self.preset_var.get()
        if selected_preset == "Chinese":
            self.regex_var.set(r'[\u4e00-\u9fff]')
        elif selected_preset == "None":
            self.regex_var.set("")
        self.check_for_regex_change()

    def check_for_regex_change(self):
        # Enable Rescan button if regex has changed
        if self.regex_var.get() != self.previous_regex:
            self.rescan_button.config(state="normal")
        else:
            self.rescan_button.config(state="disabled")

    def select_folder(self):
        # Folder selection dialog
        self.selected_folder = filedialog.askdirectory()
        if not self.selected_folder:
            return

        # Update folder path label and automatically search files
        self.folder_path_label.config(text=f"Selected Folder: {self.selected_folder}")
        self.search_files()

    def search_files(self):
        # Ensure folder is selected
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        # Get regex pattern from input field
        try:
            search_pattern = re.compile(self.regex_var.get())
        except re.error:
            messagebox.showerror("Error", "Invalid regex pattern.")
            return

        # Search files matching the regex
        self.found_files = self.find_matching_files(self.selected_folder, search_pattern)
        self.display_files()

        # Update the previous regex to current one after search
        self.previous_regex = self.regex_var.get()

    def find_matching_files(self, directory, search_pattern):
        matched_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if search_pattern.search(file):
                    file_path = os.path.join(root, file)
                    size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 1)  # In MB
                    creation_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    matched_files.append((file_path, size_mb, creation_date))
        return matched_files

    def display_files(self):
        # Clear existing items from table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # No files found
        if not self.found_files:
            messagebox.showinfo("Info", "No files match the selected regex.")
            self.file_info_label.config(text="Total files found: 0, Selected files: 0, Total selected size: 0 MB")
            return

        # Add files to the table
        for file in self.found_files:
            self.tree.insert("", "end", values=file)

        # Update file count label
        self.file_info_label.config(text=f"Total files found: {len(self.found_files)}, Selected files: 0, Total selected size: 0 MB")

        # Reset selection info
        self.update_selection_info()

    def sort_column(self, col_name):
        # Reverse sort order for the column
        reverse = self.sort_order[col_name]
        self.found_files.sort(key=lambda x: x[0] if col_name == "File Path" else x[1] if col_name == "Size (MB)" else x[2], reverse=reverse)
        self.sort_order[col_name] = not reverse  # Toggle sort order for next click

        # Display sorted file list
        self.display_files()

        # Update sort arrow icon
        for col in self.columns:
            icon = "▲" if self.sort_order[col] else "▼" if col == col_name else ""
            self.tree.heading(col, text=f"{col} {icon}")

    def update_selection_info(self, event=None):
        # Get selected items from treeview
        selected_items = self.tree.selection()
        selected_files = [self.tree.item(item, "values")[0] for item in selected_items]

        # Calculate total size of selected files
        total_size = sum(os.path.getsize(file) for file in selected_files)
        total_size_mb = round(total_size / (1024 * 1024), 1)  # Convert to MB
        self.file_info_label.config(text=f"Total files found: {len(self.found_files)}, Selected files: {len(selected_items)}, Total selected size: {total_size_mb} MB")

        # Enable/Disable delete button based on selection
        if selected_items:
            self.delete_button.config(state="normal")
        else:
            self.delete_button.config(state="disabled")

    def show_context_menu(self, event):
        # Show context menu on right-click
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def view_in_finder(self):
        # Get selected file path
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], "values")[0]
            folder = os.path.dirname(file_path)

            # Get current OS to determine command
            current_os = platform.system().lower()
            if current_os == "darwin":
                # macOS: Open the folder in Finder and select the file
                subprocess.run(["open", "-R", file_path])  # -R shows the file in Finder
            elif current_os == "windows":
                # Windows: Open the folder and select the file
                subprocess.run(["explorer", "/select,", file_path])  # "/select," selects the file in Explorer

    def delete_selected_files(self):
        # Get selected files from treeview
        selected_items = self.tree.selection()
        selected_files = [self.tree.item(item, "values")[0] for item in selected_items]

        # Confirm before deleting
        confirm = messagebox.askyesno("Delete Files", f"Are you sure you want to delete {len(selected_files)} file(s)?")
        if confirm:
            success_files = []
            failed_files = []
            for file in selected_files:
                try:
                    os.remove(file)  # Delete the file
                    success_files.append(file)
                except Exception as e:
                    failed_files.append((file, str(e)))

            # Show success message
            if success_files:
                messagebox.showinfo("Success", f"Successfully deleted {len(success_files)} file(s).")

            # Show error message
            if failed_files:
                error_message = "\n".join([f"{file}: {error}" for file, error in failed_files])
                messagebox.showerror("Error", f"Failed to delete the following files:\n{error_message}")

            # Rescan after deletion
            self.search_files()

# Create the main window
root = tk.Tk()

# Create the application instance
app = FileSearcherApp(root)

# Run the application
root.mainloop()
