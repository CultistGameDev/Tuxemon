import pygame
from core import prepare
from core.components.menu import Menu

# Import the android mixer if on the android platform
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

class InteractionMenu(Menu):

    def __init__(self, screen, resolution, game, name="Interaction Menu"):

        # Initialize the parent menu class's default shit
        Menu.__init__(self, screen, resolution, game, name)
        self.first_run = True
        self.save = False
        self.state = "closed"
        self.visible = False
        
        self.menu_select_sound = mixer.Sound(
            prepare.BASEDIR + "resources/sounds/interface/50561__broumbroum__sf3-sfx-menu-select.ogg")


    def get_event(self, event, game=None):

        if len(self.menu_items) > 0:
            self.line_spacing = (self.size_y / len(self.menu_items)) - self.font_size

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.selected_menu_item += 1
            if self.selected_menu_item > len(self.menu_items) -1:
                self.selected_menu_item = 0

            self.menu_select_sound.play()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.selected_menu_item -= 1
            if self.selected_menu_item < 0:
                self.selected_menu_item = len(self.menu_items) -1

            self.menu_select_sound.play()

        # If the player presses Enter while a menu item is selected
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.menu_select_sound.play()

            if self.menu_items[self.selected_menu_item] == "DUEL":
                if self.game.game.isclient:
                    self.game.game.client.player_interact(self.player, "DUEL")
                    pass
                elif self.game.game.ishost:
                    client = None
                    cuuid = str(self.game.client.client.cuuid)
                    for client_id in self.game.server.server.registry:
                        if self.player == self.game.server.server.registry[client_id]["sprite"]:
                            client = client_id 
                    
                    event_data = {"type": "CLIENT_INTERACTION",
                                  "interaction": "DUEL",
                                  "target": client,
                                  }
                    self.game.game.server.notify_client_interaction(cuuid, event_data)
                    
            elif self.menu_items[self.selected_menu_item] == "TRADE":
                self.game.not_implmeneted_menu.visible = True
                self.game.not_implmeneted_menu.interactable = True
            


