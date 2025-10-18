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
    {'email': 'partnerships@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'business@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'collaborations@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'deals@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'marketing@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'etsy_customer', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'partnership@tahidem.com', 'password': 'GM8+h!M>An5', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'amazonpartnership@tahidem.com', 'password': '5V7SOWq:V&zQ', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'partnershipamazon@tahidem.com', 'password': 'u&17]ukQ', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'exclusivebrand@tahidem.com', 'password': '5M?$Kz^m', 'type': 'brand_partnership', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'outreach@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_hunter', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'team@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'brand_hunter', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'hello@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'etsy_customer', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'connect@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'growth@tahidem.com', 'password': '8JCQaK/;L$w', 'type': 'supplier_outreach', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'soulminecraft@tahidem.com', 'password': 'lxB6LJ/u=L0', 'type': 'etsy_customer', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    # 🎃 PIONDE HALLOWEEN HESAPLARI
    {'email': 'pionde@tahidem.com', 'password': 'kY]0AOKhiD', 'type': 'pionde_halloween', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465},
    {'email': 'piondediscount@tahidem.com', 'password': 'Bw^98ft[:3qW', 'type': 'pionde_halloween', 'sent_today': 0, 'smtp_server': 'smtp.hostinger.com', 'smtp_port': 465}
]

