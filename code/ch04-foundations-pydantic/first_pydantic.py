import datetime
from typing import Optional

import pydantic


class Item(pydantic.BaseModel):
    item_id: int
    created_date: datetime.datetime
    pages_visited: list[int]
    price: float
    name: Optional[str] = "Jane Doe"


def main():
    data = {
        'item_id': '123',
        'created_date': '2002-11-24 12:22',
        'pages_visited': [1, 2, '3'],
        'price': 17.22,
        'name': "Michael"
    }

    item = Item(**data)

    print(item)


if __name__ == '__main__':
    main()
