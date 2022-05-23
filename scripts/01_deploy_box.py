from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def deploy():
    account = get_account()
    print(f"deploying to {network.show_active}")
    box = Box.deploy({"from": account})
    print(box.retrive())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # intitalizer= box.store, 1
    box_encode_initilizer_funtion = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encode_initilizer_funtion,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"proxy deployed to {proxy}, u can deploy to V2")
    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)
    proxy_box.store(1, {"from": account})

    ##upgrading
    box_V2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(
        account, proxy, box_V2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_V2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrive())


def main():
    deploy()
