import random

def simulate_payment() -> bool:
    """
    Simulates a payment process with a random outcome.

    Returns:
        bool: True for a successful payment, False for a failed one.
    """
    # Simulate a 90% success rate
    return random.random() < 0.9
