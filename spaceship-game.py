# implementation of Spaceship game - program 
# Author : hitesh agrawal
# Email: hitesha1981@gmail.com
## Please copy the below code to http://www.codeskulptor.org/
## and enjoy the game.
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
rock_group = set([])
missile_group = set([])
explosion_group = set([])
life_group = set([])
started = False
timer = 0
pause = False
grant_life = False
life_lost = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

#life image
life_info = ImageInfo([20,20], [40, 40], 20, 400)
life_image = simplegui.load_image("http://www.sunflat.net/iphone/static/images/papijumpcave/oneup.png")
life_sound = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_1-up.wav")
died_sound = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_bump.wav")
gameover_sound = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_gameover.wav")
# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        global pause
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        if pause:
           pass
        else:
            # update angle
            self.angle += self.angle_vel
        
            # update position
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

            # update velocity
            if self.thrust:
                acc = angle_to_vector(self.angle)
                self.vel[0] += acc[0] * .1
                self.vel[1] += acc[1] * .1
            
            self.vel[0] *= .99
            self.vel[1] *= .99

    def set_thrust(self, on):
        if pause:
            self.thrust = False
            ship_thrust_sound.rewind()
            pass
        else:
            self.thrust = on
            if on:
                ship_thrust_sound.rewind()
                ship_thrust_sound.play()
            else:
                ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
                  
    def shoot(self):
        global missile_group
        if pause:
            pass
        else:
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
            missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        global pause
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age,
                                           self.image_center[1]], self.image_size,
                                           self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        if pause:
            pass
        else:
            # update angle
            self.angle += self.angle_vel
            self.age += 1
      
            # update position
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < self.radius + other_object.radius:
            return True
        else:
            return False
  

