import deGonziConfig8 as cf
import CamaraScan as CS
import cv2
import multiprocessing
# Programa distribucion - Ing. Gonzalo Balonga.
import pygame
import sys
import numpy as np


for i in range(1):
    sid = 17
    np.random.seed(sid)

    # Colores
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    Yellow = (255, 255, 0)

    Background = White

    Salidas = [100, 200, 300, 400, 500, 600, 700]
    Ramal = [100, 300]

    # Una matriz que contiene la cantidad de paquetes que acumule
    CantPaq = np.zeros(14)

    # Imágenes
    Mydotimage = pygame.Surface([10, 10])
    Mydotimage.fill(Background)
    pygame.draw.circle(Mydotimage, Blue, (5, 5), 5)

    Mycajonvac = pygame.Surface([30, 30])
    Mycajonvac.fill(Background)
    pygame.draw.rect(Mycajonvac, Red, [0, 0, 15, 15], 2)

    Mycajon14 = pygame.Surface([30, 30])
    Mycajon14.fill(Background)
    pygame.draw.rect(Mycajon14, Red, [0, 0, 15, 15], 2)
    pygame.draw.rect(Mycajon14, Blue, [1, 12, 14, 3], 0)

    Mycajonsemi = pygame.Surface([30, 30])
    Mycajonsemi.fill(Background)
    pygame.draw.rect(Mycajonsemi, Red, [0, 0, 15, 15], 2)
    pygame.draw.rect(Mycajonsemi, Yellow, [1, 8, 14, 3], 0)
    pygame.draw.rect(Mycajonsemi, Blue, [1, 12, 14, 3], 0)

    Mycajon34 = pygame.Surface([30, 30])
    Mycajon34.fill(Background)
    pygame.draw.rect(Mycajon34, Red, [0, 0, 15, 15], 2)
    pygame.draw.rect(Mycajon34, Blue, [1, 4, 14, 3], 0)
    pygame.draw.rect(Mycajon34, Yellow, [1, 8, 14, 3], 0)
    pygame.draw.rect(Mycajon34, Blue, [1, 12, 14, 3], 0)

    Mycajonfull = pygame.Surface([30, 30])
    Mycajonfull.fill(Background)
    pygame.draw.rect(Mycajonfull, Red, [0, 0, 15, 15], 0)


# Defino la entidad Dot, que luego pasara a ser paquete
class Dot(pygame.sprite.Sprite):
    # El init define los valores que va a tomar el class
    def __init__(
            self,
            x,
            y,
            width,
            height,
            Destino,
            color=Black,
            radius=5,
            velocity=[0, 0],

    ):
        # Luego, definimos que va a hacer el class con esos valores.
        # A su vez definimos que otros atributos necesitara el class (que no vendran dados por datos externos)
        super().__init__()
        # Destino y ramal, son las posiciones de las 14 salidas
        self.Destino = Destino*100  #np.random.choice(Salidas)
        self.Ramal = 100
        # vely y velx son las velocidades de los paquetes self.quieto, es un booleano que me frena las iteraciones cuando llego a posicion
        self.vely = 0

        # lo siguiente genera la imagen de los paquetes
        h = 1
        if h == 1:
            self.image = Mydotimage
        else:
            self.image = pygame.Surface([radius * 2, radius * 2])
            self.image.fill(Background)
            pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()

        # Posicion velocidad y tamaño de pantalla.
        self.pos = np.array([x, y], dtype=np.float64)
        self.velx = np.asarray(velocity, dtype=np.float64)
        self.WIDTH = width
        self.HEIGHT = height

    def update(self):
        # Mueve el paquete (En realidad mueve la variable posicion, y con esta luego muevo el paquete al fin del update
        self.pos[0] += self.velx
        self.pos[1] += self.vely
        x, y = self.pos

        # Si llego a su posicion x, le da velocidad en Y. Cuando llega a su posicion en Y el paquete se detiene
        # Cuando llego a Y tambien lo saco de estado quieto, para que no se mueva ni sume mas en Cant de paquetes
        if x == self.Destino:
            print("destino", self.Destino)
            # averigua si es positivo o negativo y usa ese signo. (Np.sign)
            self.vely = np.sign(self.Ramal - 200) * 5

        if y == self.Ramal:
            self.velx = 0
            self.vely = 0
            # Recorro los vectores Ramal y salidas, para encontrar las coodenadas, luego estas coordenadas
            # las paso a un vector de 1x14 (Que luego usare como lista para seleccionar mis cajones)
            i = 0
            j = 0

            while Ramal[i] != self.Ramal:
                i = i + 1
            while Salidas[j] != self.Destino:
                j = j + 1
            if i == 0:
                CantPaq[j] = CantPaq[j] + 1
            else:
                CantPaq[j + 7] = CantPaq[j + 7] + 1

            self.kill()

            # Esto hace que se muevan!
        self.rect.x = np.int64(x)
        self.rect.y = np.int64(y)


