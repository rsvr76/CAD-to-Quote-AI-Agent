import asyncio

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.sample_parts import get_sample
from backend.main import api_dfm_simulate, api_quote


async def _run() -> None:
    sample = get_sample("steel_bracket")

    quote = await api_quote({"geometry": sample["geometry"], "inputs": sample["inputs"]})
    dfm = quote.get("dfm_suggestions") or []
    if not dfm:
        raise RuntimeError("No dfm_suggestions returned from api_quote")

    suggestion_id = dfm[0]["suggestion_id"]
    res = await api_dfm_simulate({"suggestion_id": suggestion_id, "quote": quote})

    for k in ("quote_original", "quote_modified", "savings_inr", "savings_pct"):
        if k not in res:
            raise RuntimeError(f"Missing key in response: {k}")

    print("DFM_SIM_OK", suggestion_id, res["savings_inr"], res["savings_pct"])


if __name__ == "__main__":
    asyncio.run(_run())
