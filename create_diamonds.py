"""
Create placeholder diamond images for the game.
"""
import pygame
import os

# Initialize pygame
pygame.init()

def create_diamond_image(color, filename):
    """Create a simple diamond shape image."""
    size = 16
    surface = pygame.Surface((size, size))
    surface.set_colorkey((255, 0, 255))
    surface.fill((255, 0, 255))  # Magenta background (transparent)
    
    # Draw diamond shape (4 triangles)
    center = size // 2
    points = [
        (center, 2),           # Top
        (size - 2, center),    # Right
        (center, size - 2),    # Bottom
        (2, center)            # Left
    ]
    
    pygame.draw.polygon(surface, color, points)
    
    # Add a lighter inner diamond for depth
    inner_points = [
        (center, 4),
        (size - 4, center),
        (center, size - 4),
        (4, center)
    ]
    lighter_color = tuple(min(255, c + 50) for c in color)
    pygame.draw.polygon(surface, lighter_color, inner_points)
    
    # Save the image
    pygame.image.save(surface, filename)
    print(f"Created {filename}")

# Create directory if it doesn't exist
os.makedirs('data/collectibles', exist_ok=True)

# Create blue diamond (for water girl)
create_diamond_image((0, 150, 255), 'data/collectibles/blue_diamond.png')

# Create red diamond (for fire boy)
create_diamond_image((255, 50, 50), 'data/collectibles/red_diamond.png')

print("Diamond images created successfully!")
pygame.quit()
