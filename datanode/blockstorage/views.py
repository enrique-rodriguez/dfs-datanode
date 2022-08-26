def get_block(bus, bid):
    store = bus.deps.get("store")
    return store.get(bid)