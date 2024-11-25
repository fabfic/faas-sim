from typing import Dict

from skippy.core.priorities import Priority
from skippy.core.clustercontext import ClusterContext
from skippy.core.model import Pod, Node, Capacity, ImageState


class EdgeLocalityPriority(Priority):
    """
    EdgeLocalityPriority prefers nodes that have the locality label 'locality.skippy.io/type': 'edge'
    """

    def map_node_score(self, context: ClusterContext, pod: Pod, node: Node) -> int:
        # Either return the priority for the type label or 0
        priority_mapping: Dict[str, int] = {
            # Give edge nodes the highest priority
            'edge': context.max_priority,
            'cloud': 0
        }
        try:
            return priority_mapping.get(node.labels['locality.skippy.io/type'], 0)
        except KeyError:
            return 0

class CloudLocalityPriority(Priority):
    """
    CloudLocalityPriority prefers nodes that have the locality label 'locality.skippy.io/type': 'cloud'
    """

    def map_node_score(self, context: ClusterContext, pod: Pod, node: Node) -> int:
        # Either return the priority for the type label or 0
        priority_mapping: Dict[str, int] = {
            # Give cloud nodes the highest priority
            'cloud': context.max_priority,
            'edge': 0
        }
        try:
            return priority_mapping.get(node.labels['locality.skippy.io/type'], 0)
        except KeyError:
            return 0