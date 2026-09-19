"""Public naming constants and backwards-compatible environment translation.

Constants are checked against project_identity.json. Neither public branding nor
an environment alias changes serialized neuron IDs, data or scientific status.
"""

from __future__ import annotations

from collections.abc import Mapping

PROJECT_NAME = "MHRN"
PROJECT_TITLE = "Multi-Scale Homeostatic Recurrence Network"
PROJECT_SUBTITLE_DE = "Mehrskaliges homöostatisches Rekurrenznetzwerk"
PUBLICATION_TITLE = "Recursive Epistemics in Embodied Spiking Neural Architectures: A Framework for Delegated Agency and Multi-Scale Recurrence"
PUBLICATION_SUBTITLE_DE = "Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen: Ein Framework für delegierte Handlungsmacht und mehrskalige Rekurrenz"
AUTHOR_DISPLAY_NAME = "Thomas Heisig"
AUTHOR_GIVEN_NAMES = "Thomas"
AUTHOR_FAMILY_NAME = "Heisig"
AUTHOR_ORCID = "0009-0002-9589-1872"
AUTHOR_ORCID_URI = f"https://orcid.org/{AUTHOR_ORCID}"
PROJECT_OSF_URI = "https://osf.io/p34uq/"


def public_author_identity() -> dict[str, str]:
    """Return the public author identity used for attribution linking.

    Private contact details from external identity providers are deliberately
    excluded from this project-level identity record.
    """
    return {
        "display_name": AUTHOR_DISPLAY_NAME,
        "given_names": AUTHOR_GIVEN_NAMES,
        "family_name": AUTHOR_FAMILY_NAME,
        "orcid": AUTHOR_ORCID,
        "orcid_uri": AUTHOR_ORCID_URI,
    }


def public_project_resources() -> dict[str, str]:
    """Return public project resources used for provenance linking."""
    return {
        "github": "https://github.com/Thomas-Heisig/MHRN",
        "osf": PROJECT_OSF_URI,
    }


def legacy_environment_aliases(environment: Mapping[str, str]) -> dict[str, str]:
    """New prefix takes precedence, including explicit empty strings.

    Returned keys are only compatibility aliases. Existing legacy-only settings
    remain intact. Values are not logged and permission/safety defaults do not
    change. Call at a process entrypoint before importing runtime configuration.
    """
    return {
        "BRAIN5D_" + key.removeprefix("MHRN_"): value
        for key, value in environment.items()
        if key.startswith("MHRN_") and len(key) > len("MHRN_")
    }
