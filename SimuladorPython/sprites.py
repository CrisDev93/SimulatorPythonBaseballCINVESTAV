import pygame

def grab_sprite_sheet(filename, rows, columns, **kwargs):  
   """Grabs images from a sprite sheet, converts them to pygame images  
   (surfaces), then puts them all in a list and returns that list.  
   Make sure you call pygame.display.set_mode() (and probably pygame.init())  
   before calling this function.  
   """  
   ##This line assumes you're working with some per-pixel format with a  
   ##transparent background. If not, use .convert() instead and  
   ##.set_colorkey(whatever the background color is) on the newly  
   ##created surface object.    
   base_image = pygame.image.load(filename).convert_alpha()  
   sprite_width = base_image.get_width() / columns  
   sprite_height = base_image.get_height() / rows  
   ##If kwargs contains all the needed sub-set arguments, uses that.  
   ##Else, use default values.  
   current_row, current_column = kwargs.get('start', (0, 0))  
   end_row, end_column = kwargs.get('end', (rows - 1, columns - 1))  
   image_list = []  
   ##Creates the Rect object we will be using in base_image.subsurface()  
   ##to capture our sub-images.    
   current_frame = pygame.Rect(0, 0, sprite_width, sprite_height)  
   while current_row <= end_row:  
     current_frame.top = sprite_height * current_row  
     while (current_row < end_row and current_column < columns) or (current_row == end_row and current_column <= end_column):  
       current_frame.left = sprite_width * current_column  
       image_list.append(base_image.subsurface(current_frame))  
       current_column += 1  
     current_column = 0  
     current_row += 1  
   return image_list 
