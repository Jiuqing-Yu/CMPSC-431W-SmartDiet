import pygame
from Default import *
from connection import *
class DisplayBox:
    def __init__(self, center_x, y, width, height, initial_text="",font_size=24):
        self.font = pygame.font.Font("quaver.ttf", font_size)
        self.templete = pygame.Surface((width, height)) 
        self.templete.fill(BLACK)  
        self.rect = self.templete.get_rect()
        self.rect.centerx = center_x
        self.center_x = center_x
        self.rect.top = y
        self.width = width
        self.height = height

        self.color = WHITE  
        self.text = initial_text

    def set_text(self, new_text):
        self.text = new_text

    def draw(self, surface, padding=5):
        self.templete.fill(BLACK)
        lines = self.text.split('\n')  
        x_start = padding
        y = padding
        max_width = self.width - 2 * padding
        line_height = self.font.get_height()
        space_width, _ = self.font.size(' ')

        for line in lines:
            words = line.split(' ')
            x = x_start
            for word in words:
                word_surface = self.font.render(word, True, WHITE)
                word_width = word_surface.get_width()

                # Word wrapping if exceeds box width
                if x + word_width > max_width:
                    x = x_start
                    y += line_height
                if y + line_height > self.height - padding:
                    break
                self.templete.blit(word_surface, (x, y))
                x += word_width + space_width

            # Move to next line after \n
            y += line_height
            if y + line_height > self.height - padding:
                break

        surface.blit(self.templete, self.rect.topleft)
        pygame.draw.rect(surface, self.color, self.rect, 2)

