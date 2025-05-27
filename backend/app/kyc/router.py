"""
KYC routes for the Super App
Banking-grade document verification and identity management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
import logging

from ..core.database import get_db
from ..schemas.kyc import (
    KYCProfileCreate, KYCProfileResponse, DocumentUpload, DocumentResponse,
    BankAccountCreate, BankAccountResponse, PaymentCardCreate, PaymentCardResponse,
    FaceVerificationUpload, FaceVerificationResponse, UPIGenerationRequest, 
    UPIGenerationResponse, VerificationStatusResponse
)
from ..kyc.service import kyc_service
from ..auth.dependencies import get_current_user, get_client_info
from ..models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/kyc", tags=["kyc"])


@router.post("/profile", response_model=KYCProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_kyc_profile(
    profile_data: KYCProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> KYCProfileResponse:
    """
    Create KYC profile for authenticated user
    
    - **personal_details**: Full name, DOB, gender, parents' names
    - **address_details**: Complete address information
    """
    try:
        result = await kyc_service.create_kyc_profile(
            current_user.user_id,
            profile_data,
            db
        )
        
        return KYCProfileResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"KYC profile creation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="KYC profile creation failed"
        )


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    document_type: str = Form(...),
    document_number: str = Form(...),
    document_name: str = Form(...),
    front_image: UploadFile = File(...),
    back_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DocumentResponse:
    """
    Upload identity document for verification
    
    - **document_type**: aadhar, pan, passport, driving_license, voter_id
    - **document_number**: Document number (will be validated)
    - **document_name**: Name as per document
    - **front_image**: Front side of document (required)
    - **back_image**: Back side of document (optional, for applicable documents)
    """
    try:
        # Validate file types
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        if front_image.content_type not in allowed_types:
            raise ValueError("Front image must be JPEG or PNG")
        
        if back_image and back_image.content_type not in allowed_types:
            raise ValueError("Back image must be JPEG or PNG")
        
        # Read image data
        front_image_data = await front_image.read()
        back_image_data = await back_image.read() if back_image else None
        
        # Validate file sizes (5MB limit)
        if len(front_image_data) > 5 * 1024 * 1024:
            raise ValueError("Front image size must be less than 5MB")
        
        if back_image_data and len(back_image_data) > 5 * 1024 * 1024:
            raise ValueError("Back image size must be less than 5MB")
        
        # Create document upload request
        from ..schemas.kyc import DocumentTypeEnum
        document_data = DocumentUpload(
            document_type=DocumentTypeEnum(document_type),
            document_number=document_number,
            document_name=document_name
        )
        
        result = await kyc_service.upload_document(
            current_user.user_id,
            document_data,
            front_image_data,
            back_image_data,
            db
        )
        
        return DocumentResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Document upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document upload failed"
        )


@router.post("/face/upload", response_model=FaceVerificationResponse)
async def upload_face_image(
    face_image: UploadFile = File(...),
    image_quality_check: bool = Form(True),
    face_detection_required: bool = Form(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> FaceVerificationResponse:
    """
    Upload face image for verification
    
    - **face_image**: Clear face photo (JPEG/PNG, max 5MB)
    - **image_quality_check**: Enable image quality validation
    - **face_detection_required**: Require face detection in image
    """
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        if face_image.content_type not in allowed_types:
            raise ValueError("Face image must be JPEG or PNG")
        
        # Read image data
        face_image_data = await face_image.read()
        
        # Validate file size
        if len(face_image_data) > 5 * 1024 * 1024:
            raise ValueError("Face image size must be less than 5MB")
        
        # Create verification request
        verification_data = FaceVerificationUpload(
            image_quality_check=image_quality_check,
            face_detection_required=face_detection_required
        )
        
        result = await kyc_service.upload_face_image(
            current_user.user_id,
            face_image_data,
            verification_data,
            db
        )
        
        return FaceVerificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Face verification failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face verification failed"
        )


@router.post("/bank-account", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
async def add_bank_account(
    account_data: BankAccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BankAccountResponse:
    """
    Add bank account for payments
    
    - **bank_name**: Name of the bank
    - **ifsc_code**: IFSC code in correct format
    - **account_number**: Bank account number
    - **account_holder_name**: Name as per bank account
    - **account_type**: savings, current, salary, nri
    - **is_primary**: Set as primary account for payments
    """
    try:
        result = await kyc_service.add_bank_account(
            current_user.user_id,
            account_data,
            db
        )
        
        return BankAccountResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Bank account addition failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bank account addition failed"
        )


@router.post("/payment-card", response_model=PaymentCardResponse, status_code=status.HTTP_201_CREATED)
async def add_payment_card(
    card_data: PaymentCardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> PaymentCardResponse:
    """
    Add payment card for transactions
    
    - **card_number**: 13-19 digit card number (will be validated using Luhn algorithm)
    - **card_holder_name**: Name as per card
    - **expiry_month**: MM format (01-12)
    - **expiry_year**: YYYY format
    - **card_type**: debit, credit, prepaid
    - **is_primary**: Set as primary card for payments
    """
    try:
        result = await kyc_service.add_payment_card(
            current_user.user_id,
            card_data,
            db
        )
        
        return PaymentCardResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Payment card addition failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment card addition failed"
        )


@router.post("/upi/generate", response_model=UPIGenerationResponse)
async def generate_upi_id(
    upi_request: UPIGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UPIGenerationResponse:
    """
    Generate UPI ID for verified user
    
    - **preferred_handle**: Optional preferred handle for UPI ID
    
    **Requirements**: User must have completed full KYC verification
    """
    try:
        result = await kyc_service.generate_upi_id(
            current_user.user_id,
            upi_request,
            db
        )
        
        return UPIGenerationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"UPI generation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UPI generation failed"
        )


@router.get("/status", response_model=VerificationStatusResponse)
async def get_kyc_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> VerificationStatusResponse:
    """
    Get comprehensive KYC verification status
    
    Returns complete status including:
    - Overall verification status and level
    - Completion percentage
    - Pending verification steps
    - Document verification status
    - UPI eligibility
    - All uploaded documents, bank accounts, and cards
    """
    try:
        result = await kyc_service.get_kyc_status(current_user.user_id, db)
        
        return VerificationStatusResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"KYC status retrieval failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="KYC status retrieval failed"
        )


@router.post("/update-verification", status_code=status.HTTP_200_OK)
async def update_verification_level(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update verification level based on completed KYC steps
    
    This endpoint checks all completed KYC steps and updates the verification level accordingly.
    """
    try:
        result = await kyc_service.update_verification_level(
            current_user.user_id,
            db
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating verification level: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update verification level"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for KYC service"""
    return {"status": "healthy", "service": "kyc"}