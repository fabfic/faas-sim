import logging
from typing import List, Tuple

from skippy.core.scheduler import Scheduler
from skippy.core.priorities import Priority, BalancedResourcePriority, \
    LatencyAwareImageLocalityPriority, CapabilityPriority, DataLocalityPriority
from ext.fabfic.priorities import CloudLocalityPriority, EdgeLocalityPriority

import ext.fabfic.parametrized_sim as param
from sim.core import Environment
from sim.faassim import Simulation

logger = logging.getLogger(__name__)

#Set this flag true to schedule functions in the cloud
cloud = False

def main():
    logging.basicConfig(level=logging.DEBUG)

    # prepare simulation with topology and benchmark from basic example
    sim = Simulation(param.example_topology(), param.ExampleBenchmark())

    # override the scheduler factory
    sim.create_scheduler = CustomScheduler.create

    # run the simulation
    sim.run()


class CustomScheduler:

    @staticmethod
    def create(env: Environment):
        """
        Factory method that is injected into the Simulation
        """
        logger.info('creating CustomScheduler')

        if cloud:
            priorities: List[Tuple[float, Priority]] = [(1.0, BalancedResourcePriority()),
                                                        (1.0, LatencyAwareImageLocalityPriority()),
                                                        (1.0, CloudLocalityPriority()),
                                                        (1.0, DataLocalityPriority()),
                                                        (1.0, CapabilityPriority())]
            return Scheduler(env.cluster,priorities=priorities)
        else:
            priorities: List[Tuple[float, Priority]] = [(1.0, BalancedResourcePriority()),
                                                        (1.0, LatencyAwareImageLocalityPriority()),
                                                        (1.0, EdgeLocalityPriority()),
                                                        (1.0, DataLocalityPriority()),
                                                        (1.0, CapabilityPriority())]
            return Scheduler(env.cluster,priorities=priorities)


if __name__ == '__main__':
    main()
