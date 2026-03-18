from math import ceil

def paginate(data: list, page: int = 1, limit: int = 10):

    total = len(data)
    total_pages = ceil(total / limit) if limit else 1

    start = (page - 1) * limit
    end = start + limit

    paginated_data = data[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": paginated_data
    }