import customtkinter as ctk
import json
import os
from datetime import datetime
from pagos.pago_factory import PagoFactory
from documentos.documento_factory import DocumentoFactory

# ── Persistent storage for recurring users ──────────────────────────────────
USERS_FILE = "usuarios_recurrentes.json"

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_usuario(cliente, monto, metodo):
    usuarios = cargar_usuarios()
    # Update existing or add new
    for u in usuarios:
        if u["cliente"].lower() == cliente.lower():
            u["ultimo_monto"] = monto
            u["ultimo_metodo"] = metodo
            u["ultimo_pago"] = datetime.now().strftime("%d/%m/%Y")
            u["total_pagos"] = u.get("total_pagos", 1) + 1
            break
    else:
        usuarios.append({
            "cliente": cliente,
            "ultimo_monto": monto,
            "ultimo_metodo": metodo,
            "ultimo_pago": datetime.now().strftime("%d/%m/%Y"),
            "total_pagos": 1
        })
    # Keep only last 8 users
    usuarios = usuarios[-8:]
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    return usuarios


# ── Color palette ────────────────────────────────────────────────────────────
BG        = "#0D0F14"
PANEL     = "#13161E"
CARD      = "#1A1E2A"
BORDER    = "#252A38"
ACCENT    = "#4F8EF7"
ACCENT2   = "#6C63FF"
SUCCESS   = "#2DD4A7"
TEXT      = "#E8ECF5"
SUBTEXT   = "#6B7280"
HOVER     = "#1F2435"


