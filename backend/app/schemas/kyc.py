"""
KYC schemas for request/response validation
Banking-grade document verification
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class KYCStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DocumentTypeEnum(str, Enum):
    AADHAR = "aadhar"
    PAN = "pan"
    PASSPORT = "passport"
    DRIVING_LICENSE = "driving_license"
    VOTER_ID = "voter_id"


class BankAccountTypeEnum(str, Enum):
    SAVINGS = "savings"
    CURRENT = "current"
    SALARY = "salary"
    NRI = "nri"


class CardTypeEnum(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    PREPAID = "prepaid"


# Personal Details Schemas
class PersonalDetailsCreate(BaseModel):
    """Personal details for KYC"""
    full_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    gender: str = Field(..., pattern=r'^(male|female|other)$')
    father_name: str = Field(..., min_length=2, max_length=100)
    mother_name: Optional[str] = Field(None, min_length=2, max_length=100)
    
    @field_validator('date_of_birth')
    def validate_age(cls, v):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('Must be at least 18 years old')
        if age > 100:
            raise ValueError('Invalid date of birth')
        return v


class AddressDetailsCreate(BaseModel):
    """Address details for KYC"""
    address_line1: str = Field(..., min_length=5, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    pincode: str = Field(..., pattern=r'^\d{6}$')
    country: str = Field(default="India", max_length=50)


# Document Schemas
class DocumentUpload(BaseModel):
    """Document upload request"""
    document_type: DocumentTypeEnum
    document_number: str = Field(..., min_length=5, max_length=50)
    document_name: str = Field(..., min_length=2, max_length=100)
    
    @field_validator('document_number')
    def validate_document_number(cls, v, info):
        doc_type = info.data.get('document_type')
        
        if doc_type == DocumentTypeEnum.AADHAR:
            if not v.replace(' ', '').isdigit() or len(v.replace(' ', '')) != 12:
                raise ValueError('Aadhar number must be 12 digits')
        elif doc_type == DocumentTypeEnum.PAN:
            import re
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', v.upper()):
                raise ValueError('Invalid PAN format')
        
        return v


class DocumentResponse(BaseModel):
    """Document response"""
    id: int
    document_id: str
    document_type: DocumentTypeEnum
    document_number: str  # Masked
    document_name: str
    verification_status: str
    verification_score: Optional[float]
    face_match_status: str
    face_match_score: Optional[float]
    is_primary: bool
    uploaded_at: datetime
    verified_at: Optional[datetime]
    
    model_config = {"from_attributes": True}


# Bank Account Schemas
class BankAccountCreate(BaseModel):
    """Bank account creation"""
    bank_name: str = Field(..., min_length=2, max_length=100)
    branch_name: Optional[str] = Field(None, max_length=100)
    ifsc_code: str = Field(..., pattern=r'^[A-Z]{4}0[A-Z0-9]{6}$')
    account_number: str = Field(..., min_length=8, max_length=20)
    account_holder_name: str = Field(..., min_length=2, max_length=100)
    account_type: BankAccountTypeEnum = BankAccountTypeEnum.SAVINGS
    is_primary: bool = Field(default=False)
    
    @field_validator('account_number')
    def validate_account_number(cls, v):
        if not v.isdigit():
            raise ValueError('Account number must contain only digits')
        return v


class BankAccountResponse(BaseModel):
    """Bank account response"""
    id: int
    account_id: str
    bank_name: str
    branch_name: Optional[str]
    ifsc_code: str
    account_number: str  # Masked
    account_holder_name: str
    account_type: BankAccountTypeEnum
    is_verified: bool
    is_primary: bool
    is_active: bool
    created_at: datetime
    verified_at: Optional[datetime]
    
    model_config = {"from_attributes": True}


# Payment Card Schemas
class PaymentCardCreate(BaseModel):
    """Payment card creation"""
    card_number: str = Field(..., min_length=13, max_length=19)
    card_holder_name: str = Field(..., min_length=2, max_length=100)
    expiry_month: str = Field(..., pattern=r'^(0[1-9]|1[0-2])$')
    expiry_year: str = Field(..., pattern=r'^20[2-9][0-9]$')
    card_type: CardTypeEnum
    bank_name: Optional[str] = Field(None, max_length=100)
    is_primary: bool = Field(default=False)
    
    @field_validator('card_number')
    def validate_card_number(cls, v):
        # Remove spaces and validate
        card_num = v.replace(' ', '')
        if not card_num.isdigit():
            raise ValueError('Card number must contain only digits')
        
        # Luhn algorithm validation
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        if luhn_checksum(card_num) != 0:
            raise ValueError('Invalid card number')
            
        return card_num


class PaymentCardResponse(BaseModel):
    """Payment card response"""
    id: int
    card_id: str
    card_last_four: str
    card_holder_name: str
    expiry_month: str
    expiry_year: str
    card_type: CardTypeEnum
    bank_name: Optional[str]
    card_network: Optional[str]
    is_verified: bool
    is_primary: bool
    is_active: bool
    created_at: datetime
    verified_at: Optional[datetime]
    
    model_config = {"from_attributes": True}


# KYC Profile Schemas
class KYCProfileCreate(BaseModel):
    """KYC profile creation"""
    personal_details: PersonalDetailsCreate
    address_details: AddressDetailsCreate


class KYCProfileResponse(BaseModel):
    """KYC profile response"""
    id: int
    kyc_id: str
    status: KYCStatusEnum
    verification_level: int
    full_name: str
    date_of_birth: date
    gender: str
    address_line1: str
    city: str
    state: str
    pincode: str
    upi_id: Optional[str]
    upi_status: str
    verification_attempts: int
    created_at: datetime
    verified_at: Optional[datetime]
    expires_at: Optional[datetime]
    
    # Related data
    documents: List[DocumentResponse] = []
    bank_accounts: List[BankAccountResponse] = []
    cards: List[PaymentCardResponse] = []
    
    model_config = {"from_attributes": True}


# Face Verification Schema
class FaceVerificationUpload(BaseModel):
    """Face image upload for verification"""
    image_quality_check: bool = Field(default=True)
    face_detection_required: bool = Field(default=True)


class FaceVerificationResponse(BaseModel):
    """Face verification response"""
    verification_id: str
    face_detected: bool
    image_quality_score: float
    verification_status: str
    confidence_score: Optional[float]
    message: str


# UPI Generation Schema
class UPIGenerationRequest(BaseModel):
    """UPI ID generation request"""
    preferred_handle: Optional[str] = Field(None, max_length=20, pattern=r'^[a-zA-Z0-9]+$')


class UPIGenerationResponse(BaseModel):
    """UPI ID generation response"""
    upi_id: str
    status: str
    activation_required: bool
    message: str


# Verification Status Schema
class VerificationStatusResponse(BaseModel):
    """Overall verification status"""
    kyc_id: str
    overall_status: KYCStatusEnum
    verification_level: int
    completion_percentage: int
    pending_steps: List[str]
    next_action: str
    upi_eligible: bool
    
    # Step-wise status
    personal_details_complete: bool
    address_verified: bool
    documents_verified: bool
    face_verified: bool
    bank_account_added: bool
    payment_card_added: bool