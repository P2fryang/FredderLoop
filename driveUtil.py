# drive documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html

# constants
WRITER_PERMISSION = "writer"


def share_document(drive_service, file_id: str, emails: list) -> None:
    if type(emails) != list:
        raise TypeError(f"incorrect emails type: {type(emails)}")
    for email in emails:
        print(f"adding: {email}")
        drive_service.permissions().create(
            fileId=file_id,
            body={"type": "user", "emailAddress": email, "role": WRITER_PERMISSION},
        ).execute()
        print(f"added writer role for: {email}")


# https://developers.google.com/drive/api/guides/manage-sharing#python
def _transfer_ownership(
    drive_service, file_id: str, permission_id: str, email: str
) -> None:
    # https://issuetracker.google.com/issues/228791253
    print(
        "Currently Drive does not support changing the ownership for items which are owned by gmail.com accounts; it's supported for Workspace accounts."
    )


def get_permissions(drive_service, file_id: str) -> dict:
    permissions = (
        drive_service.permissions().list(fileId=file_id).execute()["permissions"]
    )
    print(permissions)
    return permissions


def delete_permission(drive_service, file_id: str, permission_id: str) -> None:
    print(f"deleting permission {permission_id} for file {file_id}")
    drive_service.permissions().delete(
        fileId=file_id, permissionId=permission_id
    ).execute()


def trash_document(drive_service, file_id: str) -> None:
    print(f"Trashing document: {file_id}")
    body = {"trashed": True}
    drive_service.files().update(fileId=file_id, body=body).execute()


def untrash_file(drive_service, file_id: str) -> None:
    print(f"Attempting to untrash file: {file_id}")
    body = {"trashed": False}
    drive_service.files().update(fileId=file_id, body=body).execute()


def add_anyone_write(drive_service, file_id: str) -> None:
    print(f"Adding anyoneWithLink can write permission: {file_id}")
    body = {
        "type": "anyone",
        "role": "writer",
        "allowFileDiscovery": False,
    }
    drive_service.permissions().create(fileId=file_id, body=body).execute()


def add_anyone_reader(drive_service, file_id: str) -> None:
    print(f"Adding anyone can ready: {file_id}")
    body = {"type": "anyone", "role": "reader"}
    drive_service.permissions.create(fildId=file_id, body=body).execute()


def clear_nonowner_permissions(drive_service, file_id: str) -> None:
    print(f"Clear all permissions besides owner for {file_id}")
    result = get_permissions(drive_service=drive_service, file_id=file_id)
    for permission in result["permissions"]:
        if permission["role"] != "owner":
            delete_permission(
                drive_service=drive_service,
                file_id=file_id,
                permission_id=permission["id"],
            )


def list_files(drive_service, query: str = None) -> dict:
    return drive_service.files().list(q=query).execute()

def list_files_in_folder(drive_service, folder_id: str) -> dict:
    query = f"parents in '{folder_id}'"
    return drive_service.files().list(q=query).execute()


def list_folders(drive_service) -> dict:
    query = "mimeType='application/vnd.google-apps.folder'"
    return drive_service.files().list(q=query).execute()


def list_drives(drive_service) -> dict:
    return drive_service.drives().list().execute()


def list_file_labels(drive_service, file_id: str) -> dict:
    return drive_service.files().listLabels(fileId=file_id).execute()


def get_file(drive_service, file_id: str) -> dict:
    return drive_service.files().get(fileId=file_id, fields="*").execute()
