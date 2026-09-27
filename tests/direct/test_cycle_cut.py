import json


NODES = ["Collect", "Review", "Publish"]
TEXT = "Collect must happen before Review. Review must happen before Publish. Publish currently feeds back into Collect."
CYCLIC_EDGES = [[0, 1], [1, 2], [2, 0]]


def _infer(contract, vm, owner, *, key="release", nodes=None, edges=None, text=TEXT):
    vm.sender = owner
    vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": CYCLIC_EDGES if edges is None else edges}))
    return contract.infer_map(key, json.dumps(NODES if nodes is None else nodes), text)


def test_detects_cycle_and_concrete_cut(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice)
    state = contract.get_map(map_id)
    assert state["schema"] == "cyclecut/map/v2"
    assert state["state"] == "CYCLIC"
    assert contract.next_cut(map_id) == [2, 0]


def test_owner_cuts_then_seals_topology(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice)
    contract.cut_suggested(map_id, "Remove the accidental publication feedback dependency.")
    contract.seal_order(map_id)
    assert contract.is_sealed_order(map_id, json.dumps([0, 1, 2])) is True


def test_multiple_cycles_are_cut_one_deterministic_edge_at_a_time(contract, direct_vm, direct_alice):
    nodes = ["Plan", "Review", "Build", "Ship"]
    edges = [[0, 1], [1, 0], [1, 2], [2, 3], [3, 2]]
    map_id = _infer(contract, direct_vm, direct_alice, key="multi", nodes=nodes, edges=edges)
    assert contract.next_cut(map_id) == [1, 0]
    contract.cut_suggested(map_id, "Remove the first feedback dependency from the planning loop.")
    assert contract.next_cut(map_id) == [3, 2]
    contract.cut_suggested(map_id, "Remove the second feedback dependency from the delivery loop.")
    contract.seal_order(map_id)
    state = contract.get_map(map_id)
    assert state["order"] == [0, 1, 2, 3]
    assert [entry["edge"] for entry in state["cuts"]] == [[1, 0], [3, 2]]


def test_topological_order_uses_stable_node_index_tie_break(contract, direct_vm, direct_alice):
    map_id = _infer(
        contract,
        direct_vm,
        direct_alice,
        key="stable",
        nodes=["Draft", "Review", "Publish"],
        edges=[[1, 2], [0, 2]],
    )
    contract.seal_order(map_id)
    assert contract.get_map(map_id)["order"] == [0, 1, 2]


def test_non_owner_cannot_cut(contract, direct_vm, direct_alice, direct_bob):
    map_id = _infer(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.cut_suggested(map_id, "Unauthorized change to dependency semantics.")


def test_non_owner_cannot_seal(contract, direct_vm, direct_alice, direct_bob):
    map_id = _infer(contract, direct_vm, direct_alice, key="seal-auth", edges=[[0, 1], [1, 2]])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.seal_order(map_id)


def test_cyclic_map_cannot_be_sealed_before_cut(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice)
    with direct_vm.expect_revert("map_not_ready"):
        contract.seal_order(map_id)


def test_ready_map_cannot_cut_a_nonexistent_cycle(contract, direct_vm, direct_alice):
    map_id = _infer(contract, direct_vm, direct_alice, key="ready", edges=[[0, 1], [1, 2]])
    with direct_vm.expect_revert("map_not_cyclic"):
        contract.cut_suggested(map_id, "There is no cycle available for an owner-approved cut.")


def test_map_key_is_unique_per_owner(contract, direct_vm, direct_alice):
    _infer(contract, direct_vm, direct_alice)
    with direct_vm.expect_revert("map_exists"):
        _infer(contract, direct_vm, direct_alice)


def test_node_labels_are_unique_case_insensitively(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("duplicate_node"):
        contract.infer_map("duplicate", json.dumps(["Review", " review "]), TEXT)


def test_rejects_self_edge_model_output(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": [[0, 0]]}))
    with direct_vm.expect_revert("[LLM_ERROR] invalid_edge_endpoint"):
        contract.infer_map("self", json.dumps(NODES), TEXT)


def test_rejects_out_of_range_edge_model_output(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": [[0, 3]]}))
    with direct_vm.expect_revert("[LLM_ERROR] invalid_edge_endpoint"):
        contract.infer_map("range", json.dumps(NODES), TEXT)


def test_rejects_duplicate_edges(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": [[0, 1], [0, 1]]}))
    with direct_vm.expect_revert("[LLM_ERROR] duplicate_edge"):
        contract.infer_map("duplicate-edge", json.dumps(NODES), TEXT)


def test_rejects_non_integer_edge_endpoints(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": [[True, 1]]}))
    with direct_vm.expect_revert("[LLM_ERROR] invalid_edge"):
        contract.infer_map("bool-edge", json.dumps(NODES), TEXT)


def test_edge_limit_is_checked_before_processing_model_items(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    edges = [[source, target] for source in range(10) for target in range(10) if source != target][:37]
    direct_vm.mock_llm(r".*Infer a directed dependency graph.*", json.dumps({"edges": edges}))
    with direct_vm.expect_revert("[LLM_ERROR] edge_limit"):
        contract.infer_map("edge-limit", json.dumps([f"Node {index}" for index in range(10)]), TEXT)


def test_model_output_has_one_exact_json_field(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(
        r".*Infer a directed dependency graph.*",
        json.dumps({"edges": [[0, 1]], "explanation": "extra fields are forbidden"}),
    )
    with direct_vm.expect_revert("[LLM_ERROR] wrong_edge_shape"):
        contract.infer_map("shape", json.dumps(NODES), TEXT)
