"""
Helper script to visualize and adjust diamond positions for each level.
This can be used to fine-tune diamond placements based on level layout.
"""

# Recommended diamond positions for each level based on game structure

LEVEL_DIAMONDS = {
    "level1": [
        # Format: (x, y, type)
        # Blue diamonds for Hydro Girl (water character)
        (60, 340, "blue"),    # Near starting position
        (280, 280, "blue"),   # Mid-level platform
        (100, 180, "blue"),   # Upper left area
        
        # Red diamonds for Magma Boy (fire character)
        (300, 80, "red"),     # Near top right
        (450, 150, "red"),    # Right side platform
        (220, 340, "red"),    # Lower middle area
    ],
    
    "level2": [
        # Blue diamonds
        (80, 300, "blue"),
        (350, 200, "blue"),
        (200, 150, "blue"),
        
        # Red diamonds
        (450, 250, "red"),
        (250, 100, "red"),
        (150, 350, "red"),
    ],
    
    "level3": [
        # Blue diamonds - place near water-safe areas
        (150, 150, "blue"),
        (300, 250, "blue"),
        (100, 320, "blue"),
        
        # Red diamonds - place near lava-safe areas
        (400, 150, "red"),
        (450, 280, "red"),
        (250, 200, "red"),
    ]
}

def print_diamond_positions():
    """Print diamond positions for easy copying into main.py"""
    for level_name, diamonds in LEVEL_DIAMONDS.items():
        print(f"\n{level_name.upper()}:")
        print("collectibles = CollectiblesManager()")
        for x, y, dtype in diamonds:
            print(f'collectibles.add_diamond(({x}, {y}), "{dtype}")')

def get_diamond_stats():
    """Get statistics about diamonds in each level"""
    for level_name, diamonds in LEVEL_DIAMONDS.items():
        blue_count = sum(1 for d in diamonds if d[2] == "blue")
        red_count = sum(1 for d in diamonds if d[2] == "red")
        total = len(diamonds)
        blue_points = blue_count * 10
        red_points = red_count * 20
        total_points = blue_points + red_points
        
        print(f"\n{level_name}:")
        print(f"  Blue diamonds: {blue_count} ({blue_points} points)")
        print(f"  Red diamonds: {red_count} ({red_points} points)")
        print(f"  Total: {total} diamonds ({total_points} points)")

if __name__ == "__main__":
    print("=" * 60)
    print("DIAMOND PLACEMENT HELPER")
    print("=" * 60)
    
    print("\n### DIAMOND STATISTICS ###")
    get_diamond_stats()
    
    print("\n\n### CODE TO COPY INTO main.py ###")
    print_diamond_positions()
    
    print("\n\n### TIPS FOR PLACEMENT ###")
    print("1. Place diamonds on platforms, not in mid-air")
    print("2. Blue diamonds should be reachable by Hydro Girl")
    print("3. Red diamonds should be reachable by Magma Boy")
    print("4. Spread diamonds throughout the level for exploration")
    print("5. Consider placing some diamonds in challenging spots")
    print("6. Balance between easy and hard-to-reach diamonds")
    print("7. Avoid placing diamonds in deadly areas (lava/water pools)")
