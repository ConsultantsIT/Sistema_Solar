import pygame
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
width, height = 1600, 800
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Sistema Solar 3D Colorido")

# Configuración de OpenGL
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 1, 10000)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])

# Parámetros ajustados
ESCALA = 6
VEL_ROTACION = 0.5
INCLINACION = 0

# Paleta de colores realistas (RGB)
COLORES = {
    "sol": [(1.0, 0.5, 0.0), (1.0, 0.3, 0.0), (1.0, 0.7, 0.0)],  # Naranja degradado
    "mercurio": (0.6, 0.6, 0.6),     # Gris metálico
    "venus": (0.9, 0.6, 0.2),        # Amarillo oscuro
    "tierra": (0.2, 0.4, 0.9),       # Azul océano
    "marte": (0.8, 0.3, 0.1),        # Rojo marciano
    "jupiter": (0.8, 0.6, 0.4),      # Marrón atmosférico
    "saturno": (0.9, 0.8, 0.6),      # Beige anillado
    "urano": (0.4, 0.8, 0.9),        # Azul verdoso
    "neptuno": (0.2, 0.2, 0.8)       # Azul profundo
}

class Planeta:
    def __init__(self, nombre, distancia, radio, velocidad, anillos=False):
        self.nombre = nombre
        self.distancia = distancia * ESCALA
        self.radio = radio * ESCALA * 2
        self.velocidad = velocidad
        self.angulo = np.random.uniform(0, 360)
        self.anillos = anillos
        
        # Configurar material con color
        self.material = GL_DIFFUSE
        self.color = COLORES[nombre.lower()]
        
    def dibujar(self):
        glPushMatrix()
        
        # Inclinación y movimiento orbital
        glRotatef(INCLINACION, 1, 0, 0)
        glRotatef(self.angulo, 0, 1, 0)
        glTranslatef(self.distancia, 0, 0)
        
        # Rotación axial
        glRotatef(self.angulo * 3, 0, 1, 0)
        
        # Configurar material
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        
        # Dibujar planeta
        quad = gluNewQuadric()
        gluSphere(quad, self.radio, 64, 64)
        
        # Anillos de Saturno
        if self.anillos:
            # Materiales para anillos más realistas
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.8, 0.8, 0.9, 1.0))  # Base blanco-azulado
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.9, 0.9, 1.0, 1.0))  # Brillos fríos
            glMaterialf(GL_FRONT, GL_SHININESS, 80)
            glMaterialfv(GL_FRONT, GL_EMISSION, (0.3, 0.3, 0.6, 0.5))  # Tenue brillo azulado
            
            # Ajuste de geometría de anillos (más estrechos)
            glRotatef(100, 1, 0, 0)
            gluDisk(quad, 
                    self.radio * 1.2,  # Radio interno aumentado (anillo más estrecho)
                    self.radio * 1.6,  # Radio externo reducido
                    64, 1)
            
            # Efecto de bandas de color
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.3, 0.3, 0.3, 0.3))
            gluDisk(quad, self.radio * 1.9, self.radio * 2.1, 64, 1)
            
            # Resetear propiedades materiales
            glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1.0))
        
        glPopMatrix()
        self.angulo += self.velocidad

class Sol:
    def __init__(self):
        self.radio = 15 * ESCALA/10
        self.angulo = 0
        self.colores = [
            (1.0, 0.3, 0.0),  # Núcleo rojo
            (1.0, 0.6, 0.0),  # Capa media naranja
            (1.0, 0.8, 0.3)   # Corona amarilla
        ]
        
    def dibujar(self):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        
        # Rotación axial acelerada
        glRotatef(self.angulo, 0, 1, 0)
        self.angulo += 1.2  # Más velocidad de rotación
        
        # Núcleo con gradiente tridimensional
        quad = gluNewQuadric()
        for i, color in enumerate(self.colores):
            glColor3f(*color)
            gluSphere(quad, self.radio * (1 + i*0.3), 64, 64)
        
        # Efecto de plasma energético
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glPointSize(2.5)
        glBegin(GL_POINTS)
        for _ in range(500):
            # Variación de color en las partículas
            intensidad = np.random.uniform(0.7, 1.0)
            glColor4f(1.0, intensidad*0.4, 0.0, 0.4)
            
            # Posición aleatoria en esfera
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            r = self.radio * np.random.uniform(1.5, 2.2)
            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)
            glVertex3f(x, y, z)
        glEnd()
        
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopMatrix()

# Configurar sistema solar
cuerpos = [
    Planeta("Mercurio", 10, 0.8, 1.5),
    Planeta("Venus", 15, 1.2, 1.0),
    Planeta("Tierra", 20, 1.5, 0.8),
    Planeta("Marte", 25, 1.0, 0.6),
    Planeta("Jupiter", 35, 4.0, 0.3),
    Planeta("Saturno", 55, 3.5, 0.2, anillos=True),
    Planeta("Urano", 75, 2.5, 0.1),
    Planeta("Neptuno", 85, 2.4, 0.05)
]
sol = Sol()

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 200, 500, 0, 0, 0, 0, 1, 0)
    glRotatef(VEL_ROTACION, 0, 1, 0)
    
    # Dibujar elementos
    sol.dibujar()
    for planeta in cuerpos:
        planeta.dibujar()
    
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()