#Robust authentication implementation with H
#JWT authentication role-based access control.

import jwt
from datetime import datetime, timedelta
from functools import wraps
from kivy.app import App
from database.models import User
from database.db_connector import db
from kivy.clock import Clock
import bcrypt
from jwt.exceptions import InvalidTokenError

class AuthManager:
    def __init__(self):
        self.secret_key = self._load_secret_key()
        self.token_expiry = timedelta(hours=8)  # Session duration
        self.current_user = None

    def _load_secret_key(self):
        """Load secret key from environment or config file"""
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            return os.getenv('JWT_SECRET', 'fallback-secret-key-for-dev')
        except:
            return 'fallback-secret-key-for-dev'

    def authenticate(self, username, password):
        """Verify credentials and return JWT token"""
        with db.session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                return None
            
            if not user.is_active:
                raise AccountDisabledError("Account is disabled")
            
            self.current_user = user
            token = self._generate_token(user)
            self._schedule_token_refresh(token)
            return token

    def _generate_token(self, user):
        """Generate JWT token with user claims"""
        payload = {
            'sub': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def _schedule_token_refresh(self, token):
        """Schedule token refresh 5 minutes before expiry"""
        payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        expiry = datetime.fromtimestamp(payload['exp'])
        refresh_time = expiry - timedelta(minutes=5)
        
        def refresh_token(dt):
            if self.current_user:
                new_token = self._generate_token(self.current_user)
                App.get_running_app().dispatch('on_token_refresh', new_token)
        
        Clock.schedule_once(refresh_token, (refresh_time - datetime.utcnow()).total_seconds())

    def verify_token(self, token):
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            with db.session_scope() as session:
                user = session.query(User).get(payload['sub'])
                if not user or not user.is_active:
                    raise InvalidTokenError("User not found or inactive")
                self.current_user = user
                return user
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Session expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")

    def role_required(self, *allowed_roles):
        """Decorator for role-based access control"""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if not self.current_user:
                    raise AuthenticationError("Not authenticated")
                if self.current_user.role.value not in [r.value for r in allowed_roles]:
                    raise PermissionError("Insufficient privileges")
                return f(*args, **kwargs)
            return wrapped
        return decorator

    def logout(self):
        """Clear current session"""
        self.current_user = None
        App.get_running_app().dispatch('on_logout')

# Custom Exceptions
class AuthenticationError(Exception): pass
class TokenExpiredError(AuthenticationError): pass
class InvalidTokenError(AuthenticationError): pass
class AccountDisabledError(AuthenticationError): pass
class PermissionError(AuthenticationError): pass

# Singleton instance
auth_manager = AuthManager()

# Kivy Event Handlers
def on_token_refresh(new_token):
    """Update stored token in app"""
    app = App.get_running_app()
    if hasattr(app, 'store'):
        app.store.put('auth', token=new_token)

def on_logout():
    """Clear auth data on logout"""
    app = App.get_running_app()
    if hasattr(app, 'store'):
        app.store.delete('auth')
