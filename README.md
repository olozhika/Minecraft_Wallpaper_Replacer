# Minecraft Wallpaper Replacer

![image](https://github.com/olozhika/Minecraft_Wallpaper_Replacer/assets/37537943/aec1299d-bf21-47a7-bacf-85a7e410b4d3)

Enhance your Minecraft wallpapers with this convenient Python tool. Quickly swap skin texture to give your creations a unique look.

## Features

- **One-Click Operation:** Easily replace the skin in your Minecraft wallpaper without the need for 3D design tools.

- **Customizability:** Apply your favorite skin to Minecraft wallpapers, making your wallpaper truly unique.

- **Suitable for Minecraft and Beyond:** While initially designed for Minecraft wallpapers, the same principle applies to other renderings, provided they meet the preparation requirements.

## Prerequisites

Please note that this tool is suitable for renderings where:

- Each pixel in Original Texture (the texture to be changed) has a unique color.
- Renderings are created with layered rendering techniques.

## Installation

1. Go to the folder you want to place the tool and get in your terminal, (all the commands below are runned in the terminal!)
2. Clone the repository:
   ```bash
   git clone https://github.com/your-username/minecraft-wallpaper-replacement.git
   cd minecraft-wallpaper-replacement
   ```
3. Make sure you have python and pip installed
4. install the requirements
   ```bash
   python requirements.py
   ```

## Usage

1. Right click and open the `eye_color_player.py` as a txt file, change the RGB colors within. Save the file. 
2. Make sure you can find the following folders or paths
   - the wallpaper templates
   - the output folder
   - your skin
3. In the terminal, fill the paths/folders below and run
   ```bash
   python Run_MCR.py --wallpaper_path= --output_path= --yourskin=
   ```
   you can also change the name of the eye_color_file to some `XXXXX` by adding `--eye_color_file=XXXXXX` to the command above
4. That's all!
   For example, by running
   ```bash
   python Run_MCR.py --wallpaper_path='wallpaper/Rep_test/Alex_1eyes' --output_path='output/olozhika' --yourskin='tex/olozhika472_NMO.png'
   ```
   one will get
   ![image](https://github.com/olozhika/Minecraft_Wallpaper_Replacer/assets/37537943/32a1b86f-dc42-4c85-a5ee-4d20759625f9)
   these files in the `output/olozhika` folder.
   And the final image looks like the one maked with blue. 
   
   
## Creating wallpaper templates

both the instructions and the files are to be updated

## Wait... No more wallpapers?

*Wait, so there is only one template for us to test on?*

Be patient! Of cource **there will be more templates**, maybe in a few weeks?

______
By olozhika (olozhika472 in Minecraft)
