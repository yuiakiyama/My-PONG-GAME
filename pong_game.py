import pyxel


SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_PLAYER1_WIN = 2
SCENE_PLAYER2_WIN = 3

class App:
    def __init__(self):
        pyxel.init(450, 270, fps=60)
        self.player_L_y = pyxel.height // 2 - 25
        self.player_L_x = 8
        self.player_L_score = 0

        self.player_R_y = pyxel.height // 2 - 25
        self.player_R_x = pyxel.width - 18
        self.player_R_score = 0

        self.player_width = 10
        self.player_heigth = 50
        self.player_speed = 3

        self.ball_x = pyxel.width // 2
        self.ball_y = pyxel.height // 2
        self.ball_radius = 3
        self.ball_speed_x = 1.75
        self.ball_speed_y = 2
        self.ball_col = 7

        self.scene = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def ctext(self,tx,ty,msg,col):
        cx = pyxel.width / 2
        cy = pyxel.height / 2
        num = len(msg)
        x = cx - (num*4)/2
        y = cy - 4
        pyxel.text(x+tx,y+ty,msg,col)

        return
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.restart_game()
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_PLAYER1_WIN or self.scene == SCENE_PLAYER2_WIN:
            self.update_gameover_scene()


    def reset(self):
        self.ball_x = pyxel.width // 2
        self.ball_y = pyxel.height // 2
        self.ball_speed_y = 2
        self.ball_col = 7
        self.player_speed = 3
        if pyxel.rndi(1, 2) == 1 :
            self.ball_speed_y = -self.ball_speed_y
    def R_ball(self):
        self.ball_speed_x = -1.5
    def L_ball(self):
        self.ball_speed_x = 1.5

    def restart_game(self):
        self.player_L_y = pyxel.height // 2 - 25
        self.player_L_x = 8
        self.player_L_score = 0

        self.player_R_y = pyxel.height // 2 - 25
        self.player_R_x = pyxel.width - 18
        self.player_R_score = 0

        self.player_speed = 3

        self.ball_x = pyxel.width // 2
        self.ball_y = pyxel.height // 2
        self.ball_col = 7
        self.scene = SCENE_TITLE

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        self.update_player_L()
        self.update_player_R()
        self.update_ball()
        self.update_score()
        if self.player_L_score >= 5:
            self.scene = SCENE_PLAYER1_WIN
        elif self.player_R_score >= 5:
            self.scene = SCENE_PLAYER2_WIN

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.restart_game()

    def update_player_L(self):
        if pyxel.btn(pyxel.KEY_W):
            self.player_L_y -=  self.player_speed
        elif pyxel.btn(pyxel.KEY_S):
            self.player_L_y += self.player_speed
        if self.player_L_y <= 0:
            self.player_L_y = 0
        elif self.player_L_y >= 220:
            self.player_L_y = 220

    def update_player_R(self):
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_R_y +=  self.player_speed
        elif pyxel.btn(pyxel.KEY_UP):
            self.player_R_y -= self.player_speed
        if self.player_R_y <= 0:
            self.player_R_y = 0
        elif self.player_R_y >= 220:
            self.player_R_y = 220

    def update_ball(self):
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        if self.ball_x + 3 >= pyxel.width or self.ball_x - 3 <= 0:
            self.ball_speed_x = -self.ball_speed_x
        if self.ball_y + 3 >= pyxel.height or self.ball_y - 3 <= 0:
            self.ball_speed_y = -self.ball_speed_y

        if (self.ball_x <= self.player_L_x + self.player_width and self.player_L_y <= self.ball_y <= self.player_L_y + self.player_heigth
        ):
            self.ball_speed_x = -self.ball_speed_x
            self.ball_col = 8
            if self.ball_speed_x >= 0:
                self.player_speed += 0.1
                self.ball_speed_x += 0.15
                self.ball_speed_y += 0.1
            else:
                self.player_speed += 0.1
                self.ball_speed_x -= 0.15
                self.ball_speed_y -= 0.1

        elif(self.ball_x + self.ball_radius >= self.player_R_x and self.player_R_y <= self.ball_y <= self.player_R_y + self.player_heigth
        ):
            self.ball_speed_x = -self.ball_speed_x
            self.ball_col = 5
            if self.ball_speed_x >= 0:
                self.player_speed += 0.1
                self.ball_speed_x += 0.15
                self.ball_speed_y += 0.1
            else:
                self.player_speed += 0.1
                self.ball_speed_x -= 0.15
                self.ball_speed_y -= 0.1

    def update_score(self):
        if self.ball_x <= self.ball_radius:
            self.player_R_score += 1
            self.reset()
            self.R_ball()
        elif self.ball_x >= pyxel.width - self.ball_radius:
            self.player_L_score += 1
            self.reset()
            self.L_ball()

    def draw(self):
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_PLAYER1_WIN:
            self.draw_player1_win_scene()
        elif self.scene == SCENE_PLAYER2_WIN:
            self.draw_player2_win_scene()

    def draw_title_scene(self):
        self.ctext(0, -20, "PONG GAME", 7)
        self.ctext(0, 10, "- PRESS SPECCCCE -", 7)

    def draw_play_scene(self):
        pyxel.cls(0)
        pyxel.rect(self.player_L_x, self.player_L_y, self.player_width, self.player_heigth, 8)
        pyxel.rect(self.player_R_x , self.player_R_y, self.player_width, self.player_heigth, 5)
        pyxel.circ(self.ball_x, self.ball_y, self.ball_radius, self.ball_col)
        pyxel.text(pyxel.width // 2 - 10, 4, f"{self.player_L_score} - {self.player_R_score}", 7)

    def draw_player1_win_scene(self):
        self.ctext(0, -80, "PLAYER1 WON!", 8)
        self.ctext(0, -60, "- PRESS R to restart -", 7)

    def draw_player2_win_scene(self):
        self.ctext(0, -80, "PLAYER2 WON!", 5)
        self.ctext(0, -60, "- PRESS R to restart -", 7)

App()
