import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --- GUI THEME CONFIGURATION ---
# You can change these values to customize the look and feel
THEME_CONFIG = {
    'bg_main': '#121212',
    'bg_card': '#1E1E1E',
    'bg_header': '#121212',
    'bg_input': '#252525',
    'text_primary': '#E0E0E0',
    'text_secondary': '#A0A0A0',
    'text_accent': '#3498db',
    'border_color': '#333333',
    'separator_color': '#4A4A25', # Pastel Yellow
    
    # Selection Colors (Pastel Tones)
    'color_yes': '#1B3C1B',      # Soft Dark Green
    'color_no': '#3C1B1B',       # Soft Dark Red
    'color_modified': '#1B2A3C', # Soft Dark Blue
    
    # Dashboard Verdict Colors
    'v_nok_bg': '#4A2525',
    'v_nok_fg': '#FF9999',
    'v_marg_bg': '#4A4A25',
    'v_marg_fg': '#FFFF99',
    'v_ok_bg': '#254A25',
    'v_ok_fg': '#B2FFB2',
    'v_manual_bg': '#333333',
    
    # Typography
    'font_header': ('Segoe UI', 12, 'bold'),
    'font_sub': ('Segoe UI', 8),
    'font_table': ('Segoe UI', 9),
    'font_table_bold': ('Segoe UI', 8, 'bold'),
    'font_mono': ('Consolas', 9),
    'font_title': ('Segoe UI', 18, 'bold')
}

