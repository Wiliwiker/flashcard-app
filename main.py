from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import json
import os


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
            json.dump(data, f)
    
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
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Flashcard App', font_size='24sp', size_hint=(1, 0.2))
        layout.add_widget(title)
        
        study_btn = Button(text='Study Cards', size_hint=(1, 0.2))
        study_btn.bind(on_press=self.go_to_study)
        layout.add_widget(study_btn)
        
        add_btn = Button(text='Add New Card', size_hint=(1, 0.2))
        add_btn.bind(on_press=self.go_to_add)
        layout.add_widget(add_btn)
        
        manage_btn = Button(text='Manage Cards', size_hint=(1, 0.2))
        manage_btn.bind(on_press=self.go_to_manage)
        layout.add_widget(manage_btn)
        
        self.add_widget(layout)
    
    def go_to_study(self, instance):
        self.manager.current = 'study'
        self.manager.get_screen('study').update_card()
    
    def go_to_add(self, instance):
        self.manager.current = 'add'
    
    def go_to_manage(self, instance):
        self.manager.current = 'manage'
        self.manager.get_screen('manage').refresh_list()


class StudyScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        self.show_answer = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.card_label = Label(text='No cards available', font_size='20sp', size_hint=(1, 0.5))
        layout.add_widget(self.card_label)
        
        flip_btn = Button(text='Show Answer', size_hint=(1, 0.15))
        flip_btn.bind(on_press=self.flip_card)
        layout.add_widget(flip_btn)
        
        nav_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        prev_btn = Button(text='Previous')
        prev_btn.bind(on_press=self.prev_card)
        nav_layout.add_widget(prev_btn)
        
        next_btn = Button(text='Next')
        next_btn.bind(on_press=self.next_card)
        nav_layout.add_widget(next_btn)
        layout.add_widget(nav_layout)
        
        back_btn = Button(text='Back to Home', size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_home)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def update_card(self):
        self.show_answer = False
        card = self.manager_ref.get_current_card()
        if card:
            self.card_label.text = f"Q: {card.question}"
        else:
            self.card_label.text = "No cards available"
    
    def flip_card(self, instance):
        card = self.manager_ref.get_current_card()
        if card:
            self.show_answer = not self.show_answer
            if self.show_answer:
                self.card_label.text = f"A: {card.answer}"
            else:
                self.card_label.text = f"Q: {card.question}"
    
    def next_card(self, instance):
        self.manager_ref.next_card()
        self.update_card()
    
    def prev_card(self, instance):
        self.manager_ref.prev_card()
        self.update_card()
    
    def go_home(self, instance):
        self.manager.current = 'home'


class AddCardScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Add New Card', font_size='20sp', size_hint=(1, 0.1))
        layout.add_widget(title)
        
        layout.add_widget(Label(text='Question:', size_hint=(1, 0.1)))
        self.question_input = TextInput(multiline=True, size_hint=(1, 0.3))
        layout.add_widget(self.question_input)
        
        layout.add_widget(Label(text='Answer:', size_hint=(1, 0.1)))
        self.answer_input = TextInput(multiline=True, size_hint=(1, 0.3))
        layout.add_widget(self.answer_input)
        
        save_btn = Button(text='Save Card', size_hint=(1, 0.15))
        save_btn.bind(on_press=self.save_card)
        layout.add_widget(save_btn)
        
        back_btn = Button(text='Back', size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_home)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def save_card(self, instance):
        question = self.question_input.text.strip()
        answer = self.answer_input.text.strip()
        
        if question and answer:
            self.manager_ref.add_card(question, answer)
            self.question_input.text = ''
            self.answer_input.text = ''
            self.manager.current = 'home'
    
    def go_home(self, instance):
        self.manager.current = 'home'


class ManageCardsScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Manage Cards', font_size='20sp', size_hint=(1, 0.1))
        layout.add_widget(title)
        
        scroll = ScrollView(size_hint=(1, 0.75))
        self.cards_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.cards_layout.bind(minimum_height=self.cards_layout.setter('height'))
        scroll.add_widget(self.cards_layout)
        layout.add_widget(scroll)
        
        back_btn = Button(text='Back', size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_home)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def refresh_list(self):
        self.cards_layout.clear_widgets()
        for i, card in enumerate(self.manager_ref.cards):
            card_layout = BoxLayout(size_hint_y=None, height=100, spacing=5)
            
            text = f"Q: {card.question[:30]}...\nA: {card.answer[:30]}..."
            card_btn = Button(text=text, size_hint_x=0.7)
            card_layout.add_widget(card_btn)
            
            delete_btn = Button(text='Delete', size_hint_x=0.3)
            delete_btn.bind(on_press=lambda x, idx=i: self.delete_card(idx))
            card_layout.add_widget(delete_btn)
            
            self.cards_layout.add_widget(card_layout)
    
    def delete_card(self, index):
        self.manager_ref.delete_card(index)
        self.refresh_list()
    
    def go_home(self, instance):
        self.manager.current = 'home'


class FlashcardApp(App):
    def build(self):
        self.card_manager = FlashCardManager()
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(self.card_manager, name='home'))
        sm.add_widget(StudyScreen(self.card_manager, name='study'))
        sm.add_widget(AddCardScreen(self.card_manager, name='add'))
        sm.add_widget(ManageCardsScreen(self.card_manager, name='manage'))
        
        return sm


if __name__ == '__main__':
    FlashcardApp().run()
