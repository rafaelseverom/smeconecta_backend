from typing import List, Any


def paginate(query, page: int, limit: int):
    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    }