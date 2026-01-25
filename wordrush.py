import pygame
import sys
import random
import socket
import threading
import json
import os
import math
import urllib.request
import datetime
import base64
import io
try:
    import winsound
except ImportError:
    winsound = None

CURRENT_VERSION = "0.4"
PORT = 5000

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 980
BG_COLOR = (20, 25, 35)
ACCENT_COLOR = (0, 200, 150)
HOVER_COLOR = (0, 230, 180)
PANEL_COLOR = (30, 35, 45)
TEXT_COLOR = (240, 240, 240)
ALERT_COLOR = (255, 80, 80)
FONT_SIZE = 30

SETTINGS_FILE = "world_rush_settings.json"
HISTORY_FILE = "game_history.json"
AVATARS = [
    "🙂", "😎", "🤖", "👽", "🦊", "🐱", "🐶", "🦁", "🦄", "💀", "👻", "💩", "👾", "🤡", "🤠", "👺",
    "😊", "😂", "🤣", "😍", "😒", "😘", "😜", "🤔", "🙄", "😴", "😷", "🤒", "🤕", "🤢", "🤧", "😇",
    "🥳", "🥺", "🤬", "😈", "👿", "👹", "👺", "☠️", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
    "😾", "🙈", "🙉", "🙊", "🐵", "🐺", "🐯", "🦒", "🦝", "🐷", "🐗", "🐭", "🐹", "🐰", "🐻", "🐨",
    "🐼", "🐸", "🦓", "🐴", "🐔", "🐲", "🐾", "🐒", "🦍", "🦧", "🦮", "🐕", "🐩", "🐈", "🐅", "🐆",
    "⚡", "🔥", "💧", "❄️", "🌈", "☀️", "🌙", "⭐", "🌟", "🍀", "🍄", "🌵", "🌴", "🌲", "🍁", "🍂",
    "🍔", "🍕", "🍟", "🌭", "🍿", "🍩", "🍪", "🎂", "🍰", "🧁", "🍫", "🍬", "🍭", "🎮", "🕹️", "🎲"
]

# Catégories de mots
WORD_CATEGORIES = {
    "GÉNÉRAL": ["Ferme", "Tracteur", "Plage", "Informatique", "Cuisine", "Voiture", "Montagne", "Pizza", "École", "Musique", "Cinéma", "Sport", "Voyage", "Livre", "Téléphone"],
    "ANIMAUX": ["Chien", "Chat", "Éléphant", "Lion", "Tigre", "Oiseau", "Poisson", "Cheval", "Vache", "Singe", "Girafe", "Dauphin", "Aigle", "Loup", "Ours"],
    "OBJETS": ["Chaise", "Table", "Lampe", "Stylo", "Ordinateur", "Télévision", "Montre", "Sac", "Chaussure", "Lunettes", "Clé", "Bouteille", "Tasse", "Couteau", "Fenêtre"],
    "MÉTIERS": ["Pompier", "Policier", "Médecin", "Professeur", "Boulanger", "Cuisinier", "Agriculteur", "Astronaute", "Acteur", "Chanteur", "Juge", "Avocat", "Plombier", "Électricien", "Coiffeur"],
    "PAYS": ["France", "Espagne", "Italie", "Japon", "Chine", "États-Unis", "Brésil", "Canada", "Allemagne", "Australie", "Russie", "Inde", "Mexique", "Égypte", "Maroc"],
    "SPORT": ["Football", "Tennis", "Basketball", "Rugby", "Natation", "Athlétisme", "Judo", "Boxe", "Golf", "Ski", "Volleyball", "Handball", "Cyclisme", "Escalade", "Surf"], # Ajout de catégories
    "MARQUES": ["Nike", "Adidas", "Apple", "Samsung", "Coca-Cola", "McDonald's", "Disney", "Google", "Amazon", "Tesla", "Microsoft", "Sony", "Lego", "Ikea", "Netflix"],
    "VILLES": ["Paris", "Londres", "New York", "Tokyo", "Rome", "Berlin", "Madrid", "Pékin", "Moscou", "Sydney", "Le Caire", "Rio", "Dubaï", "Amsterdam", "Séoul"],
    "ANIMAUX MARINS": ["Requin", "Dauphin", "Baleine", "Poisson-clown", "Crabe", "Méduse", "Pieuvre", "Étoile de mer", "Hippocampe", "Tortue de mer", "Phoque", "Loutre", "Corail", "Anémone", "Crevette"],
    "INSTRUMENTS": ["Guitare", "Piano", "Batterie", "Violon", "Trompette", "Flûte", "Saxophone", "Clarinette", "Harmonica", "Ukulélé", "Harpe", "Contrebasse", "Synthétiseur", "Accordéon", "Tambour"]
}

# Catalogue du Magasin
SHOP_CATALOG = {
    "border_gold": {"type": "border", "name": "Bordure OR", "price": 200, "color": (255, 215, 0)},
    "border_neon": {"type": "border", "name": "Bordure NÉON", "price": 150, "color": (0, 255, 255)},
    "border_fire": {"type": "border", "name": "Bordure FEU", "price": 150, "color": (255, 69, 0)},
    "border_royal": {"type": "border", "name": "Bordure ROYALE", "price": 300, "color": (138, 43, 226)},
    "border_rainbow": {"type": "border", "name": "Bordure RAINBOW", "price": 400, "color": (255, 0, 255)},
    "border_ice": {"type": "border", "name": "Bordure GLACE", "price": 250, "color": (100, 200, 255)},
    "border_nature": {"type": "border", "name": "Bordure NATURE", "price": 200, "color": (50, 200, 50)},
    "border_galaxy": {"type": "border", "name": "Bordure GALAXY", "price": 500, "color": (100, 0, 150)},
    "border_pixel": {"type": "border", "name": "Bordure PIXEL", "price": 300, "color": (50, 200, 50)},
    "border_diamond": {"type": "border", "name": "Bordure DIAMANT", "price": 600, "color": (185, 242, 255)},
    "border_lava": {"type": "border", "name": "Bordure LAVE", "price": 450, "color": (207, 16, 32)},
    "border_electric": {"type": "border", "name": "Bordure ÉLECTRIQUE", "price": 350, "color": (50, 50, 255)},
    "border_shadow": {"type": "border", "name": "Bordure OMBRE", "price": 300, "color": (50, 50, 50)},
    "border_sun": {"type": "border", "name": "Bordure SOLEIL", "price": 400, "color": (255, 255, 100)},
    "border_toxic": {"type": "border", "name": "Bordure TOXIQUE", "price": 350, "color": (100, 255, 50)},
    "border_double": {"type": "border", "name": "Bordure DOUBLE", "price": 450, "color": (255, 255, 255)},
    "border_glitch": {"type": "border", "name": "Bordure GLITCH", "price": 550, "color": (0, 255, 100)},
    "color_red": {"type": "name_color", "name": "Pseudo ROUGE", "price": 100, "color": (255, 80, 80)},
    "color_blue": {"type": "name_color", "name": "Pseudo BLEU", "price": 100, "color": (80, 150, 255)},
    "color_gold": {"type": "name_color", "name": "Pseudo OR", "price": 500, "color": (255, 215, 0)},
    "color_green": {"type": "name_color", "name": "Pseudo VERT", "price": 100, "color": (80, 255, 80)},
    "color_pink": {"type": "name_color", "name": "Pseudo ROSE", "price": 150, "color": (255, 100, 200)},
    "color_purple": {"type": "name_color", "name": "Pseudo VIOLET", "price": 200, "color": (180, 80, 255)},
    "color_cyan": {"type": "name_color", "name": "Pseudo CYAN", "price": 150, "color": (0, 255, 255)},
    "color_lime": {"type": "name_color", "name": "Pseudo LIME", "price": 150, "color": (50, 255, 50)},
    "color_magenta": {"type": "name_color", "name": "Pseudo MAGENTA", "price": 150, "color": (255, 0, 255)},
    "color_silver": {"type": "name_color", "name": "Pseudo ARGENT", "price": 300, "color": (192, 192, 192)},
    "color_orange": {"type": "name_color", "name": "Pseudo ORANGE", "price": 150, "color": (255, 165, 0)},
    "name_color_dark_red": {"type": "name_color", "name": "Pseudo SANG", "price": 250, "color": (139, 0, 0)},
    "theme_matrix": {"type": "theme", "name": "Thème MATRIX", "price": 500, "color": (0, 20, 0)},
    "theme_ocean": {"type": "theme", "name": "Thème OCÉAN", "price": 250, "color": (0, 30, 60)},
    "theme_sunset": {"type": "theme", "name": "Thème SUNSET", "price": 250, "color": (60, 20, 40)},
    "theme_forest": {"type": "theme", "name": "Thème FORÊT", "price": 300, "color": (20, 40, 20)},
    "theme_candy": {"type": "theme", "name": "Thème CANDY", "price": 350, "color": (50, 20, 40)},
    "theme_space": {"type": "theme", "name": "Thème ESPACE", "price": 400, "color": (10, 10, 20)},
    "theme_dark": {"type": "theme", "name": "Thème SOMBRE", "price": 400, "color": (10, 10, 10)},
    "theme_retro": {"type": "theme", "name": "Thème RÉTRO", "price": 450, "color": (43, 30, 30)},
    "theme_cyber": {"type": "theme", "name": "Thème CYBER", "price": 600, "color": (0, 10, 20)},
    "theme_desert": {"type": "theme", "name": "Thème DÉSERT", "price": 300, "color": (60, 40, 20)},
    "theme_arctic": {"type": "theme", "name": "Thème ARCTIQUE", "price": 300, "color": (200, 220, 255)},
    "theme_volcano": {"type": "theme", "name": "Thème VOLCAN", "price": 450, "color": (40, 10, 10)},
    "theme_midnight": {"type": "theme", "name": "Thème MINUIT", "price": 400, "color": (5, 5, 20)},
    "theme_blood": {"type": "theme", "name": "Thème SANG", "price": 500, "color": (40, 0, 0)},
    "theme_hacker": {"type": "theme", "name": "Thème HACKER", "price": 600, "color": (0, 0, 0)},
    "name_color_rainbow": {"type": "name_color", "name": "Pseudo RAINBOW", "price": 1000, "color": (255, 255, 255)},
    "border_ghost": {"type": "border", "name": "Bordure FANTÔME", "price": 400, "color": (200, 200, 200)},
    "theme_royal": {"type": "theme", "name": "Thème ROYAL", "price": 800, "color": (40, 0, 40)},
    "upgrade_freeze": {"type": "upgrade", "name": "Stock Gel Temps (+1)", "price": 300, "color": (100, 200, 255)},
    "gift_daily": {"type": "gift", "name": "Cadeau du Jour", "price": 0, "color": (255, 255, 255)},
    "cat_videogames": {"type": "category", "name": "JEUX VIDÉO", "price": 500, "color": (100, 100, 255), "content": ["Mario", "Zelda", "Minecraft", "Fortnite", "Tetris", "Pac-Man", "Sonic", "GTA", "Call of Duty", "Pokémon", "Sims", "FIFA", "Among Us", "Roblox", "League of Legends"]},
    "cat_food": {"type": "category", "name": "NOURRITURE", "price": 400, "color": (255, 150, 50), "content": ["Sushi", "Burger", "Tacos", "Salade", "Pâtes", "Steak", "Frites", "Glace", "Chocolat", "Pomme", "Banane", "Pain", "Fromage", "Oeuf", "Soupe"]},
    "cat_superheroes": {"type": "category", "name": "SUPER-HÉROS", "price": 600, "color": (255, 50, 50), "content": ["Batman", "Superman", "Spiderman", "Iron Man", "Wonder Woman", "Thor", "Hulk", "Captain America", "Flash", "Black Panther", "Aquaman", "Wolverine", "Deadpool", "Thanos", "Joker"]},
    "cat_horror": {"type": "category", "name": "HORREUR", "price": 666, "color": (100, 0, 0), "content": ["Fantôme", "Vampire", "Zombie", "Sorcière", "Loup-garou", "Momie", "Squelette", "Démon", "Frankenstein", "Clown", "Hache", "Sang", "Cimetière", "Manoir", "Cauchemar"]}
}

