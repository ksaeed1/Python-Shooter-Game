import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Shooter')
pygame.display.set_caption("Main Menu")

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
game_paused = False
menu_state = "main"
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 1
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

#define player action variables
moving_left = False
moving_right = False
shoot = False

#load music and sounds
pygame.mixer.music.load('audio/arabic_desert.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.mp3')
jump_fx.set_volume(0.4)
shot_fx = pygame.mixer.Sound('audio/gunshot.mp3')
shot_fx.set_volume(0.09)


#load images
#button images
start_img = pygame.image.load("images/start_img.png").convert_alpha()
exit_img = pygame.image.load("images/exit_img.png").convert_alpha()
restart_img = pygame.image.load("images/restart_img.png").convert_alpha()

resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()


#background
pine1_img = pygame.image.load('img/background/pine1.png').convert_alpha() 
ground_img = pygame.image.load('img/background/ground.png').convert_alpha() 
desert_img = pygame.image.load('img/background/desert.png').convert_alpha() 
sky_cloud_img = pygame.image.load('img/background/sky_cloud.png').convert_alpha() 


#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha() 
#pickupboxes 
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha() 
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha() 
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img
}


#define colours
BG = (251, 147, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0 , 0)
PINK = (235, 65, 54)

#define font here

font = pygame.font.Font(None, 32)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
	screen.fill(BG)
	screen.blit(sky_cloud_img, (0,0))
	screen.blit(desert_img, (0, SCREEN_HEIGHT - desert_img.get_height() - 125))
	screen.blit(ground_img, (0, SCREEN_HEIGHT - ground_img.get_height() - 15))

#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data

class Menu:
    def __init__(self):
        self.game_paused = True  # Start with menu open
        self.menu_state = "main"

        #button class
class Button():
  def __init__(self, x, y, image, scale):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False

  def draw(self, surface):
    action = False

    #get mouse position
    pos = pygame.mouse.get_pos()

    #check mouseover and clicked conditions
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        
        action = True
        self.clicked = True

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    #draw button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action


class Soldier(pygame.sprite.Sprite):
	def __init__(self, x, y, scale,char_type, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.ammo = ammo
		self.start_ammo = ammo
		self.shoot_cooldown = 0
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#create ai specific variables
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0

		#load all images for players
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:

			#reset temporary list of images
			temp_list = []
			#count number of files in the folder
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png'). convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect() #controlls positions and collisions
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self):
		self.update_animation()
		self.check_alive()
		#update cooldown
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0
		dx = 0
		dy = 0

		#assign moving variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		#apply gravity
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		#check for collision 
		for tile in world.obstacle_list:
			#check collision in the x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
		#check for collision in the y direction
			if tile[1].colliderect(self.rect.x + dy, self.rect.y, self.width, self.height):
			#check if below the ground, i.e., jumping
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e., falling
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom

		#check for collision with water
		level_complete = False
		if pygame.sprite.spritecollide(self, water_group, False):
			self.health = 0

		#check for collision with exit
		if pygame.sprite.spritecollide(self, exit_group, False):
			level_complete = True

		#check if fallen off the map
		if self.rect.bottom > SCREEN_HEIGHT:
			self.health = 0


		if self.char_type == 'player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll based on player position
		if self.char_type == 'player':
			if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
				self.rect.x -= dx 
				screen_scroll = -dx

		return screen_scroll, level_complete

	def shoot(self):
	    if self.shoot_cooldown == 0 and self.ammo > 0:
	        self.shoot_cooldown = 20
	        bullet = Bullet(
	            self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),
	            self.rect.centery,
	            self.direction,
	            "player" if self.char_type == "player" else "enemy",
	        )
	        bullet_group.add(bullet)
	        self.ammo -= 1
	        shot_fx.play()


	def ai(self):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0) #0 is idle
				self.idling = True
				self.idling_counter = 50
				#check if the ai is near the player
			if self.vision.colliderect(player.rect):
				#stop running and face the player
				self.update_action(0) #0 is idle
				#shoot
				self.shoot()
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_moving_right = True
					else:
						ai_moving_right = False
					ai_moving_left = not ai_moving_right
					self.move(ai_moving_left, ai_moving_right)
					self.update_action(1) #1 to run
					self.move_counter += 1
					#update ai vision as enemy moves
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
					

					if self.move_counter > TILE_SIZE:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0: 
							self.idling = False


		#scroll
		self.rect.x += screen_scroll

	def update_animation(self):
		#update the animation
		ANIMATION_COOLDOWN = 100
		#update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if animation has run out, then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0 


	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animation settings
			self.frame_index = 0 
			self.update_time = pygame.time.get_ticks()


	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)
					elif tile >= 9 and tile <= 10:
						water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <= 14:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 15: #create player
						player = Soldier(x * TILE_SIZE, y * TILE_SIZE, 0.3, 'player', 5, 20)
						health_bar = HealthBar(10, 10, player.health, player.health)
					elif tile == 16: #create enemy
					 	enemy = Soldier(x * TILE_SIZE, y * TILE_SIZE, 0.3, 'enemy', 2, 20)
					 	enemy_group.add(enemy)
					elif tile == 17: #create ammo box
						item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 18:
						item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 19:
						item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 20: #create exit
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)

		return player, health_bar

	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll
			screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		#scroll
		self.rect.x += screen_scroll
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			#delete the item box
			self.kill()


