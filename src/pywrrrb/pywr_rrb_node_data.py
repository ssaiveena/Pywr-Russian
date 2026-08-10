"""Node and connection data for the Russian River Basin."""

immediate_downstream_nodes_dict = {
    "junction20": "vanArsdale",
    "vanArsdale": "junction21",
    "junction21": "downstreamVanArsdale",
    "potterValleyProject": "calpella",
    "calpella": "mendocinoInflow",
    "mendocinoInflow": "lakeMendocino",
    "lakeMendocino": "lakeMendocinoOutflow",
    "lakeMendocinoOutflow": "eastWestJunction",
    "westForkInflow": "eastWestJunction",
    "eastWestJunction": "hopland",
    "hopland": "cloverdale",
    "cloverdale": "healdsburg",
    "sonomaInflow": "lakeSonoma",
    "lakeSonoma": "lakeSonomaOutflow",
    "lakeSonomaOutflow": "dryCreekNearGeyserville",
    "dryCreekNearGeyserville": "aboveDryCreekDiversionDam",
    "aboveDryCreekDiversionDam": "dryCreekDiversionDam",
    "dryCreekDiversionDam": "dryCreek",
    "dryCreek": "dryCreekRR",
    "healdsburg": "dryCreekRR",
    "dryCreekRR": "upstreamScwaWithdrawal",
    "upstreamScwaWithdrawal": "scwaDiversionDam",
    "scwaDiversionDam": "scwaWithdrawal",
    "scwaWithdrawal": "markWestCreek",
    "markWestCreek": "hacienda",
    "hacienda": "ocean",
}

downstream_node_lags = {
    node: 0 for node in immediate_downstream_nodes_dict
}
downstream_node_lags.update(
    {
        "hopland": 1,
        "cloverdale": 2,
        "dryCreekNearGeyserville": 1,
        "dryCreekRR": 1,
        "markWestCreek": 1,
    }
)

diversion_nodes_dict = {
    "calpella": ["calpellaDiversion"],
    "hopland": ["hoplandDiversion"],
    "cloverdale": ["cloverdaleDiversion"],
    "healdsburg": ["healdsburgDiversion"],
    "hacienda": ["rrcwdDiversion"],
}

catchment_nodes_dict = {
    "nerfRelease": "junction20",
    "westForkHeadwater": "westForkInflow",
    "lakeSonomaHeadwater": "sonomaInflow",
}

interbasin_transfer_edges = [
    ("vanArsdale", "potterValleyProject"),
]
