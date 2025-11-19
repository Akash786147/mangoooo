"""
Simple AI controller for MagmaBoy and HydroGirl.

This is a lightweight, deterministic greedy controller intended for demos
and course projects. It does not perform full search/planning — instead
it moves horizontally toward a target (nearest matching diamond or the
assigned door) and attempts a jump when it detects a blocking tile ahead.

Usage: instantiate with references to the `board`, `collectibles_manager`,
and the player's door object. Call `control_player(events, player)` each
frame (events is ignored). The controller sets `player.moving_left`,
`player.moving_right`, and `player.jumping` flags like the human controllers.
"""
import math
import pygame


class GreedyAIController:
    def __init__(self, board, collectibles_manager, door, player_type="magma", debug=False):
        self.board = board
        self.collectibles = collectibles_manager
        self.door = door
        self.player_type = player_type
        # frames to wait between jump attempts to avoid repeated jumping
        self.jump_cooldown = 0
        # avoidance: if a direction is deemed fatal, try opposite for a short window
        self.avoid_until = 0
        self.avoid_dir = 0
        # debug logging
        self.debug = debug
        self._debug_counter = 0
        # on-screen debug shapes produced each frame (cleared each control call)
        # shapes are tuples: (kind, payload, color)
        # kind in {'rect','circle','lines','tile'}
        self.debug_shapes = []

    def _nearest_diamond(self, player_rect):
        # Return location (x,y) of nearest uncollected diamond matching player type
        diamonds = self.collectibles.get_uncollected_diamonds()
        best = None
        best_dist = None
        for d in diamonds:
            if (d.diamond_type == "red" and self.player_type == "magma") or \
               (d.diamond_type == "blue" and self.player_type == "water"):
                dx = d.rect.centerx - player_rect.centerx
                dy = d.rect.centery - player_rect.centery
                dist = math.hypot(dx, dy)
                if best is None or dist < best_dist:
                    best = d
                    best_dist = dist
        if best:
            return best.rect.topleft
        return None

    def _is_blocking_tile(self, player_rect, direction):
        # Simple check: look slightly ahead at foot level for a solid block
        # direction: -1 (left) or 1 (right)
        LOOK_AHEAD = 10
        CHUNK = self.board.CHUNK_SIZE
        # probe near the player's mid-body (not the very bottom) to avoid
        # detecting the ground tile beneath the player as a frontal block
        probe_x = player_rect.centerx + direction * LOOK_AHEAD
        probe_y = player_rect.centery
        # convert probe coords to a rect matching chunk
        test_rect = (probe_x // CHUNK, probe_y // CHUNK)
        # inspect game_map: if a non-air tile exists at that chunk, consider it blocking
        game_map = self.board.get_game_map()
        gx = int(test_rect[0])
        gy = int(test_rect[1])
        if gy < 0 or gy >= len(game_map) or gx < 0 or gx >= len(game_map[0]):
            return False
        tile = game_map[gy][gx]
        # tile not in liquids or air means solid
        return tile not in ["0", "2", "3", "4"]

    def control_player(self, events, player):
        # decrement timers
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.avoid_until > 0:
            self.avoid_until -= 1
        if self._debug_counter > 0:
            self._debug_counter -= 1
        # Decide a target: nearest diamond of matching type, else the door
        target = self._nearest_diamond(player.rect)
        if target is None:
            target = self.door.door_location

        tx, ty = target
        px = player.rect.x
        # reset movement
        player.moving_left = False
        player.moving_right = False
        # clear debug shapes for this frame
        self.debug_shapes = []

        # If in avoidance mode, try moving in the avoid direction instead of toward target
        if self.avoid_until > 0 and self.avoid_dir != 0:
            direction = self.avoid_dir
        elif abs(tx - px) > 4:
            direction = 1 if tx > px else -1
        else:
            direction = 0

        # move horizontally if we have a direction
        if direction != 0:

            # quick constants (match Character motion constants)
            LATERAL_SPEED = 3

            # create a predicted rect if the player moves one step horizontally
            # Check ahead to jump early before reaching hazard edge
            # MUCH longer lookahead when grounded to see water/lava pools ahead before walking off edges
            # Shorter when airborne since already committed to the jump arc
            lookahead_dist = 4 if player.air_timer > 6 else 14
            next_rect_x = player.rect.x + direction * LATERAL_SPEED * lookahead_dist
            next_rect = player.rect.copy()
            next_rect.x = next_rect_x

            # add predicted next rect to debug shapes
            if self.debug:
                self.debug_shapes.append(('rect', next_rect.copy(), (200, 200, 0)))

            # check hazardous pools ahead
            lava_pools = self.board.get_lava_pools()
            water_pools = self.board.get_water_pools()
            goo_pools = self.board.get_goo_pools()

            will_hit_lava = any(next_rect.colliderect(r) for r in lava_pools)
            will_hit_water = any(next_rect.colliderect(r) for r in water_pools)
            will_hit_goo = any(next_rect.colliderect(r) for r in goo_pools)
            # More robust hazard detection: check the board's tile map under the
            # predicted next position. This avoids mismatches between small probe
            # rects and the pool rects' half-height layout.
            # ALSO check directly below player if airborne to catch immediate hazards
            try:
                CHUNK = self.board.CHUNK_SIZE
                game_map = self.board.get_game_map()
                
                # Check predicted position AND tiles below it (check 2 tiles down to catch pits)
                gx = int(next_rect.centerx // CHUNK)
                gy = int(next_rect.bottom // CHUNK)
                # Check current tile and next 2 tiles below
                for check_y in [gy, gy + 1, gy + 2]:
                    if check_y >= 0 and check_y < len(game_map) and gx >= 0 and gx < len(game_map[0]):
                        tile = game_map[check_y][gx]
                        if self.debug and self._debug_counter == 0:
                            print(f"[TILE CHECK] gx={gx}, gy={check_y}, tile='{tile}', next_rect.x={int(next_rect.x)}, lookahead={lookahead_dist}")
                        if tile == '2':
                            will_hit_lava = True
                        if tile == '3':
                            will_hit_water = True
                        if tile == '4':
                            will_hit_goo = True
                
                # If in air, ALSO check directly below current position
                if player.air_timer > 6:
                    gx_below = int(player.rect.centerx // CHUNK)
                    gy_below = int(player.rect.bottom // CHUNK)
                    if gy_below >= 0 and gy_below < len(game_map) and gx_below >= 0 and gx_below < len(game_map[0]):
                        tile_below = game_map[gy_below][gx_below]
                        if tile_below == '2':
                            will_hit_lava = True
                        if tile_below == '3':
                            will_hit_water = True
                        if tile_below == '4':
                            will_hit_goo = True
                
                # also check one tile below predicted position in case next_rect bottom sits on tile boundary
                gy2 = gy + 1
                if gy2 >= 0 and gy2 < len(game_map) and gx >= 0 and gx < len(game_map[0]):
                    tile2 = game_map[gy2][gx]
                    if tile2 == '2':
                        will_hit_lava = True
                    if tile2 == '3':
                        will_hit_water = True
                    if tile2 == '4':
                        will_hit_goo = True
            except Exception:
                # fallback: keep previous rect-based checks
                pass

            # produce a simulated trajectory for debug overlay
            def simulate_trajectory(simulate_jump=False, lookahead_frames=40):
                CHUNK = self.board.CHUNK_SIZE
                sim_x = player.rect.x
                sim_y = player.rect.y
                sim_yv = getattr(player, 'y_velocity', 0)
                if simulate_jump and player.air_timer < 6:
                    sim_yv = -5
                lateral = direction * LATERAL_SPEED
                points = []
                for _ in range(lookahead_frames):
                    sim_x += lateral
                    sim_y += sim_yv
                    sim_yv += 0.2
                    if sim_yv > 3:
                        sim_yv = 3
                    # record center-bottom as visual point
                    cx = sim_x + player.rect.width // 2
                    cy = sim_y + player.rect.height
                    points.append((int(cx), int(cy)))
                return points

            if self.debug:
                traj = simulate_trajectory(False, 30)
                traj_jump = simulate_trajectory(True, 30)
                if traj:
                    self.debug_shapes.append(('lines', traj, (255, 255, 0)))
                if traj_jump:
                    self.debug_shapes.append(('lines', traj_jump, (255, 200, 0)))

            # Advanced lookahead: simulate a short forward trajectory to detect
            # whether moving (or moving+jumping) will lead to a fatal pool within
            # the next N frames. This helps avoid cases where an immediate tile
            # check misses a subsequent fall into a pool.
            def will_path_be_fatal(simulate_jump=False, lookahead_frames=40):
                CHUNK = self.board.CHUNK_SIZE
                game_map = self.board.get_game_map()

                # initialize simulation state from player
                sim_x = player.rect.x
                sim_y = player.rect.y
                sim_yv = getattr(player, 'y_velocity', 0)

                if simulate_jump and player.air_timer < 6:
                    sim_yv = -5  # jump speed used in Character.calc_movement

                lateral = direction * LATERAL_SPEED

                for _ in range(lookahead_frames):
                    # apply lateral movement
                    sim_x += lateral
                    # apply vertical movement
                    sim_y += sim_yv
                    sim_yv += 0.2
                    if sim_yv > 3:
                        sim_yv = 3

                    # compute tile under feet
                    gx = int((sim_x + player.rect.width // 2) // CHUNK)
                    gy = int((sim_y + player.rect.height) // CHUNK)
                    if gy < 0 or gy >= len(game_map) or gx < 0 or gx >= len(game_map[0]):
                        # out of bounds considered non-fatal here
                        continue
                    tile = game_map[gy][gx]
                    if tile == '2':
                        if self.player_type == 'water' or tile == '2':
                            return True
                    if tile == '3':
                        if self.player_type == 'magma' or tile == '3':
                            return True
                    if tile == '4':
                        return True
                return False

            sim_fatal = will_path_be_fatal(simulate_jump=False)
            sim_fatal_jump = will_path_be_fatal(simulate_jump=True)

            # determine if this hazard would be fatal for this player
            fatal = False
            if self.player_type == "magma" and will_hit_water:
                fatal = True
            if self.player_type == "water" and will_hit_lava:
                fatal = True
            if will_hit_goo:
                fatal = True

            # If moving forward would be fatal, ALWAYS jump (don't back up)
            if fatal or sim_fatal:
                # Check if jumping over the hazard is safe by simulating jump trajectory
                # Allow passing through hazard during jump as long as we land safely
                can_jump_over = False
                if player.air_timer < 6 and self.jump_cooldown == 0:
                    # Simulate a jump arc and see if we land safely beyond hazard
                    CHUNK = self.board.CHUNK_SIZE
                    game_map = self.board.get_game_map()
                    sim_x = player.rect.x
                    sim_y = player.rect.y
                    sim_yv = -5  # jump velocity
                    lateral = direction * LATERAL_SPEED
                    
                    landed_safe = False
                    passed_hazard = False
                    for frame in range(60):  # simulate up to 60 frames
                        sim_x += lateral
                        sim_y += sim_yv
                        sim_yv += 0.2
                        if sim_yv > 3:
                            sim_yv = 3
                        
                        # check tile under feet
                        gx = int((sim_x + player.rect.width // 2) // CHUNK)
                        gy = int((sim_y + player.rect.height) // CHUNK)
                        
                        if gy < 0 or gy >= len(game_map) or gx < 0 or gx >= len(game_map[0]):
                            break
                        
                        tile = game_map[gy][gx]
                        
                        # track if we've passed beyond the initial hazard zone
                        if gx > int((player.rect.centerx + direction * 64) // CHUNK):
                            passed_hazard = True
                        
                        # check if we've landed on solid ground (tile below is solid and current tile is air)
                        gy_below = gy + 1
                        if gy_below < len(game_map) and tile == '0':
                            tile_below = game_map[gy_below][gx]
                            if tile_below not in ['0', '2', '3', '4'] and passed_hazard:
                                # landed safely beyond hazard
                                landed_safe = True
                                break
                    
                    if landed_safe:
                        can_jump_over = True
                
                # ALWAYS try to jump over hazards - don't back up
                # This prevents oscillation at goo/water/lava pools
                if player.air_timer < 6 and self.jump_cooldown == 0:
                    if direction == 1:
                        player.moving_right = True
                    else:
                        player.moving_left = True
                    player.jumping = True
                    self.jump_cooldown = 30
                elif player.air_timer >= 6:
                    # Already in air - keep moving forward to try to clear the hazard
                    if direction == 1:
                        player.moving_right = True
                    else:
                        player.moving_left = True
                # If cooling down and grounded, just wait
            else:
                # safe to move horizontally
                if direction == 1:
                    player.moving_right = True
                else:
                    player.moving_left = True

                # if there is a blocking tile in front while on ground, attempt jump
                # Check further ahead to jump earlier over obstacles
                if player.air_timer < 6 and self.jump_cooldown == 0:
                    dir_flag = 1 if player.moving_right else (-1 if player.moving_left else 0)
                    if dir_flag != 0:
                        # Check multiple tiles ahead for blocking
                        CHUNK = self.board.CHUNK_SIZE
                        game_map = self.board.get_game_map()
                        ahead_x = int((player.rect.centerx + dir_flag * 20) // CHUNK)
                        foot_y = int((player.rect.bottom - 1) // CHUNK)
                        
                        should_jump = False
                        if 0 <= ahead_x < len(game_map[0]) and 0 <= foot_y < len(game_map):
                            tile = game_map[foot_y][ahead_x]
                            if tile not in ['0', '2', '3', '4']:  # solid tile
                                should_jump = True
                        
                        if should_jump:
                            player.jumping = True
                            self.jump_cooldown = 25

        # Debug logging: throttle to avoid flooding console
        if self.debug and self._debug_counter == 0:
            try:
                info = {
                    'type': self.player_type,
                    'px': player.rect.x,
                    'py': player.rect.y,
                    'target': (tx, ty),
                    'moving_left': player.moving_left,
                    'moving_right': player.moving_right,
                    'jumping': player.jumping,
                    'air_timer': player.air_timer,
                    'jump_cooldown': self.jump_cooldown,
                    'avoid_until': self.avoid_until,
                    'avoid_dir': self.avoid_dir,
                    'will_hit_lava': will_hit_lava,
                    'will_hit_water': will_hit_water,
                    'will_hit_goo': will_hit_goo,
                }
                print(f"[AI DEBUG] {info}")
            except Exception:
                pass
            self._debug_counter = 15

        # do not return anything; mutate player flags just like human controllers
