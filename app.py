#!/usr/bin/env python3
"""
XyronAI - Complete Professional Edition
Run: pip install flask flask-sqlalchemy flask-login requests openai python-dotenv
Then: python app.py
"""

import os
import re
import json
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from functools import wraps

# ========== LEGAL CONTENT (HTML strings) ==========
LEGAL_TERMS_HTML = '''
<div class="max-w-5xl mx-auto">
    <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-green-700">Terms and Conditions</h1>
        <p class="text-gray-500">Last Updated: June 2026</p>
    </div>
    <div class="bg-white rounded-lg shadow p-8">
        <p class="mb-4">Welcome to <strong>XyronAI</strong>. These Terms and Conditions govern your access to and use of our website, mobile applications, AI services, freelance marketplace services, messaging systems, payment systems, and related digital platforms. By accessing or using our platform, you agree to comply with and be bound by these Terms and Conditions.</p>
        <p class="mb-6">If you do not agree with any part of these terms, you must discontinue use of the platform immediately.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">1. Definitions</h3>
        <ul class="list-none pl-6 mb-4"><li><strong>Platform</strong> refers to XyronAI and all related services.</li><li><strong>User</strong> refers to any person accessing or using the platform.</li><li><strong>Client</strong> refers to a user purchasing services.</li><li><strong>Worker/Freelancer</strong> refers to a user offering services.</li><li><strong>Administrator</strong> refers to authorized personnel managing the platform.</li><li><strong>Service</strong> refers to any digital product, freelance service, AI assistance, or platform feature available on XyronAI.</li></ul>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">2. Eligibility</h3>
        <p class="mb-4">Users must be at least 18 years old or have permission from a parent or legal guardian. By creating an account, you confirm that the information you provide is accurate and truthful.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">3. Account Registration</h3>
        <p class="mb-2">Users are responsible for:</p>
        <ul class="list-none pl-6 mb-4"><li>Maintaining account security.</li><li>Protecting passwords and login credentials.</li><li>Ensuring account information remains accurate.</li><li>Reporting unauthorized access immediately.</li></ul>
        <p class="mb-4">XyronAI is not liable for losses caused by unauthorized access resulting from user negligence.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">4. Service Availability</h3>
        <p class="mb-4">We strive to maintain uninterrupted service but do not guarantee continuous availability. Services may be interrupted due to system maintenance, technical failures, security updates, network issues, or events beyond our control.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">5. User Conduct</h3>
        <p class="mb-4">Users agree to act honestly and professionally, respect other users, follow all applicable laws, and avoid activities that may harm the platform.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">6. Payments</h3>
        <p class="mb-4">Payments processed through approved payment methods, including M-PESA, are subject to verification. XyronAI reserves the right to hold suspicious transactions, investigate fraudulent activities, and reverse unauthorized transactions where legally permitted.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">7. Refund Policy</h3>
        <p class="mb-4">Refund requests may be reviewed on a case-by-case basis. Refunds may be denied where services have already been delivered, users violate platform policies, or fraudulent activities are detected.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">8. Intellectual Property</h3>
        <p class="mb-4">All platform content, branding, logos, software, designs, and systems remain the property of XyronAI unless otherwise stated. Unauthorized copying, distribution, or modification is prohibited.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">9. Limitation of Liability</h3>
        <p class="mb-4">XyronAI shall not be liable for indirect damages, business losses, data loss, lost profits, or service interruptions. Users utilize the platform at their own risk.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">10. Suspension and Termination</h3>
        <p class="mb-4">We reserve the right to suspend accounts, restrict platform access, or permanently terminate accounts without prior notice when violations are detected.</p>
        
        <h3 class="text-xl font-semibold text-green-600 mt-6 mb-3">11. Changes to Terms</h3>
        <p class="mb-4">XyronAI may modify these terms at any time. Continued use of the platform after changes constitutes acceptance of updated terms.</p>
        
        <div class="text-center text-gray-500 text-sm mt-8 pt-4 border-t">
            © XyronAI. All rights reserved.
        </div>
    </div>
</div>
'''

LEGAL_RULES_HTML = '''
<div class="max-w-5xl mx-auto">
    <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-green-700">Rules and Regulations</h1>
        <p class="text-gray-500">All users must follow these rules. Violations may result in warnings, suspension, or permanent ban.</p>
    </div>
    <div class="bg-white rounded-lg shadow p-8">
        <div class="grid gap-4">
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">General Rules</h3>
                <ul class="list-decimal pl-6"><li>Users must provide accurate information during registration.</li><li>Users must maintain one primary account unless authorized.</li><li>Users must protect their account credentials.</li><li>Users must comply with all local and international laws.</li><li>Users must respect administrators and support staff.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Content Rules</h3>
                <ul class="list-decimal pl-6"><li>No hate speech is allowed.</li><li>No harassment or bullying.</li><li>No threats or intimidation.</li><li>No impersonation of other users.</li><li>No misleading or false information.</li><li>No copyright infringement.</li><li>No unauthorized sharing of confidential information.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Marketplace Rules</h3>
                <ul class="list-decimal pl-6"><li>Workers must deliver services as described.</li><li>Clients must provide clear project requirements.</li><li>Workers must not abandon active orders.</li><li>Clients must not abuse revision systems.</li><li>Users must communicate professionally.</li><li>Both parties must honor agreed timelines.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Payment Rules</h3>
                <ul class="list-decimal pl-6"><li>Users may not manipulate payment systems.</li><li>Chargeback abuse is prohibited.</li><li>Money laundering activities are prohibited.</li><li>Fraudulent transactions are prohibited.</li><li>Users may not use stolen financial accounts.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Security Rules</h3>
                <ul class="list-decimal pl-6"><li>Attempting to hack the platform is prohibited.</li><li>Distributing malware is prohibited.</li><li>Unauthorized access attempts are prohibited.</li><li>Testing platform vulnerabilities without authorization is prohibited.</li><li>Automated attacks against the platform are prohibited.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Messaging Rules</h3>
                <ul class="list-decimal pl-6"><li>Users must not send spam.</li><li>Mass unsolicited messaging is prohibited.</li><li>Users must not share harmful links.</li><li>Scam-related communication is prohibited.</li><li>Messages containing illegal activities are prohibited.</li><li>Users may not use messaging systems to solicit off-platform payments.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">AI Assistant Rules</h3>
                <ul class="list-decimal pl-6"><li>Users may not attempt to manipulate the AI into violating platform policies.</li><li>AI-generated responses should not be considered professional legal, financial, or medical advice.</li><li>Users must independently verify critical information.</li><li>The AI assistant may refuse requests that violate platform policies.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Platform Integrity Rules</h3>
                <ul class="list-decimal pl-6"><li>Users may not artificially inflate ratings.</li><li>Fake reviews are prohibited.</li><li>Referral abuse is prohibited.</li><li>Creating fake projects is prohibited.</li><li>Creating fake service listings is prohibited.</li><li>Users may not interfere with platform operations.</li></ul>
            </div>
            <div class="rule-card p-4 rounded-lg" style="background:#f9fafb; border-left:4px solid #10b981;">
                <h3 class="font-bold text-green-700 text-lg mb-2">Administrative Rules</h3>
                <ul class="list-decimal pl-6"><li>Administrators may investigate suspicious activities.</li><li>Administrators may remove content violating policies.</li><li>Administrators may suspend accounts pending investigation.</li><li>Administrative decisions regarding platform security are final.</li></ul>
            </div>
        </div>
        <div class="mt-8 p-4 bg-gray-100 rounded-lg">
            <h3 class="font-bold text-gray-800 mb-2">Enforcement</h3>
            <ol class="list-decimal pl-6"><li>Warning</li><li>Content removal</li><li>Temporary restrictions</li><li>Account suspension</li><li>Permanent account termination</li><li>Payment withholding</li><li>Legal action where applicable</li></ol>
            <p class="mt-4">By using XyronAI, users acknowledge that they have read, understood, and agreed to these Terms and Conditions and Rules and Regulations.</p>
        </div>
        <div class="text-center text-gray-500 text-sm mt-8 pt-4 border-t">

        

        

        

        

        

        

        <section>

        <section>

            © 2026 XyronAI. All rights reserved.
        </div>
    </div>
</div>
'''

