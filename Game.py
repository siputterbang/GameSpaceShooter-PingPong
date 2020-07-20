#MODUL
import pygame
import random
import turtle
import time
#INIT
pygame.font.init()
pygame.mixer.init()
#Layar
LEBARL,TINGGIL = 720,720
LAYAR = pygame.display.set_mode((LEBARL,TINGGIL))
pygame.display.set_caption("Space Shooter")
#GAMBAR PLAYER
PESAWAT_MUSUH1 =pygame.image.load("assets/musuh/musuh1.png")
PESAWAT_MUSUH2 =pygame.image.load("assets/musuh/musuh2.png")
PESAWAT_MUSUH3 = pygame.image.load("assets/musuh/musuh3.png")
PESAWAT_MUSUH4 =pygame.image.load("assets/musuh/musuh4.png")
PESAWAT_MUSUH5 = pygame.image.load("assets/musuh/musuh5.png")
PESAWAT_MUSUH6 = pygame.image.load("assets/musuh/musuh6.png")
PESAWAT_MUSUH7 = pygame.image.load("assets/musuh/musuh7.png")
PESAWAT_MUSUH8 = pygame.image.load("assets/musuh/musuh8.png")
PESAWAT_MUSUH9 = pygame.image.load("assets/musuh/musuh9.png")
PESAWAT_MUSUH10 = pygame.image.load("assets/musuh/musuh10.png")
PESAWAT_MUSUH11 = pygame.image.load("assets/musuh/musuh11.png")
PESAWAT_MUSUH12 = pygame.image.load("assets/musuh/musuh12.png")
PESAWAT_MUSUH13 = pygame.image.load("assets/musuh/musuh13.png")
PESAWAT_MUSUH14 = pygame.image.load("assets/musuh/musuh14.png")
PESAWAT_MUSUH15 = pygame.image.load("assets/musuh/musuh15.png")
PESAWAT_MUSUH16 = pygame.image.load("assets/musuh/musuh16.png")
PESAWAT_MUSUH17 = pygame.image.load("assets/musuh/musuh17.png")
PESAWAT_MUSUH18 = pygame.image.load("assets/musuh/musuh18.png")
PESAWAT_MUSUH19 = pygame.image.load("assets/musuh/musuh19.png")
PESAWAT_MUSUH20 = pygame.image.load("assets/musuh/musuh20.png")
PESAWAT_MUSUH21 = pygame.image.load("assets/musuh/musuh21.png")
#PLAYERUTAMA
PESAWAT_PLAYER1 = pygame.image.load("assets/pesawatlevel1.png")
PESAWAT_PLAYER2 = pygame.image.load("assets/pesawatlevel2.png")
PESAWAT_PLAYER3 = pygame.image.load("assets/pesawatlevel3.png")
PESAWAT_PLAYER4 = pygame.image.load("assets/pesawatlevel4.png")
PESAWAT_PLAYER5 = pygame.image.load("assets/pesawatlevel5.png")
#SENJATA
LASER_MERAH = pygame.image.load("assets/pixel_laser_red.png")
LASER_HIJAU = pygame.image.load("assets/pixel_laser_green.png")
LASER_BIRU = pygame.image.load("assets/pixel_laser_blue.png")
LASER_KUNING = pygame.image.load("assets/pixel_laser_yellow.png")
#BACKGROUNDLAYAR
BACKGRND = pygame.transform.scale(pygame.image.load("assets/background-black.png"),(LEBARL,TINGGIL))
BACKGRNDAWAL = pygame.transform.scale(pygame.image.load("assets/backgorund.png"),(LEBARL,TINGGIL))
#LAGU AWAL
mainlagu = pygame.mixer.Sound("assets/mainmenulagu.wav")
mainlagu.play(-2)
skor = 0
#CLASS & FUNGSI
class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        #menampilkan laser ke layar, || window = LAYAR
        window.blit(self.img,(self.x,self.y))

    def move(self,kecepatan):
        #pergerakan pesawat/laser
        self.y += kecepatan

    def off_screen(self,obj):
        #apabila obj/laser keluar dari layar.
        return  not (self.y <= TINGGIL and self.y >=0)

    def menabrak(self,obj):
        #apabila objek/laser/pesawat saling bertabrakan
        return collide(self,obj)
