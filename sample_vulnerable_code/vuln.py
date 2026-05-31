# Sample vulnerable file for Mythosguard demo
import os

def compute(user_input):
    # insecure: uses eval on user input
    return eval(user_input)

password = "hunter2"  # hardcoded password (intentional vuln)
