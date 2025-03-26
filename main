from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config

# Set window size (optional for desktop)
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Window.size = (1024, 768)

# Import screen KV files
Builder.load_file('screens/login.kv')
Builder.load_file('screens/dashboard.kv')
Builder.load_file('screens/personnel.kv')
Builder.load_file('screens/threats.kv')

# Screen Classes
class LoginScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class PersonnelScreen(Screen):
    pass

class ThreatsScreen(Screen):
    pass

# Screen Manager
class SEMSScreenManager(ScreenManager):
    pass

# Main App Class
class SEMSApp(App):
    def build(self):
        self.title = 'Aviation Security Management System (SEMS)'
        self.icon = 'assets/icons/security-icon.png'  # Add your icon
        
        sm = SEMSScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(PersonnelScreen(name='personnel'))
        sm.add_widget(ThreatsScreen(name='threats'))
        
        return sm

    def on_start(self):
        # Initialize database connection here if needed
        pass

if __name__ == '__main__':
    SEMSApp().run()
