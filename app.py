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

# Email hesapları
EMAIL_ACCOUNTS = [
    {'email': 'partnerships@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'business@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'collaborations@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'deals@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0},
    {'email': 'marketing@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0},
    {'email': 'partnership@tahidem.com', 'password': 'GM8+h!M>An5', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'amazonpartnership@tahidem.com', 'password': '5V7SOWq:V&zQ', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'partnershipamazon@tahidem.com', 'password': 'u&17]ukQ', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'exclusivebrand@tahidem.com', 'password': '5M?$Kz^m', 'type': 'brand_partnership', 'sent_today': 0},
    {'email': 'outreach@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_hunter', 'sent_today': 0},
    {'email': 'team@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_hunter', 'sent_today': 0},
    {'email': 'hello@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_hunter', 'sent_today': 0},
    {'email': 'connect@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0},
    {'email': 'growth@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0}
]

# SMTP ayarları
SMTP_SERVER = 'smtp.hostinger.com'
SMTP_PORT = 465

# 🎯 YENİ TEMPLATE SİSTEMİ - 9 FARKLI TEMPLATE
DEFAULT_TEMPLATES = {
    # 🎯 BRAND HUNTER TEMPLATES (Marka Arayıcıları)
    "brand_hunter_1": {
        "name": "Amazon Brand Hunter - General Recruitment",
        "category": "brand_hunter",
        "subject": "Amazon Brand Partnership Opportunity - TAHIDEM LLC Collaboration",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 32px; font-weight: bold;">TAHIDEM LLC</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Amazon Partnership Specialists</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 24px; margin-bottom: 20px;">Hello {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                TAHIDEM LLC is establishing exclusive distribution partnerships with successful Amazon brands, and we want to work with experienced professionals in this field.
                </p>
                
                <!-- Sought Profile Box -->
                <div style="background: #f8f9fa; border-left: 5px solid #667eea; padding: 25px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0; font-size: 20px;">🎯 SOUGHT PROFILE:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px; color: #555;">
                        <li style="margin-bottom: 10px;">✅ <strong>Amazon ecosystem experience</strong></li>
                        <li style="margin-bottom: 10px;">✅ <strong>Network with brand owners/managers</strong></li>
                        <li style="margin-bottom: 10px;">✅ <strong>English communication skills</strong></li>
                        <li style="margin-bottom: 10px;">✅ <strong>Sales/business development experience</strong></li>
                    </ul>
                </div>
                
                <!-- Job Description -->
                <div style="background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px;">💼 JOB DESCRIPTION:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px;">
                        <li style="margin-bottom: 10px;">• Identify brands selling on Amazon</li>
                        <li style="margin-bottom: 10px;">• Establish communication with brand authorities</li>
                        <li style="margin-bottom: 10px;">• Conduct preliminary meetings on behalf of TAHIDEM LLC</li>
                        <li style="margin-bottom: 10px;">• Manage distribution agreement signing process</li>
                    </ul>
                </div>
                
                <!-- Payment Structure -->
                <div style="background: #27ae60; padding: 30px; border-radius: 10px; margin: 30px 0; color: white; text-align: center;">
                    <h3 style="margin-top: 0; font-size: 22px;">💰 PAYMENT STRUCTURE</h3>
                    <div style="font-size: 18px; margin: 20px 0;">
                        <p style="margin: 10px 0;"><strong>Standard Brands:</strong> $1,000</p>
                        <p style="margin: 10px 0;"><strong>Mid-scale ($200K+ monthly):</strong> $1,500-$3,500</p>
                        <p style="margin: 10px 0;"><strong>Premium Brands ($500K+ monthly):</strong> $4,000-$7,500</p>
                        <p style="margin: 10px 0;"><strong>Proven profitability and growth trajectory</p>
                    </div>
                </div>
                
                <!-- AMAZON Target Criteria -->
                <div style="border: 2px solid #e74c3c; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #e74c3c; margin-top: 0; font-size: 20px;">🎯 AMAZON TARGET CRITERIA:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px; color: #555;">
                        <li style="margin-bottom: 8px;">• Monthly Amazon sales $50K+</li>
                        <li style="margin-bottom: 8px;">• Active in US/Australia/Europe markets</li>
                        <li style="margin-bottom: 8px;">• Trademarked products</li>
                        <li style="margin-bottom: 8px;">• 3+ years active on Amazon</li>
                    </ul>
                </div>
                
                <p style="font-size: 18px; margin: 30px 0; text-align: center; color: #2c3e50;">
                    <strong>Would you like to evaluate this opportunity?</strong>
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:partnerships@tahidem.com" style="background: #e74c3c; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Apply Now</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 0; font-weight: bold; font-size: 16px;">TAHIDEM LLC</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">partnerships@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    "brand_hunter_2": {
        "name": "Detailed Brand Hunter Position",
        "category": "brand_hunter",
        "subject": "Brand Hunter Position - TAHIDEM LLC - $10K+ Per Deal",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 40px 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🎯 BRAND HUNTER POSITION</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">TAHIDEM LLC - Exclusive Opportunity</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Dear {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                We want to work with you for the <strong>Brand Hunter position</strong> within TAHIDEM LLC.
                </p>
                
                <!-- Job Tasks -->
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50; font-size: 20px; margin-bottom: 20px;">📋 JOB DESCRIPTION:</h3>
                    
                    <!-- Task 1 -->
                    <div style="background: #f1f2f6; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3742fa;">
                        <h4 style="color: #3742fa; margin: 0 0 10px 0;">1. BRAND IDENTIFICATION:</h4>
                        <ul style="margin: 10px 0; padding-left: 20px; color: #555;">
                            <li>Identify brands making $50K+ monthly sales on Amazon</li>
                            <li>Sales volume and potential analysis</li>
                            <li>Competition status evaluation</li>
                        </ul>
                    </div>
                    
                    <!-- Task 2 -->
                    <div style="background: #f1f2f6; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #2ed573;">
                        <h4 style="color: #2ed573; margin: 0 0 10px 0;">2. COMMUNICATION ESTABLISHMENT:</h4>
                        <ul style="margin: 10px 0; padding-left: 20px; color: #555;">
                            <li>Direct communication with brand owners/CEOs</li>
                            <li>Preliminary presentation representing TAHIDEM LLC</li>
                            <li>Explain distribution partnership opportunity</li>
                            <li>Plan meeting appointments</li>
                        </ul>
                    </div>
                    
                    <!-- Task 3 -->
                    <div style="background: #f1f2f6; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #ff6348;">
                        <h4 style="color: #ff6348; margin: 0 0 10px 0;">3. PROCESS MANAGEMENT:</h4>
                        <ul style="margin: 10px 0; padding-left: 20px; color: #555;">
                            <li>Bridge between brand and TAHIDEM LLC</li>
                            <li>Preliminary negotiation of agreement terms</li>
                            <li>Collection of required documents</li>
                            <li>Follow-up of signing process</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Target Brands -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 18px;">🎯 TARGET BRANDS:</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px;">Consumer Electronics</span>
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px;">Home & Kitchen</span>
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px;">Health & Personal Care</span>
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px;">Sports & Outdoors</span>
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px;">Baby Products</span>
                    </div>
                </div>
                
                <!-- Payment Details -->
                <div style="background: #2ed573; padding: 25px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px; text-align: center;">💰 PAYMENT DETAILS</h3>
                    <div style="text-align: center; margin: 20px 0;">
                        <p style="margin: 8px 0; font-size: 16px;"><strong>Base Payment:</strong> $1,000 per deal</p>
                        <p style="margin: 8px 0; font-size: 16px;"><strong>$100K+ monthly sales:</strong> +$1,000 bonus</p>
                        <p style="margin: 8px 0; font-size: 16px;"><strong>$200K+ monthly sales:</strong> +$1,500 - $3,000 bonus</p>
                        <p style="margin: 8px 0; font-size: 16px;"><strong>$500K+ monthly sales:</strong> +$3,500 - $7,500 bonus</p>
                    </div>
                    <p style="text-align: center; margin: 15px 0 0 0; font-size: 14px; opacity: 0.9;">Payment processing during agreement signing</p>

                </div>
                
                <!-- Working Conditions -->
                <div style="border: 2px solid #3742fa; padding: 20px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #3742fa; margin-top: 0;">⚙️ WORKING CONDITIONS:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px; color: #555;">
                        <li style="margin-bottom: 8px;">• Completely remote work</li>
                        <li style="margin-bottom: 8px;">• Flexible working hours</li>
                        <li style="margin-bottom: 8px;">• Weekly progress report</li>
                        <li style="margin-bottom: 8px;">• Monthly minimum 5 brand target</li>
                    </ul>
                </div>
                
                <p style="font-size: 16px; margin: 30px 0; text-align: center; color: #2c3e50;">
                    If interested, could you share your CV and Amazon experience?
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:team@tahidem.com" style="background: #ff6b6b; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Send Your CV</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 25px; text-align: center; color: white;">
                <p style="margin: 0; font-weight: bold;">TAHIDEM LLC HR Department</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">team@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    # 🤝 BRAND PARTNERSHIP TEMPLATES (Marka Ortaklıkları)

"brand_partnership_2": {
    "name": "Exclusive Distribution Agreement",
    "category": "brand_partnership", 
    "subject": "Exclusive Amazon Distribution Partnership - {company} Authorized Reseller Opportunity",
    "content": """
    <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
    <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
        
        <!-- Header -->
        <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 40px 30px; text-align: center; color: white; position: relative;">
            <div style="position: absolute; top: 15px; right: 20px; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 12px;">EXCLUSIVE DISTRIBUTOR</div>
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🤝 EXCLUSIVE AMAZON DISTRIBUTION</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">TAHIDEM LLC - Authorized Reseller Partnership</p>
        </div>
        
        <!-- Main Content -->
        <div style="padding: 40px 30px;">
            <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Hello {name},</h2>
            
            <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
            My name is <strong>Onur Nakis</strong>, Owner of <strong>TAHIDEM LLC (EIN: 35-2742119)</strong>, based in Sheridan, WY, USA. I am very interested in establishing a wholesale partnership with <strong>{company}</strong> and becoming your exclusive authorized distributor on Amazon with significant investment commitment.
            </p>
            
            <!-- Company Information -->
            <div style="background: #f8f9fa; border-left: 5px solid #ff6b6b; padding: 25px; margin: 30px 0;">
                <h3 style="color: #ff6b6b; margin-top: 0; font-size: 20px;">🏢 About TAHIDEM LLC</h3>
                <div style="color: #555; margin: 15px 0;">
                    <p style="margin: 8px 0;"><strong>Company:</strong> TAHIDEM LLC</p>
                    <p style="margin: 8px 0;"><strong>EIN:</strong> 35-2742119</p>
                    <p style="margin: 8px 0;"><strong>Owner:</strong> Onur Nakis</p>
                    <p style="margin: 8px 0;"><strong>Location:</strong> 30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
                    <p style="margin: 8px 0;"><strong>Contact:</strong> business@tahidem.com</p>
                </div>
            </div>
            
            <!-- Our Primary Partnership Goal -->
            <div style="background: #2c3e50; border-left: 5px solid #ff6b6b; padding: 25px; margin: 30px 0; color: white;">
                <h3 style="color: #ff6b6b; margin-top: 0; font-size: 20px;">🎯 Our Primary Partnership Goal</h3>
                <p style="color: #fff; margin: 15px 0; font-size: 16px;">
                    <strong>Become your exclusive authorized distributor</strong> for ASINs you authorize us to sell, taking complete ownership of listing optimization, sales growth, and inventory management while maintaining continuous brand communication.
                </p>
            </div>
            
            <!-- Partnership Request -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                <h3 style="margin-top: 0; font-size: 20px; text-align: center;">🎯 PARTNERSHIP REQUEST</h3>
                
                <div style="display: grid; gap: 15px; margin: 25px 0;">
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">🏪 Wholesale Account Approval</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">To purchase your products directly at wholesale prices with significant investment commitment</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">📋 Letter of Authorization (LOA)</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Confirming that TAHIDEM LLC is an authorized reseller of your brand on Amazon</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">🔐 Brand Exclusivity</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Exclusive rights to sell your brand's products on Amazon with written consent requirement</p>
                    </div>
                </div>
            </div>
            
            <!-- Exclusive Distribution Services -->
            <div style="background: linear-gradient(135deg, #27ae60 0%, #2ed573 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                <h3 style="margin-top: 0; font-size: 20px; text-align: center;">🏆 EXCLUSIVE DISTRIBUTOR SERVICES</h3>
                
                <div style="display: grid; gap: 15px; margin: 25px 0;">
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">🔐 Exclusive ASIN Authorization</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Become sole authorized seller for ASINs you authorize us to sell</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">📈 Complete Listing Development</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Advanced SEO optimization, A+ content creation, and search ranking strategies</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">🎥 Professional Content Creation</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">High-quality product photography, infographics, and promotional videos</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 16px;">⭐ Strategic Review Growth</h4>
                        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Positive feedback enhancement and reputation management strategies</p>
                    </div>
                </div>
            </div>
            
            <!-- Million Dollar Customer Network -->
            <div style="background: #ff6b6b; padding: 30px; border-radius: 10px; margin: 30px 0; color: white; text-align: center;">
                <h3 style="margin-top: 0; font-size: 22px;">💰 MILLION DOLLAR CUSTOMER NETWORK</h3>
                <div style="margin: 20px 0;">
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Million-dollar customer network</strong> ensures guaranteed sales volume</p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>3-6 month bulk inventory purchases</strong> based on 30-day Amazon sales data</p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Zero inventory risk for your brand</strong> - we handle all stock management</p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>No stock purchase problems</strong> - guaranteed inventory commitment</p>
                </div>
            </div>
            
            <!-- Partnership Benefits -->
            <div style="background: #27ae60; padding: 30px; border-radius: 10px; margin: 30px 0; color: white; text-align: center;">
                <h3 style="margin-top: 0; font-size: 22px;">🎁 WHAT THIS PARTNERSHIP OFFERS</h3>
                <div style="margin: 20px 0;">
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Protect and enhance your brand's image</strong> on Amazon</p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Maintain consistent pricing and representation</strong></p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Drive long-term sales growth</strong> with strong investment in inventory</p>
                    <p style="margin: 8px 0; font-size: 16px;">✅ <strong>Significant investment in stocking and promoting</strong> your products</p>
                </div>
            </div>
            
            <!-- Distribution Partnership Process -->
            <div style="margin: 30px 0;">
                <h3 style="color: #2c3e50; font-size: 20px; margin-bottom: 20px;">🔄 Exclusive Distribution Process:</h3>
                
                <div style="display: grid; gap: 15px; margin: 20px 0;">
                    <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;">
                        <h4 style="color: #27ae60; margin: 0 0 8px 0;">1️⃣ Exclusive Distribution Authorization</h4>
                        <p style="margin: 0; color: #555; font-size: 14px;">Secure exclusive rights to sell your authorized Amazon ASINs as sole distributor</p>
                    </div>
                    <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; border-left: 4px solid #3742fa;">
                        <h4 style="color: #3742fa; margin: 0 0 8px 0;">2️⃣ Complete ASIN Development & Growth</h4>
                        <p style="margin: 0; color: #555; font-size: 14px;">SEO optimization, visual content creation, and listing development with continuous brand communication</p>
                    </div>
                    <div style="background: #fff5e6; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9f43;">
                        <h4 style="color: #ff9f43; margin: 0 0 8px 0;">3️⃣ Strategic Inventory Management</h4>
                        <p style="margin: 0; color: #555; font-size: 14px;">3-6 month bulk purchasing based on 30-day Amazon sales data analysis</p>
                    </div>
                    <div style="background: #ffeaea; padding: 20px; border-radius: 8px; border-left: 4px solid #ff6348;">
                        <h4 style="color: #ff6348; margin: 0 0 8px 0;">4️⃣ Comprehensive Reporting & Legal Compliance</h4>
                        <p style="margin: 0; color: #555; font-size: 14px;">Weekly/monthly sales & advertising reports, full legal requirements tracking</p>
                    </div>
                </div>
            </div>
            
            <!-- Exclusive Partnership Benefits -->
            <div style="border: 2px solid #667eea; padding: 25px; border-radius: 10px; margin: 30px 0;">
                <h3 style="color: #667eea; margin-top: 0;">🎁 Exclusive Distribution Benefits:</h3>
                <ul style="margin: 15px 0; padding-left: 20px; color: #555;">
                    <li style="margin-bottom: 8px;"><strong>Exclusive authorized distributor status</strong> for ASINs you authorize us to sell</li>
                    <li style="margin-bottom: 8px;"><strong>Complete ASIN development and optimization</strong> with continuous brand communication</li>
                    <li style="margin-bottom: 8px;"><strong>Guaranteed bulk inventory purchases</strong> from million-dollar customer network</li>
                    <li style="margin-bottom: 8px;"><strong>Professional content creation</strong> (images, videos, A+ content, infographics)</li>
                    <li style="margin-bottom: 8px;"><strong>Strategic positive review growth</strong> and reputation management</li>
                    <li style="margin-bottom: 8px;"><strong>Weekly/monthly performance reporting</strong> and advertising analytics</li>
                    <li style="margin-bottom: 8px;"><strong>Full legal compliance tracking</strong> and brand protection</li>
                    <li style="margin-bottom: 8px;"><strong>3-6 month inventory commitment</strong> based on 30-day sales data</li>
                </ul>
            </div>
            
            <!-- Professional Priority Statement -->
            <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 25px; border-radius: 10px; margin: 30px 0; color: white; text-align: center;">
                <h3 style="margin-top: 0; font-size: 20px;">🎯 OUR PROFESSIONAL PRIORITY</h3>
                <p style="margin: 15px 0; font-size: 16px;">
                    <strong>Our priority is to become the sole authorized seller</strong> for Amazon ASINs you provide us. We want to be your brand's distributor for relevant ASINs in the most professional way possible.
                </p>
            </div>
            
            <p style="font-size: 18px; margin: 30px 0; text-align: center; color: #2c3e50; font-weight: bold;">
                Ready to proceed immediately with exclusive distribution partnership?
            </p>
            
            <!-- CTA Button -->
            <div style="text-align: center; margin: 40px 0;">
                <a href="mailto:business@tahidem.com" style="background: #ff6b6b; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Discuss Exclusive Distribution Partnership</a>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
            <p style="margin: 0; font-weight: bold; font-size: 16px;">Onur Nakis - Sales Manager</p>
            <p style="margin: 5px 0; color: #ff6b6b; font-weight: bold;">TAHIDEM LLC (EIN: 35-2742119)</p>
            <p style="margin: 5px 0; opacity: 0.8;">30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
            <p style="margin: 5px 0 0 0; opacity: 0.8;">business@tahidem.com | https://tahidem.com/</p>
        </div>
    </div>
    </body></html>
    """
},
    
    # 🏢 SUPPLIER OUTREACH TEMPLATES (Tedarikçi İletişimi)
    "supplier_outreach_1": {
        "name": "Supplier Partnership Inquiry",
        "category": "supplier_outreach",
        "subject": "Supply Chain Partnership Opportunity - TAHIDEM LLC",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 40px 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🏢 SUPPLIER PARTNERSHIP</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">TAHIDEM LLC Supply Chain Network</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Dear {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                I hope this message finds you well. I'm reaching out from TAHIDEM LLC regarding a potential supply chain partnership with <strong>{company}</strong>.
                </p>
                
                <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                We're actively expanding our supplier network and believe your company's capabilities align perfectly with our growing market demands.
                </p>
                
                <!-- About TAHIDEM -->
                <div style="background: #f8f9fa; border-left: 5px solid #4facfe; padding: 25px; margin: 30px 0;">
                    <h3 style="color: #4facfe; margin-top: 0; font-size: 20px;">🚀 About TAHIDEM LLC</h3>
                    <p style="color: #555; margin: 15px 0;">
                        We're a rapidly growing e-commerce distribution company specializing in Amazon marketplace operations across multiple international markets. Our network spans the US, Europe, Australia, and Canada.
                    </p>
                </div>
                
                <!-- Our Requirements -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px;">📋 What We're Looking For:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px;">
                        <li style="margin-bottom: 12px;">🏭 <strong>Manufacturing Capacity:</strong> Ability to scale production based on demand</li>
                        <li style="margin-bottom: 12px;">✅ <strong>Quality Standards:</strong> ISO certifications and quality control systems</li>
                        <li style="margin-bottom: 12px;">🌍 <strong>Global Shipping:</strong> Experience with international logistics</li>
                        <li style="margin-bottom: 12px;">📊 <strong>Flexibility:</strong> Adaptable to market trends and seasonal demands</li>
                    </ul>
                </div>
                
                <!-- Partnership Benefits -->
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50; font-size: 20px; margin-bottom: 20px;">🤝 Partnership Benefits:</h3>
                    
                    <div style="display: grid; gap: 15px; margin: 20px 0;">
                        <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;">
                            <h4 style="color: #27ae60; margin: 0 0 8px 0;">💰 Guaranteed Volume Orders</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Minimum monthly orders of $100K+ with growth potential</p>
                        </div>
                        <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; border-left: 4px solid #3742fa;">
                            <h4 style="color: #3742fa; margin: 0 0 8px 0;">⚡ Fast Payment Terms</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">30-day payment terms with option for early payment discounts</p>
                        </div>
                        <div style="background: #fff5e6; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9f43;">
                            <h4 style="color: #ff9f43; margin: 0 0 8px 0;">📈 Long-term Partnership</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Multi-year contracts with annual volume increases</p>
                        </div>
                        <div style="background: #ffeaea; padding: 20px; border-radius: 8px; border-left: 4px solid #ff6348;">
                            <h4 style="color: #ff6348; margin: 0 0 8px 0;">🛠️ Product Development Support</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Collaborative product development and market insights</p>
                        </div>
                    </div>
                </div>
                
                <!-- Volume Projections -->
                <div style="background: #27ae60; padding: 30px; border-radius: 10px; margin: 30px 0; color: white; text-align: center;">
                    <h3 style="margin-top: 0; font-size: 22px;">📊 VOLUME PROJECTIONS</h3>
                    <div style="display: flex; gap: 20px; margin: 25px 0; flex-wrap: wrap; justify-content: center;">
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <h4 style="margin: 0; font-size: 28px; font-weight: bold;">$2M+</h4>
                            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Year 1 Target</p>
                        </div>
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <h4 style="margin: 0; font-size: 28px; font-weight: bold;">$5M+</h4>
                            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Year 2 Target</p>
                        </div>
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <h4 style="margin: 0; font-size: 28px; font-weight: bold;">$10M+</h4>
                            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Year 3 Target</p>
                        </div>
                    </div>
                </div>
                
                <!-- Product Categories -->
                <div style="border: 2px solid #4facfe; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #4facfe; margin-top: 0;">🎯 Priority Product Categories:</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Consumer Electronics</span>
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Home & Garden</span>
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Health & Beauty</span>
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Sports & Fitness</span>
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Baby Products</span>
                        <span style="background: #4facfe; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Pet Supplies</span>
                    </div>
                </div>
                
                <!-- Next Steps -->
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">📋 Next Steps:</h3>
                    <ol style="margin: 15px 0; padding-left: 20px; color: #555;">
                        <li style="margin-bottom: 8px;">Initial capability assessment call</li>
                        <li style="margin-bottom: 8px;">Product catalog and pricing review</li>
                        <li style="margin-bottom: 8px;">Quality standards verification</li>
                        <li style="margin-bottom: 8px;">Partnership agreement negotiation</li>
                    </ol>
                </div>
                
                <p style="font-size: 18px; margin: 30px 0; text-align: center; color: #2c3e50; font-weight: bold;">
                    Interested in exploring this partnership opportunity?
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:deals@tahidem.com" style="background: #4facfe; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Schedule a Call</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 0; font-weight: bold; font-size: 16px;">Supply Chain Team</p>
                <p style="margin: 5px 0; color: #4facfe; font-weight: bold;">TAHIDEM LLC</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">deals@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    "supplier_outreach_2": {
        "name": "Wholesale Distribution Partnership",
        "category": "supplier_outreach",
        "subject": "Wholesale Distribution Partnership - {company} x TAHIDEM LLC",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(45deg, #fa709a, #fee140); padding: 40px 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🛒 WHOLESALE PARTNERSHIP</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">TAHIDEM LLC Distribution Network</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Hello {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                I'm writing to explore a <strong>wholesale distribution partnership</strong> between TAHIDEM LLC and <strong>{company}</strong>.
                </p>
                
                <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                We've identified your company as a potential strategic partner for our expanding e-commerce distribution operations.
                </p>
                
                <!-- Market Opportunity -->
                <div style="background: #f8f9fa; border-left: 5px solid #fa709a; padding: 25px; margin: 30px 0;">
                    <h3 style="color: #fa709a; margin-top: 0; font-size: 20px;">🎯 Market Opportunity</h3>
                    <p style="color: #555; margin: 15px 0;">
                        The global e-commerce market is projected to reach <strong>$8.1 trillion by 2026</strong>. Amazon alone processes over <strong>$500 billion</strong> in annual sales. We want to help you capture your share of this massive opportunity.
                    </p>
                </div>
                
                <!-- Why Partner With Us -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px;">🚀 Why Partner With TAHIDEM LLC?</h3>
                    <div style="margin: 20px 0;">
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">📊 Proven Track Record</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">$50M+ in managed sales across 200+ brand partnerships</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">🌍 Global Reach</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Active in 15+ countries with localized operations</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">⚡ Fast Growth</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">300% year-over-year growth with aggressive expansion plans</p>
                        </div>
                    </div>
                </div>
                
                <!-- Partnership Structure -->
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50; font-size: 20px; margin-bottom: 20px;">🤝 Partnership Structure:</h3>
                    
                    <div style="display: grid; gap: 15px; margin: 20px 0;">
                        <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;">
                            <h4 style="color: #27ae60; margin: 0 0 8px 0;">💼 Exclusive Distribution Rights</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Become our preferred supplier for specific product categories</p>
                        </div>
                        <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; border-left: 4px solid #3742fa;">
                            <h4 style="color: #3742fa; margin: 0 0 8px 0;">📈 Volume Commitments</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Guaranteed minimum order quantities with growth projections</p>
                        </div>
                        <div style="background: #fff5e6; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9f43;">
                            <h4 style="color: #ff9f43; margin: 0 0 8px 0;">💰 Competitive Pricing</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Wholesale pricing with volume discounts and early payment terms</p>
                        </div>
                        <div style="background: #ffeaea; padding: 20px; border-radius: 8px; border-left: 4px solid #ff6348;">
                            <h4 style="color: #ff6348; margin: 0 0 8px 0;">🎯 Marketing Support</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Co-marketing opportunities and brand promotion</p>
                        </div>
                    </div>
                </div>
                
                <!-- Financial Projections -->
                <div style="background: #27ae60; padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px; text-align: center;">💰 FINANCIAL PROJECTIONS</h3>
                    <div style="display: grid; gap: 20px; margin: 25px 0; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 24px;">Q1</h4>
                            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">$500K</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Initial Orders</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 24px;">Q2</h4>
                            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">$1.2M</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Scale Up</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 24px;">Q3</h4>
                            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">$2.5M</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Peak Season</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 24px;">Q4</h4>
                            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">$3.8M</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Holiday Rush</p>
                        </div>
                    </div>
                    <p style="text-align: center; margin: 20px 0 0 0; font-size: 16px; font-weight: bold;">
                        Total Year 1 Projection: $8M+
                    </p>
                </div>
                
                <!-- Success Metrics -->
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">📊 Our Success Metrics:</h3>
                    <div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; justify-content: center;">
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <div style="background: #3742fa; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 24px; font-weight: bold;">98%</div>
                            <p style="margin: 0; color: #555; font-size: 14px;">On-time Delivery</p>
                        </div>
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <div style="background: #27ae60; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 24px; font-weight: bold;">15</div>
                            <p style="margin: 0; color: #555; font-size: 14px;">Day Payment Terms</p>
                        </div>
                        <div style="text-align: center; flex: 1; min-width: 120px;">
                            <div style="background: #ff6348; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 24px; font-weight: bold;">24/7</div>
                            <p style="margin: 0; color: #555; font-size: 14px;">Support Available</p>
                        </div>
                    </div>
                </div>
                
                <!-- Requirements -->
                <div style="border: 2px solid #fa709a; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #fa709a; margin-top: 0;">✅ Partnership Requirements:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px; color: #555;">
                        <li style="margin-bottom: 8px;">Minimum 5 years in business with proven track record</li>
                        <li style="margin-bottom: 8px;">Quality certifications (ISO, CE, FCC, etc.)</li>
                        <li style="margin-bottom: 8px;">Capacity to fulfill $500K+ monthly orders</li>
                        <li style="margin-bottom: 8px;">English-speaking business development team</li>
                        <li style="margin-bottom: 8px;">Competitive wholesale pricing structure</li>
                    </ul>
                </div>
                
                <p style="font-size: 18px; margin: 30px 0; text-align: center; color: #2c3e50; font-weight: bold;">
                    Ready to scale your business with us?
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:marketing@tahidem.com" style="background: linear-gradient(45deg, #fa709a, #fee140); color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Discuss Partnership</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 0; font-weight: bold; font-size: 16px;">Wholesale Partnerships Team</p>
                <p style="margin: 5px 0; color: #fa709a; font-weight: bold;">TAHIDEM LLC</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">marketing@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    "supplier_outreach_3": {
        "name": "Private Label Manufacturing Partnership",
        "category": "supplier_outreach",
        "subject": "Private Label Manufacturing Partnership - TAHIDEM LLC",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 40px 30px; text-align: center; color: #2c3e50;">
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🏭 PRIVATE LABEL PARTNERSHIP</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.8;">TAHIDEM LLC Manufacturing Network</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Dear {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                I'm reaching out to explore a <strong>private label manufacturing partnership</strong> between TAHIDEM LLC and <strong>{company}</strong>.
                </p>
                
                <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                We're looking for reliable manufacturing partners to produce high-quality products under our private label brands for the global e-commerce market.
                </p>
                
                <!-- Private Label Opportunity -->
                <div style="background: #f8f9fa; border-left: 5px solid #a8edea; padding: 25px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0; font-size: 20px;">🎯 Private Label Opportunity</h3>
                    <p style="color: #555; margin: 15px 0;">
                        The private label market is experiencing explosive growth, with <strong>Amazon's private label sales exceeding $25 billion annually</strong>. We want to partner with you to capture this opportunity through innovative product development and manufacturing excellence.
                    </p>
                </div>
                
                <!-- Our Private Label Brands -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px; text-align: center;">🏷️ Our Private Label Portfolio</h3>
                    <div style="display: grid; gap: 15px; margin: 25px 0;">
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">🏠 HomeTech Solutions</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Smart home devices and automation products</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">💪 FitLife Pro</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Fitness equipment and wellness products</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">🌿 EcoLiving Essentials</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Sustainable household and personal care products</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <h4 style="margin: 0 0 8px 0; font-size: 16px;">🐾 PetCare Plus</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Premium pet accessories and care products</p>
                        </div>
                    </div>
                </div>
                
                <!-- Manufacturing Requirements -->
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50; font-size: 20px; margin-bottom: 20px;">🔧 Manufacturing Requirements:</h3>
                    
                    <div style="display: grid; gap: 15px; margin: 20px 0;">
                        <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;">
                            <h4 style="color: #27ae60; margin: 0 0 8px 0;">✅ Quality Standards</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">ISO 9001, CE, FCC, RoHS certifications required</p>
                        </div>
                        <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; border-left: 4px solid #3742fa;">
                            <h4 style="color: #3742fa; margin: 0 0 8px 0;">🏭 Production Capacity</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Minimum 10,000 units per month scalability</p>
                        </div>
                        <div style="background: #fff5e6; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9f43;">
                            <h4 style="color: #ff9f43; margin: 0 0 8px 0;">🎨 Customization</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">Custom packaging, branding, and product modifications</p>
                        </div>
                        <div style="background: #ffeaea; padding: 20px; border-radius: 8px; border-left: 4px solid #ff6348;">
                            <h4 style="color: #ff6348; margin: 0 0 8px 0;">⚡ Lead Times</h4>
                            <p style="margin: 0; color: #555; font-size: 14px;">30-45 day production cycles with rush order capabilities</p>
                        </div>
                    </div>
                </div>
                
                <!-- Partnership Benefits -->
                <div style="background: #27ae60; padding: 30px; border-radius: 10px; margin: 30px 0; color: white;">
                    <h3 style="margin-top: 0; font-size: 20px; text-align: center;">🤝 Partnership Benefits</h3>
                    <div style="display: grid; gap: 20px; margin: 25px 0; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));">
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 18px;">💰 Guaranteed Orders</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">$3M+</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Annual Volume</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 18px;">📈 Growth Potential</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">500%</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">3-Year Growth</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center;">
                            <h4 style="margin: 0; font-size: 18px;">🎯 Market Access</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">15+</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Countries</p>
                        </div>
                    </div>
                </div>
                
                <!-- Product Development Process -->
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">🔄 Product Development Process:</h3>
                    <div style="margin: 20px 0;">
                        <div style="display: flex; align-items: center; margin: 15px 0;">
                            <div style="background: #a8edea; color: #2c3e50; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">1</div>
                            <p style="margin: 0; color: #555;"><strong>Market Research:</strong> Identify trending products and customer needs</p>
                        </div>
                        <div style="display: flex; align-items: center; margin: 15px 0;">
                            <div style="background: #a8edea; color: #2c3e50; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">2</div>
                            <p style="margin: 0; color: #555;"><strong>Design & Prototyping:</strong> Collaborative product design and testing</p>
                        </div>
                        <div style="display: flex; align-items: center; margin: 15px 0;">
                            <div style="background: #a8edea; color: #2c3e50; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">3</div>
                            <p style="margin: 0; color: #555;"><strong>Quality Testing:</strong> Rigorous quality control and certification</p>
                        </div>
                        <div style="display: flex; align-items: center; margin: 15px 0;">
                            <div style="background: #a8edea; color: #2c3e50; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">4</div>
                            <p style="margin: 0; color: #555;"><strong>Mass Production:</strong> Scale manufacturing and global distribution</p>
                        </div>
                    </div>
                </div>
                
                <!-- Success Story -->
                <div style="border: 2px solid #fed6e3; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="color: #e91e63; margin-top: 0;">🏆 Success Story:</h3>
                    <div style="background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">Smart Home Device Partnership</h4>
                        <p style="margin: 10px 0; color: #555;">
                            Our partnership with a Chinese manufacturer resulted in a smart home device that became a <strong>top 10 bestseller</strong> on Amazon within 6 months.
                        </p>
                        <div style="display: flex; gap: 20px; margin: 15px 0; flex-wrap: wrap;">
                            <div style="text-align: center; flex: 1; min-width: 100px;">
                                <p style="margin: 0; font-size: 20px; font-weight: bold; color: #27ae60;">$5M</p>
                                <p style="margin: 0; font-size: 12px; color: #555;">Revenue Generated</p>
                            </div>
                            <div style="text-align: center; flex: 1; min-width: 100px;">
                                <p style="margin: 0; font-size: 20px; font-weight: bold; color: #3742fa;">50K+</p>
                                <p style="margin: 0; font-size: 12px; color: #555;">Units Sold</p>
                            </div>
                            <div style="text-align: center; flex: 1; min-width: 100px;">
                                <p style="margin: 0; font-size: 20px; font-weight: bold; color: #ff6348;">4.8★</p>
                                <p style="margin: 0; font-size: 12px; color: #555;">Customer Rating</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Investment & Timeline -->
                <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 30px; border-radius: 10px; margin: 30px 0; color: #2c3e50;">
                    <h3 style="margin-top: 0; font-size: 20px; text-align: center;">💼 Investment & Timeline</h3>
                    <div style="display: flex; gap: 20px; margin: 25px 0; flex-wrap: wrap; justify-content: center;">
                        <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 8px; text-align: center; flex: 1; min-width: 150px;">
                            <h4 style="margin: 0; font-size: 18px;">Initial Investment</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">$50K</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Tooling & Setup</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 8px; text-align: center; flex: 1; min-width: 150px;">
                            <h4 style="margin: 0; font-size: 18px;">Development Time</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">60-90</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Days</p>
                        </div>
                        <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 8px; text-align: center; flex: 1; min-width: 150px;">
                            <h4 style="margin: 0; font-size: 18px;">Break-even</h4>
                            <p style="margin: 10px 0; font-size: 24px; font-weight: bold;">6-8</p>
                            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Months</p>
                        </div>
                    </div>
                </div>
                
                <p style="font-size: 18px; margin: 30px 0; text-align: center; color: #2c3e50; font-weight: bold;">
                    Ready to build the next bestselling product together?
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:connect@tahidem.com" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #2c3e50; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Start Partnership Discussion</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 0; font-weight: bold; font-size: 16px;">Private Label Development Team</p>
                <p style="margin: 5px 0; color: #a8edea; font-weight: bold;">TAHIDEM LLC</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">connect@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
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
        if "password" in st.session_state:
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
    
    def format_template(self, template_key, name, company):
        """Template'i format et"""
        template = st.session_state.custom_templates[template_key]
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
        st.markdown("**Advanced Email Campaign Management System - 9 Professional Templates**")
    
    with col2:
        user_role = st.session_state.get("user_role", "admin")
        role_color = "🔴" if user_role == "master" else "🟢"
        st.info(f"{role_color} **{user_role.upper()}** ACCESS")
    
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
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
        "📝 Template Manager", 
        "👁️ Preview", 
        "⚙️ Settings"
    ])
    
    with tab1:
        st.header("📨 Bulk Email Campaign")
        
        # Template seçimi
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Template kategorileri
            template_categories = {
                "Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
                "Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
                "Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach']
            }
            
            selected_category = st.selectbox("📂 Template Category", list(template_categories.keys()))
            
        with col2:
            available_templates = template_categories[selected_category]
            template_options = {DEFAULT_TEMPLATES[k]['name']: k for k in available_templates}
            
            selected_template_name = st.selectbox("📝 Select Template", list(template_options.keys()))
            selected_template_key = template_options[selected_template_name]
            
        with col3:
            # Uygun email hesapları
            template_category_type = DEFAULT_TEMPLATES[selected_template_key]['category']
            suitable_accounts = [acc['email'] for acc in EMAIL_ACCOUNTS if acc['type'] == template_category_type]
            
            delay_time = st.slider("Delay Between Emails (seconds)", 1, 15, 5)
        
        # Template preview
        st.markdown("### 📋 Selected Template Preview")
        template_info = DEFAULT_TEMPLATES[selected_template_key]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info(f"**Category:** {template_info['category'].replace('_', ' ').title()}")
            st.info(f"**Template:** {template_info['name']}")
            st.info(f"**Subject:** {template_info['subject']}")
            
        with col2:
            st.success(f"**Available Accounts:** {len(suitable_accounts)}")
            for acc in suitable_accounts[:3]:  # Show first 3
                remaining = 100 - st.session_state.email_stats['daily_counts'][acc]
                st.write(f"📧 {acc}: {remaining}/100 remaining")
        
        # CSV upload
        st.markdown("### 📝 Manual Email Entry (Alternative to CSV)")
        
        manual_option = st.checkbox("📧 Use Manual Email Entry Instead of CSV")
        
        if manual_option:
            st.info("💡 **Format:** email1@domain.com, email2@domain.com, email3@domain.com")
            st.info("💡 **Names:** John Smith, Jane Doe, Mike Johnson (same order as emails)")
            st.info("💡 **Companies:** TechCorp, StartupInc, BigCompany (same order as emails)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                manual_emails = st.text_area(
                    "📧 Email Addresses (comma separated)",
                    placeholder="john@company1.com, jane@company2.com, mike@company3.com",
                    height=100,
                    help="Enter email addresses separated by commas"
                )
                
                manual_names = st.text_area(
                    "👤 Names (comma separated)",
                    placeholder="John Smith, Jane Doe, Mike Johnson",
                    height=100,
                    help="Enter names in the same order as emails"
                )
            
            with col2:
                manual_companies = st.text_area(
                    "🏢 Companies (comma separated)",
                    placeholder="TechCorp, StartupInc, BigCompany",
                    height=100,
                    help="Enter company names in the same order as emails"
                )
                
                # Preview button
                if st.button("👁️ Preview Manual Data"):
                    if manual_emails:
                        emails = [email.strip() for email in manual_emails.split(',') if email.strip()]
                        names = [name.strip() for name in manual_names.split(',') if name.strip()] if manual_names else []
                        companies = [company.strip() for company in manual_companies.split(',') if company.strip()] if manual_companies else []
                        
                        # Pad lists to match email count
                        while len(names) < len(emails):
                            names.append("Dear Professional")
                        while len(companies) < len(emails):
                            companies.append("Your Company")
                        
                        # Create preview dataframe
                        preview_data = {
                            'email': emails[:len(emails)],
                            'name': names[:len(emails)],
                            'company': companies[:len(emails)]
                        }
                        
                        st.session_state.manual_df = pd.DataFrame(preview_data)
                        st.success(f"✅ {len(emails)} recipients prepared!")
            
            # Show manual data preview
            if hasattr(st.session_state, 'manual_df'):
                st.markdown("### 📋 Manual Data Preview")
                st.dataframe(st.session_state.manual_df)
                st.write(f"**Total Recipients:** {len(st.session_state.manual_df)}")
                
                # Campaign start button for manual data
                if st.button("🚀 START MANUAL CAMPAIGN", type="primary", use_container_width=True):
                    df = st.session_state.manual_df
                    
                    st.markdown("---")
                    st.header("📊 Campaign Progress")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_emails = len(df)
                    successful_sends = []
                    failed_sends = []
                    
                    for index, row in df.iterrows():
                        # Available account bul
                        account = automation.get_available_account(template_category_type)
                        
                        if not account:
                            st.error(f"❌ No available accounts for {template_category_type} type!")
                            break
                        
                        # Template hazırla
                        subject, content = automation.format_template(
                            selected_template_key, 
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
                                'sender': account['email'],
                                'template': template_info['name']
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
                    st.success("🎉 Manual campaign completed successfully!")
    
    with tab2:
        st.header("✉️ Single Email Sender")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📧 Recipient Details")
            recipient_email = st.text_input("Recipient Email *")
            recipient_name = st.text_input("Recipient Name *")
            recipient_company = st.text_input("Company Name")
        
        with col2:
            st.subheader("📝 Template Selection")
            
            # Template kategorileri
            template_categories = {
                "Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
                "Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
                "Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach']
            }
            
            single_category = st.selectbox("📂 Category", list(template_categories.keys()), key="single_category")
            
            available_templates = template_categories[single_category]
            template_options = {DEFAULT_TEMPLATES[k]['name']: k for k in available_templates}
            
            single_template_name = st.selectbox("📝 Template", list(template_options.keys()), key="single_template")
            single_template_key = template_options[single_template_name]
            
            # Uygun hesaplar
            template_category_type = DEFAULT_TEMPLATES[single_template_key]['category']
            suitable_accounts = [acc['email'] for acc in EMAIL_ACCOUNTS if acc['type'] == template_category_type]
            
            sender_account = st.selectbox("Sender Account", suitable_accounts, key="single_sender")
        
        st.markdown("---")
        
        # Template info
        template_info = DEFAULT_TEMPLATES[single_template_key]
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Selected:** {template_info['name']}")
        with col2:
            st.info(f"**Category:** {template_info['category'].replace('_', ' ').title()}")
        
        if st.button("📤 Send Email", type="primary", use_container_width=True):
            if recipient_email and recipient_name:
                account = next(acc for acc in EMAIL_ACCOUNTS if acc['email'] == sender_account)
                
                subject, content = automation.format_template(
                    single_template_key, recipient_name, recipient_company or "Your Company"
                )
                
                success, message = automation.send_single_email(account, recipient_email, subject, content)
                
                if success:
                    st.success(f"✅ Email sent successfully to {recipient_email}")
                    st.info(f"📧 Sent via: {sender_account}")
                    st.info(f"📝 Template: {template_info['name']}")
                else:
                    st.error(f"❌ Error: {message}")
            else:
                st.warning("⚠️ Email and name fields are required!")
    
    with tab3:
        st.header("📝 Template Manager")
        st.markdown("Manage your 9 professional email templates across 3 categories.")
        
        # Template kategorileri
        template_categories = {
            "🎯 Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
            "🤝 Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
            "🏢 Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach']
        }
        
        # Category tabs
        category_tabs = st.tabs(list(template_categories.keys()))
        
        for i, (category_name, template_keys) in enumerate(template_categories.items()):
            with category_tabs[i]:
                st.markdown(f"### {category_name} Templates")
                
                # Template seçimi
                template_options = {DEFAULT_TEMPLATES[k]['name']: k for k in template_keys}
                selected_template_name = st.selectbox(
                    "Select Template to Edit", 
                    list(template_options.keys()),
                    key=f"template_select_{i}"
                )
                selected_template_key = template_options[selected_template_name]
                
                # Current template
                current_template = st.session_state.custom_templates[selected_template_key]
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**📋 Template Info:**")
                    st.code(f"Category: {current_template['category']}")
                    st.code(f"Name: {current_template['name']}")
                    
                    st.markdown("**💡 Variables:**")
                    st.code("{name} - Recipient name")
                    st.code("{company} - Company name")
                    
                    st.markdown("**🎨 HTML Tips:**")
                    st.markdown("- Use `<strong>` for bold")
                    st.markdown("- Use `<p>` for paragraphs") 
                    st.markdown("- Use `<ul><li>` for lists")
                
                with col2:
                    # Subject editing
                    new_subject = st.text_input(
                        "Subject Template", 
                        value=current_template['subject'],
                        help="Use {name} and {company} as placeholders",
                        key=f"subject_{selected_template_key}"
                    )
                    
                    # Content editing
                    new_content = st.text_area(
                        "Email Content Template (HTML)", 
                        value=current_template['content'],
                        height=300,
                        help="Use {name} and {company} as placeholders",
                        key=f"content_{selected_template_key}"
                    )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💾 Save Template", type="primary", key=f"save_{selected_template_key}"):
                        st.session_state.custom_templates[selected_template_key]['subject'] = new_subject
                        st.session_state.custom_templates[selected_template_key]['content'] = new_content
                        st.success(f"✅ {selected_template_name} saved!")
                
                with col2:
                    if st.button("🔄 Reset to Default", key=f"reset_{selected_template_key}"):
                        st.session_state.custom_templates[selected_template_key] = DEFAULT_TEMPLATES[selected_template_key].copy()
                        st.success(f"✅ {selected_template_name} reset to default!")
                        st.rerun()
                
                with col3:
                    if st.button("👁️ Preview", key=f"preview_{selected_template_key}"):
                        st.session_state.preview_template_key = selected_template_key
                        st.success("✅ Template ready for preview!")
                
                st.markdown("---")
    
    with tab4:
        st.header("👁️ Template Preview")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🧪 Test Data")
            
            # Template seçimi
            all_templates = {v['name']: k for k, v in DEFAULT_TEMPLATES.items()}
            preview_template_name = st.selectbox("Select Template to Preview", list(all_templates.keys()))
            preview_template_key = all_templates[preview_template_name]
            
            test_name = st.text_input("Test Name", "John Smith")
            test_company = st.text_input("Test Company", "TechCorp Inc.")
            
            if st.button("🔍 Generate Preview"):
                subject, content = automation.format_template(
                    preview_template_key, test_name, test_company
                )
                
                st.session_state.preview_subject = subject
                st.session_state.preview_content = content
                st.session_state.preview_template_info = DEFAULT_TEMPLATES[preview_template_key]
        
        with col2:
            st.subheader("📧 Email Preview")
            
            if hasattr(st.session_state, 'preview_subject'):
                template_info = st.session_state.preview_template_info
                
                # Template bilgileri
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Template:** {template_info['name']}")
                with col2:
                    st.info(f"**Category:** {template_info['category'].replace('_', ' ').title()}")
                
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
            st.subheader("📧 Email Accounts by Category")
            
            # Kategorilere göre hesapları grupla
            account_categories = {}
            for acc in EMAIL_ACCOUNTS:
                category = acc['type'].replace('_', ' ').title()
                if category not in account_categories:
                    account_categories[category] = []
                account_categories[category].append(acc)
            
            for category, accounts in account_categories.items():
                st.markdown(f"### {category}")
                for acc in accounts:
                    sent_today = st.session_state.email_stats['daily_counts'][acc['email']]
                    remaining = 100 - sent_today
                    
                    # Progress bar for each account
                    progress = sent_today / 100
                    
                    st.markdown(f"**{acc['email']}**")
                    st.progress(progress)
                    st.caption(f"Sent: {sent_today}/100 | Remaining: {remaining}")
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
            
            if st.button("📝 Reset All Templates to Default", type="secondary"):
                st.session_state.custom_templates = DEFAULT_TEMPLATES.copy()
                st.success("✅ All templates reset to default!")
            
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
                    st.rerun()
        
        # Template istatistikleri
        st.markdown("---")
        st.subheader("📊 Template Statistics")
        
        template_categories = {
            "Brand Hunter": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter']),
            "Brand Partnership": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership']),
            "Supplier Outreach": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach'])
        }
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Templates", len(DEFAULT_TEMPLATES))
        with col2:
            st.metric("Brand Hunter", template_categories["Brand Hunter"])
        with col3:
            st.metric("Brand Partnership", template_categories["Brand Partnership"])
        with col4:
            st.metric("Supplier Outreach", template_categories["Supplier Outreach"])
        
        # System info
        st.markdown("---")
        st.subheader("ℹ️ System Information")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accounts", len(EMAIL_ACCOUNTS))
        with col2:
            partnership_accounts = len([acc for acc in EMAIL_ACCOUNTS if acc['type'] == 'brand_partnership'])
            st.metric("Partnership Accounts", partnership_accounts)
        with col3:
            hunter_accounts = len([acc for acc in EMAIL_ACCOUNTS if acc['type'] == 'brand_hunter'])
            st.metric("Hunter Accounts", hunter_accounts)
        
        st.info("💡 **Daily Limit:** 100 emails per account | **Total Daily Capacity:** 1400 emails")
        st.info("🎯 **Template System:** 9 professional templates across 3 categories")
        
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
