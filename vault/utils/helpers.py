from pathlib import Path
import bcrypt
import uuid

def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    if size_bytes == 0:
        return "0 B"

    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"
    
def validate_file_type(filepath: str) -> bool:
    """Validate file type (reject potentially dangerous files)"""
    dangerous_extensions = ['.exe', '.bat', '.cmd', '.scr', '.com', '.pif']
    file_ext = Path(filepath).suffix.lower()
    return file_ext not in dangerous_extensions

def validate_email(email: str) -> bool:
    """Basic email varification"""
    return '@' in email and '.' in email.split('@')[1]

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_session_token() -> str:
    """Generate a secure session token"""
    return str(uuid.uuid4())
