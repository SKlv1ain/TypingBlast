import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import subprocess
import sys
import os

class StatsDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Typing Blast Stats Dashboard")
        self.geometry("1000x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.df = self._load_data()

        self.topbar = ctk.CTkFrame(self, height=40)
        self.topbar.grid(row=0, column=0, sticky="new")
        self.topbar.grid_columnconfigure((0,1), weight=0)

        ctk.CTkButton(
            self.topbar, text="Back to Game",
            command=self._back_to_game,
            fg_color="green", hover_color="#157347", text_color="white"
        ).grid(row=0, column=0, padx=10, pady=5)

        ctk.CTkButton(
            self.topbar, text="Exit",
            command=self.destroy,
            fg_color="red", hover_color="#a30000", text_color="white"
        ).grid(row=0, column=1, padx=10, pady=5)

        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        for name in ("Descriptive Stats", "Visualization", "Comparison", "Raw Data"):
            self.tabview.add(name)

        self._setup_descriptive()
        self._setup_visualization()
        self._setup_comparison()
        self._setup_raw_data()

    def _back_to_game(self):
        self.destroy()
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "main.py")])


    def _load_data(self):
        try:
            return pd.read_csv("results.csv")
        except FileNotFoundError:
            return pd.DataFrame()

    def _setup_descriptive(self):
        tab = self.tabview.tab("Descriptive Stats")
        if self.df.empty:
            ctk.CTkLabel(tab, text="No data.", font=("Arial", 16)).pack(pady=20)
            return

        numeric_cols = [c for c in self.df.columns if pd.api.types.is_numeric_dtype(self.df[c])]
        self.desc_var = ctk.StringVar(value=numeric_cols[0])
        ctk.CTkOptionMenu(
            tab,
            values=numeric_cols,
            variable=self.desc_var,
            command=self._render_descriptive
        ).pack(pady=(10,5))

        container = ctk.CTkScrollableFrame(tab, width=900, height=550)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        container.grid_columnconfigure(0, weight=1)
        self.desc_container = container
        self.desc_container.bind_all("<MouseWheel>", self._on_mousewheel)
        self._render_descriptive(self.desc_var.get())

    def _on_mousewheel(self, event):
        try:
            self.desc_container._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except AttributeError:
            pass

    def _render_descriptive(self, column):
        for widget in self.desc_container.winfo_children():
            widget.destroy()
        data = self.df[column].dropna()
        desc = data.describe()
        q1, q3 = desc['25%'], desc['75%']
        iqr = q3 - q1
        lower_iqr = q1 - 1.5 * iqr
        upper_iqr = q3 + 1.5 * iqr
        mean, sd = desc['mean'], data.std()
        lower_sd = mean - 3 * sd
        upper_sd = mean + 3 * sd
        sections = [
            ("Centrality", [
                ("Count", int(desc['count'])),
                ("Mean", round(mean,4)),
                ("Median", round(desc['50%'],4)),
                ("Mode", data.mode().iloc[0] if not data.mode().empty else None)
            ]),
            ("Dispersion", [
                ("Min", desc['min']),
                ("Max", desc['max']),
                ("Range", round(desc['max'] - desc['min'],4)),
                ("Variance", round(data.var(),4)),
                ("Std Dev", round(sd,4)),
                ("CV", round(sd/mean if mean!=0 else 0,4)),
                ("MAD", round(np.mean(np.abs(data - mean)),4)),
                ("Q1", round(q1,4)),
                ("Q3", round(q3,4)),
                ("IQR", round(iqr,4))
            ]),
            ("Outliers", [
                ("Q1-1.5 IQR", round(lower_iqr,4)),
                ("Q3+1.5 IQR", round(upper_iqr,4)),
                ("IQR-based", ", ".join(map(str,data[(data<lower_iqr)|(data>upper_iqr)].tolist())) or "None"),
                ("Mean-3 SD", round(lower_sd,4)),
                ("Mean+3 SD", round(upper_sd,4)),
                ("SD-based", ", ".join(map(str,data[(data<lower_sd)|(data>upper_sd)].tolist())) or "None")
            ])
        ]
        for title, items in sections:
            sec = ctk.CTkFrame(self.desc_container, fg_color="#f7f7f7", corner_radius=8)
            sec.pack(fill="x", pady=8, padx=5)
            ctk.CTkLabel(sec, text=title, font=("Arial", 18, "bold"), anchor="w").pack(fill="x", padx=10, pady=(8,4))
            inner = ctk.CTkFrame(sec)
            inner.pack(fill="x", padx=10, pady=(0,8))
            for idx, (lbl, val) in enumerate(items):
                row = idx//2
                col = idx%2
                cell = ctk.CTkFrame(inner, fg_color="#ffffff", corner_radius=6)
                cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                ctk.CTkLabel(cell, text=lbl, font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w", pady=(4,0), padx=6)
                ctk.CTkLabel(cell, text=str(val), font=("Arial", 15), text_color="#000").pack(anchor="w", pady=(0,4), padx=6)
                inner.grid_columnconfigure(col, weight=1)

    def _setup_visualization(self):
        tab = self.tabview.tab("Visualization")
        if self.df.empty:
            ctk.CTkLabel(tab, text="No data.", font=("Arial",16), text_color="black").pack(pady=20)
            return
        chart_types = ["Scatter", "Histogram", "Line", "Boxplot"]
        self.viz_type = ctk.StringVar(value=chart_types[0])
        ctk.CTkOptionMenu(
            tab,
            values=chart_types,
            variable=self.viz_type,
            command=self._draw_viz
        ).pack(pady=10)

        self.viz_ctrl = ctk.CTkFrame(tab)
        self.viz_ctrl.pack(fill="x", padx=20)
        self.viz_area = ctk.CTkFrame(tab)
        self.viz_area.pack(fill="both", expand=True, padx=20, pady=10)
        self._draw_viz(self.viz_type.get())

    def _draw_viz(self, kind):
        for w in self.viz_ctrl.winfo_children():
            w.destroy()
        for w in self.viz_area.winfo_children():
            w.destroy()
        numeric_cols = [c for c in self.df.columns if pd.api.types.is_numeric_dtype(self.df[c])]
        row = 0
        if kind == "Scatter":
            x_var = ctk.StringVar(value=numeric_cols[0])
            y_var = ctk.StringVar(value=numeric_cols[1] if len(numeric_cols)>1 else numeric_cols[0])
            ctk.CTkLabel(self.viz_ctrl, text="X:", text_color="black").grid(row=row, column=0)
            ctk.CTkOptionMenu(self.viz_ctrl, values=numeric_cols, variable=x_var).grid(row=row, column=1)
            ctk.CTkLabel(self.viz_ctrl, text="Y:", text_color="black").grid(row=row, column=2)
            ctk.CTkOptionMenu(self.viz_ctrl, values=numeric_cols, variable=y_var).grid(row=row, column=3)
            ctk.CTkButton(
                self.viz_ctrl,
                text="Plot",
                command=lambda: self._plot_scatter(x_var.get(), y_var.get())
            ).grid(row=row, column=4, padx=10)
        elif kind == "Histogram":
            var = ctk.StringVar(value=numeric_cols[0])
            ctk.CTkOptionMenu(self.viz_ctrl, values=numeric_cols, variable=var).grid(row=row, column=0)
            ctk.CTkButton(
                self.viz_ctrl,
                text="Plot",
                command=lambda: self._plot_hist(var.get())
            ).grid(row=row, column=1, padx=10)
        elif kind == "Line":
            var = ctk.StringVar(value=numeric_cols[0])
            ctk.CTkOptionMenu(self.viz_ctrl, values=numeric_cols, variable=var).grid(row=row, column=0)
            ctk.CTkButton(
                self.viz_ctrl,
                text="Plot",
                command=lambda: self._plot_line(var.get())
            ).grid(row=row, column=1, padx=10)
        elif kind == "Boxplot":
            var = ctk.StringVar(value=numeric_cols[0])
            ctk.CTkOptionMenu(self.viz_ctrl, values=numeric_cols, variable=var).grid(row=row, column=0)
            ctk.CTkButton(
                self.viz_ctrl,
                text="Plot",
                command=lambda: self._plot_box(var.get())
            ).grid(row=row, column=1, padx=10)

    def _plot_scatter(self, x, y):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.scatter(self.df[x], self.df[y], alpha=0.7)
        ax.set_title(f"{y} vs {x}")
        ax.grid(True)
        self._embed(fig, self.viz_area)

    def _plot_hist(self, col):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.hist(self.df[col].dropna(), bins=20, alpha=0.7)
        ax.set_title(col)
        ax.grid(True)
        self._embed(fig, self.viz_area)

    def _plot_line(self, col):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(self.df[col].index, self.df[col], marker='o')
        ax.set_title(col)
        ax.grid(True)
        self._embed(fig, self.viz_area)

    def _plot_box(self, col):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.boxplot(self.df[col].dropna())
        ax.set_title(col)
        ax.grid(True)
        self._embed(fig, self.viz_area)

    def _setup_comparison(self):
        tab = self.tabview.tab("Comparison")
        if self.df.empty:
            ctk.CTkLabel(tab, text="No data.", font=("Arial",16), text_color="black").pack(pady=20)
            return
        numeric_cols = [c for c in self.df.columns if pd.api.types.is_numeric_dtype(self.df[c])]
        v1 = ctk.StringVar(value=numeric_cols[0])
        v2 = ctk.StringVar(value=numeric_cols[1] if len(numeric_cols)>1 else numeric_cols[0])
        frame = ctk.CTkFrame(tab)
        frame.pack(pady=10)
        ctk.CTkLabel(frame, text="Var1:", text_color="black").grid(row=0, column=0)
        ctk.CTkOptionMenu(frame, values=numeric_cols, variable=v1).grid(row=0, column=1)
        ctk.CTkLabel(frame, text="Var2:", text_color="black").grid(row=0, column=2)
        ctk.CTkOptionMenu(frame, values=numeric_cols, variable=v2).grid(row=0, column=3)
        ctk.CTkButton(
            frame,
            text="Plot",
            command=lambda: self._plot_cmp(v1.get(), v2.get())
        ).grid(row=0, column=4, padx=10)
        self.cmp_frame = ctk.CTkFrame(tab)
        self.cmp_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def _plot_cmp(self, a, b):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(self.df[a], marker='o', label=a)
        ax.plot(self.df[b], marker='s', label=b)
        ax.legend()
        ax.set_title("Comparison")
        ax.grid(True)
        self._embed(fig, self.cmp_frame)

    def _setup_raw_data(self):
        tab = self.tabview.tab("Raw Data")
        if self.df.empty:
            ctk.CTkLabel(tab, text="No data.", font=("Arial",16), text_color="black").pack(pady=20)
            return
        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=list(self.df.columns), show='headings')
        vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill='both', expand=True)
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        for _, row in self.df.iterrows():
            tree.insert('', 'end', values=list(row))

    def _embed(self, fig, container):
        for w in container.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == '__main__':
    app = StatsDashboard()
    app.mainloop()
