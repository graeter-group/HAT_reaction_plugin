import MDAnalysis as MDA
from pathlib import Path
from HATreaction.utils.trajectory_utils import find_radical_pos
import json


def make_references(save_all=False, show=True):
    import nglview as ngl

    ref_json = Path(__file__).parent / "test_rad_pos" / "reference.json"
    ref_d = {}
    if ref_json.exists():
        with open(ref_json) as f:
            ref_d = json.load(f)

    for pdb in (Path(__file__).parent / "test_rad_pos").glob("*.pdb"):
        u = MDA.Universe(pdb)

        view = ngl.show_mdanalysis(u)
        view.clear()
        view.representations = [
            {
                "type": "ball+stick",
                "params": {
                    "sele": "all",
                },
            },
            {
                "type": "label",
                "params": {
                    "sele": "all",
                    "color": "black",
                    "labelType": "atomindex",
                },
            },
        ]

        idx = pdb.stem.split("_")[-1]

        test_atom = u.select_atoms(f"index {idx}")[0]
        test_atom_bonded = test_atom.bonded_atoms

        rad_poss = find_radical_pos(test_atom, test_atom_bonded)
        sorted(rad_poss, key=lambda a: a[0])
        rad_poss = [list(pos.astype(float)) for pos in rad_poss]

        print(pdb.name)
        for rad_pos in rad_poss:
            view.shape.add("sphere", rad_pos, (0.8, 0.4, 0.3), 0.4, 0.5)
        if show:
            yield view

        response = "y"
        if not save_all:
            response = input("Save prediction? [y/n]")

        if response.lower() == "y":
            ref_d[pdb.name] = rad_poss
            with open(ref_json, "w") as f:
                json.dump(ref_d, f, indent=2)

        print(ref_d[pdb.name] == rad_poss, ref_d[pdb.name], rad_poss)


def test_radical_pos():
    ref_json = Path(__file__).parent / "test_rad_pos" / "reference.json"
    if ref_json.exists():
        with open(ref_json) as f:
            ref_d = json.load(f)

    for pdb in (Path(__file__).parent / "test_rad_pos").glob("*.pdb"):
        u = MDA.Universe(pdb)
        idx = pdb.stem.split("_")[-1]

        test_atom = u.select_atoms(f"index {idx}")[0]
        test_atom_bonded = test_atom.bonded_atoms

        rad_poss = find_radical_pos(test_atom, test_atom_bonded)
        sorted(rad_poss, key=lambda a: a[0])
        rad_poss = [list(pos.astype(float)) for pos in rad_poss]

        assert ref_d[pdb.name] == rad_poss
