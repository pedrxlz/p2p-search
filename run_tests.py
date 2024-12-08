import json
import time

from main import create_network, flooding_search, random_walk_search

algorithms = {
    "flooding": flooding_search,
    "random_walk": random_walk_search,
}


def test_search_algorithms(G, node_id, resource_id, ttl):
    results = {}

    for algorithm in algorithms:
        # Test without cache
        cache = {}
        start_time = time.time()

        visited, messages, result, frames = algorithms[algorithm](
            G, node_id, resource_id, ttl, cache
        )

        end_time = time.time()
        results[f"{algorithm}_no_cache"] = {
            "visited": visited,
            "messages": messages,
            "result": result,
            "time": end_time - start_time,
        }

        # Test with cache
        cache = {}

        # First run to populate the cache
        visited, messages, result, frames = algorithms[algorithm](
            G, node_id, resource_id, ttl, cache
        )

        start_time = time.time()
        visited, messages, result, frames = algorithms[algorithm](
            G, node_id, resource_id, ttl, cache
        )

        end_time = time.time()
        results[f"{algorithm}_with_cache"] = {
            "visited": visited,
            "messages": messages,
            "result": result,
            "time": end_time - start_time,
        }

    return results


with open("config.json", "r") as f:
    CONFIG = json.load(f)

G = create_network(CONFIG)


results = test_search_algorithms(G, node_id="n1", resource_id="r7", ttl=8)

for key, value in results.items():
    print(f"Algoritmo: {key}")
    print(f"Resultado: {value['result']}")
    print(f"Número total de nós envolvidos: {value['visited']}")
    print(f"Número total de mensagens trocadas: {value['messages']}")
    print(f"Tempo de execução: {value['time']} segundos")
    print()
