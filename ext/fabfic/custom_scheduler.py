import logging
from typing import List, Tuple

from skippy.core.predicates import Predicate, PodFitsResourcesPred, CheckNodeLabelPresencePred
from ext.fabfic.predicates import CheckCloudNodePred, CheckEdgeNodePred
from skippy.core.scheduler import Scheduler
from skippy.core.priorities import Priority, BalancedResourcePriority, \
    LatencyAwareImageLocalityPriority, CapabilityPriority, DataLocalityPriority
from ext.fabfic.priorities import CloudLocalityPriority, EdgeLocalityPriority

import ext.fabfic.parametrized_sim as param
from sim.core import Environment
from sim.faassim import Simulation

logger = logging.getLogger(__name__)

#Set this flag true to schedule functions in the cloud
consider_cloud_nodes = False

def main():
    logging.basicConfig(level=logging.DEBUG)

    # prepare simulation with topology and benchmark from basic example
    sim = Simulation(param.example_topology(), param.ExampleBenchmark())

    # override the scheduler factory
    sim.create_scheduler = CustomScheduler.create

    # run the simulation
    sim.run()


class CustomScheduler:
    '''
    This scheduler puts into consideration the locality of the node 
    by implementig  a cloud/edge locality scheduling policy.
    Use priorities to affect the scoring of nodes during scheduling.
    Use predicates to completely remove cloud/edge nodes from scheduling.
    '''

    @staticmethod
    def create(env: Environment):
        """
        Factory method that is injected into the Simulation
        """
        logger.info('creating CustomScheduler')

        if consider_cloud_nodes:
            priorities: List[Tuple[float, Priority]] = [(1.0, BalancedResourcePriority()),
                                                        (1.0, LatencyAwareImageLocalityPriority()),
                                                        (1.0, CloudLocalityPriority()),
                                                        (1.0, DataLocalityPriority()),
                                                        (1.0, CapabilityPriority())]
            #Add predicates to completely exclude edge node from scheduling
            # predicates: List[Predicate] = [
            #                                 PodFitsResourcesPred(),
            #                                 CheckNodeLabelPresencePred(['data.skippy.io/storage'], False),
            #                                 CheckCloudNodePred()
            #                             ]
            return Scheduler(env.cluster,priorities=priorities)
        else:
            priorities: List[Tuple[float, Priority]] = [(1.0, BalancedResourcePriority()),
                                                        (1.0, LatencyAwareImageLocalityPriority()),
                                                        (1.0, EdgeLocalityPriority()),
                                                        (1.0, DataLocalityPriority()),
                                                        (1.0, CapabilityPriority())]
            #Add predicates to completely exclude cloud node from scheduling
            # predicates: List[Predicate] = [
            #                                 PodFitsResourcesPred(),
            #                                 CheckNodeLabelPresencePred(['data.skippy.io/storage'], False),
            #                                 CheckEdgeNodePred()
            #                             ]
            return Scheduler(env.cluster,priorities=priorities)


if __name__ == '__main__':
    main()