class UserChip(ctk.CTkFrame):
    """A compact clickable chip for a recurring user."""

    def __init__(self, master, user_data, on_click, **kwargs):
        super().__init__(
            master,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER,
            **kwargs
        )
        self.user_data = user_data
        self.on_click  = on_click
        self._build()
        self.bind("<Button-1>", self._clicked)
        for w in self.winfo_children():
            w.bind("<Button-1>", self._clicked)

    def _build(self):
        # Avatar circle (initials)
        initials = "".join(p[0].upper() for p in self.user_data["cliente"].split()[:2])
        avatar = ctk.CTkLabel(
            self,
            text=initials,
            width=36, height=36,
            fg_color=ACCENT2,
            corner_radius=18,
            font=ctk.CTkFont("Courier", 13, "bold"),
            text_color="white"
        )
        avatar.grid(row=0, column=0, rowspan=2, padx=(10, 8), pady=8)

        name_lbl = ctk.CTkLabel(
            self,
            text=self.user_data["cliente"],
            font=ctk.CTkFont("Courier", 12, "bold"),
            text_color=TEXT,
            anchor="w"
        )
        name_lbl.grid(row=0, column=1, sticky="w", padx=(0, 10))

        detail = f"${self.user_data['ultimo_monto']}  ·  {self.user_data['ultimo_metodo']}"
        detail_lbl = ctk.CTkLabel(
            self,
            text=detail,
            font=ctk.CTkFont("Courier", 10),
            text_color=SUBTEXT,
            anchor="w"
        )
        detail_lbl.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 4))

        # Badge: total pagos
        badge = ctk.CTkLabel(
            self,
            text=f"×{self.user_data.get('total_pagos', 1)}",
            width=28, height=18,
            fg_color=ACCENT,
            corner_radius=9,
            font=ctk.CTkFont("Courier", 9, "bold"),
            text_color="white"
        )
        badge.grid(row=0, column=2, rowspan=2, padx=(0, 10))

        self.columnconfigure(1, weight=1)

    def _clicked(self, _event=None):
        self.on_click(self.user_data)


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.title("Sistema de Pagos")
        self.geometry("820x600")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self._build_layout()
        self._build_left_panel()
        self._build_right_panel()
        self._refresh_users()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self.columnconfigure(0, weight=0)   # sidebar
        self.columnconfigure(1, weight=1)   # main
        self.rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=PANEL, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew", padx=0)

    # ── Left panel: recurring users ───────────────────────────────────────────

    def _build_left_panel(self):
        # Header
        hdr = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(24, 6))

        ctk.CTkLabel(
            hdr,
            text="💳  SistemaPagos",
            font=ctk.CTkFont("Courier", 15, "bold"),
            text_color=ACCENT
        ).pack(anchor="w")

        ctk.CTkLabel(
            hdr,
            text="Usuarios recurrentes",
            font=ctk.CTkFont("Courier", 11),
            text_color=SUBTEXT
        ).pack(anchor="w", pady=(14, 0))

        # Separator
        sep = ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER)
        sep.pack(fill="x", padx=16, pady=8)

        # Scrollable list
        self.users_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            scrollbar_button_color=BORDER
        )
        self.users_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _refresh_users(self):
        for w in self.users_frame.winfo_children():
            w.destroy()

        usuarios = cargar_usuarios()
        if not usuarios:
            ctk.CTkLabel(
                self.users_frame,
                text="Sin registros aún",
                font=ctk.CTkFont("Courier", 11),
                text_color=SUBTEXT
            ).pack(pady=20)
            return

        for u in reversed(usuarios):
            chip = UserChip(self.users_frame, u, self._fill_from_user)
            chip.pack(fill="x", pady=4)

    def _fill_from_user(self, user_data):
        """Pre-fill form with the selected recurring user."""
        self.entry_cliente.delete(0, "end")
        self.entry_cliente.insert(0, user_data["cliente"])
        self.entry_monto.delete(0, "end")
        self.entry_monto.insert(0, user_data["ultimo_monto"])
        self.metodo.set(user_data["ultimo_metodo"])
        self._flash_form()

    # ── Right panel: payment form ─────────────────────────────────────────────

    def _build_right_panel(self):
        self.main.columnconfigure(0, weight=1)

        # Title row
        title_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        title_frame.pack(fill="x", padx=36, pady=(32, 4))

        ctk.CTkLabel(
            title_frame,
            text="Nuevo pago",
            font=ctk.CTkFont("Courier", 22, "bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text=datetime.now().strftime("%d %b %Y"),
            font=ctk.CTkFont("Courier", 11),
            text_color=SUBTEXT
        ).pack(side="right", pady=(6, 0))

        # Card
        self.card = ctk.CTkFrame(
            self.main,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )
        self.card.pack(fill="both", expand=True, padx=36, pady=12)

        self._build_form()

    def _build_form(self):
        pad = {"padx": 28, "pady": 8}

        # Cliente
        ctk.CTkLabel(
            self.card,
            text="CLIENTE",
            font=ctk.CTkFont("Courier", 10, "bold"),
            text_color=SUBTEXT
        ).pack(anchor="w", padx=28, pady=(24, 2))

        self.entry_cliente = ctk.CTkEntry(
            self.card,
            placeholder_text="Nombre del cliente",
            height=42,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont("Courier", 13),
            text_color=TEXT
        )
        self.entry_cliente.pack(fill="x", **pad)

        # Monto
        ctk.CTkLabel(
            self.card,
            text="MONTO  (USD)",
            font=ctk.CTkFont("Courier", 10, "bold"),
            text_color=SUBTEXT
        ).pack(anchor="w", padx=28, pady=(8, 2))

        self.entry_monto = ctk.CTkEntry(
            self.card,
            placeholder_text="0.00",
            height=42,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont("Courier", 18, "bold"),
            text_color=ACCENT
        )
        self.entry_monto.pack(fill="x", **pad)

        # Método
        ctk.CTkLabel(
            self.card,
            text="MÉTODO DE PAGO",
            font=ctk.CTkFont("Courier", 10, "bold"),
            text_color=SUBTEXT
        ).pack(anchor="w", padx=28, pady=(8, 2))

        self.metodo = ctk.CTkOptionMenu(
            self.card,
            values=["Tarjeta", "PayPal" ],
            height=42,
            fg_color=PANEL,
            button_color=ACCENT2,
            button_hover_color=ACCENT,
            dropdown_fg_color=CARD,
            dropdown_hover_color=HOVER,
            corner_radius=10,
            font=ctk.CTkFont("Courier", 13),
            text_color=TEXT
        )
        self.metodo.pack(fill="x", **pad)

        # Button
        self.boton = ctk.CTkButton(
            self.card,
            text="⟶  Realizar pago",
            height=48,
            fg_color=ACCENT,
            hover_color=ACCENT2,
            corner_radius=12,
            font=ctk.CTkFont("Courier", 14, "bold"),
            text_color="white",
            command=self.procesar_pago
        )
        self.boton.pack(fill="x", padx=28, pady=(16, 10))

        # Result label
        self.resultado = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont("Courier", 12),
            text_color=SUCCESS
        )
        self.resultado.pack(pady=(0, 20))

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _flash_form(self):
        """Brief highlight animation when a user chip is clicked."""
        self.card.configure(border_color=ACCENT)
        self.after(400, lambda: self.card.configure(border_color=BORDER))

    def procesar_pago(self):
        cliente = self.entry_cliente.get().strip()
        monto   = self.entry_monto.get().strip()
        metodo  = self.metodo.get()

        if not cliente or not monto:
            self.resultado.configure(text="⚠  Completa todos los campos.", text_color="#F59E0B")
            return

        # FACTORY 1: crear método de pago
        pago      = PagoFactory.crear_pago(metodo)
        resultado = pago.pagar(monto)

        self.resultado.configure(
            text=f"✓  {resultado}",
            text_color=SUCCESS
        )

        datos = {"cliente": cliente, "monto": monto, "metodo": metodo}

        # FACTORY 2: crear documento
        documento = DocumentoFactory.crear_documento("PDF")
        archivo   = documento.generar(datos)
        print("Factura generada:", archivo)

        # Persist & refresh sidebar
        guardar_usuario(cliente, monto, metodo)
        self._refresh_users()


if __name__ == "__main__":
    App().mainloop()