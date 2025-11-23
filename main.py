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
        self.background_color = (0, 0, 0, 0)
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
            Color(*get_color_from_hex('#F9AA33'))
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
            Color(*get_color_from_hex('#4A6572'))
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
            Color(*get_color_from_hex('#E53935'))
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )


class SuccessButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex('#43A047'))  # Green
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )


class StyledLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = get_color_from_hex('#344955')
        self.halign = 'center'
        self.valign = 'middle'


class TitleLabel(StyledLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = dp(28)
        self.bold = True
        self.color = get_color_from_hex('#232F34')


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
        self.write_tab = False
        self.hint_text_color = get_color_from_hex('#888888')


class DeckWidget(BoxLayout):
    def __init__(self, deck, index, select_callback, edit_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(140)  # Augmenté pour accommoder les boutons en colonne
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(10)
        
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )
            Color(*get_color_from_hex('#4A6572'), a=0.1)
            self.border = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=(self.size[0]-2, self.size[1]-2),
                pos=(self.pos[0]+1, self.pos[1]+1)
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Deck content
        content_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        name_label = StyledLabel(
            text=deck['name'],
            font_size=dp(18),
            bold=True,
            size_hint_y=0.6,
            halign='left'
        )
        content_layout.add_widget(name_label)
        
        count_label = StyledLabel(
            text=f"{len(deck['cards'])} cartes",
            font_size=dp(14),
            size_hint_y=0.4,
            halign='left'
        )
        content_layout.add_widget(count_label)
        
        self.add_widget(content_layout)
        
        # Buttons en COLONNE comme dans la gestion des cartes
        button_layout = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=dp(5))
        
        select_btn = PrimaryButton(
            text='Ouvrir',
            size_hint_y=0.33
        )
        select_btn.bind(on_press=lambda x: select_callback(index))
        button_layout.add_widget(select_btn)
        
        edit_btn = SuccessButton(
            text='Modifier', 
            size_hint_y=0.33
        )
        edit_btn.bind(on_press=lambda x: edit_callback(index))
        button_layout.add_widget(edit_btn)
        
        delete_btn = DangerButton(
            text='Supprimer',
            size_hint_y=0.33
        )
        delete_btn.bind(on_press=lambda x: delete_callback(index))
        button_layout.add_widget(delete_btn)
        
        self.add_widget(button_layout)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.size = (self.size[0]-2, self.size[1]-2)
        self.border.pos = (self.pos[0]+1, self.pos[1]+1)

