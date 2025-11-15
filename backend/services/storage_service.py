import cloudinary
import cloudinary.uploader
import cloudinary.api
from config.settings import settings
from utils.app_logger import logger
import os
from typing import List, Dict, Optional
from datetime import datetime

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

class StorageService:

    @staticmethod
    def upload_file(file_path: str, folder: str = None, public_id: str = None, resource_type: str = "raw") -> str:
        """
        Upload a file (PDF, Word doc, etc.) to Cloudinary and return the download URL
        
        Args:
            file_path: Local path to the file to upload
            folder: Optional folder path in Cloudinary (e.g., 'teachers/teacher_id')
            public_id: Optional public ID for the file (filename without extension)
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            str: Download URL of the uploaded file, or None if upload failed
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            # Prepare upload options
            upload_options = {
                'resource_type': resource_type
            }
            
            if folder:
                upload_options['folder'] = folder
            
            if public_id:
                upload_options['public_id'] = public_id
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(file_path, **upload_options)
            
            # Get the secure URL
            url = result.get('secure_url') or result.get('url')
            
            logger.info(f"File uploaded successfully to Cloudinary: {os.path.basename(file_path)}")
            logger.info(f"Download URL: {url}")
            
            return url
            
        except Exception as e:
            logger.error(f"Error uploading file to Cloudinary: {e}")
            logger.exception("Full error details:")
            return None

    @staticmethod
    def upload_file_from_bytes(file_bytes: bytes, filename: str, folder: str = None, public_id: str = None, resource_type: str = "raw") -> str:
        """
        Upload file from bytes to Cloudinary and return the download URL
        
        Args:
            file_bytes: File content as bytes
            filename: Original filename (used to determine file type)
            folder: Optional folder path in Cloudinary
            public_id: Optional public ID for the file
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            str: Download URL of the uploaded file, or None if upload failed
        """
        try:
            upload_options = {
                'resource_type': resource_type
            }
            
            if folder:
                upload_options['folder'] = folder
            
            if public_id:
                upload_options['public_id'] = public_id
            
            # Upload from bytes
            result = cloudinary.uploader.upload(
                file_bytes,
                filename=filename,
                **upload_options
            )
            
            # Get the secure URL
            url = result.get('secure_url') or result.get('url')
            
            logger.info(f"File uploaded from bytes successfully to Cloudinary: {filename}")
            logger.info(f"Download URL: {url}")
            
            return url
            
        except Exception as e:
            logger.error(f"Error uploading file from bytes to Cloudinary: {e}")
            logger.exception("Full error details:")
            return None

    @staticmethod
    def upload_files_bulk(file_paths: List[str], folder: str = None, resource_type: str = "raw") -> Dict[str, Optional[str]]:
        """
        Upload multiple files to Cloudinary in bulk
        
        Args:
            file_paths: List of local file paths to upload
            folder: Optional folder path in Cloudinary
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            Dict[str, Optional[str]]: Dictionary mapping file paths to their download URLs
                                      (None if upload failed for that file)
        """
        results = {}
        total_files = len(file_paths)
        successful = 0
        failed = 0
        
        logger.info(f"Starting bulk upload of {total_files} files...")
        
        for idx, file_path in enumerate(file_paths, 1):
            logger.info(f"\n[{idx}/{total_files}] Uploading: {os.path.basename(file_path)}")
            
            # Generate public_id from filename
            filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
            public_id = f"{filename_without_ext}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            url = StorageService.upload_file(
                file_path=file_path,
                folder=folder,
                public_id=public_id,
                resource_type=resource_type
            )
            
            if url:
                results[file_path] = url
                successful += 1
                logger.info(f"✓ Success: {os.path.basename(file_path)}")
            else:
                results[file_path] = None
                failed += 1
                logger.error(f"✗ Failed: {os.path.basename(file_path)}")
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Bulk upload complete: {successful} successful, {failed} failed out of {total_files} total")
        logger.info(f"{'=' * 60}")
        
        return results

    @staticmethod
    def get_download_url(public_id: str, folder: str = None, resource_type: str = "raw") -> str:
        """
        Get a download URL for a file in Cloudinary
        
        Args:
            public_id: Public ID of the file in Cloudinary
            folder: Optional folder path if file is in a folder
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            str: Download URL, or None if file not found
        """
        try:
            # Construct the full public_id with folder if provided
            full_public_id = f"{folder}/{public_id}" if folder else public_id
            
            # Get resource info
            resource = cloudinary.api.resource(full_public_id, resource_type=resource_type)
            
            if resource:
                url = resource.get('secure_url') or resource.get('url')
                logger.info(f"Retrieved download URL for: {full_public_id}")
                return url
            else:
                logger.error(f"File not found in Cloudinary: {full_public_id}")
                return None
                
        except cloudinary.exceptions.NotFound:
            logger.error(f"File not found in Cloudinary: {public_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting download URL from Cloudinary: {e}")
            logger.exception("Full error details:")
            return None

    @staticmethod
    def delete_file(public_id: str, folder: str = None, resource_type: str = "raw") -> bool:
        """
        Delete a file from Cloudinary
        
        Args:
            public_id: Public ID of the file in Cloudinary
            folder: Optional folder path if file is in a folder
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            # Construct the full public_id with folder if provided
            full_public_id = f"{folder}/{public_id}" if folder else public_id
            
            result = cloudinary.uploader.destroy(full_public_id, resource_type=resource_type)
            
            if result.get('result') == 'ok':
                logger.info(f"File deleted successfully from Cloudinary: {full_public_id}")
                return True
            else:
                logger.warning(f"File deletion result: {result.get('result')}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting file from Cloudinary: {e}")
            logger.exception("Full error details:")
            return False

    @staticmethod
    def file_exists(public_id: str, folder: str = None, resource_type: str = "raw") -> bool:
        """
        Check if a file exists in Cloudinary
        
        Args:
            public_id: Public ID of the file in Cloudinary
            folder: Optional folder path if file is in a folder
            resource_type: Type of resource - 'raw' for PDFs/docs, 'image' for images
        
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            # Construct the full public_id with folder if provided
            full_public_id = f"{folder}/{public_id}" if folder else public_id
            
            resource = cloudinary.api.resource(full_public_id, resource_type=resource_type)
            return resource is not None
            
        except cloudinary.exceptions.NotFound:
            return False
        except Exception as e:
            logger.error(f"Error checking file existence in Cloudinary: {e}")
            return False
