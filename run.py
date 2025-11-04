import sys
import heapq
from functools import cache

def solve(lines):
    room_depth = len(lines) - 3
    room_positions = [2, 4, 6, 8]
    target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    
    hallway_positions = [0, 1, 3, 5, 7, 9, 10]
    
    # Парсим начальное состояние
    initial_rooms = [[] for _ in range(4)]
    for depth in range(room_depth):
        for room_idx in range(4):
            char = lines[2 + depth][3 + room_idx * 2]
            initial_rooms[room_idx].append(char)
    
    # Представляем состояние как хешируемую строку для экономии памяти
    def state_to_key(rooms, hallway):
        key = ""
        for room in rooms:
            for pos in room:
                key += pos if pos != '.' else '.'
            key += "|"
        for pos in hallway:
            key += pos if pos != '.' else '.'
        return key
    
    def key_to_state(key):
        parts = key.split("|")
        rooms = []
        for i in range(4):
            room_str = parts[i]
            rooms.append(list(room_str))
        hallway = list(parts[4])
        return rooms, hallway
    
    initial_hallway = ['.'] * 11
    initial_key = state_to_key(initial_rooms, initial_hallway)
    
    def is_path_clear(hallway, start, end):
        if start < end:
            for pos in range(start + 1, end + 1):
                if hallway[pos] != '.':
                    return False
        else:
            for pos in range(end, start):
                if hallway[pos] != '.':
                    return False
        return True
    
    def is_room_available(rooms, room_idx, amphipod_type):
        if target_rooms[amphipod_type] != room_idx:
            return False
        for amphipod in rooms[room_idx]:
            if amphipod != '.' and amphipod != amphipod_type:
                return False
        return True
    
    def room_has_foreigners(rooms, room_idx):
        target_type = ['A', 'B', 'C', 'D'][room_idx]
        for amphipod in rooms[room_idx]:
            if amphipod != '.' and amphipod != target_type:
                return True
        return False
    
    def get_top_amphipod(rooms, room_idx):
        for i in range(room_depth):
            if rooms[room_idx][i] != '.':
                return i, rooms[room_idx][i]
        return None
    
    def get_free_spot(rooms, room_idx):
        for i in range(room_depth - 1, -1, -1):
            if rooms[room_idx][i] == '.':
                return i
        return -1
    
    def move_to_room_cost(amphipod_type, hallway_pos, room_idx, room_spot):
        hallway_steps = abs(hallway_pos - room_positions[room_idx])
        room_steps = room_spot + 1
        return (hallway_steps + room_steps) * costs[amphipod_type]
    
    def move_to_hallway_cost(amphipod_type, room_idx, room_spot, hallway_pos):
        room_steps = room_spot + 1
        hallway_steps = abs(room_positions[room_idx] - hallway_pos)
        return (room_steps + hallway_steps) * costs[amphipod_type]
    
    def is_final_state(rooms, hallway):
        for i, room in enumerate(rooms):
            target_type = ['A', 'B', 'C', 'D'][i]
            for amphipod in room:
                if amphipod != target_type:
                    return False
        for amphipod in hallway:
            if amphipod != '.':
                return False
        return True
    
    def dijkstra(start_key):
        visited = set()
        heap = [(0, start_key)]
        
        while heap:
            cost, state_key = heapq.heappop(heap)
            
            if state_key in visited:
                continue
            visited.add(state_key)
            
            rooms, hallway = key_to_state(state_key)
            
            if is_final_state(rooms, hallway):
                return cost
            
            # Move from hallway to room (приоритетное движение)
            for hallway_pos in hallway_positions:
                if hallway[hallway_pos] != '.':
                    amphipod_type = hallway[hallway_pos]
                    target_room = target_rooms[amphipod_type]
                    
                    if not is_room_available(rooms, target_room, amphipod_type):
                        continue
                    
                    if not is_path_clear(hallway, hallway_pos, room_positions[target_room]):
                        continue
                    
                    free_spot = get_free_spot(rooms, target_room)
                    if free_spot == -1:
                        continue
                    
                    move_cost = move_to_room_cost(amphipod_type, hallway_pos, target_room, free_spot)
                    
                    new_rooms = [room.copy() for room in rooms]
                    new_hallway = hallway.copy()
                    
                    new_rooms[target_room][free_spot] = amphipod_type
                    new_hallway[hallway_pos] = '.'
                    
                    new_key = state_to_key(new_rooms, new_hallway)
                    heapq.heappush(heap, (cost + move_cost, new_key))
            
            # Move from room to hallway (только если есть иностранцы)
            for room_idx in range(4):
                if not room_has_foreigners(rooms, room_idx):
                    continue
                
                top_info = get_top_amphipod(rooms, room_idx)
                if top_info is None:
                    continue
                
                room_spot, amphipod_type = top_info
                
                # Если амфипод уже в своей целевой комнате и все ниже него правильные - не двигаем
                if target_rooms[amphipod_type] == room_idx:
                    all_below_correct = True
                    for i in range(room_spot + 1, room_depth):
                        if rooms[room_idx][i] != amphipod_type:
                            all_below_correct = False
                            break
                    if all_below_correct:
                        continue
                
                for hallway_pos in hallway_positions:
                    if not is_path_clear(hallway, room_positions[room_idx], hallway_pos):
                        continue
                    
                    move_cost = move_to_hallway_cost(amphipod_type, room_idx, room_spot, hallway_pos)
                    
                    new_rooms = [room.copy() for room in rooms]
                    new_hallway = hallway.copy()
                    
                    new_rooms[room_idx][room_spot] = '.'
                    new_hallway[hallway_pos] = amphipod_type
                    
                    new_key = state_to_key(new_rooms, new_hallway)
                    heapq.heappush(heap, (cost + move_cost, new_key))
        
        return float('inf')
    
    return dijkstra(initial_key)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()