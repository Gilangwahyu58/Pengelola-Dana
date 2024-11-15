# storage.py
import pyrebase
from datetime import datetime
import os
from config import get_firebase_config

class StorageManager:
    config = get_firebase_config()
    try:
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        print("Firebase Storage initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase Storage: {e}")
        raise e

    @staticmethod
    def upload_profile_image(file_path, folder="fotoProfil"):
        """
        Upload profile image to Firebase Storage
        """
        try:
            print(f"Attempting to upload profile image: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return {
                    "status": "error",
                    "message": "File not found",
                    "path": None,
                    "url": None
                }

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file_path)[1]
            firebase_path = f"{folder}/{timestamp}{file_extension}"
            print(f"Generated Firebase path: {firebase_path}")

            # Upload file
            print("Starting upload...")
            StorageManager.storage.child(firebase_path).put(file_path)
            print("Upload completed")

            # Get URL
            print("Getting download URL...")
            image_url = StorageManager.storage.child(firebase_path).get_url(None)
            print(f"Got URL: {image_url}")

            return {
                "status": "success",
                "url": image_url,
                "path": firebase_path
            }

        except Exception as e:
            print(f"Error in upload_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }

    @staticmethod
    def delete_profile_image(firebase_path):
        """
        Delete profile image from Firebase Storage
        """
        try:
            print(f"Attempting to delete profile image: {firebase_path}")
            
            if not firebase_path:
                print("No path provided")
                return {
                    "status": "error",
                    "message": "No image path provided"
                }

            StorageManager.storage.delete(firebase_path)
            print("Delete successful")
            
            return {
                "status": "success",
                "message": "Profile image deleted successfully"
            }
        except Exception as e:
            print(f"Error in delete_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def update_profile_image(old_firebase_path, new_file_path, folder="fotoProfil"):
        """
        Update profile image in Firebase Storage
        """
        try:
            print(f"Attempting to update profile image. Old path: {old_firebase_path}, New file: {new_file_path}")
            
            # Delete old image if exists
            if old_firebase_path:
                print("Deleting old profile image...")
                StorageManager.delete_profile_image(old_firebase_path)
            
            # Upload new image
            print("Uploading new profile image...")
            return StorageManager.upload_profile_image(new_file_path, folder)
            
        except Exception as e:
            print(f"Error in update_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }


class StorageManagerKemajuan:
    config = get_firebase_config()
    try:
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        print("Firebase Storage initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase Storage: {e}")
        raise e

    @staticmethod
    def upload_profile_image(file_path, folder="fotoKemajuan"):
        """
        Upload profile image to Firebase Storage
        """
        try:
            print(f"Attempting to upload profile image: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return {
                    "status": "error",
                    "message": "File not found",
                    "path": None,
                    "url": None
                }

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file_path)[1]
            firebase_path = f"{folder}/{timestamp}{file_extension}"
            print(f"Generated Firebase path: {firebase_path}")

            # Upload file
            print("Starting upload...")
            StorageManager.storage.child(firebase_path).put(file_path)
            print("Upload completed")

            # Get URL
            print("Getting download URL...")
            image_url = StorageManager.storage.child(firebase_path).get_url(None)
            print(f"Got URL: {image_url}")

            return {
                "status": "success",
                "url": image_url,
                "path": firebase_path
            }

        except Exception as e:
            print(f"Error in upload_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }

    @staticmethod
    def delete_profile_image(firebase_path):
        """
        Delete profile image from Firebase Storage
        """
        try:
            print(f"Attempting to delete profile image: {firebase_path}")
            
            if not firebase_path:
                print("No path provided")
                return {
                    "status": "error",
                    "message": "No image path provided"
                }

            StorageManager.storage.delete(firebase_path)
            print("Delete successful")
            
            return {
                "status": "success",
                "message": "Profile image deleted successfully"
            }
        except Exception as e:
            print(f"Error in delete_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def update_profile_image(old_firebase_path, new_file_path, folder="fotoProfil"):
        """
        Update profile image in Firebase Storage
        """
        try:
            print(f"Attempting to update profile image. Old path: {old_firebase_path}, New file: {new_file_path}")
            
            # Delete old image if exists
            if old_firebase_path:
                print("Deleting old profile image...")
                StorageManager.delete_profile_image(old_firebase_path)
            
            # Upload new image
            print("Uploading new profile image...")
            return StorageManager.upload_profile_image(new_file_path, folder)
            
        except Exception as e:
            print(f"Error in update_profile_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }