import os
from utility import get_team_logos, get_player_images

def main(player_images=True, team_logos=True):
    '''
    A script that fetches either or both nba logos and player images in .png format.
    '''

    project_path = os.getcwd()

    if team_logos==True:

        if any(x == "team_logos" for x in os.listdir(project_path)):
            get_team_logos(project_path, keep_svg=False)
        else:
            team_logos_path = os.path.join(os.getcwd(), 'team_logos')
            os.mkdir(team_logos_path)
            get_team_logos(project_path, keep_svg=False)

    if player_images==True:
        
        if any(x == "player_images" for x in os.listdir(project_path)):
            get_player_images(project_path)
        else:
            player_images_path = os.path.join(os.getcwd(), 'player_images')
            os.mkdir(player_images_path)
            get_player_images(project_path)

    

    


    return

main()