#class tidak dikhususkan untuk karakter tertentu ,namun digunakan untuk semua karakter
class Pesawat:
    COOLDOWN = 30
    def __init__(self,x,y,nyawa=100 ):
        self.x = x
        self.y = y
        self.nyawa = nyawa
        self.pesawat_img = None
        self.laser_img = None
        self.laser = []
        self.cooldown_counter = 0

    def draw(self,window):
        window.blit(self.pesawat_img,(self.x,self.y))
        for laser in self.laser:
            laser.draw(window)

    def move_lasers(self,kecepatan,obj):
        self.cooldown()
        for laser in self.laser:
            laser.move(kecepatan)
            if laser.off_screen(TINGGIL):
                self.laser.remove(laser)
            elif laser.menabrak(obj):
                obj.nyawa -= 10
                self.laser.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter+= 1
    def tembak(self):
        #fungsi untuk menembak
        if self.cooldown_counter == 0 :
            laser = Laser(self.x ,self.y,self.laser_img)
                    #fungsi |Lokasi x,y |gambar
            self.laser.append(laser)
            self.cooldown_counter = 1

    #fungsi mencari lebar secara otomatis
    def get_width(self):
        return self.pesawat_img.get_width()
    def get_height(self):
        return self.pesawat_img.get_height()

class Player(Pesawat):
    skor = 0
    def __init__(self,x,y,nyawa = 100 ):
        super().__init__(x,y,nyawa)
        self.pesawat_img = PESAWAT_PLAYER1
        self.laser_img = LASER_KUNING
        self.mask = pygame.mask.from_surface(self.pesawat_img)
        self.nyawa_penuh = nyawa

    def move_lasers(self,kecepatan,objs):
        global skor
        self.cooldown()
        for laser in self.laser:
            laser.move(kecepatan)
            if laser.off_screen(TINGGIL):
                self.laser.remove(laser)
            else:
                for obj in objs:
                    if laser.menabrak(obj):
                        objs.remove(obj)
                        self.laser.remove(laser)
                        skor += 1
                        return skor

    def draw(self,window):
        super().draw(window)
        self.nyawa_bar(window)
        self.poin(window)

    def poin(self,window):
        point = str(skor)
        skor_font = pygame.font.SysFont("comicsans",60)
        nilai = skor_font.render(point, 1, (255, 255, 255))
        window.blit(nilai, (LAYAR.get_width()/2,LAYAR.get_height()/30))
    def nyawa_bar(self,window ):
        pygame.draw.rect(window,(0,255,0),(self.x ,self.y + self.pesawat_img.get_height()+10,self.pesawat_img.get_width() * ( - (self.nyawa -100) / self.nyawa_penuh),10))
        pygame.draw.rect(window,(255,0,0),(self.x,self.y + self.pesawat_img.get_height() + 10,self.pesawat_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y + self.pesawat_img.get_height()+10,self.pesawat_img.get_width() * (self.nyawa/self.nyawa_penuh),10))


