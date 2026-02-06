SEQUENZA_ORDER = [
    ("recent", "Recenti", "-created_at"),
    ("old", "Meno recenti", "created_at"),
    ("price_asc", "Prezzo ↑", "prezzo"),
    ("price_desc", "Prezzo ↓", "-prezzo"),
]

def ordina(queryset, current_order):
    keys = [o[0] for o in SEQUENZA_ORDER]
    index = keys.index(current_order) if current_order in keys else 0

    key, label, order_by = SEQUENZA_ORDER[index]
    next_order = SEQUENZA_ORDER[(index + 1) % len(SEQUENZA_ORDER)][0]

    return (
        queryset.order_by(order_by),
        label,
        next_order,
    )
