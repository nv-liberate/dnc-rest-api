from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_session
from app.handlers import get_dnc_phone, add_dnc_phone

router = APIRouter()


@router.post("/dnc_phone/")
async def add_phone(dnc_phone: dict, session: AsyncSession = Depends(get_session)):
    added_item = await add_dnc_phone(
        session,
        organization_id=dnc_phone.get("organization_id"),
        campaign_id=dnc_phone.get("campaign_id"),
        phone=dnc_phone.get("phone"),
        reason=dnc_phone.get("reason")
    )
    return added_item


@router.get("/dnc_phone/{organization_id}/{campaign_id}/{phone}")
async def get_phone(organization_id: str, campaign_id: str, phone: str, session: AsyncSession = Depends(get_session)):
    item = await get_dnc_phone(session, organization_id, campaign_id, phone)
    return item.reason if item else None

# @router.put("/items/{item_id}", response_model=dict)
# async def update_item(item_id: int, item: dict, session: AsyncSession = Depends(get_session)):
#     db_item = await get_item(session, item_id)
#     for key, value in item.items():
#         setattr(db_item, key, value)
#     await session.commit()
#     await session.refresh(db_item)
#     return {"id": db_item.id, "name": db_item.name, "description": db_item.description}

# @router.delete("/items/{item_id}", response_model=dict)
# async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
#     db_item = await get_item(session, item_id)
#     await session.delete(db_item)
#     await session.commit()
#     return {"result": "deleted"}
