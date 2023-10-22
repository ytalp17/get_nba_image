import os
from nba_api.stats.endpoints import PlayerIndex
from tqdm import tqdm
import time
import shutil
import requests
from svglib import svglib
import fitz #pyMuPdf
from reportlab.graphics import renderPDF
from PIL import Image #pillow




def get_team_logos(project_path, keep_svg=False):
    team_logos_path = os.path.join(project_path, "team_logos")
    player_info = PlayerIndex(season = '2023-24').get_data_frames()[0]
   

    for team_id in tqdm(player_info['TEAM_ID'].unique(), desc="Fetching NBA Teams Logo"):
        time.sleep(1)

        try:
            svg_url = f'https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg'
            svg = requests.get(svg_url, stream = True)

            if svg.status_code == 200:
                svg.raw.decode_content = True
                svg_path = os.path.join(team_logos_path, f"{team_id}.svg")

                with open(svg_path, 'wb') as file:
                    shutil.copyfileobj(svg.raw, file)
        except:
            print(f'Unable to fetch logo of the team with id {team_id}')
            break

        # Convert svg to pdf 
        drawing = svglib.svg2rlg(svg_path)
        pdf = renderPDF.drawToString(drawing)

        # Open pdf with fitz (pyMuPdf) and convert to PNG
        doc = fitz.Document(stream=pdf)
        pix = doc.load_page(0).get_pixmap(alpha=True, dpi=300)
        pix.save(os.path.join(team_logos_path, f"{team_id}.png"))

        if keep_svg!=True:
            os.remove(svg_path) 

    return


def get_player_images(project_path):
    player_images_path = os.path.join(project_path, "player_images")
    player_info = PlayerIndex(season = '2023-24').get_data_frames()[0]
    

    for player_id in tqdm(player_info['PERSON_ID'].values, desc='Fetching NBA Player Images'):
        time.sleep(1)

        try:
            img_url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
            img = Image.open(requests.get(img_url, stream = True).raw)
            img.save(os.path.join(player_images_path, f"{player_id}.png"))
        except:
            print(f'Unable to fetch logo of the team with id {player_id}')

    return
