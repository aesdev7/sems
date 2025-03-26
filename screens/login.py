# screens/login.kv
<LoginScreen>:
    canvas.before:
        Color:
            rgba: 0.96, 0.96, 0.96, 1  # Light gray background
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.1, 0.5, 0.8, 1  # Blue accent
        Rectangle:
            pos: 0, self.height*0.7
            size: self.width, self.height*0.3

    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.8, 0.8

        # Logo/Header
        BoxLayout:
            size_hint_y: 0.3
            orientation: 'vertical'
            spacing: 10
            
            Image:
                source: 'assets/images/logo.png'
                size_hint: (0.5, 0.5)
                pos_hint: {'center_x': 0.5}
            
            Label:
                text: 'AVIATION SECURITY SYSTEM'
                font_size: 24
                bold: True
                color: 1, 1, 1, 1
                halign: 'center'

        # Login Form
        BoxLayout:
            orientation: 'vertical'
            spacing: 15
            size_hint_y: 0.5
            padding: [30, 0, 30, 0]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                Line:
                    width: 1
                    rectangle: self.x, self.y, self.width, self.height

            Label:
                text: 'PLEASE LOGIN'
                font_size: 18
                bold: True
                color: 0.2, 0.2, 0.2, 1
                size_hint_y: None
                height: 30

            TextInput:
                id: username
                hint_text: 'Username'
                size_hint_y: None
                height: 50
                padding: 10
                multiline: False
                background_normal: ''
                background_color: 0.95, 0.95, 0.95, 1
                cursor_color: 0.1, 0.5, 0.8, 1

            TextInput:
                id: password
                hint_text: 'Password'
                size_hint_y: None
                height: 50
                padding: 10
                password: True
                multiline: False
                background_normal: ''
                background_color: 0.95, 0.95, 0.95, 1
                cursor_color: 0.1, 0.5, 0.8, 1

            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 10

                CheckBox:
                    size_hint_x: None
                    width: 30
                    active: False
                    on_active: root.remember_me = self.active

                Label:
                    text: 'Remember me'
                    color: 0.4, 0.4, 0.4, 1

                Widget:  # Spacer
                    size_hint_x: 0.5

                Button:
                    text: 'Forgot Password?'
                    size_hint_x: None
                    width: 150
                    background_color: 0, 0, 0, 0
                    color: 0.1, 0.5, 0.8, 1
                    bold: True
                    on_release: root.forgot_password()

        # Login Button
        Button:
            text: 'LOGIN'
            size_hint_y: None
            height: 60
            background_color: 0.1, 0.5, 0.