def group_collide(group, other_object):
    global explosion_group, grant_life
    for item in list(group):
        if item.collide(other_object):
            group.remove(item)
            if (not grant_life):
                explosion_group.add(Sprite(item.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            else:
                grant_life = False
            return True


def group_group_collide(group1,group2):
    global score
    for item in list(group1):
        if group_collide(group2,item):
            group1.remove(item)
            score += 10
#    return collide_score
        
    

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        shoot_timer.start()

def missile_shoot():
    my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
    elif key == simplegui.KEY_MAP['space']:
        shoot_timer.stop()    
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, rock_group, missile_group, lives, score, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if started:
        pause_handler()
    elif (not started) and inwidth and inheight:
        started = True
        rock_group = set([])
        missile_group = set([])
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, started, rock_group, missile_group, explosion_group, life_group, grant_life, life_lost, my_ship, lives, score, soundtrack, pause
    
    # animiate background
    if pause:
        wtime = (time / 4) % WIDTH
        center = debris_info.get_center()
        size = debris_info.get_size()
        pass
    else:
        time += 1
        wtime = (time / 4) % WIDTH
        center = debris_info.get_center()
        size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives:", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [120, 50], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    #Draw lives board
    lives_board(canvas)  
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
    process_sprite_group(life_group,canvas)

    #check for rock and ship collide
    if group_collide(rock_group, my_ship):
        lives -= 1
        life_lost = True
        died_sound.play()

    
    #check for life and ship collide, if yes increase the life
    if group_collide(life_group, my_ship):
        lives += 1
        grant_life = True
        life_sound.play()
        
    
    # update ship and sprites
    my_ship.update()
    
    # Check missile rock collision
    group_group_collide(rock_group,missile_group)

    # draw splash screen if not started
    if (not started) or pause and (not life_lost):
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if pause and (not life_lost):
        canvas.draw_text("PAUSED", [WIDTH/2 - 100, HEIGHT/2 + 100], 50, "White")
        
    
    # If lives are 0 then set started flag to false
    if lives == 0 :
        started = False
        lives = 0
        rock_group = set([])
        life_group = set([])
        life_lost = False
        canvas.draw_text("GAMEOVER", [WIDTH/2 - 130, HEIGHT/2 + 100], 50, "Red")
#        gameover_sound.play()
        soundtrack.rewind()

    if grant_life:
        canvas.draw_text("YOU GOT A LIFE", [WIDTH/2 - 160, HEIGHT/2], 50, "WHITE")
    
    if life_lost:
        canvas.draw_text("YOU LOST A LIFE", [WIDTH/2 - 200, HEIGHT/2], 50, "RED")
        canvas.draw_text("PAUSING FOR 3 SECS", [WIDTH/2 - 160, HEIGHT/2 + 30 ], 20, "WHITE")
        pause = True
        #Calling the life_lost_timer, which will pause the screen for 3 secs once the life is lost.
        life_lost_timer.start()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship, score, started, pause, life_lost, grant_life
    rock_limit = 12
    avel_multiplier = 1
    if pause:
        pass
    else:
        if started:
            if len(rock_group) < rock_limit:
                rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
                #rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
                ## Accelerate velocity of rock if score increases past in multiple of 100
                avel_multiplyer = 0.03 * score  
                rock_vel = [(random.random() * .6 - .3) * avel_multiplyer, (random.random() * .6  - .3) * avel_multiplyer] 
                rock_avel = random.random() * .2 - .1
                #check if new rock is too nearer to the ship, 40 being rock size, do not spawn the rock
                if dist((rock_pos), my_ship.pos) < 100 + my_ship.radius:
                    pass
                else:
                    rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
# The below displays the text as the rock_swapner is run every 1 secs., the text is removed.                    
    if grant_life:
        grant_life = False
# Creates a life object with the timer
def life_spawner():
    global life_group, my_ship, started, pause
    if pause:
        pass
    elif started:
        life_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        life_vel = [random.random() * .6 - .3, random.random() * .6  - .3] 
        life_group.add(Sprite(life_pos, life_vel, 0, 0, life_image, life_info)) 

# Creates a lives board sprite object
def lives_board(canvas):
    global lives
    for x in range(lives):
        ship_center = [45, 45]
        ship_size = [90, 90]
        xaxis = x * 40
        dest_pos = [ 60 + xaxis, 80 ] 
        dest_size = [40, 40]
        dest_angle = - 1.6 
        canvas.draw_image(ship_image, ship_center, ship_size, dest_pos, dest_size, dest_angle)
        
def process_sprite_group(set_group,canvas):
    for item in list(set_group):
        item.draw(canvas)
        item.update()
        #Remove the sprite from the set once it has reached its age.
        if item.age >= item.lifespan:
            set_group.remove(item)

def pause_handler():
    global pause, soundtrack, show_string, pause_button
    if pause:
        pause = False
        soundtrack.play()
#        pause_button.set_text('Pause')
    else:
        pause = True
        soundtrack.pause()
#        pause_button.set_text('Resume')

#create a Frame unload_handler routine
def unload_timer_check():
    global soundtrack
    try:
        t = frame.get_canvas_textwidth("Lives",12)
    except:
        t = 0
    if t==0:
        print "The frame has been closed."
        soundtrack.rewind()
        unload_timer.stop()
        life_timer.stop()
        shoot_timer.stop()
        frame.stop()

def my_choice():
    return random.choice([True,False])

def life_lost_timer_handler():
    global life_lost, pause
    if life_lost and pause:
        life_lost = False
        pause = False
    life_lost_timer.stop()
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
shoot_timer = simplegui.create_timer(200.0, missile_shoot)
life_timer = simplegui.create_timer(10000.0, life_spawner)
life_lost_timer = simplegui.create_timer(3000.0, life_lost_timer_handler)
#Randomly spawn a one up sprite
if my_choice:
    life_timer.start()
else:
    life_timer.stop()
#pause_button = frame.add_button('Pause', pause_handler)
labelmain = frame.add_label('INSTRUCTIONS', 200)
label1 = frame.add_label('1) Press up arrow key to move ship forward', 200)
blank_label1 = frame.add_label('',200)
label2 = frame.add_label('2) Press lef/right arrow key to move ship left/right', 200)
blank_label2 = frame.add_label('',200)
label3 = frame.add_label('3) When Started, Click anywhere on the canvas to pause/resume the game.', 200)
blank_label3 = frame.add_label('',200)
label4 = frame.add_label('4) To continiously fire missile, keep the spacebar pressed', 200)
timer = simplegui.create_timer(1000.0, rock_spawner)
unload_timer = simplegui.create_timer(1000,unload_timer_check)
unload_timer.start()
# get things rolling
timer.start()
frame.start()

