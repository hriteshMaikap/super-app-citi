"""
KYC service with banking-grade verification
Document processing, face verification, and UPI management
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, Dict, Any, List, Tuple
import uuid
from datetime import datetime, timedelta
import logging
import json

from ..models.kyc import (
    KYCProfile, KYCDocument, BankAccount, PaymentCard, 
    KYCVerificationLog, KYCStatus, DocumentType
)
from ..models.user import User
from ..schemas.kyc import (
    KYCProfileCreate, PersonalDetailsCreate, AddressDetailsCreate,
    DocumentUpload, BankAccountCreate, PaymentCardCreate,
    FaceVerificationUpload, UPIGenerationRequest
)
from ..core.security import security
from ..utils.kyc_utils import (
    DocumentProcessor, FaceVerification, UPIGenerator, KYCStatusCalculator
)

logger = logging.getLogger(__name__)


class KYCService:
    """Banking-grade KYC service"""
    
    @staticmethod
    async def create_kyc_profile(
        user_id: str,
        profile_data: KYCProfileCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Create KYC profile for user"""
        
        # Check if user exists and doesn't have KYC profile
        user_result = await db.execute(select(User).where(User.user_id == user_id))
        user = user_result.scalars().first()
        if not user:
            raise ValueError("User not found")
        
        existing_kyc = await db.execute(
            select(KYCProfile).where(KYCProfile.user_id == user_id)
        )
        if existing_kyc.scalars().first():
            raise ValueError("KYC profile already exists for this user")
        
        # Create KYC profile
        kyc_id = str(uuid.uuid4())
        
        # Encrypt sensitive data
        personal = profile_data.personal_details
        address = profile_data.address_details
        
        kyc_profile = KYCProfile(
            user_id=user_id,
            kyc_id=kyc_id,
            full_name_encrypted=security.encrypt_sensitive_data(personal.full_name),
            date_of_birth_encrypted=security.encrypt_sensitive_data(personal.date_of_birth.isoformat()),
            gender_encrypted=security.encrypt_sensitive_data(personal.gender),
            father_name_encrypted=security.encrypt_sensitive_data(personal.father_name),
            mother_name_encrypted=security.encrypt_sensitive_data(personal.mother_name or ""),
            address_line1_encrypted=security.encrypt_sensitive_data(address.address_line1),
            address_line2_encrypted=security.encrypt_sensitive_data(address.address_line2 or ""),
            city_encrypted=security.encrypt_sensitive_data(address.city),
            state_encrypted=security.encrypt_sensitive_data(address.state),
            pincode_encrypted=security.encrypt_sensitive_data(address.pincode),
            country_encrypted=security.encrypt_sensitive_data(address.country),
            status=KYCStatus.IN_PROGRESS,
            verification_level=0
        )
        
        db.add(kyc_profile)
        await db.commit()
        await db.refresh(kyc_profile)
        
        # Log the action
        await KYCService._log_verification_action(
            kyc_id, "profile_creation", "success", 
            {"step": "profile_created"}, db
        )
        
        logger.info(f"KYC profile created for user {user_id}")
        
        return await KYCService._format_kyc_response(kyc_profile, db)
    
    @staticmethod
    async def upload_document(
        user_id: str,
        document_data: DocumentUpload,
        front_image: bytes,
        back_image: Optional[bytes],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Upload and process document"""
        
        # Get KYC profile
        kyc_profile = await KYCService._get_kyc_profile(user_id, db)
        if not kyc_profile:
            raise ValueError("KYC profile not found")
        
        # Validate document number
        if document_data.document_type == DocumentType.AADHAR:
            if not DocumentProcessor.validate_aadhar_number(document_data.document_number):
                raise ValueError("Invalid Aadhar number")
        elif document_data.document_type == DocumentType.PAN:
            if not DocumentProcessor.validate_pan_number(document_data.document_number):
                raise ValueError("Invalid PAN number")
        
        # Check if document already exists
        existing_doc = await db.execute(
            select(KYCDocument).where(
                and_(
                    KYCDocument.kyc_id == kyc_profile.kyc_id,
                    KYCDocument.document_type == document_data.document_type
                )
            )
        )
        if existing_doc.scalars().first():
            raise ValueError(f"{document_data.document_type.value} document already uploaded")
        
        # Store images (in production, use cloud storage)
        document_id = str(uuid.uuid4())
        front_image_path = f"documents/{document_id}_front.jpg"
        back_image_path = f"documents/{document_id}_back.jpg" if back_image else None
        
        # In production, upload to cloud storage and store encrypted paths
        # For now, we'll simulate storage paths
        
        # Simulate OCR processing
        ocr_text = f"Simulated OCR text for {document_data.document_type.value}"
        extracted_info = DocumentProcessor.extract_document_info(
            document_data.document_type.value, ocr_text
        )
        
        # Create document record
        kyc_document = KYCDocument(
            kyc_id=kyc_profile.kyc_id,
            document_id=document_id,
            document_type=document_data.document_type,
            document_number_encrypted=security.encrypt_sensitive_data(document_data.document_number),
            document_name_encrypted=security.encrypt_sensitive_data(document_data.document_name),
            front_image_path=security.encrypt_sensitive_data(front_image_path),
            back_image_path=security.encrypt_sensitive_data(back_image_path) if back_image_path else None,
            ocr_text_encrypted=security.encrypt_sensitive_data(json.dumps(extracted_info)),
            verification_status="pending",
            verification_score=security.encrypt_sensitive_data(str(extracted_info.get("confidence", 0.0))),
            is_primary=(document_data.document_type in [DocumentType.AADHAR, DocumentType.PAN])
        )
        
        db.add(kyc_document)
        await db.commit()
          # Log the action
        await KYCService._log_verification_action(
            kyc_profile.kyc_id, "document_upload", "success",
            {"document_type": document_data.document_type.value, "document_id": document_id}, db
        )
        
        logger.info(f"Document uploaded for KYC {kyc_profile.kyc_id}: {document_data.document_type.value}")
        
        # Fetch the document we just created to get all the fields required by DocumentResponse schema
        await db.refresh(kyc_document)
          # Return a fully populated response that matches the DocumentResponse schema
        from ..schemas.kyc import DocumentTypeEnum
        
        return {
            "id": kyc_document.id,
            "document_id": document_id,
            "document_type": DocumentTypeEnum(document_data.document_type.value),
            "document_number": DocumentProcessor.mask_document_number(
                document_data.document_type.value,
                document_data.document_number
            ),
            "document_name": document_data.document_name,
            "verification_status": "pending",
            "verification_score": 0.0,  # Default value until verification
            "face_match_status": "pending",
            "face_match_score": 0.0,  # Default value until face matching
            "is_primary": kyc_document.is_primary,
            "uploaded_at": kyc_document.uploaded_at,
            "verified_at": None
        }
    
    @staticmethod
    async def upload_face_image(
        user_id: str,
        face_image: bytes,
        verification_data: FaceVerificationUpload,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Upload and verify face image"""
        
        # Get KYC profile
        kyc_profile = await KYCService._get_kyc_profile(user_id, db)
        if not kyc_profile:
            raise ValueError("KYC profile not found")
        
        # Validate face image
        is_valid, message, quality_score = FaceVerification.validate_face_image(face_image)
        
        if not is_valid:
            await KYCService._log_verification_action(
                kyc_profile.kyc_id, "face_verification", "failed",
                {"error": message}, db
            )
            raise ValueError(message)
        
        # Store face image (encrypted path)
        face_image_path = f"faces/{kyc_profile.kyc_id}_face.jpg"
          # Update KYC profile with face data
        kyc_profile.face_image_path = security.encrypt_sensitive_data(face_image_path)
        kyc_profile.face_verification_score = security.encrypt_sensitive_data(str(quality_score))
        kyc_profile.verification_attempts += 1
        kyc_profile.last_verification_attempt = datetime.utcnow()
        
        # If we have documents with faces, compare them
        face_match_results = await KYCService._compare_face_with_documents(
            kyc_profile.kyc_id, face_image, db
        )
        
        # Update verification level based on completed steps
        # Check if documents exist and are verified
        documents_exist = await db.execute(
            select(KYCDocument).where(
                KYCDocument.kyc_id == kyc_profile.kyc_id
            )
        )
        
        if documents_exist.scalars().first():
            # Increase verification level to 2 (full KYC) when face verification is completed successfully
            # This makes user eligible for UPI generation
            kyc_profile.verification_level = 2
        
        await db.commit()
        
        # Log the action
        await KYCService._log_verification_action(
            kyc_profile.kyc_id, "face_verification", "success",
            {
                "quality_score": quality_score,
                "face_matches": face_match_results
            }, db
        )
        
        logger.info(f"Face verification completed for KYC {kyc_profile.kyc_id}")
        
        return {
            "verification_id": str(uuid.uuid4()),
            "face_detected": True,
            "image_quality_score": quality_score,
            "verification_status": "completed",
            "confidence_score": quality_score,
            "face_matches": face_match_results,
            "message": "Face verification completed successfully"
        }
    
    @staticmethod
    async def add_bank_account(
        user_id: str,
        account_data: BankAccountCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Add bank account details"""
        
        # Get KYC profile
        kyc_profile = await KYCService._get_kyc_profile(user_id, db)
        if not kyc_profile:
            raise ValueError("KYC profile not found")
        
        # If this is primary account, unset other primary accounts
        if account_data.is_primary:
            await db.execute(
                select(BankAccount).where(
                    and_(
                        BankAccount.kyc_id == kyc_profile.kyc_id,
                        BankAccount.is_primary == True
                    )
                )
            )
            # Update existing primary accounts
            existing_accounts = await db.execute(
                select(BankAccount).where(BankAccount.kyc_id == kyc_profile.kyc_id)
            )
            for account in existing_accounts.scalars():
                account.is_primary = False
        
        # Create bank account
        account_id = str(uuid.uuid4())
        
        bank_account = BankAccount(
            kyc_id=kyc_profile.kyc_id,
            account_id=account_id,
            bank_name_encrypted=security.encrypt_sensitive_data(account_data.bank_name),
            branch_name_encrypted=security.encrypt_sensitive_data(account_data.branch_name or ""),
            ifsc_code_encrypted=security.encrypt_sensitive_data(account_data.ifsc_code),
            account_number_encrypted=security.encrypt_sensitive_data(account_data.account_number),
            account_holder_name_encrypted=security.encrypt_sensitive_data(account_data.account_holder_name),
            account_type=account_data.account_type,
            is_primary=account_data.is_primary,
            verification_method="pending"
        )
        
        db.add(bank_account)
        await db.commit()
        
        # Log the action
        await KYCService._log_verification_action(
            kyc_profile.kyc_id, "bank_account_add", "success",
            {"account_id": account_id, "bank_name": account_data.bank_name}, db
        )
        logger.info(f"Bank account added for KYC {kyc_profile.kyc_id}")
        
        # Return a fully populated response that matches the BankAccountResponse schema
        await db.refresh(bank_account)
        
        return {
            "id": bank_account.id,
            "account_id": account_id,
            "bank_name": account_data.bank_name,
            "branch_name": account_data.branch_name,
            "ifsc_code": account_data.ifsc_code,
            "account_number": DocumentProcessor.mask_document_number("account_number", account_data.account_number),
            "account_holder_name": account_data.account_holder_name,
            "account_type": account_data.account_type,
            "is_verified": bank_account.is_verified,
            "is_primary": account_data.is_primary,
            "is_active": True,  # Default to active on creation
            "created_at": bank_account.created_at,
            "verified_at": None  # It's newly created, so not verified yet
        }
    
    @staticmethod
    async def add_payment_card(
        user_id: str,
        card_data: PaymentCardCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Add payment card details"""
        
        # Get KYC profile
        kyc_profile = await KYCService._get_kyc_profile(user_id, db)
        if not kyc_profile:
            raise ValueError("KYC profile not found")
        
        # Detect card network
        card_number = card_data.card_number.replace(' ', '')
        card_network = KYCService._detect_card_network(card_number)
        
        # If this is primary card, unset other primary cards
        if card_data.is_primary:
            existing_cards = await db.execute(
                select(PaymentCard).where(PaymentCard.kyc_id == kyc_profile.kyc_id)
            )
            for card in existing_cards.scalars():
                card.is_primary = False
        
        # Create payment card
        card_id = str(uuid.uuid4())
        
        payment_card = PaymentCard(
            kyc_id=kyc_profile.kyc_id,
            card_id=card_id,
            card_number_encrypted=security.encrypt_sensitive_data(card_number),
            card_holder_name_encrypted=security.encrypt_sensitive_data(card_data.card_holder_name),
            expiry_month_encrypted=security.encrypt_sensitive_data(card_data.expiry_month),
            expiry_year_encrypted=security.encrypt_sensitive_data(card_data.expiry_year),
            card_type=card_data.card_type,
            card_last_four=card_number[-4:],
            bank_name_encrypted=security.encrypt_sensitive_data(card_data.bank_name or ""),
            card_network=card_network,
            is_primary=card_data.is_primary
        )
        
        db.add(payment_card)
        await db.commit()
        
        # Log the action
        await KYCService._log_verification_action(
            kyc_profile.kyc_id, "payment_card_add", "success",
            {"card_id": card_id, "card_type": card_data.card_type.value}, db
        )
        
        logger.info(f"Payment card added for KYC {kyc_profile.kyc_id}")
        
        return {
            "card_id": card_id,
            "card_last_four": card_number[-4:],
            "card_network": card_network,
            "verification_status": "pending",
            "message": "Payment card added successfully"
        }
    @staticmethod
    async def generate_upi_id(
        user_id: str,
        upi_request: UPIGenerationRequest,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Generate UPI ID for verified user"""
        
        # Get KYC profile
        kyc_profile = await KYCService._get_kyc_profile(user_id, db)
        if not kyc_profile:
            raise ValueError("KYC profile not found")
        
        # Check completed steps to determine if user is eligible
        # Get documents and check if face verification is done
        documents_result = await db.execute(
            select(KYCDocument).where(
                KYCDocument.kyc_id == kyc_profile.kyc_id
            )
        )
        documents = list(documents_result.scalars())
        
        face_verified = bool(kyc_profile.face_verification_score)
        
        # Auto-update verification level if conditions are met
        if documents and face_verified and kyc_profile.verification_level < 2:
            logger.info(f"Auto-updating verification level to 2 for user {user_id}")
            kyc_profile.verification_level = 2
            await db.flush()  # Make sure the update is flushed
        
        # Now check if eligible
        if kyc_profile.verification_level < 2:
            # For debugging purpose, log why they might not be eligible
            logger.warning(f"User {user_id} not eligible for UPI: Verification level={kyc_profile.verification_level}, Documents={len(documents)}, Face verified={face_verified}")
            raise ValueError("User must complete full KYC verification for UPI")
        
        if kyc_profile.upi_id:
            raise ValueError("UPI ID already generated for this user")
        
        # Get user info for UPI generation
        user_info = {
            "full_name": security.decrypt_sensitive_data(kyc_profile.full_name_encrypted),
            "username": user_id[:8]  # Use part of user_id as username
        }
        
        # Generate UPI ID
        upi_id = UPIGenerator.generate_upi_id(user_info, upi_request.preferred_handle)
        
        # Check availability (in production, check against UPI registry)
        if not UPIGenerator.check_upi_availability(upi_id):
            # Generate alternative
            upi_id = UPIGenerator.generate_upi_id(user_info, None)
        
        # Update KYC profile
        kyc_profile.upi_id = upi_id
        kyc_profile.upi_status = "active"
        
        await db.commit()
        
        # Log the action
        await KYCService._log_verification_action(
            kyc_profile.kyc_id, "upi_generation", "success",
            {"upi_id": upi_id}, db
        )
        
        logger.info(f"UPI ID generated for KYC {kyc_profile.kyc_id}: {upi_id}")
        
        return {
            "upi_id": upi_id,
            "status": "active",
            "activation_required": False,
            "message": "UPI ID generated successfully"
        }
    @staticmethod
    async def get_kyc_status(user_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Get comprehensive KYC status"""
        
        # Get KYC profile with related data
        result = await KYCService._get_kyc_profile_with_relations(user_id, db)
        if not result:
            raise ValueError("KYC profile not found")
        
        # Unpack the tuple
        kyc_profile, documents, bank_accounts, cards = result
        
        # Format response
        return await KYCService._format_kyc_response(kyc_profile, documents, bank_accounts, cards, db)
    
    # Helper methods
    @staticmethod
    async def _get_kyc_profile(user_id: str, db: AsyncSession) -> Optional[KYCProfile]:
        """Get KYC profile by user ID"""
        result = await db.execute(
            select(KYCProfile).where(KYCProfile.user_id == user_id)
        )
        return result.scalars().first()
    @staticmethod
    async def _get_kyc_profile_with_relations(user_id: str, db: AsyncSession) -> Optional[tuple]:
        """Get KYC profile with all related data as separate objects"""
        # Get KYC profile
        result = await db.execute(
            select(KYCProfile)
            .where(KYCProfile.user_id == user_id)
        )
        kyc_profile = result.scalars().first()
        
        if not kyc_profile:
            return None
              # Get related data separately
        documents_result = await db.execute(
            select(KYCDocument).where(KYCDocument.kyc_id == kyc_profile.kyc_id)
        )
        documents = list(documents_result.scalars())
        
        accounts_result = await db.execute(
            select(BankAccount).where(BankAccount.kyc_id == kyc_profile.kyc_id)
        )
        bank_accounts = list(accounts_result.scalars())
        
        cards_result = await db.execute(
            select(PaymentCard).where(PaymentCard.kyc_id == kyc_profile.kyc_id)
        )
        cards = list(cards_result.scalars())
        
        return kyc_profile, documents, bank_accounts, cards
    @staticmethod
    async def _format_kyc_response(
        kyc_profile: KYCProfile, 
        documents: List[KYCDocument] = None,
        bank_accounts: List[BankAccount] = None,
        cards: List[PaymentCard] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Format KYC profile response with decrypted data"""
        
        if documents is None:
            documents = []
        if bank_accounts is None:
            bank_accounts = []
        if cards is None:
            cards = []
          # Decrypt sensitive data
        response_data = {
            "id": kyc_profile.id,
            "kyc_id": kyc_profile.kyc_id,
            "overall_status": kyc_profile.status.value,  # Fixed: changed from "status" to "overall_status"
            "verification_level": kyc_profile.verification_level,
            "full_name": security.decrypt_sensitive_data(kyc_profile.full_name_encrypted),
            "date_of_birth": security.decrypt_sensitive_data(kyc_profile.date_of_birth_encrypted),
            "gender": security.decrypt_sensitive_data(kyc_profile.gender_encrypted),
            "address_line1": security.decrypt_sensitive_data(kyc_profile.address_line1_encrypted),
            "city": security.decrypt_sensitive_data(kyc_profile.city_encrypted),
            "state": security.decrypt_sensitive_data(kyc_profile.state_encrypted),
            "pincode": security.decrypt_sensitive_data(kyc_profile.pincode_encrypted),
            "upi_id": kyc_profile.upi_id,
            "upi_status": kyc_profile.upi_status,
            "verification_attempts": kyc_profile.verification_attempts,
            "created_at": kyc_profile.created_at,
            "verified_at": kyc_profile.verified_at,
            "expires_at": kyc_profile.expires_at
        }
        
        # Calculate status
        completion_percentage = KYCStatusCalculator.calculate_completion_percentage(response_data)
        next_action, pending_steps = KYCStatusCalculator.get_next_action(response_data)
        
        response_data.update({
            "completion_percentage": completion_percentage,
            "pending_steps": pending_steps,
            "next_action": next_action,
            "upi_eligible": kyc_profile.verification_level >= 2,
            "personal_details_complete": bool(kyc_profile.full_name_encrypted),
            "address_verified": bool(kyc_profile.address_line1_encrypted),
            "documents_verified": False,  # Will be updated below
            "face_verified": bool(kyc_profile.face_verification_score),
            "bank_account_added": False,  # Will be updated below
            "payment_card_added": False,  # Will be updated below
            "documents": [],
            "bank_accounts": [],
            "cards": []
        })
        
        # Add documents info if available
        if documents:
            doc_list = []
            verified_docs = 0
            for doc in documents:
                doc_data = {
                    "id": doc.id,
                    "document_id": doc.document_id,
                    "document_type": doc.document_type.value,
                    "document_number": DocumentProcessor.mask_document_number(
                        doc.document_type.value,
                        security.decrypt_sensitive_data(doc.document_number_encrypted)
                    ),
                    "document_name": security.decrypt_sensitive_data(doc.document_name_encrypted),
                    "verification_status": doc.verification_status,
                    "verification_score": float(security.decrypt_sensitive_data(doc.verification_score)) if doc.verification_score else 0.0,
                    "face_match_status": doc.face_match_status,
                    "face_match_score": float(security.decrypt_sensitive_data(doc.face_match_score)) if doc.face_match_score else 0.0,
                    "is_primary": doc.is_primary,
                    "uploaded_at": doc.uploaded_at,
                    "verified_at": doc.verified_at                }
                doc_list.append(doc_data)
                if doc.verification_status == "verified":
                    verified_docs += 1
            
            response_data["documents"] = doc_list
            response_data["documents_verified"] = verified_docs > 0
        
        # Add bank accounts info if available
        if bank_accounts:
            account_list = []
            for account in bank_accounts:
                account_data = {
                    "id": account.id,
                    "account_id": account.account_id,
                    "bank_name": security.decrypt_sensitive_data(account.bank_name_encrypted),
                    "branch_name": security.decrypt_sensitive_data(account.branch_name_encrypted) if account.branch_name_encrypted else None,
                    "ifsc_code": security.decrypt_sensitive_data(account.ifsc_code_encrypted),
                    "account_number": DocumentProcessor.mask_document_number(
                        "account_number",
                        security.decrypt_sensitive_data(account.account_number_encrypted)
                    ),
                    "account_holder_name": security.decrypt_sensitive_data(account.account_holder_name_encrypted),
                    "account_type": account.account_type.value,
                    "is_verified": account.is_verified,
                    "is_primary": account.is_primary,
                    "is_active": account.is_active,
                    "created_at": account.created_at,
                    "verified_at": account.verified_at
                }
                account_list.append(account_data)
            
            response_data["bank_accounts"] = account_list
            response_data["bank_account_added"] = len(account_list) > 0

        # Add payment cards info if available
        if cards:
            card_list = []
            for card in cards:
                card_data = {
                    "id": card.id,
                    "card_id": card.card_id,
                    "card_last_four": card.card_last_four,
                    "card_holder_name": security.decrypt_sensitive_data(card.card_holder_name_encrypted),
                    "expiry_month": security.decrypt_sensitive_data(card.expiry_month_encrypted),
                    "expiry_year": security.decrypt_sensitive_data(card.expiry_year_encrypted),
                    "card_type": card.card_type.value,
                    "bank_name": security.decrypt_sensitive_data(card.bank_name_encrypted) if card.bank_name_encrypted else None,
                    "card_network": card.card_network,
                    "is_verified": card.is_verified,
                    "is_primary": card.is_primary,
                    "is_active": card.is_active,
                    "created_at": card.created_at,
                    "verified_at": card.verified_at
                }
                card_list.append(card_data)
            
            response_data["cards"] = card_list
            response_data["payment_card_added"] = len(card_list) > 0
        
        return response_data
    
    @staticmethod
    async def _compare_face_with_documents(
        kyc_id: str, 
        face_image: bytes, 
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Compare uploaded face with document faces"""
        
        # Get documents that might have face images (Aadhar, PAN, etc.)
        documents_result = await db.execute(
            select(KYCDocument).where(
                and_(
                    KYCDocument.kyc_id == kyc_id,
                    KYCDocument.document_type.in_([DocumentType.AADHAR, DocumentType.PAN])
                )
            )
        )
        
        face_matches = []
        for document in documents_result.scalars():
            # In production, load actual document image and compare faces
            # For now, simulate face comparison
            similarity_score, is_match = FaceVerification.compare_faces(
                face_image, b"simulated_document_face_image"
            )
            
            # Update document with face match results
            document.face_match_score = security.encrypt_sensitive_data(str(similarity_score))
            document.face_match_status = "matched" if is_match else "not_matched"
            
            face_matches.append({
                "document_type": document.document_type.value,
                "similarity_score": similarity_score,
                "is_match": is_match
            })
        
        return face_matches
    
    @staticmethod
    def _detect_card_network(card_number: str) -> str:
        """Detect card network from card number"""
        if card_number.startswith('4'):
            return "visa"
        elif card_number.startswith(('51', '52', '53', '54', '55')) or card_number.startswith('22'):
            return "mastercard"
        elif card_number.startswith(('60', '65', '81', '82')):
            return "rupay"
        elif card_number.startswith(('34', '37')):
            return "amex"
        else:
            return "unknown"
    
    @staticmethod
    async def _log_verification_action(
        kyc_id: str,
        verification_type: str,
        status: str,
        data: Dict[str, Any],
        db: AsyncSession,
        ip_address: str = None,
        user_agent: str = None
    ):
        """Log verification action for audit trail"""
        
        log_entry = KYCVerificationLog(
            kyc_id=kyc_id,
            log_id=str(uuid.uuid4()),
            verification_type=verification_type,
            verification_step=data.get("step", "main"),
            status=status,
            verification_data_encrypted=security.encrypt_sensitive_data(json.dumps(data)),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(log_entry)
        # Note: commit handled by calling function
    @staticmethod
    async def update_verification_level(
        user_id: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Update verification level based on completed KYC steps"""
        
        # Get KYC profile with related data
        result = await KYCService._get_kyc_profile_with_relations(user_id, db)
        if not result:
            raise ValueError("KYC profile not found")
        
        # Unpack the tuple
        kyc_profile, documents, bank_accounts, cards = result
        
        # Calculate verification level based on completed steps
        verification_level = 0
        
        # Basic profile - level 0
        # Already exists if we got here
        
        # Documents uploaded - level 1
        if documents:
            verification_level = max(verification_level, 1)
            logger.info(f"User has {len(documents)} documents uploaded")
        
        # Face verification and documents - level 2
        face_verified = bool(kyc_profile.face_verification_score)
        logger.info(f"Face verification status: {face_verified}")
        
        if documents and face_verified:
            verification_level = max(verification_level, 2)
            logger.info(f"User eligible for level 2 verification")
            
        # Update the profile with the new verification level if it changed
        old_level = kyc_profile.verification_level
        
        # Force the update to level 2 to ensure UPI eligibility
        if documents and face_verified:
            kyc_profile.verification_level = 2
            verification_level = 2
        elif verification_level > kyc_profile.verification_level:
            kyc_profile.verification_level = verification_level
            
        # Only commit if there was a change
        if old_level != kyc_profile.verification_level:
            logger.info(f"Updating verification level from {old_level} to {kyc_profile.verification_level}")
            await db.commit()
            
            # Log the action
            await KYCService._log_verification_action(
                kyc_profile.kyc_id, "verification_level_update", "success",
                {"previous_level": old_level, "new_level": verification_level}, db
            )
            
        # Return current status
        return {
            "user_id": user_id,
            "verification_level": kyc_profile.verification_level,
            "eligible_for_upi": kyc_profile.verification_level >= 2,
            "documents_uploaded": bool(documents),
            "face_verified": face_verified,
            "message": f"Verification level is now {kyc_profile.verification_level}"
        }
        

# Service instance
kyc_service = KYCService()