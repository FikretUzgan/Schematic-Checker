"""
Tkinter-based interactive net selector with filtering.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Tuple


class TkNetSelector:
    """
    Tkinter-based net selector with real-time filtering.
    Shows filtered list as user types characters.
    Supports multi-select with CTRL+click.
    """
    
    def __init__(self, parent, available_nets: List[str]):
        self.available_nets = sorted(available_nets)
        self.selected_nets = []  # Changed to list for multi-select
        self.selected_voltage = None
        
        self.window = tk.Toplevel(parent)
        self.window.title("Add Net Voltage")
        self.window.geometry("500x450")
        self.window.configure(bg='#121212')
        self.window.grab_set()
        
        # Make window modal and center it
        self.window.transient(parent)
        self.window.update_idletasks()
        
        # Header
        header_frame = tk.Frame(self.window, bg='#1E1E1E', pady=10)
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="SELECT NET(S) FROM NETLIST", 
                font=('Segoe UI', 11, 'bold'), bg='#1E1E1E', fg='#E0E0E0').pack()
        tk.Label(header_frame, text="Type to filter | CTRL+Click for multiple | Double-click to confirm", 
                font=('Segoe UI', 8), bg='#1E1E1E', fg='#A0A0A0').pack()
        
        # Filter input
        input_frame = tk.Frame(self.window, bg='#121212', pady=10)
        input_frame.pack(fill='x', padx=15)
        
        tk.Label(input_frame, text="Filter:", font=('Segoe UI', 9), 
                bg='#121212', fg='#E0E0E0').pack(side='left', padx=(0, 5))
        
        # Create StringVar and trace it with mode 'w' (write)
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add('write', self._on_filter_change)
        
        self.filter_entry = tk.Entry(input_frame, textvariable=self.filter_var,
                                     font=('Segoe UI', 10), bg='#252525', fg='#E0E0E0',
                                     insertbackground='white', borderwidth=1, relief='flat')
        self.filter_entry.pack(side='left', fill='x', expand=True)
        self.filter_entry.focus()
        
        # Net list frame with scrollbar
        list_frame = tk.Frame(self.window, bg='#121212')
        list_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.net_listbox = tk.Listbox(list_frame, font=('Segoe UI', 9),
                                      bg='#252525', fg='#E0E0E0',
                                      selectmode='extended',  # Changed to extended for CTRL+click
                                      yscrollcommand=scrollbar.set,
                                      borderwidth=1, relief='flat',
                                      highlightthickness=0)
        self.net_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.net_listbox.yview)
        self.net_listbox.bind('<Double-Button-1>', self._on_net_selected)
        self.net_listbox.bind('<Return>', self._on_net_selected)
        
        # Info label showing match count
        self.info_label = tk.Label(self.window, text=f"Available: {len(self.available_nets)} nets",
                                   font=('Segoe UI', 8), bg='#121212', fg='#A0A0A0')
        self.info_label.pack(fill='x', padx=15, pady=(0, 10))
        
        # Voltage input frame
        voltage_frame = tk.Frame(self.window, bg='#121212')
        voltage_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(voltage_frame, text="Voltage (V):", font=('Segoe UI', 9),
                bg='#121212', fg='#E0E0E0').pack(side='left', padx=(0, 5))
        
        self.voltage_var = tk.StringVar(value='3.3')
        self.voltage_entry = tk.Entry(voltage_frame, textvariable=self.voltage_var,
                                      font=('Segoe UI', 10), bg='#252525', fg='#E0E0E0',
                                      insertbackground='white', borderwidth=1, relief='flat',
                                      width=15, justify='right')
        self.voltage_entry.pack(side='left', padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#121212', pady=10)
        button_frame.pack(fill='x', padx=15)
        
        tk.Button(button_frame, text="ADD", command=self._on_add,
                 bg='#3498db', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='flat', padx=20).pack(side='right', padx=5)
        
        tk.Button(button_frame, text="CANCEL", command=self._on_cancel,
                 bg='#555555', fg='white', font=('Segoe UI', 9),
                 relief='flat', padx=20).pack(side='right', padx=5)
        
        # Populate initial list
        self._populate_list()
    
    def _populate_list(self, filter_text: str = ""):
        """Populate listbox with filtered nets."""
        self.net_listbox.delete(0, tk.END)
        
        filter_lower = filter_text.lower()
        filtered = [net for net in self.available_nets 
                   if net.lower().startswith(filter_lower)]
        
        for net in filtered:
            self.net_listbox.insert(tk.END, net)
        
        # Update info label
        if filtered:
            self.info_label.config(text=f"Showing: {len(filtered)}/{len(self.available_nets)} nets")
            if filtered:
                self.net_listbox.selection_set(0)
                self.net_listbox.see(0)
        else:
            self.info_label.config(text=f"No matches (filtered from {len(self.available_nets)} nets)")
    
    def _on_filter_change(self, *args):
        """Update list as filter text changes."""
        filter_text = self.filter_var.get()
        self._populate_list(filter_text)
    
    def _on_net_selected(self, event=None):
        """Handle net selection via double-click or Enter."""
        selection = self.net_listbox.curselection()
        if selection:
            # Get all selected nets
            self.selected_nets = [self.net_listbox.get(idx) for idx in selection]
            self._on_add()
    
    def _on_add(self):
        """Confirm selection and close dialog."""
        selection = self.net_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("No Selection", "Please select at least one net from the list.")
            return
        
        # Get all selected nets
        self.selected_nets = [self.net_listbox.get(idx) for idx in selection]
        
        try:
            self.selected_voltage = float(self.voltage_var.get())
        except ValueError:
            tk.messagebox.showerror("Invalid Voltage", 
                                   f"'{self.voltage_var.get()}' is not a valid number.")
            return
        
        self.window.destroy()
    
    def _on_cancel(self):
        """Cancel selection."""
        self.selected_nets = []
        self.selected_voltage = None
        self.window.destroy()


def show_net_selector(parent, available_nets: List[str]) -> Optional[List[Tuple[str, float]]]:
    """
    Show net selector dialog and return list of (net_name, voltage) tuples or None if cancelled.
    Supports multi-select with CTRL+click - all selected nets get the same voltage.
    """
    selector = TkNetSelector(parent, available_nets)
    parent.wait_window(selector.window)
    
    if selector.selected_nets and selector.selected_voltage is not None:
        # Return list of tuples, all with the same voltage
        return [(net, selector.selected_voltage) for net in selector.selected_nets]
    return None
