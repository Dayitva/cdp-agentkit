import requests

def fetch_data(url, key):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get(key, None)
    else:
        return None

def fetch_kelpdao_details():
    kelp_tvl_url = "https://universe.kelpdao.xyz/rseth/tvl/?lrtToken"
    kelp_apy_url = "https://universe.kelpdao.xyz/rseth/apy"

    kelp_assets = ["eth", "steth", "ethx"]

    tvl = fetch_data(kelp_tvl_url, 'usdTvl')
    if tvl is not None:
        print(f"KelpDAO TVL in USD: {tvl}")
    else:
        print("Failed to fetch TVL data.")

    apy = fetch_data(kelp_apy_url, 'value')
    if apy is not None:
        print(f"KelpDAO APY: {apy}%")
    else:
        print("Failed to fetch APY data.")

    return tvl, apy

def fetch_renzo_details():
    renzo_data_url = "https://app.renzoprotocol.com/api/stats"

    renzo_assets = ["eth", "weth", "steth", "wsteth"]

    renzo_data = fetch_data(renzo_data_url, 'data')

    if renzo_data is not None and 'restakedTVL' in renzo_data and 'ezETH' in renzo_data['restakedTVL'] and 'usd' in renzo_data['restakedTVL']['ezETH']:
        print(f"Restaked TVL (ezETH) in USD: {renzo_data['restakedTVL']['ezETH']['usd']}")
    else:
        print("Failed to fetch restaked TVL data.")

    if renzo_data is not None and 'restakedTVL' in renzo_data and 'pzETH' in renzo_data['restakedTVL'] and 'usd' in renzo_data['restakedTVL']['pzETH']:
        print(f"Restaked TVL (pzETH) in USD: {renzo_data['restakedTVL']['pzETH']['usd']}")
    else:
        print("Failed to fetch restaked TVL data for pzETH.")

    if renzo_data is not None and 'apr' in renzo_data and 'data' in renzo_data['apr'] and 'rate' in renzo_data['apr']['data']:
        apr_rate = round(renzo_data['apr']['data']['rate'], 2)
        print(f"ezETH APR: {apr_rate}%")
    else:
        print("Failed to fetch APR data.")

    if renzo_data is not None and 'apr' in renzo_data and 'pzETHAPR' in renzo_data['apr'] and 'rate' in renzo_data['apr']['pzETHAPR']:
        pzeth_apr_rate = round(renzo_data['apr']['pzETHAPR']['rate'], 2)
        print(f"pzETH APR: {pzeth_apr_rate}%")
    else:
        print("Failed to fetch pzETH APR data.")

    return renzo_data['restakedTVL']['ezETH']['usd'], round(renzo_data['apr']['data']['rate'], 2)

def fetch_etherfi_details():
    etherfi_tvl_url = "https://app.ether.fi/api/protocol/tvl"
    etherfi_apy_url = "https://app.ether.fi/api/lrt2/apr"

    etherfi_assets = ["eth", "steth", "weth", "wsteth", "insteth"]

    tvl = fetch_data(etherfi_tvl_url, 'tvl')
    if tvl is not None:
        print(f"Etherfi TVL in USD: {tvl}")
    else:
        print("Failed to fetch TVL data.")

    apy = fetch_data(etherfi_apy_url, 'lrt2Apr')
    if apy is not None:
        print(f"Etherfi APY: {round(2.9 + apy, 2)}%")
    else:
        print("Failed to fetch APY data.")

    return tvl, round(2.9 + apy, 2)

def fetch_inception_details():
    inception_apy_url = "https://bff.prod.inceptionlrt.com/stakingwatch/proxy/metric/apr/"

    inception_assets = ["lido/steth/", "rocket-pool/reth/", "frax/sfrxeth/", "ankr/ankreth/", "coinbase/cbeth/", "swell/sweth/", "stader/ethx/", "mantle/meth/", "inceptionlrt/insteth/"]

    for i in inception_assets:
        inception_apy = fetch_data(inception_apy_url+i+"apr_7d", 'data')

        if inception_apy is not None and 'value' in inception_apy:
            print(f"Inception APY for {i}: {round(float(inception_apy['value']), 2)}%")
        else:
            print(f"Failed to fetch Inception APY data for {i}.")

    return inception_apy

def fetch_swell_details():
    swell_tvl_url = "https://v3-lrt.svc.swellnetwork.io/api/tokens/rsweth/tvl"
    swell_apy_url = "https://v3-lrt.svc.swellnetwork.io/api/tokens/rsweth/apr"

    swell_assets = []

    tvl = fetch_data(swell_tvl_url, 's')
    if tvl is not None:
        print(f"Swell Finance TVL: {tvl}")
    else:
        print("Failed to fetch TVL data.")

    apy = fetch_data(swell_apy_url, 'value')
    if apy is not None:
        print(f"Swell Finance APY: {apy}%")
    else:
        print("Failed to fetch APY data.")

    return tvl, apy

if __name__ == "__main__":
    fetch_kelpdao_details()
    fetch_renzo_details()
    fetch_etherfi_details()
    fetch_inception_details()
    fetch_swell_details()

# {"wallet_id": "d2ce0251-da1c-4fe3-9b40-4bacf9e30aec", "seed": "1523a08ae95db4332b1ab93cfc61ff540ac92dfabc3fdf07c016e9015f116d3e2cf9dcd323ed7040d205cfa23c226ad480d64aa371a1d4abf1d22ac4c860c4dc", "network_id": "base-sepolia", "default_address_id": "0xD73d5DA49aaa6E0F973f81C1B617DC3D3BD1E2D3"}
