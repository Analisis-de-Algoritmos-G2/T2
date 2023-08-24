from nltk.tokenize import word_tokenize
from neo4j import GraphDatabase
import networkx as nx
import itertools
import os


def create_node4j_map(file):

    with open(file, "r", encoding="utf-8") as file:
        text = file.read().lower()

    tokens = word_tokenize(text)
    bigrams = list(itertools.combinations(tokens, 2))
    graph = nx.Graph()

    for bigram in bigrams:
        if graph.has_edge(bigram[0], bigram[1]):
            graph[bigram[0]][bigram[1]]["weight"] += 1
        else:
            graph.add_edge(bigram[0], bigram[1], weight=1)

    # 2. Creación de nodos y relaciones en Neo4j
    uri = "bolt://localhost:7687"  # Asume que Neo4j está corriendo localmente
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    def add_edge_to_neo4j(tx, word1, word2, weight):
        query = (
            "MERGE (a:Word {name: $word1})"
            "MERGE (b:Word {name: $word2})"
            "MERGE (a)-[r:COOCCURS]->(b)"
            "SET r.weight = $weight"
        )
        tx.run(query, word1=word1, word2=word2, weight=weight)

    with driver.session() as session:
        for edge in graph.edges(data=True):
            session.write_transaction(add_edge_to_neo4j, edge[0], edge[1], edge[2]['weight'])

    driver.close()