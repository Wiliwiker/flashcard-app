from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import json
import os


class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.background_normal = ''
        self.font_size = dp(16)
        self.bold = True
        self.color = get_color_from_hex('#FFFFFF')
        
        with self.canvas.before:
            Color(*get_color_from_hex('#4A6572'))
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PrimaryButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex('#F9AA33'))  # Orange
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )


class SecondaryButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex('#4A6572'))  # Dark blue-gray
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )


class DangerButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex('#E53935'))  # Red
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )


class StyledLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = get_color_from_hex('#344955')  # Dark blue
        self.halign = 'center'
        self.valign = 'middle'


class TitleLabel(StyledLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = dp(28)
        self.bold = True
        self.color = get_color_from_hex('#232F34')  # Darker blue


class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 1)
        self.background_normal = ''
        self.background_active = ''
        self.foreground_color = get_color_from_hex('#344955')
        self.font_size = dp(16)
        self.padding = [dp(15), dp(15)]
        self.multiline = True
        
        with self.canvas.before:
            Color(*get_color_from_hex('#B0BEC5'))  # Light gray border
            self.rect = RoundedRectangle(
                radius=[dp(5), dp(5), dp(5), dp(5)],
                size=self.size,
                pos=self.pos
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CardWidget(BoxLayout):
    def __init__(self, card, index, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(10)
        
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))  # White background
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )
            Color(*get_color_from_hex('#F9AA33'), a=0.1)  # Light orange border
            self.border = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=(self.size[0]-2, self.size[1]-2),
                pos=(self.pos[0]+1, self.pos[1]+1)
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Card content
        content_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        question_label = StyledLabel(
            text=f"Q: {card.question[:50]}{'...' if len(card.question) > 50 else ''}",
            font_size=dp(16),
            bold=True,
            size_hint_y=0.5
        )
        content_layout.add_widget(question_label)
        
        answer_label = StyledLabel(
            text=f"A: {card.answer[:50]}{'...' if len(card.answer) > 50 else ''}",
            font_size=dp(14),
            size_hint_y=0.5
        )
        content_layout.add_widget(answer_label)
        
        self.add_widget(content_layout)
        
        # Delete button
        delete_btn = DangerButton(
            text='Delete',
            size_hint_x=0.3
        )
        delete_btn.bind(on_press=lambda x: delete_callback(index))
        self.add_widget(delete_btn)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.size = (self.size[0]-2, self.size[1]-2)
        self.border.pos = (self.pos[0]+1, self.pos[1]+1)


class FlashCard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


