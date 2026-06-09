from collections import defaultdict

money_flow = defaultdict(float)


def update_flow(symbol, value):

    money_flow[symbol] += value


def get_score(symbol):

    flow = money_flow[symbol]

    score = 0

    if flow > 1000000:
        score += 20

    if flow > 5000000:
        score += 30

    if flow > 10000000:
        score += 50

    return min(score, 100)


def get_top_candidates():

    rows = []

    for symbol in money_flow:

        rows.append({
            "symbol": symbol,
            "score": get_score(symbol),
            "money_flow": money_flow[symbol]
        })

    rows.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return rows[:20]
