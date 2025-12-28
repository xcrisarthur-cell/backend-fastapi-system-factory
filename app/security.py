"""
Security utilities for password hashing
"""
import bcrypt

# Bcrypt has a maximum password length of 72 bytes
BCRYPT_MAX_PASSWORD_LENGTH = 72


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Convert to bytes to check length accurately
    password_bytes = password.encode('utf-8')
    
    # Truncate if password is longer than 72 bytes (bcrypt limit)
    if len(password_bytes) > BCRYPT_MAX_PASSWORD_LENGTH:
        password_bytes = password_bytes[:BCRYPT_MAX_PASSWORD_LENGTH]
        print(f"[WARNING] Password truncated to {BCRYPT_MAX_PASSWORD_LENGTH} bytes (bcrypt limit)")
    
    # Generate salt and hash password using bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    # Convert to bytes
    plain_bytes = plain_password.encode('utf-8')
    if len(plain_bytes) > BCRYPT_MAX_PASSWORD_LENGTH:
        plain_bytes = plain_bytes[:BCRYPT_MAX_PASSWORD_LENGTH]
    
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

