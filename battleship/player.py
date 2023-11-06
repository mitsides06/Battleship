import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ The strategy goes as follows: We randomly attack cells, and once we successfully hit a ship, 
        we save the coordinates of that successful cell and start hitting its neighbors until the ship sinks. 
        Once the ship has sunk, we continue with the same strategy.
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        
        # TODO: Add any other attributes necessary for your strategic player

        self.unsuccessful_directions = []  # needed to track the directions tried

        self.tracker = set()    # for the same purpose as the random player

        self.prev_result = (False, False)  # 2-tuple of the result of (is_ship_hit, has_ship_sunk) from the previous attack

        self.target = None  # the cell of the first successful hit to a particular ship

        self.prev_move = None  # the cell corresponing to the previous move

        self.direction = None   # the direction we moved, having already successfully hit a particular ship

        
        
    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        # TODO: Complete this method
        if self.prev_move is not None:
            possibe_moves_from_prev_move = {"left" : self.move_left(self.prev_move), "right" : self.move_right(self.prev_move),
                                            "up" : self.move_up(self.prev_move), "down" : self.move_down(self.prev_move)}
        if self.target is not None:
            possibe_moves_from_target = {"left" : self.move_left(self.target), "right" : self.move_right(self.target),
                                        "up" : self.move_up(self.target), "down" : self.move_down(self.target)}

        

        # The very start
        if len(self.tracker) == 0:
            target_cell = self.generate_random_target()
            self.prev_move = target_cell
            self.tracker.add(target_cell)
            print(target_cell)

            return target_cell
        
        
        #  Stage where we choose randomly our move as opponent's ship has been sunk
        elif self.prev_result[-1]:
            self.unsuccessful_directions = []
            self.dict_target = {}
            target_cell = self.generate_random_target()
            self.target = None
            self.prev_move = target_cell
            self.tracker.add(target_cell)
            print(target_cell)

            return target_cell
        
        #  Stage where we have already successfully hit a ship, and we keep trying to make it sink
        elif self.prev_result[0]:
            # Check if our previous move was the first successfull hit on the ship
            if self.target == None:
                self.target = self.prev_move
                for direction in list(possibe_moves_from_prev_move.keys()):
                    if self.is_valid(possibe_moves_from_prev_move[direction]):
                        self.direction = direction
                        target_cell = possibe_moves_from_prev_move[direction]
                        self.prev_move = target_cell
                        self.tracker.add(target_cell)
                        print(target_cell)

                        return target_cell
      
            # If this is not the first successful hit on a ship
            else:
                # continue trying in the successful direction if valid
                if self.is_valid(possibe_moves_from_prev_move[self.direction]):
                    target_cell = possibe_moves_from_prev_move[self.direction]
                    self.prev_move = target_cell
                    self.tracker.add(target_cell)
                    print(target_cell)

                    return target_cell
                
                # If not valid, try opposite direction, but change pivot point to self.target
                else:
                    new_direction = self.opposite_direction(self.direction)
                    self.direction = new_direction
                    target_cell = possibe_moves_from_target[self.direction]
                    self.prev_move = target_cell
                    self.tracker.add(target_cell)
                    print(target_cell)

                    return target_cell
                
        # If previous hit was unsuccesfull
        else:
            # Check if we were already working to make a ship sink
            if self.target is not None:
                self.unsuccessful_directions.append(self.direction)
                for direction in possibe_moves_from_target.keys():
                    if direction not in self.unsuccessful_directions:
                        if self.is_valid(possibe_moves_from_target[direction]):
                            self.direction = direction
                            target_cell = possibe_moves_from_target[self.direction]
                            self.prev_move = target_cell
                            self.tracker.add(target_cell)
                            print(target_cell)

                            return target_cell
            
            # If we haven't recently successfully hit a ship
            else:
                target_cell = self.generate_random_target()
                self.prev_move = target_cell
                self.tracker.add(target_cell)
                print(target_cell)

                return target_cell

                




            

                

    
                
            
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Save the results of our previous move to the self.prev_result attribute.

            Args: 
                is_ship_hit (bool) :  True or False
                has_ship_sunk (bool) :  True or False

            Returns:
                None
        """
        
        self.prev_result = (is_ship_hit, has_ship_sunk)


    def is_valid(self, cell):
        """ Check if the cell is within the board and that this particular cell has not been used for attack yet.

            Args:
                cell (tuple) : 2-tuple of the coordinates of the cell
            
            Returns:
                bool : True if this cell is valid to be used for next attack, False otherwise.
        """
        return (cell not in self.tracker) and (1 <= cell[0] <= self.board.width) \
                and (1 <= cell[1] <= self.board.height)
    
    def move_left(self, curr_cell):
        """ Move one cell to the left.

            Args:
                curr_cell (tuple) : 2-tuple of the coordinates of the current cell
            
            Returns:
                tuple : 2-tuple of the coodinates of cell which is one step to the left of the current one.
        """ 
        return (curr_cell[0]-1, curr_cell[1])
    
    def move_right(self, curr_cell):
        """ Move one cell to the right.

            Args:
                curr_cell (tuple) : 2-tuple of the coordinates of the current cell
            
            Returns:
                tuple : 2-tuple of the coodinates of cell which is one step to the right of the current one.
        """ 
        return (curr_cell[0]+1, curr_cell[1])
    
    def move_up(self, curr_cell):
        """ Move one cell up.

            Args:
                curr_cell (tuple) : 2-tuple of the coordinates of the current cell
            
            Returns:
                tuple : 2-tuple of the coodinates of cell which is one step above the current one.
        """ 
        return (curr_cell[0], curr_cell[1]-1)
    
    def move_down(self, curr_cell):
        """ Move one cell down.

            Args:
                curr_cell (tuple) : 2-tuple of the coordinates of the current cell
            
            Returns:
                tuple : 2-tuple of the coodinates of cell which is one step below the current one.
        """ 
        return (curr_cell[0], curr_cell[1]+1)
    
    def opposite_direction(self, direction):
        """ Find the opposite direction of the direction (input of this function).

            Args:
                direction (str) : "left" or "right" or "up" or "down"
            
            Returns:
                str : opposite direction of direction as a string
        """
        if direction == "left":
            return "right"
        elif direction == "right":
            return "left"
        elif direction == "up":
            return "down"
        else:
            return "up"
    
    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)
    
