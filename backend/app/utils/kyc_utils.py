"""
KYC utility functions
Document processing, face verification, and UPI generation
"""
import uuid
import hashlib
import base64
import json
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from PIL import Image
import io

from ..core.security import security
from ..core.config import settings


class DocumentProcessor:
    """Document processing and OCR utilities"""
    
    @staticmethod
    def validate_aadhar_number(aadhar: str) -> bool:
        """Validate Aadhar number format and checksum"""
        # Remove spaces and validate format
        aadhar_clean = aadhar.replace(' ', '').replace('-', '')
        
        if len(aadhar_clean) != 12 or not aadhar_clean.isdigit():
            return False
        
        # Verhoeff algorithm for Aadhar validation
        multiplication_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        
        permutation_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        
        try:
            c = 0
            for i, digit in enumerate(reversed(aadhar_clean)):
                c = multiplication_table[c][permutation_table[i % 8][int(digit)]]
            return c == 0
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def validate_pan_number(pan: str) -> bool:
        """Validate PAN number format"""
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pan_pattern, pan.upper()))
    
    @staticmethod
    def extract_document_info(document_type: str, ocr_text: str) -> Dict[str, Any]:
        """Extract structured information from OCR text"""
        extracted_info = {
            "document_type": document_type,
            "extracted_fields": {},
            "confidence": 0.0
        }
        
        if document_type == "aadhar":
            # Extract Aadhar number
            aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
            aadhar_match = re.search(aadhar_pattern, ocr_text)
            if aadhar_match:
                extracted_info["extracted_fields"]["aadhar_number"] = aadhar_match.group()
            
            # Extract name (usually after "Name" or before father's name)
            name_patterns = [
                r'(?:Name|नाम)[\s:]+([A-Za-z\s]+?)(?:\n|Father|पिता)',
                r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            ]
            
            for pattern in name_patterns:
                name_match = re.search(pattern, ocr_text, re.MULTILINE | re.IGNORECASE)
                if name_match:
                    extracted_info["extracted_fields"]["name"] = name_match.group(1).strip()
                    break
        
        elif document_type == "pan":
            # Extract PAN number
            pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
            pan_match = re.search(pan_pattern, ocr_text)
            if pan_match:
                extracted_info["extracted_fields"]["pan_number"] = pan_match.group()
            
            # Extract name
            name_pattern = r'(?:Name|नाम)[\s:]+([A-Za-z\s]+?)(?:\n|Father|पिता|Date)'
            name_match = re.search(name_pattern, ocr_text, re.IGNORECASE)
            if name_match:
                extracted_info["extracted_fields"]["name"] = name_match.group(1).strip()
        
        # Calculate confidence based on extracted fields
        if extracted_info["extracted_fields"]:
            extracted_info["confidence"] = min(0.85, len(extracted_info["extracted_fields"]) * 0.3)
        
        return extracted_info
    
    @staticmethod
    def mask_document_number(doc_type: str, doc_number: str) -> str:
        """Mask document number for display"""
        if doc_type == "aadhar":
            clean_num = doc_number.replace(' ', '').replace('-', '')
            return f"XXXX XXXX {clean_num[-4:]}"
        elif doc_type == "pan":
            return f"{doc_number[:3]}XXXXXX{doc_number[-1:]}"
        elif doc_type == "account_number":
            return f"XXXXXXXX{doc_number[-4:]}"
        elif doc_type == "card_number":
            return f"XXXX XXXX XXXX {doc_number[-4:]}"
        else:
            return f"XXXXX{doc_number[-4:]}"


class FaceVerification:
    """Face verification and matching utilities"""
    
    @staticmethod
    def validate_face_image(image_data: bytes) -> Tuple[bool, str, float]:
        """Validate face image quality and detect face"""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Basic image quality checks
            if image.size[0] < 300 or image.size[1] < 300:
                return False, "Image resolution too low", 0.0
            
            if len(image_data) > 5 * 1024 * 1024:  # 5MB limit
                return False, "Image file too large", 0.0
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Simulate face detection (in production, use actual face detection)
            # This is a placeholder - integrate with actual face detection library
            face_detected = FaceVerification._simulate_face_detection(image)
            
            if not face_detected:
                return False, "No face detected in image", 0.0
            
            # Quality score (placeholder)
            quality_score = FaceVerification._calculate_image_quality(image)
            
            return True, "Face detected successfully", quality_score
            
        except Exception as e:
            return False, f"Error processing image: {str(e)}", 0.0
    
    @staticmethod
    def _simulate_face_detection(image: Image.Image) -> bool:
        """Simulate face detection (replace with actual implementation)"""
        # In production, integrate with libraries like:
        # - face_recognition
        # - OpenCV
        # - dlib
        # - Azure Face API
        # - AWS Rekognition
        
        # For now, return True if image meets basic criteria
        width, height = image.size
        return width >= 300 and height >= 300
    
    @staticmethod
    def _calculate_image_quality(image: Image.Image) -> float:
        """Calculate image quality score"""
        # Basic quality metrics
        width, height = image.size
        pixel_count = width * height
        
        # Size score
        size_score = min(1.0, pixel_count / (640 * 480))
        
        # Aspect ratio score
        aspect_ratio = width / height
        aspect_score = 1.0 if 0.7 <= aspect_ratio <= 1.4 else 0.5
        
        # Overall quality
        quality = (size_score * 0.6 + aspect_score * 0.4) * 0.9
        
        return round(quality, 2)
    
    @staticmethod
    def compare_faces(face_image1: bytes, face_image2: bytes) -> Tuple[float, bool]:
        """Compare two face images and return similarity score"""
        # Placeholder implementation
        # In production, use actual face comparison libraries
        
        try:
            # Load both images
            img1 = Image.open(io.BytesIO(face_image1))
            img2 = Image.open(io.BytesIO(face_image2))
            
            # Simulate face comparison
            # This should be replaced with actual face recognition comparison
            similarity_score = FaceVerification._simulate_face_comparison(img1, img2)
            
            # Consider match if similarity > 0.7
            is_match = similarity_score > 0.7
            
            return similarity_score, is_match
            
        except Exception:
            return 0.0, False
    
    @staticmethod
    def _simulate_face_comparison(img1: Image.Image, img2: Image.Image) -> float:
        """Simulate face comparison (replace with actual implementation)"""
        # Very basic simulation based on image properties
        # In production, use actual face encoding comparison
        
        size_similarity = min(img1.size[0] / img2.size[0], img2.size[0] / img1.size[0])
        
        # Random factor for simulation (remove in production)
        import random
        random_factor = random.uniform(0.6, 0.95)
        
        return min(0.95, size_similarity * random_factor)


