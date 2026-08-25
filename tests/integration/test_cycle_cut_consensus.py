import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def test_five_validator_cycle_cut_flow():
    owner = create_accounts(1)[0]
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "cycle_cut.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    contract = factory.build_contract(extract_contract_address(receipt), account=owner)
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Infer a directed dependency graph": json.dumps({"edges": [[0, 1], [1, 2], [2, 0]]})}})
    context = {"validators": [v.to_dict() for v in validators], "genvm_datetime": "2026-08-25T12:00:00Z"}
    map_id = f"{str(owner.address).lower()}:RELEASE"
    receipt = contract.infer_map(args=["release", json.dumps(["Collect", "Review", "Publish"]), "Collect must precede Review; Review precedes Publish; and an accidental rule makes Publish precede Collect."]).transact(transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    _ok(contract.cut_suggested(args=[map_id, "Remove the accidental feedback dependency."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(contract.seal_order(args=[map_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.is_sealed_order(args=[map_id, json.dumps([0, 1, 2])]).call() is True
