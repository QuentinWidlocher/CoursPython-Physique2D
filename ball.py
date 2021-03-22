from pygame.constants import K_LEFT, K_RIGHT, K_SPACE
from box import Box
from pygame.rect import Rect
from constants import G, WHITE
from pygame import Vector2, draw, key

class Ball():

    # On crée toutes les valeurs
    def __init__(self):
        self.diameter = 15
        self.pos = Vector2(400, self.diameter)

        # L'accélération de la balle à chaque frame. Cette valeur est mise à jour par toutes
        # les autres et c'est elle qui défini où sera la futur position de la balle
        self.acc = Vector2(0,0)

        # Diviseur de force dû au rebond. Quand une balle touche le sol elle rebondit avec
        # la même force, divisé par ce nombre. (1 = même hauteur, 2 = 2x moins haut, 0.5 = 2x plus haut)
        self.bounciness= 1.8

        # La balle est au sol O/N
        self.grounded = False

        # La vitesse d'accélération latérale de la balle
        self.x_acc = 0.002

        # La vitesse de décélération latérale de la balle
        self.x_dec = 0.001

        # La vitesse latérale maximale de la balle
        self.max_speed = 0.4

        # La force du saut d'une balle
        self.jump_force = -1.5

    def init(self, screen):
        return

    def update(self, screen, boxes):

        # On récupère la boite qui est en colision avec la balle ou None
        collider: Box = self.collision(boxes)

        if (collider != None):

            # S'il y a une collision, on pose la balle juste au dessus de la boite
            self.pos.y = collider.pos.y - self.diameter + 1

            # On crée un rebond en inversant l'accélération de la balle
            # On divise par le quotient de rebond et on met un seuil pour éviter
            # que la balle rebondisse à l'infini (passé 0.1 on arrête)
            self.acc.y = - (self.acc.y/self.bounciness) if self.acc.y > 0.1 else 0

            # On indique qu'on a touché le sol
            self.grounded = True
        else:
            # Sinon, on est dans les airs, donc on ajoute la gravité à l'accélération
            self.acc.y += G
            # et on indique qu'on est pas au sol
            self.grounded = False

        # On ne peut sauter que lorsqu'on est au sol
        if (self.grounded and key.get_pressed()[K_SPACE]):
            # On met brutalement l'accélération à la force de saut, ce qui la propulse
            # dans les airs
            self.acc.y = self.jump_force

        # On regarde le joueur se déplace
        if (key.get_pressed()[K_LEFT]):

            # S'il se déplace à gauche on accélère à la vitesse -x_acc
            self.acc.x -= self.x_acc

            # et s'il dépasse -max_speed, on cap à -max_speed
            self.acc.x = max(self.acc.x, -self.max_speed)
        elif (key.get_pressed()[K_RIGHT]):

            # S'il se déplace à droite on accélère à la vitesse x_acc
            self.acc.x += self.x_acc

            # et s'il dépasse max_speed, on cap à max_speed
            self.acc.x = min(self.acc.x, self.max_speed)
        else:

            # Si le joueur ne se déplace plus, il faut décélérer (tendre vers 0)
            # Si on est à plusieurs fois x_dec de 0, on se rapproche de 0 dans le
            # bon sens
            if (self.acc.x < -self.x_dec):
                self.acc.x += self.x_dec
            elif (self.acc.x > self.x_dec):
                self.acc.x -= self.x_dec
            else:
                # Sinon, si on est à x_dec de 0, on met directement à 0 pour stopper
                # la balle, sinon elle accélère et décélère en bouche
                self.acc.x = 0

        # Avec tous ces calculs, on change la position de la balle
        self.pos += self.acc

        # Et on la dessine
        draw.circle(screen, WHITE, self.pos + Vector2(self.diameter/2), self.diameter/2)

    def collision(self, boxes):
        boxes_as_rect = []
        b: Box
        for b in boxes:
            # Pour chaque boite, on stocke sa valeur en temps que Rect()
            boxes_as_rect.append(b.as_rect())

        # On utilise la fonction collidelist de PyGame pour trouver une collision
        collision_index = self.as_rect().collidelist(boxes_as_rect)
        is_colliding = collision_index >= 0

        # S'il y a une collision on renvoi la boite, sinon None
        return boxes[collision_index] if is_colliding else None

    def as_rect(self):
        return Rect(self.pos, (self.diameter, self.diameter))
