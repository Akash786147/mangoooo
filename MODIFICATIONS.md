# Game Modifications Summary

## New Features Added

### 1. Diamond Collectibles System

- **File Created**: `collectibles.py`
  - `Diamond` class: Manages individual diamonds (blue and red)
  - `CollectiblesManager` class: Tracks all diamonds in a level
  - Red diamonds (20 points) - can only be collected by Magma Boy
  - Blue diamonds (10 points) - can only be collected by Hydro Girl
  - Collision detection for collection

### 2. Scoring System

- **File Created**: `scoring.py`
  - `ScoreCalculator` class: Calculates grades based on performance
  - Grade system (A, B, C, D) based on:
    - Time taken to complete level
    - Percentage of diamonds collected
  - Grade thresholds:
    - **A**: ≤30 seconds, ≥90% diamonds
    - **B**: ≤60 seconds, ≥70% diamonds
    - **C**: ≤90 seconds, ≥50% diamonds
    - **D**: Any completion

### 3. Timer System

- Real-time timer tracking level completion time
- Displays in MM:SS format at top center of screen
- Golden/yellow text with decorative border
- Timer starts when level begins

### 4. UI Enhancements

**Modified**: `game.py`

- `draw_timer()`: Displays elapsed time with styled background
- `draw_collectibles()`: Renders uncollected diamonds
- `draw_diamond_counter()`: Shows collected/total diamonds at top left
- Added font initialization for UI text

### 5. Win Screen with Scoring

**Modified**: `main.py` - `show_win_screen()` function

- Displays final grade with color coding:
  - Grade A: Green
  - Grade B: Blue
  - Grade C: Yellow
  - Grade D: Orange
- Shows completion time
- Shows diamonds collected vs total
- Displays grade-specific message

### 6. Game Loop Integration

**Modified**: `main.py` - `run_game()` function

- Initialize `CollectiblesManager` for each level
- Track elapsed time using pygame ticks
- Check diamond collection each frame for both players
- Draw timer, diamonds, and counter during gameplay
- Pass score data to win screen

### 7. Diamond Images

**Created**: `create_diamonds.py` (utility script)

- Generates `blue_diamond.png` and `red_diamond.png`
- 16x16 pixel diamond shapes
- Blue diamond: RGB(0, 150, 255)
- Red diamond: RGB(255, 50, 50)
- Stored in `data/collectibles/` folder

## Files Modified

1. `game.py` - Added timer and collectibles drawing methods
2. `main.py` - Integrated timer, collectibles, and scoring
3. `collectibles.py` - NEW FILE
4. `scoring.py` - NEW FILE
5. `create_diamonds.py` - NEW FILE (utility)

## Diamond Placement (Sample)

- Level 1: 6 diamonds (3 red, 3 blue)
- Level 2: 4 diamonds (2 red, 2 blue)
- Level 3: 4 diamonds (2 red, 2 blue)

_Note: Diamond positions can be adjusted for better gameplay balance_

## How It Works

1. Player starts level - timer begins
2. Players move through level collecting colored diamonds
3. Red diamonds only collectible by Magma Boy (fire character)
4. Blue diamonds only collectible by Hydro Girl (water character)
5. Timer and collection count displayed during play
6. Upon completing level (both characters in doors):
   - Calculate grade based on time and diamonds
   - Display score screen with grade, time, and diamonds
   - Show motivational message based on grade

## Testing

Run the game with: `python main.py`

- Timer displays at top center
- Diamond counter at top left
- Collect diamonds by touching them with matching character
- Complete level to see grade screen
