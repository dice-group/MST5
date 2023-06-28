from components.Knowledge_graph import Knowledge_graph

class Query:
    def __init__(self, sparql: str, knowledge_graph: Knowledge_graph) -> None:
        self.sparql = sparql
        self.knowledge_graph = knowledge_graph