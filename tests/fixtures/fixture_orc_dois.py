from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def fixture_priem_culbert_dois():
    pairs = pd.read_csv(Path(__file__).parent / "jason.list", header=0)
    return list(pairs["DOI"])


@pytest.fixture(scope="session")
def fixture_priem_culbert_oa():
    pairs = pd.read_csv(Path(__file__).parent / "jason.list", header=0)
    return list(pairs["OA"])


@pytest.fixture(scope="session")
def fixture_priem_culbert_both():
    pairs = pd.read_csv(Path(__file__).parent / "jason.list", header=0)
    return list(pairs["DOI"]), list(pairs["OA"])