class Cajon(pygame.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            width,
            height,
            velocity,
            foto
    ):
        super().__init__()

        self.image = foto
        self.rect = self.image.get_rect()
        self.rect.center = (x + 5, y + 9)
        self.velocity = velocity

    def update(self):

        self.rect.x = self.rect.x + self.velocity

    # funcion de pablo para cajones rellenos
    def relle(self, cc):
        if cc == 0:
            # cuando llego a 4 reincio el contador y despacho el cajon
            CantPaq[j] = 0
            self.velocity = 0
            self.image = Mycajonvac

        elif cc == 1:
            self.image = Mycajon14

        elif cc == 2:
            self.image = Mycajonsemi

        elif cc == 3:
            self.image = Mycajon34

    def respawn(self):
        self.velocity = 1
        if self.rect.y > 200:
            y = 320
        else:
            y = 70
        return Cajon(
            self.rect.x,
            y,
            self.rect.width,
            self.rect.height,
            self.velocity,
            Mycajonfull
        )


# las palabras
class Cantidad(pygame.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            width,
            height,
            color=Black,
            radius=5,
            velocity=0,
    ):
        super().__init__()
        self.dato = 0
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.tt = self.font.render(str(self.dato), True, Red, Black)
        self.ttRect = self.tt.get_rect()
        # ubicar el centro
        fact = -1
        if y > 200: fact = 1
        self.ttRect.center = (x - 7, y + fact * 60)

    def notificar(self, upup):
        self.dato = upup

    def update(self, screen):
        self.tt = self.font.render(str(self.dato), True, White, Black)
        screen.blit(self.tt, self.ttRect)


# -------Textos del final---------------------------
def finale(txt):
    pygame.display.quit()
    pygame.quit()  # este puede sobrar
    print('Simulacion Sorter Andreani')
    print(txt)
    print(CantPaq, sum(CantPaq))
    print("semilla ", sid)
    sys.exit()


# ----------------------------------
# Definiciones globales.
# Defino el tamaño de pantalla, y empiezo el programa

WIDTH = 800
HEIGHT = 400
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('Simulacion Sorter Andreani')
#programIcon = pygame.image.load('C:/Users/gbalonga/Desktop/ikon.png')
#pygame.display.set_icon(programIcon)

font = pygame.font.Font('freesansbold.ttf', 16)
text = font.render('GeeksForGeeks', True, Black, Green)
textRect = text.get_rect()

# ubicar el centro
textRect.center = (80, 10)
screen.blit(text, textRect)

# Container es el contenedor del conjunto de sprites (Objetos)
container = pygame.sprite.Group()
cajones = pygame.sprite.Group()
letreros = pygame.sprite.Group()

T = 10000  # T es el tiempo maximo de la simulacion
clock = pygame.time.Clock()

# Creo los cajones y cantidades
# Lista es una lista que contiene todos los Cajones que necesitamos crear.
# Una vez crada la Lista, agregamos el grupo entero a Cajones
# idem para cantidad y letreros
Lista = []
Listex = []
for i in Ramal:
    for n in Salidas:
        nuevo = Cajon(n - 15, i, WIDTH, HEIGHT, velocity=0, foto=Mycajonvac)
        Lista.append(nuevo)
        niu = Cantidad(n - 15, i, WIDTH, HEIGHT)
        Listex.append(niu)
cajones.add(Lista)
letreros.add(Listex)

# ///////////////////////////////Comienza el programa//////////////////////////

for i in range(T):

    # Creo el paquete cada x tiempo
    if i % 200 == 0:
        x = 790
        y = 200
        velx = -1
        print(CS.Scan())
        lugar = CS.Scan()
        if lugar != 0:
            guy = Dot(x, y, WIDTH, HEIGHT, color=Blue, velocity=velx, Destino=lugar)
            container.add(guy)

    container.update()

    # Me fijo si el cajon esta lleno y lo despacho
    for j in range(14):
        if CantPaq[j] == 0: continue
        if CantPaq[j] == 4:
            nuevo = Lista[j].respawn()
            cajones.add(nuevo)

        if CantPaq[j] < 5: Lista[j].relle(CantPaq[j] % 4)
        Listex[j].notificar(CantPaq[j])

    cajones.update()

    datos = "tiempo : " + str(i) + " : "
    datos += "    total  " + str(sum(CantPaq)) + "   paquetes "
    text = font.render(datos, False, Green, Black)

    screen.fill(Background)
    screen.blit(text, textRect)

    container.draw(screen)
    cajones.draw(screen)
    # letreros no tiene un método .draw , uso el update
    letreros.update(screen)

    pygame.display.flip()
    clock.tick(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finale("Interrumpido por el usuario")
        if event.type == pygame.KEYDOWN and event.key == 27:
            finale("terminado por " + str(event.key) + " pressed")

finale("NORMAL")

## pygame.quit()
