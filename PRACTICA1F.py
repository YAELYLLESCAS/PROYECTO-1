import tkinter as tk 
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import serial
import time
from ttkthemes import ThemedTk

ser = None
lectura_activa = False

def conectar():
    global ser
    puerto = combo_puerto.get()
    velocidad = combo_baudrate.get()

    try:
        ser = serial.Serial(puerto, int(velocidad), timeout=1)
        time.sleep(2)
        label_led.config(image=led_verde)
        messagebox.showinfo("Conectado", f"Conectado al puerto {puerto} a {velocidad} baudios.")
        ser.write(f'SET_BAUD,{velocidad}\n'.encode())
        time.sleep(1)

    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))
        label_led.config(image=led_rojo)

def controlar_led(estado):
    if ser:
        if estado == 'on':
            ser.write(b'LED_ON\n')
        else:
            ser.write(b'LED_OFF\n')
    else:
        messagebox.showerror("Error de conexión", "No hay conexión con el dispositivo.")

def seleccionar_opcion():
    opcion = spinbox_opcion.get()
    btn_ejecutar.config(state='normal')
    entry_dato.grid_remove()
    label_entrada.grid_remove()
    entry_pwm.grid_remove()
    label_pwm.grid_remove()
    label_resistencia.grid_remove()

    if opcion == '1':
        label_entrada.grid(column=0, row=2, padx=10, pady=10)
        entry_dato.grid(column=1, row=2, padx=10, pady=10)
    elif opcion == '3':
        label_pwm.grid(column=0, row=3, padx=10, pady=10)
        entry_pwm.grid(column=1, row=3, padx=10, pady=10)

def iniciar_lectura_resistencia():
    label_resistencia.grid(column=0, row=5, padx=10, pady=10)
    global lectura_activa
    lectura_activa = True
    leer_resistencia_tiempo_real()

def detener_lectura_resistencia():
    global lectura_activa
    lectura_activa = False

def leer_resistencia_tiempo_real():
    global lectura_activa
    if ser and lectura_activa:
        ser.write(b'TAREA_2\n')  
        valor_analogico = ser.readline().decode('utf-8').strip()
        if valor_analogico.isdigit():
            resistencia = calcular_resistencia(int(valor_analogico))
            label_resistencia.config(text=f"Resistencia: {resistencia} ohms")
        else:
            label_resistencia.config(text="Valor no válido")
        root.after(500, leer_resistencia_tiempo_real)

def ejecutar_tarea():
    opcion = spinbox_opcion.get()
    
    if opcion == '1':
        numero = entry_dato.get()
        if numero.isdigit():
            ser.write(f'TAREA_1{numero}\n'.encode())
            time.sleep(1.5)
            while True:
                respuesta = ser.readline().decode('utf-8').strip()
                if respuesta.isdigit():
                    messagebox.showinfo("Resultado", f"El resultado es: {respuesta}")
                    break
                else:
                    print(f"Recibido: {respuesta}")
        else:
            messagebox.showerror("Error", "Introduce un número válido.")
    
    elif opcion == '2':
        btn_detener.config(state="normal")
        iniciar_lectura_resistencia()
        
    elif opcion == '3':
        valor_pwm = entry_pwm.get()
        if valor_pwm.isdigit() and 0 <= int(valor_pwm) <= 255:
            ser.write(f'TAREA_3,{valor_pwm}\n'.encode())
            messagebox.showinfo("PWM", f"Intensidad ajustada a: {valor_pwm}")
        else:
            messagebox.showerror("Error", "Introduce un valor entre 0 y 255.")
            
    else:
        messagebox.showinfo("Opción inválida", "Selecciona una opción válida.")

def calcular_resistencia(valor_analogico):
    resistencia = (valor_analogico / 4095) * 10000 
    return round(resistencia, 2)

root = ThemedTk() 
root.title("Control de LED y Dispositivo Serial")
root.set_theme("equilux")  

led_rojo_img = Image.open("led_rojo.jpg").resize((50, 50))
led_rojo = ImageTk.PhotoImage(led_rojo_img)
led_verde_img = Image.open("led_verde.jpg").resize((50, 50))
led_verde = ImageTk.PhotoImage(led_verde_img)

notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="Conectar")
notebook.add(tab2, text="Control de Tareas")
notebook.pack(expand=True, fill="both")

label_puerto = ttk.Label(tab1, text="Puerto:")
label_puerto.grid(column=0, row=0, padx=10, pady=10)
combo_puerto = ttk.Combobox(tab1, values=["COM3", "COM4", "COM5", "COM6"], state="readonly")
combo_puerto.grid(column=1, row=0, padx=10, pady=10)

label_baudrate = ttk.Label(tab1, text="Velocidad:")
label_baudrate.grid(column=0, row=1, padx=10, pady=10)
combo_baudrate = ttk.Combobox(tab1, values=["9600", "115200"], state="readonly")
combo_baudrate.grid(column=1, row=1, padx=10, pady=10)

btn_conectar = ttk.Button(tab1, text="Conectar", command=conectar)
btn_conectar.grid(column=0, row=2, padx=10, pady=10)

label_led = tk.Label(tab1)
label_led.grid(column=1, row=2, padx=10, pady=10)
label_led.config(image=led_rojo)

btn_led_on = ttk.Button(tab1, text="LED ON", command=lambda: controlar_led('on'))
btn_led_on.grid(column=0, row=3, padx=10, pady=10)

btn_led_off = ttk.Button(tab1, text="LED OFF", command=lambda: controlar_led('off'))
btn_led_off.grid(column=1, row=3, padx=10, pady=10)

label_opcion = ttk.Label(tab2, text="Selecciona una opción:")
label_opcion.grid(column=0, row=0, padx=10, pady=10)

spinbox_opcion = ttk.Spinbox(tab2, from_=1, to=3, state="readonly")
spinbox_opcion.grid(column=1, row=0, padx=10, pady=10)

btn_enter = ttk.Button(tab2, text="Enter", command=seleccionar_opcion)
btn_enter.grid(column=2, row=0, padx=10, pady=10)

label_entrada = ttk.Label(tab2, text="Introduce un número:")
entry_dato = ttk.Entry(tab2)

label_pwm = ttk.Label(tab2, text="Intensidad (0-255):")
entry_pwm = ttk.Entry(tab2)

label_resistencia = ttk.Label(tab2)

btn_ejecutar = ttk.Button(tab2, text="Ejecutar", state='disabled', command=ejecutar_tarea)
btn_ejecutar.grid(column=0, row=4, padx=10, pady=10)

btn_detener = ttk.Button(tab2, text="Detener Lectura", command=detener_lectura_resistencia, state='disabled')
btn_detener.grid(column=1, row=4, padx=10, pady=10)

root.mainloop()
