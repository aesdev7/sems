# File: ui/screens/login_screen.py
# SEMS Authentication Interface

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from core.auth import authenticate

class LoginScreen(Screen):
    """SEMS user authentication screen"""
    status = StringProperty("Ready")
    
    def verify_credentials(self, username, password):
        """Handle SEMS login attempts"""
        if authenticate(username, password):
            self.status = "Access granted"
            self.manager.current = 'dashboard'
        else:
            self.status = "Invalid credentials"
