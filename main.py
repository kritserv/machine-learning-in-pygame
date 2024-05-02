import numpy as np
import moderngl
import pygame as pg
from time import time

pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.display.set_caption("game_title")

window_size = (640, 360)

screen = pg.display.set_mode(
	(window_size), 
	pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF
	)

display = pg.Surface(
	(window_size)
	)

from src import ctx, \
	quad_buffer, \
	vert_shader, \
	frag_shader, \
	program, \
	render_object, \
	surf_to_texture, \
	Player, \
	Computer, \
	Menu

pg.display.set_icon(
	pg.image.load(
		"asset/icon.png"
		).convert_alpha()
	)

def blit_text(text, font, col, x_y_pos):
	text_image = font.render(text, True, col)
	display.blit(text_image, x_y_pos)

def check_type(event):
	keydown, keyup, quit= False, False, False
	if event.type == pg.KEYDOWN:
		keydown = True
	elif event.type == pg.KEYUP:
		keyup = True
	elif event.type == pg.QUIT:
		quit = True
	return keydown, keyup, quit

def check_arrow_key(event, keydown, keyup):
	up, down, left, right = False, False, False, False
	if keydown:
		if event.key == pg.K_UP:
			up = True
		elif event.key == pg.K_DOWN:
			down = True
		elif event.key == pg.K_LEFT:
			left = True
		elif event.key == pg.K_RIGHT:
			right = True
	elif keyup:
		if event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
			up, down, left, right = False, False, False, False

	return up, down, left, right

def check_interact(event, keydown, keyup):
	interact = False
	if keydown:
		if event.key == pg.K_RETURN:
			interact = True
	elif keyup:
		if event.key == pg.K_z or event.key == pg.K_SPACE:
			interact = True

	return interact

def check_cancel(event, keydown, keyup):
	cancel = False
	if keydown:
		if event.key == pg.K_ESCAPE:
			cancel = True
	elif keyup:
		if event.key == pg.K_x or event.key == pg.K_KP0:
			cancel = True

	return cancel

def check_quit_game_event(event, quit, keydown):
	run = True
	if quit:
		run = False
	if keydown:
		if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
			run = False
		elif event.key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
			run = False

	return run

def main():

	player = Player(display.get_width()/2-16, display.get_height()/2-24)
	computer = Computer(display.get_width()/2-16, display.get_height()/10)
	computer_collision = pg.Rect([display.get_width()/2-16, display.get_height()/10, 32, 64])
	menu = Menu()

	clock = pg.time.Clock()

	black = pg.Color("grey0")
	white = pg.Color("grey90")
	red = pg.Color("crimson")

	font = pg.font.Font(
		"asset/fonts/PixeloidSans-mLxMm.ttf", 
		9
		)

	result_font = pg.font.Font(
		"asset/fonts/PixeloidSans-mLxMm.ttf", 
		10
		)

	cap_fps = True
	run = True

	prev_time = time()
	while run:

		dt = time() - prev_time
		prev_time = time()
		if cap_fps:
			clock.tick(100)
		else:
			clock.tick()

		# Input

		for event in pg.event.get():
			keydown, keyup, quit = check_type(event)
			interact = check_interact(event, keydown, keyup)
			cancel = check_cancel(event, keydown, keyup)
			run = check_quit_game_event(event, quit, keydown)
			up, down, left, right = check_arrow_key(event, keydown, keyup)

		key = pg.key.get_pressed()

		# Logic

		if not menu.open:
			player.update(key, dt, display)
			computer.update(player, computer_collision)

		menu.update(dt, interact, cancel, computer, up, down, left, right)

		# Graphic

		display.fill(white)

		menu.draw_result(display, blit_text, result_font)
		blit_text(
			"Use Arrow Key To Move\nEnter, Z, Space To Interact\nESC, Numpad0 To Cancel\n\nPut Dataset .csv file in data directory\nProgram Will Automaticly\nSelect Last Column As Target\nAnd The Rest Will Be Features", 
			font, 
			black, 
			(420, 260)
			)

		display.blit(computer.image, (computer.pos))
		display.blit(player.image, (player.pos))

		menu.draw(display, blit_text, font)

		fps = str(clock.get_fps() // 0.1 / 10)

		blit_text(f"fps = {fps}", font, black, (540, 5))

		
		frame_tex = surf_to_texture(display)
		frame_tex.use(0)
		program["tex"] = 0
		render_object.render(
			mode=moderngl.TRIANGLE_STRIP
			)

		pg.display.flip()

		frame_tex.release()

	pg.quit()


if __name__ == "__main__":
	main()