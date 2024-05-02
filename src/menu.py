import numpy as np
import pygame as pg
import os

from .corr import correlation_analysis
from .lr import linear_regression
from .dt import decision_tree
from .kmns import kmeans

class Menu:
	def __init__(self):
		self.open = False
		self.background = pg.Surface((220, 152))
		self.background.set_alpha(200)

		self.black = pg.Color("grey0")
		self.background.fill(self.black)

		self.white = pg.Color("grey100")
		self.aqua = pg.Color("aqua")

		self.main_options = ["Correlation Analysis", "Supervised ML", "Unsupervised ML", "Cancel"]
		self.data_options = {}
		self.data_names = []
		self.load_data()

		self.select_data_options = [name for name in self.data_options]
		self.select_data_options.append("Back")

		self.super_options = ["Linear Regression", "Decision Tree", "Back"]
		self.unsuper_options = ["KMeans", "Back"]
		self.selected = 0
		self.cooldown = 10

		self.options = self.main_options
		self.point_to = self.options[0]
		self.previous_options = []

		self.select_function = ""

		self.latest_result = []

	def load_data(self):
		for filename in os.listdir("data"):
			if filename.endswith(".csv"):
				file_path = os.path.join("data", filename)
				data = np.genfromtxt(file_path, delimiter=",", dtype=None, encoding=None)
				key = os.path.splitext(filename)[0]
				self.data_options[key] = data
				self.data_names.append(key)

	def draw(self, display, blit_text, font):
		if self.open:
			display.blit(self.background, (8, 8))
			y = 16
			for i, option in enumerate(self.options):
				if i == self.selected:
					blit_text(f"> {option}", font, self.aqua, (16, y))
				else:
					blit_text(option, font, self.white, (16, y))
				y += 16

	def draw_result(self, display, blit_text, font):
		if self.latest_result:
			blit_text(self.latest_result, font, self.black, (8, 100))

	def reset_select(self):
		self.selected = 0
		self.cooldown = 20

	def make_prev_options(self):
		self.previous_options = self.options

	def update(self, dt, interact, cancel, computer, up, down, left, right):

		if computer.player_collide:
			if interact:
				if self.cooldown <= 0 and self.open == False:
					self.open = True
					self.cooldown = 30
					self.previous_options = self.main_options.copy()
			elif cancel:
				self.options = self.main_options.copy()
				self.open = False
				self.cooldown = 1

		if self.open:
			if self.cooldown <= 0:
				if up:
					if self.selected > 0:
						self.selected -= 1
					self.cooldown = 10

				elif down:
					if self.selected < len(self.options)-1:
						self.selected += 1
					self.cooldown = 10

			self.point_to = self.options[self.selected]

			if interact:
				if self.cooldown <= 0:
					if self.point_to == "Correlation Analysis":
						self.select_function = "Correlation Analysis"
						self.make_prev_options()
						self.options = self.select_data_options
						self.reset_select()
					elif self.point_to == "Supervised ML":
						self.make_prev_options()
						self.options = self.super_options
						self.reset_select()
					elif self.point_to == "Linear Regression":
						self.select_function = "Linear Regression"
						self.make_prev_options()
						self.options = self.select_data_options
						self.reset_select()
					elif self.point_to == "Decision Tree":
						self.select_function = "Decision Tree"
						self.make_prev_options()
						self.options = self.select_data_options
						self.reset_select()
					elif self.point_to == "Unsupervised ML":
						self.make_prev_options()
						self.options = self.unsuper_options
						self.reset_select()
					elif self.point_to == "KMeans":
						self.select_function = "KMeans"
						self.make_prev_options()
						self.options = self.select_data_options
						self.reset_select()
					elif self.point_to == "Back":
						if self.previous_options:
							self.options = self.previous_options
							self.reset_select()
						if self.options == self.previous_options:
							self.options = self.main_options.copy()
							self.reset_select()
					elif self.point_to == "Cancel":
						self.options = self.main_options.copy()
						self.open = False
						self.reset_select()

					for data_name in self.data_names:
						if self.point_to == data_name:
							if self.select_function == "Correlation Analysis":
								self.latest_result = correlation_analysis(self.data_options[data_name])
								self.reset_select()
							elif self.select_function == "Linear Regression":
								self.latest_result = linear_regression(self.data_options[data_name])
								self.reset_select()
							elif self.select_function == "Decision Tree":
								self.latest_result = decision_tree(self.data_options[data_name])
								self.reset_select()
							elif self.select_function == "KMeans":
								self.latest_result = kmeans(self.data_options[data_name])
								self.reset_select()
							else:
								self.reset_select()
						else:
							self.reset_select()

		if self.cooldown >= 0:
			self.cooldown -= 100 * dt