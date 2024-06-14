WINDOW_SIZE = 800
WS = WINDOW_SIZE
N = 7

FPS = 200

epsilon = 10
sigma = 0.05
mouse_forse = 1*10**-4
mouse_forse_k = 0
gravity_force = 0.5

dT = [10**-6, 10**-5, 5*10**-5, 10**-4, 5*10**-4, 8*10**-4, 10**-3, 10**-3, 10**-3, 10**-3]
nT = [4,      4,      8,        4,      8,        16,       2,      6,     10,      15]
iT = 0



k_tr = 0.00
k_otr = 1
v_otr = 0

##Не трогать
A_forse = epsilon * sigma**6 / 1.5
B_forse = epsilon * sigma**12 / 3

import pygame as pg
import math
import random

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

f = pg.font.Font(None, int(round(WINDOW_SIZE*36/850)))
pg.font.init()



class Partical:
    def __init__(self):
        self.x = random.random()
        self.y = random.random()
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.m = 1
        
    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    def force_by_another_partical(self, other):
        r = ((other.x - self.x)**2 + (other.y - self.y)**2)**0.5
        if r < sigma/10:
            self.x+=0.03*(random.random()-0.5)
            self.y+=0.03*(random.random()-0.5)
            r = sigma/10
        alpha = math.atan2(other.y - self.y, other.x - self.x)
        self.ax += math.cos(alpha) * (A_forse / r**7 - B_forse / r**13)
        self.ay += math.sin(alpha) * (A_forse / r**7 - B_forse / r**13)

    def force_by_mouse(self, mouse_pos):
        r = ((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)**0.5
        if r < 10**-10:
            r = 10**-5
        alpha = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
        if(r<0.01):
            return
        self.ax += math.cos(alpha) * mouse_forse / max(r, 0.01)**1 * mouse_forse_k / (dT[iT]*nT[iT])
        self.ay += math.sin(alpha) * mouse_forse / max(r, 0.01)**1 * mouse_forse_k / (dT[iT]*nT[iT])

    def force_by_gravity(self):
        if(self.y<0.99):
            self.ay += gravity_force

    def update(self, dt):
        if abs(self.ax) > 700/dt:
            self.x+=0.03*(random.random()-0.5)
            self.ax = 0
        if abs(self.ay) > 700/dt:
            self.y+=0.03*(random.random()-0.5)
            self.ay = 0
        self.vx += self.ax*dt
        self.vy += self.ay*dt

        self.vx *= (1-k_tr*dt)
        self.vy *= (1-k_tr*dt)

        if(abs(self.vx) > 0.5*sigma/dt):
            self.vx = random.random()-0.5
        if(abs(self.vy) > 0.5*sigma/dt):
            self.vy = random.random()-0.5
        if abs(self.ax) > 0.2*sigma/dt/dt:
            self.x+=0.03*(random.random()-0.5)
        if abs(self.ay) > 0.2*sigma/dt/dt:
            self.y+=0.03*(random.random()-0.5)
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.ax = 0
        self.ay = 0

    def wall(self):
        if(self.x > 1):
#            self.x = 1 - 0.01 * random.random()
            self.vx = -abs(self.vx)*k_otr - v_otr * random.random()
        elif(self.x < 0):
#            self.x = 0 + 0.01 * random.random()
            self.vx = abs(self.vx)*k_otr + v_otr * random.random()
        if(self.y > 1):
            self.y = 1
            self.vy = -abs(self.vy)*k_otr - v_otr * random.random()
        elif(self.y < 0):
#            self.y = + 0.01 * random.random()
            self.vy = abs(self.vy)*k_otr + v_otr * random.random()

        if(self.x<-1.2):
            self.x = random.random()
            self.vx = 0
        if(self.x>1.2):
            self.x = random.random()
            self.vx = 0
        if(self.y<-1.2):
            self.y = random.random()
            self.vy = 0
        if(self.y>1.2):
            self.y = random.random()
            self.vy = 0

particals = []
for i in range(N):
    for j in range(N):
        partical = Partical()
        partical.x = 0.01 + i*sigma
        partical.y = 0.99 - j*sigma
        particals.append(partical)


mouse_pos = (0.5, 0.5)

k_otobr = WINDOW_SIZE*0.9

sim = True

def sim_update(dt):
    for partical in particals:
        for another_partical in particals:
            if(partical == another_partical):
                continue
            partical.force_by_another_partical(another_partical)
            partical.force_by_mouse(mouse_pos)
            partical.force_by_gravity()
    for partical in particals:
        partical.update(dt)
        partical.wall()
    attach_partical()

def attach_partical():
    if not is_attach:
        return
    r_min = 100
    closest_partical = None
    for partical in particals:
        r = (partical.x - mouse_pos[0])**2 + (partical.y-mouse_pos[1])**2
        if(r < r_min):
            r_min = r
            closest_partical = partical
    closest_partical.x = mouse_pos[0]
    closest_partical.y = mouse_pos[1]
    closest_partical.vx = 0
    closest_partical.vy = 0

is_attach = 0

while sim:
    screen.fill((0,0,0))

    for i in range(nT[iT]):
        sim_update(dT[iT])

    T = 0
    for partical in particals:
        pg.draw.circle(screen, (255,255,255), (WINDOW_SIZE/20 + partical.x*k_otobr, WINDOW_SIZE/20 + partical.y*k_otobr), 5)
        T += partical.vx**2 + partical.vy**2
    T = T/N
    
#    pg.draw.circle(screen, (0,255,255), (WINDOW_SIZE/20 + mouse_pos[0]*k_otobr, WINDOW_SIZE/20 + mouse_pos[1]*k_otobr), 5)

    screen.blit(f.render(f"T = {T}", 1, (0, 255, 100)) , (WS*1/100, WS * 4/100))

    pg.display.update()
    clock.tick(FPS)


    for event in pg.event.get():
        if event.type == pg.QUIT:
            sim = False
        if event.type == pg.MOUSEMOTION:
            mouse_pos = ((event.pos[0] - WINDOW_SIZE/20)/k_otobr,  (event.pos[1] - WINDOW_SIZE/20)/k_otobr)
        if event.type == pg.MOUSEBUTTONDOWN:
            if(event.button == 1):
                mouse_forse_k = 1
            if(event.button == 3):
                is_attach = 1
        if event.type == pg.MOUSEBUTTONUP:
            if(event.button == 1):
                mouse_forse_k = 0
            if(event.button == 3):
                is_attach = 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_MINUS:
                iT-=1
                if(iT<0):
                    iT = 0
            if event.key == pg.K_EQUALS:
                iT+=1
                if(iT>9):
                    iT = 9

            if event.key == pg.K_q:
                for partical in particals:
                    partical.vx = 0
                    partical.vy = 0
            if event.key == pg.K_w:
                for partical in particals:
                    partical.vx *= 0.8
                    partical.vy *= 0.8
            if event.key == pg.K_e:
                for partical in particals:
                    partical.vx *= 1.2
                    partical.vy *= 1.2
                
    print(nT[iT], dT[iT])
pg.quit()