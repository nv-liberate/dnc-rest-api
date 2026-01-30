from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint

Base = declarative_base()


class DNCPhone(Base):
    __tablename__ = "dnc_phones"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    __table_args__ = (
        UniqueConstraint("organization_id", "campaign_id", "phone", name="uq_org_campaign_phone"),
    )
