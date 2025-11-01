def send_email(api_key, to_email, message):
    print(f"[Mock Email] To: {to_email} | Message: {message[:80]}...")

def send_push(user_key, token, message):
    print(f"[Mock Push] {message[:80]}...")
