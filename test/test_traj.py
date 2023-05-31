#%%
from pathlib import Path
from HATreaction import HAT_reaction
import pickle
import json
import pytest
from pprint import pprint

#%%
class DummyClass:
    pass

class DummyRunmanager:
    config = DummyClass()
    config.reactions = DummyClass()
    config.reactions.Hat_reaction = DummyClass()
    config.reactions.Hat_reaction.h_cutoff = 3
    config.reactions.Hat_reaction.frequency_factor = 1e8
    config.reactions.Hat_reaction.polling_rate = 10
    radical_idxs = []

@pytest.fixture
def recipe_collection(tmpdir):
    
    plgn = HAT_reaction("Hat_reaction", DummyRunmanager())

    files = DummyClass()
    files.input = {
        "tpr": Path(__file__).parent / "test_traj_io" / "equilibrium1.tpr",
        "trr": Path(__file__).parent / "test_traj_io" / "equilibrium1.trr",
    }
    files.outputdir = Path(tmpdir)

    return plgn.get_recipe_collection(files)

def test_traj_to_recipes(recipe_collection):
    
    assert len(recipe_collection.recipes) == 5
    recipe_collection.aggregate_reactions()
    assert len(recipe_collection.recipes) == 5
    
    for recipe in recipe_collection.recipes:
        assert len(recipe.rates) == 3
        assert len(recipe.timespans) == 3





