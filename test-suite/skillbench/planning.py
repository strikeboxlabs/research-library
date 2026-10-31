from __future__ import annotations

from pathlib import Path
import random
import re

from .common import metadata


def library_inventory(library):
    return {p.name: metadata(p) for p in sorted((Path(library) / "skills").iterdir())
            if p.is_dir() and not p.is_symlink() and (p / "SKILL.md").is_file()}


def choose_skills(target, inventory, size, method, seed):
    if target not in inventory:
        raise ValueError(f"Target skill missing: {target}")
    if size > len(inventory):
        raise ValueError(f"Requested {size} skills but only {len(inventory)} are available")
    others = sorted(set(inventory) - {target})
    rng = random.Random(seed)
    rng.shuffle(others)
    if method == "similar":
        # Lexical overlap is only a cheap source of potential distractors, never a correctness score.
        words = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))
        query = words(inventory[target]["description"])
        def similarity(name):
            tokens = words(inventory[name]["description"])
            return len(query & tokens) / max(1, len(query | tokens))
        others.sort(key=similarity, reverse=True)
    selected = [target] + others[:size - 1]
    rng.shuffle(selected)
    return selected


def build_plan(config, inventory):
    from .cases import CASES
    blocks = []
    for case_id in config["cases"]:
        case = CASES[case_id]
        for repeat in range(config["repetitions"]):
            # Same world and advertised order for every arm within this block.
            seed = config["seed"] + repeat
            selected = choose_skills(case.skill, inventory, config["selection"]["catalog_size"],
                                     config["selection"]["distractors"], seed)
            arms = list(config["conditions"])
            random.Random(f"{config['seed']}:{case_id}:{repeat}").shuffle(arms)
            block = f"{case_id}-{repeat:03d}"
            blocks.append([{"trial_id": f"{block}-{arm}", "block_id": block, "case_id": case_id,
                            "family": case.family, "split": case.split, "skill": case.skill,
                            "repeat": repeat, "seed": seed, "condition": arm,
                            "selected_skills": [] if arm == "baseline" else selected,
                            "mode": config["selection"]["mode"]} for arm in arms])
    random.Random(config["seed"]).shuffle(blocks)
    return [trial for block in blocks for trial in block]