class Musuh(Pesawat):
    WARNA_PESAWAT = {
        "1":(PESAWAT_MUSUH1,LASER_MERAH),
        "2" : (PESAWAT_MUSUH2,LASER_HIJAU),
        "3": (PESAWAT_MUSUH20, LASER_BIRU),
        "4" :(PESAWAT_MUSUH3,LASER_BIRU),
        "5": (PESAWAT_MUSUH4, LASER_HIJAU),
        "6": (PESAWAT_MUSUH5, LASER_MERAH),
        "7": (PESAWAT_MUSUH6, LASER_HIJAU),
        "8": (PESAWAT_MUSUH7, LASER_MERAH),
        "9": (PESAWAT_MUSUH8, LASER_HIJAU),
        "10": (PESAWAT_MUSUH9, LASER_HIJAU),
        "11": (PESAWAT_MUSUH10, LASER_BIRU),
        "12": (PESAWAT_MUSUH11, LASER_MERAH),
        "13": (PESAWAT_MUSUH12, LASER_MERAH),
        "14": (PESAWAT_MUSUH13, LASER_BIRU),
        "15": (PESAWAT_MUSUH14, LASER_HIJAU),
        "16": (PESAWAT_MUSUH15, LASER_BIRU),
        "17": (PESAWAT_MUSUH16, LASER_MERAH),
        "18": (PESAWAT_MUSUH17, LASER_HIJAU),
        "19": (PESAWAT_MUSUH18, LASER_BIRU),
        "20": (PESAWAT_MUSUH19, LASER_MERAH),


    }

    def __init__(self,x,y,warna,nyawa=100):
        super().__init__(x,y,nyawa)
        self.pesawat_img,self.laser_img = self.WARNA_PESAWAT[warna]
        self.mask = pygame.mask.from_surface(self.pesawat_img)

    def bergerak(self,kecepatan):
        self.y += kecepatan

####NYAWA
class TambahNyawa(Pesawat):
    WARNA_NYAWA = {
        "21": (PESAWAT_MUSUH21, None),
    }

    def __init__(self,x,y,warna):
        super().__init__(x,y)
        self.pesawat_img,self.laser_img = self.WARNA_NYAWA[warna]
        self.mask = pygame.mask.from_surface(self.pesawat_img)

    def bergerak(self,kecepatan):
        self.y += kecepatan

def collide(obj1,obj2):
    maksimalx = obj2.x - obj1.x
    maksimaly = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(maksimalx,maksimaly)) != None

