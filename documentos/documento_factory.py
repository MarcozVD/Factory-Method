from .factura_pdf import FacturaPDF

class DocumentoFactory:

    @staticmethod
    def crear_documento(tipo):

        if tipo == "PDF":
            return FacturaPDF()

        else:
            raise ValueError("Tipo de documento no soportado")