from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint,choice

class Game():
    def __init__(self):

        # init 
        pygame.init()
        self.pos=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.clock=pygame.time.Clock()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.running=True
        self.load_image()
        self.score=0
        
        # groups
        # self.all_sprites=pygame.sprite.Group()
        self.all_sprites= AllSprites()#in order to change the camera and see the objects which are not vsible on the screen 
        self.collision_sprites=pygame.sprite.Group()
        self.bullet_sprites=pygame.sprite.Group()
        self.enemy_sprites=pygame.sprite.Group()


        # sprites
        # self.player=Player(self.pos,self.all_sprites,self.collision_sprites)
        # for i in range(6):
        #     x,y=randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)
        #     w,h=randint(60,100),randint(50,100)
        #     CollisionSprite((x,y),(w,h),(self.all_sprites,self.collision_sprites))
        
        self.can_shoot=True
        self.shoot_time=0
        self.gun_cooldown=20

        # enemy timer 
        self.enemy_event=pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,1000)
        self.spawn_positions=[]

        # audio
        self.game_music=pygame.mixer.Sound(join('audio','music.wav'))
        self.game_music.set_volume(0.4)
        self.shoot_music=pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_music.set_volume(0.4)
        self.impact_music=pygame.mixer.Sound(join('audio','impact.ogg'))
        self.impact_music.set_volume(0.4)
    
        self.game_music.play(loops=-1)
        self.setup()

    def load_image(self):
            self.bullet_surf=pygame.image.load(join('images','gun','bullet.png')).convert_alpha()

            folders= list(walk(join('images','enemies')))[0][1]
            self.enemy_frames={}
            for folder in folders:
                for folder_path,_,file_names in walk(join('images','enemies',folder)):
                    self.enemy_frames[folder]= []
                    for file_name in sorted(file_names,key=lambda name:int(name.split('.')[0])):
                        full_path=join(folder_path,file_name)
                        surf=pygame.image.load(full_path).convert_alpha()
                        self.enemy_frames[folder].append(surf)

    def input(self):
         if pygame.mouse.get_just_pressed()[0] and self.can_shoot:
            self.shoot_music.play()
            pos=self.gun.rect.center +self.gun.player_direction*50
            Bullet(self.bullet_surf,pos,self.gun.player_direction,(self.all_sprites,self.bullet_sprites))    
            self.can_shoot=True
            self.shoot_time=pygame.time.get_ticks()

    def setup(self):
        map=load_pygame(join('data','maps','world.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name=='Player':
                self.player=Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
                self.gun=Gun(self.player,self.all_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))
           
    def collisions(self):
        collisionPE=pygame.sprite.spritecollide(self.player,self.enemy_sprites,True,pygame.sprite.collide_mask)
        if collisionPE:
            self.running=False
        
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites=pygame.sprite.spritecollide(bullet,self.enemy_sprites,False,pygame.sprite.collide_mask)
                if collision_sprites:
                    self.score+=1
                    self.display_score()
                    self.impact_music.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def display_score(self):
        self.font=pygame.font.SysFont(None,50)
        self.score_surf=self.font.render(str(self.score),True,('black'))
        self.rect=self.score_surf.get_frect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
        self.display_surface.blit(self.score_surf, self.rect)
        pygame.draw.rect(self.display_surface,'black',self.rect.inflate(30,30).move(0,-10),10,10)

    def run(self):
        while(self.running):
            self.dt=self.clock.tick()/1000

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running= False
                if event.type==self.enemy_event:
                    Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites)

            self.input()
            self.all_sprites.update(self.dt)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.collisions()
            
            self.display_score()

            pygame.display.update()
        pygame.quit()

if __name__=='__main__':
    game=Game()
    game.run()



    