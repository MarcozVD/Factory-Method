from .metodo_pago import MetodoPago

class PagoTarjeta(MetodoPago):

    def pagar(self, monto):
        return f"Pago de ${monto} realizado con TARJETA"