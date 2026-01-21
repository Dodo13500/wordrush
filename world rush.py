import pygame
import sys
import random
import socket
import threading
import json
import os
import math
import urllib.request

# --- Configuration ---
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
BG_COLOR = (15, 18, 25)       # Fond très sombre
PANEL_COLOR = (30, 35, 45)    # Panneaux
TEXT_COLOR = (230, 230, 230)
ACCENT_COLOR = (0, 220, 255)  # Cyan néon
ALERT_COLOR = (255, 80, 100)  # Rouge vif
HOVER_COLOR = (50, 220, 255)
FONT_SIZE = 28
PORT = 5555
SETTINGS_FILE = "world_rush_settings.json"

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

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.SysFont("Arial", 26, bold=True)

    def draw(self, screen, offset_y=0):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Bouton avec effet néon/moderne
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        # Effet de pulsation sur la bordure
        alpha = int(100 + 50 * math.sin(pygame.time.get_ticks() * 0.005))
        pygame.draw.rect(screen, (255, 255, 255, alpha), self.rect, 2, border_radius=15)
        
        text_surf = self.font.render(self.text, True, (20, 25, 35))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

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
        self.medium_font = pygame.font.SysFont("Arial", 45, bold=True)
        self.timer_font = pygame.font.SysFont("Consolas", 80, bold=True) # Police fixe pour chrono fluide
        
        # États du jeu
        self.state = "INPUT_NAME" # INPUT_NAME, MENU_MAIN, MENU_ONLINE, SETUP, SETTINGS, CONTROLS, LOBBY, HOW_TO, GAME, JUDGMENT, GAME_OVER, ROUND_COUNTDOWN, OPPONENT_LEFT
        
        # Paramètres de la partie
        self.settings = {
            'players': 2,
            'time': 5,
            'mode': 'VOCAL',
            'win_score': 5,
            'category': 'GÉNÉRAL'
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
        self.time_left = 0
        self.opponent_text = "" # Texte de l'adversaire en temps réel
        self.opponent_name = "Adversaire"
        self.score = [0, 0] # Joueur 1, Joueur 2
        self.current_player = 0 # 0 (Host) ou 1 (Client)
        self.my_id = 0 # Mon identité
        self.winner_text = ""
        self.username = ""
        self.rematch_ready = [False, False] # [Host, Client] ou [J1, J2...]
        self.judge_id = -1
        self.round_num = 1
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
        
        # Réseau
        self.server = None
        self.conn = None
        self.input_ip = "127.0.0.1"
        self.network_queue = []
        self.is_host = False
        self.connected = False
        self.is_local_game = False
        self.connect_status = "" # "", "CONNECTING", "FAILED"
        
        # Mode Test / Debug
        self.test_mode = False
        self.t_press_count = 0
        self.last_t_press = 0
        self.bot_timer = 0

        # Chargement des paramètres
        self.load_settings()
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
                    self.first_run = data.get("first_run", True)
                    # Charger les touches si elles existent
                    saved_keys = data.get("keys", {})
                    for k, v in saved_keys.items():
                        self.keys[k] = v
            except:
                pass

    def save_settings(self):
        # Sauvegarder pseudo et touches
        data = {"username": self.username, "keys": self.keys, "first_run": self.first_run}
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
        self.settings['players'] = 2
        self.settings['win_score'] = 5
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

    def create_menu_buttons(self):
        cx = SCREEN_WIDTH // 2
        self.buttons = []
        if self.state == "TUTORIAL":
            self.buttons = [
                Button("J'AI COMPRIS !", cx - 150, 650, 300, 70, ACCENT_COLOR, HOVER_COLOR, self.close_tutorial)
            ]

        elif self.state == "INPUT_NAME":
            self.buttons = [Button("VALIDER", cx - 100, 400, 200, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_name)]

        elif self.state == "MENU_MAIN":
            btn_w = 360
            btn_h = 60
            gap = 20
            start_y = 280
            self.buttons = [
                Button("LOCAL (Même PC)", cx - btn_w//2, start_y, btn_w, btn_h, ACCENT_COLOR, HOVER_COLOR, self.setup_local),
                Button("EN LIGNE (Réseau)", cx - btn_w//2, start_y + btn_h + gap, btn_w, btn_h, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_ONLINE")),
                Button("PARAMÈTRES", cx - btn_w//2, start_y + (btn_h + gap)*2, btn_w, btn_h, (100, 100, 120), (140, 140, 160), lambda: self.set_state("SETTINGS")),
                Button("COMMENT JOUER", cx - btn_w//2, start_y + (btn_h + gap)*3, btn_w, btn_h, (100, 100, 120), (140, 140, 160), lambda: self.set_state("HOW_TO")),
                Button("QUITTER", cx - btn_w//2, start_y + (btn_h + gap)*4, btn_w, btn_h, ALERT_COLOR, (255, 100, 120), self.cleanup_and_exit)
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
            btn_off = 220   # Écartement des boutons pour laisser place au texte
            
            # 1. Joueurs
            if self.is_local_game:
                self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', -1)))
                self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', 1)))
            current_y += block_gap
            
            # 2. Mode
            self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('mode', 0)))
            self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('mode', 0)))
            current_y += block_gap
            
            # 3. Catégorie
            self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', -1)))
            self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', 1)))
            current_y += block_gap
            
            # 4. Temps
            self.buttons.append(Button("<", cx - btn_off, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', -1)))
            self.buttons.append(Button(">", cx + btn_off - 60, current_y, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', 1)))
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
            self.buttons = [
                Button("RÉINITIALISER DONNÉES", cx - 180, 300, 360, 60, ALERT_COLOR, (255, 100, 120), self.reset_app),
                Button("TOUCHES / CLAVIER", cx - 180, 400, 360, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("CONTROLS")),
                Button("RETOUR", cx - 180, 500, 360, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))
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
                Button("CONNEXION", cx - 150, 550, 300, 70, ACCENT_COLOR, HOVER_COLOR, self.connect_to_host),
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_ONLINE"))
            ]
        elif self.state == "GAME_OVER":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("RECOMMENCER", cx - 300, 500, 250, 60, ACCENT_COLOR, HOVER_COLOR, self.request_rematch),
                Button("MENU PRINCIPAL", cx + 50, 500, 250, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN")),
                Button("QUITTER", cx - 100, 600, 200, 60, ALERT_COLOR, (255, 100, 120), self.cleanup_and_exit)
            ]

    def set_state(self, new_state):
        self.state = new_state
        self.buttons = []
        if new_state in ["MENU_MAIN", "MENU_ONLINE", "SETUP", "INPUT_NAME", "GAME_OVER", "SETTINGS", "CONTROLS", "OPPONENT_LEFT", "MENU_JOIN", "TUTORIAL"]:
            self.create_menu_buttons()
        elif new_state == "HOW_TO":
            self.buttons = [Button("RETOUR", 50, 50, 150, 50, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))]
        elif new_state == "LOBBY":
            self.buttons = [Button("RETOUR", 50, 50, 150, 50, ALERT_COLOR, (255, 100, 120), self.reset_network)]
        elif new_state == "JUDGMENT":
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
            cats = list(WORD_CATEGORIES.keys())
            current_idx = cats.index(self.settings['category'])
            next_idx = (current_idx + delta) % len(cats)
            if next_idx < 0: # Handle negative modulo result for previous button
                next_idx += len(cats)
            self.settings['category'] = cats[next_idx]
        
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
            self.send_data(f"READY|{self.my_id}|{status_str}")
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

    def setup_local(self):
        self.is_local_game = True
        self.score = [0] * self.settings['players']
        self.rematch_ready = [False] * self.settings['players']
        self.set_state("SETUP")
        self.ready_status = [False] * self.settings['players']

    def start_local_game(self):
        self.start_round()

    def setup_host(self):
        self.is_host = True
        self.is_local_game = False
        self.my_id = 0
        self.settings['players'] = 2
        self.round_num = 1
        self.score = [0, 0]
        self.last_round_reason = ""
        self.rematch_ready = [False, False]
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

    def cleanup_and_exit(self):
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
        threading.Thread(target=self.wait_for_connection, daemon=True).start()

    def wait_for_connection(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(('0.0.0.0', PORT))
            self.server.listen(1)
            self.conn, addr = self.server.accept()
            self.connected = True
            threading.Thread(target=self.receive_data, daemon=True).start()
        except:
            pass

    def setup_join(self):
        self.is_host = False
        self.is_local_game = False
        self.my_id = 1
        self.settings['players'] = 2
        self.round_num = 1
        self.score = [0, 0]
        self.last_round_reason = ""
        self.rematch_ready = [False, False]
        self.set_state("MENU_JOIN")
        self.chat_messages = []
        self.ready_status = [False, False]
        self.connect_status = ""

    def connect_to_host(self):
        self.connect_status = "Connexion..."
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.settimeout(5)
            self.conn.connect((self.input_ip, PORT))
            self.conn.settimeout(None)
            self.connected = True
            self.connect_status = "Connecté !"
            self.set_state("LOBBY")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except:
            self.connect_status = "Échec connexion"
            self.connected = False

    def receive_data(self):
        buffer = b""
        while self.connected:
            try:
                data = self.conn.recv(1024)
                if not data: break
                buffer += data
                while b"\n" in buffer:
                    msg_bytes, buffer = buffer.split(b"\n", 1)
                    try:
                        msg = msg_bytes.decode('utf-8').strip()
                        if msg: self.network_queue.append(msg)
                    except: pass
            except:
                break
        self.connected = False
        self.set_state("MENU_MAIN")

    def send_data(self, data):
        if self.conn:
            try:
                self.conn.sendall((data + "\n").encode())
            except:
                pass

    def send_action(self, action):
        # Envoie une action et l'exécute localement aussi si nécessaire
        if not self.is_local_game:
            self.send_data(f"ACTION|{action}")
        self.process_action(action)
    
    def send_name(self):
        # Envoie mon pseudo à l'autre
        self.send_data(f"NAME|{self.username}")

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
        return random.choice(WORD_CATEGORIES[self.settings['category']])

    def check_start_game(self):
        # Si tout le monde est prêt
        if all(self.ready_status):
            if self.is_host or self.is_local_game:
                self.send_data(f"START|{self.settings['mode']}|{self.settings['time']}|{self.settings['win_score']}|{self.settings['category']}")
                self.start_round()

    def start_round(self, new_word=True, specific_word=None):
        # Seul l'hôte ou le jeu local décide du mot
        if self.is_host or self.is_local_game:
            if new_word:
                self.current_word = self.get_random_word() if specific_word is None else specific_word
            if not self.is_local_game:
                self.send_data(f"NEW_ROUND|{self.current_word}|{self.settings['time']}|{self.settings['win_score']}|{self.round_num}")
            self.reset_round_state()

    def reset_round_state(self):
        self.user_text = ""
        self.opponent_text = ""
        self.start_ticks = pygame.time.get_ticks()
        self.time_left = float(self.settings['time']) # Initialiser le temps pour éviter le timeout immédiat
        self.state = "GAME"
        self.buttons = [
            Button("QUITTER", 20, 20, 120, 40, ALERT_COLOR, (255, 100, 100), self.quit_game)
        ]
        self.rematch_ready = [False] * self.settings['players']
        self.particles = []
        self.judge_id = -1
        self.ready_status = [False] * self.settings['players'] # Reset ready correct pour N joueurs

    def draw_text(self, text, font, color, x, y, center=True):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_text_shadow(self, text, font, color, x, y, center=True):
        # Ombre
        surface_s = font.render(text, True, (0, 0, 0))
        rect_s = surface_s.get_rect()
        if center: rect_s.center = (x+2, y+2)
        else: rect_s.topleft = (x+2, y+2)
        self.screen.blit(surface_s, rect_s)
        # Texte
        self.draw_text(text, font, color, x, y, center)

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
                
                # Le joueur actuel a perdu le point
                # C'est l'autre joueur (ou le suivant) qui gagne le point
                winner_idx = (self.current_player + 1) % self.settings['players']
                self.score[winner_idx] += 1
                self.round_num += 1
                self.last_round_winner = winner_idx
                self.add_particles(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, ACCENT_COLOR)
                
                # Vérification victoire
                if self.score[winner_idx] >= self.settings['win_score']:
                    self.winner_text = f"Joueur {winner_idx + 1}" if self.is_local_game else (self.username if winner_idx == self.my_id else self.opponent_name)
                    self.set_state("GAME_OVER")
                else:
                    self.current_player = winner_idx
                    # Lancer le compte à rebours avant la prochaine manche
                    self.state = "ROUND_COUNTDOWN"
                    self.countdown_start = pygame.time.get_ticks()
                    # Réinitialiser les boutons pour éviter de cliquer pendant le compte à rebours
                    self.buttons = []
            
            elif action_type == "CONTINUE":
                self.reset_round_state()
            
            elif action_type == "NEXT_TURN":
                # Récupérer le mot tapé s'il y en a un (Mode écrit)
                next_word = args[1] if len(args) > 1 else None
                
                self.current_player = (self.current_player + 1) % self.settings['players']
                
                if self.is_host or self.is_local_game:
                    # En mode écrit, le nouveau mot est celui qui vient d'être validé
                    # En mode vocal, on garde le même mot affiché (ou on ne change rien) pour ne pas perturber la chaîne
                    should_change = (self.settings['mode'] == 'WRITTEN')
                    self.start_round(new_word=should_change, specific_word=next_word)
            
            elif action_type == "JUDGE":
                self.judge_id = int(args[1]) if len(args) > 1 else -1
                self.set_state("JUDGMENT")
            
            elif action_type == "REMATCH":
                player_id = int(args[1])
                if 0 <= player_id < len(self.rematch_ready):
                    self.rematch_ready[player_id] = True
                
                # Si tout le monde est prêt
                if all(self.rematch_ready):
                    self.score = [0] * self.settings['players']
                    self.last_round_reason = ""
                    self.round_num = 1
                    self.ready_status = [False] * self.settings['players'] # Reset ready
                    if self.is_host or self.is_local_game:
                        self.start_round()
        except Exception as e:
            print(f"Erreur action: {e}")

    def draw_background(self):
        self.screen.fill(BG_COLOR)
        # Grille mouvante (Effet moderne)
        grid_color = (25, 30, 40)
        offset = (pygame.time.get_ticks() // 50) % 50
        
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
            
        for y in range(-50, SCREEN_HEIGHT, 50):
            draw_y = y + offset
            pygame.draw.line(self.screen, grid_color, (0, draw_y), (SCREEN_WIDTH, draw_y))
        
        # Vignette (Assombrir les coins pour un look pro)
        # On crée une surface avec un dégradé radial simulé ou juste des bords sombres
        # Pour optimiser, on dessine juste un cadre épais flou ou semi-transparent
        # Ici, méthode simple :
        pass # Le fond uni + grille est déjà propre, les panneaux feront le reste

    def draw_panel(self, x, y, w, h):
        # Panneau semi-transparent (Glassmorphism)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((30, 35, 45, 230)) # Couleur sombre avec transparence (Alpha 230)
        self.screen.blit(s, (x, y))
        
        # Bordure fine
        pygame.draw.rect(self.screen, (60, 70, 90), (x, y, w, h), 2, border_radius=20)

    def run(self):
        running = True
        while running:
            self.draw_background()
            
            # Gestion des événements globaux
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
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

                # Gestion des boutons
                for btn in self.buttons:
                    if btn.check_click(event):
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
                                else:
                                    if len(self.user_text) < 20 and event.key != self.keys["CONTEST"]:
                                        self.user_text += event.unicode
                        
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
                # Timer & Timeout
                elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                self.time_left = float(self.settings['time']) - elapsed
                
                if (self.is_host or self.is_local_game) and self.time_left <= 0:
                    self.send_action("POINT|TIMEOUT")
            
            elif self.state == "ROUND_COUNTDOWN":
                if pygame.time.get_ticks() - self.countdown_start > 3000: # 3 secondes
                    self.start_round()

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
            while self.network_queue:
                msg = self.network_queue.pop(0)
                parts = msg.split("|")
                cmd = parts[0]
                
                if cmd == "START":
                    self.settings['mode'] = parts[1]
                    self.settings['time'] = int(parts[2])
                    self.settings['win_score'] = int(parts[3])
                    if len(parts) > 4: self.settings['category'] = parts[4]
                    self.round_num = 1
                    self.send_name() # Envoyer mon nom en réponse
                    # Le client attend le mot
                elif cmd == "NEW_ROUND":
                    self.current_word = parts[1]
                    self.reset_round_state()
                elif cmd == "ACTION":
                    self.process_action(parts[1])
                    if parts[1].startswith("NEXT_TURN") and len(parts) > 2: # Cas spécial pour passer le mot
                        self.process_action(f"NEXT_TURN|{parts[2]}")
                elif cmd == "TYPE":
                    self.opponent_text = parts[1]
                elif cmd == "NAME":
                    self.opponent_name = parts[1]
                elif cmd == "READY":
                    try:
                        pid = int(parts[1])
                        self.ready_status[pid] = (parts[2] == "1")
                        self.check_start_game()
                    except: pass

            if not running:
                break

            # --- AFFICHAGE ---
            if self.state == "TUTORIAL":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 600)
                self.draw_text_shadow("BIENVENUE !", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 160)
                
                lines = [
                    "World Rush est un jeu d'association d'idées rapide.",
                    "1. Un mot s'affiche (ex: 'Plage').",
                    "2. Vous devez donner un mot lié (ex: 'Sable').",
                    "3. Attention au chrono ! Si le temps tombe à 0, vous perdez.",
                    "4. Jouez en local ou en ligne avec vos amis.",
                    "5. Utilisez 'CONTESTER' si un mot est mauvais."
                ]
                for i, line in enumerate(lines):
                    self.draw_text(line, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 260 + i*50)

            elif self.state == "INPUT_NAME":
                self.draw_text("BIENVENUE DANS WORLD RUSH", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                self.draw_text("Entrez votre pseudo :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 250)
                pygame.draw.rect(self.screen, (50, 50, 60), (SCREEN_WIDTH//2 - 150, 300, 300, 50), border_radius=10)
                self.draw_text(self.username, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 325)

            elif self.state == "MENU_JOIN":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 200, 800, 500)
                self.draw_text_shadow("REJOINDRE UNE PARTIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 260)
                self.draw_text("Entrez l'IP de l'hôte :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 360)
                
                pygame.draw.rect(self.screen, (20, 25, 30), (SCREEN_WIDTH//2 - 250, 410, 500, 70), border_radius=15)
                pygame.draw.rect(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2 - 250, 410, 500, 70), 2, border_radius=15)
                
                # Curseur clignotant
                cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
                self.draw_text(self.input_ip + cursor, self.big_font, TEXT_COLOR, SCREEN_WIDTH//2, 445)
                
                if self.connect_status:
                    col = ACCENT_COLOR if "Connecté" in self.connect_status else ALERT_COLOR
                    self.draw_text(self.connect_status, self.font, col, SCREEN_WIDTH//2, 520)
                
                self.draw_text("Demandez l'IP Internet à l'hôte (ou utilisez Radmin/Hamachi)", self.font, (100, 100, 100), SCREEN_WIDTH//2, 650)

            elif self.state == "SETUP":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 50, 800, 750)
                self.draw_text_shadow("CONFIGURATION DE LA PARTIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                cx = SCREEN_WIDTH // 2
                y = 220
                gap = 100
                
                # 1. Joueurs
                if self.is_local_game:
                    self.draw_text("JOUEURS", self.font, (150,150,150), cx, y - 10)
                    self.draw_text(f"{self.settings['players']}", self.big_font, TEXT_COLOR, cx, y + 30)
                    y += gap
                else:
                    self.draw_text(f"JOUEURS : 2 (En ligne)", self.font, (150, 150, 150), cx, y + 25)
                    y += gap
                
                # 2. Mode
                mode_str = "ÉCRIT" if self.settings['mode'] == 'WRITTEN' else "VOCAL"
                self.draw_text("MODE DE JEU", self.font, (150,150,150), cx, y - 10)
                self.draw_text(mode_str, self.big_font, TEXT_COLOR, cx, y + 30)
                y += gap
                
                # 3. Catégorie
                self.draw_text("THÈME", self.font, (150,150,150), cx, y - 10)
                cat_font = self.medium_font if len(self.settings['category']) > 10 else self.big_font
                self.draw_text(self.settings['category'], cat_font, ACCENT_COLOR, cx, y + 30)
                y += gap
                
                # 4. Temps
                self.draw_text("TEMPS PAR TOUR", self.font, (150,150,150), cx, y - 10)
                self.draw_text(f"{self.settings['time']}s", self.big_font, TEXT_COLOR, cx, y + 30)
                y += gap

            elif self.state == "SETTINGS" or self.state == "CONTROLS":
                self.draw_panel(SCREEN_WIDTH//2 - 250, 200, 500, 500)
                title = "PARAMÈTRES" if self.state == "SETTINGS" else "TOUCHES"
                self.draw_text_shadow(title, self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 250)
                if self.state == "CONTROLS":
                    self.draw_text("Cliquez pour changer", self.font, (150, 150, 150), SCREEN_WIDTH//2, 350)

            elif self.state == "HOW_TO":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 150, 600, 300)
                self.draw_text_shadow("COMMENT JOUER", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                self.draw_text("1. Un mot du thème choisi s'affiche.", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 200)
                self.draw_text("2. Répondez vite ! (Chacun son tour à 3+ joueurs)", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 250)
                self.draw_text("3. Si le temps est écoulé, le joueur suivant gagne le point.", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 300)
                self.draw_text("4. Utilisez CONTESTER si le mot est mauvais.", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 350)
                contest_key_name = "MAJ" if self.keys["CONTEST"] == pygame.K_LSHIFT else "TAB"
                self.draw_text(f"TOUCHES : Entrée (Valider), {contest_key_name} (Contester)", self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 420)
            
            elif self.state.startswith("MENU"):
                # Titre stylisé pour les menus principaux
                self.draw_text("WORLD RUSH", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                self.draw_text("Association d'idées rapide", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 210)
            
            elif self.state.startswith("MENU"):
                # Titre stylisé pour les menus principaux
                self.draw_text("WORLD RUSH", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                self.draw_text("Association d'idées rapide", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 210)

            elif self.state == "LOBBY":
                # --- INTERFACE LOBBY ---
                self.draw_text_shadow("SALON D'ATTENTE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 60)
                
                # Zone Gauche : Joueurs
                left_panel = pygame.Rect(50, 120, 500, 500)
                self.draw_panel(left_panel.x, left_panel.y, left_panel.w, left_panel.h)
                self.draw_text("JOUEURS", self.font, ACCENT_COLOR, left_panel.centerx, left_panel.y + 30)
                
                # Joueur 1 (Moi ou Host)
                p1_color = (100, 255, 100) if self.ready_status[0] else (255, 100, 100)
                p1_status = "PRÊT" if self.ready_status[0] else "PAS PRÊT"
                p1_name = self.username if self.is_host or self.is_local_game else self.opponent_name
                if self.is_local_game: p1_name = "Joueur 1"
                self.draw_text(f"{p1_name} - {p1_status}", self.font, p1_color, left_panel.centerx, left_panel.y + 100)

                # Joueur 2
                p2_color = (100, 255, 100) if self.ready_status[1] else (255, 100, 100)
                p2_status = "PRÊT" if self.ready_status[1] else "PAS PRÊT"
                p2_name = self.opponent_name if self.is_host else self.username
                if self.is_local_game: p2_name = "Joueur 2"
                if self.test_mode: p2_name += " (BOT)"
                
                if not self.connected and not self.is_local_game and not self.test_mode:
                    p2_name = "En attente..."
                    p2_color = (150, 150, 150)
                    p2_status = "..."
                self.draw_text(f"{p2_name} - {p2_status}", self.font, p2_color, left_panel.centerx, left_panel.y + 160)

                # Infos IP (si Host)
                if self.is_host:
                    self.draw_text(f"IP Locale: {self.local_ip}", self.font, TEXT_COLOR, left_panel.centerx, left_panel.y + 300)
                    if self.public_ip:
                        self.draw_text(f"IP Internet: {self.public_ip}", self.font, ACCENT_COLOR, left_panel.centerx, left_panel.y + 340)
                    self.draw_text(f"UPnP: {self.upnp_status}", self.font, (150, 150, 150), left_panel.centerx, left_panel.y + 380)

                # Zone Droite : Chat
                chat_panel = pygame.Rect(570, 120, 660, 500)
                self.draw_panel(chat_panel.x, chat_panel.y, chat_panel.w, chat_panel.h)
                self.draw_text("CHAT", self.font, ACCENT_COLOR, chat_panel.centerx, chat_panel.y + 30)
                
                # Messages
                start_msg_y = chat_panel.y + 70
                for i, msg in enumerate(self.chat_messages[-10:]): # Affiche les 10 derniers
                    self.draw_text(msg, self.font, TEXT_COLOR, chat_panel.x + 20, start_msg_y + i * 30, center=False)
                
                # Input Chat
                pygame.draw.rect(self.screen, (20, 25, 35), (chat_panel.x + 20, chat_panel.bottom - 60, chat_panel.w - 40, 40), border_radius=10)
                self.draw_text(self.chat_input, self.font, TEXT_COLOR, chat_panel.x + 30, chat_panel.bottom - 55, center=False)

                # Bouton PRET
                ready_col = (100, 200, 100) if self.ready_status[self.my_id] else (200, 100, 100)
                ready_txt = "ANNULER" if self.ready_status[self.my_id] else "PRÊT !"
                
                # On dessine un bouton spécial pour le statut prêt
                ready_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 650, 200, 60)
                pygame.draw.rect(self.screen, ready_col, ready_btn_rect, border_radius=15)
                self.draw_text_shadow(ready_txt, self.font, (30, 30, 30), ready_btn_rect.centerx, ready_btn_rect.centery)
                
                # Gestion du clic sur le bouton PRET (zone manuelle car bouton dynamique)
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    if ready_btn_rect.collidepoint(mx, my):
                        # Petit debounce basique
                        if not hasattr(self, 'last_click') or pygame.time.get_ticks() - self.last_click > 300:
                            self.toggle_ready()
                            self.last_click = pygame.time.get_ticks()

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

            elif self.state == "OPPONENT_LEFT":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 200, 600, 400)
                self.draw_text_shadow("ADVERSAIRE PARTI", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 250)
                self.draw_text("Votre adversaire a quitté la partie.", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 350)

            elif self.state == "GAME_OVER":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 100, 600, 500)
                title = "VICTOIRE !" if self.winner_text == self.username else "DÉFAITE..."
                if self.is_local_game: title = "FIN DE PARTIE"
                
                color = ACCENT_COLOR if title == "VICTOIRE !" else ALERT_COLOR
                self.draw_text_shadow(title, self.big_font, color, SCREEN_WIDTH//2, 180)
                self.draw_text(f"Gagnant : {self.winner_text}", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 250)
                
                # Status rematch
                rematch_count = sum(self.rematch_ready)
                self.draw_text(f"Rejouer : {rematch_count}/{self.settings['players']}", self.font, (150, 150, 150), SCREEN_WIDTH//2, 450)

            elif self.state == "GAME":
                # Affichage HUD
                if self.is_local_game:
                    score_text = "   ".join([f"J{i+1}: {s}" for i, s in enumerate(self.score)])
                else:
                    # Afficher les pseudos en ligne
                    p1 = self.username if self.my_id == 0 else self.opponent_name
                    p2 = self.opponent_name if self.my_id == 0 else self.username
                    score_text = f"{p1}: {self.score[0]}   |   {p2}: {self.score[1]}"
                
                self.draw_text(score_text, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 30)
                
                turn_msg = f"Tour du Joueur {self.current_player + 1}" if self.is_local_game else ("C'est votre tour !" if self.current_player == self.my_id else "Tour de l'adversaire...")
                self.draw_text(turn_msg, self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 70)
                
                # Affichage Mot de l'adversaire (Haut Droite)
                self.draw_panel(SCREEN_WIDTH - 450, 20, 430, 120)
                self.draw_text("MOT PRÉCÉDENT :", self.font, (150, 150, 150), SCREEN_WIDTH - 235, 45)
                self.draw_text_shadow(f"{self.current_word}", self.big_font, ACCENT_COLOR, SCREEN_WIDTH - 235, 95)
                
                # Affichage Timer
                timer_color = ALERT_COLOR if self.time_left < 2 else TEXT_COLOR
                self.draw_text(f"{max(0, self.time_left):05.2f}", self.timer_font, timer_color, SCREEN_WIDTH//2, 250)
                
                # Barre de temps
                bar_width = 600
                bar_height = 30
                fill_width = max(0, (self.time_left / self.settings['time']) * bar_width)
                pygame.draw.rect(self.screen, (40, 40, 50), (SCREEN_WIDTH//2 - bar_width//2, 300, bar_width, bar_height), border_radius=15)
                pygame.draw.rect(self.screen, timer_color, (SCREEN_WIDTH//2 - bar_width//2, 300, fill_width, bar_height), border_radius=15)

                # Flash rouge si temps < 2s
                if 0 < self.time_left <= 2:
                    flash_s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    flash_s.fill(ALERT_COLOR)
                    alpha = int(40 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
                    flash_s.set_alpha(alpha)
                    self.screen.blit(flash_s, (0, 0))

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
                        display_text = "L'adversaire écrit..."
                    
                    # Correction alignement vertical (remonté de 410 à 408)
                    self.draw_text(display_text, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 408)
                    self.draw_text("Écrivez et appuyez sur ENTRÉE.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 500)
                
                # Spécifique Mode Vocal
                if self.settings['mode'] == "VOCAL":
                    self.draw_text_shadow("Parlez maintenant !", self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 400)
                    self.draw_text("ESPACE quand fini. 'A' pour contester.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 550)

            # Affichage des boutons (en dernier pour être au-dessus des panneaux)
            for btn in self.buttons:
                btn.draw(self.screen)

            # Copyright & Version
            self.draw_text("© dodosi", self.font, (80, 80, 90), SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30)
            self.draw_text("v0.1", self.font, (80, 80, 90), 40, SCREEN_HEIGHT - 30)

            # Indicateur Mode Développeur
            if self.test_mode:
                self.draw_text("DEV MODE", self.font, ALERT_COLOR, 80, 30)

            pygame.display.flip()
            self.clock.tick(60)

        self.remove_upnp()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
