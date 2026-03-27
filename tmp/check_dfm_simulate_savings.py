import json
import sys
import urllib.request

BASE = "http://127.0.0.1:5000"
SAMPLE = sys.argv[1] if len(sys.argv) > 1 else "steel_bracket"


def _get_json(url: str):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_json(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    sample = _get_json(f"{BASE}/api/samples/{SAMPLE}")
    quote = _post_json(f"{BASE}/api/quote", sample)

    dfm = quote.get("dfm_suggestions") or []
    if not dfm:
        print("No DFM suggestions returned from /api/quote")
        return 2

    print("/api/quote dfm_suggestions savings:")
    for s in dfm:
        print(" ", s.get("suggestion_id"), s.get("savings_inr"))

    sid = dfm[0].get("suggestion_id")
    sim = _post_json(f"{BASE}/api/dfm/simulate", {"suggestion_id": sid, "quote": quote})

    mod_dfm = ((sim.get("quote_modified") or {}).get("dfm_suggestions")) or []
    print("\n/api/dfm/simulate quote_modified dfm_suggestions savings:")
    for s in mod_dfm:
        print(" ", s.get("suggestion_id"), s.get("savings_inr"))

    missing = [s.get("suggestion_id") for s in mod_dfm if not isinstance(s.get("savings_inr"), (int, float))]
    if missing:
        print("\nERROR: Missing/invalid savings_inr for:", missing)
        return 1

    print("\nOK: simulate returns savings_inr on modified quote.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
