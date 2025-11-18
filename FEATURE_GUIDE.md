# Game Feature Guide

## Visual Elements Added

### 1. Timer Display (Top Center)

```
┌────────────────┐
│    00:15       │  ← Golden/yellow text
└────────────────┘  ← Black background with border
```

- Shows elapsed time in MM:SS format
- Updates every frame
- Positioned at top center of screen

### 2. Diamond Counter (Top Left)

```
┌──────────────────┐
│ Diamonds: 3/6    │  ← White text
└──────────────────┘  ← Black background with border
```

- Shows collected/total diamonds
- Updates when diamonds are collected
- Positioned at top left of screen

### 3. Diamonds (In-Game Collectibles)

- **Blue Diamond** 💎 - 10 points
  - Only Hydro Girl (water) can collect
  - Blue color (RGB: 0, 150, 255)
- **Red Diamond** 💎 - 20 points
  - Only Magma Boy (fire) can collect
  - Red color (RGB: 255, 50, 50)

### 4. Win Screen Display

```
┌─────────────────────────────┐
│                             │
│       Grade: A              │  ← Large, color-coded
│                             │
│      Time: 00:25            │  ← White text
│                             │
│    Diamonds: 6/6            │  ← Blue text
│                             │
│ Outstanding! You are a      │  ← Golden text
│        master!              │
│                             │
│  Press ENTER to continue    │  ← Gray text
└─────────────────────────────┘
```

## Grade Color Coding

- **Grade A**: 🟢 Green - Outstanding performance
- **Grade B**: 🔵 Blue - Great job
- **Grade C**: 🟡 Yellow - Good effort
- **Grade D**: 🟠 Orange - Completed

## Controls

- **Arrow Keys**: Control Magma Boy (red character)
- **WASD Keys**: Control Hydro Girl (blue character)
- **ESC**: Return to level select
- **ENTER**: Confirm selections

## Gameplay Tips

1. **Speed matters**: Complete levels quickly for better grades
2. **Collect everything**: More diamonds = better grade
3. **Match colors**: Each character can only collect their color
4. **Work together**: Both characters must reach their doors
5. **Aim for Grade A**:
   - Complete in under 30 seconds
   - Collect at least 90% of diamonds

## Grade Requirements

| Grade | Max Time | Min Diamonds |
| ----- | -------- | ------------ |
| A     | 30 sec   | 90%          |
| B     | 60 sec   | 70%          |
| C     | 90 sec   | 50%          |
| D     | Any      | 0%           |

## Example Scores

- **Perfect Run**: 15 seconds, 6/6 diamonds → Grade A
- **Good Run**: 45 seconds, 5/6 diamonds (83%) → Grade B
- **Okay Run**: 75 seconds, 3/6 diamonds (50%) → Grade C
- **Completed**: 120 seconds, 2/6 diamonds (33%) → Grade D
