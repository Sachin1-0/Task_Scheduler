from flask_mail import Message
from flask import render_template, current_app, url_for
from app import mail
from threading import Thread
from itsdangerous import URLSafeTimedSerializer

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def get_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id}, salt='password-reset-salt')

def verify_reset_token(token, expires_sec=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
    except:
        return None
    from app.models import User
    return User.query.get(data['user_id'])

def send_password_reset_email(user):
    token = get_reset_token(user)
    text_body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    html_body = f'''<p>To reset your password, visit the following link:</p>
<p><a href="{url_for('auth.reset_token', token=token, _external=True)}">Reset Password</a></p>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
'''
    send_email('[Task Scheduler] Reset Your Password',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=text_body,
               html_body=html_body)

def get_verification_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id}, salt='email-verify-salt')

def verify_email_token(token, expires_sec=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt='email-verify-salt', max_age=expires_sec)
    except:
        return None
    from app.models import User
    return User.query.get(data['user_id'])

def send_verification_email(user):
    token = get_verification_token(user)
    text_body = f'''To verify your email address, visit the following link:
{url_for('auth.verify_email', token=token, _external=True)}

If you did not register for an account then simply ignore this email.
'''
    html_body = f'''<p>To verify your email address, visit the following link:</p>
<p><a href="{url_for('auth.verify_email', token=token, _external=True)}">Verify Email</a></p>
<p>If you did not register for an account then simply ignore this email.</p>
'''
    send_email('[Task Scheduler] Verify Your Email',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=text_body,
               html_body=html_body)
