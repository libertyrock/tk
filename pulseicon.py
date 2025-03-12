import tkinter as tk
import subprocess
from tkinter import messagebox
from pulsectl import Pulse
import time

def quit():
    window.quit()


def obtener_sink_defecto():
    # Ejecuta el comando pulseaudio para obtener el dispositivo por defecto
    return pulse.server_info().default_sink_name


# Función que refresca los botones en la interfaz
def actualizar_botones():
    # Obtiene los dispositivos de PulseAudio
    sinks = pulse.sink_list()

    # Elimina los botones anteriores
    for button in frame.winfo_children():
        button.destroy()

    label = tk.Label(
        frame,
        text="Sinks",
        font=("Arial", 8),
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    label.pack(fill="x")

    # Crea un botón por cada dispositivo
    for sink in sinks:
        if obtener_sink_defecto() == sink.name:
            button = tk.Button(
                frame,
                text=sink.description,
                font=("Arial", 8),
                command=lambda s=sink: seleccionar_sink(s),
                bg="Black",
                fg="White",
                bd=0,
                activebackground="black",
                activeforeground=window.cget("bg"),
                highlightthickness=0,
            )
            slider_bg = "Black"
            slider_fg = "White"
        else:
            button = tk.Button(
                frame,
                text=sink.description,
                font=("Arial", 8),
                command=lambda s=sink: seleccionar_sink(s),
                bg="White",
                fg="Gray",
                bd=0,
                highlightthickness=0,
            )
            slider_bg = "White"
            slider_fg = "Gray"

        button.pack(fill="x")

        slider = tk.Scale(
            frame,
            font=("Arial", 8),
            from_=0.00,
            to=1.53,
            resolution=0.01,
            orient="horizontal",
            command=lambda value, s=sink: pulse.volume_set_all_chans(s, float(value)),
            bg=slider_bg,
            fg=slider_fg,
            bd=0,
            highlightthickness=0,
        )
        slider.pack(fill="x")
        slider.set(pulse.volume_get_all_chans(sink))

        if obtener_sink_defecto() == sink.name:
            button = tk.Button(
                frame,
                text="mute " + mute_active(sink.mute),
                font=("Arial", 8),
                command=lambda s=sink: mute(s),
                bg=slider_bg,
                fg=slider_fg,
                bd=0,
                activebackground="black",
                activeforeground=window.cget("bg"),
                highlightthickness=0,
            )
        else:
            button = tk.Button(
                frame,
                text="mute " + mute_active(sink.mute),
                font=("Arial", 8),
                command=lambda s=sink: mute(s),
                bg="White",
                fg="Gray",
                bd=0,
                highlightthickness=0,
            )

        button.pack(fill="x")

        separator = tk.Label(
            frame, font=("Arial", 8), bg="#7B1957", bd=0, highlightthickness=0
        )
        separator.pack(fill="x")

    label = tk.Label(
        frame,
        font=("Arial", 8),
        bg="#7B1957",
        fg="white",
        bd=0,
        highlightthickness=0,
        text=info.server_name + "\nVersion: " + info.server_version,
    )
    label.pack(fill="x")

    # Botones Quit y Refresh
    button = tk.Button(
        frame,
        text="Quit",
        font=("Arial", 8),
        command=quit,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="left", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="Cards",
        font=("Arial", 8),
        command=cards_botones,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="(Refresh)",
        font=("Arial", 8),
        command=actualizar_botones,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")


def mute_active(mutenum):
    if mutenum:
        return "on"
    else:
        return "off"


# Función que refresca los botones en la interfaz
def cards_botones():
    # Obtiene los dispositivos de PulseAudio
    cards = pulse.card_list()
    print(cards)

    # Elimina los botones anteriores
    for button in frame.winfo_children():
        button.destroy()

    label = tk.Label(
        frame,
        text="Cards",
        font=("Arial", 8),
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    label.pack(fill="x")

    # Crea un botón por cada dispositivo
    fila = 0
    for card in cards:
        button = tk.Button(
            frame,
            text=card.proplist.get("device.description")
            + "  ( "
            + card.profile_active.description
            + " )",
            font=("Arial", 8),
            command=lambda c=card: seleccionar_card(c),
            bg="White",
            fg="Black",
            bd=0,
            highlightthickness=0,
        )
        button.pack(fill="both")
        fila += 1

    # Botones Quit y Refresh
    button = tk.Button(
        frame,
        text="Quit",
        font=("Arial", 8),
        command=quit,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="left", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="<<<",
        font=("Arial", 8),
        command=actualizar_botones,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="(Refresh)",
        font=("Arial", 8),
        command=cards_botones,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")


# Función que refresca los botones en la interfaz
def profiles_botones(card):
    profiles = card.profile_list
    # print(profiles)

    # Elimina los botones anteriores
    for button in frame.winfo_children():
        button.destroy()

    label = tk.Label(
        frame,
        text="Profiles",
        font=("Arial", 8),
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    label.pack(fill="x")

    # Crea un botón por cada dispositivo
    for profile in profiles:
        button = tk.Button(
            frame,
            text=profile.description,
            font=("Arial", 8),
            command=lambda p=profile: seleccionar_profile(p, card),
            bg="White",
            fg="Black",
            bd=0,
            highlightthickness=0,
        )
        button.pack(fill="x")

    # Botones Quit y Refresh
    button = tk.Button(
        frame,
        text="Quit",
        font=("Arial", 8),
        command=quit,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="left", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="<<<",
        font=("Arial", 8),
        command=cards_botones,
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")

    button = tk.Button(
        frame,
        text="(Refresh)",
        font=("Arial", 8),
        command=lambda c=card: profiles_botones(c),
        bg="#92366F",
        fg="white",
        bd=0,
        highlightthickness=0,
    )
    button.pack(side="right", fill="x", expand="yes")


def mute(s):
    pulse.mute(s, not s.mute)
    actualizar_botones()


# Función para manejar la selección de un dispositivo
def seleccionar_sink(sink):
    print(sink)
    pulse.sink_default_set(sink)
    subprocess.run("bash -c '. /usr/local/lm/_lm_source && _lm_volumeicon'", shell=True)
    time.sleep(0.2)
    actualizar_botones()


# Función para manejar la selección de un dispositivo
def seleccionar_card(card):
    print(card)
    profiles_botones(card)


# Función para manejar la selección de un dispositivo
def seleccionar_profile(profile, card):
    print(profile)
    pulse.card_profile_set(card, profile)
    cards_botones()


########################################################################################
# Comienza el programa

try:
    # Intenta conectarse al servidor PulseAudio
    pulse = Pulse("mi-pulseaudio-cliente")
    info = (
        pulse.server_info()
    )  # Si esta llamada no lanza una excepción, PulseAudio está funcionando
    print("PulseAudio is working")
    time.sleep(1)
except Exception as e:
    messagebox.showerror("Error", "Pulseaudio is not working")
    quit()


# Configuración de la ventana principal
window = tk.Tk()
window.title("linuxmin pulsectl")
window.attributes("-topmost", True)

window.resizable(False, False)  # No permitir redimensionar la ventana

# Marco para los botones
frame = tk.Frame(window, padx=10, pady=10, bg="#7B1957")
frame.pack(fill="both", expand=True)

print(info)

actualizar_botones()

# Ejecuta el bucle de eventos
window.mainloop()
