from skippy.core.clustercontext import ClusterContext
from skippy.core.model import Pod, Node
from skippy.core.predicates import Predicate


class CheckEdgeNodePred(Predicate):
    def __init__(self, should_be_edge=True) -> None:
        super().__init__()
        self.should_be_edge = should_be_edge

        if should_be_edge:
            self._passes_predicate = self.is_edge_node
        else:
            self._passes_predicate = self.is_not_edge_node

    def passes_predicate(self, context: ClusterContext, pod: Pod, node: Node) -> bool:
        return self._passes_predicate(node)

    def is_edge_node(self, node: Node) -> bool:
        if node.labels.get('locality.skippy.io/type') == 'edge':
            return True
        else:
            return False

    def is_not_edge_node(self, node: Node) -> bool:
        if node.labels.get('locality.skippy.io/type') == 'edge':
            return False
        else:
            return True
        
class CheckCloudNodePred(Predicate):
    def __init__(self, in_cloud=True) -> None:
        super().__init__()
        self.in_cloud = in_cloud

        if in_cloud:
            self._passes_predicate = self.is_in_cloud
        else:
            self._passes_predicate = self.not_in_cloud

    def passes_predicate(self, context: ClusterContext, pod: Pod, node: Node) -> bool:
        return self._passes_predicate(node)

    def is_in_cloud(self, node: Node) -> bool:
        if node.labels.get('locality.skippy.io/type') == 'cloud':
            return True
        else:
            return False

    def not_in_cloud(self, node: Node) -> bool:
        if node.labels.get('locality.skippy.io/type') == 'cloud':
            return False
        else:
            return True