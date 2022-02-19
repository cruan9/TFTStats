import requests
if __name__ == '__main__':
    name = input()
    api = open('API_KEY.txt')
    api_key = api.read()\
    print(api_key)
    puuid_api = requests.get("https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/"+name+"?api_key="+api_key)
    #print(puuid_api.content)
    json_parse_puuid= puuid_api.json()
    player_puuid = json_parse_puuid["puuid"]
    matches = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"+player_puuid+"/ids?api_key="+api_key)
    #print(matches.content)
    galiocount = 0
    json_parse_matches = matches.json()
    for i in range(20):
            player_matches = json_parse_matches[i]
            match = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/"+player_matches+"?api_key="+api_key)
            json_parse_match = match.json()
            game_stats = json_parse_match["info"]
            participant_stats = game_stats["participants"]

            metadata = json_parse_match["metadata"]
            participants_list = metadata["participants"]
            player_num = 0
            for j in range(8):
                if player_puuid == participants_list[j]:
                    player_num = j
            player_game_stats = (participant_stats[player_num])
            player_units = player_game_stats["units"]
            for j in player_units:
                if j["character_id"] == "TFT6_Galio": 
                    galiocount = galiocount + 1
    print("You have "+ str(galiocount) + " galios in your last 20 games!")

            


    

    