class CardWidget(BoxLayout):
    def __init__(self, card, index, edit_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(10)
        
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.rect = RoundedRectangle(
                radius=[dp(10), dp(10), dp(10), dp(10)],
                size=self.size,
                pos=self.pos
            )
            Color(*get_color_from_hex('#F9AA33'), a=0.1)
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
            size_hint_y=0.5,
            halign='left'
        )
        content_layout.add_widget(question_label)
        
        answer_label = StyledLabel(
            text=f"A: {card.answer[:50]}{'...' if len(card.answer) > 50 else ''}",
            font_size=dp(14),
            size_hint_y=0.5,
            halign='left'
        )
        content_layout.add_widget(answer_label)
        
        self.add_widget(content_layout)
        
        # Buttons
        button_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(5))
        
        edit_btn = SuccessButton(text='Modifier')
        edit_btn.bind(on_press=lambda x: edit_callback(index))
        button_layout.add_widget(edit_btn)
        
        delete_btn = DangerButton(text='Supprimer')
        delete_btn.bind(on_press=lambda x: delete_callback(index))
        button_layout.add_widget(delete_btn)
        
        self.add_widget(button_layout)
    
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
        self.decks = []
        self.current_deck_index = 0
        self.current_card_index = 0
        self.data_file = 'flashcards.json'
        self.load_decks()
        
        # Create default deck if no decks exist
        if not self.decks:
            self.add_deck("Mes Cartes")
    
    @property
    def current_deck(self):
        if self.decks and 0 <= self.current_deck_index < len(self.decks):
            return self.decks[self.current_deck_index]
        return None
    
    @property
    def cards(self):
        deck = self.current_deck
        return deck['cards'] if deck else []
    
    def add_deck(self, name):
        new_deck = {
            'name': name,
            'cards': []
        }
        self.decks.append(new_deck)
        self.save_decks()
    
    def edit_deck(self, index, new_name):
        if 0 <= index < len(self.decks):
            self.decks[index]['name'] = new_name
            self.save_decks()
    
    def delete_deck(self, index):
        if 0 <= index < len(self.decks):
            self.decks.pop(index)
            # Adjust current deck index if needed
            if self.current_deck_index >= len(self.decks) and len(self.decks) > 0:
                self.current_deck_index = len(self.decks) - 1
            elif len(self.decks) == 0:
                self.current_deck_index = 0
                self.add_deck("Nouvelle Liste")
            self.save_decks()
    
    def set_current_deck(self, index):
        if 0 <= index < len(self.decks):
            self.current_deck_index = index
            self.current_card_index = 0
    
    def add_card(self, question, answer):
        deck = self.current_deck
        if deck:
            deck['cards'].append(FlashCard(question, answer))
            self.save_decks()
    
    def edit_card(self, index, question, answer):
        deck = self.current_deck
        if deck and 0 <= index < len(deck['cards']):
            deck['cards'][index].question = question
            deck['cards'][index].answer = answer
            self.save_decks()
    
    def delete_card(self, index):
        deck = self.current_deck
        if deck and 0 <= index < len(deck['cards']):
            deck['cards'].pop(index)
            # Adjust current card index if needed
            if self.current_card_index >= len(deck['cards']) and len(deck['cards']) > 0:
                self.current_card_index = len(deck['cards']) - 1
            elif len(deck['cards']) == 0:
                self.current_card_index = 0
            self.save_decks()
    
    def get_current_card(self):
        cards = self.cards
        if cards and 0 <= self.current_card_index < len(cards):
            return cards[self.current_card_index]
        return None
    
    def next_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index + 1) % len(self.cards)
    
    def prev_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index - 1) % len(self.cards)
    
    def save_decks(self):
        # Convert FlashCard objects to dictionaries for JSON serialization
        data = {
            'decks': [],
            'current_deck_index': self.current_deck_index
        }
        
        for deck in self.decks:
            deck_data = {
                'name': deck['name'],
                'cards': [{'question': card.question, 'answer': card.answer} for card in deck['cards']]
            }
            data['decks'].append(deck_data)
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def load_decks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    # Handle both old format (list of cards) and new format (decks)
                    if isinstance(data, list):
                        # Old format - convert to new format with one deck
                        self.decks = [{
                            'name': 'Mes Cartes',
                            'cards': [FlashCard(item['question'], item['answer']) for item in data]
                        }]
                        self.current_deck_index = 0
                    else:
                        # New format with decks
                        self.decks = []
                        for deck_data in data.get('decks', []):
                            deck = {
                                'name': deck_data['name'],
                                'cards': [FlashCard(item['question'], item['answer']) for item in deck_data['cards']]
                            }
                            self.decks.append(deck)
                        self.current_deck_index = data.get('current_deck_index', 0)
            except Exception as e:
                print(f"Error loading decks: {e}")
                self.decks = []


class HomeScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title
        title = TitleLabel(text='Flashcard Master', size_hint=(1, 0.15))
        main_layout.add_widget(title)
        
        # Current deck info
        self.deck_info = StyledLabel(
            text='',
            font_size=dp(18),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.deck_info)
        
        # Stats
        self.stats_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.stats_label)
        
        # Buttons
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.65))
        
        study_btn = PrimaryButton(text='Étudier', size_hint=(1, 0.2))
        study_btn.bind(on_press=self.go_to_study)
        button_layout.add_widget(study_btn)
        
        add_btn = SecondaryButton(text='Ajouter une Carte', size_hint=(1, 0.2))
        add_btn.bind(on_press=self.go_to_add)
        button_layout.add_widget(add_btn)
        
        manage_btn = SecondaryButton(text='Gérer les Cartes', size_hint=(1, 0.2))
        manage_btn.bind(on_press=self.go_to_manage)
        button_layout.add_widget(manage_btn)
        
        decks_btn = SecondaryButton(text='Gérer les Listes', size_hint=(1, 0.2))
        decks_btn.bind(on_press=self.go_to_decks)
        button_layout.add_widget(decks_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        # Update info when entering the home screen
        self.update_info()
    
    def update_info(self):
        deck = self.manager_ref.current_deck
        if deck:
            self.deck_info.text = f"Liste: {deck['name']}"
            card_count = len(deck['cards'])
            self.stats_label.text = f'{card_count} carte{"s" if card_count != 1 else ""}'
        else:
            self.deck_info.text = "Aucune liste"
            self.stats_label.text = "0 cartes"
    
    def go_to_study(self, instance):
        if self.manager_ref.cards:
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
    
    def go_to_decks(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'decks'
        self.manager.get_screen('decks').refresh_list()


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
        
        # Deck info
        self.deck_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.05)
        )
        main_layout.add_widget(self.deck_label)
        
        # Progress indicator
        self.progress_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.05)
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
            text='Aucune carte disponible.\nAjoutez des cartes pour étudier!',
            font_size=dp(20),
            text_size=(Window.width - dp(80), None)
        )
        self.card_label.bind(texture_size=self.update_text_size)
        card_container.add_widget(self.card_label)
        
        main_layout.add_widget(card_container)
        
        # Flip button
        self.flip_btn = PrimaryButton(text='Montrer la Réponse', size_hint=(1, 0.1))
        self.flip_btn.bind(on_press=self.flip_card)
        main_layout.add_widget(self.flip_btn)
        
        # Navigation
        nav_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        prev_btn = SecondaryButton(text='Précédent')
        prev_btn.bind(on_press=self.prev_card)
        nav_layout.add_widget(prev_btn)
        
        next_btn = SecondaryButton(text='Suivant')
        next_btn.bind(on_press=self.next_card)
        nav_layout.add_widget(next_btn)
        
        main_layout.add_widget(nav_layout)
        
        # Back button
        back_btn = SecondaryButton(text='Retour', size_hint=(1, 0.1))
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
        deck = self.manager_ref.current_deck
        
        if deck:
            self.deck_label.text = f"Liste: {deck['name']}"
        
        if card:
            self.card_label.text = card.question
            self.flip_btn.text = 'Montrer la Réponse'
            self.update_progress()
        else:
            self.card_label.text = "Aucune carte disponible.\nAjoutez des cartes pour étudier!"
            self.progress_label.text = ""
    
    def update_progress(self):
        cards = self.manager_ref.cards
        if cards:
            current = self.manager_ref.current_card_index + 1
            total = len(cards)
            self.progress_label.text = f"Carte {current} sur {total}"
    
    def flip_card(self, instance):
        card = self.manager_ref.get_current_card()
        if card:
            self.show_answer = not self.show_answer
            if self.show_answer:
                self.card_label.text = card.answer
                instance.text = 'Montrer la Question'
            else:
                self.card_label.text = card.question
                instance.text = 'Montrer la Réponse'
    
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
        
        # Title and deck info
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        title = TitleLabel(text='Ajouter une Carte', size_hint=(1, 0.6))
        title_layout.add_widget(title)
        
        self.deck_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.4)
        )
        title_layout.add_widget(self.deck_label)
        
        main_layout.add_widget(title_layout)
        
        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.7))
        
        # Question
        form_layout.add_widget(StyledLabel(text='Question:', size_hint=(1, 0.1)))
        self.question_input = StyledTextInput(
            hint_text='Entrez votre question ici...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.question_input)
        
        # Answer
        form_layout.add_widget(StyledLabel(text='Réponse:', size_hint=(1, 0.1)))
        self.answer_input = StyledTextInput(
            hint_text='Entrez la réponse ici...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.answer_input)
        
        main_layout.add_widget(form_layout)
        
        # Buttons
        button_layout = BoxLayout(spacing=dp(10), size_hint=(1, 0.15))
        
        back_btn = SecondaryButton(text='Annuler')
        back_btn.bind(on_press=self.go_home)
        button_layout.add_widget(back_btn)
        
        save_btn = PrimaryButton(text='Sauvegarder')
        save_btn.bind(on_press=self.save_card)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Update deck info when entering the screen
        deck = self.manager_ref.current_deck
        if deck:
            self.deck_label.text = f"Liste: {deck['name']}"
    
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


class EditCardScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        self.card_index = None
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title and deck info
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        title = TitleLabel(text='Modifier la Carte', size_hint=(1, 0.6))
        title_layout.add_widget(title)
        
        self.deck_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.4)
        )
        title_layout.add_widget(self.deck_label)
        
        main_layout.add_widget(title_layout)
        
        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.7))
        
        # Question
        form_layout.add_widget(StyledLabel(text='Question:', size_hint=(1, 0.1)))
        self.question_input = StyledTextInput(
            hint_text='Entrez votre question ici...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.question_input)
        
        # Answer
        form_layout.add_widget(StyledLabel(text='Réponse:', size_hint=(1, 0.1)))
        self.answer_input = StyledTextInput(
            hint_text='Entrez la réponse ici...',
            size_hint=(1, 0.4)
        )
        form_layout.add_widget(self.answer_input)
        
        main_layout.add_widget(form_layout)
        
        # Buttons
        button_layout = BoxLayout(spacing=dp(10), size_hint=(1, 0.15))
        
        back_btn = SecondaryButton(text='Annuler')
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        save_btn = SuccessButton(text='Mettre à jour')
        save_btn.bind(on_press=self.update_card)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Update deck info when entering the screen
        deck = self.manager_ref.current_deck
        if deck:
            self.deck_label.text = f"Liste: {deck['name']}"
        
        # Load card data if index is set
        if self.card_index is not None:
            card = self.manager_ref.cards[self.card_index]
            self.question_input.text = card.question
            self.answer_input.text = card.answer
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_card(self, instance):
        question = self.question_input.text.strip()
        answer = self.answer_input.text.strip()
        
        if question and answer and self.card_index is not None:
            self.manager_ref.edit_card(self.card_index, question, answer)
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'manage'
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'manage'


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
        
        # Title and deck info
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1))
        title = TitleLabel(text='Gérer les Cartes', size_hint=(1, 0.6))
        title_layout.add_widget(title)
        
        self.deck_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.4)
        )
        title_layout.add_widget(self.deck_label)
        
        main_layout.add_widget(title_layout)
        
        # Scroll view for cards
        scroll = ScrollView(size_hint=(1, 0.8))
        self.cards_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.cards_layout.bind(minimum_height=self.cards_layout.setter('height'))
        scroll.add_widget(self.cards_layout)
        main_layout.add_widget(scroll)
        
        # Back button
        back_btn = SecondaryButton(text='Retour', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_home)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Update deck info when entering the screen
        deck = self.manager_ref.current_deck
        if deck:
            self.deck_label.text = f"Liste: {deck['name']}"
        self.refresh_list()
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def refresh_list(self):
        self.cards_layout.clear_widgets()
        self.cards_layout.height = 0
        
        cards = self.manager_ref.cards
        if not cards:
            no_cards_label = StyledLabel(
                text='Aucune carte dans cette liste.\nAjoutez des cartes pour commencer !',
                font_size=dp(18)
            )
            self.cards_layout.add_widget(no_cards_label)
            return
        
        for i, card in enumerate(cards):
            card_widget = CardWidget(card, i, self.edit_card, self.delete_card)
            self.cards_layout.add_widget(card_widget)
            self.cards_layout.height += card_widget.height + dp(10)
    
    def edit_card(self, index):
        edit_screen = self.manager.get_screen('edit_card')
        edit_screen.card_index = index
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'edit_card'
    
    def delete_card(self, index):
        self.manager_ref.delete_card(index)
        self.refresh_list()
    
    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'


