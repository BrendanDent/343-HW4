from random import randint
import observer
#random class taken from example: https://pythonspot.com/random-numbers/
#"multidemnsional array" from https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array-in-python
#this class controls the game
class game:
	def __init__(self):
		p = player()
		n = neighborhood(2,1, p)
		while n.num_monsters != 0:
			n.clear_house()
		print "You win"	
#this class controls the neighborhood which is also the array of houses
# @param observer.Observer this is the observer for the home class
class neighborhood(observer.Observer):
        def __init__(self, row, col, player):
                self.num_rows = row
                self.num_cols = col
                self.p = player
		self.player_row = 0
                self.player_col = 0
                self.num_monsters = 0
                self.grid = [[0 for x in range(col)] for y in range(row)]
		for i in range(row):
			for j in range(col):
				self.grid[i][j] = home(self.p, self)
				self.num_monsters += self.grid[i][j].get_num_monsters()
        def move_player(self):
		print "This house is clear."
		print "These houses still have monsters in them:"
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				if self.grid[i][j].num_monsters != 0:
					print str(i) + "," + str(j)
		self.player_row = input("Choose a house to go to")
		self.player_col = input()

        def clear_house(self):
                self.grid[self.player_row][self.player_col].clear_house()
        def observer_update(self,observer, sender):
                self.num_monsters -= self.grid[self.player_row][self.player_col].starting_monsters
                if self.num_monsters != 0:
                        self.move_player()
# this class controls the home interactions which include fighing monsters
class home():
	def __init__(self, player, observerr):
                self.o = observer.Observable()
                self.o.add_observer(observerr)
                self.p = player
		monsters = randint(0,10)
		self.num_monsters = 0
		self.num_people = 0
		self.monster_list = []
		for i in range(monsters):
			mon_type = randint(0,4)
			if mon_type == 0:
				self.num_people += 1			
				self.monster_list.append(person(self))
			elif mon_type == 1:
				self.num_monsters += 1
				self.monster_list.append(zombie(self))
			elif mon_type == 2:
				self.num_monsters += 1
				self.monster_list.append(vampire(self))
			elif mon_type == 3:
				self.num_monsters += 1
				self.monster_list.append(ghoul(self))
			elif mon_type == 4:
				self.num_monsters += 1
				self.monster_list.append(werewolf(self))
		self.starting_monsters = self.num_monsters
	def take_turn(self):
		print "In the house are still " + str(self.num_monsters) + " monsters left"
                print "Your health is currently " + str(self.p.health)
		print "The house contains: "
                for npc in self.monster_list:
			print npc.type
                        print npc.health
                self.p.checkWeapons()
		weapon = raw_input("Which weapon will you attack with? ")
		while weapon not in self.p.weapons:
			weapon = raw_input("Invalid choice. Choose again")
		damage = self.p.attack(weapon)
		for npc in self.monster_list:
                        if weapon in npc.special:
                                taken_damage = damage * npc.special_multi
                        else:
                                taken_damage = damage
			npc.take_damage(taken_damage)
			self.p.take_damage(npc.attack)
	def get_num_monsters(self):
		return self.num_monsters
	def clear_house(self):
                while self.num_monsters != 0:
			self.take_turn()
                       
	def observer_update(self,observer,sender):
                self.monster_list.remove(sender)
                self.monster_list.append(person(self))
		self.num_monsters -= 1
		self.num_people += 1
		if self.num_monsters == 0:
			self.o.update(self)

		
		
#this class is the parent of all npcs. It controls all of the npc damage, attacks and deaths
class npc():
	def __init__(self, npc_type, atk, hp, spc, multi, observerr):
                self.type = npc_type
                self.attack = atk
                self.health = hp
                self.special = spc
                self.special_multi = multi
		self.o = observer.Observable()
                self.o.__init__()
                self.o.add_observer(observerr)           
                
	def take_damage(self, damage):
		self.health -= damage
                if self.health <= 0:
                        print self.type + " has been turned back into a human"
			self.o.update(self)


class person(npc) :
	def __init__(self, observer):
		npc.__init__(self,"person", -1, 100, [ "HersheyKisses", "SourStraws", "ChocolateBars", "NerdBombs"], 0, observer)

class zombie(npc) :
	def __init__(self, observer) :
		npc.__init__(self, "zombie", randint(0,10), randint(50,100), ["SourStraws"], 2, observer)

class vampire(npc) :
	def __init__(self, observer) :
		npc.__init__(self, "vampire", randint(10, 20), randint(100, 150), ["ChocolateBars"], 0, observer)

class ghoul(npc) :
	def __init__(self, observer) :
		npc.__init__(self, "ghoul", randint(15,30), randint(40,80), ["NerdBombs"], 5, observer)

class werewolf(npc) :
	def __init__(self, observer) :
		npc.__init__(self, "werewolf", randint(0,40), 200, ["ChocolateBars", "SourStraws"], 0, observer)

#this contols the player character. It determines the player health and attack
class player():
	def __init__(self):
		self.weapons = []
                weapon_randoms = []
		self.health = randint(100,125)
                for i in range (10):
			weapon_randoms.append(randint(0,3))
		for i in weapon_randoms:
			if i == 0:
				self.weapons.append("HersheyKisses")
			elif i == 1:
				self.weapons.append("SourStraws")
				self.weapons.append("SourStraws")
			elif i == 2:
				self.weapons.append("ChocolateBars")
				self.weapons.append("ChocolateBars")
				self.weapons.append("ChocolateBars")
				self.weapons.append("ChocolateBars")
			elif i == 3:
				self.weapons.append("NerdBombs")

	def attack(self, weapon):
		multi = 0
		if weapon == "HersheyKisses":
                        multi = 1
			
		elif weapon == "SourStraws":
                        multi = randint(100,175)/100
                        self.weapons.remove("SourStraws")
			
		elif weapon == "ChocolateBars":
                        multi = randint(200,240)/100
                        self.weapons.remove("ChocolateBars")
			
		elif weapon == "NerdBombs":
                        multi = randint(350,500)/100
                        self.weapons.remove("NerdBombs")
		damage = randint(10, 20)
		return damage * multi
			
	def checkWeapons(self):
		for weapon in self.weapons:
			print weapon
	def take_damage(self, damage):
		self.health -= damage
		if self.health <= 0:
			print "You have died"
			exit()

#this starts the game
g = game()