class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x  
		self.y = y  
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.owner = owner  # Track who fired the bullet (player or enemy)

    def update(self):
        # Move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll

        # Check if the bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Check collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with characters
        if self.owner == "player":
            # Bullet fired by player should not hit the player
            for enemy in enemy_group:
                if pygame.sprite.collide_rect(self, enemy) and enemy.alive:
                    enemy.health -= 35
                    self.kill()
        elif self.owner == "enemy":
            # Bullet fired by enemy should not hit other enemies
            if pygame.sprite.collide_rect(self, player) and player.alive:
                player.health -= 2
                self.kill()


class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed 
		self.fade_counter = 0 

	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1: #whole screen fade
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))

		if self.direction == 2: #vertical screen fade down
			pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete
			
#create screen Fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)


#create buttons
button_spacing = 80  # Space between buttons

start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

resume_button = button.Button(304, 100, resume_img, 1)
options_button = button.Button(297, 100 + button_spacing, options_img, 1)
video_button = button.Button(226, 100 + 3 * button_spacing, video_img, 1)
audio_button = button.Button(225, 100 + 4 * button_spacing, audio_img, 1)
keys_button = button.Button(246, 100 + 5 * button_spacing, keys_img, 1)
back_button = button.Button(332, 100 + 6 * button_spacing, back_img, 1)
quit_button = button.Button(336, 100 + 2 * button_spacing, quit_img, 1)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range (ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data [x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)



#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate (row):
			world_data[x][y] = int(tile)


world = World()
player, health_bar = world.process_data(world_data)



run = True
while run:


	clock.tick(FPS)


	if game_paused == True:
		#draw menu
		screen.fill(BG)
		if menu_state == "main":
			if resume_button.draw(screen):
				game_paused = False
			if options_button.draw(screen):
				menu_state = "options"
			if quit_button.draw(screen):
				run = False
			if menu_state == "options":
				if video_button.draw(screen):
					print("Video Settings")
				if keys_button.draw(screen):
					print("Change Key Bindings")
				if back_button.draw(screen):
					menu_state = "main"
		else:
			draw_text("Press p to pause", font, TEXT_COL, 160, 250)
		

	if start_game == False:
		screen.fill(BG)
		if start_button.draw(screen):
			start_game = True
			start_intro = True
		if exit_button.draw(screen):
			run = False

	else:	#update background
		draw_bg()

			#draw world map
		world.draw()
			#show player health
		health_bar.draw(player.health)

			#show ammo
		draw_text('AMMO: ', font, WHITE, 10, 35)
		for x in range(player.ammo):
				screen.blit(bullet_img, (90 + (x * 10), 40 ))

		player.update()
		player.draw()

		for enemy in enemy_group:
				enemy.ai()
				enemy.update()
				enemy.draw()


			#update and draw groups
		bullet_group.update()
		item_box_group.update()
		decoration_group.update()
		water_group.update()
		exit_group.update()
		bullet_group.draw(screen)
		item_box_group.draw(screen)
		decoration_group.draw(screen)
		water_group.draw(screen)
		exit_group.draw(screen)

		#show intro
		if start_intro == True:
			if intro_fade.fade():
				start_intro = False
				intro_fade.fade_counter = 0

			#update player actions
		if player.alive:
				#shooting bullets
			if shoot:
					player.shoot()
			if player.in_air:
					player.update_action(2) #2 to jump
			elif moving_left or moving_right:
					player.update_action(1) #1 means run
			else: 
					player.update_action(0) #0 is idle
			screen_scroll, level_complete = player.move(moving_left, moving_right)
			bg_scroll -+ screen_scroll
			#check if player has completed the level
			if level_complete:
				start_intro = True
				level += 1
				bg_scroll = 0
				world_data = reset_level()
				if level <= MAX_LEVELS:
					#load level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate (row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)

		else:
			screen_scroll = 0
			if death_fade.fade():
				if restart_button.draw(screen):
					death_fade.fade_counter = 0
					start_intro = True
					bg_scroll = 0
					world_data = reset_level()
					#load level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate (row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)



	for event in pygame.event.get(): #event handler. i.e., things such as mouse clicks
		#to quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
				jump_fx.play()
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					game_paused = True
					if event.type == pygame.QUIT:
						run = False

		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False
			

	pygame.display.update()

pygame.quit()
