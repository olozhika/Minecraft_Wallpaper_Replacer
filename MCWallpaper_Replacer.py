from PIL import Image,ImageChops
import cv2
import numpy as np
from tqdm import tqdm
import importlib

void=(0, 0, 0, 255)

def generate_raw_texture(width,height,output_path='tex/random_texture.png'):
    if width>255 or height>255:
        return('Error! img width and height should be less than 255x255')
    import random
    # 创建一个空白的图像
    image = Image.new("RGB", (width, height))
    # 获取图像的像素数据
    pixels = image.load()
    # 遍历图像的每个像素，并为每个像素生成随机颜色
    for y in range(height):
        for x in range(width):
            # 生成随机的RGB颜色
            red = 64
            green = x*int(255/width)
            blue = y*int(255/height)
            # 将生成的颜色设置为当前像素的颜色
            pixels[x, y] = (red, green, blue)
    # 保存生成的贴图文件
    image.save(output_path)

def highlight_player(mat_color_path, layer_alpha_path, output_path):
    # import the img
    mat_color = Image.open(mat_color_path).convert('RGBA')
    layer_alpha = Image.open(layer_alpha_path).convert('RGBA')
    if mat_color.size != layer_alpha.size:
        return('Error! The mat_color_map and layer_alpha_map have different sizes!')
    
    # highlight player
    pixels_mat = mat_color.load()
    pixels_layer = layer_alpha.load()
    width, height = mat_color.size
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels_layer[x, y]
            # 找出layer像素不透明的部分
            if pixels_layer[x, y] != void:
                pixels_layer[x, y]=pixels_mat[x, y]
    
    layer_alpha.save(output_path)

def replace_pixel0(pixels_rgba,texture_a,texture_b):
    width_a, height_a = texture_a.size
    r, g, b, a = pixels_rgba
    # 获取贴图A中对应像素的颜色
    for y_a in range(height_a):
        for x_a in range(width_a):
            # 判断颜色是否与贴图A中独特颜色相同
            if texture_a.getpixel((x_a, y_a)) == pixels_rgba:
                # 获取贴图B中对应像素的颜色
                new_color = texture_b.getpixel((x_a, y_a))
                # 更新highlighted_player中的像素颜色
                return(new_color)
    return((0, 0, 0, 0))

def replace_pixel(pixels_rgba, texture_a, texture_b):
    # 将贴图A和B转换为NumPy数组，以便更快地操作
    arr_a = np.array(texture_a)
    arr_b = np.array(texture_b)

    # 创建一个布尔掩码，标记颜色匹配的位置
    mask = np.all(arr_a == pixels_rgba, axis=-1)
    
    if not np.any(mask):
        return((0, 0, 0, 0))

    new_texture = tuple(arr_b[np.where(mask)][0])
    return(new_texture)

def replace_texture(highlighted_player_path, texture_a_path, texture_b_path, output_path):
    highlighted_player = Image.open(highlighted_player_path).convert('RGBA')
    texture_a = Image.open(texture_a_path).convert('RGBA')
    texture_b = Image.open(texture_b_path).convert('RGBA')

    # 获取highlighted_player的像素数据
    pixels = highlighted_player.load()
    width, height = highlighted_player.size

    # 获取texture_a,b的像素数据
    if texture_a.size!=texture_b.size:
        return('Error! The two skins have different sizes! Plz use a 64x64 skin.')

    # 将贴图A替换为贴图B
    for y in tqdm(range(height)):
        for x in range(width):
            # 找出layer像素不透明的部分
            if pixels[x, y]!=void and pixels[x, y]!=(0, 0, 0, 0):
                pixels[x, y]=replace_pixel(pixels[x, y],texture_a,texture_b)
            else:
                pixels[x, y]=(0, 0, 0, 0)
    # return修改后的渲染图
    highlighted_player.save(output_path)

def composite_image(matcolormap, lighting, output_path):
    matcolor_image = Image.open(matcolormap).convert('RGBA')  # 色彩图，转换为RGBA模式
    lighting_image = Image.open(lighting).convert('RGBA')  # 光照图，转换为RGBA模式
    composite_image = ImageChops.multiply(matcolor_image, lighting_image)
    composite_image.save(output_path)

