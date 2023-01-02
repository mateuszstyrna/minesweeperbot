from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class MineSweeperBot():
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.delay = 15
		self.maxX = 8
		self.maxY = 8
		self.bombs = []
		self.toBeSkipped = []
		self.login = "Login"
		self.password = "password"

	def randomCell(self):
		X = random.randint(0, self.maxX)
		Y = random.randint(0, self.maxY)
		if ("hd_closed" in self.driver.find_element(By.ID, f"cell_{X}_{Y}").get_attribute("class").split() and self.driver.find_element(By.ID, f"cell_{X}_{Y}") not in self.bombs):
			cell = self.driver.find_element(By.ID, f"cell_{X}_{Y}")
		else:
			return self.randomCell()
		return cell

	def didLost(self):
		try:
			self.driver.find_element(By.CLASS_NAME, "hd_type11")
			return True
		except Exception as e:
			return False

	def didWon(self):
		try:
			self.driver.find_element(By.CLASS_NAME, "hd_top-area-face-win")
			exit("Easy B-)")
		except Exception as e:
			return False

	def markAsBomb(self, cell):
		print(f"There is a bomb: {cell.get_attribute('data-x')}, {cell.get_attribute('data-y')}")
		self.bombs.append(cell)
		self.didWon()
		self.lookForSafeOnes()
		return self.bombs

	def howManyBombsAround(self, classes):
		classes = classes.split()
		if ("hd_type0" in classes):
			return 0
		if ("hd_type1" in classes):
			return 1
		if ("hd_type2" in classes):
			return 2
		if ("hd_type3" in classes):
			return 3
		if ("hd_type4" in classes):
			return 4
		if ("hd_type5" in classes):
			return 5
		if ("hd_type6" in classes):
			return 6
		if ("hd_type7" in classes):
			return 7
		if ("hd_type8" in classes):
			return 8

	def findBombs(self, bombsQty, cell):
		X = int(cell.get_attribute("data-x"))
		Y = int(cell.get_attribute("data-y"))

		neighbors = self.getNeighbors(cell)
		susNeighbors = self.getSusNeighbors(neighbors)

		#skip if every neighbor is safe and never check it again
		if (len(susNeighbors) == 0):
			self.toBeSkipped.append(cell)
			return True

		#if its only neighbors are known to be bombs then do not check this cell ever again
		i = 0
		for susNeighbor in susNeighbors:
			if (susNeighbor in self.bombs):
				i += 1
		if (i == len(susNeighbors)):
			self.toBeSkipped.append(cell)

		#if bobms quantity is equal to suspect cells then these are bombs
		didFindBomb = False
		if (bombsQty == len(susNeighbors)):
			for susNeighbor in susNeighbors:
				if (susNeighbor not in self.bombs):
					self.markAsBomb(susNeighbor)
					didFindBomb = True
		if (didFindBomb):
			self.lookForSafeOnes()

		#if there are N bombs around and its positions are known then click any other neighbors because these are safe
		maybeSafeOnes = []
		bombsAround = 0
		for neighbor in susNeighbors:
			if (neighbor in self.bombs):
				bombsAround += 1
			else:
				maybeSafeOnes.append(neighbor)

		if (bombsAround == bombsQty): #if true then these are safe for sure
			for safeOne in maybeSafeOnes:
				print(f"I think {safeOne.get_attribute('data-x')}, {safeOne.get_attribute('data-y')} is safe.")
				safeOne.click()
				self.didWon()

		return True

	def getNeighbors(self, cell):
		X = int(cell.get_attribute("data-x"))
		Y = int(cell.get_attribute("data-y"))
		neighbors = []

		#top-left corner
		if (X == 0 and Y == 0):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))

		#bottom-right corner
		if (X == self.maxX and Y == self.maxY):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))

		#bottom-left corner
		if (X == 0 and Y == self.maxY):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))

		#top-right corner
		if (X == self.maxX and Y == 0):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))

		#first column
		if ((X == 0 and Y > 0 and Y < self.maxY)):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))

		#last column
		if ((X == self.maxX and Y > 0 and Y < self.maxY)):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))

		#first row
		if ((Y == 0 and X > 0 and X < self.maxX)):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))

		#last row
		if ((Y == self.maxY and X > 0 and X < self.maxX)):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))

		#not touching any walls
		if ((Y > 0 and Y < self.maxY) and (X > 0 and X < self.maxX)):
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y-1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X+1}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X}_{Y+1}"))
			neighbors.append(self.driver.find_element(By.ID, f"cell_{X-1}_{Y+1}"))

		return neighbors

	def getSusNeighbors(self, neighbors):
		susNeighbors = []

		for neighbor in neighbors:
			if ("hd_closed" in neighbor.get_attribute("class").split()):
				susNeighbors.append(neighbor)

		return susNeighbors

	def lookForSafeOnes(self):
		openedCells = self.driver.find_elements(By.CLASS_NAME, 'hd_opened')
		for singleCell in openedCells:
			classes = singleCell.get_attribute("class")
			if ("hd_type0" not in classes.split() and singleCell not in self.toBeSkipped):
				self.findBombs(self.howManyBombsAround(classes), singleCell)
		return True

	def logIn(self):
		self.driver.get("https://minesweeper.online/")

		#initialize form by clicking Log In
		initLoginForm = self.driver.find_element(By.CLASS_NAME, 'btn-info')
		initLoginForm.click()

		#enter login
		inputLogin = self.driver.find_element(By.ID, 'sign_in_username')
		for letter in self.login:
			inputLogin.send_keys(letter)

		#enter password
		inputPassword = self.driver.find_element(By.ID, 'sign_in_password')
		for letter in self.password:
			inputPassword.send_keys(letter)

		#there is a new btn-info button, get the new list and click the new, second one
		loginBtn = self.driver.find_elements(By.CLASS_NAME, 'btn-info')
		loginBtn[1].click()

		try:
			didLoad = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, f'//span[text()="{self.login}"]')))
			self.play()
		except TimeoutException:
			print("Loading took too much time!")


	def play(self):
		#start new game
		self.driver.get("https://minesweeper.online/new-game")

		try:
			didLoad = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'level_select_3')))

			#expert level
			#lvl = self.driver.find_element(By.ID, 'level_select_3')
			#lvl.click()
			#self.maxX = 29
			#self.maxY = 15

			cells = self.driver.find_elements(By.CLASS_NAME, 'cell')

			#play until lost or win
			while not self.didLost():
				self.lookForSafeOnes()
				cell = self.randomCell()
				print(f"I'm gonna risk it all and click: {cell.get_attribute('data-x')}, {cell.get_attribute('data-y')}")
				cell.click()
				self.didWon()
			else:
				print("Boom :( These are bombs I found: ")
				for bomb in self.bombs:
					print(f"{bomb.get_attribute('data-x')}, {bomb.get_attribute('data-y')}")
				exit("Sorry :(")

		except TimeoutException:
			print("Loading took too much time!")

bot = MineSweeperBot()
bot.logIn()