def spaceshooter():
    #SUARA
    level1 = pygame.mixer.Sound("assets/level1.wav")
    level2 = pygame.mixer.Sound("assets/level2.wav")
    level4 = pygame.mixer.Sound("assets/level4.wav")
    level6 = pygame.mixer.Sound("assets/queen.wav")
    mainlagu.stop()
    mainlagu.set_volume(0.3)
    level1.set_volume(0.3)
    level1.play(-2)


    start = True
    FPS = 60
    waktu = pygame.time.Clock()
    level = 0
    lives = 5
    gambar = pygame.image.load("assets/nyawakarakter.png")
    main_font = pygame.font.SysFont("comicsans",45)
    kalah_font = pygame.font.SysFont("comicsans",60)
    enemies = []
    casnyawa = []
    jumlahmusuh = 5
    enemi_kecepatan = 1
    player_kecepatan = 5
    laser_kecepatan= 4
    kalah = False
    hitung_kalah = 0
    count = 0
    player = Player(300,650)

    def redrawwindow():
        LAYAR.blit(BACKGRND,(0,0))
        #drawtext
        lives_label = main_font.render(f"X: {lives}",1,(255,255,255))
        level_label = main_font.render(f"Level:{level}",1,(255,255,255))
        LAYAR.blit(lives_label,(30,10))
        LAYAR.blit(gambar,(1,5))
        LAYAR.blit(level_label,(LEBARL - level_label.get_width() -10 ,10))

        for enemy in enemies:
            enemy.draw(LAYAR)
            if kalah:
                kalah_label = kalah_font.render("Game Over",1,(255,255,255))
                LAYAR.blit(kalah_label,(LEBARL/2 - kalah_label.get_width()/2,350))
                if level == 1:
                    mainlagu.stop()
                    level1.stop()
                elif level == 2 and level < 4:
                    level2.stop()
                    mainlagu.stop()
                elif level >= 4 and level < 6:
                    level4.stop()
                    mainlagu.stop()
                elif level >= 6:
                    level6.stop()
                    mainlagu.stop()

        for nyawa in casnyawa:
            nyawa.draw(LAYAR)
        player.draw(LAYAR)
        pygame.display.update()

    while start:
        waktu.tick(FPS)
        redrawwindow()
        if lives <= 0 or player.nyawa <= 0:
            kalah = True
            hitung_kalah +=1

        if kalah:
            if hitung_kalah > FPS *3 :
                start = False
            else:
                continue
        if len(enemies) == 0:
            level +=1
            jumlahmusuh += 5
            for i in range(jumlahmusuh):
                musuh = Musuh(random.randrange(50,LEBARL-100),random.randrange(-1500,100),random.choice(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",]))
                enemies.append(musuh)
                #baru
                isinyawa = TambahNyawa(random.randrange(50,LEBARL-100),random.randrange(-1500,100),random.choice(["21"]))
                count = 1
                #end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if level == 1:
                    level1.stop()
                    mainlagu.stop()
                elif level == 2 and level < 4:
                    level2.stop()
                    mainlagu.stop()
                elif level >= 4 and level < 6:
                    level4.stop()
                    mainlagu.stop()
                elif level >= 6:
                    level6.stop()
                    mainlagu.stop()
                start = False
                mainlagu.play(-2)
        kontrol = pygame.key.get_pressed()
        if kontrol[pygame.K_a] and player.x - player_kecepatan > 0:
            player.x -= player_kecepatan
        if kontrol[pygame.K_d] and player.x - player_kecepatan + player.get_width() < LEBARL:
            player.x += player_kecepatan
        if kontrol[pygame.K_w] and player.y - player_kecepatan > 0:
            player.y -= player_kecepatan
        if kontrol[pygame.K_s] and player.y + player_kecepatan + player.get_height() < TINGGIL:
            player.y += player_kecepatan
        if kontrol[pygame.K_SPACE]:
            pygame.mixer.music.load("assets/shot.wav")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            player.tembak()
        for enemy in enemies[:]:
            enemy.bergerak(enemi_kecepatan)
            enemy.move_lasers(laser_kecepatan,player)
            if random.randrange(0,2*60) == 1:
                enemy.tembak()
            elif collide(enemy,player):
                player.nyawa -= 10
                enemies.remove(enemy)
                lives -= 1
            elif enemy.y + enemy.get_height() >= TINGGIL:
                lives -= 1
                enemies.remove(enemy)
###baru
        if count == 1:
            casnyawa.append(isinyawa)
            count -=1
            pass
        for nyawa in casnyawa[:]:
            nyawa.bergerak(enemi_kecepatan) #menggunakan var kec musuh
            if collide(nyawa,player):
                if level < 5:
                    player.nyawa += 25
                elif level >=5:
                    player.nyawa += 30
                    lives += 2
                pygame.mixer.music.load("assets/nyawa.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                casnyawa.remove(nyawa)

        if level == 2:
            player.pesawat_img = PESAWAT_PLAYER2
            level1.stop()
            level2.play(-2)
            level2.set_volume(0.06)
        elif level == 4:
            player.pesawat_img = PESAWAT_PLAYER3
            level2.stop()
            level4.play(-2)
            level4.set_volume(0.06)
        elif level >= 6:
            player.pesawat_img = PESAWAT_PLAYER4
            level4.stop()
            level6.set_volume(0.06)
            level6.play(-2)

        player.move_lasers(-laser_kecepatan,enemies)

#PONG
def pingpong(z):
    suara = pygame.mixer.Sound("assets/bounce.wav")
    x = z
    if x == True:
        wn = turtle.Screen()
        wn.title("Ping Pong Mad Dog")
        wn.bgcolor("green")
        wn.setup(width=800, height=600)
        wn.tracer(0)
        # Sokor
        score_a = 0
        score_b = 0

        # Pemain A
        paddle_a = turtle.Turtle()
        paddle_a.speed(0)
        paddle_a.shape("square")
        paddle_a.color("yellow")
        paddle_a.shapesize(stretch_wid=5, stretch_len=1)
        paddle_a.penup()
        paddle_a.goto(-350, 0)

        # Pemain B
        paddle_b = turtle.Turtle()
        paddle_b.speed(0)
        paddle_b.shape("square")
        paddle_b.color("red")
        paddle_b.shapesize(stretch_wid=5, stretch_len=1)
        paddle_b.penup()
        paddle_b.goto(350, 0)

        # Ball
        ball = turtle.Turtle()
        ball.speed(0)
        ball.shape("circle")
        ball.color("blue")
        ball.penup()
        ball.goto(0, 0)
        ball.dx = 2
        ball.dy = -2

        pen = turtle.Turtle()
        pen.speed(0)
        pen.color("black")
        pen.penup()
        pen.hideturtle()
        pen.goto(0, 260)
        pen.write("Pemain A: 0  Pemain B: 0", align="center", font=("Courier", 24, "normal"))


        def paddle_a_up():
            y = paddle_a.ycor()
            y += 20
            paddle_a.sety(y)


        def paddle_a_down():
            y = paddle_a.ycor()
            y -= 20
            paddle_a.sety(y)


        def paddle_b_up():
            y = paddle_b.ycor()
            y += 20
            paddle_b.sety(y)


        def paddle_b_down():
            y = paddle_b.ycor()
            y -= 20
            paddle_b.sety(y)


        wn.listen()
        wn.onkeypress(paddle_a_up, "w")
        wn.onkeypress(paddle_a_down, "s")
        wn.onkeypress(paddle_b_up, "Up")
        wn.onkeypress(paddle_b_down, "Down")

        while True:
            time.sleep(0.01)
            wn.update()

            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            if ball.ycor() > 290:
                ball.sety(290)
                ball.dy *= -1
                suara.play()

            if ball.ycor() < -290:
                ball.sety(-290)
                ball.dy *= -1
                suara.play()

            if ball.xcor() > 390:
                ball.goto(0, 0)
                ball.dx *= -1
                score_a += 1
                pen.clear()
                pen.write("Pemain A: {}  Pemain B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

            if ball.xcor() < -390:
                ball.goto(0, 0)
                ball.dx *= -1
                score_b += 1
                pen.clear()
                pen.write("Pemain A: {}  Pemain B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

            if (ball.xcor() > 340 and ball.xcor() < 350) and (
                    ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
                ball.setx(340)
                ball.dx *= -1
                suara.play()

            if (ball.xcor() < -340 and ball.xcor() > -350) and (
                    ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
                ball.setx(-340)
                ball.dx *= -1
                suara.play()



def main_menu():
    judul_font = pygame.font.SysFont("comicsans",50)
    game_font =  pygame.font.SysFont('iconfont',30)
    run = True
    while run:
        kontrol = pygame.key.get_pressed()
        LAYAR.blit(BACKGRNDAWAL,(0,0))
        judul_label = game_font.render("WELCOME TO GAMEE",1,(255,255,255))
        game1 = game_font.render("Press X Untuk SpaceShooter",1,(255,255,255))
        game2 = game_font.render("Press Y Untuk PongPong",1,(255,255,255))
        LAYAR.blit(judul_label,((LEBARL/2 - judul_label.get_width()/2 )+ 20,200))
        LAYAR.blit(game1,(LEBARL/2 - judul_label.get_width()/2,270))
        LAYAR.blit(game2,(LEBARL/2 - judul_label.get_width()/2,300))
        pygame.display.update()
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
              run = False
           elif kontrol[pygame.K_x]:
               mainlagu.stop()
               spaceshooter()
               mainlagu.play(-2)
           elif kontrol[pygame.K_y]:
                mainlagu.stop()
                # PingPong Ngebug
                try:
                    pingpong(True)
                except:
                    pass
                mainlagu.play(-2)
    pygame.quit()


main_menu()