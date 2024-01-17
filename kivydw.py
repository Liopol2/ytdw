from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import options
from icecream import ic

class DownloaderApp(App):
    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Output Label and Dropdown
        output_label = Label(text='Output:')
        output_dropdown = Spinner(
            text='Select Output',  # default selection
            values=('Audio' , 'Video')
        )
        
        audioquality = Spinner(
            text='160kbps(webm)',  # default selection
            values=options.audioqualityoptions
        )
        
        videoquality = Spinner(
            text='Highest',  # default selection
            values=options.videoqualityoptions
        )      

        # Quality Label and Dropdown
        quality_label = Label(text='Quality:')
        
        # Text Entry
        text_entry = TextInput(hint_text='Enter text', multiline=False)

        # Additional Label
        additional_label = Label(text='Additional Label')

        # Adding widgets to the main layout
        main_layout.add_widget(output_label)
        main_layout.add_widget(output_dropdown)
        main_layout.add_widget(quality_label)        
        main_layout.add_widget(audioquality)
        main_layout.add_widget(videoquality)
        main_layout.add_widget(text_entry)
        main_layout.add_widget(additional_label)
        
        # Function to retrieve the selected value from Output Dropdown
        def on_output_spinner_select(spinner, text):
            ic(f"Selected Output:{text}")
            if text == 'Audio':                    
                hide_widget(audioquality,False)
                hide_widget(videoquality)
            if text == 'Video':
                hide_widget(audioquality)
                hide_widget(videoquality,False)
                
        output_dropdown.bind(text=on_output_spinner_select)        

        def hide_widget(wid, dohide=True):
            if hasattr(wid, 'saved_attrs'):
                if not dohide:
                    wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                    del wid.saved_attrs
            elif dohide:
                wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

        return main_layout

if __name__ == '__main__':
    DownloaderApp().run()
