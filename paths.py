import requests
import json
from constants import *
import time


def get_etherscan_contract_creator(addrs):
    s = 'https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={0}&apikey={1}'.format(
        addrs, ETHERSCAN_API)

    r = requests.get(s)
    return r


if __name__ == "__main__":
    '''
    results = []
    while len(results) < len(uniq_pools):
        addrs = ""
        for i in range(len(results), len(results)+5):
            addrs = addrs+uniq_pools[i]
            if i != len(results)+4:
                addrs = addrs + ","
        r = get_etherscan_contract_creator(addrs)
        r_lst = r.json()
        results = results + r_lst['result']
        time.sleep(0.2)
    '''
