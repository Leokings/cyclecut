import json
import os
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address

from tests.studionet_support import emit_record, ok, source_schema_proof, wallet_accounts


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("RUN_STUDIONET") != "1", reason="opt-in live StudioNet test"),
]


def test_studionet_dependency_cycle_cut():
    accounts = wallet_accounts("cyclecut", 1)
    owner = accounts[0]
    source = Path(__file__).resolve().parents[2] / "contracts" / "cycle_cut.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=owner)
    map_id = f"{str(owner.address).lower()}:RELEASE"
    intelligent = ok(contract.infer_map(args=["release", json.dumps(["Collect", "Review", "Publish"]), "Collect must precede Review. Review must precede Publish. An accidental feedback rule says Publish must precede Collect." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = contract.get_map(args=[map_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "cyclecut/map/v2" and state["state"] in ("CYCLIC", "READY")
    actions = []
    for _ in range(10):
        if state["state"] != "CYCLIC":
            break
        actions.append(ok(contract.cut_suggested(args=[map_id, "Remove the deterministic feedback edge proposed by the contract."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
        state = contract.get_map(args=[map_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["state"] == "READY"
    actions.append(ok(contract.seal_order(args=[map_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    state = contract.get_map(args=[map_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["state"] == "SEALED" and len(state["order"]) == 3
    proof = source_schema_proof(address, source, {"infer_map", "cut_suggested", "seal_order", "next_cut", "is_sealed_order"})
    emit_record("cyclecut", "A", address, deployed, actions, intelligent, accounts, proof, {"state": state["state"], "edge_count": len(state["edges"]), "cuts": state["cuts"], "order": state["order"]})