def add_background(foreground, background, output_path):
    foreground_image = Image.open(foreground).convert('RGBA')
    background_image = Image.open(background).convert('RGBA')
    result_image = Image.alpha_composite(background_image, foreground_image)
    result_image.save(output_path)

def replace_pixel_by_color(pixels_rgba,colorlist_a, colorlist_b):
    # 获取贴图A中对应像素的颜色
    for i_a in range(len(colorlist_a)):
        # 判断颜色是否与贴图A中独特颜色相同
        if colorlist_a[i_a] == pixels_rgba:
            # 获取贴图B中对应像素的颜色
            new_color = colorlist_b[i_a]
            # 更新highlighted_player中的像素颜色
            return(new_color)
    return(pixels_rgba)

def replace_eyes(highlighted_player_path, eyebrow_eye_color, want_eyebrow_eye_color, output_path):
    highlighted_player = Image.open(highlighted_player_path).convert('RGBA')
    if len(eyebrow_eye_color)!=7: 
        print('Plz input 7 colors for default eyebrows and eyes!')
        print('How could it happen? the sets are warpped by olozhika herself...')
        return(0)

    # 获取highlighted_player的像素数据
    pixels = highlighted_player.load()
    width, height = highlighted_player.size

    # 获取texture_a,b的像素数据
    if len(eyebrow_eye_color)!=len(eyebrow_eye_color):
        print('Error! The two color_set have different sizes!')
        print('if the eyes need only two colors, also input all the four colors')
        return(0)

    # 将贴图A替换为贴图B
    for y in range(height):
        for x in range(width):
            # 找出layer像素不透明的部分
            if pixels[x, y]!=void and pixels[x, y]!=(0, 0, 0, 0):
                pixels[x, y]=replace_pixel_by_color(pixels[x, y],eyebrow_eye_color, want_eyebrow_eye_color)
            else:
                pixels[x, y]=(0, 0, 0, 0)
    # return修改后的渲染图
    highlighted_player.save(output_path)

def edge_detection(input_path, output_path, lower_threshold=10, upper_threshold=100):
    # 读取输入图像（包含透明背景的PNG图像）
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

    # 分割通道并分别应用Canny边缘检测
    b, g, r, a = cv2.split(image)
    edges_b = cv2.Canny(b, lower_threshold, upper_threshold)
    edges_g = cv2.Canny(g, lower_threshold, upper_threshold)
    edges_r = cv2.Canny(r, lower_threshold, upper_threshold)
    edges_alpha = cv2.Canny(a, lower_threshold, upper_threshold)

    # 创建一个具有相同尺寸的透明背景的图像
    result = np.zeros_like(image)

    # 将检测到的边缘部分设为白色
    for edges in (edges_alpha,edges_b,edges_g,edges_r):
        result[edges != 0, 3] = 255  # 255 表示完全不透明

    # 保存结果图像（具有透明背景）
    cv2.imwrite(output_path, result)