class TextInputBox:
    def __init__(self, center_x, y, w, h, name="",font_size = 24):
        self.font = pygame.font.Font("quaver.ttf", font_size)
        self.name_font = pygame.font.Font("quaver.ttf", font_size+6)
        self.name = name
        self.name_surface = self.name_font.render(self.name + ":", True, WHITE)

        self.input_width = w
        self.input_height = h
        self.center_x = center_x
        self.y = y  
        self.placeholder = "Input Text Here"

        self.color_inactive = BLACK
        self.color_active = WHITE
        self.color = self.color_inactive

        self.text = ""
        self.active = False

        self.input_rect = pygame.Rect(0, 0, w, h)
        self.rect = pygame.Rect(0, 0, self.name_surface.get_width() + 10 + w, h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"{self.name} entered:", self.text)
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text)<= 18:
                    self.text += event.unicode

    def draw(self, surface):
        total_width = self.name_surface.get_width() + 10 + self.input_width
        start_x = self.center_x - total_width // 2
        self.rect.topleft = (start_x, self.y)
        self.input_rect.topleft = (start_x + self.name_surface.get_width() + 10, self.y)
        surface.blit(self.name_surface, (self.rect.x, self.rect.y + (self.rect.height - self.name_surface.get_height()) // 2))
        
        display_text = self.text if self.text or self.active else self.placeholder
        text_color = WHITE if self.text else GRAY
        text_surface = self.font.render(display_text, True, text_color)
        text_x = self.input_rect.x + 10
        text_y = self.input_rect.y + (self.input_rect.height - text_surface.get_height()) // 2
        surface.blit(text_surface, (text_x, text_y))

        pygame.draw.rect(surface, self.color, self.input_rect, 2)


        if self.active:
            cursor_visible = pygame.time.get_ticks() % 1000 < 500 
            if cursor_visible:
                cursor_x = text_x + text_surface.get_width() + 2
                cursor_y = text_y
                cursor_height = text_surface.get_height()
                pygame.draw.line(surface, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
class Button:
    def __init__(self, text, x, y, callback,fontsize =48):
        self.text = text
        self.active = True
        self.base_font_size = fontsize
        self.font = pygame.font.Font("quaver.ttf", self.base_font_size)
        self.rect = self.font.render(self.text, True, GRAY).get_rect()
        self.rect.center = (x,y)
        self.callback = callback
        self.hover_scale = 1 

    def draw(self, surface):
        if not self.active:
            return
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        text_color = GRAY if hovered else WHITE
        font_size = int(self.base_font_size * self.hover_scale) if hovered else self.base_font_size
        font = pygame.font.Font("quaver.ttf", font_size)
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class LoginPage:
    def __init__(self, surface,connection):
        self.surface = surface
        self.connection = connection
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        
        self.username_input = TextInputBox(WIDTH//2, HEIGHT//2 - 0, 300, 50, "UserId")
        self.password_input = TextInputBox(WIDTH//2, HEIGHT//2 + 60, 300, 50, "Password")
        self.login_button = Button("Login", WIDTH // 2, HEIGHT // 2 + 220,self.login)
        self.back_button = Button("Back", 100, 50, self.back)
        self.display_box = DisplayBox( WIDTH // 2 , HEIGHT // 2 + 120, 500, 50)
        self.display_box.set_text(' ')
        self.page = self
    def handle_event(self, event):
        self.username_input.handle_event(event)
        self.password_input.handle_event(event)
        self.login_button.handle_event(event)
        self.back_button.handle_event(event)
        return self.page
    def login(self):
        userid = self.username_input.text
        pw = self.password_input.text
        if not user_exist(self.connection, userid):
            self.display_box.set_text(f'Username {userid} does not exist')
        elif not user_pw_correct(self.connection, userid,hash_password(pw)):
            self.display_box.set_text(f'Password is not correct')
        else:
            self.page = FoodAvoidPage(self.connection, self.surface,userid)
    def back(self):
        self.page = HomePage(self.surface,self.connection)
    def draw(self):
        self.surface.fill(BLACK)
        title = self.title_font.render("Login Page", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.surface.blit(title, title_rect)

        self.username_input.draw(self.surface)
        self.password_input.draw(self.surface)
        self.login_button.draw(self.surface)
        self.back_button.draw(self.surface)
        self.display_box.draw(self.surface)
class RegisterPage:
    def __init__(self, surface,connection):
        self.surface = surface
        self.connection = connection
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.username_input = TextInputBox(WIDTH//2, HEIGHT//2 -220, 300, 50, "UserId")
        self.password_input = TextInputBox(WIDTH//2, HEIGHT//2 -170, 300, 50, "Password")
        self.gender_input = TextInputBox(WIDTH//2, HEIGHT//2 -120, 300, 50, "Gender")
        self.age_input = TextInputBox(WIDTH//2, HEIGHT//2 -70, 300, 50, "Age")
        self.weight_input = TextInputBox(WIDTH//2, HEIGHT//2-20, 300, 50, "Weight(lbs)")
        self.height_input = TextInputBox(WIDTH//2, HEIGHT//2 +20, 300, 50, "Height(fts)")
        self.vagen_input = TextInputBox(WIDTH//2, HEIGHT//2 +70, 300, 50, "Vegetarian?")
        self.display_box = DisplayBox( WIDTH // 2 , HEIGHT // 2 + 120, 500, 40)
        self.display_box.set_text('')
        self.register_button = Button("Register", WIDTH // 2 , HEIGHT // 2 + 220, self.register)
        self.back_button = Button("Back", 100, 50, self.back)
        
        self.page = self

    def handle_event(self, event):
        self.username_input.handle_event(event)
        self.password_input.handle_event(event)
        self.gender_input.handle_event(event)
        self.age_input.handle_event(event)
        self.height_input.handle_event(event)
        self.weight_input.handle_event(event)
        self.vagen_input.handle_event(event)
        self.register_button.handle_event(event)
        self.back_button.handle_event(event)
        return self.page
    def register(self):
        userid = self.username_input.text
        pw= self.password_input.text
        gender = self.gender_input.text
        age = self.age_input.text
        height = self.height_input.text
        weight = self.weight_input.text
        vagan = self.vagen_input.text
        
        try:
            height = float(height) 
            weight = float(weight)
        except ValueError:
            self.display_box.set_text('Height and Weight must be floats')
            return
        try:
            age = int(age)
        except ValueError:
            self.display_box.set_text('Age must be integer')
            return
        
        if vagan.lower() not in ['yes','no']:
            self.display_box.set_text('Vegetarian?: Please input Yes or No')
            return
        else:
            vagan = 1 if vagan.lower() == 'yes' else 0

        if userid == "":
            self.display_box.set_text('UserID cannot be NULL')
        elif test_userid(self.connection,userid):
            self.display_box.set_text('UserID Exists')
        elif gender.lower() not in ['male','female']:
            self.display_box.set_text('Gender:Please input Male or Female')
        else:
            insert_client(self.connection, userid, hash_password(pw), gender, age, weight, height,vagan)
            self.page = FoodAvoidPage(self.connection, self.surface,userid)
            #print(get_meal_level(gender, age, weight, height))

    def back(self):
        self.page = HomePage(self.surface,self.connection)
    def draw(self):
        self.surface.fill(BLACK)
        self.username_input.draw(self.surface)
        self.password_input.draw(self.surface)
        self.gender_input.draw(self.surface)
        self.age_input.draw(self.surface)
        self.height_input.draw(self.surface)
        self.weight_input.draw(self.surface)
        self.vagen_input.draw(self.surface)
        self.register_button.draw(self.surface)
        self.back_button.draw(self.surface)
        self.display_box.draw(self.surface)
class HomePage:
    def __init__(self, surface,connection):
        self.surface = surface
        self.connection = connection
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.login_button = Button("Login", WIDTH // 2, HEIGHT // 2 + 90,self.login)
        self.register_button = Button("Resgister", WIDTH // 2 , HEIGHT // 2 ,self.register)
        self.about_button = Button("About", WIDTH // 2 , HEIGHT // 2 + 180,self.about)
        self.page = self

    def handle_event(self, event):
        self.register_button.handle_event(event)
        self.login_button.handle_event(event)
        self.about_button.handle_event(event)
        return self.page
    def login(self):
        self.page = LoginPage(self.surface,self.connection)
    def register(self):
        self.page = RegisterPage(self.surface,self.connection)
    def about(self):
        self.page = AboutPage(self.surface,self.connection)
    
    def draw(self):
        title = self.title_font.render("Home Page", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.surface.blit(title, title_rect)
        self.about_button.draw(self.surface)
        self.register_button.draw(self.surface)
        self.login_button.draw(self.surface)
        

class AboutPage:
    def __init__(self, surface,connection):
        self.connection = connection
        self.surface = surface
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.back_button = Button("Back", 100, 50, self.back)
        self.display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 , 500, 260,font_size=18)
        self.display_box.set_text('Created by Jiuqing Yu for the course CMPSC 431W: Database Management Systems. The purpose of this application is to provide personal healthy diet suggestions for clients. It runs on a MySQL instance hosted on Google Cloud to process and store information. The application can operate on any device with a network connection on PSU Guest. All data used in this project is self-generated and fictitious.')
        self.page = self

    def handle_event(self, event):
        self.back_button.handle_event(event)
        return self.page
    def back(self):
        self.page = HomePage(self.surface,self.connection)
    
    def draw(self):
        title = self.title_font.render("About Page", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.surface.blit(title, title_rect)
        self.back_button.draw(self.surface)
        self.display_box.draw(self.surface)
        
class FoodAvoidPage:
    def __init__(self,connection, surface,userid):
        self.connection = connection
        self.surface = surface
        self.userid = userid
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.back_button = Button("Back", 100, 50, self.back)
        self.next_button = Button("Next", WIDTH-100, HEIGHT-50, self.next)
        self.food_input = TextInputBox(WIDTH//2-100, HEIGHT//2 - 220, 300, 50, "AvoidFood")
        self.reason_input = TextInputBox(WIDTH//2-100, HEIGHT//2 - 160, 300, 50, "Reason")
        self.remove_button = Button("Remove", WIDTH // 2 + 200, HEIGHT // 2 - 195,self.remove_avoid_food,fontsize=30)
        self.add_button = Button("Add", WIDTH // 2 + 300, HEIGHT // 2 - 195, self.add_avoid_food,fontsize=30)
        self.food_display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 -100, 650, 190,font_size=12)
        self.food_display_box.set_text("Food List: "+get_all_food(self.connection))
        self.food_avoid_display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 +50, 650, 95,font_size=12)
        self.food_avoid_display_box.set_text("Food Avoid List: "+get_all_avoided_food(self.connection,userid))
        self.display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 +165, 650, 40)
        self.page = self
    def remove_avoid_food(self):
        f_name = self.food_input.text
        if not food_exist_in_client_avoid_table(self.connection,self.userid,f_name):
            self.display_box.set_text('Food not exists on the Avoid List')
        else:
            remove_food_into_avoid_table(self.connection,self.userid,f_name)
            self.display_box.set_text(f'{f_name} removed on the Avoid List')
            self.food_avoid_display_box.set_text("Food Avoid List: "+get_all_avoided_food(self.connection,self.userid))
    def add_avoid_food(self):
        f_name = self.food_input.text
        reason = self.reason_input.text
        if not food_exist_in_food_table(self.connection,f_name):
            self.display_box.set_text('Food not on the Food List')
        elif food_exist_in_client_avoid_table(self.connection,self.userid,f_name):
            self.display_box.set_text('Food already exists on the Avoid List')
        else:
            add_food_into_avoid_table(self.connection,self.userid,f_name,reason)
            self.display_box.set_text(f'{f_name} added on the Avoid List')
            self.food_avoid_display_box.set_text("Food Avoid List: "+get_all_avoided_food(self.connection,self.userid))
    def handle_event(self, event):
        self.back_button.handle_event(event)
        self.food_input.handle_event(event)
        self.reason_input.handle_event(event)
        self.add_button.handle_event(event)
        self.remove_button.handle_event(event)
        self.next_button.handle_event(event)
        return self.page
    def back(self):
        self.page = HomePage(self.surface,self.connection)
    def next(self):
        self.page = PredictPage(self.surface,self.connection,self.userid)
    def draw(self):

        self.back_button.draw(self.surface)
        self.next_button.draw(self.surface)
        self.food_display_box.draw(self.surface)
        self.food_avoid_display_box.draw(self.surface)
        self.display_box.draw(self.surface)
        self.add_button.draw(self.surface)
        self.remove_button.draw(self.surface)
        self.food_input.draw(self.surface)
        self.reason_input.draw(self.surface)

class PredictPage:
    def __init__(self, surface,connection,userid):
        self.connection = connection
        self.userid = userid
        self.surface = surface
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.back_button = Button("Back", 100, 50, self.back)
        self.breakfast_display_box = DisplayBox( WIDTH // 2, HEIGHT // 2-160 , 650,60,font_size=18)
        self.regenerate_breakfast_button =Button("Regenerate", WIDTH // 2, HEIGHT // 2-80, self.predict_breakfast,fontsize=30)
        self.lunch_display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 -40,  650,60,font_size=18)
        self.regenerate_lunch_button =Button("Regenerate", WIDTH // 2, HEIGHT // 2+40, self.predict_lunch,fontsize=30)
        self.dinner_display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 +80,  650,60,font_size=18)
        self.regenerate_dinner_button =Button("Regenerate", WIDTH // 2, HEIGHT // 2+160, self.predict_dinner,fontsize=30)
        self.accept_button = Button("Accept", WIDTH // 2, HEIGHT // 2+220, self.accept)
        self.page = self
        self.foods = get_food_nutrient(self.connection)
        self.user_meal_level = get_client_meal_level(self.connection,self.userid)
        for food in self.foods:
            food["rdates"] = get_food_recommend_dates(self.connection, self.userid, food['f_name'])
            food["Avoid"] = food_exist_in_client_avoid_table(self.connection, self.userid, food['f_name'])
        self.predict_breakfast()
        self.predict_lunch()
        self.predict_dinner()

    def accept(self):
        self.page = SummaryPage(self.surface,self.connection,self.userid,self.breakfast,self.lunch,self.dinner,self.breakfast_id,self.lunch_id,self.dinner_id)

    def predict_breakfast(self):
        self.breakfast = fill_meal(self.foods,get_meal_nutrition('Breakfast', self.user_meal_level))
        self.breakfast_id = insert_meal(self.connection,self.breakfast,'Breakfast')
        self.breakfast_display_box.set_text('Breakfast: '+', '.join(f"{k}* {v}" for k, v in self.breakfast.items()))
    def predict_lunch(self):
        self.lunch = fill_meal(self.foods,get_meal_nutrition('Lunch', self.user_meal_level))
        self.lunch_id = insert_meal(self.connection,self.lunch,'Lunch')
        self.lunch_display_box.set_text('Lunch: '+', '.join(f"{k}* {v}" for k, v in self.lunch.items()))
    def predict_dinner(self):
        self.dinner = fill_meal(self.foods,get_meal_nutrition('Dinner', self.user_meal_level))
        self.dinner_id = insert_meal(self.connection,self.dinner,'Dinner')
        self.dinner_display_box.set_text('Dinner: '+', '.join(f"{k}* {v}" for k, v in self.dinner.items()))

    def handle_event(self, event):
        self.back_button.handle_event(event)
        self.accept_button.handle_event(event)
        self.regenerate_breakfast_button.handle_event(event)
        self.regenerate_lunch_button.handle_event(event)
        self.regenerate_dinner_button.handle_event(event)
        return self.page

    def back(self):
        self.page = FoodAvoidPage(self.connection, self.surface,self.userid)

    def draw(self):
        title = self.title_font.render("Meal Generator", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 220))
        self.surface.blit(title, title_rect)
        self.back_button.draw(self.surface)
        self.breakfast_display_box.draw(self.surface)
        self.lunch_display_box.draw(self.surface)
        self.dinner_display_box.draw(self.surface)
        self.accept_button.draw(self.surface)
        self.regenerate_breakfast_button.draw(self.surface)
        self.regenerate_lunch_button.draw(self.surface)
        self.regenerate_dinner_button.draw(self.surface)

class SummaryPage:
    def __init__(self, surface,connection,userid,breakfast,lunch,dinner,breakfast_id,lunch_id,dinner_id):
        self.connection = connection
        self.surface = surface
        self.userid = userid
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.breakfast_id= breakfast_id
        self.lunch_id = lunch_id
        self.dinner_id = dinner_id
        self.rdate = date.today()
        self.recommend_id = generate_recommend_id(self.userid, self.rdate)
        self.title_font = pygame.font.Font("quaver.ttf", 64)
        self.back_button = Button("Back", 100, 50, self.back)
        self.yes_button = Button("Yes", WIDTH // 2-100, HEIGHT // 2+220, self.yes)
        self.no_button = Button("No", WIDTH // 2+100, HEIGHT // 2+220, self.no)
        self.home_button = Button("Home", WIDTH // 2, HEIGHT // 2+220, self.home)
        self.display_box = DisplayBox( WIDTH // 2, HEIGHT // 2 -160, 500, 260,font_size=18)
        self.page = self
        self.summarize()
    def summarize(self):
        if client_recommended_today(self.connection,self.userid):
            self.home_button.active = False
            self.display_box.set_text('You already have a recommended meal for today. Do you want to replace it?')
        else:
            self.yes_button.active = False
            self.no_button.active = False
            
            insert_client_recommend_meal(self.connection,self.recommend_id, self.userid, self.breakfast_id,self.lunch_id,self.dinner_id,self.rdate)
            text = get_recommend_meals_text(self.connection,self.recommend_id)
            self.display_box.set_text('Your recommended meal has been successfully updated.\n'+text)
    def handle_event(self, event):
        self.yes_button.handle_event(event)
        self.no_button.handle_event(event)
        self.home_button.handle_event(event)
        self.back_button.handle_event(event)
        return self.page
    def back(self):
        self.page = PredictPage(self.surface,self.connection,self.userid)
    def home(self):
        self.page= HomePage(self.surface,self.connection)
    def yes(self):
        self.yes_button.active = False
        self.no_button.active = False
        self.home_button.active = True
        update_recommended_meal(self.connection,self.recommend_id, self.breakfast_id,self.lunch_id,self.dinner_id)
        text = get_recommend_meals_text(self.connection,self.recommend_id)

        self.display_box.set_text("Your recommended meal has been successfully replaced.\n" + text)
    def no(self):
        self.yes_button.active = False
        self.no_button.active = False
        self.home_button.active = True
        text = get_recommend_meals_text(self.connection,self.recommend_id)
        self.display_box.set_text('Your recommended meal has been successfully updated.\n'+text)

    def draw(self):
        title = self.title_font.render("Summary", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 220))
        self.surface.blit(title, title_rect)
        self.yes_button.draw(self.surface)
        self.no_button.draw(self.surface)
        self.home_button.draw(self.surface)
        self.back_button.draw(self.surface)
        self.display_box.draw(self.surface)
