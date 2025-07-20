FileVault CLI
A command-line file management system with user authentication, folder support, file visibility controls, and background thumbnail generation.
Features

User authentication (register, login, logout, whoami)
Folder creation and hierarchy (mkdir)
File upload with folder association (upload)
List files and folders (ls)
View file metadata (read)
Delete files and folders (delete)
Set file/folder visibility (publish, unpublish)
Move files/folders to different folders (mv)
Background thumbnail generation for images using Celery
Repository pattern for database access
MongoDB for data storage
Redis for session management and Celery backend

Requirements

Python 3.8+
MongoDB
Redis
Python packages: pymongo, bcrypt, redis, celery, Pillow

Installation

Clone the repository:git clone <repository-url>
cd project


Install dependencies:pip install pymongo bcrypt redis celery Pillow


Start MongoDB and Redis servers:mongod
redis-server



Usage
Install the CLI using:
pip install -e .

Start the Celery worker:celery -A vault.vault celery

Then You can use vault anywhere in your computer through your CLI

Available commands:

vault register - Register a new user
vault login - Login to your account
vault logout - Logout from your account
vault whoami - Show current logged in user
vault mkdir <folder_name> [parent_id] - Create a new folder
vault upload <filepath> [folder_name] - Upload a file to your vault
vault ls [parent_id] [--public] - List files and folders
vault read <file_id> - Display metadata for a file or folder
vault delete <file_id> - Delete a file or folder
vault publish <file_id> - Make a file or folder public
vault unpublish <file_id> - Make a file or folder private
vault mv <file_id> <parent_id> - Move a file or folder to another folder
vault help - Show help message

Example
vault register
vault login
vault mkdir Documents
vault upload photo.jpg Documents
vault ls Documents
vault publish <file_id>
vault ls --public
vault mv <file_id> <parent_id>
vault logout

Project Structure
FILEVAULT/
├─── vault/
│    │
│    ├── cli/
│    │   ├── commands/
│    │   │   ├── base.py
│    │   │   ├── register.py
│    │   │   ├── login.py
│    │   │   ├── logout.py
│    │   │   ├── whoami.py
│    │   │   ├── mkdir.py
│    │   │   ├── upload.py
│    │   │   ├── list.py
│    │   │   ├── read.py
│    │   │   ├── delete.py
│    │   │   ├── publish.py
│    │   │   ├── unpublish.py
│    │   │   ├── mv.py
│    │   │   ├── help.py
│    │   │   ├── celery.py
│    │   ├── __init__.py
│    │   ├── command_router.py
│    ├── services/
│    │   ├── auth_service.py
│    │   ├── file_service.py
│    │   ├── __init__.py
│    ├── repositories/
│    │   ├── user_repository.py
│    │   ├── file_repository.py
│    │   ├── session_repository.py
│    │   ├── __init__.py
│    ├── workers/
│    │   ├── thumbnail_worker.py
│    │   ├── __init__.py
│    ├── storage/
│    │   ├── uploads/
│    │   ├── thumbnails/
│    ├── utils/
│    │   ├── helpers.py
│    │   ├── __init__.py
│    ├── config.py
│    ├── main.py - `Entry file`
│    ├── __init__.py
├── database/
├── .env
├── README.md
├── setup.py

