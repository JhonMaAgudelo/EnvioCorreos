import smtplib
import ssl
import tkinter as tk
from tkinter import messagebox, scrolledtext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading


def enviar_correos():
    correo_origen = entry_origen.get().strip()
    contrasena = entry_password.get().strip()
    correo_destino = entry_destino.get().strip()
    cantidad_str = entry_cantidad.get().strip()
    mensaje_html = text_mensaje.get("1.0", tk.END).strip()

    # Validaciones basicas
    if not correo_origen or not contrasena or not correo_destino or not cantidad_str or not mensaje_html:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        return

    try:
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El numero de correos debe ser un entero positivo.")
        return

    btn_enviar.config(state=tk.DISABLED)
    progress_label.config(text="Enviando...")
    root.update()

    def loop_envio():
        contexto_ssl = ssl.create_default_context()
        errores = 0
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl) as servidor:
                servidor.login(correo_origen, contrasena)
                for i in range(1, cantidad + 1):
                    try:
                        msg = MIMEMultipart("alternative")
                        # Codificar Subject manualmente para soportar caracteres no-ASCII
                        from email.header import Header
                        msg["Subject"] = Header(f"Correo automatico #{i}", "utf-8").encode()
                        msg["From"] = correo_origen
                        msg["To"] = correo_destino

                        # MIMEText con charset utf-8 explicito
                        parte_html = MIMEText(mensaje_html, "html", "utf-8")
                        msg.attach(parte_html)

                        # Usar sendmail con msg.as_bytes() en lugar de as_string()
                        servidor.sendmail(
                            correo_origen,
                            correo_destino,
                            msg.as_bytes()
                        )
                        root.after(0, lambda n=i: progress_label.config(
                            text=f"Enviado {n} de {cantidad}"))
                    except Exception as e:
                        errores += 1
                        root.after(0, lambda err=str(e): progress_label.config(
                            text=f"Error en envio: {err}"))
        except smtplib.SMTPAuthenticationError:
            root.after(0, lambda: messagebox.showerror(
                "Autenticacion fallida",
                "Credenciales incorrectas. Usa una App Password de Google."))
        except Exception as e:
            root.after(0, lambda err=str(e): messagebox.showerror("Error SMTP", err))
        finally:
            if errores == 0:
                root.after(0, lambda: messagebox.showinfo(
                    "Completado", f"Se enviaron {cantidad} correos correctamente."))
            else:
                root.after(0, lambda: messagebox.showwarning(
                    "Completado con errores",
                    f"Se enviaron {cantidad - errores} de {cantidad} correos.\n{errores} fallaron."))
            root.after(0, lambda: btn_enviar.config(state=tk.NORMAL))
            root.after(0, lambda: progress_label.config(text=""))

    hilo = threading.Thread(target=loop_envio, daemon=True)
    hilo.start()


# -----------------------------------------
# Interfaz Tkinter
# -----------------------------------------
root = tk.Tk()
root.title("EnvioCorreos - SMTP Gmail")
root.resizable(False, False)
root.configure(padx=20, pady=20)

fuente = ("Segoe UI", 10)

tk.Label(root, text="Correo origen (Gmail):", font=fuente).grid(row=0, column=0, sticky="w", pady=4)
entry_origen = tk.Entry(root, width=40, font=fuente)
entry_origen.grid(row=0, column=1, pady=4)

tk.Label(root, text="App Password:", font=fuente).grid(row=1, column=0, sticky="w", pady=4)
entry_password = tk.Entry(root, width=40, show="*", font=fuente)
entry_password.grid(row=1, column=1, pady=4)

tk.Label(root, text="Correo destino:", font=fuente).grid(row=2, column=0, sticky="w", pady=4)
entry_destino = tk.Entry(root, width=40, font=fuente)
entry_destino.grid(row=2, column=1, pady=4)

tk.Label(root, text="Numero de correos:", font=fuente).grid(row=3, column=0, sticky="w", pady=4)
entry_cantidad = tk.Entry(root, width=10, font=fuente)
entry_cantidad.grid(row=3, column=1, sticky="w", pady=4)

tk.Label(root, text="Mensaje (HTML):", font=fuente).grid(row=4, column=0, sticky="nw", pady=4)
text_mensaje = scrolledtext.ScrolledText(root, width=38, height=10, font=fuente, wrap=tk.WORD)
text_mensaje.grid(row=4, column=1, pady=4)
text_mensaje.insert(tk.END, "<h1>Hola!</h1><p>Este es un correo de prueba.</p>")

btn_enviar = tk.Button(
    root, text="Enviar", font=("Segoe UI", 11, "bold"),
    bg="#4CAF50", fg="white", padx=10, pady=6,
    command=enviar_correos
)
btn_enviar.grid(row=5, column=0, columnspan=2, pady=12)

progress_label = tk.Label(root, text="", font=fuente, fg="#1565C0")
progress_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
