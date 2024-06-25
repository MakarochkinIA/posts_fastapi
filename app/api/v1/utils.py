from fastapi import HTTPException


def item_check(item):
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
