from pathlib import Path

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
