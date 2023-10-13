import argparse
import MCWallpaper_Replacer as MCR

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--wallpaper_path', type=str, default = None)
    parser.add_argument('--output_path', type=str, default = None)
    parser.add_argument('--yourskin', type=str, default = None)
    parser.add_argument('--eye_color_file', type=str, default = 'eye_color_player')
    parser.add_argument('--casual', type=int, default = 0)
    args = parser.parse_args()
    
    wallpaper_folder=args.wallpaper_path
    outputfolder=args.output_path
    your_skin=args.yourskin
    eye_color_file=args.eye_color_file
    casu=args.casual
    
    MCR.MCWallpaper_Replace(wallpaper_folder, outputfolder, your_skin, have_eyes=1, eye_color_file=eye_color_file,casu=casu)

    #usage: python Run_MCR.py --wallpaper_path= --output_path= --yourskin=
    #you can also change the name of the eye_color_file to some `XXXXX` by adding `--eye_color_file=XXXXXX` to the command above