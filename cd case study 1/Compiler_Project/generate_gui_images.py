from PIL import Image, ImageDraw, ImageFont
import os

def draw_window(input_expr, output_res, filename):
    # Window dimensions
    width = 400
    height = 250
    
    # Create blank image with standard light gray Windows GUI background
    img = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 30)], fill='#ffffff') # Modern white title bar
    
    # Try to load a generic font, fallback to default
    try:
        font_title = ImageFont.truetype("arial.ttf", 12)
        font_label = ImageFont.truetype("arial.ttf", 14)
        font_input = ImageFont.truetype("consola.ttf", 16)
        font_btn = ImageFont.truetype("arialbd.ttf", 14)
    except:
        font_title = font_label = font_input = font_btn = ImageFont.load_default()

    # Draw Title
    draw.text((10, 8), "Expression Evaluator", fill='#000000', font=font_title)
    
    # Window borders
    draw.rectangle([(0, 0), (width-1, height-1)], outline='#a0a0a0', width=1)
    draw.line([(0, 30), (width, 30)], fill='#d0d0d0', width=1)
    
    # Input Label and Field
    draw.text((30, 60), "Enter Expression:", fill='#000000', font=font_label)
    draw.rectangle([(30, 80), (width-30, 110)], fill='#ffffff', outline='#7a7a7a')
    draw.text((35, 87), input_expr, fill='#000000', font=font_input)
    
    # Button
    btn_x1, btn_y1 = 150, 130
    btn_x2, btn_y2 = 250, 160
    draw.rectangle([(btn_x1, btn_y1), (btn_x2, btn_y2)], fill='#e1e1e1', outline='#adadad')
    draw.text((165, 140), "ComputeResult", fill='#000000', font=font_btn)
    
    # Output Label and Field
    draw.text((30, 180), "Result:", fill='#000000', font=font_label)
    draw.rectangle([(80, 175), (width-30, 205)], fill='#e8e8e8', outline='#a0a0a0')
    draw.text((85, 182), output_res, fill='#000000', font=font_input)
    
    img.save(filename)

if __name__ == "__main__":
    draw_window("(10+5)*3", "45.0", "c:/Desktop/case study/cd case study 1/Compiler_Project/screenshot1.png")
    draw_window("20/4+7", "12.0", "c:/Desktop/case study/cd case study 1/Compiler_Project/screenshot2.png")
    draw_window("5+3*2", "11.0", "c:/Desktop/case study/cd case study 1/Compiler_Project/screenshot3.png")
    print("Screenshots generated successfully.")
