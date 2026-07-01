from PIL import Image

# Open the image
img = Image.open('/home/codexhawk/.gemini/antigravity/brain/704eaca0-c9ee-4a50-9c99-6f41f67c35db/media__1776893352331.png')

# The image is 1024 x 558
# The text is at the bottom, the icon is in the upper middle
# Let's crop a square around the icon
left = 512 - 130
top = 279 - 180
right = 512 + 130
bottom = 279 + 80

cropped_img = img.crop((left, top, right, bottom))
cropped_img.save('/home/codexhawk/Desktop/PromptOS/frontend/public/logo.png')
print("Cropped successfully to frontend/public/logo.png")
