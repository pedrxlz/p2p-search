import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import json


def create_network(config):
    G = nx.Graph()
    for node in config["resources"]:
        G.add_node(node, resources=config["resources"][node])
    G.add_edges_from(config["edges"])
    return G


def validate_network(G, config):
    if not nx.is_connected(G):
        raise ValueError("A rede não está conectada!")
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if (
            len(neighbors) < config["min_neighbors"]
            or len(neighbors) > config["max_neighbors"]
        ):
            raise ValueError(f"O nó {node} viola os limites de vizinhos!")
        if not G.nodes[node].get("resources"):
            raise ValueError(f"O nó {node} não possui recursos!")
    if any(u == v for u, v in G.edges()):
        raise ValueError("A rede possui loops!")
    return True


def visualize_network(G):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx(
        G, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10
    )
    plt.title("Rede P2P")
    plt.show()


def flooding_search(G, start_node, target_resource, ttl):
    visited = set()
    queue = [(start_node, 0)]  # (nó, profundidade)
    messages = 0
    frames = []  # Para a animação
    pos = nx.spring_layout(G, seed=42)

    while queue:
        node, depth = queue.pop(0)
        if depth > ttl or node in visited:
            continue
        visited.add(node)

        # Atualiza o frame da animação
        node_colors = ["red" if n in visited else "skyblue" for n in G.nodes()]
        frames.append((node_colors, list(visited)))

        if target_resource in G.nodes[node]["resources"]:
            return (
                len(visited),
                messages,
                f"Recurso {target_resource} encontrado no nó {node}.",
                frames,
            )
        for neighbor in G.neighbors(node):
            messages += 1
            queue.append((neighbor, depth + 1))

    return len(visited), messages, f"Recurso {target_resource} não encontrado.", frames


def random_walk_search(G, start_node, target_resource, ttl):
    visited = set()
    current_node = start_node
    messages = 0
    frames = []  # Para a animação
    pos = nx.spring_layout(G, seed=42)

    for _ in range(ttl):
        visited.add(current_node)

        # Atualiza o frame da animação
        node_colors = ["red" if n in visited else "skyblue" for n in G.nodes()]
        frames.append((node_colors, list(visited)))

        if target_resource in G.nodes[current_node]["resources"]:
            return (
                len(visited),
                messages,
                f"Recurso {target_resource} encontrado no nó {current_node}.",
                frames,
            )
        neighbors = list(G.neighbors(current_node))
        if not neighbors:
            break
        current_node = random.choice(neighbors)
        messages += 1

    return len(visited), messages, f"Recurso {target_resource} não encontrado.", frames


def depth_first_search(G, start_node, target_resource, ttl):
    visited = set()
    stack = [(start_node, 0)]
    messages = 0
    frames = []
    pos = nx.spring_layout(G, seed=42)

    while stack:
        node, depth = stack.pop()
        if depth > ttl or node in visited:
            continue
        visited.add(node)

        node_colors = ["red" if n in visited else "skyblue" for n in G.nodes()]
        frames.append((node_colors, list(visited)))

        if target_resource in G.nodes[node]["resources"]:
            return (
                len(visited),
                messages,
                f"Recurso {target_resource} encontrado no nó {node}.",
                frames,
            )
        for neighbor in G.neighbors(node):
            messages += 1
            stack.append((neighbor, depth + 1))

    return len(visited), messages, f"Recurso {target_resource} não encontrado.", frames


def animate_search(G, frames, pos):
    fig, ax = plt.subplots(figsize=(8, 8))

    def update(frame):
        ax.clear()
        node_colors, visited_nodes = frame
        nx.draw_networkx(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=700,
            font_size=10,
            ax=ax,
        )
        ax.set_title(f"Nós visitados: {len(visited_nodes)}")

    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=1000, repeat=False
    )
    plt.show()


with open("config.json", "r") as f:
    CONFIG = json.load(f)


G = create_network(CONFIG)
validate_network(G, CONFIG)

visualize_network(G)

node_id = "n1"
resource_id = "r7"
ttl = 8
algorithm = "random_walk"

if algorithm == "flooding":
    visited, messages, result, frames = flooding_search(G, node_id, resource_id, ttl)
elif algorithm == "random_walk":
    visited, messages, result, frames = random_walk_search(G, node_id, resource_id, ttl)
elif algorithm == "depth_first":
    visited, messages, result, frames = depth_first_search(G, node_id, resource_id, ttl)
else:
    raise ValueError("Algoritmo de busca inválido!")

print(f"Resultado: {result}")
print(f"Número total de nós envolvidos: {visited}")
print(f"Número total de mensagens trocadas: {messages}")

pos = nx.spring_layout(G, seed=42)
animate_search(G, frames, pos)
