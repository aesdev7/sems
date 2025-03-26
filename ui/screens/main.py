# File: main.py
# SEMS Application Entry Point

from kivy.app import App
from kivy.uix.label import Label

class SEMSApp(App):
    """Main application class for Security & Emergency Management"""
    def build(self):
        self.title = "SEMS - Security & Emergency Mgmt"
        self.icon = 'assets/images/sems_icon.png'
        return Label(text='Initializing SEMS...')

if __name__ == '__main__':
    SEMSApp().run()