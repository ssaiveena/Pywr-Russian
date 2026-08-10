"""Build the Russian River Basin Pywr model."""

import json

from pywrrrb.pywr_rrb_node_data import (
    catchment_nodes_dict,
    diversion_nodes_dict,
    immediate_downstream_nodes_dict,
    interbasin_transfer_edges,
)
from pywrrrb.utils.lists import (
    diversion_list,
    majorflow_list,
    output_list,
    reservoir_list,
)

__all__ = ["ModelBuilder"]


class ModelBuilder:
    """Build the Russian River Basin model dictionary."""

    def __init__(
        self,
        start_date,
        end_date,
        inflow_type=None,
        diversion_type=None,
        options=None,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.timestep = 1
        self.inflow_type = inflow_type
        self.diversion_type = inflow_type if diversion_type is None else diversion_type
        self.options = {} if options is None else dict(options)
        self.reset_model_dict()

    def reset_model_dict(self):
        """Reset the model dictionary."""
        self.reservoirs = []
        self.model_dict = {
            "metadata": {
                "title": "RRB",
                "description": "Pywr Russian River Basin representation",
                "minimum_version": "0.4",
            },
            "timestepper": {
                "start": self.start_date,
                "end": self.end_date,
                "timestep": self.timestep,
            },
            "scenarios": [{"name": "inflow", "size": 1}],
            "nodes": [],
            "edges": [],
            "parameters": {},
        }
        self.edges = self.model_dict["edges"]
        self.parameters = self.model_dict["parameters"]

    @staticmethod
    def _node_name(name):
        if name in reservoir_list:
            return f"reservoir_{name}"
        if name in output_list or name in diversion_list:
            return f"output_{name}"
        return f"link_{name}"

    def make_model(self):
        """Build the model nodes and edges."""
        self.reset_model_dict()
        nodes = self.model_dict["nodes"]

        for reservoir in reservoir_list:
            nodes.append(
                {
                    "name": self._node_name(reservoir),
                    "type": "storage",
                    "max_volume": 1.0,
                    "initial_volume": 0.0,
                }
            )
            self.reservoirs.append(reservoir)

        for node in majorflow_list:
            nodes.append({"name": self._node_name(node), "type": "link"})

        for node in output_list + diversion_list:
            nodes.append({"name": self._node_name(node), "type": "output"})

        for node, downstream_node in catchment_nodes_dict.items():
            node_name = f"catchment_{node}"
            nodes.append({"name": node_name, "type": "catchment", "flow": 0.0})
            self.edges.append([node_name, self._node_name(downstream_node)])

        for node, downstream_node in immediate_downstream_nodes_dict.items():
            self.edges.append(
                [self._node_name(node), self._node_name(downstream_node)]
            )

        for node, diversions in diversion_nodes_dict.items():
            for diversion in diversions:
                self.edges.append(
                    [self._node_name(node), self._node_name(diversion)]
                )

        for node, downstream_node in interbasin_transfer_edges:
            self.edges.append(
                [self._node_name(node), self._node_name(downstream_node)]
            )

    def write_model(self, model_filename):
        """Write the model dictionary to JSON."""
        with open(model_filename, "w") as output_file:
            json.dump(self.model_dict, output_file, indent=4)
