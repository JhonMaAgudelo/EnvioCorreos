# EnvioCorreos

Aplicación de escritorio en Python para enviar múltiples correos electrónicos vía **SMTP/Gmail** con interfaz gráfica **Tkinter**.

## 📦 Librerías utilizadas

| Librería | Propósito |
|---|---|
| `smtplib` | Envío de correos vía SMTP |
| `ssl` | Conexión segura (TLS/SSL) |
| `tkinter` | Interfaz gráfica de usuario |
| `email.mime` | Construcción de mensajes HTML |
| `threading` | Envío en hilo separado (no bloquea la UI) |

Todas son parte de la **biblioteca estándar de Python** — no requiere instalación adicional.

## 🚀 Uso

```bash
python envio_correos.py
```

## ⚙️ Configuración

### App Password de Google

> ⚠️ **No uses tu contraseña normal de Gmail.** Debes generar una *App Password*:

1. Ve a [myaccount.google.com/security](https://myaccount.google.com/security)
2. Activa la **Verificación en 2 pasos** si no la tienes.
3. Busca **"Contraseñas de aplicaciones"**.
4. Crea una nueva contraseña para la app (selecciona *Correo* y *Windows/Linux*).
5. Copia la contraseña de 16 caracteres generada.

## 🖥️ Interfaz

- **Correo origen** — tu cuenta Gmail
- **App Password** — contraseña de aplicación de Google
- **Correo destino** — destinatario
- **Número de correos** — cuántas veces se envía el mensaje
- **Mensaje HTML** — cuerpo del correo (acepta etiquetas HTML)
- **Botón Enviar** — inicia el loop de envío

## 🔄 Loop de envío

Al presionar *Enviar*, se ejecuta un bucle que:
1. Construye el mensaje `MIMEMultipart` con el cuerpo HTML.
2. Lo envía al destinatario vía `smtp.gmail.com:465`.
3. Muestra el progreso en pantalla (`Enviado X de N`).
4. Al finalizar, muestra un resumen de éxitos/errores.

El envío se ejecuta en un **hilo separado** para que la interfaz no se congele.

## 📋 Requisitos

- Python 3.6+
- Cuenta Gmail con verificación en 2 pasos habilitada
