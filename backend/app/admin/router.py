"""
Admin routes for system management and KYC review
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from ..core.database import get_db
from ..auth.dependencies import get_current_admin
from ..models.user import User
from ..schemas.admin import (
    KYCApplicationSummary, KYCApplication, KYCReviewAction,
    KYCReviewResult, AdminDashboardStats
)
from .service import admin_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/kyc/applications", response_model=List[KYCApplicationSummary])
async def list_pending_kyc_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
) -> List[KYCApplicationSummary]:
    """
    List pending KYC applications for admin review
    
    Returns list of applications with basic info
    """
    try:
        applications = await admin_service.get_pending_kyc_applications(skip, limit, db)
        return applications
        
    except Exception as e:
        logger.error(f"Error listing KYC applications: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve KYC applications"
        )


@router.get("/kyc/applications/{kyc_id}", response_model=KYCApplication)
async def get_kyc_application_details(
    kyc_id: int = Path(..., ge=1),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
) -> KYCApplication:
    """
    Get detailed KYC application for admin review
    
    Includes personal details, documents, face verification
    """
    try:
        application = await admin_service.get_kyc_application_details(kyc_id, db)
        return application
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving KYC application {kyc_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve KYC application details"
        )


@router.post("/kyc/review/{kyc_id}", response_model=KYCReviewResult)
async def review_kyc_application(
    action: KYCReviewAction,
    kyc_id: int = Path(..., ge=1),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
) -> KYCReviewResult:
    """
    Review KYC application and approve/reject
    
    Admin can approve or reject with notes
    """
    try:
        result = await admin_service.review_kyc_application(
            kyc_id, current_admin.user_id, action, db
        )
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error reviewing KYC application {kyc_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process KYC review"
        )


@router.get("/dashboard/stats", response_model=AdminDashboardStats)
async def get_admin_dashboard_stats(
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
) -> AdminDashboardStats:
    """
    Get statistics for admin dashboard
    
    Includes user counts, KYC status counts, etc.
    """
    try:
        stats = await admin_service.get_dashboard_statistics(db)
        return stats
        
    except Exception as e:
        logger.error(f"Error generating admin dashboard stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics"
        )
