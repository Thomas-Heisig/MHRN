"""Bounded literature context for exploratory PAN geometry."""

from __future__ import annotations

GEOMETRY_LITERATURE: tuple[dict[str, object], ...] = (
    {
        "key": "barthelemy_spatial_networks_2011",
        "citation": (
            "Barthélemy, M. (2011). Spatial networks. Physics Reports "
            "499(1-3), 1-101."
        ),
        "doi": "10.1016/j.physrep.2010.11.002",
        "supports": (
            "Spatial embedding and edge-length costs can strongly shape "
            "network topology and dynamics."
        ),
    },
    {
        "key": "krioukov_hyperbolic_2010",
        "citation": (
            "Krioukov, D. et al. (2010). Hyperbolic geometry of complex "
            "networks. Physical Review E 82:036106."
        ),
        "doi": "10.1103/PhysRevE.82.036106",
        "supports": (
            "Hidden metric geometry can generate heterogeneous degree "
            "distributions and clustering in complex-network models."
        ),
    },
    {
        "key": "lin_drosophila_connectome_2024",
        "citation": (
            "Lin, A. et al. (2024). Network statistics of the whole-brain "
            "connectome of Drosophila. Nature."
        ),
        "doi": "10.1038/s41586-024-07968-y",
        "supports": (
            "Whole-brain Drosophila connection probability varies with "
            "distance between approximated axonal and dendritic arbors."
        ),
    },
    {
        "key": "constantinescu_gridlike_concepts_2016",
        "citation": (
            "Constantinescu, A. O.; O'Reilly, J. X.; Behrens, T. E. J. "
            "(2016). Organizing conceptual knowledge in humans with a "
            "gridlike code. Science 352(6292), 1464-1468."
        ),
        "doi": "10.1126/science.aaf0941",
        "supports": (
            "Grid-like coding can generalize to a two-dimensional conceptual "
            "space in humans."
        ),
        "does_not_establish": (
            "Biological evidence for the specific PAN geometric 5D axes or "
            "for a 4-6 dimensional Drosophila connectome embedding."
        ),
    },
)


def geometry_literature_context() -> dict[str, object]:
    return {
        "classification": "PLAYGROUND_GEOMETRY_LITERATURE",
        "scientific_evidence_for_pan_geometry": False,
        "novelty_status": (
            "TARGETED_SEARCH_NO_XYZ_PLUS_TWO_TOROIDAL_PAN_EQUIVALENT_IDENTIFIED"
        ),
        "caveats": [
            (
                "Two independent cyclic coordinates define a torus S1 x S1; "
                "a Klein bottle requires a twisted identification and is not "
                "implemented."
            ),
            (
                "The additive mixed metric cannot create spatially-far "
                "topologically-near shortcuts because it is never shorter "
                "than the xyz distance."
            ),
            (
                "No universal d>=3 small-world threshold was identified; "
                "small-world behavior depends on the graph construction."
            ),
            (
                "The targeted search did not substantiate a claim that the "
                "Drosophila connectome has an established effective dimension "
                "between 4 and 6."
            ),
        ],
        "sources": [dict(item) for item in GEOMETRY_LITERATURE],
    }
