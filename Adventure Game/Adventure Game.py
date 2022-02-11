from matplotlib.cbook import contiguous_regions
import numpy as np
from random import randrange

class AdventureGame():
    
    def __init__(self,size=(6,7),treasure_count=5,monster_count=5,sword_count=2,potion_count=3,venom_count=3):
        self.y_size= size[0]
        self.x_size= size[1]
        self.starting_coordinate = self.rand_coordinate()
        self.map = np.empty(size,dtype=str)
        self.seen_map = np.empty(size,dtype=str)
        self.died_to_monster=0
        self.died_to_venom = 0
        self.treasure_count = treasure_count
        self.monster_count = monster_count
        self.sword_count = sword_count
        self.potion_count = potion_count
        self.venom_count = venom_count
        self.point = 0
        self.sword = 0
        self.potion = 0
        self.score = 0
        self.sword_stash = 0
        self.potion_stash = 0
        self.alert_reset()
        self.passed_coordinates =np.array(self.starting_coordinate)
        self.objective_coordinates = self.rand_coordinates()
        self.treasure_coordinates = self.objective_coordinates[1:1+self.treasure_count]
        self.monster_coordinates = self.objective_coordinates[1+self.treasure_count:1+self.treasure_count+self.monster_count]
        self.sword_coordinates = self.objective_coordinates[1+self.treasure_count+self.monster_count:1+self.treasure_count+self.monster_count+self.sword_count]
        self.potion_coordinates = self.objective_coordinates[1+self.treasure_count+self.monster_count+self.sword_count:1+self.treasure_count+self.monster_count+self.sword_count+self.potion_count]
        self.venom_coordinates = self.objective_coordinates[1+self.treasure_count+self.monster_count+self.sword_count+self.potion_count:1+self.treasure_count+self.monster_count+self.sword_count+self.potion_count+self.venom_count]
        
        
    
    def rand_coordinate(self):
        y= randrange(self.x_size)
        x= randrange(self.y_size)
        coordinate=np.array([x,y])
        return coordinate
    
    def check_if_contains(self, arr, coordinate):
        flag=0
        for i in arr:
            if np.array_equal(i,coordinate):
                flag= flag+1
        if flag==0:
            return False
        else:
            return True
        
    def rand_coordinates(self):
        count=self.treasure_count + self.monster_count + self.sword_count + self.potion_count + self.venom_count

        coordinates=np.array(self.starting_coordinate)
        
        while len(coordinates)<count+1:
            new_coordinate=self.rand_coordinate()
        
            if not(self.check_if_contains(coordinates,new_coordinate)):
                coordinates = np.vstack((coordinates,new_coordinate))
        return coordinates
    
    def player_step(self,current_coordinate,direction):
        if direction == "s":
            self.passed_coordinates = np.vstack((self.passed_coordinates,current_coordinate))
            next_coordinate = np.add(current_coordinate, [1,0])
            if not(self.check_if_passed(next_coordinate)):
                if self.is_in_boundary(next_coordinate):
                    current_coordinate = next_coordinate
                    self.score += 1
                    self.check_current_tile()
            else:
                self.passed_alert=1
        elif direction == "w":
            self.passed_coordinates = np.vstack((self.passed_coordinates,current_coordinate))
            next_coordinate = np.add(current_coordinate, [-1,0])
            if not(self.check_if_passed(next_coordinate)):
                if self.is_in_boundary(next_coordinate):
                    current_coordinate = next_coordinate
                    self.score += 1
                    self.check_current_tile()
            else:
                self.passed_alert=1
        elif direction == "d":
            self.passed_coordinates = np.vstack((self.passed_coordinates,current_coordinate))
            next_coordinate = np.add(current_coordinate, [0,1])
            if not(self.check_if_passed(next_coordinate)):
                if self.is_in_boundary(next_coordinate):
                    current_coordinate = next_coordinate
                    self.score += 1
                    self.check_current_tile()
            else:
                self.passed_alert=1
        elif direction == "a":
            self.passed_coordinates = np.vstack((self.passed_coordinates,current_coordinate))
            next_coordinate = np.add(current_coordinate, [0,-1])
            if not(self.check_if_passed(next_coordinate)):
                if self.is_in_boundary(next_coordinate):
                    current_coordinate = next_coordinate
                    self.score += 1
                    self.check_current_tile()
            else:
                self.passed_alert=1
        else:
            print("wrong direction check")
        return current_coordinate
    
    def init_scene(self):
        print("\n")
        print("\033[H\033[J", end="")
        for coordinate in self.monster_coordinates:
            self.map[coordinate[0],coordinate[1]]="M"
        for coordinate in self.treasure_coordinates:
            self.map[coordinate[0],coordinate[1]]="T"
        for coordinate in self.sword_coordinates:
            self.map[coordinate[0],coordinate[1]]="S"
        for coordinate in self.potion_coordinates:
            self.map[coordinate[0],coordinate[1]]="P"
        for coordinate in self.venom_coordinates:
            self.map[coordinate[0],coordinate[1]]="V"
            
        self.player_coordinate = self.starting_coordinate
        self.seen_map[self.starting_coordinate[0],self.starting_coordinate[1]] = "*"
        print(self.seen_map)
        
    def seen_map_update(self):
        self.seen_map[self.player_coordinate[0],self.player_coordinate[1]] = "*"
        
    def check_current_tile(self):
        for coordinate in self.monster_coordinates:
            if self.is_same_coordinate(self.player_coordinate,coordinate):
                self.alert_setup("m")
                self.sword_stash -=1
                
        for coordinate in self.treasure_coordinates:
            if self.is_same_coordinate(self.player_coordinate,coordinate):
                self.alert_setup("t")
                self.score +=1
                
        for coordinate in self.potion_coordinates:
            if self.is_same_coordinate(self.player_coordinate,coordinate):
                self.alert_setup("p")
                self.potion_stash +=1
                
        for coordinate in self.sword_coordinates:
            if self.is_same_coordinate(self.player_coordinate,coordinate):
                self.alert_setup("s")
                self.sword_stash += 1
                
        for coordinate in self.venom_coordinates:
            if self.is_same_coordinate(self.player_coordinate,coordinate):
                self.alert_setup("v")
                self.potion_stash -= 1
                
    def next_scene(self):
        direction = input("Use W,A,S,D for movement: ")[0].lower()
        self.seen_map[self.player_coordinate[0],self.player_coordinate[1]] = ""
        self.player_coordinate = self.player_step(self.player_coordinate,direction)
        
        self.seen_map_update()
        print("\033[H\033[J", end="")
        print(self.seen_map)
        
    def play(self):
        self.init_scene()
        while self.alive_check():
            self.alert_reset()
            self.next_scene()
            self.menu()
        self.dead_scene()
            
    def is_same_coordinate(self,x,y):
        if x[0] == y[0] and x[1] == y[1]:
            return True
        else:
            return False
        
    def check_if_passed(self,coordinate):
        return self.check_if_contains(self.passed_coordinates, coordinate)
    
    def alert_reset(self):
        self.monster_alert=0
        self.treasure_alert=0
        self.potion_alert=0
        self.sword_alert=0
        self.venom_alert=0
        self.passed_alert=0
    
    def alert_setup(self,alert):
        if alert == "m":
            self.monster_alert=1
        elif alert == "t":
            self.treasure_alert=1
        elif alert == "s":
            self.sword_alert=1
        elif alert == "v":
            self.venom_alert=1
        elif alert == "p":
            self.potion_alert=1
            
    def alert_print(self):
        if self.monster_alert==1:
            print("OH! You have encountered a monster!")
        elif self.treasure_alert==1:
            print("You have found a treasure!")
        elif self.sword_alert==1:
            print("That is a shiny sword you have found!")
        elif self.venom_alert==1:
            print("A venomous snake bite you")
        elif self.potion_alert==1:
            print("You have find an antidote potion")
            
    def menu(self):
        print("\n")
        print("------------------------------------------")
        self.alert_print()
        print("------------------------------------------")
        if self.passed_alert == 1:
            print("You have already passed from that tile. Try another way!")
        print("Score: [{}]  Sword:[{}]  Potion[{}]".format(self.score,self.sword_stash,self.potion_stash))
        
    def alive_check(self):
        if self.potion_stash<0:
            self.died_to_venom=1
            return False
        if self.sword_stash<0:
            self.died_to_monster=1
            return False
        else:
            return True
    
    def dead_scene(self):
        print("\033[H\033[J", end="")
        print("\n")
        if self.died_to_monster == 1:
            print("You died to a monster! Game is over.")
        elif self.died_to_venom == 1:
            print("You died to a venomous snake! Game is over.")
        print("\n")
        print("Your score is: [{}]".format(self.score-1))
        print("\n\n")
    
    def is_in_boundary(self,coordinate):
        if 0 <= coordinate[0] and coordinate[0] < self.y_size and 0 <= coordinate[1] and coordinate[1] < self.x_size:
            return True
        else:
            return False



session = AdventureGame()

session.play()