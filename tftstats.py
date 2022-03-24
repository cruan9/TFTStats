import requests
if __name__ == '__main__':
    print("Enter your username:")
    name = input()
    print("Processing...")
    api = open('API_KEY.txt')
    api_key = api.read()
    puuid_api = requests.get("https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/"+name+"?api_key="+api_key)
    #print(puuid_api.content)
    json_parse_puuid= puuid_api.json()
    player_puuid = json_parse_puuid["puuid"]
    matches = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"+player_puuid+"/ids?api_key="+api_key)
    #print(matches.content)
    json_parse_matches = matches.json()

    #variables
    galiocount = 0
    wins = 0
    top4s = 0
    average_placement = 0
    traits = ["Set6_Challenger", "Set6_Enchanter","Set6_Hextech","Set6_Mercenary","Set6_Colossus","Set6_Rivals",
    "Set6_Scrap","Set6_Socialite","Set6_Syndicate","Set6_Twinshot","Set6_Yordle","Set6_Arcanist","Set6_Assassin","Set6_Bruiser","Set6_Mercenary","Set6_Mutant","Set6_Striker","Set6_Bodyguard","Set6_Debonair","Set6_Scholar",
    "Set6_Innovator", "Set6_Chemtech","Set6_Enforcer","Set6_Mastermind","Set6_Glutton", "Set6_Yordle-Lord", "Set6_Clockwork"]
    traits_count = {}
    highest_trait_num = 0
    highest_trait_name = "Undefined"
    for i in range(20):
            #getting data
            player_matches = json_parse_matches[i]
            match = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/"+player_matches+"?api_key="+api_key)
            #print("https://americas.api.riotgames.com/tft/match/v1/matches/"+player_matches+"?api_key="+api_key)
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

            #processing data
            player_units = player_game_stats["units"]
            player_traits = player_game_stats["traits"]
            placement = player_game_stats["placement"]
            average_placement += placement
            if placement == 1:
                top4s+= 1
                wins += 1
            elif placement <= 4:
                top4s +=1
            for j in player_units:
                if j["character_id"] == "TFT6_Galio": 
                    galiocount = galiocount + 1
            for j in player_traits:
                if j["tier_current"] != 0:
                    if( j["name"] in traits_count):
                        traits_count[j["name"]] += 1
                    else:
                        traits_count[j["name"]] = 1
                        #traits_count.update({j["name"]: traits_count[j["name"]]+1})
    
    average_placement /= 20
    for j in traits:
        if j in traits_count:
            if highest_trait_num < traits_count[j]:
                highest_trait_num = traits_count[j]
                highest_trait_name = j
    print("You have "+ str(galiocount) + " galios in your last 20 games!")
    print("Your top 4 rate is " + str(top4s*5) + "% "+ "in your last 20 games!")
    print("You have gone first " + str(wins) + " times in your last 20 games!")
    print("Average placement: " + str(average_placement))
    print("Your most used trait is: " + highest_trait_name.replace("Set6_", "") + " which was used " + str(highest_trait_num) + " out of 20 times")

            


    

    