class EditDeckScreen(Screen):
    def __init__(self, manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.manager_ref = manager_ref
        self.deck_index = None
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background
        with main_layout.canvas.before:
            Color(*get_color_from_hex('#ECEFF1'))
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title
        title = TitleLabel(text='Modifier la Liste', size_hint=(1, 0.1))
        main_layout.add_widget(title)
        
        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.7))
        
        # Deck name
        form_layout.add_widget(StyledLabel(text='Nom de la liste:', size_hint=(1, 0.2)))
        self.deck_name_input = StyledTextInput(
            hint_text='Nom de la liste...',
            size_hint=(1, 0.3),
            multiline=False
        )
        form_layout.add_widget(self.deck_name_input)
        
        # Card count info
        self.card_count_label = StyledLabel(
            text='',
            font_size=dp(16),
            size_hint=(1, 0.2)
        )
        form_layout.add_widget(self.card_count_label)
        
        main_layout.add_widget(form_layout)
        
        # Buttons
        button_layout = BoxLayout(spacing=dp(10), size_hint=(1, 0.2))
        
        back_btn = SecondaryButton(text='Annuler')
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        save_btn = SuccessButton(text='Mettre à jour')
        save_btn.bind(on_press=self.update_deck)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Load deck data if index is set
        if self.deck_index is not None:
            deck = self.manager_ref.decks[self.deck_index]
            self.deck_name_input.text = deck['name']
            card_count = len(deck['cards'])
            self.card_count_label.text = f"{card_count} carte{'s' if card_count != 1 else ''} dans cette liste"
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_deck(self, instance):
        name = self.deck_name_input.text.strip()
        
        if name and self.deck_index is not None:
            self.manager_ref.edit_deck(self.deck_index, name)
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'decks'
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'decks'


