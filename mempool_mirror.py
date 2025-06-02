"""
Mempool Mirror — ищет транзакции в mempool с одинаковыми входами (возможная замена/атака RBF).
"""

import requests
import time

MEMPOOL_URL = "https://mempool.space/api/mempool/recent"

def fetch_recent_txs():
    r = requests.get(MEMPOOL_URL)
    r.raise_for_status()
    return r.json()

def fetch_tx(txid):
    r = requests.get(f"https://mempool.space/api/tx/{txid}")
    r.raise_for_status()
    return r.json()

def extract_inputs(tx):
    return {(vin["txid"], vin["vout"]) for vin in tx.get("vin", [])}

def main():
    print("🪞 Mempool Mirror запущен. Сканируем последние 25 транзакций...")

    seen_inputs = {}
    duplicates = []

    try:
        recent = fetch_recent_txs()
        for tx_meta in recent:
            txid = tx_meta["txid"]
            tx = fetch_tx(txid)
            tx_inputs = extract_inputs(tx)

            for input_ref in tx_inputs:
                if input_ref in seen_inputs:
                    print(f"⚠️ Обнаружены дубликаты входов! {input_ref}")
                    print(f" - Старый tx: {seen_inputs[input_ref]}")
                    print(f" - Новый tx: {txid}")
                    duplicates.append((seen_inputs[input_ref], txid))
                else:
                    seen_inputs[input_ref] = txid

        if not duplicates:
            print("✅ Повторяющихся входов не найдено.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
