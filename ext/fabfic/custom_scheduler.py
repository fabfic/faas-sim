import logging
from typing import List

from skippy.core.scheduler import Scheduler
from ext.fabfic.predicates import CheckEdgeNodePred
from skippy.core.predicates import Predicate, PodFitsResourcesPred, CheckNodeLabelPresencePred

import ext.fabfic.parametrized_sim as param
from sim.core import Environment
from sim.faassim import Simulation

logger = logging.getLogger(__name__)

#Set this flag true to schedule functions in the cloud
cloud = True

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
            predicates: List[Predicate] = [
                PodFitsResourcesPred(),
                CheckNodeLabelPresencePred(['data.skippy.io/storage'], False),
                CheckEdgeNodePred(False)
            ]
            return Scheduler(env.cluster, predicates=predicates)
        else:
            predicates: List[Predicate] = [
                PodFitsResourcesPred(),
                CheckNodeLabelPresencePred(['data.skippy.io/storage'], False),
                CheckEdgeNodePred(True)
            ]
            return Scheduler(env.cluster, predicates=predicates)


if __name__ == '__main__':
    main()
