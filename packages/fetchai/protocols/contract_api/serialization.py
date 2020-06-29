# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020 fetchai
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Serialization module for contract_api protocol."""

from typing import Any, Dict, cast

from aea.protocols.base import Message
from aea.protocols.base import Serializer

from packages.fetchai.protocols.contract_api import contract_api_pb2
from packages.fetchai.protocols.contract_api.custom_types import RawTransaction
from packages.fetchai.protocols.contract_api.custom_types import SignedTransaction
from packages.fetchai.protocols.contract_api.custom_types import Terms
from packages.fetchai.protocols.contract_api.custom_types import TransactionReceipt
from packages.fetchai.protocols.contract_api.message import ContractApiMessage


class ContractApiSerializer(Serializer):
    """Serialization for the 'contract_api' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'ContractApi' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(ContractApiMessage, msg)
        contract_api_msg = contract_api_pb2.ContractApiMessage()
        contract_api_msg.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        contract_api_msg.dialogue_starter_reference = dialogue_reference[0]
        contract_api_msg.dialogue_responder_reference = dialogue_reference[1]
        contract_api_msg.target = msg.target

        performative_id = msg.performative
        if performative_id == ContractApiMessage.Performative.GET_STATE:
            performative = contract_api_pb2.ContractApiMessage.Get_State_Performative()  # type: ignore
            ledger_id = msg.ledger_id
            performative.ledger_id = ledger_id
            contract_address = msg.contract_address
            performative.contract_address = contract_address
            callable = msg.callable
            performative.callable = callable
            kwargs = msg.kwargs
            performative.kwargs.update(kwargs)
            contract_api_msg.get_state.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.GET_RAW_TRANSACTION:
            performative = contract_api_pb2.ContractApiMessage.Get_Raw_Transaction_Performative()  # type: ignore
            ledger_id = msg.ledger_id
            performative.ledger_id = ledger_id
            terms = msg.terms
            Terms.encode(performative.terms, terms)
            contract_api_msg.get_raw_transaction.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.SEND_SIGNED_TRANSACTION:
            performative = contract_api_pb2.ContractApiMessage.Send_Signed_Transaction_Performative()  # type: ignore
            ledger_id = msg.ledger_id
            performative.ledger_id = ledger_id
            signed_transaction = msg.signed_transaction
            SignedTransaction.encode(
                performative.signed_transaction, signed_transaction
            )
            contract_api_msg.send_signed_transaction.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.GET_TRANSACTION_RECEIPT:
            performative = contract_api_pb2.ContractApiMessage.Get_Transaction_Receipt_Performative()  # type: ignore
            ledger_id = msg.ledger_id
            performative.ledger_id = ledger_id
            transaction_digest = msg.transaction_digest
            performative.transaction_digest = transaction_digest
            contract_api_msg.get_transaction_receipt.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.BALANCE:
            performative = contract_api_pb2.ContractApiMessage.Balance_Performative()  # type: ignore
            balance = msg.balance
            performative.balance = balance
            contract_api_msg.balance.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.RAW_TRANSACTION:
            performative = contract_api_pb2.ContractApiMessage.Raw_Transaction_Performative()  # type: ignore
            raw_transaction = msg.raw_transaction
            RawTransaction.encode(performative.raw_transaction, raw_transaction)
            contract_api_msg.raw_transaction.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.TRANSACTION_DIGEST:
            performative = contract_api_pb2.ContractApiMessage.Transaction_Digest_Performative()  # type: ignore
            transaction_digest = msg.transaction_digest
            performative.transaction_digest = transaction_digest
            contract_api_msg.transaction_digest.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.TRANSACTION_RECEIPT:
            performative = contract_api_pb2.ContractApiMessage.Transaction_Receipt_Performative()  # type: ignore
            transaction_receipt = msg.transaction_receipt
            TransactionReceipt.encode(
                performative.transaction_receipt, transaction_receipt
            )
            contract_api_msg.transaction_receipt.CopyFrom(performative)
        elif performative_id == ContractApiMessage.Performative.ERROR:
            performative = contract_api_pb2.ContractApiMessage.Error_Performative()  # type: ignore
            if msg.is_set("code"):
                performative.code_is_set = True
                code = msg.code
                performative.code = code
            if msg.is_set("message"):
                performative.message_is_set = True
                message = msg.message
                performative.message = message
            data = msg.data
            performative.data = data
            contract_api_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        contract_api_bytes = contract_api_msg.SerializeToString()
        return contract_api_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'ContractApi' message.

        :param obj: the bytes object.
        :return: the 'ContractApi' message.
        """
        contract_api_pb = contract_api_pb2.ContractApiMessage()
        contract_api_pb.ParseFromString(obj)
        message_id = contract_api_pb.message_id
        dialogue_reference = (
            contract_api_pb.dialogue_starter_reference,
            contract_api_pb.dialogue_responder_reference,
        )
        target = contract_api_pb.target

        performative = contract_api_pb.WhichOneof("performative")
        performative_id = ContractApiMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == ContractApiMessage.Performative.GET_STATE:
            ledger_id = contract_api_pb.get_state.ledger_id
            performative_content["ledger_id"] = ledger_id
            contract_address = contract_api_pb.get_state.contract_address
            performative_content["contract_address"] = contract_address
            callable = contract_api_pb.get_state.callable
            performative_content["callable"] = callable
            kwargs = contract_api_pb.get_state.kwargs
            kwargs_dict = dict(kwargs)
            performative_content["kwargs"] = kwargs_dict
        elif performative_id == ContractApiMessage.Performative.GET_RAW_TRANSACTION:
            ledger_id = contract_api_pb.get_raw_transaction.ledger_id
            performative_content["ledger_id"] = ledger_id
            pb2_terms = contract_api_pb.get_raw_transaction.terms
            terms = Terms.decode(pb2_terms)
            performative_content["terms"] = terms
        elif performative_id == ContractApiMessage.Performative.SEND_SIGNED_TRANSACTION:
            ledger_id = contract_api_pb.send_signed_transaction.ledger_id
            performative_content["ledger_id"] = ledger_id
            pb2_signed_transaction = (
                contract_api_pb.send_signed_transaction.signed_transaction
            )
            signed_transaction = SignedTransaction.decode(pb2_signed_transaction)
            performative_content["signed_transaction"] = signed_transaction
        elif performative_id == ContractApiMessage.Performative.GET_TRANSACTION_RECEIPT:
            ledger_id = contract_api_pb.get_transaction_receipt.ledger_id
            performative_content["ledger_id"] = ledger_id
            transaction_digest = (
                contract_api_pb.get_transaction_receipt.transaction_digest
            )
            performative_content["transaction_digest"] = transaction_digest
        elif performative_id == ContractApiMessage.Performative.BALANCE:
            balance = contract_api_pb.balance.balance
            performative_content["balance"] = balance
        elif performative_id == ContractApiMessage.Performative.RAW_TRANSACTION:
            pb2_raw_transaction = contract_api_pb.raw_transaction.raw_transaction
            raw_transaction = RawTransaction.decode(pb2_raw_transaction)
            performative_content["raw_transaction"] = raw_transaction
        elif performative_id == ContractApiMessage.Performative.TRANSACTION_DIGEST:
            transaction_digest = contract_api_pb.transaction_digest.transaction_digest
            performative_content["transaction_digest"] = transaction_digest
        elif performative_id == ContractApiMessage.Performative.TRANSACTION_RECEIPT:
            pb2_transaction_receipt = (
                contract_api_pb.transaction_receipt.transaction_receipt
            )
            transaction_receipt = TransactionReceipt.decode(pb2_transaction_receipt)
            performative_content["transaction_receipt"] = transaction_receipt
        elif performative_id == ContractApiMessage.Performative.ERROR:
            if contract_api_pb.error.code_is_set:
                code = contract_api_pb.error.code
                performative_content["code"] = code
            if contract_api_pb.error.message_is_set:
                message = contract_api_pb.error.message
                performative_content["message"] = message
            data = contract_api_pb.error.data
            performative_content["data"] = data
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return ContractApiMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
