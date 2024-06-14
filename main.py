WINDOW_SIZE = 1000

N = 10

FPS = 200

A_forse = 10**-2
B_forse = 10**4
mouse_forse = 1*10**-4
mouse_forse_k = 0
p = 5
dT = 10**-p
r0 = 0.01
k_tr = 0.05
k_otr = 1
v_otr = 0
import pygame as pg
import math
import random


pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


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
        if r < 10**-10:
            self.x+=0.03*(random.random()-0.5)
            self.y+=0.03*(random.random()-0.5)
            r = 10**-5
        alpha = math.atan2(other.y - self.y, other.x - self.x)
        self.ax += math.cos(alpha) * (A_forse * (r/r0)**-7 - B_forse * (r/r0)**-13)
        self.ay += math.sin(alpha) * (A_forse * (r/r0)**-7 - B_forse * (r/r0)**-13)

    def force_by_mouse(self, mouse_pos):
        r = ((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)**0.5
        if r < 10**-10:
            r = 10**-5
        alpha = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
        if(r<0.01):
            return
        self.ax += math.cos(alpha) * mouse_forse / max(r, 0.01)**1 * mouse_forse_k / dT
        self.ay += math.sin(alpha) * mouse_forse / max(r, 0.01)**1 * mouse_forse_k / dT
    def update(self, dt):
        self.vx += self.ax*dt
        self.vy += self.ay*dt

        self.vx *= (1-k_tr*dt)
        self.vy *= (1-k_tr*dt)

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
#           self.y = 1 - 0.01 * random.random()
            self.vy = -abs(self.vy)*k_otr - v_otr * random.random()
        elif(self.y < 0):
#            self.y = + 0.01 * random.random()
            self.vy = abs(self.vy)*k_otr + v_otr * random.random()


particals = []
for i in range(N):
    particals.append(Partical())

particals[0].x = 0.1
particals[0].y = 0.1
particals[1].x = 0.1+r0*1.1
particals[1].y = 0.1+r0*1.1

mouse_pos = (0.5, 0.5)

k_otobr = WINDOW_SIZE*0.9

sim = True

while sim:
    screen.fill((0,0,0))
    for partical in particals:
        for another_partical in particals:
            if(partical == another_partical):
                continue
            partical.force_by_another_partical(another_partical)
            partical.force_by_mouse(mouse_pos)

    Q = 0
    for partical in particals:
        partical.update(dT)
        partical.wall()
        pg.draw.circle(screen, (255,255,255), (WINDOW_SIZE/20 + partical.x*k_otobr, WINDOW_SIZE/20 + partical.y*k_otobr), 5)
        Q += partical.vx**2 + partical.vy**2
    Q = Q/N
    pg.draw.circle(screen, (0,255,255), (WINDOW_SIZE/20 + mouse_pos[0]*k_otobr, WINDOW_SIZE/20 + mouse_pos[1]*k_otobr), 5)









    pg.display.update()
    clock.tick(FPS)


    for event in pg.event.get():
        if event.type == pg.QUIT:
            sim = False
        if event.type == pg.MOUSEMOTION:
            mouse_pos = ((event.pos[0] - WINDOW_SIZE/20)/k_otobr,  (event.pos[1] - WINDOW_SIZE/20)/k_otobr)
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_forse_k = 1
        if event.type == pg.MOUSEBUTTONUP:
            mouse_forse_k = 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_MINUS:
                p+=1
            if event.key == pg.K_EQUALS:
                p-=1
                if p<-5:
                    p = -5

            if event.key == pg.K_q:
                for partical in particals:
                    partical.vx = 0
                    partical.vy = 0
            if event.key == pg.K_w:
                for partical in particals:
                    partical.vx *= 0.5
                    partical.vy *= 0.5
                
            dT = 10**(-p)
    print(Q)
pg.quit()