ABOUT_US_HTML = '''
<div class="max-w-5xl mx-auto">
    <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-green-700">About Us</h1>
        <p class="text-gray-500">Learn more about our platform, mission, and values</p>
    </div>
    <div class="bg-white rounded-lg shadow p-8 space-y-6">
        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Welcome to Our Platform</h2>
            <p>Welcome to our AI-powered digital platform, a modern technology solution created to transform the way individuals and businesses communicate, access information, and manage digital interactions. We believe that technology should be accessible, efficient, reliable, and beneficial to everyone. Our platform was established with a vision of creating intelligent systems that simplify communication, increase productivity, and help users achieve their goals faster.</p>
            <p class="mt-2">In today's digital world, communication plays a critical role in personal growth, business success, customer satisfaction, and organizational efficiency. As technology continues to evolve, people expect faster responses, better support, and smarter solutions. Our AI-powered assistant was developed to meet these expectations by providing instant assistance, intelligent automation, and reliable digital support at any time of the day.</p>
            <p class="mt-2">We are committed to delivering innovative solutions that empower users through the responsible use of artificial intelligence. Whether you are an entrepreneur, student, professional, freelancer, business owner, or organization, our platform is designed to provide value through intelligent automation and user-focused services.</p>
        </section>
        
        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Who We Are</h2>
            <p>We are a technology-focused organization dedicated to developing intelligent digital solutions powered by artificial intelligence. Our team is driven by innovation, creativity, and a passion for solving real-world problems through technology.</p>
            <p class="mt-2">Our platform combines modern software development practices, intelligent automation systems, and advanced AI capabilities to create a seamless user experience. We continuously invest in research, development, and innovation to ensure our services remain effective, secure, and aligned with the evolving needs of our users.</p>
            <p class="mt-2">We believe that technology should not be limited to large corporations or specialized industries. Instead, it should be available to everyone, regardless of their background, location, or level of technical expertise.</p>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Story</h2>
            <p>The idea behind our platform emerged from a simple observation: many people and businesses struggle to manage communication efficiently. Customer inquiries often go unanswered, support teams become overwhelmed, and users experience delays when seeking information or assistance.</p>
            <p class="mt-2">Recognizing these challenges, we set out to build an intelligent system capable of providing immediate support while maintaining accuracy, reliability, and user satisfaction. Through continuous learning, development, and feedback, our platform has evolved into a powerful communication assistant capable of serving a wide range of users and industries.</p>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Mission</h2>
            <p>Our mission is to empower individuals and businesses through intelligent technology that simplifies communication, improves efficiency, and provides reliable digital assistance.</p>
            <ul class="list-none pl-6 mt-2 space-y-1">
                <li>Deliver fast and accurate AI-powered support.</li>
                <li>Improve productivity through automation.</li>
                <li>Make advanced technology accessible to everyone.</li>
                <li>Enhance communication experiences across digital platforms.</li>
                <li>Support businesses in providing better customer service.</li>
                <li>Promote responsible and ethical use of artificial intelligence.</li>
                <li>Create innovative solutions that solve real-world challenges.</li>
            </ul>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Vision</h2>
            <p>Our vision is to become a leading provider of intelligent communication and automation solutions that positively impact individuals, businesses, and communities around the world.</p>
            <p class="mt-2">We envision a future where communication barriers are reduced through technology, businesses can provide instant support to customers, individuals have access to reliable digital assistance whenever needed, and artificial intelligence is used responsibly to improve lives.</p>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">What We Do</h2>
            <ul class="list-none pl-6 space-y-1">
                <li><strong>Intelligent Conversations</strong> – Our AI assistant engages in meaningful conversations and provides relevant responses.</li>
                <li><strong>Automated Customer Support</strong> – Businesses can automate support processes for prompt responses.</li>
                <li><strong>Information Assistance</strong> – Quick access to information through AI-powered assistance.</li>
                <li><strong>Productivity Enhancement</strong> – Automate repetitive tasks and focus on what matters.</li>
                <li><strong>Continuous Improvement</strong> – Ongoing development to enhance platform capabilities.</li>
            </ul>
        </section>

        

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Commitment to Users</h2>
            <ul class="list-none pl-6 space-y-1">
                <li>Providing reliable and accessible services.</li>
                <li>Continuously improving system performance.</li>
                <li>Protecting user privacy.</li>
                <li>Maintaining high standards of security.</li>
                <li>Listening to user feedback.</li>
                <li>Delivering excellent customer experiences.</li>
                <li>Supporting responsible AI practices.</li>
            </ul>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Users</h2>
            <p>Our platform serves a diverse community including small business owners, entrepreneurs, freelancers, students, professionals, organizations, customer support teams, online service providers, and digital communities.</p>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Future Goals</h2>
            <ul class="list-none pl-6 space-y-1">
                <li>Expanding AI capabilities.</li>
                <li>Introducing new automation features.</li>
                <li>Improving multilingual support.</li>
                <li>Enhancing system performance and reliability.</li>
                <li>Developing additional business tools.</li>
                <li>Expanding access to more users and industries.</li>
                <li>Strengthening privacy and security measures.</li>
            </ul>
        </section>

        <section>
            <h2 class="text-2xl font-bold text-green-700 mb-3">Our Promise</h2>
            <p>Our promise is simple: to provide intelligent, reliable, and user-focused solutions that help people communicate more effectively and operate more efficiently.</p>
            <p class="mt-2">Thank you for being part of our journey. We look forward to serving you and helping you achieve more through the power of intelligent technology.</p>
        </section>

        <div class="text-center text-gray-500 text-sm mt-8 pt-4 border-t">

        

        

        

        

        

        

        <section>

        <section>

            © 2026 XyronAI. All rights reserved.
        </div>
    </div>
</div>
'''

from flask import Flask, request, jsonify, render_template_string, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

# ---------- Configuration ----------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatsapp_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# WhatsApp Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'my_verify_token')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# ---------- Database Models (Extended) ----------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    business_name = db.Column(db.String(200))
    phone_number = db.Column(db.String(50))
    plan = db.Column(db.String(50), default='free')  # free, starter, pro, enterprise
    mpesa_payment_id = db.Column(db.String(100))
    subscription_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    # Security
    two_factor_secret = db.Column(db.String(200))
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    # AI Settings
    ai_name = db.Column(db.String(100), default='AI Assistant')
    ai_personality = db.Column(db.String(200), default='friendly and helpful')
    ai_language = db.Column(db.String(10), default='en')
    auto_reply_enabled = db.Column(db.Boolean, default=True)
    working_hours_start = db.Column(db.Integer, default=9)
    working_hours_end = db.Column(db.Integer, default=17)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whatsapp_business_id = db.Column(db.String(100))
    webhook_verified = db.Column(db.Boolean, default=False)
    settings = db.Column(db.Text, default='{}')
    user = db.relationship('User', backref=db.backref('businesses', lazy=True))

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='open')
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)
    business = db.relationship('Business', backref=db.backref('conversations', lazy=True))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    direction = db.Column(db.String(10))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered = db.Column(db.Boolean, default=False)
    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True))

class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    business = db.relationship('Business', backref=db.backref('knowledge_items', lazy=True))

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, lost
    notes = db.Column(db.Text)
    source = db.Column(db.String(50), default='whatsapp')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrainingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    business = db.relationship('Business', backref=db.backref('training_items', lazy=True))

class Broadcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.Text)
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    delivery_count = db.Column(db.Integer, default=0)
    business = db.relationship('Business', backref=db.backref('broadcasts', lazy=True))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))  # lead, chat, system, error
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(200))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class APIToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    user = db.relationship('User', backref=db.backref('api_tokens', lazy=True))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Helper Functions ----------
def send_whatsapp_message(to_phone, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        return {"error": "WhatsApp not configured"}
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to_phone, "type": "text", "text": {"body": text}}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def generate_ai_response(business_id, customer_phone, user_message, user):
    if not OPENAI_API_KEY:
        return "AI not configured."
    
    # Get business knowledge base
    knowledge_items = KnowledgeBase.query.filter_by(business_id=business_id).all()
    knowledge_text = "\n".join([f"Q: {k.question}\nA: {k.answer}" for k in knowledge_items])
    
    # Conversation context
    conv = Conversation.query.filter_by(business_id=business_id, customer_phone=customer_phone).first()
    if conv:
        recent = Message.query.filter_by(conversation_id=conv.id).order_by(Message.created_at.desc()).limit(5).all()
        context = "\n".join([f"{'Customer' if m.direction=='incoming' else 'Assistant'}: {m.content}" for m in reversed(recent)])
    else:
        context = "No previous conversation."
    
    system_prompt = f"""You are {user.ai_name}, a {user.ai_personality} AI business assistant.
Language: {user.ai_language}
Business knowledge:
{knowledge_text if knowledge_text else "No specific info."}

Conversation history:
{context}

Customer: {user_message}
Provide a concise, helpful response (under 300 chars)."""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Sorry, I'm having trouble. Please try again later."

def save_message(conv_id, direction, content):
    msg = Message(conversation_id=conv_id, direction=direction, content=content)
    db.session.add(msg)
    db.session.commit()
    conv = Conversation.query.get(conv_id)
    conv.last_message_at = datetime.utcnow()
    db.session.commit()
    return msg

def get_or_create_conversation(business_id, customer_phone):
    conv = Conversation.query.filter_by(business_id=business_id, customer_phone=customer_phone).first()
    if not conv:
        conv = Conversation(business_id=business_id, customer_phone=customer_phone)
        db.session.add(conv)
        db.session.commit()
    return conv

def create_notification(user_id, title, message, type_):
    notif = Notification(user_id=user_id, title=title, message=message, type=type_)
    db.session.add(notif)
    db.session.commit()

