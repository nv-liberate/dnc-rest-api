from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_session
from app.handlers import get_dnc_phone, add_dnc_phone

router = APIRouter()


@router.post("/dnc_phone/")
async def add_phone(call_params: dict, session: AsyncSession = Depends(get_session)):
    added_item = await add_dnc_phone(
        session,
        organization_id=call_params.get("organization_id"),
        campaign_id=call_params.get("campaign_id"),
        phone=call_params.get("phone"),
        reason=call_params.get("reason")
    )
    return added_item


@router.get("/dnc_phone/{organization_id}/{campaign_id}/{phone}")
async def get_phone(organization_id: str, campaign_id: str, phone: str, session: AsyncSession = Depends(get_session)):
    item = await get_dnc_phone(session, organization_id, campaign_id, phone)
    return item.reason if item else None

