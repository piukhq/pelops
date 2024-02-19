from datetime import datetime
from typing import TYPE_CHECKING, Literal, cast

from loguru import logger
from redis import StrictRedis

from pelops.settings import settings

if TYPE_CHECKING:
    from typing_extensions import TypedDict

    action_type = tuple[bool, bool, str, dict[str, str] | None]
    ActionsType = TypedDict(
        "ActionsType",
        {
            "ADD": action_type,
            "RET": action_type,
            "DEL": action_type,
            "": action_type,
        },
        total=False,
    )

RETAINED = "RET"
ADDED = "ADD"
DELETED = "DEL"


class Redis:
    class NotFound(Exception):
        pass

    def __init__(self, url: str) -> None:
        self.store = cast(StrictRedis, StrictRedis.from_url(url))
        self.expiry = 43200

    @staticmethod
    def _key(key: str) -> str:
        return f"pelops-{key}"

    def set(self, key: str, value: str) -> None:
        self.store.set(self._key(key), value)

    def set_expire(self, key: str, value: str, expire: int | None = None) -> None:
        if expire is None:
            expire = self.expiry
        self.store.setex(self._key(key), expire, value)

    def append_to_rlist(self, key: str, value: str, expire: int | None = None) -> None:
        if expire is None:
            expire = self.expiry
        # Appends value to redis list and resets expiry
        self.store.rpush(key, value)
        self.store.expire(key, expire)

    def get(self, key: str) -> Literal["ADD", "RET", "DEL", ""]:
        val = cast(bytes, self.store.get(self._key(key)))
        if not val:
            raise self.NotFound
        return cast(Literal["ADD", "RET", "DEL", ""], val.decode())

    def delete(self, key: str) -> None:
        self.store.delete(self._key(key))

    def rlist_to_list(self, key: str) -> list[str]:
        # Reads redis list and decodes elements to string
        list_bytes = cast(list[bytes], self.store.lrange(key, 0, -1))
        list_decoded: list[str] = [x.decode("utf-8") for x in list_bytes]
        return list_decoded

    def update_if_per(self, psp_token: str, new_status: str, token: str) -> tuple[bool, bool, str, str, str]:
        """
        For Persistence (PER):

        The PER prefix, added to the psp_token, will simulate persistence in Redis, allowing Pelops to store the results
        of some calls (currently ADD, DEL and RET) in a cache for testing purposes. This will be reflected in the card
        'status', which is updated as successful call are made to simulate card status in 3rd party vaults/dbs.:
            e.g. PER_4423snv489os093

        Individual card status can be queried via the '/cardstatus' endpoint (without the PER prefix):
            e.g. {pelops url}/cardstatus/4423snv489os093

        The status of cards added/deleted etc. without the PER prefix will not be stored/updated.
        """

        if psp_token[:4] == "PER_":
            success, log_message, err_code, err_message = self.update_status(psp_token, new_status, token, self.expiry)

            now = datetime.now(tz=settings.TZINFO)
            logger.info("Card Persistence: {}", log_message)
            self.append_to_rlist(f"cardlog_{psp_token}", f"[{now}] {log_message}", self.expiry)

            return True, success, log_message, err_code, err_message

        return False, False, "", "", ""

    def update_status(self, psp_token: str, new_status: str, token: str, expiry: int) -> tuple[bool, str, str, str]:
        # Checks logic for retain/add/delete to persistence layer and applies/rejects requested change as necessary.
        # Also returns error codes and messages for later use, if request fails logic.
        success = False
        log_message = "Failed"
        err = None
        err_code = ""
        err_message = ""

        err_message_list = {
            "RCCMP005": "Card Member already Synced for the Token - Duplicate request or malfunction in input request.",
            "RCCMU009": "Invalid Token/Token not found.",
            "RTMENRE0025": "The user key provided is already in use - duplicate card.",
            "RTMENRE0021": "Invalid user status or user already enrolled",
            "RTMENRE0050": "Invalid user status",
            "RTMENRE0026": "Enroll User not found",
            "5": "Invalid account/no account found",
            "6": "Account already exists",
            "ERROR": "Generic Pelops-generated error",
        }

        try:
            old_status = self.get(f"card_{psp_token}")
        except self.NotFound:
            self.set_expire(f"card_{psp_token}", "", expiry)
            old_status = ""

        if new_status == RETAINED:
            actions_ret: "ActionsType" = {
                "ADD": (False, True, f"Card {psp_token} re-retained (Currently ADDED).", None),
                "RET": (False, True, f"Card {psp_token} re-retained (Currently RETAINED).", None),
                "DEL": (False, True, f"Card {psp_token} re-retained (Currently DELETED).", None),
                "": (True, True, f"Card {psp_token} retained.", None),
            }

            change, success, log_message, err = actions_ret[old_status]
            if change:
                self.set_expire(f"card_{psp_token}", new_status, expiry)

        elif new_status == ADDED:
            actions_add: "ActionsType" = {
                "ADD": (
                    False,
                    False,
                    f"Card {psp_token} cannot be added - card already exists.",
                    {"amex": "RCCMP005", "visa": "RTMENRE0025", "mastercard": "6"},
                ),
                "RET": (True, True, f"Card {psp_token} added successfully.", None),
                "DEL": (True, True, f"Card {psp_token} re-added.", None),
                "": (
                    False,
                    False,
                    f"Card {psp_token} not yet retained.",
                    {"amex": "RCCMU009", "visa": "RTMENRE0021", "mastercard": "5"},
                ),
            }
            change, success, log_message, err = actions_add[old_status]
            if change:
                self.set_expire(f"card_{psp_token}", new_status, expiry)

        elif new_status == DELETED:
            actions_del: "ActionsType" = {
                "ADD": (True, True, f"Card {psp_token} deleted successfully.", None),
                "RET": (
                    False,
                    False,
                    f"Card {psp_token} not yet added.",
                    {"amex": "RCCMU009", "visa": "RTMENRE0026", "mastercard": "5"},
                ),
                "DEL": (
                    False,
                    False,
                    f"Card {psp_token} already deleted.",
                    {"amex": "RCCMU009", "visa": "RTMENRE0026", "mastercard": "5"},
                ),
                "": (
                    False,
                    False,
                    f"Card {psp_token} not yet added.",
                    {"amex": "RCCMU009", "visa": "RTMENRE0026", "mastercard": "5"},
                ),
            }
            change, success, log_message, err = actions_del[old_status]
            if change:
                self.set_expire(f"card_{psp_token}", new_status, expiry)

        if err:
            err_code = err[token]
            err_message = err_message_list[err_code]

        return success, log_message, err_code, err_message

    def add_activation(self, psp_token: str, offer_id: str, activation_id: str) -> bool:
        # If using the PER_ prefix (see above), activation records will be persistently stored and request
        # returned as successful, provided the associated psp_token has a status of 'ADDED' within Pelops'
        # persistence layer.

        now = datetime.now(tz=settings.TZINFO)
        if psp_token[:4] == "PER_":
            try:
                status = self.get(f"card_{psp_token}")
            except self.NotFound:
                return False
            if status == "ADD":
                self.append_to_rlist(f"card_activations_{psp_token}", activation_id)
                self.append_to_rlist(
                    f"cardlog_{psp_token}",
                    f"[{now}] Activated card/scheme pair with VOP for scheme "
                    f"{offer_id}. Activation id: {activation_id}",
                )
                logger.info("Card persistence: Activation {} created", activation_id)
            else:
                self.append_to_rlist(
                    f"cardlog_{psp_token}", f"[{now}] Activation failed for: {activation_id}. No added card found"
                )
                logger.info("Card persistence: Activation {} failed. No added card found", activation_id)
                return False
        return True

    def remove_activation(self, psp_token: str, activation_id: str) -> bool:
        # If using the PER_ prefix (see above), deactivation records will be removed (as well as logged) and request
        # will return as successful, provided the associated psp_token has a status of 'ADDED' within Pelops'
        # persistence layer.

        now = datetime.now(tz=settings.TZINFO)
        if psp_token[:4] == "PER_":
            try:
                status = self.get(f"card_{psp_token}")
            except self.NotFound:
                return False
            if status == "ADD":
                if self.store.lrem(f"card_activations_{psp_token}", -1, activation_id):
                    # lrem returns number of removed items, 0 if none found/removed
                    self.append_to_rlist(
                        f"cardlog_{psp_token}",
                        f"[{now}] Deactivated card/scheme pair. " f"Activation id: {activation_id}",
                    )
                    logger.info("Card persistence: Activation {} deactivated", activation_id)
                else:
                    return False
            else:
                self.append_to_rlist(
                    f"cardlog_{psp_token}",
                    f"[{now}] Deactivation failed for activation_id " f"{activation_id}. No added card found.",
                )
                logger.info(
                    f"Card persistence: Deactivation failed for activation_id {activation_id}. " f"No added card found"
                )
                return False
        return True
