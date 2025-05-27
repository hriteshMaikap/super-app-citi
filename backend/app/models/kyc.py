"""
KYC models with banking-grade security
Document verification and identity management
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..core.database import Base


class KYCStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DocumentType(enum.Enum):
    AADHAR = "aadhar"
    PAN = "pan"
    PASSPORT = "passport"
    DRIVING_LICENSE = "driving_license"
    VOTER_ID = "voter_id"


class BankAccountType(enum.Enum):
    SAVINGS = "savings"
    CURRENT = "current"
    SALARY = "salary"
    NRI = "nri"


class CardType(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    PREPAID = "prepaid"


class KYCProfile(Base):
    """
    Main KYC profile linked to user
    Contains verification status and metadata
    """
    __tablename__ = "kyc_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), unique=True, nullable=False)
    kyc_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # KYC Status
    status = Column(SQLEnum(KYCStatus), default=KYCStatus.PENDING, nullable=False)
    verification_level = Column(Integer, default=0)  # 0=basic, 1=intermediate, 2=full
    
    # Personal Details (encrypted)
    full_name_encrypted = Column(Text)
    date_of_birth_encrypted = Column(Text)
    gender_encrypted = Column(Text)
    father_name_encrypted = Column(Text)
    mother_name_encrypted = Column(Text)
    
    # Address (encrypted)
    address_line1_encrypted = Column(Text)
    address_line2_encrypted = Column(Text)
    city_encrypted = Column(Text)
    state_encrypted = Column(Text)
    pincode_encrypted = Column(Text)
    country_encrypted = Column(Text, default="India")
      # Verification metadata
    face_image_path = Column(Text)  # Encrypted path to face image
    face_verification_score = Column(Text)  # Encrypted confidence score
    verification_attempts = Column(Integer, default=0)
    last_verification_attempt = Column(DateTime(timezone=True))
    
    # UPI Details
    upi_id = Column(String(100), unique=True, index=True)  # Generated after verification
    upi_status = Column(String(20), default="inactive")  # inactive, active, suspended
    
    # Audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    verified_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))  # KYC expiry
    
    # Relationships
    documents = relationship("KYCDocument", back_populates="kyc_profile", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="kyc_profile", cascade="all, delete-orphan")
    cards = relationship("PaymentCard", back_populates="kyc_profile", cascade="all, delete-orphan")


class KYCDocument(Base):
    """
    KYC documents with verification status
    """
    __tablename__ = "kyc_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(String(36), ForeignKey("kyc_profiles.kyc_id"), nullable=False)
    document_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # Document details
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    document_number_encrypted = Column(Text, nullable=False)  # Encrypted document number
    document_name_encrypted = Column(Text)  # Name as per document (encrypted)
    
    # File storage
    front_image_path = Column(Text)  # Encrypted path to front image
    back_image_path = Column(Text)  # Encrypted path to back image (if applicable)
      # OCR and verification
    ocr_text_encrypted = Column(Text)  # Extracted text (encrypted)
    verification_status = Column(String(20), default="pending")  # pending, verified, rejected
    verification_score = Column(Text)  # Encrypted confidence score
    verification_notes = Column(Text)  # Reason for rejection if any
    
    # Face matching (for Aadhar/PAN)
    face_match_score = Column(Text)  # Encrypted face matching score
    face_match_status = Column(String(20), default="pending")  # pending, matched, not_matched
    
    # Metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True))
    is_primary = Column(Boolean, default=False)  # Primary identity document
    
    # Relationships
    kyc_profile = relationship("KYCProfile", back_populates="documents")


class BankAccount(Base):
    """
    Bank account details for payments
    """
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(String(36), ForeignKey("kyc_profiles.kyc_id"), nullable=False)
    account_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # Bank details (encrypted)
    bank_name_encrypted = Column(Text, nullable=False)
    branch_name_encrypted = Column(Text)
    ifsc_code_encrypted = Column(Text, nullable=False)
    account_number_encrypted = Column(Text, nullable=False)
    account_holder_name_encrypted = Column(Text, nullable=False)
    account_type = Column(SQLEnum(BankAccountType), default=BankAccountType.SAVINGS)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))  # penny_drop, statement, manual
    verification_reference = Column(String(100))  # Reference from bank verification
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True))
    
    # Relationships
    kyc_profile = relationship("KYCProfile", back_populates="bank_accounts")


class PaymentCard(Base):
    """
    Payment card details
    """
    __tablename__ = "payment_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(String(36), ForeignKey("kyc_profiles.kyc_id"), nullable=False)
    card_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # Card details (encrypted)
    card_number_encrypted = Column(Text, nullable=False)  # Last 4 digits stored separately
    card_holder_name_encrypted = Column(Text, nullable=False)
    expiry_month_encrypted = Column(Text, nullable=False)
    expiry_year_encrypted = Column(Text, nullable=False)
    card_type = Column(SQLEnum(CardType), nullable=False)
    
    # Card metadata
    card_last_four = Column(String(4), nullable=False)  # For display purposes
    bank_name_encrypted = Column(Text)
    card_network = Column(String(20))  # visa, mastercard, rupay, amex
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))  # otp, micro_transaction
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True))
    
    # Relationships
    kyc_profile = relationship("KYCProfile", back_populates="cards")


class KYCVerificationLog(Base):
    """
    Audit log for all KYC verification attempts
    """
    __tablename__ = "kyc_verification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(String(36), ForeignKey("kyc_profiles.kyc_id"), nullable=False)
    log_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # Verification details
    verification_type = Column(String(50), nullable=False)  # document, face, bank, card
    verification_step = Column(String(50))  # upload, ocr, face_match, etc.
    status = Column(String(20), nullable=False)  # success, failed, pending
      # Results (encrypted)
    verification_data_encrypted = Column(Text)  # JSON data about verification
    error_message = Column(Text)
    confidence_score = Column(Text)  # Encrypted score
    
    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(Text)
    device_info_encrypted = Column(Text)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())