import arcade
from arcade import Camera2D
from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, PLAYER_JUMP,PLAYER_MAX_LIFE
from config import PLAYER_SPEED,GRAVITY, MAP_NAME_STAGE_1,MAP_NAME_STAGE_2, GameState

class Gameplay(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        
        self.camera=Camera2D(zoom=2)
        self.gui_camera=Camera2D()

        self.scene=None
        self.player_sprite=None
        self.physics_engine=None
        self.score=0
        self.floating_text_list=None
        self.items=None
        self.enemies=None
        self.enemy_shooters_right=None
        self.enemy_shooters_left=None
        self.enemy_shooters_up=None
        self.enemy_shooters_down=None
        self.enemy_projectiles=None
        self.mpvertical=None
        self.mphorizontal=None
        self.timer=0
        self.shoot_interval=2
        self.spikes=None
        self.bomb=None
        self.trampoline=None
        self.next_stage_hitbox=None
        self.checkpoint=None
        self.checkpoint_x=None
        self.checkpoint_y=None
        self.portal=None
        self.portal_lookup = {}
        self.teleport_cooldown=0
        self.door=None
        self.key=None
        self.key_collected=False
        self.player_walk_textures=[]
        self.player_animation_timer=0.0
        self.player_animation_frame=0
        self.lifereg=None

        self.life=PLAYER_MAX_LIFE
        self.current_map_name = MAP_NAME_STAGE_1

        sound=':resources:sounds'
        self.collect_coin_sound=arcade.load_sound(sound+'/coin5.wav')
        self.explosion_sound=arcade.load_sound(sound+'/explosion1.wav')
        self.respawn_sound=arcade.load_sound(sound+'/hurt5.wav')
        self.jump_sound=arcade.load_sound(sound+'/jump5.wav')
        self.gameover_sound=arcade.load_sound(sound+'/gameover4.wav')
        self.lock_sound=arcade.load_sound(sound+'/error3.wav')
        self.unlock_sound=arcade.load_sound(sound+'/upgrade2.wav')
        self.regen_sound=arcade.load_sound(sound+'/upgrade2.wav')

    def load_player_walk_textures(self):
        print('Player walk texture loaded')
        self.player_walk_textures=[]
        for frame in range(8):
            texture_path=f':resources:/images/animated_characters/male_person/malePerson_walk{frame}.png'
            self.player_walk_textures.append(arcade.load_texture(texture_path))

        if self.player_walk_textures:
            self.player_sprite.textures=self.player_walk_textures
            self.player_sprite.texture=self.player_walk_textures[0]
            self.player_sprite.cur_texture_index=0
            self.player_sprite.scale=0.175
            self.player_sprite.scale_x=0.175
            self.player_sprite.scale_y=0.175

    def setup(self):
        print("lololololol")
        tile_map=arcade.load_tilemap(self.current_map_name,scaling=1,use_spatial_hash=True)
        self.scene=arcade.Scene.from_tilemap(tile_map)

        self.player_sprite=arcade.Sprite(':resources:/images/animated_characters/male_person/malePerson_idle.png',0.175)
        self.load_player_walk_textures()

        self.player_sprite.center_x=100
        self.player_sprite.center_y=100
        self.scene.add_sprite('Player',self.player_sprite)

        player_spawn=self.scene['spawnlocation'][0]
        self.player_sprite.center_x=player_spawn.center_x
        self.player_sprite.center_y=player_spawn.center_y
        self.player_spawn_x=self.player_sprite.center_x
        self.player_spawn_y=self.player_sprite.center_y
        self.checkpoint_x=self.player_spawn_x
        self.checkpoint_y=self.player_spawn_y

        self.floating_text_list=arcade.SpriteList()

        self.enemies=self.scene['Enemies'] if 'Enemies' in self.scene else arcade.SpriteList(
        )
        self.items=self.scene['Item'] if 'Item' in self.scene else arcade.SpriteList(
        )
        self.enemy_shooters_left=self.scene['shootingenemyleft'] if 'shootingenemyleft' in self.scene else arcade.SpriteList(
        )
        self.enemy_shooters_right=self.scene['shootingenemyright'] if 'shootingenemyright' in self.scene else arcade.SpriteList(
        )
        self.enemy_shooters_up=self.scene['shootingenemyup'] if 'shootingenemydown' in self.scene else arcade.SpriteList(
        )
        self.enemy_shooters_down=self.scene['shootingenemydown'] if 'shootingenemyup' in self.scene else arcade.SpriteList(
        )
        self.enemy_projectiles=arcade.SpriteList()
        self.spikes=self.scene["Spikes"]if 'Spikes' in self.scene else arcade.SpriteList(
        )
        self.bomb=self.scene["Bombs"]if 'Bombs' in self.scene else arcade.SpriteList(
        )
        self.trampoline=self.scene['trampoline']if 'trampoline' in self.scene else arcade.SpriteList(
        )
        self.flying_enemies=self.scene['Flying enemies']if 'Flying enemies' in self.scene else arcade.SpriteList(
        )
        self.checkpoint=self.scene['Checkpoints']if 'Checkpoints' in self.scene else arcade.SpriteList(
        )
        self.next_stage_hitbox=self.scene['nextstage'] if 'nextstage' in self.scene else arcade.SpriteList(
        )
        self.mpvertical=self.scene['mpvertical'] if 'mpvertical' in self.scene else arcade.SpriteList(
        )
        self.mphorizontal=self.scene['mphorizontal'] if 'mphorizontal' in self.scene else arcade.SpriteList(
        )
        self.portal=self.scene['portal'] if 'portal' in self.scene else arcade.SpriteList(
        )
        self.door=self.scene['door'] if 'door' in self.scene else arcade.SpriteList(
        )
        self.key=self.scene['key'] if 'key' in self.scene else arcade.SpriteList(
        )
        self.lifereg=self.scene['lifereg']

        for portal_sprite in self.portal:
            pid=portal_sprite.properties.get('portal_id')
            if pid is not None:
                self.portal_lookup[pid]=portal_sprite

        platforms=arcade.SpriteList()
        platforms.extend(self.mpvertical)
        platforms.extend(self.mphorizontal)

        self.physics_engine=arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene['Ground'],
            gravity_constant=GRAVITY,
            platforms=platforms,
        )
        
        self.score=0

        for shooter in self.enemy_shooters_left:
            shooter.direction= -1
            shooter.timer=1

        for shooter in self.enemy_shooters_right:
            shooter.direction=1
            shooter.timer=1

        for shooter in self.enemy_shooters_down:
            shooter.direction= -.5
            shooter.timer=1

        for shooter in self.enemy_shooters_up:
            shooter.direction=.5
            shooter.timer=1

        self.walking_enemy_speed=2
        for enemy in self.enemies:
            enemy.change_x=self.walking_enemy_speed
            enemy.direction=1

        self.flying_enemies_speed=2
        for enemy in self.flying_enemies:
            enemy.change_x=self.flying_enemies_speed
            enemy.direction=1

        for platform in self.mpvertical:
            platform.change_y=3
            platform.boundary_down=platform.center_y -100
            platform.boundary_up=platform.center_y +100

        for platform in self.mphorizontal:
            platform.change_x=3
            platform.boundary_left=platform.center_x -100
            platform.boundary_right=platform.center_x +100

    def on_draw(self):
            self.clear()
            self.camera.use()
            self.scene.draw()
            self.enemy_projectiles.draw()
            self.floating_text_list.draw()
            self.gui_camera.use()
            arcade.draw_text(f"Score: {self.score}",10,SCREEN_HEIGHT - 40, arcade.color.WHITE,20)
            arcade.draw_text(f"Life: {self.life}",10,SCREEN_HEIGHT - 70, arcade.color.WHITE,20)
            arcade.draw_text("A/D to walk, SPACE to jump", 10, SCREEN_HEIGHT - 100, arcade.color.WHITE,14)

    def on_update(self, delta_time:float):
    
            self.physics_engine.update()
            self.scene.update_animation(delta_time)
            self.center_camera()
    
            self.floating_text_list.update()
            for sprite in self.floating_text_list:
                sprite.change_y*=0.95
                sprite.alpha-=5
                if sprite.alpha<=0:
                    sprite.remove_from_sprite_lists()
    
            if self.player_walk_textures:
                if abs(self.player_sprite.change_x)>0.1 and abs(self.player_sprite.change_y) == 0:
                    self.player_animation_timer+=delta_time
                    if self.player_animation_timer>=0.08:
                        self.player_animation_timer=0.0
                        self.player_animation_frame=(
                            self.player_animation_frame+1
                        ) % len(self.player_walk_textures)
                        self.player_sprite.texture=self.player_walk_textures[self.player_animation_frame]
    
                    if self.player_sprite.change_x<0:
                        self.player_sprite.scale_x=-abs(self.player_sprite.scale_x)
                    else:
                        self.player_sprite.scale_x=abs(
                            self.player_sprite.scale_x)
                else:
                    self.player_animation_timer=0.0
                    self.player_animation_frame=0
                    # self.player_sprite.texture=arcade.load_texture(
                    #     ':resources:/images/animated_characters/male_person/malePerson_idle.png'
                    # )        
                    if (self.player_sprite.change_y>0):
                        self.player_sprite.texture = arcade.load_texture(
                            ':resources:/images/animated_characters/male_person/malePerson_jump.png'
                        )
                    elif (self.player_sprite.change_y<0):
                        self.player_sprite.texture=arcade.load_texture(
                            ':resources:/images/animated_characters/male_person/malePerson_fall.png'
                        )
                    else:
                        self.player_sprite.texture=arcade.load_texture(
                            ':resources:/images/animated_characters/male_person/malePerson_idle.png'
                        )
    
            if self.teleport_cooldown>0:
                self.teleport_cooldown-=delta_time
    
            next_stage_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.next_stage_hitbox)
            if next_stage_hit_list:
                for trigger in next_stage_hit_list:
                    trigger.remove_from_sprite_lists()
                    self.next_stage()
    
            checkpoint_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.checkpoint)
            for checkpoint in checkpoint_hit_list:
                self.checkpoint_x=checkpoint.center_x
                self.checkpoint_y=checkpoint.center_y
                checkpoint.remove_from_sprite_lists()
    
            enemy_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.enemies)
            if enemy_hit_list:
                self.respawn()
    
            enemy_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.flying_enemies)
            if enemy_hit_list:
                self.respawn()
    
            for enemy in self.enemies:
                enemy.center_x+=enemy.change_x
                if arcade.check_for_collision_with_list(enemy,self.scene['Ground']):
                    enemy.change_x*=-1
                    enemy.center_x+=enemy.change_x
                    enemy.direction*=-1
                    if (enemy.direction==-1):
                        enemy.scale_x=-abs(enemy.scale_x)
                    else:
                        enemy.scale_x=abs(enemy.scale_x)
    
            for enemy in self.flying_enemies:
                enemy.center_x+=enemy.change_x
                if arcade.check_for_collision_with_list(enemy,self.scene['Ground']):
                    enemy.change_x*=-1
                    enemy.center_x+=enemy.change_x
                    enemy.direction*=-1
                    if (enemy.direction==-1):
                        enemy.scale_x=-abs(enemy.scale_x)
                    else:
                        enemy.scale_x=abs(enemy.scale_x)
    
            for platform in self.mpvertical:
                platform.center_y+=platform.change_y
                if platform.center_y>platform.boundary_up:
                    platform.change_y*=-1
                elif platform.center_y<platform.boundary_down:
                    platform.change_y*=-1
    
            for platform in self.mphorizontal:
                platform.center_x+=platform.change_x
                if platform.center_x>platform.boundary_right:
                    platform.change_x*=-1
                elif platform.center_x<platform.boundary_left:
                    platform.change_x*=-1
    
            portal_hit_list=arcade.check_for_collision_with_list(
                self.player_sprite,self.portal
            )
            if portal_hit_list and self.teleport_cooldown<=0:
                portal_hit=portal_hit_list[0]
                target_id=portal_hit.properties.get('portal_target')
    
                target_portal=self.portal_lookup.get(target_id)
                if target_portal:
                    self.player_sprite.center_x=target_portal.center_x
                    self.player_sprite.center_y=target_portal.center_y
                    self.teleport_cooldown=1
    
            for item in arcade.check_for_collision_with_list(self.player_sprite,self.items):
                item.remove_from_sprite_lists()
                self.score+=1
                arcade.play_sound(self.collect_coin_sound)
    
            for Bombs in arcade.check_for_collision_with_list(self.player_sprite,self.bomb):
                Bombs.remove_from_sprite_lists()
                arcade.play_sound(self.explosion_sound)
                self.score = max(0,self.score-1)
    
            trampoline_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.trampoline)
            if trampoline_hit_list:
                self.player_sprite.change_y+=20
    
            if self.player_sprite.center_y<=-1:
                self.respawn()
    
            for shooter in self.enemy_shooters_left:
                shooter.timer += delta_time
                if shooter.timer>=self.shoot_interval:
                    shooter.timer=0
    
                    bullet = arcade.SpriteSolidColor(10,4,color=arcade.color.RED_DEVIL)
                    bullet.center_x=shooter.center_x
                    bullet.center_y=shooter.center_y
                    bullet.change_x=5*shooter.direction
                    self.enemy_projectiles.append(bullet)
    
            for shooter in self.enemy_shooters_right:
                shooter.timer += delta_time
                if shooter.timer>=self.shoot_interval:
                    shooter.timer=0
    
                    bullet = arcade.SpriteSolidColor(10,4,color=arcade.color.RED_DEVIL)
                    bullet.center_x=shooter.center_x
                    bullet.center_y=shooter.center_y
                    bullet.change_x=5*shooter.direction
                    self.enemy_projectiles.append(bullet)
    
            for shooter in self.enemy_shooters_down:
                shooter.timer += delta_time
                if shooter.timer>=self.shoot_interval:
                    shooter.timer=0
    
                    bullet = arcade.SpriteSolidColor(4,10,color=arcade.color.RED_DEVIL)
                    bullet.center_x=shooter.center_x
                    bullet.center_y=shooter.center_y
                    bullet.change_y=5*shooter.direction
                    self.enemy_projectiles.append(bullet)
    
            for shooter in self.enemy_shooters_up:
                shooter.timer += delta_time
                if shooter.timer>=self.shoot_interval:
                    shooter.timer=0
    
                    bullet = arcade.SpriteSolidColor(4,10,color=arcade.color.RED_DEVIL)
                    bullet.center_x=shooter.center_x
                    bullet.center_y=shooter.center_y
                    bullet.change_y=5*shooter.direction
                    self.enemy_projectiles.append(bullet)
    
    
            for bullet in self.enemy_projectiles:
                hit_ground=arcade.check_for_collision_with_list(bullet,self.scene["Ground"])
                if hit_ground:
                    bullet.remove_from_sprite_lists()
            
            self.enemy_projectiles.update()
    
            for bullet in self.enemy_projectiles:
                if bullet.right < 0 or bullet.left > SCREEN_WIDTH*3:
                    bullet.remove_from_sprite_lists()
    
            hit_bullets = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_projectiles)
            for bullet in hit_bullets:
                bullet.remove_from_sprite_lists()
                self.respawn()
    
            spike_hit_list=arcade.check_for_collision_with_list(self.player_sprite,self.spikes)
            if spike_hit_list:
                self.respawn()
    
            key_hit=arcade.check_for_collision_with_list(
                self.player_sprite,self.key)
            for key in key_hit:
                key.remove_from_sprite_lists()
                self.key_collected=True
    
            door_hit=arcade.check_for_collision_with_list(
                self.player_sprite,self.door)
    
            if door_hit:
                if self.key_collected:
                    for door in door_hit:
                        door.remove_from_sprite_lists()
                        arcade.play_sound(self.unlock_sound)
                        self.key_collected=False
                else:
                    self.respawn()
                    arcade.play_sound(self.lock_sound)
    
            heart_hit_List=arcade.check_for_collision_with_list(self.player_sprite,self.lifereg)
            if heart_hit_List:
                self.life+=1
                for heart in heart_hit_List:
                    text_sprite=arcade.create_text_sprite("+1",color=arcade.color.RED_DEVIL,font_size=16,bold=True)
                    text_sprite.center_x=heart.center_x
                    text_sprite.center_y=heart.center_y
                    text_sprite.change_y=3.5
                    self.floating_text_list.append(text_sprite)
    
                    heart.remove_from_sprite_lists()
                arcade.play_sound(self.regen_sound)
    

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
        return super().on_show_view()

    def center_camera(self):
            target_x=self.player_sprite.center_x
            target_y=self.player_sprite.center_y
            can_x=arcade.math.lerp(self.camera.position[0],target_x,0.1)
            can_y=arcade.math.lerp(self.camera.position[1],target_y,0.1)
            self.camera.position = (can_x,can_y)

    def respawn(self):
            print('respawning...')
            self.player_sprite.center_x=self.player_spawn_x
            self.player_sprite.center_y=self.player_spawn_y
            self.player_sprite.change_x=0
            self.player_sprite.change_y=0
    
            arcade.play_sound(self.respawn_sound)
    
            self.life -= 1
            if self.life <= 0:
                from gameoverscreen import Gameoverscreen
                view=Gameoverscreen()
                self.window.show_view(view)
                print("Game Over!")
                arcade.play_sound(self.gameover_sound)
            else:
                print(f"Remaining lives: {self.life}")
                self.player_sprite.center_x=self.checkpoint_x
                self.player_sprite.center_y=self.checkpoint_y
                self.player_sprite.change_x=0
                self.player_sprite.change_y=0

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y=PLAYER_JUMP
                arcade.play_sound(self.jump_sound)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x=-PLAYER_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x=PLAYER_SPEED

    def on_key_release(self, key, modifiers):
            if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
                self.player_sprite.change_x = 0

    def next_stage(self):
            if self.current_map_name==MAP_NAME_STAGE_2:
                from finishscreen import Gameoverscreen
                self.window.show_view(Gameoverscreen())
            else:
                self.current_map_name=MAP_NAME_STAGE_2
                self.setup()