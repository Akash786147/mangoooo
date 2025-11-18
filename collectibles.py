"""
Collectibles module for managing diamonds and other collectible items.
"""

import pygame
from pygame.locals import *


class Diamond:
    """Represents a collectible diamond in the game."""
    
    def __init__(self, location, diamond_type="blue"):
        """
        Initialize a diamond collectible.
        
        Args:
            location: tuple (x, y) - Position of the diamond
            diamond_type: str - Type of diamond ("blue" or "red")
        """
        self.location = location
        self.diamond_type = diamond_type
        self.collected = False
        
        # Load diamond image
        if diamond_type == "blue":
            self.image = pygame.image.load('data/collectibles/blue_diamond.png')
            self.points = 10
        else:  # red diamond
            self.image = pygame.image.load('data/collectibles/red_diamond.png')
            self.points = 20
        
        self.image.set_colorkey((255, 0, 255))
        
        # Create rect for collision detection
        self.rect = pygame.Rect(location[0], location[1], 
                               self.image.get_width(), self.image.get_height())
    
    def collect(self):
        """Mark diamond as collected."""
        self.collected = True
    
    def is_collected(self):
        """Return whether diamond has been collected."""
        return self.collected
    
    def get_points(self):
        """Return point value of the diamond."""
        return self.points
    
    def get_image(self):
        """Return diamond image."""
        return self.image
    
    def get_location(self):
        """Return diamond location."""
        return self.location
    
    def get_rect(self):
        """Return diamond rect for collision detection."""
        return self.rect


class CollectiblesManager:
    """Manages all collectibles in a level."""
    
    def __init__(self):
        """Initialize the collectibles manager."""
        self.diamonds = []
        self.total_diamonds = 0
        self.collected_diamonds = 0
        self.total_points = 0
        self.collected_points = 0
    
    def add_diamond(self, location, diamond_type="blue"):
        """
        Add a diamond to the level.
        
        Args:
            location: tuple (x, y) - Position of the diamond
            diamond_type: str - Type of diamond ("blue" or "red")
        """
        diamond = Diamond(location, diamond_type)
        self.diamonds.append(diamond)
        self.total_diamonds += 1
        self.total_points += diamond.get_points()
    
    def check_collection(self, player_rect, player_type):
        """
        Check if player has collected any diamonds.
        Red diamonds can only be collected by magma (fire) characters.
        Blue diamonds can only be collected by water characters.
        
        Args:
            player_rect: pygame.Rect - Player's collision rectangle
            player_type: str - Type of player ("magma" or "water")
            
        Returns:
            int - Points earned from collected diamonds
        """
        points_earned = 0
        for diamond in self.diamonds:
            if not diamond.is_collected() and player_rect.colliderect(diamond.get_rect()):
                # Check if player type matches diamond type
                can_collect = False
                if diamond.diamond_type == "red" and player_type == "magma":
                    can_collect = True
                elif diamond.diamond_type == "blue" and player_type == "water":
                    can_collect = True
                
                if can_collect:
                    diamond.collect()
                    points_earned += diamond.get_points()
                    self.collected_diamonds += 1
                    self.collected_points += diamond.get_points()
        return points_earned
    
    def get_uncollected_diamonds(self):
        """Return list of uncollected diamonds."""
        return [d for d in self.diamonds if not d.is_collected()]
    
    def get_collected_count(self):
        """Return number of collected diamonds."""
        return self.collected_diamonds
    
    def get_total_count(self):
        """Return total number of diamonds."""
        return self.total_diamonds
    
    def get_collected_points(self):
        """Return total points collected."""
        return self.collected_points
    
    def get_total_points(self):
        """Return total possible points."""
        return self.total_points
    
    def reset(self):
        """Reset all diamonds to uncollected state."""
        for diamond in self.diamonds:
            diamond.collected = False
        self.collected_diamonds = 0
        self.collected_points = 0
