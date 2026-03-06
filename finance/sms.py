try:
    import africastalking

    username = "YOUR_USERNAME"
    api_key = "YOUR_API_KEY"

    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    def send_fee_reminder(phone, student_name, balance):
        message = f"Reminder: {student_name} has an outstanding fee balance of {balance}. Please pay promptly."
        sms.send(message, [phone])
except Exception:
    def send_fee_reminder(phone, student_name, balance):
        # africastalking not available or failed to initialize — no-op fallback
        return None
