

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition, 
SlideTransition, CardTransition, SwapTransition, 
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)  
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from imutils.video import VideoStream
import imutils
import time
import cv2

import detect_mask_video as det

width = 375
height = 667

users = {
    "billybob": [12345, 3]
}


c1 = Color(65/255,65/255,70/255)
c2 = Color(40/255,40/255,42/255)


Config.set('graphics', 'resizable', '0') 
Config.set('graphics', 'width', '375')  
Config.set('graphics', 'height', '667')

class SignUpScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        
        self.add_widget(
            Label(
                text="SIGN UP",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        self.add_widget(
            Label(
                text="Username",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.6}))
        
        self.add_widget(
            Label(
                text="Password",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.55}))
        
        self.add_widget(
            TextInput(
                password = False,
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.7, 'center_y': 0.6}))
        
        self.add_widget(
            TextInput(
                password = True,
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.7, 'center_y': 0.55}))
        
        self.add_widget(
            Button(
                text="Submit",
                size_hint=(0.4, 0.05),
                background_normal = '',
                background_color = (48/255,48/255,54/255,1),
                on_press = self.switchMask,
                pos_hint={'center_x': 0.5, 'center_y': 0.45}))
        
        self.add_widget(
            Label(
                text="Already have an Account?",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        
        self.add_widget(
            Button(
                text="Login Here",
                size_hint=(0.4, 0.05),
                background_normal = '',
                background_color = (65/255,65/255,70/255,1),
                color = (75/255,133/255,227/255,1),
                on_press = self.switchLogin,
                pos_hint={'center_x': 0.75, 'center_y': 0.05}))
        
    
    
    def switchMask(self, instance):
        sm.current = 'mask'
        
    def switchLogin(self, instance):
        sm.current = 'login'
    
class MaskScreen(Screen, BoxLayout):  
    def __init__(self, **kwargs):
        super(MaskScreen, self).__init__(**kwargs)
        self.img1=Image()
        self.add_widget(self.img1)
        self.increment = 0
        #opencv2 stuffs
        self.vs = VideoStream(src=0).start()
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, dt):
        
        # display image from cam in opencv window
        frame = self.vs.read()
        #frame = imutils.resize(frame, width=400)
        
        (locs, preds) = det.detect_and_predict_mask(frame, det.faceNet, det.maskNet)
        self.add_widget(
                    Button(
                    size_hint=(0.8, 0.01),
                    background_normal = '',
                    background_color = (40/255,40/255,42/255 ,1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.2}))
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
    
            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            if self.increment > 10:
                Clock.unschedule(self.update)
                self.vs.stop()
                self.add_widget(
                    Button(
                    size_hint=(0.8/11*self.increment, 0.01),
                    background_normal = '',
                    background_color = (69/255,184/255,59/255 ,1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.2}))
                self.add_widget(
                    Button(
                        text="Submit",
                    size_hint=(0.4, 0.05),
                    background_normal = '',
                    background_color = (48/255,48/255,54/255,1),
                    on_press = self.switchHome,
                    pos_hint={'center_x': 0.5, 'center_y': 0.1}))
                
            elif label == "Mask":
                self.increment += 1
                self.add_widget(
                    Button(
                    size_hint=(0.8/11*self.increment, 0.01),
                    background_normal = '',
                    background_color = (69/255,184/255,59/255 ,1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.2}))

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


        
        #cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1    
        
    def switchHome(self, instance):
        sm.current = 'home'

class HealthScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(HealthScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        
        self.add_widget(
            Label(
                text="HEALTH TIPS",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'accountIconA.png', 
                on_press = self.switchAccount,
                pos_hint={'center_x': 0.1, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'shopIconA.png', 
                on_press = self.switchShop,
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 1, 1, 1), 
                background_normal = 'friendsIconA.png', 
                on_press = self.switchFriends,
                pos_hint={'center_x': 0.7, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                background_normal = 'healthIconB.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 85),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'bloomA.png', 
                on_press = self.switchHome,
                pos_hint={'center_x': 0.5, 'center_y': 0.05}))
        
             
        
    def switchHome(self, instance):
        sm.current = 'home'
    def switchSignUp(self, instance):
        sm.current = 'signup'
    def switchAccount(self, instance):
        sm.current = 'account'
    def switchShop(self, instance):
        sm.current = 'shop'
    def switchFriends(self, instance):
        sm.current = 'friends'
    def switchHealth(self, instance):
        sm.current = 'health'

class AccountScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        
        self.add_widget(
            Label(
                text="ACCOUNT",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'accountIconB.png', 
                on_press = self.switchAccount,
                pos_hint={'center_x': 0.1, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'shopIconA.png', 
                on_press = self.switchShop,
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 1, 1, 1), 
                background_normal = 'friendsIconA.png', 
                on_press = self.switchFriends,
                pos_hint={'center_x': 0.7, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                background_normal = 'healthIconA.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 85),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'bloomA.png', 
                on_press = self.switchHome,
                pos_hint={'center_x': 0.5, 'center_y': 0.05}))
        
             
        
    def switchHome(self, instance):
        sm.current = 'home'
    def switchSignUp(self, instance):
        sm.current = 'signup'
    def switchAccount(self, instance):
        sm.current = 'account'
    def switchShop(self, instance):
        sm.current = 'shop'
    def switchFriends(self, instance):
        sm.current = 'friends'
    def switchHealth(self, instance):
        sm.current = 'health'

class ShopScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(ShopScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        
        self.add_widget(
            Label(
                text="STORE",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        self.add_widget(
            Button(
                size=(50, 85),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'bloomA.png', 
                on_press = self.switchHome,
                pos_hint={'center_x': 0.5, 'center_y': 0.05}))
        
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'accountIconA.png', 
                on_press = self.switchAccount,
                pos_hint={'center_x': 0.1, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'shopIconB.png', 
                on_press = self.switchShop,
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 1, 1, 1), 
                background_normal = 'friendsIconA.png', 
                on_press = self.switchFriends,
                pos_hint={'center_x': 0.7, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                background_normal = 'healthIconA.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        
             
        
    def switchHome(self, instance):
        sm.current = 'home'
    def switchSignUp(self, instance):
        sm.current = 'signup'
    def switchAccount(self, instance):
        sm.current = 'account'
    def switchShop(self, instance):
        sm.current = 'shop'
    def switchFriends(self, instance):
        sm.current = 'friends'
    def switchHealth(self, instance):
        sm.current = 'health'

class HomeScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))

        self.add_widget(
            Label(
                text="FIND LANDMARK",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        
        self.add_widget(
            Button(
                text="Upload Image",
                size_hint=(0.4, 0.05),
                background_normal = '',
                background_color = (247/255,190/255,59/255,1),
                color = (0,0,0,1),
                on_press = self.uploadImage,
                pos_hint={'center_x': 0.5, 'center_y': 0.4}))
        
        
        self.add_widget(
            Button(
                size=(50, 85),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'bloomB.png', 
                on_press = self.switchHome,
                pos_hint={'center_x': 0.5, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'accountIconA.png', 
                on_press = self.switchAccount,
                pos_hint={'center_x': 0.1, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'shopIconA.png', 
                on_press = self.switchShop,
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 1, 1, 1), 
                background_normal = 'friendsIconA.png', 
                on_press = self.switchFriends,
                pos_hint={'center_x': 0.7, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                background_normal = 'healthIconA.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        
    
    
    def switchHome(self, instance):
        sm.current = 'home'
    def switchSignUp(self, instance):
        sm.current = 'signup'
    def switchAccount(self, instance):
        sm.current = 'account'
    def switchShop(self, instance):
        sm.current = 'shop'
    def switchFriends(self, instance):
        sm.current = 'friends'
    def switchHealth(self, instance):
        sm.current = 'health'
    def uploadImage(self, instance):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
    

class FriendsScreen(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(FriendsScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        
        self.add_widget(
            Label(
                text="FRIENDS LIST",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        
        self.add_widget(
            Button(
                size=(50, 85),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'bloomA.png', 
                on_press = self.switchHome,
                pos_hint={'center_x': 0.5, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'accountIconA.png', 
                on_press = self.switchAccount,
                pos_hint={'center_x': 0.1, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 0, .65, 1), 
                background_normal = 'shopIconA.png', 
                on_press = self.switchShop,
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                color =(1, 1, 1, 1), 
                background_normal = 'friendsIconB.png', 
                on_press = self.switchFriends,
                pos_hint={'center_x': 0.7, 'center_y': 0.05}))
        self.add_widget(
            Button(
                size=(50, 50),
                size_hint = (None, None),
                background_normal = 'healthIconA.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        
        
        
    def switchHome(self, instance):
        sm.current = 'home'
    def switchSignUp(self, instance):
        sm.current = 'signup'
    def switchAccount(self, instance):
        sm.current = 'account'
    def switchShop(self, instance):
        sm.current = 'shop'
    def switchFriends(self, instance):
        sm.current = 'friends'
    def switchHealth(self, instance):
        sm.current = 'health'

class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super(IntroScreen, self).__init__(**kwargs)




class LoginScreen(Screen, FloatLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.canvas.add(c1)
        self.canvas.add(Rectangle(size=(width, height)))
        self.add_widget(
            Button(
                size=(100, 50),
                size_hint = (None, None),
                background_normal = 'bloomLogoA.png', 
                on_press = self.switchHealth,
                pos_hint={'center_x': 0.9, 'center_y': 0.05}))
        self.add_widget(
            Label(
                text="LOG IN",
                font_size='30sp',
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        self.add_widget(
            Label(
                text="Username",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.6}))
        
        self.add_widget(
            Label(
                text="Password",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.55}))
        
        self.add_widget(
            TextInput(
                password = False,
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.7, 'center_y': 0.6}))
        
        self.add_widget(
            TextInput(
                password = True,
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.7, 'center_y': 0.55}))
        
        self.add_widget(
            Button(
                text="Submit",
                size_hint=(0.4, 0.05),
                background_normal = '',
                background_color = (48/255,48/255,54/255,1),
                on_press = self.switchMask,
                pos_hint={'center_x': 0.5, 'center_y': 0.45}))
        
        self.add_widget(
            Label(
                text="Don't have an Account?",
                size_hint=(0.4, 0.05),
                pos_hint={'center_x': 0.3, 'center_y': 0.05}))
        
        self.add_widget(
            Button(
                text="Create Account Here",
                size_hint=(0.4, 0.05),
                background_normal = '',
                background_color = (65/255,65/255,70/255,1),
                color = (75/255,133/255,227/255,1),
                on_press = self.switchSignUp,
                pos_hint={'center_x': 0.75, 'center_y': 0.05}))

        
    
    
    def switchMask(self, instance):
        
        sm.current = 'mask'
    def switchSignUp(self, instance):
        sm.current = 'signup'




sm = ScreenManager()
sm.transition = FadeTransition()
sm.add_widget(LoginScreen(name ='login'))    
sm.add_widget(HomeScreen(name ='home')) 
sm.add_widget(SignUpScreen(name ='signup')) 
sm.add_widget(FriendsScreen(name ='friends')) 
sm.add_widget(HealthScreen(name ='health')) 
sm.add_widget(ShopScreen(name ='shop')) 
sm.add_widget(AccountScreen(name ='account')) 
sm.add_widget(MaskScreen(name ='mask')) 

sm.current = 'login'

class MyApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()