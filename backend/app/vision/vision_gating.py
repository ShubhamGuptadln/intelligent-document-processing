def decide_vision(stats):
    if not stats:
        return False
    if stats.get("image_pages", 0) > 0:
        return True
    return False
