import networkx as nx
import matplotlib.pyplot as plt
import json
import os

class FlavorGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.ingredient_properties = {}
        
    def add_ingredient(self, ingredient_id, name, properties=None):
        """
        Add an ingredient node to the graph
        """
        if properties is None:
            properties = {}
            
        self.graph.add_node(ingredient_id, name=name)
        self.ingredient_properties[ingredient_id] = {
            "name": name,
            **properties
        }
        
    def add_pairing(self, ingredient1_id, ingredient2_id, affinity_score):
        """
        Add an edge between two ingredients with an affinity score
        """
        if ingredient1_id not in self.graph or ingredient2_id not in self.graph:
            raise ValueError("Both ingredients must be added to the graph first")
            
        self.graph.add_edge(
            ingredient1_id, 
            ingredient2_id, 
            affinity=affinity_score
        )
        
    def get_ingredient_pairings(self, ingredient_id, min_affinity=0.5):
        """
        Get all ingredients that pair well with the given ingredient
        """
        if ingredient_id not in self.graph:
            return []
            
        pairings = []
        for neighbor_id in self.graph.neighbors(ingredient_id):
            affinity = self.graph[ingredient_id][neighbor_id]["affinity"]
            if affinity >= min_affinity:
                pairings.append({
                    "id": neighbor_id,
                    "name": self.graph.nodes[neighbor_id]["name"],
                    "affinity": affinity
                })
                
        return sorted(pairings, key=lambda x: x["affinity"], reverse=True)
        
    def suggest_missing_flavors(self, ingredient_ids, top_n=5):
        """
        Suggest ingredients that would complement the given ingredients
        """
        if not ingredient_ids or not all(i in self.graph for i in ingredient_ids):
            return []
            
        # Create a subgraph of the selected ingredients
        subgraph = self.graph.subgraph(ingredient_ids)
        
        # Find potential ingredients that connect to multiple existing ingredients
        candidates = {}
        
        for ingredient_id in ingredient_ids:
            for neighbor in self.graph.neighbors(ingredient_id):
                if neighbor not in ingredient_ids:
                    if neighbor not in candidates:
                        candidates[neighbor] = {
                            "id": neighbor,
                            "name": self.graph.nodes[neighbor]["name"],
                            "connections": 0,
                            "total_affinity": 0
                        }
                    
                    candidates[neighbor]["connections"] += 1
                    candidates[neighbor]["total_affinity"] += self.graph[ingredient_id][neighbor]["affinity"]
        
        # Calculate average affinity and sort
        for candidate in candidates.values():
            candidate["average_affinity"] = candidate["total_affinity"] / candidate["connections"]
            
        suggestions = sorted(
            candidates.values(),
            key=lambda x: (x["connections"], x["average_affinity"]),
            reverse=True
        )
        
        return suggestions[:top_n]
        
    def visualize(self, ingredient_ids=None, output_file="flavor_graph.png"):
        """
        Visualize the flavor graph or a subset of it
        """
        if ingredient_ids:
            # Include selected ingredients and their neighbors
            nodes_to_show = set(ingredient_ids)
            for ingredient_id in ingredient_ids:
                nodes_to_show.update(self.graph.neighbors(ingredient_id))
                
            subgraph = self.graph.subgraph(nodes_to_show)
            g = subgraph
        else:
            g = self.graph
            
        plt.figure(figsize=(12, 10))
        
        # Use hierarchical layout
        pos = nx.spring_layout(g, seed=42)
        
        # Draw nodes
        node_colors = ['lightblue' if node not in ingredient_ids else 'orange' 
                      for node in g.nodes] if ingredient_ids else 'lightblue'
        
        nx.draw_networkx_nodes(
            g, pos, 
            node_color=node_colors,
            node_size=500, 
            alpha=0.8
        )
        
        # Draw edges with width based on affinity
        edge_widths = [g[u][v]['affinity'] * 2 for u, v in g.edges]
        nx.draw_networkx_edges(
            g, pos, 
            width=edge_widths,
            alpha=0.6
        )
        
        # Add labels
        labels = {node: g.nodes[node]['name'] for node in g.nodes}
        nx.draw_networkx_labels(g, pos, labels, font_size=10)
        
        plt.title("Flavor Pairing Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        
        return output_file
        
    def save(self, filepath="knowledge_base/flavor_graph.json"):
        """
        Save the flavor graph to a JSON file
        """
        data = {
            "nodes": [
                {
                    "id": node_id,
                    "name": self.graph.nodes[node_id]["name"],
                    "properties": self.ingredient_properties.get(node_id, {})
                }
                for node_id in self.graph.nodes
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "affinity": self.graph[u][v]["affinity"]
                }
                for u, v in self.graph.edges
            ]
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self, filepath="knowledge_base/flavor_graph.json"):
        """
        Load a flavor graph from a JSON file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        self.graph = nx.Graph()
        self.ingredient_properties = {}
        
        # Add nodes
        for node in data["nodes"]:
            node_id = node["id"]
            name = node["name"]
            properties = node.get("properties", {})
            
            self.graph.add_node(node_id, name=name)
            self.ingredient_properties[node_id] = {
                "name": name,
                **properties
            }
            
        # Add edges
        for edge in data["edges"]:
            source = edge["source"]
            target = edge["target"]
            affinity = edge["affinity"]
            
            self.graph.add_edge(source, target, affinity=affinity)