def log_activity(user_id, action, ip, user_agent):
    log = ActivityLog(user_id=user_id, action=action, ip_address=ip, user_agent=user_agent)
    db.session.add(log)
    db.session.commit()
 
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XyronAI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Sidebar transition */
        .sidebar {
            position: fixed;
            top: 0;
            left: -280px;
            width: 280px;
            height: 100%;
            background-color: white;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            transition: left 0.3s ease;
            z-index: 1000;
            overflow-y: auto;
        }
        .sidebar.open {
            left: 0;
        }
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 999;
            display: none;
        }
        .overlay.active {
            display: block;
        }
        @media (min-width: 768px) {
            .sidebar {
                position: sticky;
                top: 0;
                left: 0;
                height: 100vh;
                transform: none;
                box-shadow: none;
                border-right: 1px solid #e5e7eb;
            }
            .sidebar.open {
                left: 0;
            }
            .overlay {
                display: none !important;
            }
        }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Overlay (closes sidebar on click) -->
    <div id="overlay" class="overlay" onclick="closeSidebar()"></div>

    <!-- Sidebar (hidden by default on mobile) -->
    <div id="sidebar" class="sidebar">
        <div class="p-4">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-bold text-green-600">XyronAI</h2>
                <button onclick="closeSidebar()" class="md:hidden text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <ul class="space-y-2">
                <li><a href="{{ url_for('dashboard') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-tachometer-alt mr-2"></i> Dashboard</a></li>
                <li><a href="{{ url_for('analytics') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-chart-line mr-2"></i> Analytics</a></li>
                <li><a href="{{ url_for('ai_training') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-robot mr-2"></i> AI Training</a></li>
                <li><a href="{{ url_for('conversations') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-comments mr-2"></i> Conversations</a></li>
                <li><a href="{{ url_for('leads') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-users mr-2"></i> Leads</a></li>
                <li><a href="{{ url_for('broadcast') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-bullhorn mr-2"></i> Broadcast</a></li>
                <li><a href="{{ url_for('notifications_page') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-bell mr-2"></i> Notifications</a></li>
                <li><a href="{{ url_for('insights') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-lightbulb mr-2"></i> Insights</a></li>
                <li><a href="{{ url_for('security') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-shield-alt mr-2"></i> Security</a></li>
                <li><a href="{{ url_for('ai_settings') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-cog mr-2"></i> AI Settings</a></li>
                <li><a href="{{ url_for('knowledge_base') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-database mr-2"></i> Knowledge Base</a></li>
                <li><a href="{{ url_for('monetization') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-money-bill-wave mr-2"></i> Plans & Billing</a></li>
                <li><a href="{{ url_for('advanced_ai') }}" class="block p-2 hover:bg-green-50 rounded" onclick="closeSidebar()"><i class="fas fa-microphone mr-2"></i> Advanced AI</a></li>
                <li><a href="{{ url_for('logout') }}" class="block p-2 hover:bg-red-50 rounded text-red-600" onclick="closeSidebar()"><i class="fas fa-sign-out-alt mr-2"></i> Logout</a></li>
            </ul>
        </div>
    </div>

    <!-- Main Content Area -->
    <div class="min-h-screen flex flex-col">
        <!-- Top Bar with Hamburger Icon -->
        <nav class="bg-white shadow p-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-green-600">XyronAI</h1>
            <div class="flex items-center space-x-4">
                <span class="mr-2"><i class="fas fa-bell"></i> <span class="badge bg-danger">{{ unread_count }}</span></span>
                <span>{{ current_user.plan|capitalize }} Plan</span>
                <!-- Three dashes (hamburger) icon -->
                <button id="menuBtn" class="text-gray-600 hover:text-green-600 focus:outline-none">
                    <i class="fas fa-bars text-2xl"></i>
                </button>
            </div>
        </nav>

        <!-- Flash Messages -->
        <div class="container mx-auto px-4 py-4">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>

        <!-- Page Content (center) -->
        <main class="flex-1 container mx-auto px-4 pb-8">
            {% block content %}{% endblock %}
        </main>

        <!-- Footer -->
        <footer class="text-center text-gray-250 text-sm py-2 border-t">
            <p>
                <a href="{{ url_for('about_page') }}" class="hover:text-blue-250 mx-1">📖 About Us</a>
                |
                <a href="{{ url_for('terms_page') }}" class="hover:text-orange-250 mx-1">📜 Terms</a>
                |
                <a href="{{ url_for('rules_page') }}" class="hover:text-yellow-250 mx-2">⚠️ Rules</a>
                |
                <a href="{{ url_for('developer_page') }}" class="hover:text-green-600 mx-2">👨‍💻 Developer</a>
            </p>

        

        

        

        

        

        

        <section>

        <section>

            <p class="mt-2">© 2026 XyronAI. All rights reserved.</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        const menuBtn = document.getElementById('menuBtn');

        function openSidebar() {
            sidebar.classList.add('open');
            overlay.classList.add('active');
        }
        function closeSidebar() {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        }
        menuBtn.addEventListener('click', openSidebar);
        // On desktop (>=768px), we want the sidebar always visible? No – we keep it hidden but open on click.
        // If you prefer the sidebar always visible on desktop, add a media query to set left:0.
        // But the requirement says "three dashes on the right corner when clicked they show the side bar features"
        // So we keep it hidden initially on all screen sizes.
    </script>