class VoltageConfirmationList:
    """A sleek Dark Mode GUI with centralized theme config."""
    def __init__(self, parent, candidates):
        self.results = {}
        self.top = tk.Toplevel(parent)
        self.top.title("Confirm Detected Voltage Points")
        self.top.geometry("700x550")
        self.top.configure(bg=THEME_CONFIG['bg_main'])
        self.top.grab_set()
        
        # Center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

        header_frame = tk.Frame(self.top, bg=THEME_CONFIG['bg_header'], pady=10)
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="Net Voltage Confirmation", 
                 font=THEME_CONFIG['font_header'], bg=THEME_CONFIG['bg_header'], fg=THEME_CONFIG['text_primary']).pack()
        tk.Label(header_frame, text="Highlights: Green (Confirmed) | Red (Excluded) | Blue (Modified Value)", 
                 font=THEME_CONFIG['font_sub'], bg=THEME_CONFIG['bg_header'], fg=THEME_CONFIG['text_secondary']).pack()
        
        # Scrollable container
        container = tk.Frame(self.top, bg=THEME_CONFIG['bg_main'])
        container.pack(expand=True, fill='both', padx=10, pady=5)
        
        canvas = tk.Canvas(container, bg=THEME_CONFIG['bg_main'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=THEME_CONFIG['bg_main'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # Table Headers
        head_row = tk.Frame(self.scrollable_frame, bg=THEME_CONFIG['bg_main'])
        head_row.pack(fill='x', pady=(0, 2))
        tk.Label(head_row, text="NET NAME", width=35, anchor='w', font=THEME_CONFIG['font_table_bold'], 
                 bg=THEME_CONFIG['bg_main'], fg=THEME_CONFIG['text_secondary']).pack(side='left')
        tk.Label(head_row, text="VOLTAGE (V)", width=12, font=THEME_CONFIG['font_table_bold'], 
                 bg=THEME_CONFIG['bg_main'], fg=THEME_CONFIG['text_secondary']).pack(side='left')
        tk.Label(head_row, text="DECISION", width=20, font=THEME_CONFIG['font_table_bold'], 
                 bg=THEME_CONFIG['bg_main'], fg=THEME_CONFIG['text_secondary']).pack(side='left')

        self.rows = []
        for net, val in candidates.items():
            # Separator Line
            tk.Frame(self.scrollable_frame, height=1, bg=THEME_CONFIG['separator_color']).pack(fill='x')

            row_frame = tk.Frame(self.scrollable_frame, pady=4, bg=THEME_CONFIG['bg_card'])
            row_frame.pack(fill='x')
            
            # Net Name
            name_label = tk.Label(row_frame, text=net, width=35, anchor='w', font=THEME_CONFIG['font_table'],
                                 bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_primary'])
            name_label.pack(side='left', padx=2)
            
            # Voltage Input
            original_val = str(val)
            entry_var = tk.StringVar(value=original_val)
            entry = tk.Entry(row_frame, width=8, textvariable=entry_var, font=THEME_CONFIG['font_mono'], 
                            bg=THEME_CONFIG['bg_input'], fg=THEME_CONFIG['text_primary'], insertbackground='white',
                            borderwidth=1, relief='flat', justify='center')
            entry.pack(side='left', padx=5)
            
            # Decision
            decision_var = tk.StringVar(value="confirm")
            ctrl_frame = tk.Frame(row_frame, bg=THEME_CONFIG['bg_card'])
            ctrl_frame.pack(side='left', padx=10)
            
            rb_yes = tk.Radiobutton(ctrl_frame, text="Confirm", variable=decision_var, value="confirm", 
                                    font=THEME_CONFIG['font_sub'], bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_primary'],
                                    selectcolor="#333", activebackground=THEME_CONFIG['bg_card'],
                                    activeforeground="white")
            rb_yes.pack(side='left')
            
            rb_no = tk.Radiobutton(ctrl_frame, text="Exclude", variable=decision_var, value="exclude", 
                                   font=THEME_CONFIG['font_sub'], bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_primary'],
                                   selectcolor="#333", activebackground=THEME_CONFIG['bg_card'],
                                   activeforeground="white")
            rb_no.pack(side='left', padx=5)

            row_data = {
                'row_frame': row_frame,
                'name_label': name_label,
                'ctrl_frame': ctrl_frame,
                'entry': entry,
                'entry_var': entry_var,
                'decision_var': decision_var,
                'original_val': original_val,
                'rbs': [rb_yes, rb_no],
                'net': net
            }
            
            entry_var.trace_add("write", lambda *args, rd=row_data: self.update_row_color(rd))
            decision_var.trace_add("write", lambda *args, rd=row_data: self.update_row_color(rd))
            
            self.update_row_color(row_data)
            self.rows.append(row_data)

        btn_container = tk.Frame(self.top, bg=THEME_CONFIG['bg_main'], pady=15)
        btn_container.pack(fill='x')
        tk.Button(btn_container, text="Verify Ratings", bg="#2a2a2a", fg="white", 
                  activebackground="#444", font=THEME_CONFIG['font_table'], 
                  padx=25, pady=6, relief='flat', borderwidth=1, command=self.on_confirm).pack()

    def update_row_color(self, row):
        decision = row['decision_var'].get()
        current_v = row['entry_var'].get()
        
        bg_col = THEME_CONFIG['bg_card']
        
        if decision == 'exclude':
            bg_col = THEME_CONFIG['color_no']
        elif current_v != row['original_val']:
            bg_col = THEME_CONFIG['color_modified']
        elif decision == 'confirm':
            bg_col = THEME_CONFIG['color_yes']
            
        row['row_frame'].configure(bg=bg_col)
        row['name_label'].configure(bg=bg_col)
        row['ctrl_frame'].configure(bg=bg_col)
        for rb in row['rbs']:
            rb.configure(bg=bg_col)

    def on_confirm(self):
        for row in self.rows:
            try:
                v_str = row['entry_var'].get()
                v = float(v_str) if v_str else 0.0
                self.results[row['net']] = {
                    'action': row['decision_var'].get(),
                    'voltage': v
                }
            except ValueError:
                messagebox.showerror("Error", f"Invalid voltage for {row['net']}")
                return
        self.top.destroy()

class NetlistSelectionPage:
    """A professional landing page for netlist selection."""
    def __init__(self, parent, initial_path=None):
        self.parent = parent
        self.selected_path = initial_path
        self.confirmed = False
        
        self.top = tk.Toplevel(parent)
        print(f"[Debug] selection_page.top created. Title: {self.top.title()}")
        self.top.title("Auto_Altium | Rating Verification V2.0")
        self.top.geometry("600x400")
        self.top.configure(bg=THEME_CONFIG['bg_main'])
        self.top.resizable(False, False)
        
        # Simplified visibility
        self.top.geometry("600x400+50+50")
        self.top.lift()
        self.top.attributes('-topmost', True)
        self.top.attributes('-topmost', False)
        
        # self.top.update_idletasks()
        # width = 600
        # height = 400
        # x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        # y = (self.top.winfo_screenheight() // 2) - (height // 2)
        # self.top.geometry(f'{width}x{height}+{x}+{y}')

        # Background Design (Subtle gradient effect simulated with frames)
        main_frame = tk.Frame(self.top, bg=THEME_CONFIG['bg_card'], highlightbackground=THEME_CONFIG['text_accent'], highlightthickness=1)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=540, height=340)

        # Title
        tk.Label(main_frame, text="COMPONENT RATING VERIFIER", font=THEME_CONFIG['font_title'], 
                 bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_accent']).pack(pady=(40, 5))
        tk.Label(main_frame, text="Version 2.0 | Worst-Case Switching Path Mode", font=THEME_CONFIG['font_sub'], 
                 bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_secondary']).pack()

        # Input Area
        input_frame = tk.Frame(main_frame, bg=THEME_CONFIG['bg_card'])
        input_frame.pack(pady=40, fill='x', padx=40)

        self.path_var = tk.StringVar(value=self.selected_path or "No file selected...")
        self.entry = tk.Entry(input_frame, textvariable=self.path_var, font=THEME_CONFIG['font_mono'], 
                             bg='white', fg='black', readonlybackground='white',
                             borderwidth=1, relief='flat', state='readonly')
        self.entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))

        tk.Button(input_frame, text="BROWSE", command=self.browse_file, bg="#333", fg="white", 
                  relief='flat', font=THEME_CONFIG['font_table_bold'], padx=15).pack(side='right')

        # Action Button
        self.start_btn = tk.Button(main_frame, text="START ANALYSIS", command=self.start_analysis, 
                                 bg=THEME_CONFIG['text_accent'], fg="white", font=('Segoe UI', 10, 'bold'),
                                 relief='flat', padx=40, pady=10, activebackground='#2980b9')
        self.start_btn.pack(pady=20)
        
        if not self.selected_path:
            self.start_btn.configure(state='disabled', bg='#555')

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select Altium Netlist (.NET)",
            filetypes=[("Netlist files", "*.NET"), ("All files", "*.*")]
        )
        if path:
            self.selected_path = path
            self.path_var.set(path)
            self.start_btn.configure(state='normal', bg=THEME_CONFIG['text_accent'])

    def start_analysis(self):
        if self.selected_path and os.path.exists(self.selected_path):
            self.confirmed = True
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Please select a valid netlist file.")

class RatingsDashboard:
    """Main results window with Sleek Dark Theme and Executive Summary."""
    def __init__(self, parent, results_data):
        self.results = results_data
        self.top = tk.Toplevel(parent)
        self.top.title("Verification Results Dashboard")
        self.top.geometry("1100x700")
        self.top.configure(bg=THEME_CONFIG['bg_main'])
        
        # Center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

        # 1. Executive Summary Header
        total = len(results_data)
        noks = [r for r in results_data if str(r.get('Verdict', '')).startswith('NOK')]
        reviews = [r for r in results_data if str(r.get('Verdict', '')).startswith('User Review')]
        marginals = [r for r in results_data if str(r.get('Verdict', '')).startswith('Marginal')]
        missing = [r for r in results_data if "Missing Data" in str(r.get('Verdict', ''))]
        fails = [r for r in results_data if r.get('AuditVerdict') == 'FAIL']
        
        # OK is total minus everything that isn't OK
        # We need to be careful with double counting (e.g. a component with FAIL audit and NOK verdict)
        problematic_indices = set()
        for i, r in enumerate(results_data):
            v = str(r.get('Verdict', ''))
            av = r.get('AuditVerdict', '')
            if (
                v.startswith('NOK')
                or v.startswith('Marginal')
                or v.startswith('User Review')
                or "Missing Data" in v
                or av == 'FAIL'
                or av == 'WARNING'
            ):
                problematic_indices.add(i)
        
        ok_count = total - len(problematic_indices)
        
        summary_frame = tk.Frame(self.top, bg=THEME_CONFIG['bg_card'], padx=20, pady=15)
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(summary_frame, text="EXECUTIVE SUMMARY", font=('Segoe UI', 12, 'bold'), 
                 bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_accent']).pack(side='left')
        
        stats_text = (
            f"Total: {total} | NOK: {len(noks) + len(reviews)} | Marginal: {len(marginals)} "
            f"| Fail/Issue: {len(fails)} | Missing: {len(missing)} | OK: {ok_count}"
        )
        tk.Label(summary_frame, text=stats_text, font=('Segoe UI', 11), 
                 bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_primary']).pack(side='right')

        # 2. Results Table
        table_frame = tk.Frame(self.top, bg=THEME_CONFIG['bg_main'])
        table_frame.pack(expand=True, fill='both', padx=20, pady=5)
        
        cols = ['Designator', 'Type', 'Description', 'Applied', 'Rating', 'Verdict', 'AuditVerdict', 'AuditReason']
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=15)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        for col in cols:
            self.tree.heading(col, text=col.upper())
            width = 150 if 'Reason' in col or col == 'Description' else 100
            self.tree.column(col, width=width, anchor='center')
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=THEME_CONFIG['bg_card'], foreground=THEME_CONFIG['text_primary'], 
                        fieldbackground=THEME_CONFIG['bg_card'], rowheight=25, font=THEME_CONFIG['font_table'])
        style.configure("Treeview.Heading", background='#333333', foreground=THEME_CONFIG['text_accent'], font=('Segoe UI', 9, 'bold'))
        
        self.tree.tag_configure('NOK', background='#FFC7CE', foreground='#9C0006')
        self.tree.tag_configure('Marginal', background='#FFEB9C', foreground='#9C6500')
        self.tree.tag_configure('OK', background='#C6EFCE', foreground='#006100')
        self.tree.tag_configure('FAIL', background='#FF0000', foreground='white')
        self.tree.tag_configure('WARNING', background='#ADD8E6', foreground='#000080')
        self.tree.tag_configure('UNKNOWN', background='#D3D3D3', foreground='black')
        
        def _sort_key(item):
            verdict = str(item.get('Verdict', ''))
            if verdict.startswith('NOK') or verdict.startswith('User Review'):
                return 0
            if verdict.startswith('Marginal'):
                return 1
            if verdict.startswith('OK'):
                return 2
            return 3

        sorted_data = sorted(results_data, key=_sort_key)
        for item in sorted_data:
            values = tuple(item.get(col, '-') for col in cols)
            # Tag logic: AuditVerdict takes priority over Verdict
            tag = item.get('Verdict', '')
            if item.get('AuditVerdict') == 'FAIL':
                tag = 'FAIL'
            elif item.get('AuditVerdict') == 'WARNING' and not tag.startswith('NOK'):
                tag = 'WARNING'
            elif "Missing Data" in tag or tag.startswith('Unknown'):
                tag = 'UNKNOWN'
            elif tag.startswith('User Review'):
                tag = 'WARNING'  # User Review Required -> yellow
            elif tag.startswith('OK'):
                tag = 'OK'  # Handles "OK" and "OK (Switching)"
            elif tag.startswith('Marginal'):
                tag = 'Marginal'
            elif tag.startswith('NOK'):
                tag = 'NOK'
            else:
                tag = 'UNKNOWN'
                
            self.tree.insert('', 'end', values=values, tags=(tag,))
            
        self.tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        # 3. Action Buttons
        btn_frame = tk.Frame(self.top, bg=THEME_CONFIG['bg_main'], pady=20)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="CLOSE", command=self.top.destroy, width=15,
                  bg=THEME_CONFIG['bg_card'], fg=THEME_CONFIG['text_primary'], font=('Segoe UI', 9, 'bold')).pack(side='right', padx=20)
                  
    def _get_summary_text(self, data):
        total = len(data)
        noks = len([i for i in data if i.get('Verdict') == 'NOK'])
        margs = len([i for i in data if i.get('Verdict') == 'Marginal'])
        return f" VERIFICATION REPORT | Total: {total} | Flagged: {noks} NOK | {margs} Marginal "
