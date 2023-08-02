class Graph:
    def __init__(self):
        self.adj_list = {}
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.node_count += 1

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)
        self.adj_list[node1][node2] = weight
        self.edge_count += 1

    def there_is_edge(self, node1, node2):
        if node1 in self.adj_list and node2 in self.adj_list[node1]:
            return True
        return False

    def increment_edge_weight(self, node1, node2):
        if self.there_is_edge(node1, node2):
            self.adj_list[node1][node2] += 1
        else:
            print(f"ERROR! There is no edge between {node1} and {node2}")


    def add_vote_to_a_politician(self, node, weight):
        if node not in self.adj_list:
            raise ValueError ("The node {node} hasn't been found")
        self.adj_list[node]["vote"] = weight


    def __str__(self):
        output = ""
        for node in self.adj_list:
            output += str(node) + " -> "
            neighbors = self.adj_list[node]
            for neighbor, weight in neighbors.items():
                output += f"{neighbor} {weight}, "
            output = output.rstrip(", ") + "\n"
        return output
    
    def lowest_edge(self):
        lower = float("-inf")

        
        for node1 in self.adj_list:
            for node2 in self.adj_list[node1]:
                if(self.adj_list[node1][node2]>lower):
                    lower = self.adj_list[node1][node2]
        return lower
    