class UPIGenerator:
    """UPI ID generation utilities"""
    
    @staticmethod
    def generate_upi_id(user_info: Dict[str, Any], preferred_handle: Optional[str] = None) -> str:
        """Generate unique UPI ID for verified user"""
        
        # Base handles for the super app
        app_handles = ["superapp", "spapp", "myapp"]
        
        if preferred_handle and len(preferred_handle) >= 3:
            base_id = preferred_handle.lower()
        else:
            # Generate from user info
            name_parts = user_info.get('full_name', '').lower().split()
            if len(name_parts) >= 2:
                base_id = f"{name_parts[0]}{name_parts[-1]}"
            else:
                base_id = user_info.get('username', 'user')
        
        # Clean base ID
        base_id = re.sub(r'[^a-z0-9]', '', base_id)
        base_id = base_id[:15]  # Limit length
        
        # Add random suffix for uniqueness
        import random
        suffix = random.randint(100, 999)
        
        # Choose handle
        handle = random.choice(app_handles)
        
        upi_id = f"{base_id}{suffix}@{handle}"
        
        return upi_id
    
    @staticmethod
    def validate_upi_id(upi_id: str) -> bool:
        """Validate UPI ID format"""
        upi_pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+$'
        return bool(re.match(upi_pattern, upi_id))
    
    @staticmethod
    def check_upi_availability(upi_id: str) -> bool:
        """Check if UPI ID is available (placeholder)"""
        # In production, check against database and UPI registry
        return True


class KYCStatusCalculator:
    """Calculate KYC completion status and next steps"""
    
    @staticmethod
    def calculate_completion_percentage(kyc_profile: Dict[str, Any]) -> int:
        """Calculate KYC completion percentage"""
        total_steps = 6
        completed_steps = 0
        
        # Personal details
        if kyc_profile.get('full_name'):
            completed_steps += 1
        
        # Address details
        if kyc_profile.get('address_line1'):
            completed_steps += 1
        
        # Document verification
        documents = kyc_profile.get('documents', [])
        verified_docs = [d for d in documents if d.get('verification_status') == 'verified']
        if verified_docs:
            completed_steps += 1
        
        # Face verification
        if kyc_profile.get('face_verification_score', 0) > 0:
            completed_steps += 1
        
        # Bank account
        bank_accounts = kyc_profile.get('bank_accounts', [])
        if bank_accounts:
            completed_steps += 1
        
        # Payment card (optional)
        cards = kyc_profile.get('cards', [])
        if cards:
            completed_steps += 1
        
        return int((completed_steps / total_steps) * 100)
    
    @staticmethod
    def get_next_action(kyc_profile: Dict[str, Any]) -> Tuple[str, list[str]]:
        """Get next action and pending steps"""
        pending_steps = []
        
        if not kyc_profile.get('full_name'):
            pending_steps.append("Complete personal details")
        
        if not kyc_profile.get('address_line1'):
            pending_steps.append("Add address information")
        
        documents = kyc_profile.get('documents', [])
        verified_docs = [d for d in documents if d.get('verification_status') == 'verified']
        if not verified_docs:
            pending_steps.append("Upload and verify identity documents")
        
        if not kyc_profile.get('face_verification_score'):
            pending_steps.append("Complete face verification")
        
        bank_accounts = kyc_profile.get('bank_accounts', [])
        if not bank_accounts:
            pending_steps.append("Add bank account details")
        
        # Determine next action
        if pending_steps:
            next_action = pending_steps[0]
        else:
            next_action = "KYC verification complete"
        
        return next_action, pending_steps
    
    @staticmethod
    def determine_verification_level(kyc_profile: Dict[str, Any]) -> int:
        """Determine verification level (0-2)"""
        # Level 0: Basic (personal details + address)
        # Level 1: Intermediate (+ documents verified)
        # Level 2: Full (+ face verification + bank account)
        
        level = 0
        
        # Basic level
        if kyc_profile.get('full_name') and kyc_profile.get('address_line1'):
            level = 1
        
        # Intermediate level
        documents = kyc_profile.get('documents', [])
        verified_docs = [d for d in documents if d.get('verification_status') == 'verified']
        if verified_docs and level >= 1:
            level = 2
        
        # Full level
        if (kyc_profile.get('face_verification_score', 0) > 0.7 and 
            kyc_profile.get('bank_accounts') and 
            level >= 2):
            level = 3
        
        return min(level, 2)  # Max level is 2