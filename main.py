import tkinter as tk
from tkinter import ttk, messagebox

from documents import DOCUMENTS
from tfidf import search_documents


class TFIDFSearchApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "TF-IDF Document Search Engine"
        )

        self.geometry(
            "1100x700"
        )

        self.minsize(
            900,
            600
        )

        self.configure(
            bg="#eef2f7"
        )

        self.create_style()
        self.create_header()
        self.create_search_area()
        self.create_result_area()

    # =====================================================
    # STYLE
    # =====================================================

    def create_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = tk.Frame(
            self,
            bg="#1e3a8a",
            height=95
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="TF-IDF DOCUMENT SEARCH ENGINE",
            bg="#1e3a8a",
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(18, 2)
        )

        tk.Label(
            header,
            text=(
                "Information Retrieval using "
                "TF-IDF and Cosine Similarity"
            ),
            bg="#1e3a8a",
            fg="#dbeafe",
            font=("Segoe UI", 10)
        ).pack()

    # =====================================================
    # SEARCH AREA
    # =====================================================

    def create_search_area(self):

        container = tk.Frame(
            self,
            bg="#eef2f7"
        )

        container.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Label(
            container,
            text="Enter Search Query",
            bg="#eef2f7",
            fg="#1f2937",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w"
        )

        search_frame = tk.Frame(
            container,
            bg="#eef2f7"
        )

        search_frame.pack(
            fill="x",
            pady=8
        )

        self.query_entry = ttk.Entry(
            search_frame,
            font=("Segoe UI", 12)
        )

        self.query_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.query_entry.insert(
            0,
            "machine learning"
        )

        search_button = tk.Button(
            search_frame,
            text="SEARCH",
            command=self.perform_search,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=10,
            relief="flat",
            cursor="hand2"
        )

        search_button.pack(
            side="left",
            padx=8
        )

        clear_button = tk.Button(
            search_frame,
            text="CLEAR",
            command=self.clear_results,
            bg="#d1d5db",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )

        clear_button.pack(
            side="left"
        )

        self.status_label = tk.Label(
            container,
            text="Ready to search",
            bg="#eef2f7",
            fg="#64748b",
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            anchor="w"
        )

    # =====================================================
    # RESULT AREA
    # =====================================================

    def create_result_area(self):

        main_frame = tk.Frame(
            self,
            bg="#eef2f7"
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # ---------------- TABLE ----------------

        table_card = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            table_card,
            text="Ranked Search Results",
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 6)
        )

        table_frame = tk.Frame(
            table_card,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15
        )

        columns = (
            "rank",
            "document",
            "score",
            "relevance"
        )

        self.result_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.result_table.heading(
            "rank",
            text="Rank"
        )

        self.result_table.heading(
            "document",
            text="Document"
        )

        self.result_table.heading(
            "score",
            text="Cosine Similarity"
        )

        self.result_table.heading(
            "relevance",
            text="Relevance"
        )

        self.result_table.column(
            "rank",
            width=80,
            anchor="center"
        )

        self.result_table.column(
            "document",
            width=450
        )

        self.result_table.column(
            "score",
            width=160,
            anchor="center"
        )

        self.result_table.column(
            "relevance",
            width=180,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.result_table.yview
        )

        self.result_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.result_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_table.bind(
            "<<TreeviewSelect>>",
            self.show_document
        )

        # ---------------- PREVIEW ----------------

        tk.Label(
            table_card,
            text="Selected Document",
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.preview = tk.Text(
            table_card,
            height=6,
            wrap="word",
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#111827",
            relief="solid",
            bd=1,
            padx=10,
            pady=8
        )

        self.preview.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def perform_search(self):

        query = self.query_entry.get().strip()

        if not query:

            messagebox.showwarning(
                "Query Required",
                "Please enter a search query."
            )

            return

        results, tfidf_data = search_documents(
            DOCUMENTS,
            query
        )

        # Clear old rows

        for item in self.result_table.get_children():

            self.result_table.delete(
                item
            )

        # Insert ranked results

        for rank, (document, score) in enumerate(
            results,
            start=1
        ):

            if score >= 0.50:

                relevance = "Highly Relevant"

            elif score >= 0.20:

                relevance = "Relevant"

            else:

                relevance = "Low Relevance"

            self.result_table.insert(
                "",
                "end",
                values=(
                    rank,
                    document,
                    f"{score:.4f}",
                    relevance
                )
            )

        self.status_label.config(
            text=(
                f"Search completed: "
                f"{len(results)} documents ranked"
            ),
            fg="#15803d"
        )

        self.clear_preview()

    # =====================================================
    # SHOW DOCUMENT
    # =====================================================

    def show_document(self, event=None):

        selected = (
            self.result_table.selection()
        )

        if not selected:
            return

        item = selected[0]

        values = (
            self.result_table.item(
                item,
                "values"
            )
        )

        if not values:
            return

        document_name = values[1]

        self.clear_preview()

        self.preview.insert(
            "end",
            DOCUMENTS[document_name]
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_results(self):

        self.query_entry.delete(
            0,
            "end"
        )

        for item in self.result_table.get_children():

            self.result_table.delete(
                item
            )

        self.clear_preview()

        self.status_label.config(
            text="Ready to search",
            fg="#64748b"
        )

    def clear_preview(self):

        self.preview.delete(
            "1.0",
            "end"
        )


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    app = TFIDFSearchApp()

    app.mainloop()