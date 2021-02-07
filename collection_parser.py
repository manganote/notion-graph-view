import json
import uuid


class CollectionParser:
    def __init__(self, collection):
        self.props = []
        self.relation_props = []
        self.node_set = set()
        self.nodes = []
        self.edges = []
        row_blocks = collection.get_rows()
        self.get_row_props(row_blocks)

        for row in row_blocks:
            self.add_node(row.id, row.title)
            for relation_prop in self.relation_props:
                relation_block_list = row.get_property(relation_prop)
                for rb in relation_block_list:
                    self.add_node(rb.id, rb.title)
                    self.add_edge(row.id, rb.id)

    def get_row_props(self, row_blocks):
        first_block = row_blocks[0]
        for schema in first_block.schema:
            self.props.append(schema['slug'])
            if schema['type'] == 'relation':
                self.relation_props.append(schema['slug'])

    def add_node(self, node_id, node_title):
        if node_id in self.node_set:
            return
        self.node_set.add(node_id)
        self.nodes.append(dict(id=node_id, label=node_title, size=3))

    def add_edge(self, source_id, target_id):
        # self.edges.append(dict(id=str(uuid.uuid1()), source=source_id, target=target_id))
        self.edges.append(dict({"from": source_id, "to": target_id}))

    def get_graph(self):
        graph = dict(nodes=self.nodes, edges=self.edges)
        # return json.dumps(graph, ensure_ascii=False)
        return graph
