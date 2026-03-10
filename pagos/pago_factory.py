from .pago_tarjeta import PagoTarjeta
from .pago_paypal import PagoPaypal

class PagoFactory:

    @staticmethod
    def crear_pago(tipo):

        if tipo == "Tarjeta":
            return PagoTarjeta()

        elif tipo == "PayPal":
            return PagoPaypal()

        else:
            raise ValueError("Método de pago no válido")