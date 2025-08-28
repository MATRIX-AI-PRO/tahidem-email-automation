import streamlit as st
import smtplib
import pandas as pd
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import io
import csv
import hashlib

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="Tahidem Professional Email Automation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔐 GÜVENLİK AYARLARI
ADMIN_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # "password"
MASTER_PASSWORD_HASH = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"  # "secret123"

# Email hesapları (şifrelenmiş olarak saklanacak)
EMAIL_ACCOUNTS = [
    {'email': 'partnerships@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'partnership', 'sent_today': 0},
    {'email': 'business@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'partnership', 'sent_today': 0},
    {'email': 'collaborations@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'partnership', 'sent_today': 0},
    {'email': 'deals@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'partnership', 'sent_today': 0},
    {'email': 'marketing@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'partnership', 'sent_today': 0},
    {'email': 'partnership@tahidem.com', 'password': 'GM8+h!M>An5', 'type': 'partnership', 'sent_today': 0},
    {'email': 'amazonpartnership@tahidem.com', 'password': '5V7SOWq:V&zQ', 'type': 'partnership', 'sent_today': 0},
    {'email': 'partnershipamazon@tahidem.com', 'password': 'u&17]ukQ', 'type': 'partnership', 'sent_today': 0},
    {'email': 'exclusivebrand@tahidem.com', 'password': '5M?$Kz^m', 'type': 'partnership', 'sent_today': 0},
    {'email': 'outreach@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'cold', 'sent_today': 0},
    {'email': 'team@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'cold', 'sent_today': 0},
    {'email': 'hello@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'cold', 'sent_today': 0},
    {'email': 'connect@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'cold', 'sent_today': 0},
    {'email': 'growth@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'cold', 'sent_today': 0}
]

# SMTP ayarları
SMTP_SERVER = 'smtp.hostinger.com'
SMTP_PORT = 465

# Varsayılan Professional English Templates
DEFAULT_TEMPLATES = {
    "partnership": {
        "subject": "Strategic Partnership Opportunity - {company}",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 650px; margin: 0 auto; padding: 30px; background: #ffffff;">
            
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; font-size: 24px; margin: 0;">TAHIDEM</h1>
                <p style="color: #7f8c8d; font-size: 14px; margin: 5px 0;">Strategic Business Development</p>
            </div>
            
            <h2 style="color: #34495e; font-size: 20px;">Dear {name},</h2>
            
            <p style="font-size: 16px; margin-bottom: 20px;">
            I hope this message finds you well. I'm reaching out from Tahidem's partnerships team regarding a strategic collaboration opportunity with <strong>{company}</strong>.
            </p>
            
            <p style="font-size: 16px; margin-bottom: 25px;">
            We've been following your company's impressive growth and market presence, and we believe there's significant potential for a mutually beneficial partnership.
            </p>
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; margin: 25px 0; color: white;">
                <h3 style="margin-top: 0; font-size: 18px;">🎯 Partnership Benefits:</h3>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li style="margin-bottom: 8px;">📈 <strong>Market Expansion:</strong> Access to new customer segments</li>
                    <li style="margin-bottom: 8px;">💰 <strong>Revenue Growth:</strong> Shared revenue models and cross-selling</li>
                    <li style="margin-bottom: 8px;">🚀 <strong>Innovation:</strong> Joint product development opportunities</li>
                    <li style="margin-bottom: 8px;">⚡ <strong>Efficiency:</strong> Streamlined operations and cost optimization</li>
                </ul>
            </div>
            
            <p style="font-size: 16px; margin-bottom: 20px;">
            I'd love to schedule a brief 15-minute call to discuss how we can create value together. Would you be available for a conversation this week?
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="mailto:partnerships@tahidem.com" style="background: #e74c3c; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Schedule a Call</a>
            </div>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                <p style="margin-bottom: 5px;"><strong>Best regards,</strong></p>
                <p style="margin-bottom: 5px; font-weight: bold; color: #2c3e50;">Strategic Partnerships Team</p>
                <p style="margin-bottom: 5px; color: #e74c3c; font-weight: bold;">TAHIDEM</p>
                <p style="font-size: 14px; color: #7f8c8d;">partnerships@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    "cold": {
        "subject": "Quick Question About {company}'s Growth Strategy",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 650px; margin: 0 auto; padding: 30px; background: #ffffff;">
            
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; font-size: 24px; margin: 0;">TAHIDEM</h1>
                <p style="color: #7f8c8d; font-size: 14px; margin: 5px 0;">Digital Growth Solutions</p>
            </div>
            
            <h2 style="color: #34495e; font-size: 20px;">Hi {name},</h2>
            
            <p style="font-size: 16px; margin-bottom: 20px;">
            I came across your profile on LinkedIn and was impressed by your role at <strong>{company}</strong>. 
            </p>
            
            <p style="font-size: 16px; margin-bottom: 25px;">
            I'm reaching out because we've been helping companies in your industry achieve remarkable growth through our innovative digital solutions.
            </p>
            
            <div style="background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%); padding: 25px; border-radius: 10px; margin: 25px 0; color: white;">
                <h3 style="margin-top: 0; font-size: 18px;">🚀 What We Deliver:</h3>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li style="margin-bottom: 8px;">⚡ <strong>40% Faster</strong> business processes</li>
                    <li style="margin-bottom: 8px;">💡 <strong>AI-Powered</strong> automation solutions</li>
                    <li style="margin-bottom: 8px;">📊 <strong>Data-Driven</strong> growth strategies</li>
                    <li style="margin-bottom: 8px;">🎯 <strong>ROI-Focused</strong> implementations</li>
                </ul>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-left: 4px solid #e74c3c; margin: 25px 0;">
                <p style="font-size: 17px; font-weight: bold; color: #2c3e50; margin: 0;">
                Quick question: What's your biggest challenge in scaling {company} right now?
                </p>
            </div>
            
            <p style="font-size: 16px; margin-bottom: 20px;">
            I'd love to share a 3-minute case study of how we helped a similar company increase their efficiency by 40%. 
            </p>
            
            <p style="font-size: 16px; margin-bottom: 20px;">
            Worth a quick chat? ☕
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="mailto:growth@tahidem.com" style="background: #27ae60; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Let's Connect</a>
            </div>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                <p style="margin-bottom: 5px;"><strong>Best,</strong></p>
                <p style="margin-bottom: 5px; font-weight: bold; color: #2c3e50;">Growth Team</p>
                <p style="margin-bottom: 5px; color: #e74c3c; font-weight: bold;">TAHIDEM</p>
                <p style="font-size: 14px; color: #7f8c8d;">growth@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></body></html>
        """
    }
}

def hash_password(password):
    """Şifreyi hash'le"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password():
    """Şifre kontrolü"""
    def password_entered():
        """Girilen şifreyi kontrol et"""
        entered_password = st.session_state["password"]
        entered_hash = hash_password(entered_password)
        
        if entered_hash == ADMIN_PASSWORD_HASH:
            st.session_state["password_correct"] = True
            st.session_state["user_role"] = "admin"
            del st.session_state["password"]  # Şifreyi bellekten sil
        elif entered_hash == MASTER_PASSWORD_HASH:
            st.session_state["password_correct"] = True
            st.session_state["user_role"] = "master"
            del st.session_state["password"]  # Şifreyi bellekten sil
        else:
            st.session_state["password_correct"] = False

    # İlk giriş kontrolü
    if "password_correct" not in st.session_state:
        # Login sayfası
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
            <div style="text-align: center; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); background: white; max-width: 400px;">
                <h1 style="color: #2c3e50; margin-bottom: 10px;">🔐 TAHIDEM</h1>
                <h3 style="color: #7f8c8d; margin-bottom: 30px;">Email Automation System</h3>
                <p style="color: #34495e; margin-bottom: 20px;">Enter your access password to continue</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "🔑 Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter your password..."
            )
            
            if st.button("🚀 LOGIN", type="primary", use_container_width=True):
                password_entered()
        
        return False
    
    # Yanlış şifre
    elif not st.session_state["password_correct"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.error("❌ Incorrect password! Please try again.")
            st.text_input(
                "🔑 Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter your password..."
            )
            
            if st.button("🚀 LOGIN", type="primary", use_container_width=True):
                password_entered()
        
        return False
    
    # Doğru şifre - Ana uygulamaya geç
    else:
        return True

class EmailAutomation:
    def __init__(self):
        if 'email_stats' not in st.session_state:
            st.session_state.email_stats = {
                'total_sent': 0,
                'successful': 0,
                'failed': 0,
                'daily_counts': {acc['email']: 0 for acc in EMAIL_ACCOUNTS}
            }
        
        if 'custom_templates' not in st.session_state:
            st.session_state.custom_templates = DEFAULT_TEMPLATES.copy()
    
    def send_single_email(self, sender_account, recipient, subject, content):
        try:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            server.login(sender_account['email'], sender_account['password'])
            
            msg = MIMEMultipart()
            msg['From'] = f"Tahidem <{sender_account['email']}>"
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'html'))
            
            server.send_message(msg)
            server.quit()
            
            # Stats güncelle
            st.session_state.email_stats['successful'] += 1
            st.session_state.email_stats['daily_counts'][sender_account['email']] += 1
            sender_account['sent_today'] += 1
            
            return True, "Success"
            
        except Exception as e:
            st.session_state.email_stats['failed'] += 1
            return False, str(e)
    
    def get_available_account(self, campaign_type):
        """Günlük limite ulaşmayan hesap bul"""
        suitable_accounts = [acc for acc in EMAIL_ACCOUNTS 
                           if acc['type'] == campaign_type and acc['sent_today'] < 100]
        
        if suitable_accounts:
            return min(suitable_accounts, key=lambda x: x['sent_today'])
        return None
    
    def format_template(self, template_type, name, company, custom_subject=None, custom_content=None):
        """Template'i format et"""
        if custom_subject and custom_content:
            # Custom template kullan
            subject = custom_subject.format(name=name, company=company)
            content = custom_content.format(name=name, company=company)
        else:
            # Varsayılan template kullan
            template = st.session_state.custom_templates[template_type]
            subject = template['subject'].format(name=name, company=company)
            content = template['content'].format(name=name, company=company)
        
        return subject, content

# Ana uygulama
def main_app():
    automation = EmailAutomation()
    
    # Header with user info
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🚀 Tahidem Professional Email Automation")
        st.markdown("**Advanced Email Campaign Management System**")
    
    with col2:
        user_role = st.session_state.get("user_role", "admin")
        role_color = "🔴" if user_role == "master" else "🟢"
        st.info(f"{role_color} **{user_role.upper()}** ACCESS")
    
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
    
    st.markdown("---")
    
    # Sidebar - Stats
    with st.sidebar:
        st.header("📊 Campaign Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Successful", st.session_state.email_stats['successful'])
        with col2:
            st.metric("❌ Failed", st.session_state.email_stats['failed'])
        
        total_sent = st.session_state.email_stats['successful'] + st.session_state.email_stats['failed']
        success_rate = (st.session_state.email_stats['successful'] / max(total_sent, 1)) * 100
        
        st.metric("📧 Total Sent", total_sent)
        st.metric("📈 Success Rate", f"{success_rate:.1f}%")
        
        st.markdown("### 📧 Account Status")
        for acc in EMAIL_ACCOUNTS:
            remaining = 100 - st.session_state.email_stats['daily_counts'][acc['email']]
            account_name = acc['email'].split('@')[0]
            
            if remaining > 70:
                status_color = "🟢"
            elif remaining > 30:
                status_color = "🟡"
            else:
                status_color = "🔴"
            
            st.write(f"{status_color} **{account_name}**: {remaining}/100")
    
    # Ana sayfa tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Bulk Campaign", 
        "✉️ Single Email", 
        "📝 Custom Templates", 
        "👁️ Preview", 
        "⚙️ Settings"
    ])
    
    with tab1:
        st.header("📨 Bulk Email Campaign")
        
        # Campaign ayarları
        col1, col2, col3 = st.columns(3)
        
        with col1:
            campaign_type = st.selectbox(
                "Campaign Type",
                ["partnership", "cold"],
                help="Partnership: B2B partnerships, Cold: Lead generation"
            )
        
        with col2:
            delay_time = st.slider("Delay Between Emails (seconds)", 1, 15, 5)
        
        with col3:
            use_custom_template = st.checkbox("Use Custom Template", help="Use your own template instead of default")
        
        # Custom template inputs (if selected)
        if use_custom_template:
            st.markdown("### 📝 Custom Template")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_subject = st.text_input(
                    "Subject Line", 
                    placeholder="Use {name} and {company} as placeholders",
                    help="Example: Partnership Opportunity with {company}"
                )
            
            with col2:
                sender_name = st.text_input("Sender Name", value="Tahidem Team")
            
            custom_content = st.text_area(
                "Email Content (HTML)", 
                height=200,
                placeholder="Write your HTML email template here. Use {name} and {company} as placeholders.",
                help="You can use HTML tags for formatting. Variables: {name}, {company}"
            )
        
        # CSV upload
        st.markdown("### 📂 Upload Recipients")
        uploaded_file = st.file_uploader(
            "Upload CSV file (columns: email, name, company)", 
            type=['csv'],
            help="CSV should contain: email, name, company columns"
        )
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("📋 **Uploaded Data Preview:**")
            st.dataframe(df.head(10))
            
            st.write(f"**Total Recipients:** {len(df)}")
            
            # Validation
            required_columns = ['email', 'name', 'company']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing columns: {', '.join(missing_columns)}")
            else:
                st.success("✅ CSV format is correct!")
                
                # Campaign start button
                if use_custom_template and (not custom_subject or not custom_content):
                    st.warning("⚠️ Please fill in custom template fields!")
                else:
                    if st.button("🚀 START CAMPAIGN", type="primary", use_container_width=True):
                        st.markdown("---")
                        st.header("📊 Campaign Progress")
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Results containers
                        success_container = st.container()
                        error_container = st.container()
                        
                        total_emails = len(df)
                        successful_sends = []
                        failed_sends = []
                        
                        for index, row in df.iterrows():
                            # Available account bul
                            account = automation.get_available_account(campaign_type)
                            
                            if not account:
                                st.error(f"❌ No available accounts for {campaign_type} type!")
                                break
                            
                            # Template hazırla
                            if use_custom_template:
                                subject, content = automation.format_template(
                                    campaign_type, 
                                    row.get('name', 'Dear Professional'),
                                    row.get('company', 'Your Company'),
                                    custom_subject,
                                    custom_content
                                )
                            else:
                                subject, content = automation.format_template(
                                    campaign_type, 
                                    row.get('name', 'Dear Professional'),
                                    row.get('company', 'Your Company')
                                )
                            
                            # Email gönder
                            success, message = automation.send_single_email(
                                account, row['email'], subject, content
                            )
                            
                            # Progress güncelle
                            progress = (index + 1) / total_emails
                            progress_bar.progress(progress)
                            
                            status_emoji = "✅" if success else "❌"
                            status_text.text(f"{status_emoji} {index + 1}/{total_emails} - {row['email']} via {account['email']}")
                            
                            # Results topla
                            if success:
                                successful_sends.append({
                                    'email': row['email'],
                                    'name': row.get('name', ''),
                                    'company': row.get('company', ''),
                                    'sender': account['email']
                                })
                            else:
                                failed_sends.append({
                                    'email': row['email'],
                                    'error': message
                                })
                            
                            # Rate limiting
                            time.sleep(delay_time)
                        
                        # Final results
                        st.markdown("---")
                        st.header("🎯 Campaign Results")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("✅ Successful", len(successful_sends))
                        with col2:
                            st.metric("❌ Failed", len(failed_sends))
                        with col3:
                            success_rate = (len(successful_sends) / total_emails) * 100
                            st.metric("📈 Success Rate", f"{success_rate:.1f}%")
                        
                        # Detailed results
                        if successful_sends:
                            st.success("✅ **Successful Sends:**")
                            success_df = pd.DataFrame(successful_sends)
                            st.dataframe(success_df)
                        
                        if failed_sends:
                            st.error("❌ **Failed Sends:**")
                            failed_df = pd.DataFrame(failed_sends)
                            st.dataframe(failed_df)
                        
                        st.balloons()
                        st.success("🎉 Campaign completed successfully!")
    
    with tab2:
        st.header("✉️ Single Email Sender")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📧 Recipient Details")
            recipient_email = st.text_input("Recipient Email *")
            recipient_name = st.text_input("Recipient Name *")
            recipient_company = st.text_input("Company Name")
        
        with col2:
            st.subheader("⚙️ Email Settings")
            email_type = st.selectbox("Email Type", ["partnership", "cold"])
            sender_account = st.selectbox(
                "Sender Account",
                [acc['email'] for acc in EMAIL_ACCOUNTS if acc['type'] == email_type]
            )
        
        st.markdown("---")
        
        # Template seçimi
        use_custom_single = st.checkbox("Use Custom Template for Single Email")
        
        if use_custom_single:
            col1, col2 = st.columns(2)
            with col1:
                single_subject = st.text_input("Subject Line", placeholder="Use {name} and {company}")
            with col2:
                pass
            
            single_content = st.text_area(
                "Email Content (HTML)", 
                height=300,
                placeholder="Write your HTML email template here..."
            )
        
        if st.button("📤 Send Email", type="primary", use_container_width=True):
            if recipient_email and recipient_name:
                account = next(acc for acc in EMAIL_ACCOUNTS if acc['email'] == sender_account)
                
                if use_custom_single and single_subject and single_content:
                    subject, content = automation.format_template(
                        email_type, recipient_name, recipient_company or "Your Company",
                        single_subject, single_content
                    )
                else:
                    subject, content = automation.format_template(
                        email_type, recipient_name, recipient_company or "Your Company"
                    )
                
                success, message = automation.send_single_email(account, recipient_email, subject, content)
                
                if success:
                    st.success(f"✅ Email sent successfully to {recipient_email}")
                    st.info(f"📧 Sent via: {sender_account}")
                else:
                    st.error(f"❌ Error: {message}")
            else:
                st.warning("⚠️ Email and name fields are required!")
    
    with tab3:
        st.header("📝 Custom Email Templates")
        st.markdown("Create and manage your email templates with dynamic variables.")
        
        template_type = st.selectbox("Select Template Type", ["partnership", "cold"])
        
        st.markdown(f"### ✏️ Edit {template_type.title()} Template")
        
        # Current template
        current_template = st.session_state.custom_templates[template_type]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**📋 Available Variables:**")
            st.code("{name} - Recipient name")
            st.code("{company} - Company name")
            
            st.markdown("**💡 HTML Tips:**")
            st.markdown("- Use `<strong>` for bold")
            st.markdown("- Use `<p>` for paragraphs") 
            st.markdown("- Use `<ul><li>` for lists")
            st.markdown("- Use inline CSS for styling")
        
        with col2:
            # Subject editing
            new_subject = st.text_input(
                "Subject Template", 
                value=current_template['subject'],
                help="Use {name} and {company} as placeholders"
            )
            
            # Content editing
            new_content = st.text_area(
                "Email Content Template (HTML)", 
                value=current_template['content'],
                height=400,
                help="Use {name} and {company} as placeholders"
            )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Template", type="primary"):
                st.session_state.custom_templates[template_type] = {
                    'subject': new_subject,
                    'content': new_content
                }
                st.success(f"✅ {template_type.title()} template saved!")
        
        with col2:
            if st.button("🔄 Reset to Default"):
                st.session_state.custom_templates[template_type] = DEFAULT_TEMPLATES[template_type].copy()
                st.success(f"✅ {template_type.title()} template reset to default!")
                st.experimental_rerun()
    
    with tab4:
        st.header("👁️ Template Preview")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🧪 Test Data")
            preview_type = st.selectbox("Template Type", ["partnership", "cold"])
            test_name = st.text_input("Test Name", "John Smith")
            test_company = st.text_input("Test Company", "TechCorp Inc.")
            
            if st.button("🔍 Generate Preview"):
                subject, content = automation.format_template(
                    preview_type, test_name, test_company
                )
                
                st.session_state.preview_subject = subject
                st.session_state.preview_content = content
        
        with col2:
            st.subheader("📧 Email Preview")
            
            if hasattr(st.session_state, 'preview_subject'):
                st.markdown("**Subject:**")
                st.info(st.session_state.preview_subject)
                
                st.markdown("**Content:**")
                st.components.v1.html(
                    st.session_state.preview_content, 
                    height=600, 
                    scrolling=True
                )
            else:
                st.info("👆 Generate a preview to see your email template")
    
    with tab5:
        st.header("⚙️ System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📧 Email Accounts")
            
            for acc in EMAIL_ACCOUNTS:
                sent_today = st.session_state.email_stats['daily_counts'][acc['email']]
                remaining = 100 - sent_today
                
                # Progress bar for each account
                progress = sent_today / 100
                
                st.markdown(f"**{acc['email']}**")
                st.progress(progress)
                st.caption(f"Type: {acc['type']} | Sent: {sent_today}/100 | Remaining: {remaining}")
                st.markdown("---")
        
        with col2:
            st.subheader("🔧 System Controls")
            
            if st.button("🔄 Reset Daily Counters", type="secondary"):
                for acc in EMAIL_ACCOUNTS:
                    acc['sent_today'] = 0
                    st.session_state.email_stats['daily_counts'][acc['email']] = 0
                st.success("✅ Daily counters reset!")
            
            if st.button("📊 Reset All Statistics", type="secondary"):
                st.session_state.email_stats = {
                    'total_sent': 0,
                    'successful': 0,
                    'failed': 0,
                    'daily_counts': {acc['email']: 0 for acc in EMAIL_ACCOUNTS}
                }
                st.success("✅ All statistics reset!")
            
            if st.button("📝 Reset Templates to Default", type="secondary"):
                st.session_state.custom_templates = DEFAULT_TEMPLATES.copy()
                st.success("✅ Templates reset to default!")
            
            # Master user için özel ayarlar
            if st.session_state.get("user_role") == "master":
                st.markdown("---")
                st.subheader("🔴 Master Controls")
                st.warning("⚠️ Master user exclusive features")
                
                if st.button("🗑️ Clear All Data", type="secondary"):
                    # Tüm session state'i temizle
                    keys_to_keep = ["password_correct", "user_role"]
                    for key in list(st.session_state.keys()):
                        if key not in keys_to_keep:
                            del st.session_state[key]
                    st.success("✅ All data cleared!")
                    st.experimental_rerun()
        
        # System info
        st.markdown("---")
        st.subheader("ℹ️ System Information")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accounts", len(EMAIL_ACCOUNTS))
        with col2:
            partnership_accounts = len([acc for acc in EMAIL_ACCOUNTS if acc['type'] == 'partnership'])
            st.metric("Partnership Accounts", partnership_accounts)
        with col3:
            cold_accounts = len([acc for acc in EMAIL_ACCOUNTS if acc['type'] == 'cold'])
            st.metric("Cold Outreach Accounts", cold_accounts)
        
        st.info("💡 **Daily Limit:** 100 emails per account | **Total Daily Capacity:** 1400 emails")
        
        # Güvenlik bilgileri
        st.markdown("---")
        st.subheader("🔐 Security Information")
        
        user_role = st.session_state.get("user_role", "admin")
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"👤 **Current User:** {user_role.upper()}")
            st.info(f"🕒 **Session Started:** {login_time}")
        
        with col2:
            st.info("🔒 **Security Level:** High")
            st.info("🛡️ **Data Encryption:** Active")

# Ana uygulama başlatma
def main():
    # Şifre kontrolü
    if check_password():
        main_app()

if __name__ == "__main__":
    main()
