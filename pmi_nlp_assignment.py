import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import math
import re


# ============================================================
# PMI NLP ANALYZER
# Topic: Pointwise Mutual Information (PMI) in NLP
#
# Modules:
# 1. Dashboard
# 2. PMI Calculator
# 3. Co-occurrence Explorer
# 4. Learn PMI
#
# Technology:
# Python + Tkinter
#
# No external packages are required.
# ============================================================


# ============================================================
# SAMPLE CORPUS
# ============================================================

SAMPLE_CORPUS = """Machine learning is useful for data analysis.
Machine learning helps computers learn from data.
Natural language processing is useful for language analysis.
Machine learning and natural language processing are important in AI.
Deep learning is a part of machine learning.
AI applications use machine learning for prediction.
"""


# ============================================================
# TEXT PROCESSING
# ============================================================

def tokenize(text):
    """
    Convert the given text into lowercase word tokens.

    Example:
        "Machine Learning is useful"
        ->
        ["machine", "learning", "is", "useful"]
    """

    return re.findall(
        r"\b[a-zA-Z0-9']+\b",
        text.lower()
    )


# ============================================================
# CO-OCCURRENCE CALCULATION
# ============================================================

def calculate_cooccurrence(tokens, word1, word2, window=1):
    """
    Count how many times word1 and word2 occur
    within the selected context window.

    Example with window = 1:

        machine learning useful

        machine <-> learning

    They are considered co-occurring.
    """

    count = 0

    word1 = word1.lower()
    word2 = word2.lower()

    for i, word in enumerate(tokens):

        if word not in (word1, word2):
            continue

        left = max(
            0,
            i - window
        )

        right = min(
            len(tokens),
            i + window + 1
        )

        context = tokens[left:right]

        if word == word1 and word2 in context:

            count += 1

        elif word == word2 and word1 in context:

            count += 1

    return count


# ============================================================
# PMI CALCULATION
# ============================================================

def calculate_pmi(
    text,
    word1,
    word2,
    window=1
):
    """
    Calculate:

        P(x)   = Count(x) / N
        P(y)   = Count(y) / N
        P(x,y) = Co-occurrence / N

        PMI(x,y) =
            log2(P(x,y) / (P(x) * P(y)))

        PPMI =
            max(PMI, 0)
    """

    tokens = tokenize(text)

    if len(tokens) < 2:

        raise ValueError(
            "Please enter a larger corpus."
        )

    word1 = word1.strip().lower()
    word2 = word2.strip().lower()

    if not word1 or not word2:

        raise ValueError(
            "Please enter both words."
        )

    total_tokens = len(tokens)

    count_word1 = tokens.count(
        word1
    )

    count_word2 = tokens.count(
        word2
    )

    cooccurrence_count = calculate_cooccurrence(
        tokens,
        word1,
        word2,
        window
    )

    # Probability of word 1
    p_word1 = (
        count_word1 /
        total_tokens
    )

    # Probability of word 2
    p_word2 = (
        count_word2 /
        total_tokens
    )

    # Joint probability
    p_pair = (
        cooccurrence_count /
        total_tokens
    )

    # PMI
    if (
        p_word1 == 0
        or p_word2 == 0
        or p_pair == 0
    ):

        pmi = None

        ppmi = 0.0

    else:

        pmi = math.log2(
            p_pair /
            (
                p_word1 *
                p_word2
            )
        )

        # Positive PMI
        ppmi = max(
            pmi,
            0
        )

    return {

        "tokens": tokens,

        "total": total_tokens,

        "count1": count_word1,

        "count2": count_word2,

        "pair": cooccurrence_count,

        "p1": p_word1,

        "p2": p_word2,

        "p12": p_pair,

        "pmi": pmi,

        "ppmi": ppmi,

        "window": window
    }


# ============================================================
# FIND NEARBY WORDS
# ============================================================

