"""
Admin service for KYC management and approval workflows
Banking-grade security and audit logging
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_, or_, desc
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json

from ..models.user import User, UserRole
from ..models.kyc import KYCProfile, KYCDocument, KYCStatus, DocumentType, FaceVerification
from ..schemas.admin import (
    KYCReviewAction, KYCApplicationSummary, KYCApplication, 
    AdminDashboardStats, KYCReviewResult
)
from ..core.security import security

logger = logging.getLogger(__name__)


class AdminService:
    """Admin service for KYC management"""
    
    @staticmethod
    async def get_pending_kyc_applications(
        skip: int = 0,
        limit: int = 20,
        db: AsyncSession = None
    ) -> List[KYCApplicationSummary]:
        """Get pending KYC applications for admin review"""
        try:
            # Query for pending or in-progress KYC profiles
            kyc_query = select(
                KYCProfile, User.email, User.phone, User.username
            ).join(
                User, KYCProfile.user_id == User.user_id
            ).where(
                or_(
                    KYCProfile.kyc_status == KYCStatus.PENDING,
                    KYCProfile.kyc_status == KYCStatus.IN_PROGRESS
                )
            ).order_by(
                KYCProfile.created_at.desc()
            ).offset(skip).limit(limit)
            
            results = await db.execute(kyc_query)
            applications = []
            
            for kyc, email, phone, username in results:                # Count documents
                doc_query = select(func.count(KYCDocument.id)).where(
                    KYCDocument.kyc_id == kyc.kyc_id
                )
                doc_result = await db.execute(doc_query)
                doc_count = doc_result.scalar() or 0
                
                # Check face verification
                face_query = select(FaceVerification).where(
                    FaceVerification.kyc_profile_id == kyc.id
                )
                face_result = await db.execute(face_query)
                face_verification = face_result.scalars().first()
                
                # Decrypt name
                full_name = security.decrypt_sensitive_data(kyc.full_name_encrypted)
                
                application = KYCApplicationSummary(
                    kyc_id=kyc.id,
                    user_id=kyc.user_id,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    username=username,
                    kyc_status=kyc.kyc_status.value,
                    documents_count=doc_count,
                    verification_score=kyc.verification_score,
                    face_verified=bool(face_verification and face_verification.is_match),
                    created_at=kyc.created_at
                )
                applications.append(application)
            
            return applications
            
        except Exception as e:
            logger.error(f"Error fetching pending KYC applications: {str(e)}")
            raise
    
    @staticmethod
    async def get_kyc_application_details(
        kyc_id: int,
        db: AsyncSession = None
    ) -> KYCApplication:
        """Get detailed KYC application for admin review"""
        try:
            # Get KYC profile with user details
            kyc_query = select(
                KYCProfile, User.email, User.phone, User.username,
                User.first_name, User.last_name, User.created_at.label("user_created_at")
            ).join(
                User, KYCProfile.user_id == User.user_id
            ).where(
                KYCProfile.id == kyc_id
            )
            
            result = await db.execute(kyc_query)
            kyc_data = result.first()
            
            if not kyc_data:
                raise ValueError(f"KYC application with ID {kyc_id} not found")
                
            kyc, email, phone, username, first_name, last_name, user_created_at = kyc_data
              # Get documents
            doc_query = select(KYCDocument).where(
                KYCDocument.kyc_id == kyc.kyc_id
            )
            doc_result = await db.execute(doc_query)
            documents = doc_result.scalars().all()
            
            # Get face verification
            face_query = select(FaceVerification).where(
                FaceVerification.kyc_profile_id == kyc.id
            )
            face_result = await db.execute(face_query)
            face_verification = face_result.scalars().first()
            
            # Decrypt sensitive data
            full_name = security.decrypt_sensitive_data(kyc.full_name_encrypted)
            dob_str = security.decrypt_sensitive_data(kyc.date_of_birth_encrypted)
            dob = datetime.fromisoformat(dob_str).date()
            address = security.decrypt_sensitive_data(kyc.address_encrypted)
            aadhar = security.decrypt_sensitive_data(kyc.aadhar_number_encrypted)
            pan = security.decrypt_sensitive_data(kyc.pan_number_encrypted)
            
            # Format documents
            document_list = []
            for doc in documents:
                extracted_data = {}
                if doc.extracted_data_encrypted:
                    extracted_text = security.decrypt_sensitive_data(doc.extracted_data_encrypted)
                    extracted_data = json.loads(extracted_text)
                
                document_list.append({
                    "id": doc.id,
                    "document_type": doc.document_type.value,
                    "file_name": security.decrypt_sensitive_data(doc.file_name_encrypted),
                    "file_path": security.decrypt_sensitive_data(doc.file_path_encrypted),
                    "file_size": doc.file_size,
                    "mime_type": doc.mime_type,
                    "is_verified": doc.is_verified,
                    "verification_score": doc.verification_score,
                    "uploaded_at": doc.uploaded_at,
                    "extracted_data": extracted_data
                })
            
            # Format face verification
            face_data = None
            if face_verification:
                face_data = {
                    "id": face_verification.id,
                    "selfie_path": security.decrypt_sensitive_data(face_verification.selfie_path_encrypted),
                    "document_face_path": security.decrypt_sensitive_data(face_verification.document_face_path_encrypted) 
                    if face_verification.document_face_path_encrypted else None,
                    "match_score": face_verification.match_score,
                    "is_match": face_verification.is_match,
                    "confidence_score": face_verification.confidence_score,
                    "verified_at": face_verification.verified_at
                }
            
            # Create response
            application = KYCApplication(
                kyc_id=kyc.id,
                user_id=kyc.user_id,
                email=email,
                phone=phone,
                username=username,
                first_name=first_name,
                last_name=last_name,
                user_created_at=user_created_at,
                full_name=full_name,
                date_of_birth=dob,
                address=address,
                aadhar_number=aadhar,
                pan_number=pan,
                kyc_status=kyc.kyc_status.value,
                verification_score=kyc.verification_score,
                face_match_score=kyc.face_match_score,
                created_at=kyc.created_at,
                updated_at=kyc.updated_at,
                verified_at=kyc.verified_at,
                verified_by=kyc.verified_by,
                verification_notes=kyc.verification_notes,
                documents=document_list,
                face_verification=face_data
            )
            
            return application
            
        except ValueError as e:
            logger.error(f"KYC application retrieval error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error fetching KYC application details: {str(e)}")
            raise
    
    @staticmethod
    async def review_kyc_application(
        kyc_id: int,
        admin_id: str,
        action: KYCReviewAction,
        db: AsyncSession = None
    ) -> KYCReviewResult:
        """Review and approve/reject KYC application"""
        try:
            # Get KYC profile
            kyc_query = select(KYCProfile).where(KYCProfile.id == kyc_id)
            kyc_result = await db.execute(kyc_query)
            kyc = kyc_result.scalars().first()
            
            if not kyc:
                raise ValueError(f"KYC application with ID {kyc_id} not found")
                
            # Update KYC status based on action
            if action.action == "approve":
                kyc.kyc_status = KYCStatus.VERIFIED
                status_text = "approved"
            elif action.action == "reject":
                kyc.kyc_status = KYCStatus.REJECTED
                status_text = "rejected"
            else:
                raise ValueError("Invalid action. Must be 'approve' or 'reject'")
            
            # Set verification details
            kyc.verified_by = admin_id
            kyc.verification_notes = action.notes
            kyc.verified_at = datetime.utcnow()
            
            # Update user if necessary
            if action.action == "approve":
                user_query = select(User).where(User.user_id == kyc.user_id)
                user_result = await db.execute(user_query)
                user = user_result.scalars().first()
                
                if user:
                    user.is_verified = True
            
            # Commit changes
            await db.commit()
            
            logger.info(f"KYC application {kyc_id} {status_text} by admin {admin_id}")
            
            return KYCReviewResult(
                kyc_id=kyc.id,
                action=action.action,
                status=kyc.kyc_status.value,
                reviewer=admin_id,
                review_time=kyc.verified_at,
                notes=action.notes,
                message=f"KYC application successfully {status_text}"
            )
            
        except ValueError as e:
            await db.rollback()
            logger.error(f"KYC review error: {str(e)}")
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Error reviewing KYC application: {str(e)}")
            raise
    
    @staticmethod
    async def get_dashboard_statistics(db: AsyncSession = None) -> AdminDashboardStats:
        """Get admin dashboard statistics"""
        try:
            # Total users
            users_query = select(func.count(User.id))
            users_result = await db.execute(users_query)
            total_users = users_result.scalar() or 0
            
            # Verified users
            verified_users_query = select(func.count(User.id)).where(User.is_verified == True)
            verified_users_result = await db.execute(verified_users_query)
            verified_users = verified_users_result.scalar() or 0
            
            # KYC stats by status
            kyc_stats = {}
            for status in KYCStatus:
                status_query = select(func.count(KYCProfile.id)).where(
                    KYCProfile.kyc_status == status
                )
                status_result = await db.execute(status_query)
                kyc_stats[status.value] = status_result.scalar() or 0
            
            # Recent applications (last 7 days)
            recent_query = select(func.count(KYCProfile.id)).where(
                KYCProfile.created_at >= func.now() - func.interval("7 days")
            )
            recent_result = await db.execute(recent_query)
            recent_applications = recent_result.scalar() or 0
            
            # Average verification score
            avg_score_query = select(func.avg(KYCProfile.verification_score)).where(
                KYCProfile.kyc_status == KYCStatus.VERIFIED
            )
            avg_score_result = await db.execute(avg_score_query)
            avg_verification_score = avg_score_result.scalar() or 0
            
            return AdminDashboardStats(
                total_users=total_users,
                verified_users=verified_users,
                kyc_stats=kyc_stats,
                recent_applications=recent_applications,
                avg_verification_score=float(avg_verification_score)
            )
            
        except Exception as e:
            logger.error(f"Error generating admin dashboard statistics: {str(e)}")
            raise


# Create singleton instance
admin_service = AdminService()
