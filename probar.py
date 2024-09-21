import tkinter as tk
from tkinter import Canvas

def animacion():
    ventana_secundaria1 = tk.Toplevel()
    ventana_secundaria1.title("Super Pang")
    ventana_secundaria1.geometry("800x800")
    ventana_secundaria1.config(bg="#C7FFD8")
    canvas = Canvas(ventana_secundaria1, width=800, height=800, bg="black")
    canvas.pack()
    global vx, vy, grav, rebote, rectangulo,rectangulo_der,rectangulo_izq, a_extender,i_extender,d_extender, cuadrado, circulos, vidas, vidas_texto, juego_terminado,municion,municion_texto,temporizador
    vx = 10
    vy = 0
    grav = 0.5
    rebote = -1
    rectangulo = None
    rectangulo_der = None
    rectangulo_izq = None
    a_extender = -10
    d_extender = 10
    i_extender = 10
    circulos = []
    vidas = 3
    municion = 3
    juego_terminado = False
    temporizador = None
    vidas_texto = canvas.create_text(50, 20, text=f"Vidas: {vidas}", fill="white", font=("Arial", 20))
    municion_texto = canvas.create_text(70, 50, text=f"Munición: {municion}", fill="white", font=("Arial", 20))

    def extender_rectangulo():
        global rectangulo
        if rectangulo and not juego_terminado:
            x1, y1, x2, y2 = canvas.coords(rectangulo)
            if y1 > 0:
                canvas.coords(rectangulo, x1, y1 + a_extender, x2, y2)
                ventana_secundaria1.after(20, extender_rectangulo)
            else:
                canvas.delete(rectangulo)
                rectangulo = None

    def extender_rectangulo_der():
        global rectangulo_der
        if rectangulo_der and not juego_terminado:
            x1, y1, x2, y2 = canvas.coords(rectangulo_der)
            if x2 < canvas.winfo_width():
                canvas.coords(rectangulo_der, x1, y1, x2 + d_extender, y2)
                ventana_secundaria1.after(20, extender_rectangulo_der)
            else:
                canvas.delete(rectangulo_der)
                rectangulo_der = None

    def extender_rectangulo_izq():
        global rectangulo_izq
        if rectangulo_izq and not juego_terminado:
            x1, y1, x2, y2 = canvas.coords(rectangulo_izq)
            if x1 > 0:
                canvas.coords(rectangulo_izq, x1 - i_extender, y1, x2, y2)
                ventana_secundaria1.after(20, extender_rectangulo_izq)
            else:
                canvas.delete(rectangulo_izq)
                rectangulo_izq = None

    def detectar_colision(circulo, rectangulo):
        coords = canvas.bbox(circulo['id'])
        rect_coords = canvas.bbox(rectangulo)
        if (coords[2] > rect_coords[0] and coords[0] < rect_coords[2] and
                coords[3] > rect_coords[1] and coords[1] < rect_coords[3]):
            return True
        return False
    
    def disparar_rectangulo(event):
        global rectangulo, municion
        if juego_terminado or municion <= 0:
            return
        if not rectangulo:
            x1, y1, x2, y2 = canvas.bbox(cuadrado)
            rectangulo = canvas.create_rectangle(x1 + 45, y1, x2 - 45, y1 - 5, fill='red')
            extender_rectangulo()
            municion -= 1
            actualizar_municion()
            verificar_municion()

    def disparar_rectangulo_der(event):
        global rectangulo_der,municion
        if juego_terminado or municion <= 0:
            return
        if not rectangulo_der:
            x1, y1, x2, y2 = canvas.bbox(cuadrado)
            rectangulo_der = canvas.create_rectangle(x2, y1+45, x2+5 , y2-45, fill='red')
            extender_rectangulo_der()
            municion -= 1
            actualizar_municion()
            verificar_municion()
    
    def disparar_rectangulo_izq(event):
        global rectangulo_izq,municion
        if juego_terminado or municion <= 0:
            return
        if not rectangulo_izq:
            x1, y1, x2, y2 = canvas.bbox(cuadrado)
            rectangulo_izq = canvas.create_rectangle(x1-5, y1+45, x2 , y2-45, fill='red')
            extender_rectangulo_izq()
            municion -= 1
            actualizar_municion()
            verificar_municion()

    def mover_circulos(indice=0):
        if juego_terminado:
            return
        global rectangulo, division_realizada,rectangulo_der,rectangulo_izq
        if indice < len(circulos):
            circulo = circulos[indice]
            vx, vy = circulo['vel']
            vy += grav
            canvas.move(circulo['id'], vx, vy)
            coords = canvas.bbox(circulo['id'])

            if coords[3] >= 800:
                vy *= rebote
            elif coords[1] <= 0:
                canvas.move(circulo['id'], 0, -coords[1])
                vy *= rebote

            if coords[2] >= 800 or coords[0] <= 0:
                vx *= -1
            
            if rectangulo and detectar_colision(circulo, rectangulo):
                dividir_esfera(circulo, coords, vx, vy)
                canvas.delete(rectangulo)
                rectangulo = None

            if rectangulo_izq and detectar_colision(circulo, rectangulo_izq):
                dividir_esfera(circulo, coords, vx, vy)
                canvas.delete(rectangulo_izq)
                rectangulo_izq = None

            if rectangulo_der and detectar_colision(circulo, rectangulo_der):
                dividir_esfera(circulo, coords, vx, vy)
                canvas.delete(rectangulo_der)
                rectangulo_der = None

            circulo['vel'] = (vx, vy)
            ventana_secundaria1.after(20, mover_circulos, indice + 1)
        else:
            ventana_secundaria1.after(20, mover_circulos, 0)

    def dividir_esfera(circulo, coords, vx, vy):
        if coords[2] - coords[0] == 150 or coords[3] - coords[1] == 150:
            canvas.delete(circulo['id'])
            circulos.remove(circulo)
            crear_nueva_esfera(coords, vx, vy, 88)
            crear_nueva_esfera(coords, -vx, vy, 88)
        elif coords[2] - coords[0] == 88 or coords[3] - coords[1] == 88:
            canvas.delete(circulo['id'])
            circulos.remove(circulo)
            crear_nueva_esfera(coords, vx, vy, 25)
            crear_nueva_esfera(coords, -vx, vy, 25)
        elif coords[2] - coords[0] == 25 or coords[3] - coords[1] == 25:
            canvas.delete(circulo['id'])
            circulos.remove(circulo)

    def verificar_colisiones_rectangulo():
        global rectangulo_izq, rectangulo_der, rectangulo,circulos
        if juego_terminado:
            return
        if rectangulo_izq is not None:
            verificar_colision_individual(rectangulo_izq)
        if rectangulo_der is not None:
            verificar_colision_individual(rectangulo_der)
        if rectangulo is not None:
            verificar_colision_individual(rectangulo)

    def verificar_colision_individual(rect):
        global vx, vy
        if len(circulos) > 0:
            circulo = circulos[0]
            rect_bbox = canvas.bbox(rect)
            circulo_bbox = canvas.bbox(circulo['id'])
            if (rect_bbox[0] < circulo_bbox[2] and
                rect_bbox[2] > circulo_bbox[0] and
                rect_bbox[1] < circulo_bbox[3] and
                rect_bbox[3] > circulo_bbox[1]):
                coords = canvas.coords(circulo['id'])
                vx, vy = circulo['vel']
                dividir_esfera(circulo, coords, vx, vy)

    def verificar_colision_cuadrado():
        if juego_terminado:
            return
        global vidas, cuadrado_bbox
        cuadrado_bbox = canvas.bbox(cuadrado)
        for circulo in circulos:
            circulo_bbox = canvas.bbox(circulo['id'])
            if (cuadrado_bbox[0] < circulo_bbox[2] and
                cuadrado_bbox[2] > circulo_bbox[0] and
                cuadrado_bbox[1] < circulo_bbox[3] and
                cuadrado_bbox[3] > circulo_bbox[1]):
                vidas -= 1
                actualizar_vidas()
                canvas.delete(circulo['id'])
                circulos.remove(circulo)
                if vidas <= 0:
                    game_over()
                    return
        ventana_secundaria1.after(50, verificar_colision_cuadrado)

    def actualizar_vidas():
        canvas.itemconfig(vidas_texto, text=f"Vidas: {vidas}")
        
    def actualizar_municion():
        canvas.itemconfig(municion_texto, text=f"Munición: {municion}")

    def verificar_municion():
        global temporizador
        if municion <= 0:
            ventana_secundaria1.unbind("<KeyPress-w>")
            ventana_secundaria1.unbind("<KeyPress-a>")
            ventana_secundaria1.unbind("<KeyPress-d>")
            if temporizador is None:
                temporizador = ventana_secundaria1.after(10000, verificar_tiempo_sin_municion)
        else:
            if temporizador is not None:
                ventana_secundaria1.after_cancel(temporizador)
                temporizador = None
    
    def verificar_tiempo_sin_municion():
        global municion
        if municion <= 0:
            game_over()

    def game_over():
        global juego_terminado
        juego_terminado = True
        canvas.create_text(400,400, text="GAME OVER", fill="white", font=("Arial", 50))
        ventana_secundaria1.unbind("<KeyPress-Left>")
        ventana_secundaria1.unbind("<KeyPress-Right>")
        ventana_secundaria1.unbind("<KeyPress-w>")
        ventana_secundaria1.unbind("<KeyPress-a>")
        ventana_secundaria1.unbind("<KeyPress-d>")
        button_salir = tk.Button(ventana_secundaria1, text="Salir", command=ventana_secundaria1.destroy)
        button_salir_window = canvas.create_window(400, 450, anchor="nw", window=button_salir)

    def crear_nueva_esfera(coords, vx, vy, size):
        x1, y1, x2, y2 = coords
        nuevo_id = canvas.create_oval(x1, y1, x1 + size, y1 + size, fill='blue')
        circulos.append({'id': nuevo_id, 'vel': (vx, vy)})

    def mover_cuadrado(event):
        if juego_terminado:
            return
        global coords
        if event.keysym == "Left":
            canvas.move(cuadrado, -10, 0)
        elif event.keysym == "Right":
            canvas.move(cuadrado, 10, 0)

        coords = canvas.bbox(cuadrado)
        if coords[0] <= 0:
            canvas.move(cuadrado, 10, 0)
        elif coords[2] >= 800:
            canvas.move(cuadrado, -10, 0)

    

    cuadrado = canvas.create_rectangle(200, 700, 300, 800, fill='white')
    circulo_azul = canvas.create_oval(190, 0, 340, 150, fill='blue')
    circulo_rojo = canvas.create_oval(360, 0, 510, 150, fill='red')

    circulos.append({'id': circulo_azul, 'vel': (vx, vy)})
    circulos.append({'id': circulo_rojo, 'vel': (vx, vy)})

    ventana_secundaria1.bind_all("<KeyPress-Left>", mover_cuadrado)
    ventana_secundaria1.bind_all("<KeyPress-Right>", mover_cuadrado)
    ventana_secundaria1.bind_all("<KeyPress-w>", disparar_rectangulo)
    ventana_secundaria1.bind_all("<KeyPress-d>", disparar_rectangulo_der)
    ventana_secundaria1.bind_all("<KeyPress-a>", disparar_rectangulo_izq)

    mover_circulos()
    verificar_colision_cuadrado()

root = tk.Tk()
root.withdraw()
animacion()
root.mainloop()