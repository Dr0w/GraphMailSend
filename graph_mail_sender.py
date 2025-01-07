import requests

# Azure app credentials
tenant_id = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Email configuration
sender_email = "sender@yourdomain.com"  # Must be a user in the restricted group
recipient_email = "recipient@otherdomain.com"  # Test recipient
subject = "Test Email from Azure App"
body = "This is a test email sent using Microsoft Graph API."

# Authentication: Get the access token
def get_access_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()  # Raise an error for bad status
    return response.json()["access_token"]

# Send the email
def send_email(access_token):
    url = "https://graph.microsoft.com/v1.0/users/{}/sendMail".format(sender_email)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    email_message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": recipient_email}}
            ]
        }
    }
    response = requests.post(url, headers=headers, json=email_message)
    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    try:
        token = get_access_token()
        send_email(token)
    except Exception as e:
        print(f"Error: {e}")