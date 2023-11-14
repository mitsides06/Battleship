import random

from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end, should_validate=True):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
            should_validate (bool): should the constructor check whether the 
                given coordinates result in a horizontal or vertical ship? 
                Defaults to True.

        Raises:
            ValueError: if should_validate==True and 
                if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = (
            min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        )
        
        # make y_start on top and y_end on bottom
        self.y_start, self.y_end = (
            min(self.y_start, self.y_end), max(self.y_start, self.y_end)
        )
        
        if should_validate:
            if not self.is_horizontal() and not self.is_vertical():
                raise ValueError("The given coordinates are invalid. "
                    "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return (f"Ship(start=({self.x_start},{self.y_start}), "
            f"end=({self.x_end},{self.y_end}))")
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        # TODO: Complete this method

        return self.x_start == self.x_end
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
        # TODO: Complete this method
        return self.y_start == self.y_end
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """
        # TODO: Complete this method
        if self.is_horizontal():
            if self.x_start > self.x_end:
                return set((i, self.y_start) for i in range(self.x_end, self.x_start+1))
            else:
                return set((i, self.y_start) for i in range(self.x_start, self.x_end+1))
        
        else:
            if self.y_start > self.y_end:
                return set((self.x_start, i) for i in range(self.y_end, self.y_start+1))
            else:
                return set((self.x_start, i) for i in range(self.y_start, self.y_end+1))
            


    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        # TODO: Complete this method
        if self.is_horizontal():
            return abs(self.x_end - self.x_start) + 1
        else:
            return abs(self.y_start - self.y_end) + 1

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        # TODO: Complete this method
        return cell in self.get_cells()
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        # TODO: Complete this method
        if self.is_occupying_cell(cell):
            self.damaged_cells.add(cell)
            return True
        
        return False
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """
        # TODO: Complete this method
        return len(self.damaged_cells)
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """
        # TODO: Complete this method
        for cell in self.get_cells():
            if cell not in self.damaged_cells:
                return False
        
        return True

    
    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """
        # TODO: Complete this method
        for cell in other_ship.get_cells():
            if self.is_near_cell(cell):
                return True
        
        return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the 
                ship. Returns False otherwise.
        """
        return (self.x_start-1 <= cell[0] <= self.x_end+1 
                and self.y_start-1 <= cell[1] <= self.y_end+1)


class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size

        # The following will help with the ship generation
        self.forbidden_cells = set()
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be 
        too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """
        # TODO: Complete this method
        ships = []
        for length, count in self.ships_per_length.items():
            for i in range(count):
                ship = self.create_ship(length)
                ships.append(ship)
        return ships

    def create_ship_input(self, length, direction, other_direction, start_coordinate, other_direction_coordinate):
        """ Create the input of the ship to be used in the create_ship function.

            Args:
                length (int) : The length of the ship
                direction (int) : 0 or 1, depending on the direction we want our 
                        ship to be longest,0 if along x-direction,
                        1 if along y-direction.                               
                other_direction (int) : if direction is 0 then this is 1, and 
                        vice versa.
                start_coordinate (int) : the x-coordinate value or the 
                        y-coordinate value (depending on the direction)
                        of the starting cell of the ship.
                other_direction_coordinate (int) : if start_coordinate is the 
                        x-coordinate value, then this is the y-coordinate 
                        value, and vice versa.

            Returns:
                tuple : a 2-tuple consisting the starting cell of the cell as a 
                    first element, and the ending cell of the 
                    ship as a second element.
        """
        start = [None, None]
        end = [None, None]
        start[direction] = start_coordinate
        start[other_direction] = other_direction_coordinate
        end[direction] = start_coordinate + length - 1
        end[other_direction] = other_direction_coordinate
        start = tuple(start)
        end = tuple(end)
        return start, end

    

    def create_ship(self, length):
        """ Create ship of length length (the input of this function) which 
            is not near to any other ship.

            Args:
                length (int) : the length of the ship

            Returns:
                Ship : A ship instance
        """
        valid = False
        while not valid:
            # direction parallel to the largest side of the ship
            direction = random.randint(0,1)   

            # direction perpendicular to the direction variable
            other_direction = (direction + 1) % 2 

            max_cell_coordinate = self.board_size[direction] - length + 1
            start_coordinate = random.randint(1, max_cell_coordinate)
            other_direction_coordinate = random.randint(1, self.board_size[other_direction])

            start, end = self.create_ship_input(length, direction, other_direction, start_coordinate, other_direction_coordinate)
            ship = Ship(start=start,end=end)

            valid = True
            # Check if the incoming ship is near the other existing ships
            for cell in ship.get_cells():
                if cell in self.forbidden_cells:
                    valid = False
                    break
            if valid == True:
                self.update_forbidden_cells(ship)

        return ship


    def update_forbidden_cells(self, ship):
        """ We update the update_fobridden_cells attrribute every time we 
            create a valid ship. This is a set that helps us check if a 
            creation of a ship is valid or not.

            Args:
                Ship (instance) : Ship instance

            Returns:
                None
        """
        self.forbidden_cells.update(ship.get_cells())
        if ship.is_horizontal():
            add_set = set((x, y ) for x in range(max(ship.x_start-1, 1), min(11, ship.x_end+2)) for y in [max(1, ship.y_start-1), min(10, ship.y_end+1), ship.y_start])
        else:
            add_set = set((x, y ) for x in [max(1, ship.x_start-1), min(10, ship.x_end+1), ship.x_start] for y in range(max(1, ship.y_start-1), min(11, ship.y_end+2)))
        self.forbidden_cells.update(add_set)

        
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods
    """
    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.length())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    """
    ship2 = Ship(start=(4, 1), end=(4, 5))
    #print(ship.is_near_ship(ship2))

    # my test cases
    my_ship = Ship(start=(3,10), end=(3,1))
    ship_cells = my_ship.get_cells()
    assert {(3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10)} == ship_cells
    print(ship_cells)
    direction_h = my_ship.is_horizontal()
    assert direction_h == False
    direction_v = my_ship.is_vertical()
    assert direction_v == True
    length = my_ship.length()
    assert length == 10
    my_ship.receive_damage((3,1))
    my_ship.receive_damage((3,6))
    my_ship.receive_damage((3,10))
    my_ship.receive_damage((4,4))
    no_damaged_cells = my_ship.count_damaged_cells()
    assert no_damaged_cells == 3
    print(my_ship.damaged_cells)
    near_ship_t = my_ship.is_near_ship(ship2)
    assert near_ship_t == True
    near_cell_t = my_ship.is_near_cell((4,11))
    assert near_cell_t == True
    near_cell_f = my_ship.is_near_cell((3,12))
    assert near_cell_f == False


    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    