ACHIEVEMENTS = {
    "WIN_1": {"name": "Première Victoire", "desc": "Gagner une partie", "reward": 50},
    "WIN_10": {"name": "Champion", "desc": "Gagner 10 parties", "reward": 200},
    "LEVEL_5": {"name": "Niveau 5", "desc": "Atteindre le niveau 5", "reward": 100},
    "LEVEL_10": {"name": "Vétéran", "desc": "Atteindre le niveau 10", "reward": 300},
    "RICH": {"name": "Économe", "desc": "Posséder 500 pièces", "reward": 100},
    "RICH_2000": {"name": "Millionnaire", "desc": "Posséder 2000 pièces", "reward": 500},
    "SOCIAL": {"name": "Amical", "desc": "Ajouter un ami", "reward": 50},
    "SOCIAL_MAX": {"name": "Populaire", "desc": "Avoir 5 amis", "reward": 200},
    "WIN_50": {"name": "Légende", "desc": "Gagner 50 parties", "reward": 1000},
    "COLLECTOR": {"name": "Collectionneur", "desc": "Posséder 10 objets", "reward": 300},
    "SHOPPER": {"name": "Client", "desc": "Acheter un objet", "reward": 50},
    "SPEEDSTER": {"name": "Speedster", "desc": "Atteindre un combo de 10", "reward": 500},
    "SHOP_KING": {"name": "Roi du Shopping", "desc": "Acheter tout le magasin", "reward": 5000}
}

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None, font=None, text_color=None, scale_on_hover=False, notification=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = font if font else pygame.font.SysFont("Arial", 26, bold=True)
        self.text_color = text_color if text_color else (20, 25, 35)
        self.scale_on_hover = scale_on_hover
        self.notification = notification
        self.hover_progress = 0.0
        self.creation_time = pygame.time.get_ticks()

    def interpolate_color(self, c1, c2, t):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t)
        )

    def draw(self, screen, offset_y=0):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animation d'apparition (Slide Up)
        now = pygame.time.get_ticks()
        anim_progress = min(1.0, (now - self.creation_time) / 300.0)
        anim_progress = 1 - (1 - anim_progress) ** 3 # Ease Out Cubic
        anim_y = (1.0 - anim_progress) * 50 # Décalage de 50px vers le bas au début

        # Animation fluide
        target = 1.0 if is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.15
        
        current_color = self.interpolate_color(self.color, self.hover_color, self.hover_progress)
        
        # Effet d'enfoncement
        is_pressed = is_hovered and pygame.mouse.get_pressed()[0]
        offset = 3 if is_pressed else 0
        
        # Ombre portée (fixe)
        shadow_rect = self.rect.copy()
        shadow_rect.y += 6 - offset + anim_y
        s = pygame.Surface((shadow_rect.w, shadow_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 60), s.get_rect(), border_radius=15)
        screen.blit(s, shadow_rect)

        # Corps du bouton (mobile)
        btn_rect = self.rect.copy()
        btn_rect.y += offset + anim_y
        
        # Bordure (plus foncée)
        darker = (max(0, current_color[0]-40), max(0, current_color[1]-40), max(0, current_color[2]-40))
        pygame.draw.rect(screen, darker, btn_rect, border_radius=15)
        
        # Intérieur
        inner_rect = btn_rect.inflate(-4, -4)
        pygame.draw.rect(screen, current_color, inner_rect, border_radius=12)
        
        # Reflet supérieur (Glassy)
        gloss_rect = pygame.Rect(inner_rect.x, inner_rect.y, inner_rect.w, inner_rect.h // 2)
        s_gloss = pygame.Surface((gloss_rect.w, gloss_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s_gloss, (255, 255, 255, 40), s_gloss.get_rect(), border_top_left_radius=12, border_top_right_radius=12)
        screen.blit(s_gloss, gloss_rect)

        # Texte
        lines = self.text.split('\n')
        line_height = self.font.get_height()
        total_height = len(lines) * line_height
        start_y = btn_rect.centery - total_height / 2

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.text_color)
            
            # Zoom texte au survol
            if self.scale_on_hover and self.hover_progress > 0.05:
                scale = 1.0 + (0.1 * self.hover_progress)
                w = int(text_surf.get_width() * scale)
                h = int(text_surf.get_height() * scale)
                text_surf = pygame.transform.smoothscale(text_surf, (w, h))
            
            text_rect = text_surf.get_rect(center=(btn_rect.centerx, start_y + i * line_height + line_height / 2))
            
            # Ombre texte si couleur claire
            if sum(self.text_color) > 300: 
                shadow_txt = self.font.render(line, True, (0,0,0))
                if self.scale_on_hover and self.hover_progress > 0.05:
                    shadow_txt = pygame.transform.smoothscale(shadow_txt, (text_surf.get_width(), text_surf.get_height()))
                shadow_txt.set_alpha(80)
                shadow_rect = shadow_txt.get_rect(center=(text_rect.centerx+1, text_rect.centery+2))
                screen.blit(shadow_txt, shadow_rect)
                
            screen.blit(text_surf, text_rect)
            
        if self.notification:
            pygame.draw.circle(screen, (255, 50, 50), (btn_rect.right - 10, btn_rect.top + 10), 8 + (2 * math.sin(now * 0.01)))
            pygame.draw.circle(screen, (255, 255, 255), (btn_rect.right - 10, btn_rect.top + 10), 8 + (2 * math.sin(now * 0.01)), 2)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu d'Association Rapide")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.title_font = pygame.font.SysFont("Impact", 100)
        self.emoji_font = pygame.font.SysFont("Segoe UI Emoji", 80) # Pour les avatars (Grand)
        self.ui_emoji_font = pygame.font.SysFont("Segoe UI Emoji", 40) # Pour les avatars (Petit/UI)
        self.medium_font = pygame.font.SysFont("Arial", 45, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 38, bold=True)
        self.small_bold_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.timer_font = pygame.font.SysFont("Consolas", 80, bold=True) # Police fixe pour chrono fluide
        
        # États du jeu
        self.state = "INPUT_NAME" # INPUT_NAME, MENU_MAIN, MENU_ONLINE, SETUP, SETTINGS, CONTROLS, LOBBY, HOW_TO, GAME, JUDGMENT, GAME_OVER, ROUND_COUNTDOWN, OPPONENT_LEFT
        
        # Paramètres de la partie
        self.settings = {
            'players': 2,
            'time': 5,
            'mode': 'VOCAL',
            'win_score': 5,
            'category': 'GÉNÉRAL',
            'game_type': 'NORMAL'
        }

        # Touches
        self.keys = {
            "VALIDATE": pygame.K_RETURN,
            "CONTEST": pygame.K_LSHIFT,
            "VOCAL_VALIDATE": pygame.K_SPACE
        }

        self.current_word = ""
        self.user_text = ""
        self.start_ticks = 0
        self.round_duration = 5.0
        self.time_left = 0
        self.opponent_text = "" # Texte de l'adversaire en temps réel
        self.opponent_name = "Adversaire"
        self.score = [0, 0] # Joueur 1, Joueur 2
        self.opponent_level = 1
        self.avatar = AVATARS[0]
        self.opponent_avatar = "?"
        self.opponent_border = "border_default"
        self.opponent_name_color = "name_color_default"
        self.current_player = 0 # 0 (Host) ou 1 (Client)
        self.my_id = 0 # Mon identité
        self.winner_text = ""
        self.username = ""
        self.rematch_ready = [False, False] # [Host, Client] ou [J1, J2...]
        self.judge_id = -1
        self.round_num = 1
        self.turn_count = 0 # Compteur d'échanges dans la manche (pour Survival)
        self.rally_combo = 0 # Compteur de combo (réponses rapides)
        self.countdown_start = 0
        self.last_round_reason = "" # TIMEOUT ou NORMAL
        self.last_round_winner = -1
        self.particles = []
        self.public_ip = None
        self.local_ip = ""
        self.upnp_status = "Non tenté"
        self.upnp_control_url = None
        self.upnp_service_type = None
        self.chat_messages = []
        self.chat_input = ""
        self.ready_status = [False, False] # [J1, J2]
        self.first_run = True
        self.bot_msg_index = 0
        self.friends = []
        self.friend_name_input = ""
        self.friend_ip_input = ""
        self.cat_name_input = ""
        self.cat_words_input = ""
        self.custom_categories = {}
        self.all_categories = WORD_CATEGORIES.copy()
        self.active_input = "name"
        self.sound_on = True
        self.used_words = []
        self.feedback_msg = ""
        self.feedback_timer = 0
        self.prev_state = "MENU_MAIN"
        self.shake_timer = 0
        self.chat_scroll = 0
        self.avatar_scroll = 0
        self.avatar_grid_buttons = []
        self.menu_particles = []
        self.last_click = 0
        self.trade_amount = "0"
        self.shop_scroll = 0
        self.shop_tab = "ALL" # ALL, BORDER, THEME
        self.achievements_scroll = 0
        self.current_freezes = 0
        self.freeze_until = 0
        
        # Notifications
        self.notifications = []
        
        # Crop Avatar
        self.crop_image = None
        self.crop_scale = 1.0
        self.crop_offset = [0, 0]
        self.crop_dragging = False
        self.crop_last_mouse = (0, 0)
        
        # Animation XP
        self.anim_xp_val = 0.0
        self.anim_level_val = 1
        self.target_xp_val = 0
        self.target_level_val = 1
        self.xp_animating = False
        
        self.avatar_cache = {} # Cache pour les images décodées
        # Économie & Shop
        self.coins = 100
        self.inventory = ["border_default", "theme_default"]
        self.equipped = {"border": "border_default", "theme": "theme_default"}
        self.shop_items = []
        self.last_shop_date = ""
        self.last_gift_date = ""
        self.achievements_unlocked = []
        self.stats = {"wins": 0, "games": 0}
        
        self.achievement_queue = []
        self.current_achievement = None
        
        # Vignette (Modern UI)
        self.create_vignette()
        
        # Transition
        self.transition_alpha = 0
        self.transition_state = None
        self.next_state = None
        self.update_available = False
        self.is_updating = False
        self.update_progress_text = ""
        self.update_ready_to_restart = False
        
        # Réseau
        self.server = None
        self.conn = None
        self.input_ip = "127.0.0.1"
        self.network_queue = []
        self.is_host = False
        self.connected = False
        self.clients = [] # Liste des clients connectés (Host)
        self.is_local_game = False
        self.is_connecting = False
        self.connect_status = "" # "", "CONNECTING", "FAILED"
        
        # Mode Test / Debug
        self.test_mode = False
        self.t_press_count = 0
        self.last_t_press = 0
        self.bot_timer = 0
        self.cheat_buffer = ""
        pygame.scrap.init()
        
        # --- NOUVEAU SYSTÈME (Popup, Trade, Listener) ---
        self.popup = None # {title, msg, avatar, yes, no}
        self.friend_req_event = threading.Event()
        self.friend_req_result = None
        self.lobby_cache = {} # Cache des joueurs pour le client
        self.trade_lobby_data = {"me": {"coins": 0, "items": [], "locked": False}, "them": {"coins": 0, "items": [], "locked": False}, "countdown": None}
        self.hovered_friend_idx = -1
        # Démarrage du listener global pour recevoir des demandes n'importe où
        threading.Thread(target=self.start_global_listener, daemon=True).start()
        
        # --- MINI-JEU BONUS ---
        self.bonus_targets = []
        self.bonus_end_time = 0

        # Résolutions
        self.resolutions = [(1280, 720), (1600, 900), (1800, 980), (1920, 1080)]
        self.res_index = 2

        # Chargement des paramètres
        self.load_settings()
        self.apply_resolution() # Appliquer la résolution chargée

        if self.first_run:
            self.state = "TUTORIAL"
        elif self.username:
            self.state = "MENU_MAIN"
            
        # UI
        self.buttons = []
        self.create_menu_buttons()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self.username = data.get("username", "")
                    self.avatar = data.get("avatar", AVATARS[0])
                    self.sound_on = data.get("sound", True)
                    self.first_run = data.get("first_run", True)
                    # Charger les touches si elles existent
                    saved_keys = data.get("keys", {})
                    self.friends = data.get("friends", [])
                    for k, v in saved_keys.items():
                        self.keys[k] = v
                    self.custom_categories = data.get("custom_categories", {})
                    self.all_categories = WORD_CATEGORIES.copy()
                    self.all_categories.update(self.custom_categories)
                    # Ajouter les catégories achetées
                    for item_id in self.inventory:
                        if item_id in SHOP_CATALOG and SHOP_CATALOG[item_id].get('type') == 'category':
                            self.all_categories[SHOP_CATALOG[item_id]['name']] = SHOP_CATALOG[item_id]['content']
                    self.xp = data.get("xp", 0)
                    self.level = data.get("level", 1)
                    self.coins = data.get("coins", 100)
                    self.inventory = data.get("inventory", ["border_default", "theme_default", "name_color_default"])
                    self.equipped = data.get("equipped", {"border": "border_default", "theme": "theme_default", "name_color": "name_color_default"})
                    if "name_color" not in self.equipped: self.equipped["name_color"] = "name_color_default"
                    if "name_color_default" not in self.inventory: self.inventory.append("name_color_default")
                    self.settings['game_type'] = data.get("game_type", "NORMAL")
                    self.last_shop_date = data.get("last_shop_date", "")
                    self.last_gift_date = data.get("last_gift_date", "")
                    self.achievements_unlocked = data.get("achievements", [])
                    self.stats = data.get("stats", {"wins": 0, "games": 0, "history": [], "max_combo": 0})
                    if "history" not in self.stats: self.stats["history"] = []
                    if "max_combo" not in self.stats: self.stats["max_combo"] = 0
                    self.res_index = data.get("res_index", 2)
            except:
                pass

    def save_settings(self):
        # Sauvegarder pseudo et touches
        data = {
            "username": self.username, "avatar": self.avatar, "sound": self.sound_on, 
            "keys": self.keys, "first_run": self.first_run, "friends": self.friends, 
            "xp": self.xp, "level": self.level, "custom_categories": self.custom_categories,
            "coins": self.coins, "inventory": self.inventory, "equipped": self.equipped, "game_type": self.settings.get('game_type', 'NORMAL'),
            "last_shop_date": self.last_shop_date, "last_gift_date": self.last_gift_date, "res_index": self.res_index,
            "achievements": self.achievements_unlocked, "stats": self.stats
        }
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def reset_app(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                os.remove(SETTINGS_FILE)
            except:
                pass
        self.username = ""
        self.xp = 0
        self.level = 1
        self.coins = 100
        self.inventory = ["border_default", "theme_default", "name_color_default"]
        self.equipped = {"border": "border_default", "theme": "theme_default", "name_color": "name_color_default"}
        self.achievements_unlocked = []
        self.all_categories = WORD_CATEGORIES.copy()
        self.stats = {"wins": 0, "games": 0, "history": [], "max_combo": 0}
        self.settings['players'] = 2
        self.settings['win_score'] = 5
        self.settings['game_type'] = 'NORMAL'
        self.first_run = True
        self.state = "INPUT_NAME"
        self.save_settings()
        self.create_menu_buttons()

    def close_tutorial(self):
        self.first_run = False
        self.save_settings()
        if not self.username:
            self.state = "INPUT_NAME"
        else:
            self.state = "MENU_MAIN"
        self.create_menu_buttons()

    def create_vignette(self):
        self.vignette_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Dégradé vertical pour le fond
        for y in range(SCREEN_HEIGHT):
            alpha = int((y / SCREEN_HEIGHT) * 100)
            pygame.draw.line(self.vignette_surf, (0, 0, 0, alpha), (0, y), (SCREEN_WIDTH, y))
        pygame.draw.rect(self.vignette_surf, (0, 0, 0, 40), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 30)
        pygame.draw.rect(self.vignette_surf, (0, 0, 0, 80), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)

    def apply_resolution(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        if 0 <= self.res_index < len(self.resolutions):
            SCREEN_WIDTH, SCREEN_HEIGHT = self.resolutions[self.res_index]
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.create_vignette()

    def cycle_resolution(self):
        self.res_index = (self.res_index + 1) % len(self.resolutions)
        self.apply_resolution()
        self.save_settings()
        self.create_menu_buttons()

    def add_particles(self, x, y, color):
        for _ in range(30):
            self.particles.append({
                'x': x, 'y': y,
                'vx': random.uniform(-6, 6),
                'vy': random.uniform(-6, 6),
                'life': 255,
                'color': color,
                'size': random.randint(4, 10)
            })

    def update_draw_particles(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 4
            p['size'] -= 0.05
            if p['life'] <= 0 or p['size'] <= 0:
                self.particles.remove(p)
            else:
                s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], int(p['life'])), (int(p['size']), int(p['size'])), int(p['size']))
                self.screen.blit(s, (p['x'] - p['size'], p['y'] - p['size']))

    def update_draw_menu_particles(self):
        # Ajout de particules d'ambiance (Menu)
        if len(self.menu_particles) < 50:
            self.menu_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT + 10,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1, -3),
                'size': random.randint(2, 5),
                'color': (random.randint(20, 40), random.randint(30, 50), random.randint(40, 60)),
                'alpha': random.randint(50, 150)
            })

        for p in self.menu_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['alpha'] -= 0.5
            if p['y'] < -10 or p['alpha'] <= 0:
                self.menu_particles.remove(p)
            else:
                s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], int(p['alpha'])), (int(p['size']), int(p['size'])), int(p['size']))
                self.screen.blit(s, (p['x'], p['y']))

    def generate_flame_particles(self):
        # Génère des flammes sur les bords de l'écran
        sides = [
            (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, random.uniform(-1, 1), random.uniform(-3, -7)), # Bas
            (random.randint(0, SCREEN_WIDTH), 0, random.uniform(-1, 1), random.uniform(3, 7)), # Haut
            (0, random.randint(0, SCREEN_HEIGHT), random.uniform(3, 7), random.uniform(-1, 1)), # Gauche
            (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT), random.uniform(-3, -7), random.uniform(-1, 1)) # Droite
        ]
        for x, y, vx, vy in sides:
            if random.random() < 0.3: # Densité
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': vx, 'vy': vy,
                    'life': random.randint(100, 200), 'color': (255, random.randint(50, 150), 0), 'size': random.randint(5, 15)
                })

    def generate_hardcore_win_particles(self):
        # Explosion rouge et noire pour le mode Hardcore
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for _ in range(150):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 25)
            self.particles.append({
                'x': cx, 'y': cy,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(100, 255),
                'color': random.choice([(255, 0, 0), (0, 0, 0), (100, 0, 0)]),
                'size': random.randint(5, 20)
            })

    # --- SYSTÈME GLOBAL D'ÉCOUTE (AMIS / TRADE) ---
    def start_global_listener(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('0.0.0.0', PORT))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_incoming_connection, args=(conn,), daemon=True).start()
        except: pass

    def handle_incoming_connection(self, conn):
        try:
            # Lecture robuste pour supporter les gros avatars (PDP)
            conn.settimeout(10)
            buffer = b""
            while b"\n" not in buffer:
                chunk = conn.recv(4096)
                if not chunk: break
                buffer += chunk
                if len(buffer) > 5000000: break # Sécurité
            
            if b"\n" not in buffer: conn.close(); return
            data = buffer.split(b"\n", 1)[0].decode('utf-8').strip()
            conn.settimeout(None)
            
            parts = data.split('|')
            intent = parts[0]
            
            if intent == "INTENT_GAME":
                if self.state == "LOBBY" and not self.connected:
                    # Gestion Multi-joueurs (Host)
                    if self.is_host:
                        if len(self.clients) < self.settings['players'] - 1:
                            new_id = len(self.clients) + 1
                            # Accepter et envoyer l'ID
                            conn.sendall(f"ACCEPT|{new_id}\n".encode())
                            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Amélioration latence
                            
                            # Stocker infos client
                            client_data = {
                                "conn": conn, "id": new_id,
                                "name": parts[1] if len(parts) > 1 else f"Joueur {new_id+1}",
                                "avatar": parts[2] if len(parts) > 2 else "?",
                                "border": parts[3] if len(parts) > 3 else "border_default",
                                "name_color": parts[4] if len(parts) > 4 else "name_color_default",
                                "level": 1, "ready": False,
                                "ip": conn.getpeername()[0]
                            }
                            self.clients.append(client_data)
                            
                            msg = f"SYSTEM: {client_data['name']} a rejoint."
                            self.chat_messages.append(msg)
                            self.send_data(f"CHAT|{msg}")
                            
                            # Thread d'écoute pour ce client
                            threading.Thread(target=self.host_receive_client_data, args=(client_data,), daemon=True).start()
                            self.broadcast_player_list()
                        else:
                            conn.close()
                else:
                    conn.close()
            elif intent == "FRIEND_REQ":
                sender_name = parts[1]
                sender_avatar = parts[2]
                
                try:
                    remote_ip = conn.getpeername()[0]
                    # Vérification si déjà ami
                    if any(f['ip'] == remote_ip for f in self.friends):
                        conn.sendall(b"FRIEND_ALREADY\n")
                        conn.close()
                        return
                except: pass
                
                self.friend_req_result = None
                self.friend_req_event.clear()
                
                def on_accept():
                    self.friend_req_result = "ACCEPT"
                    self.friend_req_event.set()
                    self.popup = None
                
                def on_reject():
                    self.friend_req_result = "REJECT"
                    self.friend_req_event.set()
                    self.popup = None

                self.popup = {
                    "title": "DEMANDE D'AMI", "msg": f"{sender_name} veut vous ajouter !", "avatar": sender_avatar,
                    "yes": on_accept, "no": on_reject
                }
                
                # Attente réponse utilisateur (Bloquant dans le thread réseau)
                self.friend_req_event.wait(30)
                
                if self.friend_req_result == "ACCEPT":
                    conn.sendall(f"FRIEND_OK|{self.username}\n".encode())
                    try:
                        remote_ip = conn.getpeername()[0]
                        if not any(f['ip'] == remote_ip for f in self.friends):
                            self.friends.append({"name": sender_name, "ip": remote_ip})
                            self.save_settings()
                            self.check_achievements()
                            self.show_notification(f"{sender_name} ajouté !")
                    except: pass
                else:
                    conn.sendall(b"FRIEND_NO\n")
                conn.close()
            elif intent == "INTENT_TRADE":
                self.popup = {
                    "title": "ECHANGE", "msg": f"{parts[1]} veut échanger !", "avatar": parts[2],
                    "yes": lambda: self.accept_trade(conn, parts[1], parts[2]), "no": lambda: self.reject_request(conn)
                }
        except: conn.close()

    def reject_request(self, conn):
        try: conn.sendall(b"REJECT\n"); conn.close()
        except: pass
        self.popup = None

    def get_xp_threshold(self, level):
        if level == 1: return 30
        if level == 2: return 60
        if level == 3: return 80
        return level * 50

    def gain_xp(self, amount):
        self.xp += amount
        threshold = self.get_xp_threshold(self.level)
        while self.xp >= threshold:
            self.xp -= threshold
            self.level += 1
            threshold = self.get_xp_threshold(self.level)
            self.play_sound("start") # Son de level up
        self.check_achievements()
        self.save_settings()

    def play_sound(self, type):
        if self.sound_on and winsound:
            if type == "chat": threading.Thread(target=winsound.Beep, args=(1000, 100), daemon=True).start()
            elif type == "start": threading.Thread(target=winsound.Beep, args=(600, 300), daemon=True).start()
            elif type == "buzz": threading.Thread(target=winsound.Beep, args=(300, 400), daemon=True).start()
            elif type == "coin": threading.Thread(target=winsound.Beep, args=(1200, 50), daemon=True).start()
            elif type == "click": threading.Thread(target=winsound.Beep, args=(500, 50), daemon=True).start()

    def show_notification(self, text):
        self.notifications.append({"text": text, "time": pygame.time.get_ticks(), "duration": 4000, "y": -60})

    def draw_notifications(self):
        current_time = pygame.time.get_ticks()
        # Supprimer les anciennes
        self.notifications = [n for n in self.notifications if current_time - n["time"] < n["duration"]]
        
        for i, n in enumerate(self.notifications):
            # Animation slide in
            target_y = 20 + i * 70
            n["y"] += (target_y - n["y"]) * 0.1
            
            # Dessin
            s = pygame.Surface((400, 60), pygame.SRCALPHA)
            pygame.draw.rect(s, (30, 35, 45, 240), (0, 0, 400, 60), border_radius=15)
            pygame.draw.rect(s, ACCENT_COLOR, (0, 0, 400, 60), 2, border_radius=15)
            self.screen.blit(s, (SCREEN_WIDTH - 420, n["y"]))
            
            # Icône info
            pygame.draw.circle(self.screen, ACCENT_COLOR, (SCREEN_WIDTH - 390, int(n["y"]) + 30), 15)
            self.draw_text("i", self.small_bold_font, (30, 35, 45), SCREEN_WIDTH - 390, int(n["y"]) + 30)
            
            self.draw_text(n["text"], self.small_bold_font, TEXT_COLOR, SCREEN_WIDTH - 200, int(n["y"]) + 30)

    def prepare_xp_animation(self, amount):
        self.anim_xp_val = float(self.xp)
        self.anim_level_val = self.level
        self.gain_xp(amount)
        self.target_xp_val = self.xp
        self.target_level_val = self.level
        self.xp_animating = True

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.save_settings()
        self.create_menu_buttons()

    def change_avatar(self, delta):
        idx = AVATARS.index(self.avatar)
        self.avatar = AVATARS[(idx + delta) % len(AVATARS)]

    def random_avatar(self):
        self.avatar = random.choice(AVATARS)
        self.create_menu_buttons()

    def set_avatar(self, avatar):
        self.avatar = avatar
        self.create_menu_buttons()

    def reset_history(self):
        self.used_words = []
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)
        except: pass

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.used_words, f)
        except: pass
    
    def request_friend(self):
        if self.friend_name_input and self.friend_ip_input:
            threading.Thread(target=self._send_friend_req_thread, args=(self.friend_ip_input, self.friend_name_input), daemon=True).start()
            self.set_state("MENU_FRIENDS")

    def _send_friend_req_thread(self, target_ip, target_name):
        try:
            # S'assurer d'avoir l'IP locale pour l'envoyer (Aide pour le LAN)
            if not self.local_ip:
                try:
                    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); tmp.connect(("8.8.8.8", 80))
                    self.local_ip = tmp.getsockname()[0]; tmp.close()
                except: self.local_ip = "127.0.0.1"

            self.show_notification("Envoi demande...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30) # Attente longue pour la réponse utilisateur
            s.connect((target_ip, PORT))
            
            s.sendall(f"FRIEND_REQ|{self.username}|{self.avatar}\n".encode())
            
            resp = s.recv(1024).decode().strip()
            if resp.startswith("FRIEND_OK"):
                # Récupérer le nom réel de l'ami s'il est renvoyé
                friend_name = target_name
                if len(resp.split("|")) > 1: friend_name = resp.split("|")[1]
                
                self.friends.append({"name": friend_name, "ip": target_ip})
                self.save_settings()
                self.check_achievements()
                self.show_notification(f"{friend_name} ajouté !")
            elif resp.startswith("FRIEND_ALREADY"):
                self.show_notification("Déjà ami avec ce joueur !")
            else:
                self.show_notification("Demande refusée ou expirée")
            s.close()
        except (OSError, socket.timeout): self.show_notification("Hôte introuvable")
        except Exception as e:
            self.show_notification(f"Erreur: {e}")

    def direct_add_friend(self, ip, name):
        threading.Thread(target=self._send_friend_req_thread, args=(ip, name), daemon=True).start()

    def delete_friend(self, idx):
        if 0 <= idx < len(self.friends):
            del self.friends[idx]
            self.save_settings()
            self.create_menu_buttons()
            
    def copy_ip(self):
        if self.public_ip:
            try:
                pygame.scrap.put(pygame.SCRAP_TEXT, self.public_ip.encode('utf-8'))
                self.connect_status = "IP Copiée !" # Reuse connect_status for feedback
            except: pass

    def save_custom_category(self):
        if self.cat_name_input and self.cat_words_input:
            words = [w.strip() for w in self.cat_words_input.split(',')]
            if len(words) >= 5:
                self.custom_categories[self.cat_name_input.upper()] = words
                self.all_categories.update(self.custom_categories)
                self.save_settings()
                self.cat_name_input = ""
                self.cat_words_input = ""
                self.set_state("MENU_CUSTOM_CATS")
    
    def delete_custom_category(self, name):
        if name in self.custom_categories:
            del self.custom_categories[name]
            self.all_categories = WORD_CATEGORIES.copy()
            self.all_categories.update(self.custom_categories)
            # Reset category if current is deleted
            if self.settings['category'] == name:
                self.settings['category'] = 'GÉNÉRAL'
            self.save_settings()
            self.create_menu_buttons()

    def draw_coin_ui(self, x, y, amount, centered=True):
        # Dessine une pièce dorée graphique et le montant
        text_surf = self.font.render(str(amount), True, (255, 215, 0))
        
        # Rayon de la pièce
        r = 15
        padding = 8
        total_w = r*2 + padding + text_surf.get_width()
        
        start_x = x - total_w // 2 if centered else x
        
        # Dessin de la pièce (Cercle Extérieur)
        pygame.draw.circle(self.screen, (218, 165, 32), (start_x + r, y), r) # Or foncé
        pygame.draw.circle(self.screen, (255, 215, 0), (start_x + r, y), r - 2) # Or clair
        # Symbole $
        dollar = self.small_bold_font.render("$", True, (218, 165, 32))
        dollar_rect = dollar.get_rect(center=(start_x + r, y))
        self.screen.blit(dollar, dollar_rect)
        
        # Texte montant
        self.screen.blit(text_surf, (start_x + r*2 + padding, y - text_surf.get_height()//2))

    def choose_custom_avatar(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Choisir une image de profil",
                filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")]
            )
            root.destroy()
            
            if file_path:
                # Chargement et redimensionnement
                try:
                    self.crop_image = pygame.image.load(file_path).convert_alpha()
                    # Adapter la taille initiale si trop grande
                    if self.crop_image.get_width() > 1000 or self.crop_image.get_height() > 1000:
                        scale = 1000 / max(self.crop_image.get_width(), self.crop_image.get_height())
                        new_size = (int(self.crop_image.get_width() * scale), int(self.crop_image.get_height() * scale))
                        self.crop_image = pygame.transform.smoothscale(self.crop_image, new_size)
                    
                    self.crop_scale = 1.0
                    self.crop_offset = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
                    self.set_state("CROP_AVATAR")
                except Exception as e:
                    print(f"Erreur image: {e}")
        except Exception as e:
            print(f"Erreur dialogue: {e}")

    def validate_crop(self):
        if self.crop_image:
            try:
                # Création de la surface de rendu (Taille du cercle de crop : 300px)
                crop_size = 300
                surf = pygame.Surface((crop_size, crop_size), pygame.SRCALPHA)
                
                # Calculs de position relative
                img_w = int(self.crop_image.get_width() * self.crop_scale)
                img_h = int(self.crop_image.get_height() * self.crop_scale)
                
                # Centre de l'écran vs Centre de l'image
                rel_x = self.crop_offset[0] - SCREEN_WIDTH // 2
                rel_y = self.crop_offset[1] - SCREEN_HEIGHT // 2
                
                # Position de l'image sur la surface de crop (centrée)
                blit_x = (crop_size // 2) + rel_x - (img_w // 2)
                blit_y = (crop_size // 2) + rel_y - (img_h // 2)
                
                scaled_img = pygame.transform.smoothscale(self.crop_image, (img_w, img_h))
                surf.blit(scaled_img, (blit_x, blit_y))
                
                # Redimensionnement final pour stockage (100x100)
                final_surf = pygame.transform.smoothscale(surf, (100, 100))
                
                buffer = io.BytesIO()
                pygame.image.save(final_surf, buffer, "PNG")
                img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                self.avatar = "IMG:" + img_str
            except Exception as e:
                print(f"Erreur crop: {e}")
        self.set_state("INPUT_NAME")

    def get_name_color(self, item_id):
        if item_id == "name_color_rainbow":
            hue = (pygame.time.get_ticks() // 5) % 360
            c = pygame.Color(0)
            c.hsla = (hue, 100, 50, 100)
            return (c.r, c.g, c.b)
        if item_id in SHOP_CATALOG and SHOP_CATALOG[item_id]['type'] == 'name_color':
            return SHOP_CATALOG[item_id]['color']
        return TEXT_COLOR

    def unequip_item(self, type_):
        # Déséquiper = remettre par défaut
        default_id = f"{type_}_default"
        self.equipped[type_] = default_id
        self.save_settings()
        self.create_menu_buttons()

    def generate_daily_shop(self):
        today = str(datetime.date.today())
        if self.last_shop_date != today:
            self.last_shop_date = today
            # Génération déterministe basée sur la date
            random.seed(today)
            keys = list(SHOP_CATALOG.keys())
            # Toujours le cadeau gratuit + 2 items aléatoires
            daily = ["gift_daily"]
            available = [k for k in keys if k != "gift_daily"]
            daily.extend(random.sample(available, 2))
            self.shop_items = daily
            random.seed() # Reset seed
            self.save_settings()
        elif not self.shop_items:
            # Fallback si vide
            self.shop_items = ["gift_daily", "border_gold", "theme_ocean"]

    def buy_item(self, item_id, pos=None):
        if item_id in SHOP_CATALOG:
            item = SHOP_CATALOG[item_id]
            # Autoriser les doublons pour les améliorations (Upgrades) et Cadeaux
            if item_id not in self.inventory or item.get('type') in ['upgrade', 'gift']:
                if self.coins >= item['price']:
                    if item.get('type') == 'gift':
                        today = str(datetime.date.today())
                        if self.last_gift_date == today:
                            self.show_notification("Déjà récupéré aujourd'hui !")
                            self.play_sound("buzz")
                            return
                        reward = random.randint(50, 150)
                        self.coins += reward
                        self.last_gift_date = today
                        self.show_notification(f"Cadeau : +{reward} pièces !")
                    else:
                        self.coins -= item['price']
                        self.inventory.append(item_id)
                        if item.get('type') == 'category':
                            self.all_categories[item['name']] = item['content']
                    self.save_settings()
                    self.check_achievements()
                    self.play_sound("start") # Son achat
                    if pos:
                        for _ in range(40):
                            self.particles.append({
                                'x': pos[0], 'y': pos[1],
                                'vx': random.uniform(-8, 8), 'vy': random.uniform(-8, 8),
                                'life': 255, 'color': (255, 215, 0), 'size': random.randint(4, 10)
                            })
                        for _ in range(20):
                            self.particles.append({
                                'x': pos[0], 'y': pos[1],
                                'vx': random.uniform(-5, 5), 'vy': random.uniform(-5, 5),
                                'life': 255, 'color': (255, 255, 255), 'size': random.randint(2, 6)
                            })
                    self.create_menu_buttons()
                else:
                    self.show_notification("Pas assez de pièces !")
                    self.play_sound("buzz")

    def equip_item(self, item_id):
        if item_id in SHOP_CATALOG or item_id.endswith("_default"):
            type_ = "border" if "border" in item_id else ("theme" if "theme" in item_id else "name_color")
            if item_id in SHOP_CATALOG: type_ = SHOP_CATALOG[item_id]['type']
            
            self.equipped[type_] = item_id
            self.save_settings()
            self.create_menu_buttons()

    def set_shop_tab(self, tab):
        self.shop_tab = tab
        self.shop_scroll = 0
        self.create_menu_buttons()

    def request_trade(self, ip):
        threading.Thread(target=self._send_trade_req_thread, args=(ip,), daemon=True).start()

    def _send_trade_req_thread(self, ip):
        try:
            self.show_notification("Envoi demande échange...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, PORT))
            s.sendall(f"INTENT_TRADE|{self.username}|{self.avatar}\n".encode())
            resp = s.recv(1024).decode().strip()
            if resp == "ACCEPT":
                self.accept_trade(s, "Ami", "?") # On récupérera les infos après
            else:
                s.close()
                self.show_notification("Demande refusée")
        except: self.show_notification("Joueur introuvable")

    def accept_trade(self, conn, name, avatar):
        self.conn = conn
        self.connected = True
        self.opponent_name = name
        self.opponent_avatar = avatar
        self.trade_lobby_data = {"me": {"coins": 0, "items": [], "locked": False}, "them": {"coins": 0, "items": [], "locked": False}, "countdown": None}
        self.set_state("TRADE_LOBBY")
        threading.Thread(target=self.receive_data, daemon=True).start()
        self.popup = None

    def update_trade_lock(self):
        self.trade_lobby_data["me"]["locked"] = not self.trade_lobby_data["me"]["locked"]
        self.send_trade_update()

    def add_trade_coin(self, amount):
        if not self.trade_lobby_data["me"]["locked"]:
            if self.coins >= self.trade_lobby_data["me"]["coins"] + amount:
                self.trade_lobby_data["me"]["coins"] += amount
                self.send_trade_update()

    def unlock_achievement(self, ach_id):
        if ach_id in ACHIEVEMENTS and ach_id not in self.achievements_unlocked:
            self.achievements_unlocked.append(ach_id)
            reward = ACHIEVEMENTS[ach_id]["reward"]
            self.coins += reward
            # self.show_notification(f"SUCCÈS : {ACHIEVEMENTS[ach_id]['name']} (+{reward}$)") # Remplacé par popup
            self.achievement_queue.append(ACHIEVEMENTS[ach_id])
            self.play_sound("coin")
            self.save_settings()
            
            # Broadcast en ligne
            if self.connected or self.is_host:
                self.send_data(f"CHAT|SYSTEM: {self.username} a débloqué {ACHIEVEMENTS[ach_id]['name']} !")

    def check_achievements(self):
        if self.stats["wins"] >= 1: self.unlock_achievement("WIN_1")
        if self.stats["wins"] >= 10: self.unlock_achievement("WIN_10")
        
        if self.level >= 5: self.unlock_achievement("LEVEL_5")
        if self.level >= 10: self.unlock_achievement("LEVEL_10")
        
        if self.coins >= 500: self.unlock_achievement("RICH")
        if self.coins >= 2000: self.unlock_achievement("RICH_2000")
        
        if len(self.friends) > 0: self.unlock_achievement("SOCIAL")
        if len(self.friends) >= 5: self.unlock_achievement("SOCIAL_MAX")
        if len(self.inventory) > 2: self.unlock_achievement("SHOPPER")
        if len(self.inventory) >= 10: self.unlock_achievement("COLLECTOR")
        if self.stats["wins"] >= 50: self.unlock_achievement("WIN_50")
        
        # Check Shop King
        shop_items = [k for k in SHOP_CATALOG.keys() if k != "gift_daily"]
        owned = [i for i in self.inventory if i in shop_items]
        if len(owned) >= len(shop_items): self.unlock_achievement("SHOP_KING")

    def send_trade_update(self):
        d = self.trade_lobby_data["me"]
        self.send_data(f"TRADE_UPDATE|{d['coins']}|{','.join(d['items'])}|{int(d['locked'])}")

    def export_save(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            filename = filedialog.asksaveasfilename(
                title="Exporter la sauvegarde",
                defaultextension=".json",
                filetypes=[("Fichier JSON", "*.json")],
                initialfile="wordrush_backup.json"
            )
            root.destroy()
            
            if filename:
                data = {
                    "settings": {
                        "username": self.username, "avatar": self.avatar, 
                        "sound": self.sound_on, "keys": self.keys, 
                        "first_run": self.first_run, "friends": self.friends, 
                        "xp": self.xp, "level": self.level, 
                        "custom_categories": self.custom_categories,
                        "coins": self.coins, "inventory": self.inventory,
                        "equipped": self.equipped, "achievements": self.achievements_unlocked,
                        "stats": self.stats
                    },
                    "history": self.used_words
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                
                self.feedback_msg = "SAUVEGARDE EXPORTÉE !"
                self.feedback_timer = pygame.time.get_ticks()
        except Exception as e:
            print(f"Erreur export: {e}")

    def import_save(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            filename = filedialog.askopenfilename(title="Importer une sauvegarde", filetypes=[("Fichier JSON", "*.json")])
            root.destroy()
            
            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                if "settings" in data:
                    with open(SETTINGS_FILE, 'w') as f:
                        json.dump(data["settings"], f, indent=4)
                if "history" in data:
                    with open(HISTORY_FILE, 'w') as f:
                        json.dump(data["history"], f, indent=4)
                
                self.load_settings()
                self.feedback_msg = "SAUVEGARDE IMPORTÉE !"
                self.feedback_timer = pygame.time.get_ticks()
                self.create_menu_buttons()
        except Exception as e:
            print(f"Erreur import: {e}")
            self.feedback_msg = "ERREUR IMPORT !"
            self.feedback_timer = pygame.time.get_ticks()

    def join_friend(self, ip):
        self.input_ip = ip
        self.connect_to_host()

    def create_menu_buttons(self):
        cx = SCREEN_WIDTH // 2
        self.buttons = []
        if self.state == "TUTORIAL":
            self.buttons = [
                Button("J'AI COMPRIS !", cx - 150, 650, 300, 70, ACCENT_COLOR, HOVER_COLOR, self.close_tutorial)
            ]

        elif self.state == "INPUT_NAME":
            # Boutons de sélection d'avatar
            cy = SCREEN_HEIGHT // 2
            
            # Zone de défilement pour les avatars (Sous la photo de profil)
            scroll_y_start = cy - 150
            
            # Grille d'avatars
            cols = 10
            btn_size = 45
            gap = 10
            total_w = cols * btn_size + (cols - 1) * gap
            start_x = cx - total_w // 2
            
            self.avatar_grid_buttons = []
            
            for i, av in enumerate(AVATARS):
                row = i // cols
                col = i % cols
                bx = start_x + col * (btn_size + gap)
                by = scroll_y_start + row * (btn_size + gap) - self.avatar_scroll
                color = ACCENT_COLOR if av == self.avatar else PANEL_COLOR
                self.avatar_grid_buttons.append(Button(av, bx, by, btn_size, btn_size, color, HOVER_COLOR, lambda a=av: self.set_avatar(a), font=self.ui_emoji_font, text_color=(255,255,255), scale_on_hover=True))

            # Dé à côté du profil (Profil à cy - 260)
            self.buttons.append(Button("🎲", cx + 90, cy - 290, 60, 60, PANEL_COLOR, HOVER_COLOR, self.random_avatar, font=self.ui_emoji_font, text_color=(255, 255, 255)))
            self.buttons.append(Button("📷", cx + 160, cy - 290, 60, 60, PANEL_COLOR, HOVER_COLOR, self.choose_custom_avatar, font=self.ui_emoji_font, text_color=(255, 255, 255)))
            self.buttons.append(Button("HISTORIQUE", cx - 125, cy + 180, 250, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_HISTORY")))
            self.buttons.append(Button("VALIDER", cx - 125, cy + 260, 250, 70, ACCENT_COLOR, HOVER_COLOR, self.validate_name))

        elif self.state == "MENU_MAIN":
            # Redesign complet du menu principal
            self.buttons = [
                Button("JOUER EN LOCAL\n(Même PC)", cx - 300, 320, 250, 150, ACCENT_COLOR, HOVER_COLOR, self.setup_local, font=self.small_bold_font, scale_on_hover=True),
                Button("JOUER EN LIGNE\n(Réseau)", cx + 50, 320, 250, 150, (0, 150, 255), (50, 180, 255), lambda: self.set_state("MENU_ONLINE"), font=self.small_bold_font, scale_on_hover=True),
            ]
            
            # Barre d'outils en bas
            btn_w = 200
            btn_h = 60
            gap = 20
            start_y = 550
            self.buttons = [
                *self.buttons,
                Button("MON PROFIL", cx - 320, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("INPUT_NAME")),
                Button("INVENTAIRE", cx - 100, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_INVENTORY")),
                Button("MAGASIN", cx + 120, start_y, btn_w, btn_h, (255, 200, 0), (255, 220, 50), lambda: self.set_state("MENU_SHOP"), text_color=(50, 40, 0)),
                Button("AMIS", cx - 320, start_y + 80, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_FRIENDS")),
                Button("SUCCÈS", cx - 100, start_y + 80, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_ACHIEVEMENTS")),
                Button("PARAMÈTRES", cx + 120, start_y + 80, btn_w, btn_h, (100, 100, 120), (140, 140, 160), lambda: self.set_state("SETTINGS")),
                Button("QUITTER", cx - 100, start_y + 160, btn_w, btn_h, ALERT_COLOR, (255, 100, 120), self.ask_quit),
                Button("?", SCREEN_WIDTH - 80, 30, 50, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("HOW_TO"))
            ]

        elif self.state == "MENU_ONLINE":
            self.buttons = [
                Button("HÉBERGER", cx - 250, 350, 240, 60, ACCENT_COLOR, HOVER_COLOR, self.setup_host),
                Button("REJOINDRE", cx + 10, 350, 240, 60, ACCENT_COLOR, HOVER_COLOR, self.setup_join),
                Button("RETOUR", cx - 120, 500, 240, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "SETUP":
            # --- NOUVELLE INTERFACE DE CONFIGURATION INTUITIVE ---
            cx = SCREEN_WIDTH // 2
            current_y = 220 # Starting Y for the first setting block (Aligné avec l'affichage)
            block_gap = 100 # Vertical space between setting blocks (Aligné avec l'affichage)
            
            btn_off = 220   # Écartement élargi (était 150)
            btn_off_wide = 300 # Écartement pour textes longs (était 280)
            
            # 1. Joueurs
            if self.is_local_game or self.is_host:
                self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', -1)))
                self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', 1)))
            current_y += block_gap
            
            # 2. Mode
            self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('mode', 0)))
            self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('mode', 0)))
            current_y += block_gap
            
            # 3. Catégorie
            self.buttons.append(Button("<", cx - btn_off_wide, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', -1)))
            self.buttons.append(Button(">", cx + btn_off_wide - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', 1)))
            current_y += block_gap
            
            # 4. Temps
            self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', -1)))
            self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', 1)))
            current_y += block_gap

            # 5. Type de Jeu (Normal / Survie)
            self.buttons.append(Button("<", cx - btn_off_wide, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('game_type', -1)))
            self.buttons.append(Button(">", cx + btn_off_wide - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('game_type', 0)))
            current_y += block_gap

            # Valider
            action = self.start_local_game if self.is_local_game else self.start_host_lobby
            self.buttons = [
                *self.buttons,
                Button("LANCER LA PARTIE", cx - 200, 780, 400, 80, ACCENT_COLOR, HOVER_COLOR, action),
                Button("RETOUR", 40, 40, 120, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "SETTINGS":
            cx = SCREEN_WIDTH // 2
            sound_txt = "SON : ON" if self.sound_on else "SON : OFF"
            sound_col = ACCENT_COLOR if self.sound_on else (100, 100, 100)
            res_txt = f"RÉSOLUTION : {SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            self.buttons = [
                Button(res_txt, cx - 400, 220, 800, 50, PANEL_COLOR, HOVER_COLOR, self.cycle_resolution),
                Button(sound_txt, cx - 400, 280, 800, 50, sound_col, HOVER_COLOR, self.toggle_sound),
                Button("CATÉGORIES PERSO", cx - 400, 340, 800, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_CUSTOM_CATS")),
                Button("TOUCHES / CLAVIER", cx - 400, 400, 800, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("CONTROLS")),
                Button("EXPORTER SAUVEGARDE", cx - 400, 460, 800, 50, PANEL_COLOR, HOVER_COLOR, self.export_save, font=self.small_bold_font),
                Button("IMPORTER SAUVEGARDE", cx - 400, 520, 800, 50, PANEL_COLOR, HOVER_COLOR, self.import_save, font=self.small_bold_font),
                Button("RÉINITIALISER DONNÉES", cx - 400, 580, 800, 50, ALERT_COLOR, (255, 100, 120), self.reset_app),
                Button("RETOUR", cx - 400, 750, 800, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "MENU_SHOP":
            cx = SCREEN_WIDTH // 2
            
            # Onglets (Tabs)
            tab_w = 130
            self.buttons.append(Button("TOUT", cx - 350, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "ALL" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("ALL")))
            self.buttons.append(Button("BORDURES", cx - 210, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "BORDER" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("BORDER")))
            self.buttons.append(Button("COULEURS", cx - 70, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "COLOR" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("COLOR")))
            self.buttons.append(Button("THÈMES", cx + 70, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "THEME" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("THEME")))
            self.buttons.append(Button("PACKS", cx + 210, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "CATEGORY" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("CATEGORY")))

            # Configuration Grille
            card_w, card_h = 260, 300
            cols = 5
            gap = 30
            start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
            start_y = 220 - self.shop_scroll # Décalé pour les onglets
            
            # Tous les items du catalogue (Triés par type puis prix)
            all_items = list(SHOP_CATALOG.keys())
            all_items.sort(key=lambda x: (SHOP_CATALOG[x]['type'], SHOP_CATALOG[x]['price']))
            
            # Filtrage
            filtered_items = []
            for item_id in all_items:
                item = SHOP_CATALOG[item_id]
                if self.shop_tab == "ALL": filtered_items.append(item_id)
                elif self.shop_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                elif self.shop_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                elif self.shop_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                elif self.shop_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)

            for i, item_id in enumerate(filtered_items):
                item = SHOP_CATALOG[item_id]
                row = i // cols
                col = i % cols
                x = start_x + col * (card_w + gap)
                y = start_y + row * (card_h + gap)
                
                # Clipping simple pour ne pas dessiner par dessus le header
                if y + card_h < 200 or y > SCREEN_HEIGHT: continue
                
                # Bouton Action (Acheter / Équiper)
                btn_h = 50
                btn_y = y + card_h - btn_h - 15
                
                if item_id in self.inventory:
                    if self.equipped.get(item['type']) == item_id:
                        self.buttons.append(Button("ÉQUIPÉ", x + 20, btn_y, card_w - 40, btn_h, (50, 150, 50), (50, 150, 50), None, font=self.small_bold_font))
                    elif item['type'] == 'category':
                        self.buttons.append(Button("DÉBLOQUÉ", x + 20, btn_y, card_w - 40, btn_h, (100, 100, 100), (100, 100, 100), None, font=self.small_bold_font))
                    else:
                        self.buttons.append(Button("ÉQUIPER", x + 20, btn_y, card_w - 40, btn_h, PANEL_COLOR, HOVER_COLOR, lambda id=item_id: self.equip_item(id), font=self.small_bold_font))
                else:
                    if item['type'] == 'gift' and self.last_gift_date == str(datetime.date.today()):
                        self.buttons.append(Button("RÉCUPÉRÉ", x + 20, btn_y, card_w - 40, btn_h, (100, 100, 100), (100, 100, 100), None, font=self.small_bold_font))
                    else:
                        price_txt = f"{item['price']}"
                        if item['price'] == 0: price_txt = "GRATUIT"
                        can_buy = self.coins >= item['price']
                        color = ACCENT_COLOR if can_buy else (80, 80, 80)
                        center_pos = (x + card_w//2, y + card_h//2)
                        action = lambda id=item_id, p=center_pos: self.buy_item(id, p)
                        self.buttons.append(Button(price_txt, x + 20, btn_y, card_w - 40, btn_h, color, HOVER_COLOR, action, font=self.small_bold_font))

            self.buttons.append(Button("RETOUR", 40, 40, 120, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))

        elif self.state == "MENU_INVENTORY":
            cx = SCREEN_WIDTH // 2
            # Configuration Grille
            card_w, card_h = 260, 300
            cols = 5
            gap = 30
            start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
            start_y = 200 - self.shop_scroll
            
            # Liste des items possédés (hors défauts)
            owned_items = [i for i in self.inventory if i in SHOP_CATALOG]
            
            if not owned_items:
                self.buttons.append(Button("MAGASIN", cx - 100, 400, 200, 60, (255, 200, 0), (255, 220, 50), lambda: self.set_state("MENU_SHOP"), text_color=(50, 40, 0)))
            
            for i, item_id in enumerate(owned_items):
                item = SHOP_CATALOG[item_id]
                row = i // cols
                col = i % cols
                x = start_x + col * (card_w + gap)
                y = start_y + row * (card_h + gap)
                
                # Clipping
                if y + card_h < 100 or y > SCREEN_HEIGHT: continue
                
                btn_h = 50
                btn_y = y + card_h - btn_h - 15
                
                if self.equipped.get(item['type']) == item_id:
                    self.buttons.append(Button("DÉSÉQUIPER", x + 20, btn_y, card_w - 40, btn_h, (200, 80, 80), (220, 100, 100), lambda t=item['type']: self.unequip_item(t), font=self.small_bold_font))
                elif item['type'] == 'category':
                    self.buttons.append(Button("DÉBLOQUÉ", x + 20, btn_y, card_w - 40, btn_h, (100, 100, 100), (100, 100, 100), None, font=self.small_bold_font))
                else:
                    self.buttons.append(Button("ÉQUIPER", x + 20, btn_y, card_w - 40, btn_h, ACCENT_COLOR, HOVER_COLOR, lambda id=item_id: self.equip_item(id), font=self.small_bold_font))

            self.buttons.append(Button("RETOUR", 40, 40, 120, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))

        elif self.state == "MENU_FRIENDS":
            start_y = 220
            # Récupérer l'IP si pas encore fait
            if self.public_ip is None:
                threading.Thread(target=self.get_public_ip, daemon=True).start()
                
            for i, friend in enumerate(self.friends):
                # Bouton Rejoindre Ami
                self.buttons.append(Button("REJOINDRE", cx + 120, start_y + i*70, 160, 50, ACCENT_COLOR, HOVER_COLOR, lambda ip=friend['ip']: self.join_friend(ip)))
                # Bouton Échanger
                self.buttons.append(Button("ECHANGER (A)", cx + 300, start_y + i*70, 180, 50, (255, 200, 0), (255, 220, 50), lambda ip=friend['ip']: self.request_trade(ip), text_color=(50, 40, 0)))
                # Bouton Supprimer (X)
                self.buttons.append(Button("X", cx + 500, start_y + i*70, 50, 50, ALERT_COLOR, (255, 100, 100), lambda idx=i: self.delete_friend(idx)))
            
            # Bouton Copier IP
            self.buttons.append(Button("COPIER CODE AMI", cx + 180, 160, 180, 40, ACCENT_COLOR, HOVER_COLOR, self.copy_ip, font=pygame.font.SysFont("Arial", 16, bold=True)))
            
            self.buttons.append(Button("AJOUTER UN AMI", cx - 200, 750, 400, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_ADD_FRIEND")))
            self.buttons.append(Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))
        elif self.state == "MENU_ADD_FRIEND":
            self.buttons = [
                Button("ENVOYER DEMANDE", cx - 200, 550, 400, 60, ACCENT_COLOR, HOVER_COLOR, self.request_friend),
                Button("ANNULER", cx - 200, 630, 400, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_FRIENDS"))
            ]
        elif self.state == "MENU_HISTORY":
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("INPUT_NAME"))
            ]
        elif self.state == "MENU_ACHIEVEMENTS":
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "TRADE_LOBBY":
            cx = SCREEN_WIDTH // 2
            lock_txt = "VERROUILLER" if not self.trade_lobby_data["me"]["locked"] else "ATTENTE..."
            lock_col = ACCENT_COLOR if not self.trade_lobby_data["me"]["locked"] else (100, 100, 100)
            self.buttons = [
                Button("+10 Pièces", cx - 300, 500, 150, 50, (255, 215, 0), HOVER_COLOR, lambda: self.add_trade_coin(10), text_color=(0,0,0)),
                Button("+50 Pièces", cx - 300, 560, 150, 50, (255, 215, 0), HOVER_COLOR, lambda: self.add_trade_coin(50), text_color=(0,0,0)),
                Button(lock_txt, cx - 100, 650, 200, 60, lock_col, HOVER_COLOR, self.update_trade_lock),
                Button("QUITTER", cx - 100, 600, 200, 60, ALERT_COLOR, (255, 100, 120), self.reset_network)
            ]
        elif self.state == "MENU_CUSTOM_CATS":
            cx = SCREEN_WIDTH // 2
            start_y = 200
            for i, cat in enumerate(self.custom_categories.keys()):
                self.buttons.append(Button("X", cx + 200, start_y + i*60, 50, 50, ALERT_COLOR, (255, 100, 100), lambda c=cat: self.delete_custom_category(c)))
            
            self.buttons.append(Button("NOUVELLE CATÉGORIE", cx - 150, 600, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("EDIT_CAT_NAME")))
            self.buttons.append(Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETTINGS")))
        elif self.state == "EDIT_CAT_NAME":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("SUIVANT", cx - 150, 500, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("EDIT_CAT_WORDS") if self.cat_name_input else None),
                Button("ANNULER", cx - 150, 580, 300, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_CUSTOM_CATS"))
            ]
        elif self.state == "EDIT_CAT_WORDS":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("SAUVEGARDER", cx - 150, 600, 300, 60, ACCENT_COLOR, HOVER_COLOR, self.save_custom_category),
                Button("RETOUR", cx - 150, 680, 300, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("EDIT_CAT_NAME"))
            ]
        elif self.state == "CONTROLS":
            cx = SCREEN_WIDTH // 2
            # Simple toggle pour l'exemple, ou juste affichage
            contest_key = "MAJ GAUCHE" if self.keys["CONTEST"] == pygame.K_LSHIFT else "TAB"
            validate_key = "ENTRÉE"
            self.buttons = [
                Button(f"CONTESTER : {contest_key}", cx - 200, 300, 400, 60, PANEL_COLOR, HOVER_COLOR, self.toggle_contest_key),
                Button(f"VALIDER : {validate_key}", cx - 200, 400, 400, 60, PANEL_COLOR, PANEL_COLOR, None), # Informatif
                Button("RETOUR", cx - 200, 600, 400, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("SETTINGS"))
            ]
        elif self.state == "OPPONENT_LEFT":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("MENU PRINCIPAL", cx - 150, 500, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "MENU_JOIN":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("CONNEXION", cx - 150, 500, 300, 70, ACCENT_COLOR, HOVER_COLOR, self.connect_to_host),
                Button("MES AMIS", cx - 150, 590, 300, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_FRIENDS")),
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_ONLINE"))
            ]
        elif self.state == "GAME_OVER":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("RECOMMENCER" if not self.rematch_ready[self.my_id] else "EN ATTENTE...", 
                       cx - 300, 500, 250, 60, 
                       ACCENT_COLOR if not self.rematch_ready[self.my_id] else (100, 100, 100), 
                       HOVER_COLOR, self.request_rematch),
                Button("MENU PRINCIPAL", cx + 50, 500, 250, 60, PANEL_COLOR, HOVER_COLOR, self.reset_network),
                Button("QUITTER", cx - 100, 600, 200, 60, ALERT_COLOR, (255, 100, 120), self.ask_quit)
            ]
        elif self.state == "CONFIRM_QUIT":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("OUI, QUITTER", cx - 210, 500, 200, 60, ALERT_COLOR, (255, 100, 100), self.force_quit),
                Button("NON, RETOUR", cx + 10, 500, 200, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state(self.prev_state))
            ]
        elif self.state == "CONFIRM_LEAVE":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("OUI, QUITTER", cx - 210, 500, 200, 60, ALERT_COLOR, (255, 100, 100), self.reset_network),
                Button("NON, RESTER", cx + 10, 500, 200, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("LOBBY"))
            ]
        elif self.state == "LOBBY":
            self.update_lobby_buttons()

    def set_state(self, new_state):
        if new_state == self.state: return
        self.next_state = new_state
        self.transition_state = "OUT"

    def _apply_state_change(self):
        self.buttons = []
        self.avatar_grid_buttons = []
        if self.state == "INPUT_NAME":
            self.avatar_scroll = 0
        if self.state == "MENU_FRIENDS":
            self.connect_status = "" # Reset copy feedback
        if self.state in ["MENU_SHOP", "MENU_INVENTORY"]:
            self.shop_scroll = 0
        if self.state == "MENU_ACHIEVEMENTS":
            self.achievements_scroll = 0
            
        if self.state in ["MENU_MAIN", "MENU_ONLINE", "SETUP", "INPUT_NAME", "GAME_OVER", "SETTINGS", "CONTROLS", "OPPONENT_LEFT", "MENU_JOIN", "TUTORIAL", "MENU_FRIENDS", "MENU_ADD_FRIEND", "CONFIRM_QUIT", "CONFIRM_LEAVE", "MENU_CUSTOM_CATS", "EDIT_CAT_NAME", "EDIT_CAT_WORDS", "MENU_SHOP", "MENU_INVENTORY", "TRADE_LOBBY", "CROP_AVATAR", "MENU_ACHIEVEMENTS", "MENU_HISTORY"]:
            self.create_menu_buttons()
        elif self.state == "HOW_TO":
            self.buttons = [Button("RETOUR", 50, 50, 150, 50, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))]
        elif self.state == "LOBBY":
            self.update_lobby_buttons()
        elif self.state == "JUDGMENT":
            cx = SCREEN_WIDTH // 2
            if self.is_local_game or self.judge_id == self.my_id:
                self.buttons = [
                    Button("QUITTER", 20, 20, 120, 40, ALERT_COLOR, (255, 100, 100), self.quit_game),
                    Button("RECOMMENCER (R)", cx - 320, 300, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.send_action("RESTART")),
                    Button("POINT ADVERSE (P)", cx + 20, 300, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.send_action("POINT")),
                    Button("ANNULER (C)", cx - 100, 400, 200, 60, (100, 100, 100), (150, 150, 150), lambda: self.send_action("CONTINUE"))
                ]
            else:
                self.buttons = []
        elif self.state == "CROP_AVATAR":
            self.buttons = [
                Button("VALIDER", SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT - 100, 150, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_crop),
                Button("ANNULER", SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT - 100, 150, 60, ALERT_COLOR, (255, 100, 100), lambda: self.set_state("INPUT_NAME"))
            ]

    def update_lobby_buttons(self):
        cx = SCREEN_WIDTH // 2
        self.buttons = []
        
        # Bouton Retour
        self.buttons.append(Button("RETOUR", 50, 50, 150, 50, ALERT_COLOR, (255, 100, 120), self.ask_leave_lobby))
        
        # Bouton Prêt
        ready_col = (100, 200, 100) if self.ready_status[self.my_id] else (200, 100, 100)
        ready_txt = "ANNULER" if self.ready_status[self.my_id] else "PRÊT !"
        # Position sous le panneau joueurs (50, 100, 600, 650) -> Center X = 350, Bottom Y = 750
        self.buttons.append(Button(ready_txt, 350 - 125, 770, 250, 70, ready_col, HOVER_COLOR, self.toggle_ready, font=self.medium_font))

        # Boutons Ajouter Ami (Lobby)
        for i in range(self.settings['players']):
            # Identifier le joueur
            p_ip = None
            p_name = ""
            is_me = False
            
            if self.is_host:
                if i == 0: is_me = True
                elif i - 1 < len(self.clients):
                    p_ip = self.clients[i-1].get('ip')
                    p_name = self.clients[i-1].get('name')
            else:
                if i == self.my_id: is_me = True
                elif i in self.lobby_cache:
                    p_ip = self.lobby_cache[i].get('ip')
                    p_name = self.lobby_cache[i].get('name')
                elif i == 0 and not self.is_local_game: # Host
                    p_ip = self.input_ip
                    p_name = "Hôte" # Nom pas toujours dispo ici si pas dans cache, mais bon

            # Si joueur valide, pas moi, et pas déjà ami -> Bouton +
            if not is_me and p_ip and not any(f['ip'] == p_ip for f in self.friends):
                y_pos = 180 + i * 100
                self.buttons.append(Button("+", 550, y_pos - 20, 40, 40, (50, 200, 50), HOVER_COLOR, lambda ip=p_ip, n=p_name: self.direct_add_friend(ip, n)))

        # Boutons Kick (Host)
        if self.is_host:
            for i, client in enumerate(self.clients):
                # i=0 is first client. Display index is i+1 (0 is host)
                y_pos = 180 + (i + 1) * 100
                self.buttons.append(Button("X", 600, y_pos - 20, 40, 40, ALERT_COLOR, (255, 100, 100), lambda cid=client['id']: self.kick_client(cid)))

        # Bouton Wizz
        chat_x = 680
        chat_w = SCREEN_WIDTH - chat_x - 50
        chat_bottom = SCREEN_HEIGHT - 50
        self.buttons.append(Button("WIZZ", chat_x + chat_w - 100, chat_bottom - 55, 80, 40, (255, 200, 0), (255, 220, 50), lambda: self.send_action("BUZZ"), text_color=(0,0,0), font=self.small_bold_font))

    def validate_name(self):
        if len(self.username) > 0:
            self.save_settings()
            self.set_state("MENU_MAIN")

    def change_setting(self, key, delta):
        if key == 'players':
            self.settings['players'] = max(2, min(4, self.settings['players'] + delta)) # Max 4 joueurs pour fiabilité
            # Réinitialiser les scores si on change le nombre de joueurs
            self.score = [0] * self.settings['players']
            self.ready_status = [False] * self.settings['players']
            self.rematch_ready = [False] * self.settings['players']
        elif key == 'time':
            limit = 20 if self.settings['mode'] == 'WRITTEN' else 10
            self.settings['time'] = max(3, min(limit, self.settings['time'] + delta))
        elif key == 'win_score':
            self.settings['win_score'] = max(5, min(50, self.settings['win_score'] + delta))
        elif key == 'mode':
            self.settings['mode'] = 'WRITTEN' if self.settings['mode'] == 'VOCAL' else 'VOCAL'
        elif key == 'category':
            cats = list(self.all_categories.keys())
            current_idx = cats.index(self.settings['category'])
            next_idx = (current_idx + delta) % len(cats)
            if next_idx < 0: # Handle negative modulo result for previous button
                next_idx += len(cats)
            self.settings['category'] = cats[next_idx]
        elif key == 'game_type':
            modes = ['NORMAL', 'SURVIVAL', 'SPEED', 'HARDCORE', 'CHAOS']
            curr = self.settings.get('game_type', 'NORMAL')
            try:
                idx = modes.index(curr)
            except: idx = 0
            self.settings['game_type'] = modes[(idx + 1) % len(modes)]
        
        # Recréer les boutons pour mettre à jour l'affichage (si besoin)
        if self.state == "SETUP":
            self.create_menu_buttons()

    def toggle_contest_key(self):
        if self.keys["CONTEST"] == pygame.K_LSHIFT:
            self.keys["CONTEST"] = pygame.K_TAB
        else:
            self.keys["CONTEST"] = pygame.K_LSHIFT
        self.save_settings()
        self.create_menu_buttons()

    def toggle_ready(self):
        self.ready_status[self.my_id] = not self.ready_status[self.my_id]
        
        # En mode test (DEV), le bot se met prêt automatiquement avec nous
        if self.test_mode and self.is_host:
            self.ready_status[1] = self.ready_status[self.my_id]
            
        status_str = "1" if self.ready_status[self.my_id] else "0"
        if not self.is_local_game:
            if self.is_host:
                self.broadcast_player_list() # Host broadcast tout pour sync parfaite
            else:
                self.send_data(f"READY|{self.my_id}|{status_str}")
        self.create_menu_buttons() # Refresh color/text
        self.check_start_game()

    def quit_game(self):
        if not self.is_local_game:
            self.send_data("QUIT")
        self.reset_network()

    def handle_opponent_quit(self):
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        self.conn = None
        self.server = None
        self.connected = False
        self.set_state("OPPONENT_LEFT")

    # --- RÉSEAU ---
    def reset_network(self):
        self.remove_upnp()
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        self.conn = None
        self.server = None
        self.connected = False
        self.set_state("MENU_MAIN")
        self.chat_messages = []
        self.ready_status = [False, False]
        self.network_queue = [] # Vider la file pour éviter les bugs de retour en jeu

    def setup_local(self):
        self.is_local_game = True
        self.score = [0] * self.settings['players']
        self.rematch_ready = [False] * self.settings['players']
        self.set_state("SETUP")
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.ready_status = [False] * self.settings['players']
        self.turn_count = 0
        self.rally_combo = 0

    def start_local_game(self):
        self.start_round()

    def setup_host(self):
        self.is_host = True
        self.is_local_game = False
        self.my_id = 0
        self.clients = []
        self.settings['players'] = 2
        self.round_num = 1
        self.turn_count = 0
        self.rally_combo = 0
        self.score = [0, 0]
        self.last_round_reason = ""
        self.rematch_ready = [False, False]
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.ready_status = [False, False]
        self.set_state("SETUP")
        
        self.upnp_status = "Tentative..."
        # Récupération IP Locale fiable pour jouer sans ouvrir de ports (LAN)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.local_ip = s.getsockname()[0]
            s.close()
        except:
            self.local_ip = socket.gethostbyname(socket.gethostname())
            
        threading.Thread(target=self.get_public_ip, daemon=True).start()
        threading.Thread(target=self.try_upnp, daemon=True).start()

    def get_public_ip(self):
        try:
            self.public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8')
        except:
            self.public_ip = None

    def try_upnp(self):
        # Tentative d'ouverture de port automatique (UPnP) ULTRA ROBUSTE
        self.upnp_status = "Recherche Box..."
        import xml.etree.ElementTree as ET
        from urllib.parse import urlparse
        import re
        
        # Liste des services cibles (v1 et v2)
        target_services = [
            "urn:schemas-upnp-org:service:WANIPConnection:1",
            "urn:schemas-upnp-org:service:WANIPConnection:2",
            "urn:schemas-upnp-org:service:WANPPPConnection:1"
        ]

        try:
            # 1. Découverte SSDP (Broadcast multiple et écoute prolongée)
            msg = \
                'M-SEARCH * HTTP/1.1\r\n' \
                'HOST:239.255.255.250:1900\r\n' \
                'ST:urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n' \
                'MAN:"ssdp:discover"\r\n' \
                'MX:2\r\n' \
                '\r\n'
            
            locations = set()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.settimeout(2)
            s.sendto(msg.encode(), ('239.255.255.250', 1900))
            
            # On écoute pendant 2.5 secondes pour récupérer TOUTES les réponses
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < 2500:
                try:
                    data, addr = s.recvfrom(1024)
                    resp = data.decode(errors='ignore')
                    loc = re.search(r'LOCATION:\s*(.*)', resp, re.IGNORECASE)
                    if loc:
                        locations.add(loc.group(1).strip())
                except socket.timeout:
                    break
                except:
                    pass
            s.close()

            if not locations:
                self.upnp_status = "Box introuvable (UPnP OFF?)"
                return

            # 2. Essayer chaque appareil trouvé
            for location in locations:
                try:
                    # Téléchargement XML
                    xml_raw = urllib.request.urlopen(location, timeout=3).read().decode(errors='ignore')
                    
                    # Nettoyage namespaces pour parsing facile avec ElementTree
                    xml_clean = re.sub(r' xmlns="[^"]+"', '', xml_raw)
                    root = ET.fromstring(xml_clean)
                    
                    control_url = None
                    service_type = None
                    
                    # Recherche du service WAN (IP ou PPP)
                    for service in root.findall(".//service"):
                        stype = service.find("serviceType")
                        if stype is not None and stype.text in target_services:
                            surl = service.find("controlURL")
                            if surl is not None:
                                service_type = stype.text
                                control_url = surl.text
                                break
                    
                    if not control_url: continue

                    # Construction URL absolue
                    parsed = urlparse(location)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    
                    # Check URLBase
                    urlbase = root.find("URLBase")
                    if urlbase is not None and urlbase.text:
                        base_url = urlbase.text.rstrip("/")
                    
                    if not control_url.startswith("http"):
                        if not control_url.startswith("/"):
                            control_url = "/" + control_url
                        control_url = base_url + control_url

                    # 3. Envoi SOAP AddPortMapping
                    soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body><u:AddPortMapping xmlns:u="{service_type}">
<NewRemoteHost></NewRemoteHost><NewExternalPort>{PORT}</NewExternalPort><NewProtocol>TCP</NewProtocol>
<NewInternalPort>{PORT}</NewInternalPort><NewInternalClient>{self.local_ip}</NewInternalClient>
<NewEnabled>1</NewEnabled><NewPortMappingDescription>WorldRush</NewPortMappingDescription>
<NewLeaseDuration>0</NewLeaseDuration>
</u:AddPortMapping></s:Body></s:Envelope>"""
            
                    headers = {
                        'SOAPAction': f'"{service_type}#AddPortMapping"',
                        'Content-Type': 'text/xml',
                        'Connection': 'Close'
                    }
                    req = urllib.request.Request(control_url, soap_body.encode(), headers)
                    urllib.request.urlopen(req, timeout=3)
                    
                    self.upnp_status = "SUCCÈS (Port Ouvert)"
                    self.upnp_control_url = control_url
                    self.upnp_service_type = service_type
                    return
                except:
                    continue
            
            self.upnp_status = "ÉCHEC (Box incompatible)"
        except Exception as e:
            self.upnp_status = "Erreur Réseau"

    def remove_upnp(self):
        if self.upnp_control_url and self.upnp_service_type:
            print("Fermeture UPnP en cours...")
            success = False
            for i in range(2): # 2 tentatives pour être sûr
                try:
                    soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body><u:DeletePortMapping xmlns:u="{self.upnp_service_type}">
<NewRemoteHost></NewRemoteHost><NewExternalPort>{PORT}</NewExternalPort><NewProtocol>TCP</NewProtocol>
</u:DeletePortMapping></s:Body></s:Envelope>"""
                    headers = {'SOAPAction': f'"{self.upnp_service_type}#DeletePortMapping"', 'Content-Type': 'text/xml', 'Connection': 'Close'}
                    req = urllib.request.Request(self.upnp_control_url, soap_body.encode(), headers)
                    with urllib.request.urlopen(req, timeout=3) as response:
                        if response.status == 200:
                            print("UPnP: Port fermé avec succès !")
                            success = True
                            break
                except Exception as e:
                    print(f"Tentative {i+1} échouée: {e}")
            
            self.upnp_control_url = None

    def ask_quit(self):
        self.prev_state = self.state
        self.set_state("CONFIRM_QUIT")
        
    def ask_leave_lobby(self):
        self.prev_state = self.state
        self.set_state("CONFIRM_LEAVE")

    def host_receive_client_data(self, client):
        buffer = b""
        while True:
            try:
                if len(buffer) > 50000: buffer = b"" # Sécurité anti-flood
                data = client['conn'].recv(8192)
                if not data: break
                buffer += data
                while b"\n" in buffer:
                    msg_bytes, buffer = buffer.split(b"\n", 1)
                    msg = msg_bytes.decode('utf-8').strip()
                    if msg: self.network_queue.append(f"FROM|{client['id']}|{msg}")
            except Exception: break
        
        if client in self.clients:
            self.clients.remove(client)
            msg = f"SYSTEM: {client['name']} est parti."
            self.chat_messages.append(msg)
            self.send_data(f"CHAT|{msg}")
            self.broadcast_player_list()
            self.network_queue.append("REFRESH_LOBBY")

    def kick_client(self, client_id):
        for c in self.clients:
            if c['id'] == client_id:
                try: c['conn'].close()
                except: pass
                if c in self.clients: self.clients.remove(c)
                msg = f"SYSTEM: {c['name']} a été exclu."
                self.chat_messages.append(msg)
                self.broadcast_player_list()
                self.send_data(f"CHAT|{msg}")
                self.create_menu_buttons()
                break

    def force_quit(self):
        self.state = "EXITING"
        self.draw_background()
        self.draw_text("FERMETURE DES PORTS...", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.draw_text("Nettoyage UPnP et déconnexion...", self.font, TEXT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
        pygame.display.flip()
        
        self.remove_upnp()
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()

    def start_host_lobby(self):
        self.set_state("LOBBY")
        # Le listener global gère maintenant les connexions entrantes

    def broadcast_player_list(self):
        # Envoie la liste des joueurs à tout le monde
        # Format: PLAYERS|id,name,avatar,border,ready,name_color,ip;id,name...
        host_ip = self.public_ip if self.public_ip else self.local_ip
        p_list = [f"0,{self.username},{self.avatar},{self.equipped['border']},{int(self.ready_status[0])},{self.equipped['name_color']},{host_ip}"]
        for c in self.clients:
            p_list.append(f"{c['id']},{c['name']},{c['avatar']},{c['border']},{int(c['ready'])},{c.get('name_color', 'name_color_default')},{c.get('ip','')}")
        
        msg = "PLAYERS|" + ";".join(p_list)
        self.send_data(msg)
        # Update local info too (for Lobby UI)
        # self.network_queue.append(msg) # Pas besoin, on a déjà les infos locales

    def setup_join(self):
        self.is_host = False
        self.is_local_game = False
        self.my_id = 1
        self.settings['players'] = 2
        self.round_num = 1
        self.turn_count = 0
        self.rally_combo = 0
        self.score = [0, 0]
        self.last_round_reason = ""
        self.rematch_ready = [False, False]
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.set_state("MENU_JOIN")
        self.chat_messages = []
        self.ready_status = [False, False]
        self.connect_status = ""
        self.is_connecting = False
        self.reset_history()
        # Activer UPnP pour recevoir les demandes d'amis même en tant que client
        threading.Thread(target=self.try_upnp, daemon=True).start()

    def connect_to_host(self):
        if self.is_connecting: return
        self.is_connecting = True
        self.connect_status = "Connexion..."
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        try:
            if self.conn:
                try: self.conn.close()
                except: pass
                
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.settimeout(10) # Augmenté pour éviter le faux "Echec"
            self.conn.connect((self.input_ip, PORT))
            self.conn.sendall(f"INTENT_GAME|{self.username}|{self.avatar}|{self.equipped['border']}|{self.equipped['name_color']}\n".encode())
            self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Stabilité / Latence
            
            # Attente réponse ACCEPT
            resp = self.conn.recv(1024).decode().strip()
            if resp.startswith("ACCEPT"):
                self.my_id = int(resp.split("|")[1])
                self.conn.settimeout(None)
                self.connected = True
                self.connect_status = "Connecté !"
                self.set_state("LOBBY")
                threading.Thread(target=self.receive_data, daemon=True).start()
            else:
                self.connect_status = "Refusé / Plein"
                self.conn.close()
        except:
            self.connect_status = "Échec connexion"
            self.connected = False
        finally:
            self.is_connecting = False

    def receive_data(self):
        buffer = b""
        while self.connected:
            try:
                if len(buffer) > 50000: buffer = b"" # Sécurité anti-flood
                data = self.conn.recv(8192) # Augmenté pour supporter les images (Stabilité)
                if not data: break
                buffer += data
                while b"\n" in buffer:
                    msg_bytes, buffer = buffer.split(b"\n", 1)
                    try:
                        msg = msg_bytes.decode('utf-8').strip()
                        if msg: self.network_queue.append(msg)
                    except: pass
            except Exception:
                break
        self.connected = False
        self.set_state("MENU_MAIN")

    def send_data(self, data):
        if self.is_host:
            # Broadcast aux clients
            for c in self.clients:
                try:
                    c['conn'].sendall((data + "\n").encode())
                except: pass # Ignorer les erreurs d'envoi pour ne pas crash l'hôte
        else:
            # Client -> Host
            if self.conn:
                try:
                    self.conn.sendall((data + "\n").encode())
                except: pass

    def send_action(self, action):
        # Envoie une action et l'exécute localement aussi si nécessaire
        if not self.is_local_game:
            self.send_data(f"ACTION|{action}")
        self.process_action(action)
    
    def send_name(self):
        # Envoie mon pseudo à l'autre
        self.send_data(f"NAME|{self.username}|{self.avatar}|{self.equipped['border']}|{self.level}|{self.equipped['name_color']}")

    def send_chat(self):
        if self.chat_input.strip():
            msg = f"{self.username}: {self.chat_input}"
            self.chat_messages.append(msg)
            if not self.is_local_game:
                self.send_data(f"CHAT|{msg}")
            self.chat_input = ""

    def request_rematch(self):
        # Action locale et réseau
        if not self.is_local_game:
            self.send_data(f"ACTION|REMATCH|{self.my_id}")
        self.process_action(f"REMATCH|{self.my_id}")

    def get_random_word(self):
        return random.choice(self.all_categories[self.settings['category']])

    def check_start_game(self):
        # Si tout le monde est prêt
        if all(self.ready_status):
            if self.is_host or self.is_local_game:
                self.send_data(f"START|{self.settings['mode']}|{self.settings['time']}|{self.settings['win_score']}|{self.settings['category']}|{self.settings['game_type']}")
                self.start_round()

    def start_round(self, new_word=True, specific_word=None):
        # Seul l'hôte ou le jeu local décide du mot
        if self.is_host or self.is_local_game:
            if new_word:
                self.current_word = self.get_random_word() if specific_word is None else specific_word
            
            round_time = self.settings['time']
            if self.settings.get('game_type') == 'SURVIVAL':
                round_time = max(2.0, self.settings['time'] - (self.turn_count * 1.0)) # Réduction par mot dit
            elif self.settings.get('game_type') == 'SPEED':
                round_time = 3.0 # Temps fixe très court
            elif self.settings.get('game_type') == 'HARDCORE':
                round_time = 4.0 # Temps fixe court
            elif self.settings.get('game_type') == 'CHAOS':
                round_time = random.uniform(2.0, 8.0) # Temps aléatoire imprévisible

            if not self.is_local_game:
                self.send_data(f"NEW_ROUND|{self.current_word}|{round_time}|{self.settings['win_score']}|{self.round_num}")
            self.reset_round_state(round_time)

    def reset_round_state(self, time_val=None):
        self.user_text = ""
        self.opponent_text = ""
        self.start_ticks = pygame.time.get_ticks()
        if time_val is None: time_val = self.settings['time']
        self.round_duration = float(time_val)
        self.time_left = self.round_duration # Initialiser le temps pour éviter le timeout immédiat
        self.state = "GAME"
        self.freeze_until = 0
        self.update_game_buttons()
        self.rematch_ready = [False] * self.settings['players']
        self.particles = []
        self.judge_id = -1
        self.ready_status = [False] * self.settings['players'] # Reset ready correct pour N joueurs

    def update_game_buttons(self):
        self.buttons = [
            Button("QUITTER", 20, 20, 120, 40, ALERT_COLOR, (255, 100, 100), self.quit_game)
        ]
        if self.state == "GAME" and self.current_freezes > 0:
             self.buttons.append(Button(f"❄️ {self.current_freezes}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 100, 100, 60, (100, 200, 255), HOVER_COLOR, self.use_freeze, font=self.ui_emoji_font, text_color=(255, 255, 255)))

    def use_freeze(self):
        if self.current_freezes > 0 and pygame.time.get_ticks() > self.freeze_until:
            self.current_freezes -= 1
            self.send_action("FREEZE")
            self.update_game_buttons()

    def draw_text(self, text, font, color, x, y, center=True):
        if text is None: return # Sécurité anti-crash
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_text_glitch(self, text, font, color, x, y, center=True):
        # Effet Glitch (Décalage RGB aléatoire)
        off_r = (random.randint(-4, 4), random.randint(-4, 4))
        off_c = (random.randint(-4, 4), random.randint(-4, 4))
        self.draw_text(text, font, (255, 50, 50), x + off_r[0], y + off_r[1], center) # Rouge
        self.draw_text(text, font, (50, 255, 255), x + off_c[0], y + off_c[1], center) # Cyan
        self.draw_text(text, font, color, x, y, center) # Blanc

    def draw_text_shadow(self, text, font, color, x, y, center=True):
        # Ombre
        surface_s = font.render(text, True, (0, 0, 0))
        rect_s = surface_s.get_rect()
        if center: rect_s.center = (x+2, y+2)
        else: rect_s.topleft = (x+2, y+2)
        self.screen.blit(surface_s, rect_s)
        # Texte
        self.draw_text(text, font, color, x, y, center)

    def draw_text_with_emoji(self, text, base_font, emoji_font, color, x, y, center=True):
        # Gère l'affichage de texte contenant des emojis qui ne sont pas dans la police de base.
        if "❄️" in text:
            parts = text.split("❄️")
            surfaces = []
            
            # Render all parts, alternating between text and emoji
            surfaces.append(base_font.render(parts[0], True, color))
            for part in parts[1:]:
                surfaces.append(emoji_font.render("❄️", True, color))
                surfaces.append(base_font.render(part, True, color))

            # Calculate total width for centering
            total_width = sum(s.get_width() for s in surfaces)
            
            current_x = x
            if center:
                current_x = x - total_width // 2

            # Blit all surfaces, aligned vertically
            for surf in surfaces:
                rect = surf.get_rect(centery=y, left=current_x)
                self.screen.blit(surf, rect)
                current_x += surf.get_width()
        else:
            # If no emoji, use the standard function
            self.draw_text(text, base_font, color, x, y, center)

    def process_action(self, action):
        # Gestion des arguments dans l'action (ex: REMATCH|0)
        try:
            args = action.split("|")
            action_type = args[0]

            if action_type == "RESTART":
                if self.is_host or self.is_local_game: self.start_round()
            
            elif action_type == "POINT":
                # Récupérer la raison (TIMEOUT ou NORMAL)
                reason = args[1] if len(args) > 1 else "NORMAL"
                self.last_round_reason = reason
                self.used_words = [] # SUPPRIMER LES MOTS DE LA MANCHE D'AVANT (Reset pour la nouvelle manche)
                
                # Animation de tremblement (Shake) quand un point est marqué (donc perdu par qqn)
                self.shake_timer = 20
                self.play_sound("buzz")
                
                # Le joueur actuel a perdu le point
                # C'est l'autre joueur (ou le suivant) qui gagne le point
                winner_idx = (self.current_player + 1) % self.settings['players']
                
                # Sécurité Index
                if 0 <= winner_idx < len(self.score):
                    self.score[winner_idx] += 1
                self.round_num += 1
                self.turn_count = 0 # Reset du compteur de survie pour la nouvelle manche
                self.rally_combo = 0 # Reset du combo
                self.last_round_winner = winner_idx
                self.add_particles(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, ACCENT_COLOR)
                
                # Effet spécial Hardcore
                if self.settings.get('game_type') == 'HARDCORE':
                    self.generate_hardcore_win_particles()
                
                # Vérification victoire
                if 0 <= winner_idx < len(self.score) and self.score[winner_idx] >= self.settings['win_score']:
                    self.winner_text = f"Joueur {winner_idx + 1}" if self.is_local_game else (self.username if winner_idx == self.my_id else self.opponent_name)
                    
                    # Gain XP fin de partie
                    if self.is_local_game:
                        self.stats["wins"] += 1
                        self.coins += 50
                        # Historique Local
                        if "history" in self.stats: self.stats["history"].insert(0, {
                            "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
                            "opponent": "Local",
                            "score": f"{self.score[0]}-{self.score[1]}",
                            "winner": self.winner_text,
                            "result": "WIN"
                        })
                        self.prepare_xp_animation(50)
                    else:
                        if winner_idx == self.my_id:
                            self.stats["wins"] += 1
                            self.prepare_xp_animation(50)
                            self.coins += 50 # Victoire
                        else:
                            self.prepare_xp_animation(0)
                            # self.coins += 0 # Défaite (Rien)
                        
                        # Historique En Ligne
                        res_str = "VICTOIRE" if winner_idx == self.my_id else "DÉFAITE"
                        my_score = self.score[self.my_id] if self.my_id < len(self.score) else 0
                        opp_score = self.score[1 if self.my_id == 0 else 0] if len(self.score) > 1 else 0
                        if "history" in self.stats: self.stats["history"].insert(0, {
                            "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
                            "opponent": self.opponent_name,
                            "score": f"{my_score}-{opp_score}",
                            "winner": self.winner_text,
                            "result": res_str
                        })

                    if "history" in self.stats and len(self.stats["history"]) > 20: self.stats["history"].pop()
                    self.stats["games"] += 1
                    self.check_achievements()
                    self.save_settings()
                    self.set_state("GAME_OVER")
                else:
                    self.current_player = winner_idx
                    # Lancer le compte à rebours avant la prochaine manche
                    self.state = "ROUND_COUNTDOWN"
                    self.countdown_start = pygame.time.get_ticks()
                    
                    # Chance de lancer le mini-jeu bonus (20%)
                    if (self.is_host or self.is_local_game) and random.random() < 0.20:
                        self.send_action("BONUS_START")

                    # Réinitialiser les boutons pour éviter de cliquer pendant le compte à rebours
                    self.buttons = []
            
            elif action_type == "CONTINUE":
                self.reset_round_state(self.time_left) # Keep current time
            
            elif action_type == "NEXT_TURN":
                # Récupérer le mot tapé s'il y en a un (Mode écrit)
                next_word = args[1] if len(args) > 1 else None
                
                # Historique
                if next_word:
                    self.used_words.append(next_word.lower().strip())
                    self.save_history()
                
                # --- SYSTÈME DE COMBO ---
                elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                if elapsed < 2.5: # Réponse en moins de 2.5s
                    self.rally_combo += 1
                    if self.rally_combo > 1:
                        self.feedback_msg = f"COMBO x{self.rally_combo} !"
                        self.feedback_timer = pygame.time.get_ticks()
                        self.play_sound("coin")
                        
                        # Bonus pour le joueur actuel (si c'est moi)
                        if self.current_player == self.my_id:
                            bonus = self.rally_combo * 5
                            self.coins += bonus
                            self.show_notification(f"Combo x{self.rally_combo} (+{bonus}$)")
                    
                    # Mise à jour Stats & Succès
                    if self.rally_combo > self.stats.get("max_combo", 0):
                        self.stats["max_combo"] = self.rally_combo
                        self.save_settings()
                    if self.rally_combo >= 10:
                        self.unlock_achievement("SPEEDSTER")
                else:
                    self.rally_combo = 0
                
                self.current_player = (self.current_player + 1) % self.settings['players']
                self.turn_count += 1 # Incrémenter pour le mode Survie
                
                if self.is_host or self.is_local_game:
                    # En mode écrit, le nouveau mot est celui qui vient d'être validé
                    # En mode vocal, on garde le même mot affiché (ou on ne change rien) pour ne pas perturber la chaîne
                    should_change = (self.settings['mode'] == 'WRITTEN')
                    self.start_round(new_word=should_change, specific_word=next_word)
            
            elif action_type == "BUZZ":
                self.shake_timer = 20
                self.play_sound("buzz")
                # Animation Spéciale Wizz (Explosion)
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                for _ in range(80):
                    angle = random.uniform(0, 6.28)
                    speed = random.uniform(5, 30)
                    self.particles.append({
                        'x': cx, 'y': cy,
                        'vx': math.cos(angle) * speed,
                        'vy': math.sin(angle) * speed,
                        'life': random.randint(150, 255),
                        'color': (255, random.randint(200, 255), 0),
                        'size': random.randint(5, 15)
                    })
            
            elif action_type == "JUDGE":
                self.judge_id = int(args[1]) if len(args) > 1 else -1
                self.set_state("JUDGMENT")
            
            elif action_type == "REMATCH":
                if len(args) > 1:
                    player_id = int(args[1])
                    if 0 <= player_id < len(self.rematch_ready):
                        self.rematch_ready[player_id] = True
                
                # Si tout le monde est prêt
                if all(self.rematch_ready):
                    self.score = [0] * self.settings['players']
                    self.last_round_reason = ""
                    self.round_num = 1
                    self.turn_count = 0
                    self.rally_combo = 0
                    self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
                    self.reset_history()
                    self.ready_status = [False] * self.settings['players'] # Reset ready
                    if self.is_host or self.is_local_game:
                        self.start_round()
            
            elif action_type == "BONUS_START":
                self.state = "BONUS_GAME"
                self.bonus_end_time = pygame.time.get_ticks() + 5000 # 5 secondes
                self.bonus_targets = []
                self.spawn_bonus_target()
                self.play_sound("start")

            elif action_type == "TRADE_UPDATE":
                self.trade_lobby_data["them"]["coins"] = int(args[1])
                self.trade_lobby_data["them"]["items"] = args[2].split(',') if args[2] else []
                self.trade_lobby_data["them"]["locked"] = (args[3] == "1")
                
                # Check countdown
                if self.trade_lobby_data["me"]["locked"] and self.trade_lobby_data["them"]["locked"]:
                    if self.trade_lobby_data["countdown"] is None:
                        self.trade_lobby_data["countdown"] = pygame.time.get_ticks()
                else:
                    self.trade_lobby_data["countdown"] = None
            
            elif action_type == "TRADE_CONFIRM":
                # Echange validé
                self.coins -= self.trade_lobby_data["me"]["coins"]
                self.coins += self.trade_lobby_data["them"]["coins"]
                self.check_achievements()
                self.save_settings()
                self.show_notification("Echange réussi !")
                self.reset_network()
            
            elif action_type == "FREEZE":
                self.freeze_until = pygame.time.get_ticks() + 5000
                self.play_sound("start")
                self.show_notification("TEMPS GELÉ (5s) !")
        except Exception as e:
            print(f"Erreur action: {e}")

    def spawn_bonus_target(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        self.bonus_targets.append(pygame.Rect(x, y, 70, 70))

    def draw_achievement_popup(self):
        if not self.current_achievement and self.achievement_queue:
            self.current_achievement = {
                "data": self.achievement_queue.pop(0),
                "start_time": pygame.time.get_ticks(),
                "y": SCREEN_HEIGHT + 100
            }
        
        if self.current_achievement:
            ach = self.current_achievement
            now = pygame.time.get_ticks()
            elapsed = now - ach["start_time"]
            
            target_y = SCREEN_HEIGHT - 100
            
            if elapsed < 500:
                t = elapsed / 500
                ach["y"] = (SCREEN_HEIGHT + 100) - ((SCREEN_HEIGHT + 100) - target_y) * (1 - (1-t)**3)
            elif elapsed < 4500:
                ach["y"] = target_y
            elif elapsed < 5000:
                t = (elapsed - 4500) / 500
                ach["y"] = target_y + ((SCREEN_HEIGHT + 100) - target_y) * (t**3)
            else:
                self.current_achievement = None
                return

            rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, ach["y"], 400, 80)
            
            s = pygame.Surface((400, 80), pygame.SRCALPHA)
            pygame.draw.rect(s, (30, 35, 45, 240), (0, 0, 400, 80), border_radius=10)
            pygame.draw.rect(s, (50, 55, 65), (0, 0, 400, 80), 2, border_radius=10)
            
            # Icone Trophée
            pygame.draw.circle(s, (255, 215, 0), (50, 40), 25)
            pygame.draw.circle(s, (200, 150, 0), (50, 40), 20, 2)
            
            self.screen.blit(s, rect)
            self.draw_text("SUCCÈS DÉBLOQUÉ", self.small_bold_font, (255, 215, 0), rect.centerx + 20, rect.top + 20)
            self.draw_text(ach["data"]["name"], self.font, (255, 255, 255), rect.centerx + 20, rect.top + 50)

    def draw_avatar(self, avatar, x, y, size=30, border_id=None):
        # Cercle de fond
        pygame.draw.circle(self.screen, (40, 45, 60), (x, y), size)
        
        # Bordure équipée
        if border_id is None:
            border_id = self.equipped['border']
            
        border_col = ACCENT_COLOR
        if border_id == "border_rainbow":
             hue = (pygame.time.get_ticks() // 5) % 360
             c = pygame.Color(0)
             c.hsla = (hue, 100, 50, 100)
             border_col = (c.r, c.g, c.b)
        elif border_id == "border_double":
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size + 4, 1)
            border_col = (200, 200, 200)
        elif border_id in SHOP_CATALOG:
            border_col = SHOP_CATALOG[border_id]['color']
        
        pygame.draw.circle(self.screen, border_col, (x, y), size, 3)
        
        # Gestion Avatar (Image ou Emoji)
        if avatar.startswith("IMG:"):
            # Clé de cache incluant la taille pour gérer les différents affichages
            cache_key = (avatar, size)
            
            # Gestion du cache pour éviter de décoder à chaque frame
            if cache_key not in self.avatar_cache:
                try:
                    img_data = base64.b64decode(avatar[4:])
                    original = pygame.image.load(io.BytesIO(img_data)).convert_alpha()
                    
                    # Création du masque circulaire pour ne pas déborder
                    diameter = size * 2
                    # On redimensionne l'image pour qu'elle couvre le cercle
                    scaled = pygame.transform.smoothscale(original, (diameter, diameter))
                    
                    # Masque : On crée une surface transparente avec un cercle blanc, et on applique BLEND_RGBA_MIN
                    mask = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                    pygame.draw.circle(mask, (255, 255, 255), (size, size), size - 3)
                    scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                    
                    self.avatar_cache[cache_key] = scaled
                except:
                    self.avatar_cache[cache_key] = None
            
            surf = self.avatar_cache.get(cache_key)
            if surf:
                rect = surf.get_rect(center=(x, y))
                self.screen.blit(surf, rect)
            else:
                # Fallback si erreur
                font = self.emoji_font if size > 40 else self.ui_emoji_font
                txt = font.render("?", True, (255, 255, 255))
                rect = txt.get_rect(center=(x, y))
                self.screen.blit(txt, rect)
        else:
            # Emoji Classique
            font = self.emoji_font if size > 40 else self.ui_emoji_font
            try:
                txt = font.render(avatar, True, (255, 255, 255))
            except:
                txt = self.big_font.render(avatar, True, (255, 255, 255))
            rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, rect)

    def draw_background(self):
        # Thème équipé
        bg_col = BG_COLOR
        if self.equipped['theme'] in SHOP_CATALOG:
            bg_col = SHOP_CATALOG[self.equipped['theme']]['color']
            
        self.screen.fill(bg_col)
        # Grille mouvante (Effet moderne)
        grid_color = (25, 30, 40)
        offset = (pygame.time.get_ticks() // 50) % 50
        
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
            
        for y in range(-50, SCREEN_HEIGHT, 50):
            draw_y = y + offset
            pygame.draw.line(self.screen, grid_color, (0, draw_y), (SCREEN_WIDTH, draw_y))
            
        # Particules Menu
        if self.state.startswith("MENU") or self.state == "INPUT_NAME":
            self.update_draw_menu_particles()
        
        # Vignette v0.2 (Assombrir les coins)
        self.screen.blit(self.vignette_surf, (0, 0))

    def draw_panel(self, x, y, w, h):
        # Panneau semi-transparent (Glassmorphism)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*PANEL_COLOR, 240)) # Couleur sombre avec transparence
        self.screen.blit(s, (x, y))
        
        # Bordure fine
        pygame.draw.rect(self.screen, (60, 70, 90), (x, y, w, h), 2, border_radius=15)
        # Ombre portée simple (décalage)
        # pygame.draw.rect(self.screen, (0,0,0), (x+5, y+5, w, h), border_radius=15) # Trop lourd à gérer l'ordre

    def run(self):
        running = True
        while running:
            self.draw_background()
            self.update_draw_particles()
            
            # Gestion des événements globaux
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                if event.type == pygame.MOUSEWHEEL:
                    if self.state == "LOBBY":
                        self.chat_scroll += event.y
                        if self.chat_scroll < 0: self.chat_scroll = 0
                    elif self.state == "INPUT_NAME":
                        self.avatar_scroll -= event.y * 20 # Vitesse de scroll
                        if self.avatar_scroll < 0: self.avatar_scroll = 0
                        # Limite de scroll (8 lignes * 55px - 160px visible)
                        max_scroll = (math.ceil(len(AVATARS)/10) * 55) - 160
                        if self.avatar_scroll > max_scroll: self.avatar_scroll = max_scroll
                        self.create_menu_buttons() # Recalculer positions
                    elif self.state in ["MENU_SHOP", "MENU_INVENTORY"]:
                        # Refonte du défilement magasin
                        self.shop_scroll -= event.y * 40
                        if self.shop_scroll < 0: self.shop_scroll = 0
                        
                        # Calcul Max Scroll dynamique
                        card_h = 300
                        gap = 30
                        cols = 5
                        if self.state == "MENU_SHOP":
                            all_items = list(SHOP_CATALOG.keys())
                            if self.shop_tab == "BORDER": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'border']
                            elif self.shop_tab == "THEME": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'theme']
                            elif self.shop_tab == "CATEGORY": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'category']
                            count = len(all_items)
                        else:
                            count = len([i for i in self.inventory if i in SHOP_CATALOG])
                        
                        rows = math.ceil(count / cols)
                        total_h = rows * (card_h + gap)
                        visible_h = SCREEN_HEIGHT - 220
                        max_scroll = max(0, total_h - visible_h + 100)
                        
                        if self.shop_scroll > max_scroll: self.shop_scroll = max_scroll
                        self.create_menu_buttons() # Recalculer positions
                    elif self.state == "MENU_ACHIEVEMENTS":
                        self.achievements_scroll -= event.y * 30
                        if self.achievements_scroll < 0: self.achievements_scroll = 0
                        max_scroll = max(0, len(ACHIEVEMENTS) * 90 - 650)
                        if self.achievements_scroll > max_scroll: self.achievements_scroll = max_scroll

                # --- MODE TEST (Touche T x3) ---
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    now = pygame.time.get_ticks()
                    if now - self.last_t_press < 1000: # Délai augmenté pour faciliter l'activation
                        self.t_press_count += 1
                    else:
                        self.t_press_count = 1
                    self.last_t_press = now
                    
                    if self.t_press_count >= 3:
                        self.test_mode = not self.test_mode
                        self.t_press_count = 0

                # --- ACTIONS DEV MODE ---
                if self.test_mode and event.type == pygame.KEYDOWN:
                    # Cheat Code "coins"
                    if event.unicode:
                        self.cheat_buffer += event.unicode.lower()
                        if self.cheat_buffer.endswith("coins"):
                            self.coins += 10000
                            self.save_settings()
                            self.show_notification("DEV: +10000 Pièces !")
                            self.play_sound("coin")
                            self.cheat_buffer = ""
                        if len(self.cheat_buffer) > 10: self.cheat_buffer = self.cheat_buffer[-10:]

                    if event.key == pygame.K_x:
                        self.gain_xp(500)
                        self.show_notification("DEV: +500 XP")
                    elif event.key == pygame.K_u:
                        for ach in ACHIEVEMENTS:
                            if ach not in self.achievements_unlocked:
                                self.unlock_achievement(ach)
                        self.show_notification("DEV: Succès débloqués")
                    elif event.key == pygame.K_i:
                        for item in SHOP_CATALOG:
                            if item not in self.inventory:
                                self.inventory.append(item)
                        self.save_settings()
                        self.show_notification("DEV: Boutique débloquée")
                    elif event.key == pygame.K_w and self.state == "GAME":
                        # Victoire instantanée
                        self.score[self.my_id] = self.settings['win_score'] - 1
                        # On fait perdre l'adversaire pour gagner le point final
                        self.current_player = 1 if self.my_id == 0 else 0
                        self.process_action("POINT")

                    if event.unicode == ':' or event.key == pygame.K_COLON:
                        # Faire perdre le bot (donc JE gagne le point)
                        # Pour gagner le point, c'est comme si le joueur précédent (Bot) avait échoué
                        self.current_player = 1 if self.my_id == 0 else 0 # On force le tour du bot
                        self.process_action("POINT")
                    
                    elif event.unicode == '/' or event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                        # Faire gagner le bot (donc JE perds le point)
                        # C'est comme si J'avais échoué
                        self.current_player = self.my_id # On force mon tour
                        self.process_action("POINT")

                # Saisie du pseudo
                if self.state == "INPUT_NAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                        elif event.key == pygame.K_RETURN: self.validate_name()
                        elif len(self.username) < 15: self.username += event.unicode

                # Gestion Popup
                if self.popup:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if self.popup.get("rect_yes") and self.popup["rect_yes"].collidepoint(mx, my): self.popup["yes"]()
                        elif self.popup.get("rect_no") and self.popup["rect_no"].collidepoint(mx, my): self.popup["no"]()
                    continue # Bloque les autres interactions

                # --- MINI-JEU BONUS ---
                if self.state == "BONUS_GAME":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        for t in self.bonus_targets[:]:
                            if t.collidepoint(mx, my):
                                self.bonus_targets.remove(t)
                                self.coins += 5
                                self.spawn_bonus_target()
                                self.play_sound("coin")
                                self.add_particles(mx, my, (255, 215, 0))

                # Gestion des boutons
                if self.state == "CROP_AVATAR":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: self.validate_crop()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: self.crop_dragging = True; self.crop_last_mouse = event.pos
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1: self.crop_dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        if self.crop_dragging:
                            dx = event.pos[0] - self.crop_last_mouse[0]
                            dy = event.pos[1] - self.crop_last_mouse[1]
                            self.crop_offset[0] += dx
                            self.crop_offset[1] += dy
                            self.crop_last_mouse = event.pos
                    elif event.type == pygame.MOUSEWHEEL:
                        self.crop_scale += event.y * 0.05
                        if self.crop_scale < 0.1: self.crop_scale = 0.1

                if self.transition_state is None:
                    action_taken = False
                    for btn in self.buttons:
                        if btn.check_click(event):
                            self.play_sound("click")
                            action_taken = True
                            break
                    
                    if not action_taken:
                        for btn in self.avatar_grid_buttons:
                            # Vérification de visibilité pour les avatars (Scroll)
                            if self.state == "INPUT_NAME":
                                cy = SCREEN_HEIGHT // 2
                                # Zone visible : cy - 150 à cy + 10
                                if btn.rect.top > cy + 10 or btn.rect.bottom < cy - 150:
                                    continue
                            if btn.check_click(event):
                                self.play_sound("click")
                                break
                
                # --- LOGIQUE DU MENU ---
                if self.state == "MENU_JOIN":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_ip = self.input_ip[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.connect_to_host()
                        else:
                            self.input_ip += event.unicode

                elif self.state == "MENU_ADD_FRIEND":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if pygame.Rect(SCREEN_WIDTH//2 - 200, 310, 400, 50).collidepoint(mx, my):
                            self.active_input = "name"
                        elif pygame.Rect(SCREEN_WIDTH//2 - 200, 420, 400, 50).collidepoint(mx, my):
                            self.active_input = "ip"
                        elif pygame.Rect(SCREEN_WIDTH//2 - 250, 310, 500, 50).collidepoint(mx, my): self.active_input = "name"
                        elif pygame.Rect(SCREEN_WIDTH//2 - 250, 420, 500, 50).collidepoint(mx, my): self.active_input = "ip"
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            self.active_input = "ip" if self.active_input == "name" else "name"
                        elif event.key == pygame.K_RETURN:
                            self.request_friend()
                        elif event.key == pygame.K_BACKSPACE:
                            if self.active_input == "name": self.friend_name_input = self.friend_name_input[:-1]
                            else: self.friend_ip_input = self.friend_ip_input[:-1]
                        else:
                            if self.active_input == "name" and len(self.friend_name_input) < 15:
                                self.friend_name_input += event.unicode
                            elif self.active_input == "ip" and len(self.friend_ip_input) < 20:
                                self.friend_ip_input += event.unicode

                elif self.state == "MENU_FRIENDS":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            # Lancer échange avec l'ami survolé
                            if 0 <= self.hovered_friend_idx < len(self.friends):
                                self.request_trade(self.friends[self.hovered_friend_idx]['ip'])
                
                elif self.state == "EDIT_CAT_NAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.cat_name_input = self.cat_name_input[:-1]
                        elif event.key == pygame.K_RETURN and self.cat_name_input: self.set_state("EDIT_CAT_WORDS")
                        elif len(self.cat_name_input) < 20: self.cat_name_input += event.unicode.upper()

                elif self.state == "EDIT_CAT_WORDS":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.cat_words_input = self.cat_words_input[:-1]
                        elif event.key == pygame.K_RETURN: self.save_custom_category()
                        else: self.cat_words_input += event.unicode

                # --- LOGIQUE LOBBY ---
                elif self.state == "LOBBY":
                    # Gestion Chat
                    if event.type == pygame.KEYDOWN:
                        # Cheat code: 'P' pour forcer le J2 (Bot) prêt en mode Dev
                        if self.test_mode and self.is_host and event.key == pygame.K_p:
                            self.ready_status[1] = not self.ready_status[1]
                            self.check_start_game()

                        if event.key == pygame.K_BACKSPACE:
                            self.chat_input = self.chat_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.send_chat()
                        elif event.key == pygame.K_b and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            self.send_action("BUZZ")
                        else:
                            if len(self.chat_input) < 50:
                                self.chat_input += event.unicode

                    # Bouton PRET géré par self.buttons

                # --- LOGIQUE DU JEU ---
                elif self.state == "GAME":
                    # Mode ÉCRIT
                    if self.settings['mode'] == 'WRITTEN':
                        if self.is_local_game or self.current_player == self.my_id:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN and len(self.user_text.strip()) > 0:
                                    if self.user_text.lower().strip() in self.used_words:
                                        self.start_ticks -= 3000 # Pénalité de 3 secondes
                                        self.feedback_msg = "DÉJÀ DIT ! (-3s)"
                                        self.feedback_timer = pygame.time.get_ticks()
                                        self.play_sound("buzz")
                                        self.shake_timer = 10
                                    else:
                                        action_str = f"NEXT_TURN|{self.user_text}"
                                        if not self.is_local_game:
                                            self.send_data(f"ACTION|{action_str}")
                                        self.process_action(action_str)
                                elif event.key == pygame.K_BACKSPACE:
                                    self.user_text = self.user_text[:-1]
                                elif event.key == self.keys["CONTEST"]:
                                    self.send_action(f"JUDGE|{self.my_id}")
                                elif event.key == pygame.K_F3:
                                    self.user_text = f"Test_{random.randint(100, 999)}"
                                elif event.key == pygame.K_b and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                                    self.send_action("BUZZ")
                                else:
                                    if len(self.user_text) < 20 and event.key != self.keys["CONTEST"]:
                                        self.user_text += event.unicode
                                        self.play_sound("click") # Son de frappe
                                        if not self.is_local_game:
                                            self.send_data(f"TYPE|{self.user_text}")
                        
                        if not self.is_local_game and self.current_player != self.my_id:
                            if event.type == pygame.KEYDOWN and event.key == self.keys["CONTEST"]:
                                self.send_action(f"JUDGE|{self.my_id}")

                    # Mode VOCAL
                    elif self.settings['mode'] == 'VOCAL':
                        if self.is_local_game or self.current_player == self.my_id:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.send_action("NEXT_TURN")
                                elif event.key == self.keys["CONTEST"] or event.key == pygame.K_a:
                                    self.send_action(f"JUDGE|{self.my_id}")
                        
                        if not self.is_local_game and self.current_player != self.my_id:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                                self.send_action(f"JUDGE|{self.my_id}")

            # --- LOGIQUE CONTINUE (Hors événements) ---
            if self.state == "GAME":
                # Gestion Gel du Temps
                if pygame.time.get_ticks() < self.freeze_until:
                    # On décale le start_ticks pour que le temps écoulé n'augmente pas
                    self.start_ticks += self.clock.get_time()

                # Timer & Timeout
                elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                
                # Effet Flammes Combo
                if self.rally_combo > 5:
                    self.generate_flame_particles()
                
                self.time_left = self.round_duration - elapsed
                
                if (self.is_host or self.is_local_game) and self.time_left <= 0:
                    self.send_action("POINT|TIMEOUT")
            
            elif self.state == "ROUND_COUNTDOWN":
                if pygame.time.get_ticks() - self.countdown_start > 3000: # 3 secondes
                    self.start_round()
            
            elif self.state == "BONUS_GAME":
                if pygame.time.get_ticks() > self.bonus_end_time:
                    self.state = "ROUND_COUNTDOWN"
                    self.countdown_start = pygame.time.get_ticks()
            
            elif self.state == "TRADE_LOBBY":
                if self.trade_lobby_data["countdown"]:
                    if pygame.time.get_ticks() - self.trade_lobby_data["countdown"] > 5000:
                        # Fin du timer
                        self.send_action("TRADE_CONFIRM")
                        self.process_action("TRADE_CONFIRM")
                        self.trade_lobby_data["countdown"] = None

            # --- LOGIQUE BOT (TEST MODE) ---
            if self.test_mode and self.state == "GAME" and self.current_player != self.my_id:
                if self.bot_timer == 0:
                    self.bot_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.bot_timer > 2000: # 2 secondes de délai
                    # Le bot envoie a, b, c... pour tester
                    msg = chr(97 + (self.bot_msg_index % 26))
                    self.bot_msg_index += 1
                    self.process_action(f"NEXT_TURN|{msg}")
                    self.bot_timer = 0
            else:
                self.bot_timer = 0

            # --- GESTION RÉSEAU ---
            process_count = 0
            while self.network_queue and process_count < 50: # Limite de traitement par frame (Anti-Freeze)
                msg = self.network_queue.pop(0)
                process_count += 1
                parts = msg.split("|")
                cmd = parts[0]
                
                if cmd == "START":
                    self.settings['mode'] = parts[1]
                    self.settings['time'] = int(parts[2])
                    self.settings['win_score'] = int(parts[3])
                    if len(parts) > 4: self.settings['category'] = parts[4]
                    if len(parts) > 5: self.settings['game_type'] = parts[5]
                    self.round_num = 1
                    self.turn_count = 0
                    self.rally_combo = 0
                    self.reset_history()
                    self.send_name() # Envoyer mon nom en réponse
                    # Le client attend le mot
                elif cmd == "FROM":
                    # Traitement des messages venant des clients (Host)
                    # On retire le wrapper FROM|id| et on traite le message original
                    real_msg = "|".join(parts[2:])
                    self.network_queue.insert(0, real_msg)
                elif cmd == "NEW_ROUND":
                    self.current_word = parts[1]
                    self.reset_round_state(float(parts[2]))
                elif cmd == "ACTION":
                    self.process_action("|".join(parts[1:]))
                elif cmd == "TYPE":
                    self.opponent_text = parts[1]
                elif cmd == "NAME":
                    self.opponent_name = parts[1]
                    if len(parts) > 2: self.opponent_avatar = parts[2]
                    if len(parts) > 3: self.opponent_border = parts[3]
                    if len(parts) > 4: self.opponent_level = int(parts[4])
                    if len(parts) > 5: self.opponent_name_color = parts[5]
                    self.show_notification(f"{self.opponent_name} connecté !")
                elif cmd == "READY":
                    try:
                        pid = int(parts[1])
                        is_r = (parts[2] == "1")
                        if pid != self.my_id: # Sécurité : ne pas modifier mon propre statut via réseau
                            self.ready_status[pid] = is_r
                            self.check_start_game()
                            # Si je suis l'hôte, je relaie l'info aux autres clients
                            if self.is_host:
                                self.broadcast_player_list() # Sync parfaite au lieu de simple relais
                        if pid in self.lobby_cache:
                            self.lobby_cache[pid]["ready"] = is_r
                    except: pass
                elif cmd == "PLAYERS":
                    try:
                        self.lobby_cache = {}
                        raw_list = parts[1].split(';')
                        for p_str in raw_list:
                            p = p_str.split(',')
                            if len(p) >= 5:
                                pid = int(p[0])
                                self.lobby_cache[pid] = {"name": p[1], "avatar": p[2], "border": p[3], "ready": (p[4] == "1"), "name_color": p[5] if len(p) > 5 else "name_color_default", "ip": p[6] if len(p) > 6 else ""}
                                if pid >= len(self.ready_status):
                                    self.ready_status.extend([False] * (pid - len(self.ready_status) + 1))
                                self.ready_status[pid] = (p[4] == "1")
                    except: pass
                elif cmd == "CHAT":
                    self.chat_messages.append("|".join(parts[1:]))
                    self.play_sound("chat")
                elif cmd == "REFRESH_LOBBY":
                    self.create_menu_buttons()
                elif cmd == "TRADE_GIVE":
                    self.show_notification(f"Reçu {parts[1]} pièces !")
                    self.process_action(f"TRADE_GIVE|{parts[1]}")

            if not running:
                break

            # --- AFFICHAGE ---
            # Gestion du tremblement (BUZZ)
            real_screen = self.screen
            using_temp_screen = False
            if self.shake_timer > 0:
                self.shake_timer -= 1
                shake_x = random.randint(-8, 8)
                shake_y = random.randint(-8, 8)
                self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                using_temp_screen = True
            
            if self.state == "TUTORIAL":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 600)
                self.draw_text_shadow("BIENVENUE DANS WORLD RUSH !", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 160)
                
                lines = [
                    f"Bienvenue sur World Rush v{CURRENT_VERSION} !",
                    "• PRINCIPE : Trouvez le lien entre les mots avant le temps imparti.",
                    "• 5 MODES : Normal, Survie, Speed, Hardcore, Chaos.",
                    "• NOUVEAU : Gel du Temps (❄️) et Packs de Mots !",
                    "• BOUTIQUE : Achetez des bordures, thèmes et catégories.",
                    "• MULTIJOUEUR : Échangez des items, ajoutez des amis, chattez.",
                    "• PROGRESSION : Niveaux, XP et Succès à débloquer.",
                    "Bonne chance !"
                ]
                for i, line in enumerate(lines):
                    self.draw_text_with_emoji(line, self.font, self.ui_emoji_font, TEXT_COLOR, SCREEN_WIDTH//2, 260 + i*50)

            elif self.state == "INPUT_NAME":
                # Redesign complet du profil
                cy = SCREEN_HEIGHT // 2
                self.draw_panel(SCREEN_WIDTH//2 - 450, cy - 400, 900, 800) # Agrandissement du panneau
                self.draw_text_shadow("MON PROFIL", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, cy - 350)
                
                # Avatar
                self.draw_avatar(self.avatar, SCREEN_WIDTH//2, cy - 260, 70)
                
                # Zone de défilement Avatars
                self.draw_text("Choisissez votre Avatar :", self.font, (150, 150, 150), SCREEN_WIDTH//2, cy - 175)
                
                # Cadre autour des emojis
                grid_rect = pygame.Rect(SCREEN_WIDTH//2 - 390, cy - 155, 780, 170)
                pygame.draw.rect(self.screen, (30, 35, 45), grid_rect, border_radius=10)
                
                # Clipping pour le scroll
                clip_rect = pygame.Rect(SCREEN_WIDTH//2 - 380, cy - 150, 760, 160) # Hauteur réduite pour 3 lignes
                self.screen.set_clip(clip_rect)
                for btn in self.avatar_grid_buttons:
                    btn.draw(self.screen)
                self.screen.set_clip(None)
                
                # Input Pseudo
                self.draw_text("Votre Pseudo :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, cy + 60)
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 300, cy + 90, 600, 60), border_radius=10)
                pygame.draw.rect(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2 - 300, cy + 90, 600, 60), 2, border_radius=10)
                self.draw_text(self.username, self.font, self.get_name_color(self.equipped['name_color']), SCREEN_WIDTH//2, cy + 120)

            elif self.state == "MENU_HISTORY":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 50, 800, 850)
                self.draw_text_shadow("HISTORIQUE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                start_y = 180
                cx = SCREEN_WIDTH // 2
                
                if not self.stats["history"]:
                    self.draw_text("Aucune partie jouée.", self.font, (150, 150, 150), cx, 300)
                
                for i, game in enumerate(self.stats["history"]):
                    if i > 8: break # Max 9 items visible
                    y = start_y + i * 80
                    
                    col = (50, 200, 50) if game["result"] == "VICTOIRE" or game["result"] == "WIN" else ((200, 50, 50) if game["result"] == "DÉFAITE" else TEXT_COLOR)
                    
                    pygame.draw.rect(self.screen, (30, 35, 45), (cx - 350, y, 700, 70), border_radius=10)
                    self.draw_text(f"{game['date']}", self.small_bold_font, (150, 150, 150), cx - 280, y + 35)
                    self.draw_text(f"vs {game['opponent']}", self.font, TEXT_COLOR, cx, y + 35)
                    self.draw_text(f"{game['score']}", self.big_font, col, cx + 280, y + 35)

            elif self.state == "CROP_AVATAR":
                self.draw_text_shadow("AJUSTER L'IMAGE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 50)
                self.draw_text("Zoom: Molette | Déplacer: Clic gauche", self.font, (150, 150, 150), SCREEN_WIDTH//2, 100)
                
                if self.crop_image:
                    img_w = int(self.crop_image.get_width() * self.crop_scale)
                    img_h = int(self.crop_image.get_height() * self.crop_scale)
                    scaled = pygame.transform.smoothscale(self.crop_image, (img_w, img_h))
                    rect = scaled.get_rect(center=(self.crop_offset[0], self.crop_offset[1]))
                    self.screen.blit(scaled, rect)
                
                # Masque sombre
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                pygame.draw.circle(overlay, (0, 0, 0, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 150)
                self.screen.blit(overlay, (0, 0))
                
                # Cercle guide
                pygame.draw.circle(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 150, 3)

            elif self.state == "MENU_JOIN":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 150, 1000, 650) # Agrandissement fenêtre rejoindre
                self.draw_text_shadow("REJOINDRE UNE PARTIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 220)
                self.draw_text("Entrez l'IP de l'hôte :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 320)
                
                # Input Box Moderne
                input_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, 380, 600, 80)
                pygame.draw.rect(self.screen, (20, 25, 30), input_rect, border_radius=15)
                pygame.draw.rect(self.screen, ACCENT_COLOR, input_rect, 2, border_radius=15)
                # Lueur interne
                pygame.draw.rect(self.screen, (0, 240, 200, 20), input_rect.inflate(-4, -4), border_radius=12)
                
                # Curseur clignotant
                cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
                self.draw_text(self.input_ip + cursor, self.big_font, TEXT_COLOR, SCREEN_WIDTH//2, 420)
                
                if self.connect_status:
                    col = ACCENT_COLOR if "Connecté" in self.connect_status else ALERT_COLOR
                    self.draw_text(self.connect_status, self.font, col, SCREEN_WIDTH//2, 500)
                
                self.draw_text("Demandez l'IP Internet à l'hôte (ou utilisez Radmin/Hamachi)", self.font, (100, 100, 100), SCREEN_WIDTH//2, 720)

            elif self.state == "MENU_FRIENDS":
                self.draw_panel(SCREEN_WIDTH//2 - 700, 50, 1400, 850) # Cadre agrandi encore plus
                self.draw_text_shadow("MES AMIS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                # Affichage IP Publique
                ip_txt = f"Mon IP: {self.public_ip}" if self.public_ip else "Mon IP: Recherche..."
                self.draw_text(ip_txt, self.font, (150, 150, 150), SCREEN_WIDTH//2 - 50, 180)
                if self.connect_status == "IP Copiée !":
                    self.draw_text("Copié !", self.font, ACCENT_COLOR, SCREEN_WIDTH//2 + 280, 180)
                
                start_y = 220
                cx = SCREEN_WIDTH // 2
                self.hovered_friend_idx = -1
                mx, my = pygame.mouse.get_pos()
                
                for i, friend in enumerate(self.friends):
                    # Fond de la ligne
                    row_rect = pygame.Rect(cx - 500, start_y + i*70, 1000, 50)
                    col = (50, 60, 70) if row_rect.collidepoint(mx, my) else (35, 40, 50)
                    pygame.draw.rect(self.screen, col, row_rect, border_radius=10)
                    if row_rect.collidepoint(mx, my): self.hovered_friend_idx = i
                    # Infos
                    self.draw_text(f"{friend['name']}", self.font, TEXT_COLOR, cx - 350, start_y + i*70 + 25, center=True)
                    self.draw_text(f"{friend['ip']}", self.font, (120, 120, 120), cx, start_y + i*70 + 25, center=True)

            elif self.state == "MENU_ADD_FRIEND":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 150, 600, 550)
                self.draw_text_shadow("AJOUTER UN AMI", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 200)
                
                # Name Input
                col_name = ACCENT_COLOR if self.active_input == "name" else (100, 100, 100)
                self.draw_text("Nom de l'ami :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 280)
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 200, 310, 400, 50), border_radius=10)
                pygame.draw.rect(self.screen, col_name, (SCREEN_WIDTH//2 - 200, 310, 400, 50), 2, border_radius=10)
                self.draw_text(self.friend_name_input, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 335)
                
                # IP Input
                col_ip = ACCENT_COLOR if self.active_input == "ip" else (100, 100, 100)
                self.draw_text("Adresse IP :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 390)
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 200, 420, 400, 50), border_radius=10)
                pygame.draw.rect(self.screen, col_ip, (SCREEN_WIDTH//2 - 200, 420, 400, 50), 2, border_radius=10)
                self.draw_text(self.friend_ip_input, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 445)

            elif self.state == "MENU_ACHIEVEMENTS":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 50, 800, 850)
                self.draw_text_shadow("SUCCÈS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                # Pourcentage de progression
                total_ach = len(ACHIEVEMENTS)
                unlocked_count = len(self.achievements_unlocked)
                pct = int((unlocked_count / total_ach) * 100) if total_ach > 0 else 0
                self.draw_text(f"{unlocked_count}/{total_ach} ({pct}%)", self.medium_font, (200, 200, 200), SCREEN_WIDTH - 250, 100)

                # Zone de clipping pour le défilement
                clip_rect = pygame.Rect(SCREEN_WIDTH//2 - 400, 140, 800, 750)
                self.screen.set_clip(clip_rect)
                
                start_y = 150 - self.achievements_scroll # Remonté (était 180)
                cx = SCREEN_WIDTH // 2
                
                for i, (aid, data) in enumerate(ACHIEVEMENTS.items()):
                    y = start_y + i * 90
                    unlocked = aid in self.achievements_unlocked
                    
                    # Fond
                    bg_col = (40, 50, 40) if unlocked else (30, 30, 35)
                    border_col = ACCENT_COLOR if unlocked else (60, 60, 70)
                    pygame.draw.rect(self.screen, bg_col, (cx - 350, y, 700, 80), border_radius=10)
                    pygame.draw.rect(self.screen, border_col, (cx - 350, y, 700, 80), 2, border_radius=10)
                    
                    # Icone / Checkbox
                    icon_col = (50, 200, 50) if unlocked else (100, 100, 100)
                    pygame.draw.circle(self.screen, icon_col, (cx - 300, y + 40), 20)
                    if unlocked:
                        self.draw_text("V", self.small_bold_font, (0,0,0), cx - 300, y + 40)
                    
                    # Textes
                    name_col = (255, 255, 255) if unlocked else (150, 150, 150)
                    self.draw_text(data["name"], self.small_bold_font, name_col, cx - 250, y + 20, center=False)
                    self.draw_text(data["desc"], self.font, (180, 180, 180), cx - 250, y + 50, center=False)
                    
                    # Récompense
                    self.draw_text(f"+{data['reward']}$", self.small_bold_font, (255, 215, 0), cx + 250, y + 40)
                
                self.screen.set_clip(None)

            elif self.state == "MENU_CUSTOM_CATS":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 100, 600, 600)
                self.draw_text_shadow("CATÉGORIES PERSO", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                start_y = 200
                for i, cat in enumerate(self.custom_categories.keys()):
                    self.draw_text(cat, self.font, TEXT_COLOR, SCREEN_WIDTH//2 - 50, start_y + i*60 + 25)

            elif self.state == "EDIT_CAT_NAME":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 200, 600, 500)
                self.draw_text_shadow("NOM DE LA CATÉGORIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 250)
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 200, 350, 400, 60), border_radius=10)
                pygame.draw.rect(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2 - 200, 350, 400, 60), 2, border_radius=10)
                self.draw_text(self.cat_name_input, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 380)

            elif self.state == "EDIT_CAT_WORDS":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 700)
                self.draw_text_shadow("AJOUTER DES MOTS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                self.draw_text("Séparez les mots par des virgules (,)", self.font, (150, 150, 150), SCREEN_WIDTH//2, 220)
                
                # Zone de texte large
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 350, 250, 700, 300), border_radius=10)
                pygame.draw.rect(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2 - 350, 250, 700, 300), 2, border_radius=10)
                
                # Affichage multiline basique
                words_text = self.cat_words_input
                # Simple wrap visuel (très basique)
                if len(words_text) > 50: words_text = "..." + words_text[-50:]
                self.draw_text(words_text, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 400)

            elif self.state == "TRADE_LOBBY":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 100, 1000, 700)
                self.draw_text_shadow("ECHANGE", self.big_font, (255, 200, 0), SCREEN_WIDTH//2, 150)
                
                # Colonne Moi
                self.draw_text("MOI", self.medium_font, ACCENT_COLOR, SCREEN_WIDTH//2 - 200, 220)
                self.draw_coin_ui(SCREEN_WIDTH//2 - 200, 280, self.trade_lobby_data["me"]["coins"])
                if self.trade_lobby_data["me"]["locked"]:
                    self.draw_text("VERROUILLÉ", self.font, (100, 255, 100), SCREEN_WIDTH//2 - 200, 350)
                
                # Colonne Eux
                self.draw_text(self.opponent_name, self.medium_font, ALERT_COLOR, SCREEN_WIDTH//2 + 200, 220)
                self.draw_coin_ui(SCREEN_WIDTH//2 + 200, 280, self.trade_lobby_data["them"]["coins"])
                if self.trade_lobby_data["them"]["locked"]:
                    self.draw_text("VERROUILLÉ", self.font, (100, 255, 100), SCREEN_WIDTH//2 + 200, 350)
                
                # Timer
                if self.trade_lobby_data["countdown"]:
                    rem = 5 - (pygame.time.get_ticks() - self.trade_lobby_data["countdown"]) / 1000
                    self.draw_text_shadow(f"CONFIRMATION: {int(rem)+1}", self.big_font, (255, 255, 255), SCREEN_WIDTH//2, 450)

            elif self.state == "MENU_SHOP":
                self.draw_text_shadow("MAGASIN", self.big_font, (255, 200, 0), SCREEN_WIDTH//2, 80)
                self.draw_coin_ui(SCREEN_WIDTH - 150, 80, self.coins)
                
                # Grid Config
                cx = SCREEN_WIDTH // 2
                card_w, card_h = 260, 300
                cols = 5
                gap = 30
                start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
                start_y = 220 - self.shop_scroll
                
                all_items = list(SHOP_CATALOG.keys())
                all_items.sort(key=lambda x: (SHOP_CATALOG[x]['type'], SHOP_CATALOG[x]['price']))
                
                # Filtrage
                filtered_items = []
                for item_id in all_items:
                    item = SHOP_CATALOG[item_id]
                    if self.shop_tab == "ALL": filtered_items.append(item_id)
                    elif self.shop_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                    elif self.shop_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                    elif self.shop_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                    elif self.shop_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)

                for i, item_id in enumerate(filtered_items):
                    item = SHOP_CATALOG[item_id]
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap)
                    y = start_y + row * (card_h + gap)
                    
                    # Clipping
                    if y + card_h < 100 or y > SCREEN_HEIGHT: continue
                    
                    # Card BG
                    rect = pygame.Rect(x, y, card_w, card_h)
                    pygame.draw.rect(self.screen, (35, 40, 50), rect, border_radius=15)
                    
                    # Border (Color based on item color)
                    border_col = item['color']
                    if "rainbow" in item_id:
                         hue = (pygame.time.get_ticks() // 5) % 360
                         c = pygame.Color(0)
                         c.hsla = (hue, 100, 50, 100)
                         border_col = (c.r, c.g, c.b)
                    pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=15)
                    
                    # Preview Circle
                    pygame.draw.circle(self.screen, (20, 25, 30), (x + card_w//2, y + 100), 60)
                    
                    preview_col = border_col if "rainbow" in item_id else item['color']

                    if item['type'] == 'border':
                        pygame.draw.circle(self.screen, preview_col, (x + card_w//2, y + 100), 60, 5)
                    elif item['type'] == 'theme':
                        pygame.draw.circle(self.screen, preview_col, (x + card_w//2, y + 100), 50)
                    elif item['type'] == 'name_color':
                        self.draw_text("Pseudo", self.medium_font, preview_col, x + card_w//2, y + 100)
                    elif item['type'] == 'category':
                        self.draw_text("Aa", self.big_font, preview_col, x + card_w//2, y + 100)
                    
                    # Name
                    self.draw_text(item['name'], self.small_bold_font, TEXT_COLOR, x + card_w//2, y + 190)
                    
                    # Price Icon (if not owned)
                    if item_id not in self.inventory:
                         # Draw small coin next to button? Button has text.
                         pass

            elif self.state == "MENU_INVENTORY":
                self.draw_text_shadow("INVENTAIRE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 80)
                
                # Grid Config
                cx = SCREEN_WIDTH // 2
                card_w, card_h = 260, 300
                cols = 5
                gap = 30
                start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
                start_y = 200 - self.shop_scroll
                
                owned_items = [i for i in self.inventory if i in SHOP_CATALOG]
                
                if not owned_items:
                    self.draw_text("Votre inventaire est vide.", self.font, (150, 150, 150), cx, 300)

                for i, item_id in enumerate(owned_items):
                    item = SHOP_CATALOG[item_id]
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap)
                    y = start_y + row * (card_h + gap)
                    
                    # Clipping
                    if y + card_h < 200 or y > SCREEN_HEIGHT: continue
                    
                    # Card BG
                    rect = pygame.Rect(x, y, card_w, card_h)
                    pygame.draw.rect(self.screen, (35, 40, 50), rect, border_radius=15)
                    
                    border_col = item['color']
                    if "rainbow" in item_id:
                         hue = (pygame.time.get_ticks() // 5) % 360
                         c = pygame.Color(0)
                         c.hsla = (hue, 100, 50, 100)
                         border_col = (c.r, c.g, c.b)
                    pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=15)
                    
                    # Preview
                    pygame.draw.circle(self.screen, (20, 25, 30), (x + card_w//2, y + 100), 60)
                    preview_col = border_col if "rainbow" in item_id else item['color']

                    if item['type'] == 'border':
                        pygame.draw.circle(self.screen, preview_col, (x + card_w//2, y + 100), 60, 5)
                    elif item['type'] == 'theme':
                        pygame.draw.circle(self.screen, preview_col, (x + card_w//2, y + 100), 50)
                    elif item['type'] == 'name_color':
                        self.draw_text("Pseudo", self.medium_font, preview_col, x + card_w//2, y + 100)
                    elif item['type'] == 'category':
                        self.draw_text("Aa", self.big_font, preview_col, x + card_w//2, y + 100)
                        
                    # Name
                    self.draw_text(item['name'], self.small_bold_font, TEXT_COLOR, x + card_w//2, y + 190)

            elif self.state == "SETUP":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 50, 1000, 750) # Agrandissement largeur
                self.draw_text_shadow("CONFIGURATION DE LA PARTIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                cx = SCREEN_WIDTH // 2
                y = 220
                gap = 100
                
                # 1. Joueurs
                if self.is_local_game or self.is_host:
                    self.draw_text("JOUEURS", self.font, (150,150,150), cx, y - 15)
                    self.draw_text(f"{self.settings['players']}", self.medium_font, TEXT_COLOR, cx, y + 30)
                    y += gap
                else:
                    self.draw_text(f"JOUEURS : {self.settings['players']} (En ligne)", self.font, (150, 150, 150), cx, y + 10)
                    y += gap
                
                # 2. Mode
                mode_str = "ÉCRIT" if self.settings['mode'] == 'WRITTEN' else "VOCAL"
                self.draw_text("MODE DE JEU", self.font, (150,150,150), cx, y - 15)
                self.draw_text(mode_str, self.medium_font, TEXT_COLOR, cx, y + 30)
                y += gap
                
                # 3. Catégorie
                self.draw_text("THÈME", self.font, (150,150,150), cx, y - 15)
                cat_font = self.medium_font
                self.draw_text(self.settings['category'], cat_font, ACCENT_COLOR, cx, y + 30)
                y += gap
                
                # 4. Temps
                self.draw_text("TEMPS PAR TOUR", self.font, (150,150,150), cx, y - 15)
                self.draw_text(f"{self.settings['time']}s", self.medium_font, TEXT_COLOR, cx, y + 30)
                y += gap
                
                # 5. Game Type
                y = 220 + 4 * gap # Position after Time
                self.draw_text("TYPE DE JEU", self.font, (150,150,150), cx, y - 15)
                type_str = "NORMAL"
                type_col = TEXT_COLOR
                if self.settings.get('game_type') == 'SURVIVAL':
                    type_str = "SURVIE (Temps -)"
                    type_col = ALERT_COLOR
                elif self.settings.get('game_type') == 'SPEED':
                    type_str = "SPEED (3s)"
                    type_col = (255, 255, 0)
                elif self.settings.get('game_type') == 'HARDCORE':
                    type_str = "HARDCORE (4s)"
                    type_col = (255, 50, 50)
                elif self.settings.get('game_type') == 'CHAOS':
                    type_str = "CHAOS (?)"
                    type_col = (200, 50, 255)
                self.draw_text(type_str, self.medium_font, type_col, cx, y + 30)

            elif self.state == "CONFIRM_QUIT":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 300, 600, 300)
                self.draw_panel(SCREEN_WIDTH//2 - 400, 300, 800, 300)
                self.draw_text_shadow("CONFIRMATION", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 350)
                self.draw_text("Voulez-vous vraiment quitter ?", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 430)

            elif self.state == "CONFIRM_LEAVE":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 300, 600, 300)
                self.draw_panel(SCREEN_WIDTH//2 - 400, 300, 800, 300)
                self.draw_text_shadow("QUITTER LA PARTIE ?", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 350)
                self.draw_text("Voulez-vous vraiment quitter la partie ?", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 430)

            elif self.state == "SETTINGS" or self.state == "CONTROLS":
                self.draw_panel(SCREEN_WIDTH//2 - 600, 100, 1200, 800)
                title = "PARAMÈTRES" if self.state == "SETTINGS" else "TOUCHES"
                self.draw_text_shadow(title, self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 160)
                if self.state == "CONTROLS":
                    self.draw_text("Cliquez pour changer", self.font, (150, 150, 150), SCREEN_WIDTH//2, 350)

                # Feedback Import/Export
                if self.feedback_msg and pygame.time.get_ticks() - self.feedback_timer < 3000:
                    self.draw_text_shadow(self.feedback_msg, self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 580)
                else:
                    if self.state != "GAME": self.feedback_msg = ""

            elif self.state == "HOW_TO":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 100, 1000, 700)
                self.draw_text_shadow("COMMENT JOUER", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                
                lines = [
                    "BUT : Trouvez un mot en lien avec le précédent avant la fin du chrono.",
                    "MODES : Normal, Survie, Speed (3s), Hardcore (4s), Chaos.",
                    "COMBO : Répondez en < 2.5s pour multiplier vos gains !",
                    "BONUS : Wizz (Ctrl+B) pour gêner, Gel (❄️) pour figer le temps.",
                    "BOUTIQUE : Achetez des Packs de mots, Bordures et Thèmes.",
                    "MULTIJOUEUR : Jouez en ligne, ajoutez des amis et échangez des items.",
                    "TOUCHES : Entrée (Valider), Maj/Tab (Contester)."
                ]
                
                for i, line in enumerate(lines):
                    self.draw_text_with_emoji(line, self.font, self.ui_emoji_font, TEXT_COLOR, SCREEN_WIDTH//2, 250 + i*60)
            
            elif self.state.startswith("MENU"):
                # Titre stylisé pour les menus principaux
                # Animation de pulsation
                scale = 1.0 + 0.03 * math.sin(pygame.time.get_ticks() * 0.003)
                title_surf = self.title_font.render("WORLD RUSH", True, ACCENT_COLOR)
                w = int(title_surf.get_width() * scale)
                h = int(title_surf.get_height() * scale)
                scaled_title = pygame.transform.smoothscale(title_surf, (w, h))
                self.screen.blit(scaled_title, scaled_title.get_rect(center=(SCREEN_WIDTH//2, 150)))
                self.draw_text("Association d'idées rapide", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 210)
                
                # Barre d'XP (Menu Principal)
                if self.state == "MENU_MAIN":
                    xp_x, xp_y = 20, 20
                    xp_w, xp_h = 200, 20
                    # Affichage Pièces Menu Principal (Déplacé pour éviter le carré/chevauchement)
                    self.draw_coin_ui(SCREEN_WIDTH - 150, 30, self.coins)
                    
                    self.draw_text(f"Niveau {self.level}", self.font, ACCENT_COLOR, xp_x + xp_w//2, xp_y + 30)
                    threshold = self.get_xp_threshold(self.level)
                    ratio = min(1.0, self.xp / threshold)
                    pygame.draw.rect(self.screen, (30, 35, 45), (xp_x, xp_y, xp_w, xp_h), border_radius=10)
                    pygame.draw.rect(self.screen, (0, 200, 150), (xp_x, xp_y, int(xp_w * ratio), xp_h), border_radius=10)
                    pygame.draw.rect(self.screen, (100, 100, 100), (xp_x, xp_y, xp_w, xp_h), 2, border_radius=10)
                    
                    self.draw_text(f"Victoires: {self.stats['wins']} | Parties: {self.stats['games']}", self.small_bold_font, (150, 150, 150), SCREEN_WIDTH//2, SCREEN_HEIGHT - 80)

            elif self.state == "LOBBY":
                # --- INTERFACE LOBBY ---
                self.draw_text_shadow("SALON D'ATTENTE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 60)
                
                # Zone Gauche : Joueurs
                left_panel = pygame.Rect(50, 100, 600, 650) # Agrandissement panneau joueurs
                self.draw_panel(left_panel.x, left_panel.y, left_panel.w, left_panel.h)
                self.draw_text("JOUEURS", self.font, ACCENT_COLOR, left_panel.centerx, left_panel.y + 30)
                
                # Affichage dynamique des joueurs (jusqu'à 4)
                for i in range(self.settings['players']):
                    y_pos = left_panel.y + 80 + i * 100
                    
                    # Données par défaut
                    p_name = "En attente..."
                    p_status = "..."
                    p_col = (150, 150, 150)
                    p_av = "?"
                    p_border = "border_default"
                    
                    # Remplissage données réelles
                    if self.is_local_game:
                        p_name = f"Joueur {i+1}"
                        p_name_color = "name_color_default"
                        if i == 0:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']
                        else:
                            p_av = AVATARS[i % len(AVATARS)]
                        
                        if i < len(self.ready_status):
                            p_status = "PRÊT" if self.ready_status[i] else "PAS PRÊT"
                            p_col = (100, 255, 100) if self.ready_status[i] else (255, 100, 100)

                    elif self.is_host:
                        if i == 0:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']
                            p_status = "PRÊT" if self.ready_status[0] else "PAS PRÊT"
                            p_col = (100, 255, 100) if self.ready_status[0] else (255, 100, 100)
                        elif i - 1 < len(self.clients):
                            c = self.clients[i - 1]
                            p_name = c['name']; p_av = c['avatar']; p_border = c['border']; p_name_color = c.get('name_color', 'name_color_default')
                            p_status = "PRÊT" if c['ready'] else "PAS PRÊT"
                            p_col = (100, 255, 100) if c['ready'] else (255, 100, 100)
                            
                    else: # Client
                        if i in self.lobby_cache:
                            d = self.lobby_cache[i]
                            p_name = d['name']; p_av = d['avatar']; p_border = d['border']; p_name_color = d.get('name_color', 'name_color_default')
                            p_status = "PRÊT" if d['ready'] else "PAS PRÊT"
                            p_col = (100, 255, 100) if d['ready'] else (255, 100, 100)
                        elif i == self.my_id:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']
                            p_status = "PRÊT" if self.ready_status[i] else "PAS PRÊT"
                            p_col = (100, 255, 100) if self.ready_status[i] else (255, 100, 100)
                    
                    # Animation Pulse pour "PRÊT"
                    if p_status == "PRÊT":
                        scale = 1.0 + 0.05 * math.sin(pygame.time.get_ticks() * 0.01)
                        font = pygame.font.SysFont("Arial", int(30 * scale), bold=True)
                        self.draw_text(f"{p_name} - {p_status}", font, p_col, left_panel.centerx, y_pos)
                    else:
                        self.draw_text(f"{p_status}", self.font, p_col, left_panel.centerx, y_pos + 25)
                        self.draw_text(f"{p_name}", self.font, self.get_name_color(p_name_color), left_panel.centerx, y_pos - 10)
                        
                    self.draw_avatar(p_av, left_panel.centerx - 200, y_pos, 25, p_border)

                # Infos IP (si Host)
                if self.is_host:
                    self.draw_text(f"IP Locale: {self.local_ip}", self.font, TEXT_COLOR, left_panel.centerx, left_panel.y + 450)
                    if self.public_ip:
                        self.draw_text(f"IP Internet: {self.public_ip}", self.font, ACCENT_COLOR, left_panel.centerx, left_panel.y + 490)
                    self.draw_text(f"UPnP: {self.upnp_status}", self.font, (150, 150, 150), left_panel.centerx, left_panel.y + 530)
                
                # Indicateur Qualité Connexion (Simulé)
                if self.connected or (self.is_host and len(self.clients) > 0):
                    ping_col = (50, 255, 50)
                    # Position en haut à droite
                    ind_x = SCREEN_WIDTH - 40
                    ind_y = 40
                    pygame.draw.circle(self.screen, ping_col, (ind_x, ind_y), 8)
                    # Texte à gauche du point
                    text_surf = self.small_bold_font.render("Connexion Stable", True, ping_col)
                    self.screen.blit(text_surf, (ind_x - 15 - text_surf.get_width(), ind_y - text_surf.get_height() // 2))
                    # Petit effet d'onde
                    pygame.draw.circle(self.screen, ping_col, (ind_x, ind_y), 8 + (3 * math.sin(pygame.time.get_ticks() * 0.005)), 1)

                # Zone Droite : Chat
                chat_x = 680 # Décalage suite agrandissement gauche
                chat_y = 100
                chat_w = SCREEN_WIDTH - chat_x - 50
                chat_h = SCREEN_HEIGHT - chat_y - 50
                chat_panel = pygame.Rect(chat_x, chat_y, chat_w, chat_h)
                self.draw_panel(chat_panel.x, chat_panel.y, chat_panel.w, chat_panel.h)
                self.draw_text("CHAT", self.font, ACCENT_COLOR, chat_panel.centerx, chat_panel.y + 30)
                
                # Messages (avec Scroll)
                input_h = 60
                header_h = 60
                msg_area_y = chat_panel.y + header_h
                msg_area_h = chat_panel.h - header_h - input_h - 10
                line_h = 30
                max_lines = msg_area_h // line_h
                
                total_msgs = len(self.chat_messages)
                if total_msgs <= max_lines:
                    self.chat_scroll = 0
                    visible_msgs = self.chat_messages
                else:
                    max_scroll = total_msgs - max_lines
                    if self.chat_scroll > max_scroll: self.chat_scroll = max_scroll
                    start = total_msgs - max_lines - self.chat_scroll
                    end = total_msgs - self.chat_scroll
                    visible_msgs = self.chat_messages[start:end]

                for i, msg in enumerate(visible_msgs):
                    col = (255, 200, 0) if msg.startswith("SYSTEM") else TEXT_COLOR
                    self.draw_text(msg, self.font, col, chat_panel.x + 20, msg_area_y + i * line_h, center=False)
                
                # Input Chat
                pygame.draw.rect(self.screen, (20, 25, 35), (chat_panel.x + 20, chat_panel.bottom - 60, chat_panel.w - 40, 40), border_radius=10)
                self.draw_text(self.chat_input, self.font, TEXT_COLOR, chat_panel.x + 30, chat_panel.bottom - 55, center=False)

            elif self.state == "JUDGMENT":
                if self.is_local_game or self.judge_id == self.my_id:
                    self.draw_text_shadow("CONTESTATION !", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 100)
                    self.draw_text("Le dernier mot est-il valide ?", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 200)
                else:
                    self.draw_text_shadow("CONTESTATION EN COURS...", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 100)
                    self.draw_text("Attente du jugement...", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 200)

            elif self.state == "ROUND_COUNTDOWN":
                remaining = 5 - (pygame.time.get_ticks() - self.countdown_start) / 1000
                
                # Affichage du message de fin de manche
                msg_color = TEXT_COLOR
                msg_text = "Point attribué !"
                
                if self.last_round_reason == "TIMEOUT":
                    if self.last_round_winner == self.my_id:
                        msg_text = "L'adversaire a été trop lent ! Tu gagnes le point."
                        msg_color = ACCENT_COLOR
                    else:
                        msg_text = "Temps écoulé ! Tu as perdu..."
                        msg_color = ALERT_COLOR
                
                self.draw_text_shadow(msg_text, self.font, msg_color, SCREEN_WIDTH//2, 250)
                self.draw_text(f"Manche {self.round_num} dans {int(remaining) + 1}...", self.big_font, (200, 200, 200), SCREEN_WIDTH//2, 400)

            elif self.state == "BONUS_GAME":
                self.draw_text_shadow("BONUS : ATTRAPEZ LES PIÈCES !", self.big_font, (255, 215, 0), SCREEN_WIDTH//2, 50)
                rem = (self.bonus_end_time - pygame.time.get_ticks()) / 1000
                self.draw_text(f"{rem:.1f}s", self.big_font, (255, 255, 255), SCREEN_WIDTH//2, 100)
                
                for t in self.bonus_targets:
                    # Dessin pièce
                    pygame.draw.circle(self.screen, (255, 215, 0), t.center, 35)
                    pygame.draw.circle(self.screen, (255, 255, 200), (t.centerx - 10, t.centery - 10), 10)
                    self.draw_text("$", self.medium_font, (200, 150, 0), t.centerx, t.centery)

            elif self.state == "OPPONENT_LEFT":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 200, 600, 400)
                self.draw_text_shadow("ADVERSAIRE PARTI", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 250)
                self.draw_text("Votre adversaire a quitté la partie.", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 350)

            elif self.state == "GAME_OVER":
                self.draw_panel(SCREEN_WIDTH//2 - 600, 100, 1200, 700)
                title = "VICTOIRE !" if self.winner_text == self.username else "DÉFAITE..."
                if self.is_local_game: title = "FIN DE PARTIE"
                
                color = ACCENT_COLOR if title == "VICTOIRE !" else ALERT_COLOR
                self.draw_text_shadow(title, self.big_font, color, SCREEN_WIDTH//2, 150)
                
                # Animation XP
                if self.xp_animating:
                    threshold = self.get_xp_threshold(self.anim_level_val)
                    self.anim_xp_val += 0.5 # Vitesse animation
                    if self.anim_xp_val >= threshold:
                        self.anim_xp_val = 0
                        self.anim_level_val += 1
                        self.play_sound("start")
                    
                    # Fin animation
                    if self.anim_level_val > self.target_level_val or (self.anim_level_val == self.target_level_val and self.anim_xp_val >= self.target_xp_val):
                        self.anim_xp_val = self.target_xp_val
                        self.anim_level_val = self.target_level_val
                        self.xp_animating = False

                # Barre XP
                bar_w = 500
                bar_h = 30
                bx = SCREEN_WIDTH//2 - bar_w//2
                by = 360
                thresh = self.get_xp_threshold(self.anim_level_val)
                ratio = min(1.0, self.anim_xp_val / thresh)
                
                self.draw_text(f"Niveau {self.anim_level_val}", self.medium_font, ACCENT_COLOR, SCREEN_WIDTH//2, by - 30)
                pygame.draw.rect(self.screen, (30, 35, 45), (bx, by, bar_w, bar_h), border_radius=10)
                pygame.draw.rect(self.screen, (0, 200, 150), (bx, by, int(bar_w * ratio), bar_h), border_radius=10)
                pygame.draw.rect(self.screen, (100, 100, 100), (bx, by, bar_w, bar_h), 2, border_radius=10)
                
                self.draw_text(f"+{50 if title == 'VICTOIRE !' else 0} Pièces", self.medium_font, (255, 215, 0), SCREEN_WIDTH//2, 280)
                self.draw_text(f"Gagnant : {self.winner_text}", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 220)
                
                # Status rematch
                rematch_count = sum(self.rematch_ready)
                if self.rematch_ready[self.my_id]: self.draw_text("En attente de l'adversaire...", self.small_bold_font, ACCENT_COLOR, SCREEN_WIDTH//2, 480)
                self.draw_text(f"Rejouer : {rematch_count}/{self.settings['players']}", self.font, (150, 150, 150), SCREEN_WIDTH//2, 440)
                
                # Confetti si victoire
                if self.winner_text == self.username or (self.is_local_game and "Joueur" in self.winner_text):
                    if random.random() < 0.3:
                        self.add_particles(random.randint(0, SCREEN_WIDTH), -10, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))

            elif self.state == "GAME":
                # Affichage HUD
                if self.is_local_game:
                    score_text = "   ".join([f"J{i+1}: {s}" for i, s in enumerate(self.score)])
                else:
                    # Afficher les pseudos en ligne
                    p1 = self.username if self.my_id == 0 else self.opponent_name
                    p2 = self.opponent_name if self.my_id == 0 else self.username
                    
                    c1 = self.get_name_color(self.equipped['name_color']) if self.my_id == 0 else self.get_name_color(self.opponent_name_color)
                    c2 = self.get_name_color(self.opponent_name_color) if self.my_id == 0 else self.get_name_color(self.equipped['name_color'])
                    
                    # Manual positioning
                    cx = SCREEN_WIDTH // 2
                    
                    # P1 (Left-ish)
                    txt1 = f"{p1}: {self.score[0]}"
                    surf1 = self.font.render(txt1, True, c1)
                    
                    # Separator
                    sep = "   |   "
                    surf_sep = self.font.render(sep, True, TEXT_COLOR)
                    
                    # P2 (Right-ish)
                    txt2 = f"{p2}: {self.score[1]}"
                    surf2 = self.font.render(txt2, True, c2)
                    
                    total_w = surf1.get_width() + surf_sep.get_width() + surf2.get_width()
                    start_x = cx - total_w // 2
                    
                    self.screen.blit(surf1, (start_x, 30))
                    self.screen.blit(surf_sep, (start_x + surf1.get_width(), 30))
                    self.screen.blit(surf2, (start_x + surf1.get_width() + surf_sep.get_width(), 30))
                
                turn_msg = f"Tour du Joueur {self.current_player + 1}" if self.is_local_game else ("C'est votre tour !" if self.current_player == self.my_id else "Tour de l'adversaire...")
                self.draw_text(turn_msg, self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 70)
                
                # Affichage Mot de l'adversaire (Haut Droite)
                self.draw_panel(SCREEN_WIDTH - 450, 20, 430, 120)
                self.draw_text("MOT PRÉCÉDENT :", self.font, (150, 150, 150), SCREEN_WIDTH - 235, 45)
                self.draw_text_shadow(f"{self.current_word}", self.big_font, ACCENT_COLOR, SCREEN_WIDTH - 235, 95)
                
                # Affichage Timer
                timer_color = ALERT_COLOR if self.time_left < 2 else TEXT_COLOR
                if self.time_left <= 3 and self.time_left > 0:
                    self.draw_text_glitch(f"{max(0, self.time_left):05.2f}", self.timer_font, timer_color, SCREEN_WIDTH//2, 250)
                else:
                    self.draw_text(f"{max(0, self.time_left):05.2f}", self.timer_font, timer_color, SCREEN_WIDTH//2, 250)
                
                # Barre de temps
                bar_width = 600
                bar_height = 30
                fill_width = max(0, (self.time_left / self.round_duration) * bar_width)
                pygame.draw.rect(self.screen, (40, 40, 50), (SCREEN_WIDTH//2 - bar_width//2, 300, bar_width, bar_height), border_radius=15)
                pygame.draw.rect(self.screen, timer_color, (SCREEN_WIDTH//2 - bar_width//2, 300, fill_width, bar_height), border_radius=15)

                # Flash rouge si temps < 2s
                if 0 < self.time_left <= 2:
                    flash_s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    flash_s.fill(ALERT_COLOR)
                    alpha = int(40 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
                    flash_s.set_alpha(alpha)
                    self.screen.blit(flash_s, (0, 0))
                
                # Effet Visuel Gel du Temps
                if pygame.time.get_ticks() < self.freeze_until:
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    overlay.fill((100, 200, 255, 30))
                    self.screen.blit(overlay, (0, 0))
                    self.draw_text("TEMPS GELÉ", self.big_font, (100, 200, 255), SCREEN_WIDTH//2, 180)

                if self.time_left <= 0:
                    self.draw_text_shadow("TEMPS ÉCOULÉ !", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 450)
                    # Ici on pourrait forcer la fin du tour ou attendre une action

                # Spécifique Mode Écrit
                if self.settings['mode'] == "WRITTEN":
                    # Zone de texte centrée
                    input_w = 500
                    input_rect = pygame.Rect(SCREEN_WIDTH//2 - input_w//2, 380, input_w, 60)
                    
                    # Bordure colorée si c'est notre tour
                    border_col = ACCENT_COLOR if (self.is_local_game or self.current_player == self.my_id) else (60, 65, 80)
                    pygame.draw.rect(self.screen, (30, 35, 45), input_rect, border_radius=15)
                    pygame.draw.rect(self.screen, border_col, input_rect, 2, border_radius=15)
                    
                    # Afficher le texte de l'utilisateur ou de l'adversaire
                    if self.current_player == self.my_id:
                        display_text = self.user_text
                    else:
                        display_text = self.opponent_text if self.opponent_text else "L'adversaire réfléchit..."
                    
                    # Correction alignement vertical (remonté de 410 à 408)
                    self.draw_text(display_text, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 408)
                    self.draw_text("Écrivez et appuyez sur ENTRÉE.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 500)
                    
                    # Feedback "Déjà dit"
                    if self.feedback_msg and pygame.time.get_ticks() - self.feedback_timer < 2000:
                        self.draw_text_shadow(self.feedback_msg, self.font, ALERT_COLOR, SCREEN_WIDTH//2, 350)
                    else:
                        self.feedback_msg = ""
                
                # Spécifique Mode Vocal
                if self.settings['mode'] == "VOCAL":
                    self.draw_text_shadow("Parlez maintenant !", self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 400)
                    self.draw_text("ESPACE quand fini. 'A' pour contester.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 550)

            # Affichage des boutons (en dernier pour être au-dessus des panneaux)
            for btn in self.buttons:
                btn.draw(self.screen)
            
            # Affichage Popup (Overlay)
            if self.popup:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 180))
                self.screen.blit(s, (0, 0))
                
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                w, h = 600, 400
                self.draw_panel(cx - w//2, cy - h//2, w, h)
                
                self.draw_text_shadow(self.popup["title"], self.big_font, ACCENT_COLOR, cx, cy - 120)
                self.draw_text(self.popup["msg"], self.font, TEXT_COLOR, cx, cy - 50)
                
                if "avatar" in self.popup:
                    self.draw_avatar(self.popup["avatar"], cx, cy + 20, 40)
                
                # Boutons Popup
                btn_w, btn_h = 200, 60
                yes_rect = pygame.Rect(cx - btn_w - 20, cy + 100, btn_w, btn_h)
                no_rect = pygame.Rect(cx + 20, cy + 100, btn_w, btn_h)
                
                self.popup["rect_yes"] = yes_rect
                self.popup["rect_no"] = no_rect
                
                mx, my = pygame.mouse.get_pos()
                col_yes = HOVER_COLOR if yes_rect.collidepoint(mx, my) else ACCENT_COLOR
                col_no = (255, 100, 100) if no_rect.collidepoint(mx, my) else ALERT_COLOR
                
                pygame.draw.rect(self.screen, col_yes, yes_rect, border_radius=15)
                self.draw_text("ACCEPTER", self.small_bold_font, (20, 25, 35), yes_rect.centerx, yes_rect.centery)
                
                pygame.draw.rect(self.screen, col_no, no_rect, border_radius=15)
                self.draw_text("REFUSER", self.small_bold_font, (255, 255, 255), no_rect.centerx, no_rect.centery)

            # Notifications (Tout au dessus)
            self.draw_notifications()
            
            # Popup Succès (Steam style)
            self.draw_achievement_popup()

            if using_temp_screen:
                real_screen.blit(self.screen, (shake_x, shake_y))
                self.screen = real_screen

            # Copyright & Version
            self.draw_text("© dodosi", self.font, (80, 80, 90), SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30)
            self.draw_text(CURRENT_VERSION, self.font, (80, 80, 90), 40, SCREEN_HEIGHT - 30)
            
            # Indicateur Mode Développeur
            if self.test_mode:
                pygame.draw.rect(self.screen, ALERT_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)
                self.draw_text("DEV MODE ACTIF", self.medium_font, ALERT_COLOR, SCREEN_WIDTH//2, 30)
                self.draw_text("X: XP | U: Succès | I: Items | W: Win | coins: $$$ | /: Lose | : : Win Pt", self.small_bold_font, ALERT_COLOR, SCREEN_WIDTH//2, 60)

            # --- TRANSITION ---
            if self.transition_state == "OUT":
                self.transition_alpha += 15
                if self.transition_alpha >= 255:
                    self.transition_alpha = 255
                    self.state = self.next_state
                    self._apply_state_change()
                    self.transition_state = "IN"
            elif self.transition_state == "IN":
                self.transition_alpha -= 15
                if self.transition_alpha <= 0:
                    self.transition_alpha = 0
                    self.transition_state = None
            
            if self.transition_alpha > 0:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                s.set_alpha(self.transition_alpha)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        self.remove_upnp()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        game.remove_upnp()
        pygame.quit()