class FlashCardManager:
    def __init__(self):
        self.cards = []
        self.current_index = 0
        self.data_file = 'flashcards.json'
        self.load_cards()
    
    def add_card(self, question, answer):
        self.cards.append(FlashCard(question, answer))
        self.save_cards()
    
    def delete_card(self, index):
        if 0 <= index < len(self.cards):
            self.cards.pop(index)
            # Adjust current index if needed
            if self.current_index >= len(self.cards) and len(self.cards) > 0:
                self.current_index = len(self.cards) - 1
            elif len(self.cards) == 0:
                self.current_index = 0
            self.save_cards()
    
    def get_current_card(self):
        if self.cards:
            return self.cards[self.current_index]
        return None
    
    def next_card(self):
        if self.cards:
            self.current_index = (self.current_index + 1) % len(self.cards)
    
    def prev_card(self):
        if self.cards:
            self.current_index = (self.current_index - 1) % len(self.cards)
    
    def save_cards(self):
        data = [{'question': card.question, 'answer': card.answer} for card in self.cards]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_cards(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.cards = [FlashCard(item['question'], item['answer']) for item in data]
            except:
                self.cards = []


class HomeScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))  # Light gray background
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title
        title = TitleLabel(text='Flashcard Master', size_hint=(1, 0.2))
        main_layout.add_widget(title)
        
        # Stats
        stats_label = StyledLabel(
            text=f'Total Cards: {len(self.manager_ref.cards)}',
            font_size=dp(18),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(stats_label)
        
        # Buttons
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.7))
        
        study_btn = PrimaryButton(text='Study Cards', size_hint=(1, 0.25))
        study_btn.bind(on_press=self.go_to_study)
        button_layout.add_widget(study_btn)
        
        add_btn = SecondaryButton(text='Add New Card', size_hint=(1, 0.25))
        add_btn.bind(on_press=self.go_to_add)
        button_layout.add_widget(add_btn)
        
        manage_btn = SecondaryButton(text='Manage Cards', size_hint=(1, 0.25))
        manage_btn.bind(on_press=self.go_to_manage)
        button_layout.add_widget(manage_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        # Update stats when entering the home screen
        stats_label = self.children[0].children[1]  # Get the stats label
        stats_label.text = f'Total Cards: {len(self.manager_ref.cards)}'
    
    def go_to_study(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'study'
        self.manager.get_screen('study').update_card()
    
    def go_to_add(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'add'
    
    def go_to_manage(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'manage'
        self.manager.get_screen('manage').refresh_list()


class StudyScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        self.show_answer = False
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Progress indicator
        self.progress_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.progress_label)
        
        # Card display
        card_container = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        
        with card_container.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.card_bg = RoundedRectangle(
                radius=[dp(15), dp(15), dp(15), dp(15)],
                size=card_container.size,
                pos=card_container.pos
            )
        card_container.bind(pos=self.update_card_bg, size=self.update_card_bg)
        
        self.card_label = StyledLabel(
            text='No cards available.\nAdd some cards to start studying!',
            font_size=dp(20),
            text_size=(Window.width - dp(80), None)
        )
        self.card_label.bind(texture_size=self.update_text_size)
        card_container.add_widget(self.card_label)
        
        main_layout.add_widget(card_container)
        
        # Flip button
        flip_btn = PrimaryButton(text='Show Answer', size_hint=(1, 0.15))
        flip_btn.bind(on_press=self.flip_card)
        main_layout.add_widget(flip_btn)
        
        # Navigation
        nav_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        
        prev_btn = SecondaryButton(text='Previous')
        prev_btn.bind(on_press=self.prev_card)
        nav_layout.add_widget(prev_btn)
        
        next_btn = PrimaryButton(text='Next')
        next_btn.bind(on_press=self.next_card)
        nav_layout.add_widget(next_btn)
        
        main_layout.add_widget(nav_layout)
        
        # Back button
        back_btn = SecondaryButton(text='Back to Home', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_home)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_card_bg(self, instance, value):
        self.card_bg.pos = instance.pos
        self.card_bg.size = instance.size
    
    def update_text_size(self, instance, value):
        instance.text_size = (Window.width - dp(80), None)
    
    def update_card(self):
        self.show_answer = False
        card = self.manager_ref.get_current_card()
        if card:
            self.card_label.text = card.question
            self.update_progress()
        else:
            self.card_label.text = "No cards available.\nAdd some cards to start studying!"
            self.progress_label.text = ""
    
    def update_progress(self):
        if self.manager_ref.cards:
            current = self.manager_ref.current_index + 1
            total = len(self.manager_ref.cards)
            self.progress_label.text = f"Card {current} of {total}"
    
    def flip_card(self, instance):
        card = self.manager_ref.get_current_card()
        if card:
            self.show_answer = not self.show_answer
            if self.show_answer:
                self.card_label.text = card.answer
                instance.text = 'Show Question'
            else:
                self.card_label.text = card.question
                instance.text = 'Show Answer'
    
    def next_card(self, instance):
        self.manager_ref.next_card()
        self.update_card()
    
    def prev_card(self, instance):
        self.manager_ref.prev_card()
        self.update_card()
    
    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'


class AddCardScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title
        title = TitleLabel(text='Add New Card', size_hint=(1, 0.1))
        main_layout.add_widget(title)
        
        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.8))
        
        # Question
        form_layout.add_widget(StyledLabel(text='Question:', size_hint=(1, 0.1)))
        self.question_input = StyledTextInput(
            hint_text='Enter your question here...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.question_input)
        
        # Answer
        form_layout.add_widget(StyledLabel(text='Answer:', size_hint=(1, 0.1)))
        self.answer_input = StyledTextInput(
            hint_text='Enter the answer here...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.answer_input)
        
        main_layout.add_widget(form_layout)
        
        # Buttons
        button_layout = BoxLayout(spacing=dp(10), size_hint=(1, 0.1))
        
        back_btn = SecondaryButton(text='Cancel')
        back_btn.bind(on_press=self.go_home)
        button_layout.add_widget(back_btn)
        
        save_btn = PrimaryButton(text='Save Card')
        save_btn.bind(on_press=self.save_card)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def save_card(self, instance):
        question = self.question_input.text.strip()
        answer = self.answer_input.text.strip()
        
        if question and answer:
            self.manager_ref.add_card(question, answer)
            self.question_input.text = ''
            self.answer_input.text = ''
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
    
    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'


class ManageCardsScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title
        title = TitleLabel(text='Manage Cards', size_hint=(1, 0.1))
        main_layout.add_widget(title)
        
        # Scroll view for cards
        scroll = ScrollView(size_hint=(1, 0.8))
        self.cards_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.cards_layout.bind(minimum_height=self.cards_layout.setter('height'))
        scroll.add_widget(self.cards_layout)
        main_layout.add_widget(scroll)
        
        # Back button
        back_btn = SecondaryButton(text='Back to Home', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_home)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def refresh_list(self):
        self.cards_layout.clear_widgets()
        self.cards_layout.height = 0
        
        if not self.manager_ref.cards:
            no_cards_label = StyledLabel(
                text='No cards yet.\nAdd some cards to get started!',
                font_size=dp(18)
            )
            self.cards_layout.add_widget(no_cards_label)
            return
        
        for i, card in enumerate(self.manager_ref.cards):
            card_widget = CardWidget(card, i, self.delete_card)
            self.cards_layout.add_widget(card_widget)
            self.cards_layout.height += card_widget.height + dp(10)
    
    def delete_card(self, index):
        self.manager_ref.delete_card(index)
        self.refresh_list()
    
    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'


class FlashcardApp(App):
    def build(self):
        self.title = 'Flashcard Master'
        self.card_manager = FlashCardManager()
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(self.card_manager, name='home'))
        sm.add_widget(StudyScreen(self.card_manager, name='study'))
        sm.add_widget(AddCardScreen(self.card_manager, name='add'))
        sm.add_widget(ManageCardsScreen(self.card_manager, name='manage'))
        
        return sm


if __name__ == '__main__':
    FlashcardApp().run()