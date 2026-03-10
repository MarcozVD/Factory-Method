# Sistema de Pagos - Pattern Factory Method 💳

Este proyecto es una implementación práctica del patrón de diseño **Factory Method** en Python, aplicado a un sistema de gestión de pagos y generación de facturas. Cuenta con una interfaz gráfica moderna construida con `customtkinter`.

## 🚀 Características Principales

-   **Interfaz Gráfica Premium**: Diseño oscuro y elegante con animaciones sutiles y chips de usuarios recurrentes.
-   **Múltiples Métodos de Pago**: Soporte para pagos con **Tarjeta** y **PayPal**, extendibles fácilmente gracias al patrón Factory.
-   **Generación de Facturas**: Creación automática de facturas en formato **PDF** tras cada pago exitoso.
-   **Persistencia Local**: Almacenamiento de usuarios recurrentes en formato JSON para un acceso rápido.

## 🏗️ Arquitectura: Patrón Factory Method

El proyecto utiliza el patrón **Factory Method** en dos áreas críticas:

1.  **Pagos (`pagos/`)**: Una fábrica central (`PagoFactory`) decide qué clase de pago instanciar (`PagoTarjeta` o `PagoPaypal`) basándose en la selección del usuario. Esto permite añadir nuevos métodos de pago sin modificar la lógica principal de la aplicación.
2.  **Documentos (`documentos/`)**: Similar a los pagos, `DocumentoFactory` se encarga de instanciar el generador de documentos adecuado (actualmente soporta PDF).

### Estructura del Proyecto

```text
.
├── documentos/             # Lógica de generación de facturas (PDF)
├── interfaz/               # GUI moderna con customtkinter
├── pagos/                  # Implementación del Patrón Factory para pagos
├── usuarios_recurrentes.json # Persistencia de datos
├── main.py                 # Punto de entrada de la aplicación
└── requirements.txt        # Dependencias del proyecto
```

## 🛠️ Tecnologías Utilizadas

-   **Python 3.x**
-   **customtkinter**: Interfaces de usuario modernas y personalizables.
-   **reportlab**: Generación profesional de documentos PDF.
-   **JSON**: Almacenamiento ligero de datos locales.

## 🏁 Instalación y Uso

1.  **Clonar el repositorio** (o descargar los archivos).
2.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecutar la aplicación**:
    ```bash
    python main.py
    ```

---

*Desarrollado como un ejemplo de buenas prácticas en arquitectura de software y diseño de interfaces.*
