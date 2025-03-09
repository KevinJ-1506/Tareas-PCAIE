import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
# Configuración de grabación
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def menu():
    opcion = 0
    while opcion != 5:
        print("Seleccione una Opción")
        print("1. Grabar audio")
        print("2. Reproducir audio")
        print("3. Graficar Espectro")
        print("4. Graficar Espectro de Densidad")
        print("5. Salir")
        try:
            opcion = input("Ingrese opción:")
            opcion = int(opcion)
            if (opcion == 1):
               
                duracion = int(input("Ingrese la duración de la grabación en segundos: "))
                 

                grabar_audio(duracion)
    
            elif (opcion == 2):
                reproducir_audio()
            elif (opcion == 3):
                graficar_audio()
            elif (opcion == 4):
                graficar_densidad()
            elif (opcion == 5):
                print("¡Gracias por visitarnos! Vuelva pronto.")
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.\n")

 
def grabar_audio(duracion, filename="audio.wav"):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Comenzando la Grabación...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * duracion)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Grabación Finalizada.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    print("Archivo de audio grabado correctamente.")


def reproducir_audio(filename="audio.wav"):
    p = pyaudio.PyAudio()
    wf = wave.open(filename, "rb")
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Reproducción finalizada.")


def graficar_audio(filename="audio.wav"):
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
        tiempo = np.linspace(0, len(audio_data) / RATE, num=len(audio_data))
        plt.figure()
        plt.plot(tiempo, audio_data)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title("Audio")
        plt.show()


def graficar_densidad(filename="audio.wav"):
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
        f, Pxx = welch(audio_data, RATE, nperseg=1024)
        plt.figure()
        plt.semilogy(f, Pxx)
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Densidad Espectral de Potencia (dB/Hz)")
        plt.title("Espectro de Frecuencia de la señal grabada")
        plt.show()

menu()