def MCWallpaper_Replace(wallpaper_folder, outputfolder, your_skin, have_eyes=1, eye_color_file='eye_color_player',casu=0):
    import os
    # 检查文件夹是否存在
    if not os.path.exists(outputfolder):
        # 使用os.makedirs递归创建文件夹及其嵌套文件夹
        os.makedirs(outputfolder)
    # 自动地址
    mat_color_path=wallpaper_folder+'/layer_matcolor0000.png'
    mat_color_hat_path=wallpaper_folder+'/layer_matcolor0001.png'
    layer_alpha_path=wallpaper_folder+'/layer_object_1_0000.png'
    layer_alpha_hat_path=wallpaper_folder+'/layer_object_1_0001.png'
    layer_alpha_eyes_path=wallpaper_folder+'/layer_object_2_0000.png'
    background_path=wallpaper_folder+'/background0000.png'
    # 自设output地址
    highlighted_player_path=outputfolder+'/highlighted_player.png'
    highlighted_player_hat_path=outputfolder+'/highlighted_player_hat.png'
    highlighted_player_eyes_path=outputfolder+'/highlighted_player_eyes.png'
    replaced_texture_path=[outputfolder+'/changed_player.png',\
                           outputfolder+'/changed_player_shadowed0.png',\
                           outputfolder+'/changed_player_shadowed.png']
    replaced_texture_hat_path=[outputfolder+'/changed_player_hat.png',\
                               outputfolder+'/changed_player_hat_shadowed0.png',\
                               outputfolder+'/changed_player_hat_shadowed.png']
    replaced_texture_eyes_path=[outputfolder+'/changed_player_eyes.png',\
                               outputfolder+'/changed_player_eyes_shadowed0.png',\
                               outputfolder+'/changed_player_eyes_shadowed.png']
    edge_detection_path=[outputfolder+'/edge_detection.png',\
                         outputfolder+'/edge_detection_shadowed0.png',\
                         outputfolder+'/edge_detection_shadowed.png']
    full_player_path=[outputfolder+'/full_player_mat.png',\
                      outputfolder+'/full_player_illum.png',\
                      outputfolder+'/full_player_shadowed.png']
    full_image_path=outputfolder+'/full_image.png'
    # 自动地址
    texture_a_path='tex/random_texture.png'
    texture_b_path=your_skin
    eye_color_default_file='eye_colors'
    
    #什么是透明
    void=(0, 0, 0, 255)
    ################# the code ##################
    #处理眼睛
    if have_eyes:
        eyes = importlib.import_module(eye_color_file)
        eyes_def = importlib.import_module(eye_color_default_file)
        highlight_player(mat_color_path,layer_alpha_eyes_path,highlighted_player_eyes_path)
        replace_eyes(highlighted_player_eyes_path, eyes_def.colors_default, eyes.colors, replaced_texture_eyes_path[0])
        composite_image(replaced_texture_eyes_path[0],wallpaper_folder+'/layer_illum0000.png',replaced_texture_eyes_path[1])
        composite_image(replaced_texture_eyes_path[1],wallpaper_folder+'/layer_ao0000.png',replaced_texture_eyes_path[2])
    # 筛选玩家&替换贴图
    if casu==0 or os.path.exists(replaced_texture_path[0])==0:
        highlight_player(mat_color_path,layer_alpha_path,highlighted_player_path)
        replace_texture(highlighted_player_path, texture_a_path, texture_b_path, replaced_texture_path[0])
    if casu==0 or os.path.exists(replaced_texture_hat_path[0])==0:
        highlight_player(mat_color_hat_path,layer_alpha_hat_path,highlighted_player_hat_path)
        replace_texture(highlighted_player_hat_path, texture_a_path, texture_b_path, replaced_texture_hat_path[0])
    # 叠加光照
    composite_image(replaced_texture_path[0],wallpaper_folder+'/layer_illum0000.png',replaced_texture_path[1])
    composite_image(replaced_texture_path[1],wallpaper_folder+'/layer_ao0000.png',replaced_texture_path[2])
    composite_image(replaced_texture_hat_path[0],wallpaper_folder+'/layer_illum0001.png',replaced_texture_hat_path[1])
    composite_image(replaced_texture_hat_path[1],wallpaper_folder+'/layer_ao0001.png',replaced_texture_hat_path[2])
    # 合成人物
    for i in range(3):
        if have_eyes:
            add_background(replaced_texture_eyes_path[i], replaced_texture_path[i], full_player_path[i])
            add_background(replaced_texture_hat_path[i], full_player_path[i], full_player_path[i])
        else:
            add_background(replaced_texture_hat_path[i], replaced_texture_path[i], full_player_path[i])
    # 合成图片
    add_background(full_player_path[2], background_path, full_image_path)
    # 边缘检测并保存输出图像
    for i in range(3):
        edge_detection(full_player_path[i], edge_detection_path[i], lower_threshold=50, upper_threshold=100)
    print('Done! Enjoy your wallpaper :D')
    print('##############################################')
    print('If you find this tool helpful, please consider')
    print('1. starring the repository on GitHub, ')
    print('2. sharing it with others, ')
    print('3. playing with olozhika472 in Minecraft :D')
    print('##############################################')
    print('# MCWallpaper_Replacer, by olozhika472 #')
    print('https://github.com/olozhika/Minecraft_Wallpaper_Replacer')

    
