from tests.unit.test_b_compiler import make_contract, profile

from pp_food_runtime.stage_b.compiler import compile_stage_b


def test_same_contract_same_profile_same_prompt():
    first = compile_stage_b(make_contract(), profile())
    second = compile_stage_b(make_contract(), profile())
    assert first.text == second.text
    assert first.sha256 == second.sha256
