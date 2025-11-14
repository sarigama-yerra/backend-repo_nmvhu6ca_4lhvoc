from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class PickupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=5, max_length=20)
    address: str = Field(..., min_length=5, max_length=200)
    service_type: str = Field(..., description="Type of laundry service requested")
    pickup_date: date
    notes: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="pending")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "+1 555-1234",
                "address": "123 Main St, Springfield",
                "service_type": "Wash & Fold",
                "pickup_date": "2025-01-15",
                "notes": "Please ring the doorbell.",
                "status": "pending",
            }
        }
