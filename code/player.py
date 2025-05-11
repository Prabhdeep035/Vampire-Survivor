from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group,collision_sprites):
        super().__init__(group)
        self.image=pygame.image.load(join('images','player','down','0.png')).convert_alpha()
        self.rect=self.image.get_frect(center=(pos))
        self.hitbox_rect=self.rect.inflate(-60,-90)

        # movement
        self.direction=pygame.Vector2()
        self.speed=500
        self.frame_index=0
        self.collision_sprites=collision_sprites
     

    # def load_images(self): 
        self.down_frames=[pygame.image.load(join('images','player','down',f'{i}.png')).convert_alpha() for i in range(0,4)]
        self.up_frames=[pygame.image.load(join('images','player','up',f'{i}.png')).convert_alpha() for i in range(0,4)]
        self.left_frames=[pygame.image.load(join('images','player','left',f'{i}.png')).convert_alpha() for i in range(0,4)]
        self.right_frames=[pygame.image.load(join('images','player','right',f'{i}.png')).convert_alpha() for i in range(0,4)]

    def input(self):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_RIGHT] or keys[pygame.K_d])-int(keys[pygame.K_LEFT]or keys[pygame.K_a]) 
        self.direction.y=int(keys[pygame.K_DOWN] or keys[pygame.K_s])-int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction=self.direction.normalize() if self.direction else self.direction

    def move(self,dt):
        self.hitbox_rect.x+=self.direction.x*self.speed*dt
        self.collision('horizontal')
        self.hitbox_rect.y+=self.direction.y*self.speed*dt
        self.collision('vertical')
        self.rect.center=self.hitbox_rect.center

    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction=='horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else :
                    if self.direction.y > 0: self.hitbox_rect.bottom=sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top=sprite.rect.bottom
                    

    def update(self,dt):
        self.input()
        self.move(dt)
        keys=pygame.key.get_pressed()
        if  int(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.image=self.right_frames[int(self.frame_index)%4]
            self.frame_index+=10*dt
        
        if  int(keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.image=self.left_frames[int(self.frame_index)%4]
            self.frame_index+=10*dt

        if  int(keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.image=self.down_frames[int(self.frame_index)%4]
            self.frame_index+=10*dt

        if  int(keys[pygame.K_UP] or keys[pygame.K_w]):
            self.image=self.up_frames[int(self.frame_index)%4]
            self.frame_index+=10*dt