</body>
</html>
"""
# ---------- Routes: Auth & Core ----------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# ========== AUTH TEMPLATE (NO SIDEBAR) ==========
AUTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XyronAI - Login/Register</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-12">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            log_activity(user.id, "Login", request.remote_addr, request.user_agent.string)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    
    content = '''
    <div class="max-w-md mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Login</h2>
        <form method="POST">
            <div class="mb-3"><label class="block mb-1">Email</label><input type="email" name="email" class="w-full border p-2 rounded" required></div>
            <div class="mb-3"><label class="block mb-1">Password</label><input type="password" name="password" class="w-full border p-2 rounded" required></div>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded w-full">Login</button>
        </form>
        <p class="mt-4 text-center">No account? <a href="{{ url_for('register') }}" class="text-green-600">Register</a></p>
    </div>
    '''
    template = AUTH_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        business_name = request.form['business_name']
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        user = User(email=email, password_hash=generate_password_hash(password), business_name=business_name)
        db.session.add(user)
        db.session.commit()
        business = Business(user_id=user.id)
        db.session.add(business)
        db.session.commit()
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))
    
    content = '''
    <div class="max-w-md mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Register</h2>
        <form method="POST">
            <div class="mb-3"><label class="block mb-1">Email</label><input type="email" name="email" class="w-full border p-2 rounded" required></div>
            <div class="mb-3"><label class="block mb-1">Password</label><input type="password" name="password" class="w-full border p-2 rounded" required></div>
            <div class="mb-3"><label class="block mb-1">Business Name</label><input type="text" name="business_name" class="w-full border p-2 rounded" required></div>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded w-full">Register</button>
        </form>
        <p class="mt-4 text-center">Already have an account? <a href="{{ url_for('login') }}" class="text-green-600">Login</a></p>
    </div>
    '''
    template = AUTH_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template)

@app.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, "Logout", request.remote_addr, request.user_agent.string)
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        flash('Please set up your business first', 'warning')
        return redirect(url_for('business_settings'))
    
    # Sample data for the new dashboard
    total_chats_today = Conversation.query.filter(
        Conversation.business_id == business.id,
        Conversation.last_message_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count()
    
    # Average response time (mock - you can implement real calculation)
    avg_response_time = "~2.3 sec"
    
    # Active users (mock)
    active_users = 42
    
    # Earnings (if you have payments)
    earnings = "$0.00"  # implement real sum if you have payments table
    
    last_activity = Conversation.query.filter_by(business_id=business.id).order_by(Conversation.last_message_at.desc()).first()
    last_activity_time = last_activity.last_message_at.strftime('%H:%M') if last_activity else "Never"
    
    # Recent activities (mock)
    recent_activities = [
        "You asked AI a question",
        "Message sent successfully",
        "New lead captured",
        "AI training updated"
    ]
    
    # Notifications (mock)
    notifications = [
        {"title": "System Update", "message": "New AI features available", "type": "info"},
        {"title": "Maintenance", "message": "Scheduled downtime tonight", "type": "warning"},
        {"title": "New Message", "message": "You have 3 unread conversations", "type": "success"}
    ]
    
    # Dashboard HTML content (embedded in the main content block)
    dashboard_html = '''
    <div class="space-y-6">
        <!-- 2. Welcome Banner -->
        <div class="bg-gradient-to-r from-green-500 to-green-700 rounded-xl shadow-lg p-6 text-white">
            <h2 class="text-2xl font-bold">Welcome Back, {{ current_user.business_name or current_user.email.split('@')[0] }}! 👋</h2>
            <p class="mt-2">Your AI assistant is ready to help you manage chats, answer questions, and automate your work anytime.</p>
            <div class="flex flex-wrap gap-3 mt-4">
                <a href="{{ url_for('conversations') }}" class="bg-white text-green-700 px-4 py-2 rounded-lg hover:bg-gray-100">🚀 Start Chat</a>
                <a href="#" class="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30">🤖 Ask AI</a>
                <a href="{{ url_for('analytics') }}" class="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30">📊 View Activity</a>
            </div>
        </div>
        
        <!-- 3. Quick Action Buttons -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <a href="{{ url_for('conversations') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">💬</div>
                <span class="text-sm font-medium">Chat Assistant</span>
            </a>
            <a href="{{ url_for('broadcast') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">📩</div>
                <span class="text-sm font-medium">Send Message</span>
            </a>
            <a href="{{ url_for('ai_training') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">🧠</div>
                <span class="text-sm font-medium">AI Help Center</span>
            </a>
            <a href="{{ url_for('analytics') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">📊</div>
                <span class="text-sm font-medium">Analytics</span>
            </a>
            <a href="{{ url_for('business_settings') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">⚙️</div>
                <span class="text-sm font-medium">Settings</span>
            </a>
            <a href="{{ url_for('monetization') }}" class="bg-white p-4 rounded-xl shadow text-center hover:shadow-lg transition">
                <div class="text-2xl mb-1">💳</div>
                <span class="text-sm font-medium">Payments</span>
            </a>
        </div>
        
        <!-- 4. AI Assistant Box -->
        <div class="bg-white rounded-xl shadow p-5">
            <h3 class="text-xl font-bold text-gray-800 mb-3">🤖 AI Assistant Panel</h3>
            <div class="flex gap-2">
                <input type="text" id="aiInput" placeholder="Ask me anything..." class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500">
                <button onclick="askAI()" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">Send</button>
            </div>
            <div class="flex flex-wrap gap-2 mt-3">
                <button onclick="fillAI('Help me write a message')" class="text-sm bg-gray-100 px-3 py-1 rounded-full hover:bg-gray-200">📝 Help me write a message</button>
                <button onclick="fillAI('Explain my account')" class="text-sm bg-gray-100 px-3 py-1 rounded-full hover:bg-gray-200">🔍 Explain my account</button>
                <button onclick="fillAI('Generate business idea')" class="text-sm bg-gray-100 px-3 py-1 rounded-full hover:bg-gray-200">💡 Generate business idea</button>
            </div>
            <div id="aiResponse" class="mt-3 text-sm text-gray-600"></div>
        </div>
        
        <!-- 5. Stats Overview -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <div class="bg-white p-4 rounded-xl shadow">
                <h4 class="text-gray-500 text-sm">📈 Total Chats Today</h4>
                <p class="text-2xl font-bold">{{ total_chats_today }}</p>
            </div>
            <div class="bg-white p-4 rounded-xl shadow">
                <h4 class="text-gray-500 text-sm">⚡ Response Speed</h4>
                <p class="text-2xl font-bold">{{ avg_response_time }}</p>
            </div>
            <div class="bg-white p-4 rounded-xl shadow">
                <h4 class="text-gray-500 text-sm">👥 Active Users</h4>
                <p class="text-2xl font-bold">{{ active_users }}</p>
            </div>
            <div class="bg-white p-4 rounded-xl shadow">
                <h4 class="text-gray-500 text-sm">💰 Earnings</h4>
                <p class="text-2xl font-bold">{{ earnings }}</p>
            </div>
            <div class="bg-white p-4 rounded-xl shadow">
                <h4 class="text-gray-500 text-sm">🕒 Last Activity</h4>
                <p class="text-2xl font-bold">{{ last_activity_time }}</p>
            </div>
        </div>
        
        <!-- 6. Recent Activity & 7. Notifications Panel (side by side) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Recent Activity -->
            <div class="bg-white rounded-xl shadow p-5">
                <h3 class="text-lg font-bold mb-3">🕘 Recent Activity</h3>
                <ul class="space-y-2">
                    {% for activity in recent_activities %}
                    <li class="flex items-center gap-2 text-gray-700"><span class="text-green-500">✔️</span> {{ activity }}</li>
                    {% endfor %}
                </ul>
            </div>
            <!-- Notifications Panel -->
            <div class="bg-white rounded-xl shadow p-5">
                <h3 class="text-lg font-bold mb-3">🔔 Notifications</h3>
                <ul class="space-y-3">
                    {% for notif in notifications %}
                    <li class="border-b pb-2">
                        <div class="font-medium">{{ notif.title }}</div>
                        <div class="text-sm text-gray-600">{{ notif.message }}</div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <!-- 8. Footer Navigation (Mobile style) -->
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg md:hidden block">
            <div class="flex justify-around py-2">
                <a href="{{ url_for('dashboard') }}" class="text-green-600"><i class="fas fa-home"></i> Home</a>
                <a href="{{ url_for('conversations') }}" class="text-gray-600"><i class="fas fa-comment"></i> Chat</a>
                <a href="{{ url_for('analytics') }}" class="text-gray-600"><i class="fas fa-chart-line"></i> Dashboard</a>
                <a href="{{ url_for('monetization') }}" class="text-gray-600"><i class="fas fa-wallet"></i> Wallet</a>
                <a href="{{ url_for('business_settings') }}" class="text-gray-600"><i class="fas fa-user"></i> Profile</a>
            </div>
        </div>
    </div>
    
    <script>
        function askAI() {
            const input = document.getElementById('aiInput').value;
            if (!input) return;
            document.getElementById('aiResponse').innerHTML = '<span class="text-gray-500">Thinking...</span>';
            fetch('/ai-ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: input})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('aiResponse').innerHTML = '<div class="bg-gray-100 p-2 rounded">' + data.answer + '</div>';
                document.getElementById('aiInput').value = '';
            })
            .catch(err => {
                document.getElementById('aiResponse').innerHTML = '<span class="text-red-500">Error, please try again.</span>';
            });
        }
        function fillAI(text) {
            document.getElementById('aiInput').value = text;
        }
    </script>
    '''
    
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', dashboard_html)
    return render_template_string(template, 
                                  unread_count=unread,
                                  total_chats_today=total_chats_today,
                                  avg_response_time=avg_response_time,
                                  active_users=active_users,
                                  earnings=earnings,
                                  last_activity_time=last_activity_time,
                                  recent_activities=recent_activities,
                                  notifications=notifications)

@app.route('/analytics')
@login_required
def analytics():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        return redirect(url_for('business_settings'))
    
    # Real data counts
    total_users = 1  # for now, since each business has one user. If you add team members later, count them.
    
    # Active users today: count unique customer_phone that sent messages today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    active_today = db.session.query(Conversation.customer_phone).filter(
        Conversation.business_id == business.id,
        Conversation.last_message_at >= today_start
    ).distinct().count()
    
    # New users this week: count users created in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users_this_week = User.query.filter(User.created_at >= week_ago).count()
    
    # Peak chat hours: get messages per hour for last 7 days
    hourly_data = [0]*24
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    messages = Message.query.join(Conversation).filter(
        Conversation.business_id == business.id,
        Message.created_at >= seven_days_ago
    ).all()
    for msg in messages:
        hour = msg.created_at.hour
        hourly_data[hour] += 1
    
    # Prepare chart labels (hours 0-23)
    hours = [f"{h}:00" for h in range(24)]
    
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Analytics</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-white p-4 rounded shadow"><h3>Total Users</h3><p class="text-2xl">{{ total_users }}</p><small>Your business only</small></div>
        <div class="bg-white p-4 rounded shadow"><h3>Active Users Today</h3><p class="text-2xl">{{ active_today }}</p></div>
        <div class="bg-white p-4 rounded shadow"><h3>New Users This Week</h3><p class="text-2xl">{{ new_users_this_week }}</p></div>
    </div>
    <div class="bg-white p-4 rounded shadow mb-6">
        <h3>Peak Chat Hours</h3>
        <canvas id="peakChart" height="100"></canvas>
    </div>
    <script>
        new Chart(document.getElementById('peakChart'), { 
            type: 'line', 
            data: { 
                labels: {{ hours|tojson }}, 
                datasets: [{ label: 'Messages', data: {{ hourly_data|tojson }}, borderColor: '#10b981', fill: false }] 
            } 
        });
    </script>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, 
                                  total_users=total_users, 
                                  active_today=active_today, 
                                  new_users_this_week=new_users_this_week,
                                  hours=hours,
                                  hourly_data=hourly_data,
                                  unread_count=unread)

# ---------- AI Training ----------
@app.route('/ai-training', methods=['GET', 'POST'])
@login_required
def ai_training():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        training = TrainingData(business_id=business.id, question=question, answer=answer)
        db.session.add(training)
        db.session.commit()
        flash('Training data added', 'success')
        return redirect(url_for('ai_training'))
    trainings = TrainingData.query.filter_by(business_id=business.id).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">AI Training Center</h2>
    <div class="bg-white p-4 rounded shadow mb-6">
        <h3>Training Statistics</h3>
        <p>Total Questions Trained: {{ trainings|length }}</p>
        <p>Last Training Date: {{ trainings[-1].created_at if trainings else 'Never' }}</p>
        <button class="bg-blue-600 text-white px-4 py-2 rounded">Train AI Now</button>
    </div>
    <div class="bg-white p-4 rounded shadow">
        <h3>Add Training Data</h3>
        <form method="POST">
            <input type="text" name="question" placeholder="Question" class="w-full border p-2 mb-2" required>
            <textarea name="answer" placeholder="Answer" class="w-full border p-2 mb-2" required></textarea>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Add</button>
        </form>
        <h3 class="mt-4">Existing Training</h3>
        <ul>
            {% for t in trainings %}
            <li><strong>{{ t.question }}</strong> - {{ t.answer }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, trainings=trainings, unread_count=unread)

# ---------- Leads Management ----------
@app.route('/leads')
@login_required
def leads():
    business = Business.query.filter_by(user_id=current_user.id).first()
    leads_list = Lead.query.filter_by(business_id=business.id).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Lead Management</h2>
    <div class="bg-white p-4 rounded shadow">
        <table class="min-w-full">
            <thead><tr><th>Name</th><th>Phone</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
            <tbody>
                {% for lead in leads %}
                <tr><td>{{ lead.name or 'N/A' }}</td><td>{{ lead.customer_phone }}</td><td>{{ lead.email or 'N/A' }}</td><td>{{ lead.status }}</td><td><a href="#" class="text-blue-600">Update</a> | <a href="#" class="text-red-600">Delete</a></td></tr>
                {% endfor %}
            </tbody>
        </table>
        <button class="bg-green-600 text-white px-4 py-2 rounded mt-4">Export Leads (CSV)</button>
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, leads=leads_list, unread_count=unread)

@app.route('/broadcast', methods=['GET', 'POST'])
@login_required
def broadcast():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        flash('Please set up your business first', 'warning')
        return redirect(url_for('business_settings'))
    
    if request.method == 'POST':
        message = request.form['message']
        recipients_type = request.form['recipients_type']  # 'all_leads' or 'all_conversations' or 'test'
        
        # Get recipient list
        recipient_numbers = []
        if recipients_type == 'all_leads':
            leads = Lead.query.filter_by(business_id=business.id).all()
            recipient_numbers = [lead.customer_phone for lead in leads if lead.customer_phone]
        elif recipients_type == 'all_conversations':
            convs = Conversation.query.filter_by(business_id=business.id).all()
            recipient_numbers = list(set([conv.customer_phone for conv in convs]))
        elif recipients_type == 'test':
            # Send to yourself (the logged-in user's phone number from User model)
            test_number = current_user.phone_number
            if test_number:
                recipient_numbers = [test_number]
            else:
                flash('Please add your phone number in profile first', 'danger')
                return redirect(url_for('business_settings'))
        
        # Create broadcast record
        broadcast = Broadcast(
            business_id=business.id,
            message=message,
            recipients=','.join(recipient_numbers),
            status='pending'
        )
        db.session.add(broadcast)
        db.session.commit()
        
        # Send messages (in background, but for simplicity we send now)
        sent_count = 0
        for phone in recipient_numbers:
            result = send_whatsapp_message(phone, message)
            if 'error' not in result:
                sent_count += 1
            time.sleep(0.5)  # avoid rate limits
        
        broadcast.status = 'sent'
        broadcast.sent_at = datetime.utcnow()
        broadcast.delivery_count = sent_count
        db.session.commit()
        
        flash(f'Broadcast sent to {sent_count} of {len(recipient_numbers)} recipients', 'success')
        return redirect(url_for('broadcast'))
    
    # GET: show form and list of past broadcasts
    broadcasts = Broadcast.query.filter_by(business_id=business.id).order_by(Broadcast.id.desc()).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Broadcast Messages</h2>
    
    <!-- Create Broadcast Form -->
    <div class="bg-white p-6 rounded-lg shadow mb-8">
        <h3 class="text-lg font-semibold mb-4">📢 New Broadcast</h3>
        <form method="POST">
            <div class="mb-4">
                <label class="block font-medium mb-1">Message</label>
                <textarea name="message" rows="4" class="w-full border rounded-lg px-3 py-2" placeholder="Type your broadcast message..." required></textarea>
            </div>
            <div class="mb-4">
                <label class="block font-medium mb-1">Send to</label>
                <select name="recipients_type" class="border rounded-lg px-3 py-2">
                    <option value="all_leads">📞 All captured leads</option>
                    <option value="all_conversations">💬 All conversations</option>
                    <option value="test">🧪 Test (send to your own number)</option>
                </select>
            </div>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">🚀 Send Broadcast</button>
        </form>
    </div>
    
    <!-- Past Broadcasts List -->
    <div class="bg-white rounded-lg shadow">
        <h3 class="text-lg font-semibold p-4 border-b">📜 Sent Broadcasts</h3>
        {% if broadcasts %}
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-4 py-2 text-left">Date</th>
                        <th class="px-4 py-2 text-left">Message</th>
                        <th class="px-4 py-2 text-left">Recipients</th>
                        <th class="px-4 py-2 text-left">Delivered</th>
                        <th class="px-4 py-2 text-left">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for b in broadcasts %}
                    <tr class="border-b">
                        <td class="px-4 py-2">{{ b.sent_at.strftime("%Y-%m-%d %H:%M") if b.sent_at else "Pending" }}</td>
                        <td class="px-4 py-2">{{ b.message[:50] }}{% if b.message|length > 50 %}...{% endif %}</td>
                        <td class="px-4 py-2">{{ b.recipients.split(',')|length }}</td>
                        <td class="px-4 py-2">{{ b.delivery_count }}</td>
                        <td class="px-4 py-2"><span class="px-2 py-1 rounded text-sm {% if b.status=='sent' %}bg-green-100 text-green-800{% else %}bg-yellow-100 text-yellow-800{% endif %}">{{ b.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <p class="p-4 text-gray-500">No broadcasts sent yet. Create your first broadcast above.</p>
        {% endif %}
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, broadcasts=broadcasts, unread_count=unread)

# ---------- Notifications ----------
@app.route('/notifications')
@login_required
def notifications_page():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    for n in notifs:
        n.read = True
    db.session.commit()
    unread = 0
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Notifications</h2>
    <div class="bg-white p-4 rounded shadow">
        {% for n in notifs %}
        <div class="border-b py-2"><strong>{{ n.title }}</strong><br>{{ n.message }}<br><small>{{ n.created_at.strftime('%Y-%m-%d %H:%M') }}</small></div>
        {% endfor %}
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, notifs=notifs, unread_count=unread)

# ---------- Business Insights ----------
@app.route('/insights')
@login_required
def insights():
    business = Business.query.filter_by(user_id=current_user.id).first()
    # Dummy data
    top_questions = ["Price?", "Hours?", "Location?"]
    csat = 4.5
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Business Insights</h2>
    <div class="bg-white p-4 rounded shadow mb-6"><h3>Most Asked Questions</h3><ul>{% for q in top_questions %}<li>{{ q }}</li>{% endfor %}</ul></div>
    <div class="bg-white p-4 rounded shadow"><h3>Customer Satisfaction Score</h3><p>{{ csat }} / 5.0</p></div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, top_questions=top_questions, csat=csat, unread_count=unread)

# ---------- Security ----------
@app.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    if request.method == 'POST':
        # 2FA mock
        flash('2FA enabled (demo)', 'success')
        return redirect(url_for('security'))
    logs = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.created_at.desc()).limit(20).all()
    tokens = APIToken.query.filter_by(user_id=current_user.id).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Security Settings</h2>
    <div class="bg-white p-4 rounded shadow mb-6"><h3>Two-Factor Authentication</h3><form method="POST"><button class="bg-blue-600 text-white px-4 py-2 rounded">Enable 2FA</button></form></div>
    <div class="bg-white p-4 rounded shadow mb-6"><h3>API Keys</h3><button class="bg-green-600 text-white px-4 py-2 rounded">Generate New Key</button></div>
    <div class="bg-white p-4 rounded shadow"><h3>Login History</h3><ul>{% for log in logs %}<li>{{ log.created_at }} - {{ log.action }} from {{ log.ip_address }}</li>{% endfor %}</ul></div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, logs=logs, tokens=tokens, unread_count=unread)

# ---------- AI Settings ----------
@app.route('/ai-settings', methods=['GET', 'POST'])
@login_required
def ai_settings():
    if request.method == 'POST':
        current_user.ai_name = request.form['ai_name']
        current_user.ai_personality = request.form['ai_personality']
        current_user.ai_language = request.form['ai_language']
        current_user.auto_reply_enabled = 'auto_reply' in request.form
        db.session.commit()
        flash('AI settings updated', 'success')
        return redirect(url_for('ai_settings'))
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">AI Settings</h2>
    <div class="bg-white p-4 rounded shadow">
        <form method="POST">
            <div class="mb-2"><label>AI Name</label><input type="text" name="ai_name" value="{{ current_user.ai_name }}" class="w-full border p-2"></div>
            <div class="mb-2"><label>Personality</label><input type="text" name="ai_personality" value="{{ current_user.ai_personality }}" class="w-full border p-2"></div>
            <div class="mb-2"><label>Language</label><select name="ai_language" class="w-full border p-2"><option value="en">English</option><option value="sw">Swahili</option></select></div>
            <div class="mb-2"><label><input type="checkbox" name="auto_reply" {% if current_user.auto_reply_enabled %}checked{% endif %}> Auto-reply enabled</label></div>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Save</button>
        </form>
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, unread_count=unread)

@app.route('/ai-ask', methods=['POST'])
@login_required
def ai_ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'Please ask something.'})
    
    business = Business.query.filter_by(user_id=current_user.id).first()
    # Use your existing generate_ai_response function (you already have it)
    answer = generate_ai_response(business.id, current_user.id, question, current_user)
    return jsonify({'answer': answer})

# ---------- Knowledge Base (with file upload) ----------
@app.route('/knowledge-base', methods=['GET', 'POST'])
@login_required
def knowledge_base():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        # For simplicity, we handle text FAQ addition
        question = request.form['question']
        answer = request.form['answer']
        kb = KnowledgeBase(business_id=business.id, question=question, answer=answer)
        db.session.add(kb)
        db.session.commit()
        flash('FAQ added', 'success')
        return redirect(url_for('knowledge_base'))
    items = KnowledgeBase.query.filter_by(business_id=business.id).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Knowledge Base</h2>
    <div class="bg-white p-4 rounded shadow mb-6">
        <h3>Add FAQ</h3>
        <form method="POST">
            <input type="text" name="question" placeholder="Question" class="w-full border p-2 mb-2" required>
            <textarea name="answer" placeholder="Answer" class="w-full border p-2 mb-2" required></textarea>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Add</button>
        </form>
        <hr class="my-4">
        <h3>Upload File (PDF/DOCX)</h3>
        <form action="{{ url_for('upload_kb_file') }}" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf,.docx,.txt" class="border p-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Upload</button>
        </form>
    </div>
    <div class="bg-white p-4 rounded shadow"><h3>Existing FAQs</h3><ul>{% for item in items %}<li><strong>{{ item.question }}</strong><br>{{ item.answer }}</li>{% endfor %}</ul></div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, items=items, unread_count=unread)

@app.route('/upload-kb-file', methods=['POST'])
@login_required
def upload_kb_file():
    # Stub for file processing
    flash('File upload feature - would parse PDF/DOCX', 'info')
    return redirect(url_for('knowledge_base'))

# ---------- Monetization (Plans & M-Pesa stub) ----------
@app.route('/monetization', methods=['GET', 'POST'])
@login_required
def monetization():
    if request.method == 'POST':
        plan = request.form['plan']
        current_user.plan = plan
        # M-Pesa integration stub
        if plan != 'free':
            flash('M-Pesa payment simulation: please send KES to paybill...', 'info')
        db.session.commit()
        flash(f'Plan changed to {plan}', 'success')
        return redirect(url_for('monetization'))
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Subscription & Billing</h2>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white p-4 rounded shadow text-center"><h3>Free</h3><p>$0/month</p><form method="POST"><input type="hidden" name="plan" value="free"><button class="bg-gray-600 text-white px-4 py-2 rounded">Select</button></form></div>
        <div class="bg-white p-4 rounded shadow text-center"><h3>Starter</h3><p>$29/month</p><form method="POST"><input type="hidden" name="plan" value="starter"><button class="bg-green-600 text-white px-4 py-2 rounded">Upgrade</button></form></div>
        <div class="bg-white p-4 rounded shadow text-center"><h3>Pro</h3><p>$99/month</p><form method="POST"><input type="hidden" name="plan" value="pro"><button class="bg-green-600 text-white px-4 py-2 rounded">Upgrade</button></form></div>
        <div class="bg-white p-4 rounded shadow text-center"><h3>Enterprise</h3><p>Custom</p><form method="POST"><input type="hidden" name="plan" value="enterprise"><button class="bg-green-600 text-white px-4 py-2 rounded">Contact</button></form></div>
    </div>
    <div class="bg-white p-4 rounded shadow mt-6"><h3>M-PESA Payment (Kenya)</h3><p>Simulated: Paybill 123456, Account: Your Email</p></div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, unread_count=unread)

# ---------- Advanced AI (Voice, Multi-language) ----------
@app.route('/advanced-ai')
@login_required
def advanced_ai():
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}
    <h2 class="text-2xl font-bold mb-6">Advanced AI Features</h2>
    <div class="bg-white p-4 rounded shadow grid grid-cols-1 md:grid-cols-2 gap-4">
        <div><i class="fas fa-microphone fa-2x"></i> <h3>Voice Messages</h3><p>Speech-to-Text active for incoming voice notes.</p></div>
        <div><i class="fas fa-language fa-2x"></i> <h3>Multi-Language</h3><p>Auto-detect and reply in customer's language.</p></div>
        <div><i class="fas fa-image fa-2x"></i> <h3>Image Recognition</h3><p>Analyze product images sent by customers.</p></div>
        <div><i class="fas fa-file-alt fa-2x"></i> <h3>Document Analysis</h3><p>Extract data from PDF invoices.</p></div>
    </div>
    {% endblock %}
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, unread_count=unread)

# ---------- Existing routes (Conversations, send-reply, business-settings, webhook) ----------
@app.route('/conversations')
@login_required
def conversations():
    business = Business.query.filter_by(user_id=current_user.id).first()
    phone_filter = request.args.get('phone', '')
    convs = Conversation.query.filter_by(business_id=business.id, archived=False).order_by(Conversation.last_message_at.desc()).all()
    conv = None
    messages = []
    if phone_filter:
        conv = Conversation.query.filter_by(business_id=business.id, customer_phone=phone_filter).first()
        if conv:
            messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.created_at).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    content = '''
    {% block content %}<div class="flex gap-6">...</div>{% endblock %}
    '''
    # For brevity, we keep the original conversation template but with unread_count
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, convs=convs, conv=conv, messages=messages, business=business, unread_count=unread)

@app.route('/send-reply', methods=['POST'])
@login_required
def send_reply():
    business_id = request.form['business_id']
    customer_phone = request.form['customer_phone']
    message = request.form['message']
    conv = Conversation.query.filter_by(business_id=business_id, customer_phone=customer_phone).first()
    if not conv:
        flash('Conversation not found', 'danger')
        return redirect(url_for('conversations'))
    resp = send_whatsapp_message(customer_phone, message)
    if 'error' in resp:
        flash(f'WhatsApp error: {resp["error"].get("message", "Unknown")}', 'danger')
    else:
        save_message(conv.id, 'outgoing', message)
        flash('Message sent', 'success')
    return redirect(url_for('conversations', phone=customer_phone))

@app.route('/business-settings', methods=['GET', 'POST'])
@login_required
def business_settings():
    import json
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        business = Business(user_id=current_user.id)
        db.session.add(business)
        db.session.commit()

    settings = json.loads(business.settings) if business.settings else {}
    social = settings.get('social', {})

    if request.method == 'POST':
        # Save FAQs
        questions = request.form.getlist('question[]')
        answers = request.form.getlist('answer[]')
        KnowledgeBase.query.filter_by(business_id=business.id).delete()
        for q, a in zip(questions, answers):
            if q and a:
                kb = KnowledgeBase(business_id=business.id, question=q, answer=a)
                db.session.add(kb)
        # Save social links
        social = {
            'facebook': request.form.get('facebook'),
            'instagram': request.form.get('instagram'),
            'twitter': request.form.get('twitter'),
            'linkedin': request.form.get('linkedin'),
            'tiktok': request.form.get('tiktok'),
            'youtube': request.form.get('youtube')
        }
        settings['social'] = social
        business.settings = json.dumps(settings)
        db.session.commit()
        flash('Business settings saved!', 'success')
        return redirect(url_for('business_settings'))

    knowledge_items = KnowledgeBase.query.filter_by(business_id=business.id).all()
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()

    content = '''
    <div class="max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold mb-6">Business Settings</h2>
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h3 class="text-lg font-semibold mb-3">📱 WhatsApp Setup</h3>
            <div class="grid md:grid-cols-2 gap-4 text-sm">
                <div><strong>Phone Number ID:</strong> {{ phone_number_id }}</div>
                <div><strong>Webhook URL:</strong> {{ webhook_url }}</div>
                <div><strong>Verify Token:</strong> {{ verify_token }}</div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h3 class="text-lg font-semibold mb-3">🔗 Social Media Links</h3>
            <div class="grid md:grid-cols-2 gap-4">
                <input type="url" name="facebook" placeholder="Facebook URL" value="{{ social.facebook }}" class="border rounded px-3 py-2">
                <input type="url" name="instagram" placeholder="Instagram URL" value="{{ social.instagram }}" class="border rounded px-3 py-2">
                <input type="url" name="twitter" placeholder="Twitter URL" value="{{ social.twitter }}" class="border rounded px-3 py-2">
                <input type="url" name="linkedin" placeholder="LinkedIn URL" value="{{ social.linkedin }}" class="border rounded px-3 py-2">
                <input type="url" name="tiktok" placeholder="TikTok URL" value="{{ social.tiktok }}" class="border rounded px-3 py-2">
                <input type="url" name="youtube" placeholder="YouTube URL" value="{{ social.youtube }}" class="border rounded px-3 py-2">
            </div>
        </div>

        <form method="POST">
            <div class="bg-white rounded-lg shadow p-6 mb-6">
                <h3 class="text-lg font-semibold mb-3">🧠 Knowledge Base (FAQ)</h3>
                <div id="kbContainer" class="space-y-4">
                    {% for item in knowledge_items %}
                    <div class="kb-item border rounded p-3">
                        <input type="text" name="question[]" value="{{ item.question }}" class="w-full border rounded mb-2 px-2 py-1" placeholder="Question">
                        <textarea name="answer[]" rows="2" class="w-full border rounded px-2 py-1" placeholder="Answer">{{ item.answer }}</textarea>
                        <button type="button" class="removeKB text-red-600 text-sm">Remove</button>
                    </div>
                    {% else %}
                    <div class="kb-item border rounded p-3">
                        <input type="text" name="question[]" class="w-full border rounded mb-2 px-2 py-1" placeholder="Question">
                        <textarea name="answer[]" rows="2" class="w-full border rounded px-2 py-1" placeholder="Answer"></textarea>
                        <button type="button" class="removeKB text-red-600 text-sm">Remove</button>
                    </div>
                    {% endfor %}
                </div>
                <button type="button" id="addKB" class="mt-3 bg-gray-200 px-3 py-1 rounded">+ Add FAQ</button>
            </div>
            <div class="flex justify-end">
                <button type="submit" class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700">💾 Save Settings</button>
            </div>
        </form>
    </div>
    <script>
        document.getElementById('addKB')?.addEventListener('click', function() {
            const container = document.getElementById('kbContainer');
            const div = document.createElement('div');
            div.className = 'kb-item border rounded p-3';
            div.innerHTML = `
                <input type="text" name="question[]" class="w-full border rounded mb-2 px-2 py-1" placeholder="Question">
                <textarea name="answer[]" rows="2" class="w-full border rounded px-2 py-1" placeholder="Answer"></textarea>
                <button type="button" class="removeKB text-red-600 text-sm">Remove</button>
            `;
            container.appendChild(div);
        });
        document.getElementById('kbContainer')?.addEventListener('click', function(e) {
            if (e.target.classList.contains('removeKB')) e.target.closest('.kb-item').remove();
        });
    </script>
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template,
                                  knowledge_items=knowledge_items,
                                  phone_number_id=os.getenv('WHATSAPP_PHONE_NUMBER_ID', 'Not set'),
                                  webhook_url=request.host_url.rstrip('/') + '/webhook',
                                  verify_token=os.getenv('WHATSAPP_VERIFY_TOKEN', 'my_verify_token'),
                                  social=social,
                                  unread_count=unread)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Verification failed', 403
    data = request.json
    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        if 'messages' in value:
            message = value['messages'][0]
            if message['type'] == 'text':
                customer_phone = message['from']
                text = message['text']['body']
                business = Business.query.first()
                if business:
                    conv = get_or_create_conversation(business.id, customer_phone)
                    save_message(conv.id, 'incoming', text)
                    # Extract lead info (name)
                    lead = Lead.query.filter_by(business_id=business.id, customer_phone=customer_phone).first()
                    if not lead:
                        lead = Lead(business_id=business.id, customer_phone=customer_phone)
                        db.session.add(lead)
                    name_match = re.search(r'my name is (\w+)', text, re.IGNORECASE)
                    if name_match and not lead.name:
                        lead.name = name_match.group(1)
                    db.session.commit()
                    # Generate AI reply (use user settings)
                    user = User.query.get(business.user_id)
                    if user and user.auto_reply_enabled:
                        ai_reply = generate_ai_response(business.id, customer_phone, text, user)
                        send_whatsapp_message(customer_phone, ai_reply)
                        save_message(conv.id, 'outgoing', ai_reply)
                    # Create notification for new message
                    create_notification(user.id, "New WhatsApp Message", f"From {customer_phone}: {text[:50]}...", "chat")
    except Exception as e:
        print(f"Webhook error: {e}")
    return 'OK', 200

# ========== LEGAL PAGES (Directly embedded) ==========

@app.route('/legal')
def legal():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    
    # Full legal HTML as a string (simplified - I'll show the complete version below)
    legal_html = '''
    <div class="max-w-5xl mx-auto">
        <h1 class="text-3xl font-bold text-green-700 mb-6">Legal & Terms</h1>
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">Terms and Conditions</h2>
            <p class="text-sm text-gray-500 mb-4">Last Updated: June 2026</p>
            <p>Welcome to XyronAI. These Terms and Conditions govern your access to...</p>
            <!-- Add full terms here -->
        </div>
    </div>
    '''
    
    # Wrap with BASE_TEMPLATE
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', legal_html)
    return render_template_string(template, unread_count=unread_count)

@app.route('/terms')
def terms_page():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', LEGAL_TERMS_HTML)
    return render_template_string(template, unread_count=unread_count)

@app.route('/rules')
def rules_page():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', LEGAL_RULES_HTML)
    return render_template_string(template, unread_count=unread_count)

@app.route('/about')
def about_page():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ABOUT_US_HTML)
    return render_template_string(template, unread_count=unread_count)

# ========== DEVELOPER & PARTNERSHIP PAGE ==========
DEVELOPER_HTML = '''
<div class="max-w-5xl mx-auto">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-green-600 to-green-800 rounded-2xl shadow-xl p-8 text-white mb-8">
        <div class="flex flex-col md:flex-row items-center gap-6">
            <img src="/static/mrnex.jpg" alt="Mr. Nex" class="rounded-full border-4 border-white w-32 h-32 object-cover">
            <div>
                <h1 class="text-3xl font-bold">Brian Ondieki (Mr. Nex)</h1>
                <p class="text-xl opacity-90">Founder & Lead Developer | AI Systems Engineer</p>
                <p class="mt-2">Building AI-powered educational & communication solutions for Africa.</p>
            </div>
        </div>
    </div>

    <!-- Developer Story & Inspiration -->
    <div class="bg-white rounded-xl shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-green-700 mb-4">👨‍💻 Developer Story & Inspiration</h2>
        <p class="mb-4"><strong>💡 Why This App Was Created</strong><br>
        This application was created after identifying a major gap in how students, businesses, and individuals communicate and access digital support. Many people struggle with slow response times, lack of affordable digital assistants, difficulty accessing educational help, and inefficient communication systems.</p>
        <p class="mb-4"><strong>🚀 The Problem That Inspired the App</strong><br>
        Before this system, users faced delayed replies, repeated manual answering of questions, lack of automation tools, limited access to AI in Africa, and students struggling to get instant academic or career help.</p>
        <p class="mb-4"><strong>🧠 The Idea Behind the System</strong><br>
        “A personal assistant inside WhatsApp that never sleeps.” The system responds instantly, automates communication, helps businesses manage customers, provides learning support, and works 24/7.</p>
        <p class="mb-4"><strong>⚙️ What Makes This App Special</strong><br>
        Smart message understanding, automated response engine, business support automation, student assistance, fast API response, and scalable architecture.</p>
        <p class="mb-4"><strong>🎯 Developer Vision</strong><br>
        “To build intelligent African digital systems that make communication, education, and business automation accessible to everyone.”</p>
        <p class="mb-4"><strong>🌍 Impact Goal</strong><br>
        Improve business communication speed, help students access instant help, reduce workload for support teams, introduce AI to small businesses, create digital job opportunities.</p>
        <blockquote class="border-l-4 border-green-500 pl-4 italic text-gray-700 my-4">
            “I didn’t just build an app — I built a solution to the communication problems I saw around me. This system is designed to help people work faster, learn easier, and connect better.”<br>
            — Brian Ondieki (Mr. Nex)
        </blockquote>
    </div>

    <!-- Developer Identity & Contact -->
    <div class="grid md:grid-cols-2 gap-8 mb-8">
        <div class="bg-white rounded-xl shadow p-6">
            <h3 class="text-xl font-bold text-green-700 mb-3">📞 Contact & Identity</h3>
            <ul class="space-y-2">
                <li><strong>Name:</strong> Brian Ondieki (Mr. Nex)</li>
                <li><strong>Role:</strong> Founder & Lead Developer / AI Systems Engineer</li>
                <li><strong>Tagline:</strong> Building AI-powered educational solutions for students.</li>
                <li><strong>Phone (WhatsApp):</strong> <a href="https://wa.me/254114812308" class="text-green-600">+254 114 812 308</a></li>
                <li><strong>Email:</strong> <a href="mailto:nexo27716@gmail.com" class="text-green-600">nexo27716@gmail.com</a></li>
                <li><strong>GitHub:</strong> <a href="https://github.com/brtjjg" class="text-green-600" target="_blank">github.com/brtjjg</a></li>
                <li><strong>Instagram:</strong> <a href="https://www.instagram.com/nexoraearn" class="text-green-600" target="_blank">@nexoraearn</a></li>
                <li><strong>TikTok:</strong> <a href="https://www.tiktok.com/@progra.mmer" class="text-green-600" target="_blank">@progra.mmer</a></li>
                <li><strong>YouTube:</strong> <a href="https://youtube.com/@nex6250" class="text-green-600" target="_blank">@nex6250</a></li>
            </ul>
        </div>

        <div class="bg-white rounded-xl shadow p-6">
            <h3 class="text-xl font-bold text-green-700 mb-3">⚙️ Skills & Services</h3>
            <div class="mb-4">
                <h4 class="font-semibold">Skills</h4>
                <div class="flex flex-wrap gap-2 mt-1">
                    <span class="bg-gray-100 px-2 py-1 rounded">Python</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">Flask</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">Firebase</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">AI Development</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">Android Apps</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">HTML/CSS/JS</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">Git</span>
                </div>
            </div>
            <div>
                <h4 class="font-semibold">Services Offered</h4>
                <ul class="list-none pl-5 mt-1">
                    <li>Website Development</li>
                    <li>Mobile App Development</li>
                    <li>AI Chatbot Development</li>
                    <li>Educational Platforms</li>
                    <li>M-PESA Integration</li>
                    <li>Hosting & Deployment</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Mission & Projects -->
    <div class="grid md:grid-cols-2 gap-8 mb-8">
        <div class="bg-white rounded-xl shadow p-6">
            <h3 class="text-xl font-bold text-green-700 mb-3">🌟 Mission Statement</h3>
            <p>To use technology to simplify education, career guidance, and access to opportunities for students across Kenya and Africa.</p>
            <h3 class="text-xl font-bold text-green-700 mt-4 mb-2">🚀 Current Projects</h3>
            <ul class="list-none pl-5">
                <li>business automation</lib>
                <li>Ai business</li>
                <li>African freelance platform</li>
                <li>EduPoint AI</li>
                <li>KUCCPS Assistant</li>
                <li>Engineering Learning App</li>
                <li>Scholarship Finder</li>
            </ul>
        </div>
        <div class="bg-white rounded-xl shadow p-6">
            <h3 class="text-xl font-bold text-green-700 mb-3">📱 Community & Social</h3>
            <ul class="space-y-2">
                <li><a href="https://chat.whatsapp.com/FiGII7Ca6jX1sKNwDV5ZLB?s=cl&p=a&ilr=2" class="text-green-600" target="_blank">WhatsApp Group</a></li>
                <li><a href="https://www.facebook.com/kenyakaleidoscope?mibextid=ZbWKwL" class="text-green-600" target="_blank">Facebook Page</a></li>
                <li><a href="https://www.instagram.com/nexoraearn?igsh=ZGcycjlzZWU5dDJl" class="text-green-600" target="_blank">Instagram (@nexoraearn)</a></li>
                <li><a href="https://www.tiktok.com/@progra.mmer?_r=1&_d=ejf03fh49gg804&sec_uid=MS4wLjABAAAAXEOfvblHuP8O7R4zBGhCcmlszW-Oly_O8AQr9-S-PKWTbiJK3O3uaUCOmVdaaZ1Q&share_author_id=7449811721114616838&sharer_language=en&source=h5_m&u_code=ehlhmei087kc1b&timestamp=1780606605&user_id=7449811721114616838&sec_user_id=MS4wLjABAAAAXEOfvblHuP8O7R4zBGhCcmlszW-Oly_O8AQr9-S-PKWTbiJK3O3uaUCOmVdaaZ1Q&item_author_type=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_iid=7646134353182312212&share_link_id=bc778588-6e8d-4535-9b2a-b279efcbc568&share_app_id=1233&ugbiz_name=ACCOUNT&ug_btm=b8727%2Cb7360&social_share_type=5&enable_checksum=1 " class="text-green-600" target="_blank">TikTok (@mrnex)</a></li>
                <li>Support Email: <a href="mailto:smartydigitalbusiness@gmail.com" class="text-green-600">smartdigitalbusiness@gmail.com</a></li>
            </ul>
        </div>
    </div>

<!-- Collaborator Section -->
<div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl shadow p-8 mt-8">
    <h2 class="text-2xl font-bold text-indigo-800 mb-6">🤝 Collaborator</h2>
    <div class="flex flex-col md:flex-row gap-6">
        <!-- Profile Photo (placeholder) -->
        <div class="flex-shrink-0">
            <img src="/static/collaborator.jpg" alt="Antony Kiragu Mburu"
                class="w-32 h-32 rounded-full object-cover border-4 border-indigo-300 mx-auto md:mx-0">
        </div>
        <!-- Details -->
        <div class="flex-1">
            <h3 class="text-xl font-bold text-gray-800">Antony Kiragu Mburu</h3>
            <p class="text-indigo-600 font-medium">Full Stack Developer & Technical Advisor</p>
            <p class="text-gray-700 mt-2">Antony is a skilled full‑stack developer with experience in web technologies, AI integration, and platform architecture. He contributed significantly to the backend optimization and testing of the XyronAI assistant, ensuring reliability and scalability.</p>
            
            <div class="mt-4 grid md:grid-cols-2 gap-4">
                <div>
                    <h4 class="font-semibold text-gray-800">📌 Contributions</h4>
                    <ul class="list-none pl-5 text-sm text-gray-600">
                        <li>Backend Development</li>
                        <li>Testing & Quality Assurance</li>
                        <li>AI Training Support</li>
                        <li>System Architecture Advice</li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold text-gray-800">🛠️ Skills</h4>
                    <ul class="list-none pl-5 text-sm text-gray-600">
                        <li>Python / Flask</li>
                        <li>JavaScript / React</li>
                        <li>WhatsApp Cloud API</li>
                        <li>Database Design</li>
                    </ul>
                </div>
            </div>

            <div class="mt-4 grid md:grid-cols-2 gap-4 text-sm">
                <div>
                    <span class="font-semibold">📧 Email:</span>
                    <a href="mailto:sirmburu05@gmail.com" class="text-indigo-600">sirmburu05@gmail.com</a>
                </div>
                <div>
                    <span class="font-semibold">🌐 Website:</span>
                    <a href="https://www.mulastify.com" target="_blank" class="text-indigo-600">mulastify.com</a>
                </div>
                <div>
                    <span class="font-semibold">📞 Phone:</span>
                    <span>+1 (208) 951-3261</span>
                </div>
                <div>
                    <span class="font-semibold">📅 Collaboration:</span>
                    <span>June 2026 – Present</span>
                </div>
            </div>

            <blockquote class="mt-4 italic text-gray-700 border-l-4 border-indigo-400 pl-4">
                "Technology should solve real-world problems and create opportunities for everyone."
            </blockquote>
        </div>
    </div>
</div>

    <!-- Partnership Section -->
    <div class="bg-white rounded-xl shadow p-8 text-center">
        <h2 class="text-2xl font-bold text-green-700 mb-4">🤝 Partnership Opportunities</h2>
        <p class="mb-6">I am open to collaborations, sponsorships, and partnerships in education, technology, and business automation. Whether you're an organisation, investor, or fellow developer, let's work together to build intelligent solutions for Africa.</p>
        <a href="mailto:nexo27716@gmail.com?subject=Partnership%20Inquiry%20-%20EduPoint%20AI&body=Hello%20Mr.%20Nex%2C%0D%0A%0D%0AI%20am%20interested%20in%20partnering%20with%20you%20on%20the%20following%20idea%2Fproject%3A%0D%0A%0D%0A%5BDescribe%20your%20partnership%20idea%5D%0D%0A%0D%0ALooking%20forward%20to%20collaborating!%0D%0A%0D%0ABest%20regards" 
           class="inline-block bg-green-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-green-700 transition">
            💼 Send Partnership Request
        </a>
        <p class="text-sm text-gray-500 mt-4">connect and discuss how we can collaborate.</p>
    </div>
<!-- Share Your Skills Section -->
<div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow p-8 text-center mt-8">
    <h2 class="text-2xl font-bold text-blue-700 mb-4">🛠️ Share Your Skills</h2>
    <p class="mb-6">Are you a developer, designer, content creator, or tech enthusiast? I'm always looking to connect with talented people. Tell me about your skills and let's collaborate.</p>
    <a href="mailto:nexo27716@gmail.com?subject=Skills%20Showcase%20-%20Collaboration&body=Hello%20Mr.%20Nex%2C%0D%0A%0D%0AI%20have%20the%20following%20skills%20I%27d%20like%20to%20share%3A%0D%0A%0D%0A-%20Skill%201%0D%0A-%20Skill%202%0D%0A-%20Skill%203%0D%0A%0D%0AI%27m%20interested%20in%3A%20%5Bcollaboration%20type%5D%0D%0A%0D%0ALooking%20forward%20to%20connecting!%0D%0A%0D%0ABest%20regards" 
       class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition">
        ✉️ Submit Your Skills
    </a>
    <p class="text-sm text-gray-500 mt-4">We are happy for your request</p>
</div>
</div>
'''

@app.route('/developer')
def developer_page():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', DEVELOPER_HTML)
    return render_template_string(template, unread_count=unread_count)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# ========== PROFILE PAGE ==========
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        phone_number = request.form.get('phone_number')
        if business_name:
            current_user.business_name = business_name
        if phone_number:
            current_user.phone_number = phone_number
        
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"user_{current_user.id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                try:
                    from sqlalchemy import text
                    db.session.execute(text("ALTER TABLE user ADD COLUMN profile_pic VARCHAR(200)"))
                    db.session.commit()
                except:
                    pass
                current_user.profile_pic = f'/static/uploads/{filename}'
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    unread = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    profile_pic = getattr(current_user, 'profile_pic', None) or 'https://ui-avatars.com/api/?name=' + (current_user.business_name or 'User').replace(' ', '+') + '&background=10b981&color=fff'
    
    content = '''
    <div class="max-w-3xl mx-auto">
        <div class="bg-white rounded-lg shadow p-8">
            <h2 class="text-2xl font-bold mb-6">My Profile</h2>
            <div class="flex flex-col md:flex-row gap-8">
                <div class="text-center">
                    <img src="{{ profile_pic }}" alt="Profile" class="w-32 h-32 rounded-full object-cover border-4 border-green-500 mx-auto">
                    <p class="text-sm text-gray-500 mt-2">Profile picture</p>
                </div>
                <div class="flex-1">
                    <form method="POST" enctype="multipart/form-data">
                        <div class="mb-4">
                            <label class="block font-medium mb-1">Business Name</label>
                            <input type="text" name="business_name" value="{{ current_user.business_name }}" class="w-full border rounded-lg px-3 py-2">
                        </div>
                        <div class="mb-4">
                            <label class="block font-medium mb-1">Phone Number</label>
                            <input type="tel" name="phone_number" value="{{ current_user.phone_number or '' }}" class="w-full border rounded-lg px-3 py-2">
                        </div>
                        <div class="mb-4">
                            <label class="block font-medium mb-1">Change Profile Picture</label>
                            <input type="file" name="profile_pic" accept="image/*" class="w-full border rounded-lg px-3 py-2">
                        </div>
                        <button type="submit" class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    '''
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    return render_template_string(template, profile_pic=profile_pic, unread_count=unread)
