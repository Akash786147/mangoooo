"""
Pathfinding AI controller using A* on the level tile graph.

This file contains a simple A* pathfinder that constructs a graph of
standable tile positions (player can stand at these tile coords) and
searches for a path to a target tile (diamond or door). The PathAIController
follows the path by setting movement flags on the player; it attempts a
jump when the next path node is higher than the current node.

This is intended as a practical, robust controller for demos and course
presentations. It is not a perfect physics-aware planner, but it reliably
navigates platforms by reasoning over tile positions.
"""
from heapq import heappush, heappop
import math
import pygame


class Pathfinder:
    def __init__(self, board):
        self.board = board
        self.game_map = board.get_game_map()
        self.CHUNK = board.CHUNK_SIZE

    def in_bounds(self, x, y):
        return 0 <= y < len(self.game_map) and 0 <= x < len(self.game_map[0])

    def is_solid(self, x, y):
        if not self.in_bounds(x, y):
            return False
        return self.game_map[y][x] not in ['0', '2', '3', '4']

    def is_hazard(self, x, y):
        if not self.in_bounds(x, y):
            return False
        return self.game_map[y][x] in ['2', '3', '4']

    def standable_nodes(self):
        """Return list of tile coords (x,y) where player can stand.

        Node definition: the tile at (x,y) is empty ('0') and the tile below
        (x,y+1) is solid (not air or liquid). This approximates tiles where the
        player can rest their feet.
        """
        nodes = []
        for y, row in enumerate(self.game_map):
            for x, tile in enumerate(row):
                # candidate must be empty
                if tile != '0':
                    continue
                # below must be solid (so we can stand)
                by = y + 1
                if not self.in_bounds(x, by):
                    continue
                if self.is_solid(x, by):
                    nodes.append((x, y))
        return nodes

    def neighbors(self, node):
        x, y = node
        nbrs = set()
        # horizontal move left/right if destination is standable
        for dx in (-1, 1):
            nx, ny = x + dx, y
            if self.in_bounds(nx, ny) and self.game_map[ny][nx] == '0' and self.in_bounds(nx, ny+1) and self.is_solid(nx, ny+1):
                nbrs.add((nx, ny))

        # jumps: allow stepping to nodes up to 4 tiles higher within 3 tiles horizontal
        for dx in (-3, -2, -1, 1, 2, 3):
            for dy in (-1, -2, -3, -4):
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.game_map[ny][nx] == '0' and self.in_bounds(nx, ny+1) and self.is_solid(nx, ny+1):
                    nbrs.add((nx, ny))

        # falls: allow dropping down to lower standable nodes within a wider horizontal range
        # this lets the AI walk off edges and fall to lower platforms
        for dx in (-3, -2, -1, 0, 1, 2, 3):
            for dy in (1, 2, 3, 4, 5, 6):
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.game_map[ny][nx] == '0' and self.in_bounds(nx, ny+1) and self.is_solid(nx, ny+1):
                    nbrs.add((nx, ny))

        return list(nbrs)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start_px, start_py, goal_px, goal_py, debug=False):
        """Find path from pixel coordinates (start_px, start_py) to goal pixel coords.

        Returns list of tile (x,y) nodes (in tile coords) or None if no path.
        """
        sx = int(start_px // self.CHUNK)
        sy = int(start_py // self.CHUNK)
        gx = int(goal_px // self.CHUNK)
        gy = int(goal_py // self.CHUNK)

        # find closest standable node to start and goal
        nodes = set(self.standable_nodes())
        if not nodes:
            if debug:
                print(f"[PATH FINDER] no standable nodes in map")
            return None

        def closest_node(px, py):
            # use fractional tile coordinates so we pick the node whose center
            # is closest in tile-space to the pixel position
            fx = px / self.CHUNK
            fy = py / self.CHUNK
            best = None
            bestd = None
            for n in nodes:
                d = abs(n[0] + 0.5 - fx) + abs(n[1] + 0.5 - fy)
                if best is None or d < bestd:
                    best = n
                    bestd = d
            return best

        start = closest_node(start_px, start_py)
        goal = closest_node(goal_px, goal_py)
        if debug:
            print(f"[PATH FINDER] sx,sy=({sx},{sy}) gx,gy=({gx},{gy}) nodes={len(nodes)} start_node={start} goal_node={goal}")
        if start is None or goal is None:
            if debug:
                print(f"[PATH FINDER] failed to find closest start/goal node")
            return None

        # A* search
        frontier = []
        heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heappop(frontier)
            if current == goal:
                break
            for nxt in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    priority = new_cost + self.heuristic(goal, nxt)
                    heappush(frontier, (priority, nxt))
                    came_from[nxt] = current

        if goal not in came_from:
            if debug:
                print(f"[PATH FINDER] goal {goal} not reached after search (visited {len(came_from)} nodes)")
            # if we reached some nodes but not the exact goal, return a partial
            # path to the reached node that's closest to the goal. This helps the
            # AI move toward the goal even when exact standable goal is isolated.
            if came_from:
                best = min(came_from.keys(), key=lambda n: self.heuristic(n, goal))
                if debug:
                    print(f"[PATH FINDER] returning partial path to best_reached={best}")
                path = []
                cur = best
                while cur is not None:
                    path.append(cur)
                    cur = came_from[cur]
                path.reverse()
                return path
            return None

        # reconstruct path
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path


class PathAIController:
    def __init__(self, board, collectibles_manager, door, player_type='magma', debug=False):
        self.board = board
        self.collectibles = collectibles_manager
        self.door = door
        self.player_type = player_type
        self.debug = debug
        self.pathfinder = Pathfinder(board)
        self.path = None
        self.path_index = 0
        self.recompute_cooldown = 0
        self.failed_recomputes = 0
        self.debug_shapes = []

    def _target(self, player_rect):
        # prefer nearest matching diamond, else door
        diamonds = self.collectibles.get_uncollected_diamonds()
        best = None
        bestd = None
        for d in diamonds:
            if (d.diamond_type == 'red' and self.player_type == 'magma') or (d.diamond_type == 'blue' and self.player_type == 'water'):
                dx = d.rect.centerx - player_rect.centerx
                dy = d.rect.centery - player_rect.centery
                dist = abs(dx) + abs(dy)
                if best is None or dist < bestd:
                    best = (d.rect.centerx, d.rect.centery)
                    bestd = dist
        if best:
            return best
        # door center
        return (self.door.door_location[0] + 8, self.door.door_location[1] + 16)

    def control_player(self, events, player):
        # reset movement flags
        player.moving_left = False
        player.moving_right = False
        player.jumping = False
        self.debug_shapes = []

        target = self._target(player.rect)
        tx, ty = target

        # compute path if none or if target changed significantly, but limit recompute frequency
        recompute = False
        if self.recompute_cooldown > 0:
            self.recompute_cooldown -= 1
        if self.path is None:
            recompute = True
        else:
            # if target tile changed (e.g., a diamond removed), recompute
            cur_goal = (self.path[-1][0] * self.pathfinder.CHUNK + self.pathfinder.CHUNK//2,
                        self.path[-1][1] * self.pathfinder.CHUNK + self.pathfinder.CHUNK//2)
            if abs(cur_goal[0] - tx) > 12 or abs(cur_goal[1] - ty) > 12 or self.path_index >= len(self.path):
                recompute = True

        if recompute and self.recompute_cooldown <= 0:
            # use player center for finding closest nodes
            self.path = self.pathfinder.find_path(player.rect.centerx, player.rect.centery, tx, ty, debug=self.debug)
            self.path_index = 0
            # set a small cooldown to avoid recomputing each frame
            self.recompute_cooldown = 12
            if self.path:
                self.failed_recomputes = 0
            else:
                self.failed_recomputes += 1
            if self.debug:
                if self.path:
                    print(f"[PATH AI] found path length={len(self.path)} start={self.path[0]} goal={self.path[-1]}")
                else:
                    print(f"[PATH AI] no path found from {(player.rect.centerx, player.rect.centery)} to {(tx,ty)} (failed {self.failed_recomputes})")

        # debug: draw planned path (tile centers)
        if self.debug and self.path:
            pts = []
            for (px, py) in self.path:
                cx = px * self.pathfinder.CHUNK + self.pathfinder.CHUNK//2
                cy = py * self.pathfinder.CHUNK + self.pathfinder.CHUNK//2
                pts.append((cx, cy))
                # draw small circle for each node
                self.debug_shapes.append(('circle', (cx, cy, 4), (0, 255, 0)))
            if len(pts) >= 2:
                self.debug_shapes.append(('lines', pts, (0, 200, 0)))

        # if we repeatedly fail to compute a useful path, fall back to a simple direct mover
        if not self.path:
            if self.failed_recomputes >= 3:
                # simple direct move toward target (greedy fallback)
                self._direct_move_toward(player, tx, ty)
            return

        # follow path: get next node
        if self.path_index >= len(self.path):
            return
        next_node = self.path[self.path_index]
        node_px = next_node[0] * self.pathfinder.CHUNK + self.pathfinder.CHUNK // 2
        node_py = next_node[1] * self.pathfinder.CHUNK + self.pathfinder.CHUNK // 2

        # if player close enough to node, advance
        # compare using player center to match node centers
        pcx = player.rect.centerx
        pcy = player.rect.centery
        if abs(pcx - node_px) < 8 and abs(pcy - node_py) < 12:
            self.path_index += 1
            if self.path_index >= len(self.path):
                return
            next_node = self.path[self.path_index]
            node_px = next_node[0] * self.pathfinder.CHUNK + self.pathfinder.CHUNK // 2
            node_py = next_node[1] * self.pathfinder.CHUNK + self.pathfinder.CHUNK // 2

        # decide movement
        if node_px > pcx + 2:
            player.moving_right = True
        elif node_px < pcx - 2:
            player.moving_left = True

        # if next node is higher (smaller y), try jump if grounded
        if next_node[1] < int(player.rect.y // self.pathfinder.CHUNK):
            if player.air_timer < 6:
                player.jumping = True

    def _direct_move_toward(self, player, tx, ty):
        """Very small greedy fallback: move horizontally toward target and try a jump
        if a blocking tile is detected in front."""
        pcx = player.rect.centerx
        # horizontal direction
        if pcx + 6 < tx:
            player.moving_right = True
        elif pcx - 6 > tx:
            player.moving_left = True

        # detect blocking tile in front at foot level
        sign = 1 if player.moving_right else -1 if player.moving_left else 0
        if sign != 0:
            ahead_x = int((player.rect.centerx + sign * 8) // self.pathfinder.CHUNK)
            foot_y = int((player.rect.bottom - 1) // self.pathfinder.CHUNK)
            if self.pathfinder.in_bounds(ahead_x, foot_y) and self.pathfinder.is_solid(ahead_x, foot_y):
                # try jump if grounded
                if player.air_timer < 6:
                    player.jumping = True

    # helper for external debug drawing (optional)
    def get_debug_shapes(self):
        return self.debug_shapes