# 🎯 YENİ TEMPLATE SİSTEMİ - HALLOWEEN ÖZEL KAMPANYA DAHİL
DEFAULT_TEMPLATES = {
    # 🎃 PIONDE HALLOWEEN TEMPLATES
    "pionde_halloween_1": {
        "name": "Pionde Halloween Special - Spooky Savings",
        "category": "pionde_halloween",
        "subject": "🎃 BOO! Halloween Special - 40% OFF Everything at Pionde! 👻",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background: #1a1a1a;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff;">
            
            <!-- Halloween Header -->
            <div style="background: linear-gradient(135deg, #ff6b35 0%, #ff4500 100%); padding: 40px 30px; text-align: center; color: white; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><text y=\"50\" font-size=\"40\">🎃👻🕷️🦇</text></svg>'); opacity: 0.1; background-repeat: repeat;"></div>
                <div style="position: relative; z-index: 1;">
                    <h1 style="margin: 0; font-size: 36px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎃 PIONDE 🎃</h1>
                    <p style="margin: 10px 0 0 0; font-size: 22px; opacity: 0.95;">HALLOWEEN SPOOKTACULAR SALE!</p>
                    <div style="margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px; display: inline-block;">
                        <p style="margin: 0; font-size: 48px; font-weight: bold; letter-spacing: 3px;">40% OFF</p>
                        <p style="margin: 5px 0 0 0; font-size: 16px;">EVERYTHING IN STORE!</p>
                    </div>
                </div>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px; background: #fff;">
                <h2 style="color: #ff4500; font-size: 28px; margin-bottom: 20px; text-align: center;">👻 BOO! Hello {name}! 🎃</h2>
                
                <p style="font-size: 18px; margin-bottom: 25px; color: #333; text-align: center; line-height: 1.8;">
                    <strong>Halloween is here, and we've got a SPOOKY surprise for you!</strong><br>
                    Get ready for the most FRIGHTFULLY GOOD deals of the year! 🕷️
                </p>
                
                <!-- Halloween Offer Box -->
                <div style="background: linear-gradient(135deg, #ff6b35 0%, #ff4500 100%); padding: 35px; border-radius: 15px; margin: 30px 0; color: white; text-align: center; box-shadow: 0 10px 30px rgba(255,69,0,0.3);">
                    <h3 style="margin-top: 0; font-size: 32px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎃 HALLOWEEN MEGA SALE 🎃</h3>
                    <div style="background: rgba(255,255,255,0.2); padding: 25px; border-radius: 12px; margin: 25px 0; backdrop-filter: blur(10px);">
                        <h2 style="margin: 0; font-size: 56px; font-weight: bold; letter-spacing: 2px; text-shadow: 3px 3px 6px rgba(0,0,0,0.4);">40% OFF</h2>
                        <p style="margin: 15px 0 10px 0; font-size: 22px; font-weight: bold;">USE CODE:</p>
                        <div style="background: #fff; color: #ff4500; padding: 15px 30px; border-radius: 8px; display: inline-block; font-size: 28px; font-weight: bold; letter-spacing: 3px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                            HALLOWEEN40
                        </div>
                    </div>
                    <p style="margin: 20px 0; font-size: 18px; line-height: 1.6;">
                        🕷️ <strong>Valid:</strong> October 25-31, 2024<br>
                        👻 <strong>On:</strong> ALL Products - No Exclusions!<br>
                        🦇 <strong>Free Shipping:</strong> Orders over $50
                    </p>
                </div>
                
                <!-- Why Shop This Halloween -->
                <div style="background: #fff5e6; padding: 30px; border-radius: 12px; margin: 30px 0; border: 3px dashed #ff6b35;">
                    <h3 style="color: #ff4500; margin-top: 0; font-size: 24px; text-align: center;">🎃 Why Shop Pionde This Halloween? 🎃</h3>
                    <div style="display: grid; gap: 20px; margin: 25px 0;">
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6b35; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff4500; margin: 0 0 10px 0; font-size: 18px;">👻 Spooktacular Savings</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">40% OFF everything - our biggest discount ever!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff8c00; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff4500; margin: 0 0 10px 0; font-size: 18px;">🕷️ Premium Quality</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Handcrafted items with attention to every detail</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6347; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff4500; margin: 0 0 10px 0; font-size: 18px;">🦇 Fast Delivery</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Free shipping on orders over $50 - arrives before Halloween!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4500; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff4500; margin: 0 0 10px 0; font-size: 18px;">🎃 Perfect Gifts</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Unique items perfect for Halloween gifting!</p>
                        </div>
                    </div>
                </div>
                
                <!-- Popular Categories -->
                <div style="background: #f8f9fa; padding: 30px; border-radius: 12px; margin: 30px 0;">
                    <h3 style="color: #ff4500; margin-top: 0; font-size: 24px; text-align: center;">🛍️ Popular Halloween Categories 🛍️</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 20px; margin: 25px 0; text-align: center;">
                        <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <div style="font-size: 40px; margin-bottom: 10px;">🎃</div>
                            <h4 style="margin: 0; color: #333; font-size: 16px;">Halloween Decor</h4>
                        </div>
                        <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <div style="font-size: 40px; margin-bottom: 10px;">👻</div>
                            <h4 style="margin: 0; color: #333; font-size: 16px;">Spooky Gifts</h4>
                        </div>
                        <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <div style="font-size: 40px; margin-bottom: 10px;">🕷️</div>
                            <h4 style="margin: 0; color: #333; font-size: 16px;">Party Supplies</h4>
                        </div>
                        <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <div style="font-size: 40px; margin-bottom: 10px;">🦇</div>
                            <h4 style="margin: 0; color: #333; font-size: 16px;">Costumes</h4>
                        </div>
                    </div>
                </div>
                
                <!-- Urgency Message -->
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 30px; border-radius: 12px; margin: 30px 0; color: white; text-align: center; border: 3px solid #ff4500;">
                    <h3 style="margin-top: 0; font-size: 26px; color: #ff6b35;">⏰ LIMITED TIME ONLY! ⏰</h3>
                    <p style="margin: 20px 0; font-size: 18px; line-height: 1.8;">
                        This SPOOKTACULAR sale ends on <strong style="color: #ff6b35;">October 31st at midnight!</strong><br>
                        Don't let these BOO-tiful deals slip away! 👻<br>
                        <strong style="font-size: 22px; color: #ff4500;">Shop NOW before it's too late!</strong>
                    </p>
                </div>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="https://www.etsy.com/shop/Pionde" style="background: linear-gradient(135deg, #ff6b35 0%, #ff4500 100%); color: white; padding: 20px 50px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 20px; display: inline-block; box-shadow: 0 10px 30px rgba(255,69,0,0.4); transition: all 0.3s; text-transform: uppercase; letter-spacing: 2px;">
                        🎃 SHOP HALLOWEEN SALE NOW 🎃
                    </a>
                </div>
                
                <!-- Social Proof -->
                <div style="background: #fff5e6; padding: 25px; border-radius: 12px; margin: 30px 0; text-align: center; border: 2px solid #ff6b35;">
                    <p style="color: #ff4500; margin: 10px 0; font-size: 18px; font-weight: bold;">
                        "Best Halloween deals I've found! Quality products and amazing customer service!" 🎃
                    </p>
                    <p style="color: #666; margin: 10px 0; font-size: 14px;">
                        - Sarah M., Happy Halloween Shopper
                    </p>
                    <p style="color: #ff4500; margin: 20px 0; font-size: 16px; font-weight: bold;">
                        ⭐⭐⭐⭐⭐ Join 5,000+ Happy Customers This Halloween!
                    </p>
                </div>
                
                <!-- Thank You -->
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-size: 20px; color: #333; margin: 15px 0; line-height: 1.6;">
                        Thank you for being part of the <strong style="color: #ff4500;">Pionde family!</strong>
                    </p>
                    <p style="font-size: 22px; color: #ff4500; font-weight: bold; margin: 15px 0;">
                        Have a SPOOKTACULAR Halloween! 🎃👻
                    </p>
                    <p style="font-size: 32px; margin: 20px 0;">🎃🕷️👻🦇🕸️</p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #1a1a1a; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #ff6b35; font-weight: bold; font-size: 18px;">🎃 PIONDE - Your Halloween Headquarters 🎃</p>
                <p style="margin: 10px 0; opacity: 0.9;">📧 pionde@tahidem.com</p>
                <p style="margin: 10px 0; opacity: 0.9;">
                    🌐 <a href="https://www.etsy.com/shop/Pionde" style="color: #ff6b35; text-decoration: none;">Visit Our Etsy Shop</a>
                </p>
                <p style="margin: 15px 0; font-size: 14px; opacity: 0.7;">
                    Use code <strong style="color: #ff6b35;">HALLOWEEN40</strong> at checkout for 40% OFF!
                </p>
            </div>
        </div>
        </body></html>
        """
    },

    "pionde_halloween_2": {
        "name": "Pionde Halloween - Last Chance Alert",
        "category": "pionde_halloween",
        "subject": "⚠️ LAST CHANCE! Halloween Sale Ending Soon - 40% OFF at Pionde! 🎃",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background: #1a1a1a;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff;">
            
            <!-- Urgent Header -->
            <div style="background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%); padding: 40px 30px; text-align: center; color: white; position: relative;">
                <div style="position: absolute; top: 10px; right: 20px; background: #ffff00; color: #dc143c; padding: 8px 20px; border-radius: 25px; font-size: 14px; font-weight: bold; animation: pulse 1.5s infinite;">
                    ⚠️ URGENT
                </div>
                <h1 style="margin: 0; font-size: 38px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">⏰ LAST CHANCE ⏰</h1>
                <p style="margin: 15px 0; font-size: 24px; opacity: 0.95;">Halloween Sale Ending TONIGHT!</p>
                <div style="margin: 25px 0; padding: 20px; background: rgba(255,255,255,0.15); border-radius: 12px; display: inline-block;">
                    <p style="margin: 0; font-size: 52px; font-weight: bold; letter-spacing: 3px;">40% OFF</p>
                    <p style="margin: 10px 0 0 0; font-size: 18px;">Ends at MIDNIGHT!</p>
                </div>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px; background: #fff;">
                <h2 style="color: #dc143c; font-size: 30px; margin-bottom: 20px; text-align: center;">🚨 Don't Miss Out, {name}! 🚨</h2>
                
                <p style="font-size: 19px; margin-bottom: 25px; color: #333; text-align: center; line-height: 1.8;">
                    <strong>This is your FINAL WARNING!</strong><br>
                    Our biggest Halloween sale of the year ends <strong style="color: #dc143c;">TONIGHT at MIDNIGHT!</strong> 🎃
                </p>
                
                <!-- Countdown Timer Visual -->
                <div style="background: linear-gradient(135deg, #ff6b35 0%, #ff4500 100%); padding: 35px; border-radius: 15px; margin: 30px 0; color: white; text-align: center; box-shadow: 0 10px 30px rgba(220,20,60,0.4);">
                    <h3 style="margin-top: 0; font-size: 28px;">⏰ TIME IS RUNNING OUT! ⏰</h3>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 25px 0;">
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px;">
                            <div style="font-size: 36px; font-weight: bold;">12</div>
                            <div style="font-size: 14px; opacity: 0.9;">HOURS</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px;">
                            <div style="font-size: 36px; font-weight: bold;">30</div>
                            <div style="font-size: 14px; opacity: 0.9;">MINUTES</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px;">
                            <div style="font-size: 36px; font-weight: bold;">45</div>
                            <div style="font-size: 14px; opacity: 0.9;">SECONDS</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px;">
                            <div style="font-size: 36px; font-weight: bold;">🎃</div>
                            <div style="font-size: 14px; opacity: 0.9;">LEFT!</div>
                        </div>
                    </div>
                    <div style="background: #fff; color: #ff4500; padding: 18px 35px; border-radius: 10px; display: inline-block; font-size: 30px; font-weight: bold; letter-spacing: 3px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); margin-top: 20px;">
                        HALLOWEEN40
                    </div>
                </div>
                
                <!-- What You're Missing -->
                <div style="background: #fff5e6; padding: 30px; border-radius: 12px; margin: 30px 0; border: 3px solid #dc143c;">
                    <h3 style="color: #dc143c; margin-top: 0; font-size: 24px; text-align: center;">😱 What You're About to MISS! 😱</h3>
                    <div style="display: grid; gap: 20px; margin: 25px 0;">
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #dc143c; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #dc143c; margin: 0 0 10px 0; font-size: 18px;">💰 40% OFF Everything</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Our BIGGEST discount ever - won't see this again until next year!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4500; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #dc143c; margin: 0 0 10px 0; font-size: 18px;">🚚 FREE Shipping</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Free delivery on orders over $50 - save even more!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6b35; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #dc143c; margin: 0 0 10px 0; font-size: 18px;">🎁 Exclusive Items</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Limited edition Halloween items - once they're gone, they're GONE!</p>
                        </div>
                    </div>
                </div>
                
                <!-- Customer Testimonials -->
                <div style="background: #f8f9fa; padding: 30px; border-radius: 12px; margin: 30px 0;">
                    <h3 style="color: #ff4500; margin-top: 0; font-size: 22px; text-align: center;">💬 What Our Customers Are Saying 💬</h3>
                    <div style="display: grid; gap: 15px; margin: 20px 0;">
                        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <p style="margin: 0 0 10px 0; color: #333; font-style: italic;">"Just ordered! Can't believe these prices! 🎃"</p>
                            <p style="margin: 0; color: #ff4500; font-weight: bold;">- Jessica T.</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <p style="margin: 0 0 10px 0; color: #333; font-style: italic;">"Best Halloween shopping experience ever! 👻"</p>
                            <p style="margin: 0; color: #ff4500; font-weight: bold;">- Michael R.</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <p style="margin: 0 0 10px 0; color: #333; font-style: italic;">"40% off is INSANE! Already placed 3 orders! 🕷️"</p>
                            <p style="margin: 0; color: #ff4500; font-weight: bold;">- Amanda K.</p>
                        </div>
                    </div>
                </div>
                
                <!-- Final Warning -->
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 35px; border-radius: 12px; margin: 30px 0; color: white; text-align: center; border: 4px solid #dc143c;">
                    <h3 style="margin-top: 0; font-size: 32px; color: #ff6b35;">🚨 FINAL WARNING! 🚨</h3>
                    <p style="margin: 20px 0; font-size: 20px; line-height: 1.8;">
                        After <strong style="color: #dc143c;">MIDNIGHT TONIGHT</strong>, prices return to normal!<br>
                        This is your <strong style="color: #ff6b35;">LAST CHANCE</strong> to save 40%!<br>
                        <strong style="font-size: 24px; color: #ff4500;">Don't have regrets tomorrow!</strong>
                    </p>
                </div>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="https://www.etsy.com/shop/Pionde" style="background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%); color: white; padding: 22px 55px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 22px; display: inline-block; box-shadow: 0 10px 30px rgba(220,20,60,0.5); transition: all 0.3s; text-transform: uppercase; letter-spacing: 2px; animation: pulse 2s infinite;">
                        🎃 SHOP NOW BEFORE IT'S TOO LATE! 🎃
                    </a>
                    <p style="margin: 20px 0; font-size: 16px; color: #dc143c; font-weight: bold;">
                        ⏰ Sale ends at MIDNIGHT - Don't miss out!
                    </p>
                </div>
                
                <!-- Stock Warning -->
                <div style="background: #fff5e6; padding: 25px; border-radius: 12px; margin: 30px 0; text-align: center; border: 2px dashed #ff4500;">
                    <p style="color: #dc143c; margin: 10px 0; font-size: 18px; font-weight: bold;">
                        ⚠️ STOCK WARNING: Many items are selling out FAST!
                    </p>
                    <p style="color: #666; margin: 10px 0; font-size: 16px;">
                        Over 500 orders placed in the last 24 hours!<br>
                        Don't wait - secure your favorites NOW!
                    </p>
                </div>
                
                <!-- Thank You -->
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-size: 20px; color: #333; margin: 15px 0; line-height: 1.6;">
                        This is your <strong style="color: #dc143c;">LAST CHANCE</strong> to save BIG!
                    </p>
                    <p style="font-size: 22px; color: #ff4500; font-weight: bold; margin: 15px 0;">
                        See you at checkout! 🎃👻
                    </p>
                    <p style="font-size: 32px; margin: 20px 0;">⏰🎃🚨</p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #1a1a1a; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #dc143c; font-weight: bold; font-size: 18px;">🎃 PIONDE - Last Chance for Halloween Savings! 🎃</p>
                <p style="margin: 10px 0; opacity: 0.9;">📧 pionde@tahidem.com</p>
                <p style="margin: 10px 0; opacity: 0.9;">
                    🌐 <a href="https://www.etsy.com/shop/Pionde" style="color: #ff6b35; text-decoration: none;">Visit Our Etsy Shop</a>
                </p>
                <p style="margin: 15px 0; font-size: 16px; opacity: 0.9; color: #ff6b35;">
                    Use code <strong>HALLOWEEN40</strong> - Ends TONIGHT at MIDNIGHT!
                </p>
            </div>
        </div>
        </body></html>
        """
    },

    "pionde_halloween_3": {
        "name": "Pionde Halloween - Exclusive VIP Offer",
        "category": "pionde_halloween",
        "subject": "🎃 VIP EXCLUSIVE: Extra 10% OFF Halloween Sale at Pionde! (50% Total!) 👻",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background: #1a1a1a;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff;">
            
            <!-- VIP Header -->
            <div style="background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%); padding: 40px 30px; text-align: center; color: #1a1a1a; position: relative;">
                <div style="position: absolute; top: 10px; right: 20px; background: #1a1a1a; color: #ffd700; padding: 8px 20px; border-radius: 25px; font-size: 12px; font-weight: bold; border: 2px solid #ffd700;">
                    👑 VIP ONLY
                </div>
                <h1 style="margin: 0; font-size: 36px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">👑 VIP EXCLUSIVE 👑</h1>
                <p style="margin: 15px 0; font-size: 22px; opacity: 0.95;">Special Halloween Offer Just For You!</p>
                <div style="margin: 25px 0; padding: 20px; background: rgba(0,0,0,0.1); border-radius: 12px; display: inline-block;">
                    <p style="margin: 0; font-size: 48px; font-weight: bold; letter-spacing: 3px; color: #dc143c;">50% OFF</p>
                    <p style="margin: 10px 0 0 0; font-size: 16px;">40% + Extra 10% VIP Bonus!</p>
                </div>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px; background: #fff;">
                <h2 style="color: #ffd700; font-size: 28px; margin-bottom: 20px; text-align: center;">🌟 Hello VIP Customer {name}! 🌟</h2>
                
                <p style="font-size: 18px; margin-bottom: 25px; color: #333; text-align: center; line-height: 1.8;">
                    As one of our <strong style="color: #ffd700;">most valued customers</strong>, we're giving you an<br>
                    <strong style="color: #dc143c; font-size: 22px;">EXCLUSIVE EXTRA 10% OFF</strong> on top of our Halloween sale! 🎃
                </p>
                
                <!-- VIP Offer Box -->
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 35px; border-radius: 15px; margin: 30px 0; color: white; text-align: center; box-shadow: 0 10px 30px rgba(255,215,0,0.3); border: 3px solid #ffd700;">
                    <h3 style="margin-top: 0; font-size: 28px; color: #ffd700;">👑 YOUR VIP HALLOWEEN PACKAGE 👑</h3>
                    
                    <div style="display: grid; gap: 20px; margin: 25px 0;">
                        <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 10px; border: 2px solid #ffd700;">
                            <h4 style="color: #ffd700; margin: 0 0 10px 0; font-size: 20px;">🎃 Base Halloween Sale</h4>
                            <p style="margin: 0; font-size: 32px; font-weight: bold; color: #ff6b35;">40% OFF</p>
                        </div>
                        <div style="font-size: 32px; color: #ffd700;">+</div>
                        <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 10px; border: 2px solid #ffd700;">
                            <h4 style="color: #ffd700; margin: 0 0 10px 0; font-size: 20px;">👑 VIP Exclusive Bonus</h4>
                            <p style="margin: 0; font-size: 32px; font-weight: bold; color: #dc143c;">EXTRA 10% OFF</p>
                        </div>
                        <div style="font-size: 32px; color: #ffd700;">=</div>
                        <div style="background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%); padding: 25px; border-radius: 10px;">
                            <h4 style="color: #1a1a1a; margin: 0 0 10px 0; font-size: 22px;">💎 TOTAL VIP SAVINGS</h4>
                            <p style="margin: 0; font-size: 48px; font-weight: bold; color: #dc143c; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">50% OFF!</p>
                        </div>
                    </div>
                    
                    <div style="background: #fff; color: #1a1a1a; padding: 20px 35px; border-radius: 10px; display: inline-block; margin-top: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                        <p style="margin: 0 0 10px 0; font-size: 14px; color: #666;">Your VIP Code:</p>
                        <p style="margin: 0; font-size: 32px; font-weight: bold; letter-spacing: 3px; color: #ffd700;">VIPHALLOWEEN</p>
                    </div>
                </div>
                
                <!-- VIP Benefits -->
                <div style="background: #fff5e6; padding: 30px; border-radius: 12px; margin: 30px 0; border: 3px solid #ffd700;">
                    <h3 style="color: #ff8c00; margin-top: 0; font-size: 24px; text-align: center;">👑 Your VIP Benefits 👑</h3>
                    <div style="display: grid; gap: 20px; margin: 25px 0;">
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ffd700; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff8c00; margin: 0 0 10px 0; font-size: 18px;">💰 Maximum Savings</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">50% OFF - the biggest discount we've EVER offered!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff8c00; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff8c00; margin: 0 0 10px 0; font-size: 18px;">🚚 FREE Priority Shipping</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Free expedited delivery on ALL orders - no minimum!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #dc143c; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff8c00; margin: 0 0 10px 0; font-size: 18px;">🎁 Exclusive Gift</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Free Halloween surprise gift with every VIP order!</p>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6b35; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                            <h4 style="color: #ff8c00; margin: 0 0 10px 0; font-size: 18px;">⚡ Priority Processing</h4>
                            <p style="margin: 0; color: #555; font-size: 15px;">Your orders are processed first - guaranteed fast delivery!</p>
                        </div>
                    </div>
                </div>
                
                <!-- Why You're VIP -->
                <div style="background: #f8f9fa; padding: 30px; border-radius: 12px; margin: 30px 0;">
                    <h3 style="color: #ffd700; margin-top: 0; font-size: 22px; text-align: center;">🌟 Why You Received This VIP Offer 🌟</h3>
                    <p style="text-align: center; color: #555; font-size: 16px; line-height: 1.8; margin: 20px 0;">
                        You're one of our <strong>most loyal customers</strong>, and we wanted to show our appreciation!<br>
                        This exclusive 50% OFF offer is our way of saying <strong style="color: #ffd700;">THANK YOU</strong> for your continued support.<br>
                        <strong style="color: #dc143c;">This offer is not available to the general public!</strong>
                    </p>
                </div>
                
                <!-- Urgency -->
                <div style="background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%); padding: 30px; border-radius: 12px; margin: 30px 0; color: white; text-align: center; border: 3px solid #ffd700;">
                    <h3 style="margin-top: 0; font-size: 26px; color: #ffd700;">⏰ VIP EXCLUSIVE - LIMITED TIME! ⏰</h3>
                    <p style="margin: 20px 0; font-size: 18px; line-height: 1.8;">
                        This <strong style="color: #ffd700;">VIP 50% OFF offer</strong> is valid for<br>
                        <strong style="font-size: 24px; color: #ffd700;">48 HOURS ONLY!</strong><br>
                        Don't miss this exclusive opportunity!
                    </p>
                </div>
                
                <!-- How to Redeem -->
                <div style="background: #fff5e6; padding: 30px; border-radius: 12px; margin: 30px 0; border: 2px dashed #ffd700;">
                    <h3 style="color: #ff8c00; margin-top: 0; font-size: 22px; text-align: center;">📝 How to Redeem Your VIP Offer 📝</h3>
                    <div style="display: grid; gap: 15px; margin: 20px 0;">
                        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ffd700;">
                            <strong style="color: #ff8c00;">Step 1:</strong> Click the button below to visit our shop
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ff8c00;">
                            <strong style="color: #ff8c00;">Step 2:</strong> Add your favorite items to cart
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #dc143c;">
                            <strong style="color: #ff8c00;">Step 3:</strong> Enter code <strong style="color: #ffd700;">VIPHALLOWEEN</strong> at checkout
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ff6b35;">
                            <strong style="color: #ff8c00;">Step 4:</strong> Enjoy your 50% savings + FREE shipping!
                        </div>
                    </div>
                </div>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="https://www.etsy.com/shop/Pionde" style="background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%); color: #1a1a1a; padding: 22px 55px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 22px; display: inline-block; box-shadow: 0 10px 30px rgba(255,215,0,0.5); transition: all 0.3s; text-transform: uppercase; letter-spacing: 2px; border: 3px solid #1a1a1a;">
                        👑 CLAIM YOUR VIP 50% OFF NOW! 👑
                    </a>
                    <p style="margin: 20px 0; font-size: 16px; color: #dc143c; font-weight: bold;">
                        🌟 Exclusive VIP offer - Not available to public!
                    </p>
                </div>
                
                <!-- VIP Testimonial -->
                <div style="background: #f8f9fa; padding: 25px; border-radius: 12px; margin: 30px 0; text-align: center; border: 2px solid #ffd700;">
                    <p style="color: #ff8c00; margin: 10px 0; font-size: 18px; font-weight: bold;">
                        "I can't believe I got 50% off! Being a VIP customer is amazing!" 👑
                    </p>
                    <p style="color: #666; margin: 10px 0; font-size: 14px;">
                        - Rachel S., VIP Customer
                    </p>
                    <p style="color: #ffd700; margin: 20px 0; font-size: 16px; font-weight: bold;">
                        ⭐⭐⭐⭐⭐ Join Our VIP Family!
                    </p>
                </div>
                
                <!-- Thank You -->
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-size: 20px; color: #333; margin: 15px 0; line-height: 1.6;">
                        Thank you for being a <strong style="color: #ffd700;">VIP member</strong> of the Pionde family!
                    </p>
                    <p style="font-size: 22px; color: #ff8c00; font-weight: bold; margin: 15px 0;">
                        Enjoy your exclusive 50% OFF! 🎃👑
                    </p>
                    <p style="font-size: 32px; margin: 20px 0;">👑🎃✨</p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #1a1a1a; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #ffd700; font-weight: bold; font-size: 18px;">👑 PIONDE VIP - Exclusive Halloween Offer 👑</p>
                <p style="margin: 10px 0; opacity: 0.9;">📧 pionde@tahidem.com</p>
                <p style="margin: 10px 0; opacity: 0.9;">
                    🌐 <a href="https://www.etsy.com/shop/Pionde" style="color: #ffd700; text-decoration: none;">Visit Our Etsy Shop</a>
                </p>
                <p style="margin: 15px 0; font-size: 16px; opacity: 0.9; color: #ffd700;">
                    VIP Code: <strong>VIPHALLOWEEN</strong> - 50% OFF Everything!
                </p>
            </div>
        </div>
        </body></html>
        """
    },

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
                <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">EIN: 35-2742119 | Sheridan, WY, USA</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 24px; margin-bottom: 20px;">Hello {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                My name is <strong>Onur Nakis</strong>, Owner of <strong>TAHIDEM LLC (EIN: 35-2742119)</strong>, based in Sheridan, WY, USA. We are establishing exclusive distribution partnerships with successful Amazon brands, and we want to work with experienced professionals in this field.
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
                        <p style="margin: 10px 0;"><strong>Proven profitability and growth trajectory</strong></p>
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
                <p style="margin: 5px 0; color: #667eea; font-weight: bold;">TAHIDEM LLC (EIN: 35-2742119)</p>
                <p style="margin: 5px 0; opacity: 0.8;">30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
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
            <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 40px 30px; text-align: center;
 color: white;">
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🎯 BRAND HUNTER POSITION</h1>
                <p style="margin: 10px 0 0  0; font-size: 16px; opacity: 0.9;">TAHIDEM LLC - Exclusive Opportunity</p>
                <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">EIN: 35-2742119 | Sheridan, WY, USA</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Dear {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                My name is <strong>Onur Nakis</strong>, Owner of <strong>TAHIDEM LLC (EIN: 35-2742119)</strong>, based in Sheridan, WY, USA. We want to work with you for the <strong>Brand Hunter position</strong> within TAHIDEM LLC.
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
                <p style="margin: 5px 0; color: #ff6b6b; font-weight: bold;">TAHIDEM LLC (EIN: 35-2742119)</p>
                <p style="margin: 5px 0; opacity: 0.8;">30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
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
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:business@tahidem.com" style="background: #ff6b6b; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Discuss Exclusive Distribution Partnership</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #ff6b6b; font-weight: bold;">TAHIDEM LLC (EIN: 35-2742119)</p>
                <p style="margin: 5px 0; opacity: 0.8;">30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">business@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },
    
    # 🏢 SUPPLIER OUTREACH TEMPLATES (Tedarikçi İletişimi)
    "supplier_outreach_4": {
        "name": "Wholesale Distribution Partnership",
        "category": "supplier_outreach",
        "subject": "Wholesale Distribution Partnership - {company} x TAHIDEM LLC - Million Dollar Opportunity",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 40px 30px; text-align: center; color: white; position: relative;">
                <div style="position: absolute; top: 15px; right: 20px; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 12px;">WHOLESALE DISTRIBUTOR</div>
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🏢 WHOLESALE DISTRIBUTION PARTNERSHIP</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">TAHIDEM LLC - Million Dollar Opportunity</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Hello {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                My name is <strong>Onur Nakis</strong>, Owner of <strong>TAHIDEM LLC (EIN: 35-2742119)</strong>, based in Sheridan, WY, USA. I am very interested in establishing a <strong>wholesale distribution partnership</strong> with <strong>{company}</strong> to scale your business through our million-dollar customer network.
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="mailto:connect@tahidem.com" style="background: #667eea; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Discuss Wholesale Partnership</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #667eea; font-weight: bold;">TAHIDEM LLC (EIN: 35-2742119)</p>
                <p style="margin: 5px 0; opacity: 0.8;">30 N Gould St Ste 24309, Sheridan, WY 82801, USA</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">connect@tahidem.com | https://tahidem.com/</p>
            </div>
        </div>
        </body></html>
        """
    },

    # 🛍️ ETSY CUSTOMER TEMPLATES (Etsy Müşteri Şablonları)
    "etsy_customer_1": {
        "name": "SoulMineCraft Weekend Special Offer",
        "category": "etsy_customer",
        "subject": "🧡 This Weekend Only - 60% OFF Your Custom 3D Portrait Keychain - SoulMineCraft",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #ff7b54 0%, #ff6b35 100%); padding: 40px 30px; text-align: center; color: white; position: relative;">
                <div style="position: absolute; top: 15px; right: 20px; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 12px;">WEEKEND SPECIAL</div>
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🎨 SoulMineCraft</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Custom 3D Portrait Keychains</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Hello from SoulMineCraft! 🧡</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                    <strong>This weekend is all about your story... :))</strong>
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="https://www.etsy.com/shop/SoulMineCraft" style="background: #ff7b54; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Shop Now - 60% OFF</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #ff7b54; font-weight: bold;">SoulMineCraft Team</p>
                <p style="margin: 5px 0; opacity: 0.8;">📧 soulminecraft@tahidem.com</p>
                <p style="margin: 10px 0 0 0; opacity: 0.8;">
                    <a href="https://www.etsy.com/shop/SoulMineCraft" style="color: #ff7b54; text-decoration: none;">Visit Our Etsy Shop</a>
                </p>
            </div>
        </div>
        </body></html>
        """
    },

    "etsy_customer_2": {
        "name": "SoulMineCraft Memory Collection - Alternative Offer",
        "category": "etsy_customer",
        "subject": "✨ Turn Your Precious Moments Into Art - Exclusive SoulMineCraft Collection",
        "content": """
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 100%); padding: 40px 30px; text-align: center; color: white; position: relative;">
                <div style="position: absolute; top: 15px; right: 20px; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 12px;">EXCLUSIVE COLLECTION</div>
                <h1 style="margin: 0; font-size: 28px; font-weight: bold;">✨ SoulMineCraft</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Where Memories Become Art</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #2c3e50; font-size: 22px; margin-bottom: 20px;">Dear {name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                    Every moment tells a story. Every memory deserves to be treasured.
                </p>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 40px 0;">
                    <a href="https://www.etsy.com/shop/SoulMineCraft" style="background: #88d8c0; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Create Your Memory</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #2c3e50; padding: 30px; text-align: center; color: white;">
                <p style="margin: 5px 0; color: #88d8c0; font-weight: bold;">SoulMineCraft Team</p>
                <p style="margin: 5px 0; opacity: 0.8;">📧 soulminecraft@tahidem.com</p>
                <p style="margin: 10px 0 0 0; opacity: 0.8;">
                    <a href="https://www.etsy.com/shop/SoulMineCraft" style="color: #88d8c0; text-decoration: none;">Visit Our Etsy Shop</a>
                </p>
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
                del st.session_state["password"]
            elif entered_hash == MASTER_PASSWORD_HASH:
                st.session_state["password_correct"] = True
                st.session_state["user_role"] = "master"
                del st.session_state["password"]
            else:
                st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
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
            # Tüm hesaplar için SSL kullan (Hostinger)
            server = smtplib.SMTP_SSL(sender_account['smtp_server'], sender_account['smtp_port'])
            server.login(sender_account['email'], sender_account['password'])
            
            msg = MIMEMultipart()
            msg['From'] = f"Pionde <{sender_account['email']}>" if 'pionde' in sender_account['email'] else f"Tahidem <{sender_account['email']}>"
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'html'))
            
            server.send_message(msg)
            server.quit()
            
            # Stats güncelle
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
        st.markdown("**Advanced Email Campaign Management System - 14 Professional Templates (Including 3 Halloween Specials)**")
    
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
                "🎃 Pionde Halloween": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'pionde_halloween'],
                "🎯 Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
                "🤝 Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
                "🏢 Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach'],
                "🛍️ Etsy Customer": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'etsy_customer']
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
            for acc in suitable_accounts[:3]:
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
                            names.append("Dear Customer")
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
                            row.get('name', 'Dear Customer'),
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
        
        else:
            # CSV Upload Section
            st.markdown("### 📁 CSV File Upload")
            uploaded_file = st.file_uploader(
                "Choose CSV file",
                type=['csv'],
                help="CSV should contain columns: email, name, company"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ CSV loaded successfully! {len(df)} recipients found.")
                    
                    # Show preview
                    st.markdown("### 📋 CSV Data Preview")
                    st.dataframe(df.head())
                    
                    # Validate columns
                    required_columns = ['email']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    
                    if missing_columns:
                        st.error(f"❌ Missing required columns: {missing_columns}")
                    else:
                        # Fill missing columns
                        if 'name' not in df.columns:
                            df['name'] = 'Dear Customer'
                        if 'company' not in df.columns:
                            df['company'] = 'Your Company'
                        
                        # Campaign start button for CSV
                        if st.button("🚀 START CSV CAMPAIGN", type="primary", use_container_width=True):
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
                                    row.get('name', 'Dear Customer'),
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
                            st.success("🎉 CSV campaign completed successfully!")
                
                except Exception as e:
                    st.error(f"❌ Error reading CSV: {str(e)}")
    
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
                "🎃 Pionde Halloween": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'pionde_halloween'],
                "🎯 Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
                "🤝 Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
                "🏢 Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach'],
                "🛍️ Etsy Customer": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'etsy_customer']
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
        st.markdown("Manage your 14 professional email templates across 5 categories (including 3 Halloween specials).")
        
        # Template kategorileri
        template_categories = {
            "🎃 Pionde Halloween": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'pionde_halloween'],
            "🎯 Brand Hunter": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter'],
            "🤝 Brand Partnership": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership'],
            "🏢 Supplier Outreach": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach'],
            "🛍️ Etsy Customer": [k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'etsy_customer']
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
                    st.caption(f"Sent: {sent_today}/100 | Remaining: {remaining} | SMTP: {acc['smtp_server']}")
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
            "Pionde Halloween": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'pionde_halloween']),
            "Brand Hunter": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_hunter']),
            "Brand Partnership": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'brand_partnership']),
            "Supplier Outreach": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'supplier_outreach']),
            "Etsy Customer": len([k for k, v in DEFAULT_TEMPLATES.items() if v['category'] == 'etsy_customer'])
        }
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🎃 Halloween", template_categories["Pionde Halloween"])
        with col2:
            st.metric("🎯 Brand Hunter", template_categories["Brand Hunter"])
        with col3:
            st.metric("🤝 Partnership", template_categories["Brand Partnership"])
        with col4:
            st.metric("🏢 Supplier", template_categories["Supplier Outreach"])
        with col5:
            st.metric("🛍️ Etsy", template_categories["Etsy Customer"])
        
        st.info(f"**Total Templates:** {len(DEFAULT_TEMPLATES)} professional email templates")
        
        # Email account summary
        st.markdown("---")
        st.subheader("📧 Email Account Summary")
        
        account_summary = []
        for acc in EMAIL_ACCOUNTS:
            account_summary.append({
                'Email': acc['email'],
                'Type': acc['type'].replace('_', ' ').title(),
                'SMTP Server': acc['smtp_server'],
                'Port': acc['smtp_port'],
                'Sent Today': st.session_state.email_stats['daily_counts'][acc['email']],
                'Remaining': 100 - st.session_state.email_stats['daily_counts'][acc['email']]
            })
        
        summary_df = pd.DataFrame(account_summary)
        st.dataframe(summary_df, use_container_width=True)
        
        # Export settings
        st.markdown("---")
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Statistics as CSV"):
                stats_data = {
                    'Metric': ['Total Sent', 'Successful', 'Failed', 'Success Rate'],
                    'Value': [
                        st.session_state.email_stats['successful'] + st.session_state.email_stats['failed'],
                        st.session_state.email_stats['successful'],
                        st.session_state.email_stats['failed'],
                        f"{(st.session_state.email_stats['successful'] / max(st.session_state.email_stats['successful'] + st.session_state.email_stats['failed'], 1)) * 100:.1f}%"
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                
                csv = stats_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Statistics CSV",
                    data=csv,
                    file_name=f"tahidem_email_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📥 Export Account Status as CSV"):
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Account Status CSV",
                    data=csv,
                    file_name=f"tahidem_account_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# Ana program akışı
def main():
    # Custom CSS
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .main {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
        .stSelectbox, .stTextInput, .stTextArea {
            border-radius: 8px;
        }
        .stInfo {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            border-radius: 8px;
        }
        .stSuccess {
            background-color: #e8f5e9;
            border-left: 4px solid #4caf50;
            border-radius: 8px;
        }
        .stWarning {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            border-radius: 8px;
        }
        .stError {
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            border-radius: 8px;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .sidebar .sidebar-content h1, 
        .sidebar .sidebar-content h2, 
        .sidebar .sidebar-content h3,
        .sidebar .sidebar-content p {
            color: white !important;
        }
        /* Animation for pulse effect */
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }
        /* Card style */
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        /* Gradient text */
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Şifre kontrolü
    if check_password():
        main_app()

if __name__ == "__main__":
    main()


            
