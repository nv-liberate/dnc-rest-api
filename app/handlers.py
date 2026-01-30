from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DNCPhone


async def get_dnc_phone(session: AsyncSession, organization_id: str, campaign_id: str, phone: str):
    result = await session.execute(
        select(DNCPhone).where(
            DNCPhone.organization_id == organization_id,
            DNCPhone.campaign_id == campaign_id,
            DNCPhone.phone == phone
        )
    )
    dnc_phone = result.scalar_one_or_none()
    return dnc_phone

async def add_dnc_phone(session: AsyncSession, organization_id: str, campaign_id: str, phone: str, reason: str = None):
    dnc_phone = DNCPhone(
        organization_id=organization_id,
        campaign_id=campaign_id,
        phone=phone,
        reason=reason
    )
    session.add(dnc_phone)
    try:
        await session.commit()
        await session.refresh(dnc_phone)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Could not add phone: {str(e)}")
    return dnc_phone
