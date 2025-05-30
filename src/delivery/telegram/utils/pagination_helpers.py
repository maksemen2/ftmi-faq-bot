from typing import Awaitable, Callable, Optional, Sequence, TypeVar

from aiogram.types import CallbackQuery

T = TypeVar("T")


async def get_paginated_items(
    call: CallbackQuery,
    list_method: Callable[[int, int], Awaitable[Sequence[T]]],
    page: int,
    per_page: int,
    first_page_msg: str = "Вы уже на первой странице",
    last_page_msg: str = "Вы уже на последней странице",
) -> Optional[Sequence[T]]:
    if page < 0:
        await call.answer(first_page_msg)
        return None

    items = await list_method(page, per_page)

    if not items:
        await call.answer(last_page_msg)
        return None
    return items
