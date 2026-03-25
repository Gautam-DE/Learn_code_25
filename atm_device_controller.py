from __future__ import annotations


class ATMException(Exception):
    pass


class DeviceLockedException(ATMException):
    pass


class NetworkConnectionException(ATMException):
    pass


class InsufficientFundsException(ATMException):
    pass


class DeviceHandle:

    INVALID = None

    def __init__(self, device_id: str):
        self.device_id = device_id

    def __bool__(self) -> bool:
        return self.device_id is not None


class DeviceRecord:

    def __init__(self, is_suspended: bool, is_wifi_connected: bool):
        self.is_suspended = is_suspended
        self.is_wifi_connected = is_wifi_connected


class ATMDeviceController:

    def withdraw(self, account_id: str, amount: float) -> None:
        try:
            self._perform_withdrawal(account_id, amount)
        except ATMException:
            raise
        except Exception as unexpected:
            raise RuntimeError("Unexpected ATM error") from unexpected

    def _perform_withdrawal(self, account_id: str, amount: float) -> None:
        handle = self._get_valid_device_handle()
        record = self._retrieve_device_record(handle)

        self._ensure_device_is_active(record)
        self._ensure_network_connection(record)
        self._ensure_sufficient_funds(account_id, amount)

        self._dispense_cash(handle, amount)

    def _ensure_device_is_active(self, record: DeviceRecord) -> None:
        if record.is_suspended:
            raise DeviceLockedException("ATM device is currently suspended.")

    def _ensure_network_connection(self, record: DeviceRecord) -> None:
        if not record.is_wifi_connected:
            raise NetworkConnectionException("ATM has no network connection.")

    def _ensure_sufficient_funds(self, account_id: str, amount: float) -> None:
        balance = self._get_balance(account_id)
        if balance < amount:
            raise InsufficientFundsException(
                f"Insufficient funds: balance {balance:.2f}, requested {amount:.2f}."
            )

    def _get_valid_device_handle(self) -> DeviceHandle:
        handle = self._get_handle("DEV1")
        if not handle:
            raise RuntimeError("Could not obtain a device handle.")
        return handle

    def _get_handle(self, device_id: str) -> DeviceHandle:
        return DeviceHandle(device_id)

    def _retrieve_device_record(self, handle: DeviceHandle) -> DeviceRecord:
        return DeviceRecord(is_suspended=False, is_wifi_connected=True)

    def _get_balance(self, account_id: str) -> float:
        mock_balances = {"ACC001": 5_000.00, "ACC002": 200.00}
        return mock_balances.get(account_id, 0.0)

    def _dispense_cash(self, handle: DeviceHandle, amount: float) -> None:
        print(f"[ATM] Dispensed {amount:.2f} from device '{handle.device_id}'.")


def process_withdrawal(account_id: str, amount: float) -> None:
    controller = ATMDeviceController()
    try:
        controller.withdraw(account_id, amount)
        print(f"[Client] Withdrawal of {amount:.2f} completed successfully.")

    except DeviceLockedException as exc:
        print(f"[Client] ATM unavailable – device locked: {exc}")

    except NetworkConnectionException as exc:
        print(f"[Client] ATM unavailable – network error: {exc}")

    except InsufficientFundsException as exc:
        print(f"[Client] Transaction declined – {exc}")

    except RuntimeError as exc:
        print(f"[Client] System error – please contact support: {exc}")


if __name__ == "__main__":
    print("=== Scenario 1: Successful withdrawal ===")
    process_withdrawal("ACC001", 1_000.00)

    print("\n=== Scenario 2: Insufficient funds ===")
    process_withdrawal("ACC002", 500.00)

    print("\n=== Scenario 3: Unknown account (zero balance) ===")
    process_withdrawal("ACC999", 100.00)
