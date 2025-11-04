import sys
from collections import deque, defaultdict

def solve(edges):
    # Строим граф
    graph = defaultdict(list)
    gateways = set()
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        if u.isupper():
            gateways.add(u)
        if v.isupper():
            gateways.add(v)
    
    virus_pos = 'a'
    result = []
    
    while True:
        # 1. Находим ВСЕ ближайшие шлюзы от текущей позиции вируса
        distances = {}
        prev = {}
        queue = deque([virus_pos])
        distances[virus_pos] = 0
        prev[virus_pos] = None
        
        while queue:
            current = queue.popleft()
            for neighbor in sorted(graph[current]):  # Сортируем для детерминированности
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    prev[neighbor] = current
                    queue.append(neighbor)
        
        # Находим минимальное расстояние до шлюзов
        min_dist = float('inf')
        for gateway in gateways:
            if gateway in distances:
                min_dist = min(min_dist, distances[gateway])
        
        if min_dist == float('inf'):
            break  # Нет достижимых шлюзов
            
        # Собираем все шлюзы на минимальном расстоянии
        candidate_gateways = [g for g in gateways if g in distances and distances[g] == min_dist]
        target_gateway = min(candidate_gateways)  # Лексикографически наименьший
        
        # 2. Находим следующий шаг вируса к целевому шлюзу
        # Восстанавливаем путь к целевому шлюзу
        path = []
        node = target_gateway
        while node != virus_pos:
            path.append(node)
            node = prev[node]
        path.append(virus_pos)
        path.reverse()
        
        next_node = path[1]  # Следующая позиция вируса
        
        # 3. На этом ходу вирус еще не переместился!
        # Мы должны отключить соединение ДО перемещения вируса
        
        # Находим все возможные соединения для отключения (шлюз-узел)
        possible_cuts = []
        for gateway in gateways:
            for neighbor in graph[gateway]:
                if not neighbor.isupper():  # Только соединения с обычными узлами
                    possible_cuts.append(f"{gateway}-{neighbor}")
        
        if not possible_cuts:
            break
            
        # ВАЖНО: Выбираем лексикографически наименьшее отключение из ВСЕХ возможных
        possible_cuts.sort()
        best_cut = possible_cuts[0]
        result.append(best_cut)
        
        # Удаляем соединение из графа
        g, n = best_cut.split('-')
        graph[g].remove(n)
        graph[n].remove(g)
        
        # 4. Теперь вирус перемещается
        virus_pos = next_node
        
        # Проверяем, не достиг ли вирус шлюза после перемещения
        if virus_pos in gateways:
            break
    
    return result

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            parts = line.split('-')
            if len(parts) == 2:
                edges.append((parts[0], parts[1]))

    result = solve(edges)
    for edge in result:
        print(edge)

if __name__ == "__main__":
    main()