def find_nearby_words(
    text,
    target,
    window=1
):
    """
    Find words occurring near the target word.
    """

    tokens = tokenize(text)

    target = target.lower()

    counter = Counter()

    for i, word in enumerate(tokens):

        if word != target:
            continue

        left = max(
            0,
            i - window
        )

        right = min(
            len(tokens),
            i + window + 1
        )

        nearby = tokens[
            left:right
        ]

        for other in nearby:

            if other != target:

                counter[other] += 1

    return counter.most_common(15)


# ============================================================
# MAIN APPLICATION
# ============================================================

class PMIApplication(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "PMI NLP Analyzer"
        )

        self.geometry(
            "1250x800"
        )

        self.minsize(
            1050,
            700
        )

        self.configure(
            bg="#eef2f7"
        )

        self.pages = {}

        self.nav_buttons = {}

        self.result = None

        self.create_style()

        self.create_layout()

        self.load_demo()

        self.show_page(
            "Dashboard"
        )

    # ========================================================
    # STYLE
    # ========================================================

    def create_style(self):

        style = ttk.Style(self)

        try:

            style.theme_use(
                "clam"
            )

        except tk.TclError:

            pass

        style.configure(
            "TCombobox",
            padding=7
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "Treeview.Heading",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

    # ========================================================
    # LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        sidebar = tk.Frame(
            self,
            bg="#0f172a",
            width=235
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(
            False
        )

        tk.Label(
            sidebar,
            text="PMI\nNLP ANALYZER",
            bg="#0f172a",
            fg="white",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=(
                25,
                5
            )
        )

        tk.Label(
            sidebar,
            text="UI-Based NLP Assignment",
            bg="#0f172a",
            fg="#94a3b8",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=23,
            pady=(
                0,
                20
            )
        )

        menu = [
            "Dashboard",
            "PMI Calculator",
            "Co-occurrence",
            "Learn PMI"
        ]

        for name in menu:

            button = tk.Button(

                sidebar,

                text="  " + name,

                anchor="w",

                command=lambda n=name:
                    self.show_page(n),

                bg="#0f172a",

                fg="#cbd5e1",

                activebackground="#1e293b",

                activeforeground="white",

                font=(
                    "Segoe UI",
                    10,
                    "bold"
                ),

                relief="flat",

                bd=0,

                padx=13,

                pady=11,

                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.nav_buttons[name] = button

        tk.Frame(
            sidebar,
            bg="#0f172a"
        ).pack(
            fill="both",
            expand=True
        )

        tk.Label(
            sidebar,
            text="Python + Tkinter\nRuns Offline",
            bg="#0f172a",
            fg="#64748b",
            font=(
                "Segoe UI",
                9
            ),
            justify="left"
        ).pack(
            anchor="w",
            padx=23,
            pady=20
        )

        # ----------------------------------------------------
        # MAIN AREA
        # ----------------------------------------------------

        main = tk.Frame(
            self,
            bg="#eef2f7"
        )

        main.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Top Bar
        topbar = tk.Frame(
            main,
            bg="white",
            height=58
        )

        topbar.pack(
            fill="x"
        )

        topbar.pack_propagate(
            False
        )

        tk.Label(
            topbar,
            text="Pointwise Mutual Information",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            side="left",
            padx=22
        )

        self.status = tk.StringVar(
            value="Ready"
        )

        tk.Label(
            topbar,
            textvariable=self.status,
            bg="white",
            fg="#64748b",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="right",
            padx=22
        )

        # Content
        self.content = tk.Frame(
            main,
            bg="#eef2f7"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        # Pages
        self.pages["Dashboard"] = (
            self.create_dashboard()
        )

        self.pages["PMI Calculator"] = (
            self.create_calculator()
        )

        self.pages["Co-occurrence"] = (
            self.create_cooccurrence()
        )

        self.pages["Learn PMI"] = (
            self.create_learn_page()
        )

        # Footer
        tk.Label(
            main,
            text="PMI NLP Analyzer | Educational Project",
            bg="#0f172a",
            fg="#cbd5e1",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            fill="x"
        )

    # ========================================================
    # HELPER FUNCTIONS
    # ========================================================

    def create_card(
        self,
        parent
    ):

        return tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

    def create_text_area(
        self,
        parent,
        height=10
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="both",
            expand=True
        )

        text = tk.Text(

            frame,

            height=height,

            wrap="word",

            font=(
                "Consolas",
                10
            ),

            bg="#f8fafc",

            fg="#0f172a",

            insertbackground="#0f172a",

            relief="solid",

            bd=1,

            padx=10,

            pady=10
        )

        scrollbar = ttk.Scrollbar(

            frame,

            orient="vertical",

            command=text.yview
        )

        text.configure(
            yscrollcommand=
            scrollbar.set
        )

        text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        return text

    def create_button(
        self,
        parent,
        text,
        command,
        primary=False
    ):

        return tk.Button(

            parent,

            text=text,

            command=command,

            bg=(
                "#2563eb"
                if primary
                else "#e2e8f0"
            ),

            fg=(
                "white"
                if primary
                else "#0f172a"
            ),

            activebackground=(
                "#1d4ed8"
                if primary
                else "#cbd5e1"
            ),

            activeforeground="white",

            font=(
                "Segoe UI",
                10,
                "bold"
            ),

            relief="flat",

            bd=0,

            padx=14,

            pady=9,

            cursor="hand2"
        )

    def create_title(
        self,
        page,
        title,
        subtitle
    ):

        tk.Label(
            page,
            text=title,
            bg="#eef2f7",
            fg="#0f172a",
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            page,
            text=subtitle,
            bg="#eef2f7",
            fg="#64748b",
            font=(
                "Segoe UI",
                10
            )
        ).pack(
            anchor="w",
            pady=(
                3,
                12
            )
        )

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def show_page(
        self,
        name
    ):

        for page in self.pages.values():

            page.pack_forget()

        self.pages[name].pack(
            fill="both",
            expand=True
        )

        for page_name, button in (
            self.nav_buttons.items()
        ):

            if page_name == name:

                button.configure(
                    bg="#2563eb",
                    fg="white"
                )

            else:

                button.configure(
                    bg="#0f172a",
                    fg="#cbd5e1"
                )

        self.status.set(
            name + " selected"
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        page = tk.Frame(
            self.content,
            bg="#eef2f7"
        )

        self.create_title(

            page,

            "PMI Analyzer",

            "Understand word association through probability."
        )

        cards = tk.Frame(
            page,
            bg="#eef2f7"
        )

        cards.pack(
            fill="x"
        )

        card_data = [

            (
                "P(x)",
                "Probability of Word 1"
            ),

            (
                "P(y)",
                "Probability of Word 2"
            ),

            (
                "P(x,y)",
                "Co-occurrence Probability"
            ),

            (
                "PMI",
                "Association Strength"
            )

        ]

        for formula, description in (
            card_data
        ):

            card = self.create_card(
                cards
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(0, 10)
            )

            tk.Label(
                card,
                text=formula,
                bg="white",
                fg="#2563eb",
                font=(
                    "Segoe UI",
                    20,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=16,
                pady=(
                    15,
                    2
                )
            )

            tk.Label(
                card,
                text=description,
                bg="white",
                fg="#64748b",
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                anchor="w",
                padx=16,
                pady=(
                    0,
                    15
                )
            )

        lower = tk.Frame(
            page,
            bg="#eef2f7"
        )

        lower.pack(
            fill="both",
            expand=True,
            pady=18
        )

        left = self.create_card(
            lower
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            left,
            text="What is PMI?",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(
                18,
                10
            )
        )

        tk.Label(
            left,
            text=(
                "Pointwise Mutual Information (PMI) "
                "measures how strongly two words are associated.\n\n"
                "PMI compares the probability of seeing two "
                "words together with what would be expected from "
                "their individual probabilities.\n\n"
                "Example:\n"
                "machine ↔ learning\n\n"
                "A positive PMI indicates stronger-than-baseline "
                "association under the chosen corpus and "
                "co-occurrence definition."
            ),
            bg="white",
            fg="#334155",
            font=(
                "Segoe UI",
                10
            ),
            justify="left",
            wraplength=430
        ).pack(
            anchor="w",
            padx=18
        )

        right = self.create_card(
            lower
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        tk.Label(
            right,
            text="PMI Workflow",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(
                18,
                10
            )
        )

        tk.Label(
            right,
            text=(
                "1. Enter corpus\n"
                "        ↓\n"
                "2. Tokenize text\n"
                "        ↓\n"
                "3. Count both words\n"
                "        ↓\n"
                "4. Count co-occurrence\n"
                "        ↓\n"
                "5. Calculate P(x), P(y), P(x,y)\n"
                "        ↓\n"
                "6. Calculate PMI\n"
                "        ↓\n"
                "7. Calculate PPMI"
            ),
            bg="white",
            fg="#334155",
            font=(
                "Consolas",
                10
            ),
            justify="left"
        ).pack(
            anchor="w",
            padx=18
        )

        return page

    # ========================================================
    # PMI CALCULATOR
    # ========================================================

    def create_calculator(self):

        page = tk.Frame(
            self.content,
            bg="#eef2f7"
        )

        self.create_title(

            page,

            "PMI Calculator",

            "Calculate PMI and see every step of the calculation."
        )

        body = tk.Frame(
            page,
            bg="#eef2f7"
        )

        body.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        left = self.create_card(
            body
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            left,
            text="1. Enter Corpus",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(
                16,
                6
            )
        )

        self.corpus_text = (
            self.create_text_area(
                left,
                12
            )
        )

        controls = tk.Frame(
            left,
            bg="white"
        )

        controls.pack(
            fill="x",
            padx=16,
            pady=12
        )

        tk.Label(
            controls,
            text="Word 1:",
            bg="white"
        ).pack(
            side="left"
        )

        self.word1_entry = ttk.Entry(
            controls,
            width=16
        )

        self.word1_entry.pack(
            side="left",
            padx=6
        )

        tk.Label(
            controls,
            text="Word 2:",
            bg="white"
        ).pack(
            side="left",
            padx=(
                10,
                4
            )
        )

        self.word2_entry = ttk.Entry(
            controls,
            width=16
        )

        self.word2_entry.pack(
            side="left",
            padx=6
        )

        tk.Label(
            controls,
            text="Window:",
            bg="white"
        ).pack(
            side="left",
            padx=(
                10,
                4
            )
        )

        self.window_combo = ttk.Combobox(

            controls,

            values=[
                "1",
                "2",
                "3"
            ],

            state="readonly",

            width=5
        )

        self.window_combo.current(
            0
        )

        self.window_combo.pack(
            side="left"
        )

        self.create_button(
            controls,
            "CALCULATE PMI",
            self.calculate,
            True
        ).pack(
            side="left",
            padx=7
        )

        self.create_button(
            controls,
            "DEMO",
            self.load_demo
        ).pack(
            side="left"
        )

        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        right = self.create_card(
            body
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        tk.Label(
            right,
            text="2. PMI Result",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(
                16,
                8
            )
        )

        metric_frame = tk.Frame(
            right,
            bg="white"
        )

        metric_frame.pack(
            fill="x",
            padx=12
        )

        self.metric_labels = {}

        metrics = [

            (
                "p1",
                "P(x)"
            ),

            (
                "p2",
                "P(y)"
            ),

            (
                "p12",
                "P(x,y)"
            ),

            (
                "pmi",
                "PMI"
            ),

            (
                "ppmi",
                "PPMI"
            )

        ]

        for key, title in metrics:

            card = tk.Frame(
                metric_frame,
                bg="#f8fafc",
                bd=1,
                relief="solid"
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=3
            )

            tk.Label(
                card,
                text=title,
                bg="#f8fafc",
                fg="#64748b",
                font=(
                    "Segoe UI",
                    9,
                    "bold"
                )
            ).pack(
                pady=(
                    8,
                    1
                )
            )

            value = tk.Label(
                card,
                text="-",
                bg="#f8fafc",
                fg="#2563eb",
                font=(
                    "Segoe UI",
                    12,
                    "bold"
                )
            )

            value.pack(
                pady=(
                    0,
                    8
                )
            )

            self.metric_labels[
                key
            ] = value

        tk.Label(
            right,
            text="Step-by-Step Calculation",
            bg="white",
            fg="#0f172a",
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(
                15,
                5
            )
        )

        self.steps_text = (
            self.create_text_area(
                right,
                12
            )
        )

        return page

    # ========================================================
    # LOAD DEMO DATA
    # ========================================================

    def load_demo(self):

        # Corpus may not exist yet during initial construction.
        if not hasattr(
            self,
            "corpus_text"
        ):
            return

        self.corpus_text.delete(
            "1.0",
            "end"
        )

        self.corpus_text.insert(
            "1.0",
            SAMPLE_CORPUS
        )

        self.word1_entry.delete(
            0,
            "end"
        )

        self.word1_entry.insert(
            0,
            "machine"
        )

        self.word2_entry.delete(
            0,
            "end"
        )

        self.word2_entry.insert(
            0,
            "learning"
        )

        self.window_combo.set(
            "1"
        )

        self.status.set(
            "Demo data loaded"
        )

    # ========================================================
    # CALCULATE PMI
    # ========================================================

    def calculate(self):

        text = self.corpus_text.get(
            "1.0",
            "end"
        ).strip()

        word1 = self.word1_entry.get().strip().lower()
        word2 = self.word2_entry.get().strip().lower()

        try:

            window = int(
                self.window_combo.get()
            )

            result = calculate_pmi(

                text,

                word1,

                word2,

                window

            )

        except ValueError as error:

            messagebox.showwarning(
                "Input Error",
                str(error)
            )

            return

        self.result = result

        # ----------------------------------------------------
        # UPDATE METRIC CARDS
        # ----------------------------------------------------

        self.metric_labels[
            "p1"
        ].config(
            text=f"{result['p1']:.4f}"
        )

        self.metric_labels[
            "p2"
        ].config(
            text=f"{result['p2']:.4f}"
        )

        self.metric_labels[
            "p12"
        ].config(
            text=f"{result['p12']:.4f}"
        )

        if result["pmi"] is None:

            pmi_text = "Undefined"

        else:

            pmi_text = (
                f"{result['pmi']:.4f}"
            )

        self.metric_labels[
            "pmi"
        ].config(
            text=pmi_text
        )

        self.metric_labels[
            "ppmi"
        ].config(
            text=f"{result['ppmi']:.4f}"
        )

        # ----------------------------------------------------
        # STEP-BY-STEP EXPLANATION
        # ----------------------------------------------------

        self.steps_text.delete(
            "1.0",
            "end"
        )

        N = result["total"]

        self.steps_text.insert(
            "end",

            "STEP 1 — TOTAL TOKENS\n"
            f"Total tokens (N) = {N}\n\n"
        )

        self.steps_text.insert(
            "end",

            "STEP 2 — WORD COUNTS\n"
            f"Count({word1}) = "
            f"{result['count1']}\n"
            f"Count({word2}) = "
            f"{result['count2']}\n"
            f"Co-occurrence count = "
            f"{result['pair']}\n\n"
        )

        self.steps_text.insert(
            "end",

            "STEP 3 — INDIVIDUAL PROBABILITIES\n"
            f"P({word1}) = "
            f"Count({word1}) / N\n"
            f"        = "
            f"{result['count1']} / {N}\n"
            f"        = "
            f"{result['p1']:.6f}\n\n"
        )

        self.steps_text.insert(
            "end",

            f"P({word2}) = "
            f"Count({word2}) / N\n"
            f"        = "
            f"{result['count2']} / {N}\n"
            f"        = "
            f"{result['p2']:.6f}\n\n"
        )

        self.steps_text.insert(
            "end",

            "STEP 4 — JOINT PROBABILITY\n"
            f"P({word1},{word2}) = "
            f"Co-occurrence / N\n"
            f"        = "
            f"{result['pair']} / {N}\n"
            f"        = "
            f"{result['p12']:.6f}\n\n"
        )

        self.steps_text.insert(
            "end",

            "STEP 5 — PMI\n"
        )

        if result["pmi"] is None:

            self.steps_text.insert(
                "end",

                "PMI is undefined because "
                "P(x), P(y), or P(x,y) is zero.\n"
            )

        else:

            self.steps_text.insert(
                "end",

                "PMI(x,y) = "
                "log2(P(x,y) / (P(x) × P(y)))\n\n"
                f"PMI = log2("
                f"{result['p12']:.6f} / "
                f"({result['p1']:.6f} × "
                f"{result['p2']:.6f}))\n\n"
                f"PMI = "
                f"{result['pmi']:.6f}\n\n"
            )

        self.steps_text.insert(
            "end",

            "STEP 6 — PPMI\n"
            "PPMI(x,y) = max(PMI(x,y), 0)\n"
            f"PPMI = "
            f"{result['ppmi']:.6f}\n\n"
        )

        # ----------------------------------------------------
        # INTERPRETATION
        # ----------------------------------------------------

        if result["pmi"] is None:

            interpretation = (
                "Interpretation:\n"
                "The two selected words do not have a "
                "non-zero observed co-occurrence under "
                "the current corpus/window definition."
            )

        elif result["pmi"] > 0:

            interpretation = (
                "Interpretation:\n"
                "The two words occur together more often "
                "than expected under the independence baseline."
            )

        elif result["pmi"] == 0:

            interpretation = (
                "Interpretation:\n"
                "The observed co-occurrence matches the "
                "independence baseline."
            )

        else:

            interpretation = (
                "Interpretation:\n"
                "The two words occur together less often "
                "than expected under the independence baseline."
            )

        self.steps_text.insert(
            "end",
            interpretation
        )

        self.status.set(
            "PMI calculated successfully"
        )

    # ========================================================
    # CO-OCCURRENCE PAGE
    # ========================================================

    def create_cooccurrence(self):

        page = tk.Frame(
            self.content,
            bg="#eef2f7"
        )

        self.create_title(

            page,

            "Co-occurrence Explorer",

            "Explore which words occur close to a selected target word."
        )

        card = self.create_card(
            page
        )

        card.pack(
            fill="both",
            expand=True
        )

        controls = tk.Frame(
            card,
            bg="white"
        )

        controls.pack(
            fill="x",
            padx=16,
            pady=15
        )

        tk.Label(
            controls,
            text="Target Word:",
            bg="white"
        ).pack(
            side="left"
        )

        self.target_entry = ttk.Entry(
            controls,
            width=20
        )

        self.target_entry.pack(
            side="left",
            padx=7
        )

        self.target_entry.insert(
            0,
            "machine"
        )

        tk.Label(
            controls,
            text="Window:",
            bg="white"
        ).pack(
            side="left",
            padx=(
                12,
                4
            )
        )

        self.co_window = ttk.Combobox(

            controls,

            values=[
                "1",
                "2",
                "3"
            ],

            state="readonly",

            width=5
        )

        self.co_window.current(
            0
        )

        self.co_window.pack(
            side="left"
        )

        self.create_button(
            controls,
            "ANALYZE",
            self.run_cooccurrence,
            True
        ).pack(
            side="left",
            padx=10
        )

        columns = (
            "word",
            "count"
        )

        self.co_table = ttk.Treeview(

            card,

            columns=columns,

            show="headings"
        )

        self.co_table.heading(
            "word",
            text="Nearby Word"
        )

        self.co_table.heading(
            "count",
            text="Co-occurrence Count"
        )

        self.co_table.column(
            "word",
            width=350
        )

        self.co_table.column(
            "count",
            width=200,
            anchor="center"
        )

        self.co_table.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(
                0,
                10
            )
        )

        tk.Label(
            card,
            text=(
                "The same context-window concept is used "
                "in the PMI calculation."
            ),
            bg="white",
            fg="#64748b",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(
                0,
                14
            )
        )

        return page

    def run_cooccurrence(self):

        target = (
            self.target_entry
            .get()
            .strip()
            .lower()
        )

        if not target:

            messagebox.showwarning(
                "Input Required",
                "Enter a target word."
            )

            return

        text = self.corpus_text.get(
            "1.0",
            "end"
        ).strip()

        window = int(
            self.co_window.get()
        )

        results = find_nearby_words(
            text,
            target,
            window
        )

        for item in (
            self.co_table
            .get_children()
        ):

            self.co_table.delete(
                item
            )

        for word, count in results:

            self.co_table.insert(
                "",
                "end",
                values=(
                    word,
                    count
                )
            )

        self.status.set(
            "Co-occurrence analysis completed"
        )

    # ========================================================
    # LEARN PMI PAGE
    # ========================================================

    def create_learn_page(self):

        page = tk.Frame(
            self.content,
            bg="#eef2f7"
        )

        self.create_title(

            page,

            "Learn PMI",

            "Use this section to understand the concept before your viva."
        )

        card = self.create_card(
            page
        )

        card.pack(
            fill="both",
            expand=True
        )

        explanation = """

POINTWISE MUTUAL INFORMATION (PMI)
==================================

1. WHAT IS PMI?

PMI measures how strongly two words are associated.

It compares:

    Actual probability of the two words occurring together

with:

    Expected probability based on their individual probabilities.


2. INDIVIDUAL PROBABILITY

For word x:

    P(x) = Count(x) / N

For word y:

    P(y) = Count(y) / N

where N is the total number of tokens.


3. JOINT PROBABILITY

    P(x,y) = Co-occurrence Count / N

Here, co-occurrence is defined using the selected context window.


4. PMI FORMULA

    PMI(x,y)
        =
    log2( P(x,y) / (P(x) × P(y)) )


5. HOW TO UNDERSTAND THE VALUE

PMI > 0
    The words occur together more often than expected
    under the independence baseline.

PMI = 0
    The observed association matches the independence baseline.

PMI < 0
    The words occur together less often than expected.


6. WHAT IS PPMI?

PPMI means Positive Pointwise Mutual Information.

It removes negative values:

    PPMI(x,y) = max(PMI(x,y), 0)


7. EXAMPLE

Suppose:

    machine
    learning

appear near each other many times.

The system compares:

    P(machine, learning)

with:

    P(machine) × P(learning)

If the joint occurrence is much larger than the
independence expectation, PMI becomes positive.


8. WHY IS PMI USED IN NLP?

PMI can be used for:

    • Word association
    • Collocation analysis
    • Finding related words
    • Distributional representations
    • PPMI vector construction


9. IMPORTANT POINT

PMI depends on:

    • The corpus
    • Word frequencies
    • The co-occurrence definition
    • Context-window size

Therefore, the PMI value can change when the data
or context window changes.


10. VIVA ANSWER

"PMI is a statistical measure that tells us how strongly
two words are associated by comparing their observed
co-occurrence probability with the probability expected
if the words were independent."
"""

        text = tk.Text(

            card,

            wrap="word",

            font=(
                "Segoe UI",
                11
            ),

            bg="white",

            fg="#334155",

            relief="flat",

            padx=22,

            pady=20
        )

        text.pack(
            fill="both",
            expand=True
        )

        text.insert(
            "1.0",
            explanation
        )

        text.configure(
            state="disabled"
        )

        return page


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = PMIApplication()

    app.mainloop()