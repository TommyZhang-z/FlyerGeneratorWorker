import os
from dotenv import load_dotenv

load_dotenv(".env.local")
import base64
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Retrieve the Base64-encoded service account credentials from the environment
ENCODED_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
TARGET_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

if not ENCODED_CREDENTIALS:
    raise ValueError("Environment variable GOOGLE_CREDENTIALS is not set.")

# Decode the Base64 string to JSON
DECODED_CREDENTIALS = base64.b64decode(ENCODED_CREDENTIALS).decode("utf-8")
SERVICE_ACCOUNT_INFO = json.loads(DECODED_CREDENTIALS)

# Define the required scope for accessing Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Authenticate using the decoded service account info
CREDENTIALS = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=CREDENTIALS)


def search_file_by_name(file_name, parent_folder_id=None):
    """Search for a file by name in the specified folder."""
    query = f"name='{file_name}'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    results = (
        drive_service.files()
        .list(q=query, spaces="drive", fields="files(id)")
        .execute()
    )
    files = results.get("files", [])
    return files[0].get("id") if files else None


def upload_or_replace_file(file_name, file_path, mime_type, parent_folder_id=None):
    """Upload or replace a file with the same name in the specified folder."""
    existing_file_id = search_file_by_name(file_name, parent_folder_id)

    file_metadata = {"name": file_name}
    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)

    if existing_file_id:
        # Update the existing file
        updated_file = (
            drive_service.files()
            .update(
                fileId=existing_file_id,
                media_body=media,
            )
            .execute()
        )
        print(f"File replaced successfully, File ID: {updated_file.get('id')}")
    else:
        # Upload a new file
        uploaded_file = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f"File uploaded successfully, File ID: {uploaded_file.get('id')}")


# Example usage
def main():

    upload_or_replace_file(
        "example3.txt",
        "requirements.txt",
        "text/plain",
        parent_folder_id=TARGET_FOLDER_ID,
    )


if __name__ == "__main__":
    main()
