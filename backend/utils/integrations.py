import smtplib
import requests
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class IntegrationService:
    # Test webhook URLs for demonstration
    TEST_WEBHOOKS = {
        "slack": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
        "google_workspace": "https://chat.googleapis.com/v1/spaces/AAAA_SAMPLE_SPACE/messages?key=SAMPLE_KEY",
        "discord": "https://discord.com/api/webhooks/000000000000000000/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

    @staticmethod
    async def send_slack_webhook(webhook_url: str, message: str, channel: Optional[str] = None, username: str = "BurnStop") -> bool:
        """Send message to Slack via webhook"""
        try:
            # Enhanced Slack message with rich formatting
            payload = {
                "text": message,
                "username": username,
                "icon_emoji": ":fire:",
                "attachments": [
                    {
                        "color": "#ff6b6b",
                        "title": "🔥 BurnStop Alert",
                        "text": message,
                        "footer": "BurnStop Cost Monitor",
                        "ts": int(time.time())
                    }
                ]
            }
            
            if channel:
                payload["channel"] = channel
            
            # For test webhook, use a mock response
            if webhook_url == IntegrationService.TEST_WEBHOOKS["slack"]:
                logger.info(f"TEST MODE: Would send Slack message: {message}")
                return True
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack webhook: {e}")
            return False

    @staticmethod
    async def send_google_workspace_webhook(webhook_url: str, message: str, space_name: Optional[str] = None) -> bool:
        """Send message to Google Workspace via webhook"""
        try:
            # Enhanced Google Chat message with cards
            payload = {
                "cards": [{
                    "header": {
                        "title": "🔥 BurnStop Alert",
                        "subtitle": space_name if space_name else "Cost Management Alert",
                        "imageUrl": "https://raw.githubusercontent.com/yourusername/burn-stop/main/assets/logo.png"
                    },
                    "sections": [{
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": f"<b>Alert:</b> {message}"
                                }
                            }
                        ]
                    }]
                }]
            }
            
            # For test webhook, use a mock response
            if webhook_url == IntegrationService.TEST_WEBHOOKS["google_workspace"]:
                logger.info(f"TEST MODE: Would send Google Workspace message: {message}")
                return True
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Google Workspace webhook: {e}")
            return False

    @staticmethod
    async def send_discord_webhook(webhook_url: str, message: str, username: str = "BurnStop") -> bool:
        """Send message to Discord via webhook"""
        try:
            payload = {
                "content": message,
                "username": username,
                "avatar_url": "https://raw.githubusercontent.com/yourusername/burn-stop/main/assets/logo.png",
                "embeds": [
                    {
                        "title": "🔥 BurnStop Alert",
                        "description": message,
                        "color": 16733525,  # #ff6b6b in decimal
                        "footer": {
                            "text": "BurnStop Cost Monitor"
                        }
                    }
                ]
            }
            
            # For test webhook, use a mock response
            if webhook_url == IntegrationService.TEST_WEBHOOKS["discord"]:
                logger.info(f"TEST MODE: Would send Discord message: {message}")
                return True
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord webhook: {e}")
            return False

    @staticmethod
    async def send_email_alert(
        smtp_server: str,
        smtp_port: int,
        email: str,
        app_password: str,
        to_email: str,
        subject: str,
        message: str,
        from_name: str = "BurnStop Alerts"
    ) -> bool:
        """Send email alert using SMTP"""
        try:
            # For test mode with specific test email
            if email == "test@burnstop.dev":
                logger.info(f"TEST MODE: Would send email to {to_email}: {subject} - {message}")
                return True

            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{from_name} <{email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Enhanced HTML email template
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
        .header {{ background-color: #ff6b6b; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 30px; }}
        .footer {{ background-color: #f4f4f4; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
        .alert-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        .button {{ background-color: #ff6b6b; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 15px 0; }}
        .stats {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 BurnStop Alert</h1>
            <p>Cost Management System</p>
        </div>
        <div class="content">
            <div class="alert-box">
                <h3>Alert Details</h3>
                <p>{message}</p>
            </div>
            
            <div class="stats">
                <h4>Alert Information</h4>
                <p>This alert was generated by your BurnStop cost monitoring system.</p>
            </div>
            
            <p><strong>Timestamp:</strong> {subject}</p>
            <p><strong>System:</strong> BurnStop Cost Monitor</p>
        </div>
        <div class="footer">
            <p>BurnStop - Stop burning money on cloud services!</p>
            <p>This is an automated message from your cost monitoring system.</p>
        </div>
    </div>
</body>
</html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Create SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable security
            server.login(email, app_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(email, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    @staticmethod
    async def send_teams_webhook(webhook_url: str, message: str) -> bool:
        """Send message to Microsoft Teams via webhook"""
        try:
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "ff6b6b",
                "summary": "BurnStop Alert",
                "sections": [{
                    "activityTitle": "🔥 BurnStop Alert",
                    "activitySubtitle": "Cost Management System",
                    "activityImage": "https://raw.githubusercontent.com/yourusername/burn-stop/main/assets/logo.png",
                    "facts": [{
                        "name": "Alert:",
                        "value": message
                    }, {
                        "name": "System:",
                        "value": "BurnStop Cost Monitor"
                    }],
                    "markdown": True
                }]
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Teams webhook: {e}")
            return False

    @staticmethod
    async def send_alert_to_integration(integration_type: str, config: Dict[str, Any], message: str, subject: str = None) -> bool:
        """Send alert through the specified integration"""
        try:
            if integration_type == "slack":
                return await IntegrationService.send_slack_webhook(
                    webhook_url=config["webhook_url"],
                    message=message,
                    channel=config.get("channel"),
                    username=config.get("username", "BurnStop")
                )
            
            elif integration_type == "google_workspace":
                return await IntegrationService.send_google_workspace_webhook(
                    webhook_url=config["webhook_url"],
                    message=message,
                    space_name=config.get("space_name")
                )
            
            elif integration_type == "discord":
                return await IntegrationService.send_discord_webhook(
                    webhook_url=config["webhook_url"],
                    message=message,
                    username=config.get("username", "BurnStop")
                )
            
            elif integration_type == "teams":
                return await IntegrationService.send_teams_webhook(
                    webhook_url=config["webhook_url"],
                    message=message
                )
            
            elif integration_type == "email":
                # For email alerts, we need a recipient email
                # This would typically come from organization members
                return await IntegrationService.send_email_alert(
                    smtp_server=config["smtp_server"],
                    smtp_port=config["smtp_port"],
                    email=config["email"],
                    app_password=config["app_password"],
                    to_email=config.get("to_email", config["email"]),  # Default to sender if no recipient
                    subject=subject or "🔥 BurnStop Alert",
                    message=message,
                    from_name=config.get("from_name", "BurnStop Alerts")
                )
            
            else:
                logger.error(f"Unknown integration type: {integration_type}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send alert through {integration_type}: {e}")
            return False

    @staticmethod
    def get_test_integration_config(integration_type: str) -> Dict[str, Any]:
        """Get test configuration for an integration type"""
        test_configs = {
            "slack": {
                "webhook_url": IntegrationService.TEST_WEBHOOKS["slack"],
                "channel": "#test-alerts",
                "username": "BurnStop-Test"
            },
            "google_workspace": {
                "webhook_url": IntegrationService.TEST_WEBHOOKS["google_workspace"],
                "space_name": "BurnStop Test Space"
            },
            "discord": {
                "webhook_url": IntegrationService.TEST_WEBHOOKS["discord"],
                "username": "BurnStop-Test"
            },
            "teams": {
                "webhook_url": "https://outlook.office.com/webhook/test-webhook-url"
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email": "test@burnstop.dev",
                "app_password": "test-app-password",
                "to_email": "admin@burnstop.dev",
                "from_name": "BurnStop Test Alerts"
            }
        }
        
        return test_configs.get(integration_type, {}) 