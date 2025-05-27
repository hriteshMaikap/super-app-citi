"""
Admin Pydantic schemas for KYC review and management
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class KYCApplicationSummary(BaseModel):
    """Summary of KYC application for admin list view"""
    kyc_id: int
    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    username: str
    kyc_status: str
    documents_count: int
    verification_score: float
    face_verified: bool
    created_at: datetime


class KYCApplication(BaseModel):
    """Detailed KYC application for admin review"""
    kyc_id: int
    user_id: str
    email: str
    phone: Optional[str] = None
    username: str
    first_name: str
    last_name: str
    user_created_at: datetime
    
    # KYC Details
    full_name: str
    date_of_birth: date
    address: str
    aadhar_number: str
    pan_number: str
    kyc_status: str
    verification_score: float
    face_match_score: float
    
    # Timing and Verification
    created_at: datetime
    updated_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    verification_notes: Optional[str] = None
    
    # Related entities
    documents: List[Dict[str, Any]]
    face_verification: Optional[Dict[str, Any]] = None


class KYCReviewAction(BaseModel):
    """Action for KYC application review"""
    action: str = Field(..., pattern="^(approve|reject)$")
    notes: Optional[str] = Field(None, max_length=1000)


class KYCReviewResult(BaseModel):
    """Result of KYC application review"""
    kyc_id: int
    action: str
    status: str
    reviewer: str
    review_time: datetime
    notes: Optional[str] = None
    message: str


class AdminDashboardStats(BaseModel):
    """Statistics for admin dashboard"""
    total_users: int
    verified_users: int
    kyc_stats: Dict[str, int]
    recent_applications: int
    avg_verification_score: float
