from .metodo_pago import MetodoPago

class PagoPaypal(MetodoPago):

    def pagar(self, monto):
        return f"Pago de ${monto} realizado con PAYPAL"