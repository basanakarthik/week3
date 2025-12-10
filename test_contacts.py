# Simple test runner for contacts manager load/save and validation
import json, os, re
from contacts_manager import validate_phone, validate_email, load_contacts, save_contacts

def test_phone():
    cases = ["+1 (234) 567-8900", "9876543210", "12345", "abcd"]
    results = [validate_phone(c)[0] for c in cases]
    print("test_phone:", results)  # Expect [True, True, False, False]

def test_email():
    cases = ["john@example.com", "invalid@", "", None]
    results = [validate_email(c) for c in cases]
    print("test_email:", results)  # Expect [True, False, True, True]

def test_io():
    data = {"Test": {"phone":"1234567890"}}
    save_contacts(data, path="test_contacts_io.json")
    loaded = load_contacts(path="test_contacts_io.json")
    print("test_io:", "OK" if loaded.get("Test") else "FAIL")
    os.remove("test_contacts_io.json")

if __name__ == '__main__':
    test_phone()
    test_email()
    test_io()