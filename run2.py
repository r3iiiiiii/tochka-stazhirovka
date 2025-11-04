import sys
from collections import deque, defaultdict

def solve(edges):
    # Строим граф
    graph = defaultdict(list)
    gateways = set()
    nodes = set()
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        nodes.add(u)
        nodes.add(v)
        # Определяем шлюзы (заглавные буквы)
        if u.isupper():
            gateways.add(u)
        if v.isupper():
            gateways.add(v)
    
    # Текущая позиция вируса
    virus_pos = 'a'
    result = []
    
    # Пока вирус не изолирован
    while True:
        # Находим все шлюзы, до которых можно добраться от текущей позиции вируса
        reachable_gateways = []
        
        # BFS для поиска кратчайших путей ко всем шлюзам
        distances = {virus_pos: 0}
        prev = {virus_pos: None}
        queue = deque([virus_pos])
        
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    prev[neighbor] = current
                    queue.append(neighbor)
        
        # Находим ближайшие шлюзы
        min_dist = float('inf')
        candidate_gateways = []
        
        for gateway in gateways:
            if gateway in distances:
                if distances[gateway] < min_dist:
                    min_dist = distances[gateway]
                    candidate_gateways = [gateway]
                elif distances[gateway] == min_dist:
                    candidate_gateways.append(gateway)
        
        # Если нет достижимых шлюзов - вирус изолирован
        if not candidate_gateways:
            break
        
        # Выбираем лексикографически наименьший шлюз
        target_gateway = min(candidate_gateways)
        
        # Восстанавливаем путь к выбранному шлюзу
        path = []
        current = target_gateway
        while current != virus_pos:
            path.append(current)
            current = prev[current]
        path.append(virus_pos)
        path.reverse()
        
        # Находим следующий узел, куда пойдет вирус
        next_node = path[1]  # path[0] - текущая позиция, path[1] - следующий узел
        
        # Теперь нужно определить, какой коридор отключить
        # Вирус пойдет из virus_pos в next_node по направлению к target_gateway
        # Нам нужно отключить шлюз, к которому ведет этот путь
        
        # Находим все соединения шлюзов с узлами на пути вируса
        critical_edges = []
        
        # Проверяем соединения target_gateway с узлами на пути
        for node in path:
            if node in graph[target_gateway]:
                critical_edges.append((target_gateway, node))
        
        # Если есть несколько критических соединений, выбираем лексикографически наименьшее
        if critical_edges:
            # Сортируем лексикографически (сначала по шлюзу, потом по узлу)
            critical_edges.sort()
            edge_to_cut = min(critical_edges)
        else:
            # Если нет прямых соединений с target_gateway, ищем любой шлюз на пути
            for gateway in gateways:
                for node in path:
                    if node in graph[gateway]:
                        critical_edges.append((gateway, node))
            
            if critical_edges:
                critical_edges.sort()
                edge_to_cut = min(critical_edges)
            else:
                # Если вообще нет шлюзов на пути (маловероятно), берем любой доступный шлюз
                available_edges = []
                for gateway in gateways:
                    for node in graph[gateway]:
                        available_edges.append((gateway, node))
                
                if available_edges:
                    available_edges.sort()
                    edge_to_cut = min(available_edges)
                else:
                    break  # Нет больше шлюзов для отключения
        
        # Форматируем отключаемый коридор (шлюз-узел)
        cut_str = f"{edge_to_cut[0]}-{edge_to_cut[1]}"
        result.append(cut_str)
        
        # Удаляем соединение из графа
        graph[edge_to_cut[0]].remove(edge_to_cut[1])
        graph[edge_to_cut[1]].remove(edge_to_cut[0])
        
        # Перемещаем вирус
        virus_pos = next_node
        
        # Проверяем, не достиг ли вирус шлюза
        if virus_pos in gateways:
            break
    
    return result

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)

if __name__ == "__main__":
    main()