class DecksScreen(Screen):
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
        title = TitleLabel(text='Gérer les Listes', size_hint=(1, 0.1))
        main_layout.add_widget(title)
        
        # Add deck section
        add_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=dp(10))
        
        self.deck_name_input = StyledTextInput(
            hint_text='Nom de la nouvelle liste...',
            size_hint_x=0.7,
            multiline=False
        )
        add_layout.add_widget(self.deck_name_input)
        
        add_btn = PrimaryButton(text='Ajouter', size_hint_x=0.3)
        add_btn.bind(on_press=self.add_deck)
        add_layout.add_widget(add_btn)
        
        main_layout.add_widget(add_layout)
        
        # Scroll view for decks
        scroll = ScrollView(size_hint=(1, 0.7))
        self.decks_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.decks_layout.bind(minimum_height=self.decks_layout.setter('height'))
        scroll.add_widget(self.decks_layout)
        main_layout.add_widget(scroll)
        
        # Back button
        back_btn = SecondaryButton(text='Retour', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_home)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def refresh_list(self):
        self.decks_layout.clear_widgets()
        self.decks_layout.height = 0
        
        if not self.manager_ref.decks:
            no_decks_label = StyledLabel(
                text='Aucune liste.\nCréez une liste pour commencer!',
                font_size=dp(18)
            )
            self.decks_layout.add_widget(no_decks_label)
            return
        
        for i, deck in enumerate(self.manager_ref.decks):
            deck_widget = DeckWidget(deck, i, self.select_deck, self.edit_deck, self.delete_deck)
            self.decks_layout.add_widget(deck_widget)
            self.decks_layout.height += deck_widget.height + dp(10)
    
    def add_deck(self, instance):
        name = self.deck_name_input.text.strip()
        if name:
            self.manager_ref.add_deck(name)
            self.deck_name_input.text = ''
            self.refresh_list()
    
    def select_deck(self, index):
        self.manager_ref.set_current_deck(index)
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'
    
    def edit_deck(self, index):
        edit_screen = self.manager.get_screen('edit_deck')
        edit_screen.deck_index = index
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'edit_deck'
    
    def delete_deck(self, index):
        # Don't delete if it's the last deck
        if len(self.manager_ref.decks) > 1:
            self.manager_ref.delete_deck(index)
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
        sm.add_widget(DecksScreen(self.card_manager, name='decks'))
        sm.add_widget(EditCardScreen(self.card_manager, name='edit_card'))
        sm.add_widget(EditDeckScreen(self.card_manager, name='edit_deck'))
        
        return sm


if __name__ == '__main__':
    FlashcardApp().run()