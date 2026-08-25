import json


NODES = json.dumps(["Collect", "Review", "Publish"])
TEXT = "Collect must happen before Review. Review must happen before Publish. Publish currently feeds back into Collect."
EDGES = {"edges": [[0, 1], [1, 2], [2, 0]]}


def _infer(contract, vm, owner):
    vm.sender = owner
    vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps(EDGES))
    return contract.infer_map("release", NODES, TEXT)


def test_detects_cycle_and_concrete_cut(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice)
    assert contract.get_map(map_id)["state"] == "CYCLIC"
    assert contract.next_cut(map_id) == [2, 0]


def test_owner_cuts_then_seals_topology(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    contract.cut_suggested(map_id, "Remove the accidental publication feedback dependency.")
    contract.seal_order(map_id)
    assert contract.is_sealed_order(map_id, json.dumps([0, 1, 2])) is True


def test_non_owner_cannot_cut(contract, direct_vm, direct_alice, direct_bob):
    map_id = _infer(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.cut_suggested(map_id, "Unauthorized change to dependency semantics.")


def test_rejects_self_edge_model_output(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": [[0, 0]]}))
    with direct_vm.expect_revert("[LLM_ERROR] invalid_edge_endpoint"):
        contract.infer_map("bad", NODES, TEXT)
