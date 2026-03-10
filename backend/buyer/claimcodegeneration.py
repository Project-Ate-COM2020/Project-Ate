import random

def generate_claim_code(length=8):
    """Generates a random alphanumeric claim code of the specified length."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    claim_code = ''.join(random.choice(characters) for _ in range(length))
    return claim_code