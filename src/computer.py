import pygame as pg

class Computer(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.player_collide = False

		self.load_sprite()

		self.rect = self.image.get_rect()
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.pos[0] = x
		self.pos[1] = y

	def load_sprite(self):
		image = pg.image.load("asset/img/computer.png")
		image = pg.transform.scale(image, (48, 64))
		self.image = image.convert_alpha()

	def update(self, player, computer_collision):
		if player.rect.colliderect(computer_collision):
			self.player_collide = True
		else:
			self.player_collide = False