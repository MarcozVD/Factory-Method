import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .documento import Documento

# ── Palette ──────────────────────────────────────────────────────────────────
DARK    = colors.HexColor("#0D0F14")
ACCENT  = colors.HexColor("#4F8EF7")
ACCENT2 = colors.HexColor("#6C63FF")
LIGHT   = colors.HexColor("#F4F6FB")
SUBTEXT = colors.HexColor("#6B7280")
SUCCESS = colors.HexColor("#2DD4A7")
WHITE   = colors.white

W, H = A4


class FacturaPDF(Documento):

    def generar(self, datos: dict) -> str:
        archivo = "factura.pdf"
        c = canvas.Canvas(archivo, pagesize=A4)
        self._draw(c, datos)
        c.save()
        return archivo

    # ─────────────────────────────────────────────────────────────────────────

    def _draw(self, c: canvas.Canvas, datos: dict) -> None:
        folio     = f"INV-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
        fecha_str = datetime.now().strftime("%d / %m / %Y")
        hora_str  = datetime.now().strftime("%H:%M")

        try:
            monto_val = float(datos["monto"])
        except (ValueError, KeyError):
            monto_val = 0.0

        self._header(c, folio, fecha_str, hora_str)
        self._bill_to(c, datos)
        self._items_table(c, datos, monto_val)
        self._totals(c, monto_val)
        self._paid_stamp(c)
        self._footer(c, folio)

    # ── Header band ──────────────────────────────────────────────────────────

    def _header(self, c, folio, fecha_str, hora_str):
        # Dark background
        c.setFillColor(DARK)
        c.rect(0, H - 72*mm, W, 72*mm, fill=1, stroke=0)

        # Blue left stripe
        c.setFillColor(ACCENT)
        c.rect(0, H - 72*mm, 6*mm, 72*mm, fill=1, stroke=0)

        # Company name
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(16*mm, H - 24*mm, "SistemaPagos")

        c.setFillColor(ACCENT)
        c.setFont("Helvetica", 10)
        c.drawString(16*mm, H - 32*mm, "Plataforma de Pagos Digitales")

        # "FACTURA" badge
        c.setFillColor(ACCENT2)
        c.roundRect(W - 54*mm, H - 42*mm, 44*mm, 22*mm, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(W - 32*mm, H - 28*mm, "FACTURA")

        # Meta info
        c.setFillColor(SUBTEXT)
        c.setFont("Helvetica", 9)
        c.drawRightString(W - 10*mm, H - 50*mm, f"N°  {folio}")
        c.drawRightString(W - 10*mm, H - 58*mm, f"Fecha:  {fecha_str}")
        c.drawRightString(W - 10*mm, H - 65*mm, f"Hora:   {hora_str}")

    # ── Bill-to / method boxes ────────────────────────────────────────────────

    def _bill_to(self, c, datos):
        y = H - 85*mm

        # Client card
        c.setFillColor(LIGHT)
        c.roundRect(10*mm, y - 22*mm, 88*mm, 30*mm, 3*mm, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(15*mm, y + 3*mm, "FACTURAR A")
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(15*mm, y - 6*mm, datos.get("cliente", "—"))
        c.setFillColor(SUBTEXT)
        c.setFont("Helvetica", 9)
        c.drawString(15*mm, y - 14*mm, "Cliente registrado")

        # Payment method card
        c.setFillColor(LIGHT)
        c.roundRect(W - 70*mm, y - 22*mm, 60*mm, 30*mm, 3*mm, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(W - 65*mm, y + 3*mm, "MÉTODO DE PAGO")
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W - 65*mm, y - 6*mm, datos.get("metodo", "—"))
        c.setFillColor(SUBTEXT)
        c.setFont("Helvetica", 9)
        c.drawString(W - 65*mm, y - 14*mm, "Pago procesado")

        # Divider
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.setLineWidth(0.5)
        c.line(10*mm, y - 30*mm, W - 10*mm, y - 30*mm)

    # ── Items table ───────────────────────────────────────────────────────────

    def _items_table(self, c, datos, monto_val):
        y = H - 85*mm - 38*mm          # below divider

        # Header row
        c.setFillColor(DARK)
        c.rect(10*mm, y - 7*mm, W - 20*mm, 10*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        cols = [14*mm, 90*mm, 130*mm, 165*mm]
        for label, x in zip(["DESCRIPCIÓN", "CANT.", "PRECIO UNIT.", "TOTAL"], cols):
            c.drawString(x, y - 3*mm, label)

        # Item row
        yr = y - 20*mm
        c.setFillColor(LIGHT)
        c.rect(10*mm, yr - 5*mm, W - 20*mm, 14*mm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont("Helvetica", 10)
        row = [
            f"Pago vía {datos.get('metodo', '—')}",
            "1",
            f"${monto_val:,.2f}",
            f"${monto_val:,.2f}",
        ]
        for text, x in zip(row, cols):
            c.drawString(x, yr + 2*mm, text)

    # ── Totals ────────────────────────────────────────────────────────────────

    def _totals(self, c, monto_val):
        y = H - 85*mm - 38*mm - 44*mm
        box_x = W - 76*mm

        lines = [
            ("Subtotal", f"${monto_val:,.2f}", False),
            ("IVA (0%)", "$0.00",              False),
            ("TOTAL",    f"${monto_val:,.2f}", True),
        ]
        for i, (label, value, bold) in enumerate(lines):
            ry = y - i * 10*mm
            if bold:
                c.setFillColor(ACCENT)
                c.roundRect(box_x - 4*mm, ry - 5*mm, 72*mm, 12*mm, 3*mm,
                            fill=1, stroke=0)
                c.setFillColor(WHITE)
            else:
                c.setFillColor(SUBTEXT)

            c.setFont("Helvetica-Bold" if bold else "Helvetica",
                      11 if bold else 9)
            c.drawString(box_x, ry + 2*mm, label)
            c.drawRightString(W - 14*mm, ry + 2*mm, value)

    # ── "PAGADO" stamp ────────────────────────────────────────────────────────

    def _paid_stamp(self, c):
        y = H - 85*mm - 38*mm - 44*mm - 10*mm
        c.setFillColor(SUCCESS)
        c.setStrokeColor(SUCCESS)
        c.roundRect(10*mm, y - 8*mm, 42*mm, 14*mm, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(31*mm, y - 1*mm, "PAGADO")

    # ── Footer band ───────────────────────────────────────────────────────────

    def _footer(self, c, folio):
        c.setFillColor(DARK)
        c.rect(0, 0, W, 18*mm, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, 0, 6*mm, 18*mm, fill=1, stroke=0)
        c.setFillColor(SUBTEXT)
        c.setFont("Helvetica", 8)
        c.drawCentredString(
            W / 2, 7*mm,
            "SistemaPagos  •  pagos@sistema.com  •  +1 (800) 000-0000"
        )
        c.drawCentredString(
            W / 2, 3*mm,
            f"Folio: {folio}  |  Generado el "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )