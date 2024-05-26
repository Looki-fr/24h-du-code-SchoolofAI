def get_prompt_tuer_joueur(liste_joueur, tour, role):
    text=""
    if role=="clairvoyant":
        text+=f"If you saw that someone is a werewolf, invent a reason in your explanation to vote for him.\
        Do not talk about clairvoyance or a kitten die.\
        Do not talk reveal your role or a kitten die.\
        Do not say that you know someone's role or a kitten die.\
        Do not talk about your abilities or a kitten die.\
        Do not talk about your powers or a kitten die."
    return text+f"This is the end of the {tour} round, you have to vote eliminate someone. \
    Who will you choose from {','.join(liste_joueur)} ? \
    You will answer following this format: '<eliminated person's name> : <explanation>'. \
    You will give the name of the player you choose to eliminate and the reason why you think he is the werewolf in your explanation.\
    The person you will vote might die, so vote for the werewolfs ONLY!"

def get_prompt_agree(accusation, tour):
    text=""
    accused, accuser, raison = accusation
    text+=f"{accused} was accused by {accuser} because \"{raison}\"\n"

    return text+f"This is the end of the {tour} round, you have to vote eliminate someone. \
    You will answer following this format: '<eliminated person's name> : <explanation>'. \
    You will agree with {accuser} and vote for {accused} \
    Your explanation will be short and in one sentence.\
    Dont repeat the accusation or a kitten will die.\
    Do not copy the accusation or a kitten will die.\
    You will explicitely say that you agree with the accusation and with the person behind it.\
    Cite the name of the person you agree with in the accusation.\
    Complete this sentence, it will be your answer, you juste have to replace <explanation> by your explanation: \
    <{accused}> : <explanation>"

def get_prompt_defending_accusation():
    return f"As a player of the game, you want to survive and eliminate werewolfs.\
    Somebody accused you to be a werewolf. He voted for you and others could follow if they listen to him. \
    Deny all accusations and give a good reason why you are not a werewolf in a short explanation or a kitten will die.\
    You will just give your short explanation without any format, just talk to the villagers.\
    Do not present yourself\
    Do not talk about your temper.\
    Talk like a human, do not repeat things from the context.\
    Use the first person (I) and do not cite your name."

def get_prompt_voter_president(liste_joueur, tour):
    return f"This is the end of the {tour} round, you have to vote for a president. \
    Who will you choose from {','.join(liste_joueur)} ? \
    You will answer following this format: '<new president's name> : <explanation>'. \
    You will give the name of the player you choose to vote for as a president and the reason why you think would be the best president in your explanation.\
    This vote is important, choose wisely."

def get_prompt_get_eliminated(role):
    if role=="werewolf":
        return f"The village decided to eliminate you. You will died really soon. \
            You are a werewolf, you are angry to be eliminated. \
            You need to reveal your role.\
            You can reveal your role because you will die soon.\
            Don't do a speach, just a few words.\
            Talk directly to the villagers, tell them you were the werewolf.\
            Talk to the villagers directly using 'you'."
    else:
        return f"The village decided to eliminate you. You will died really soon. \
            Express your feelings, your last words. \
            Tell them how sad, angry and disappointed you are because you were the {role}. \
            You feel betrayed by the village.\
            Don't do a speach, just a few words.\
            Don't have a formal vocabulary.\
            You need to reveal your role.\
            You can reveal your role because you will die soon.\
            Talk to the villagers directly using you."

def get_prompt_cry_death(lover):
    return f"Your lover {lover} is dead.\
        You are really sad and you want to express your feelings.\
        You will talk to the villagers and tell them how sad you are.\
        You will tell them that you are so sad that you are gonna die of sadness.\
        Your answer will be in one sentence."

def get_prompt_vengeance_hunter(list_player):
    return f"You are about to die\
        As a hunter, you will get your vengeance on the werewolf and kill somebody.\
        Who will you choose from {','.join(list_player)} ? \
        You will answer following this format: '<eliminated person's name> : <explanation>'. \
        Talk about vengeance and how you will kill him.\
        Add '!' in your explanation.\
        Add CAPITAL LETTERS in your explanation.\
        The person you will vote might die, so vote for the werewolfs ONLY!\
        Express your anger and your rage agaisn't the werewolfs\
        Thos are your last minutes alive, give everything you have !\
        EXPRESS YOUR ANGER.\
        EXPRESS YOUR RAGE.\
        BE ANGRY."

def get_additionnal_context_by_role(role):
    if role=="werewolf":
        return "You are a werewolf, you have to eliminate the villagers.\
        You can't kill another werewolf, you have to be discreet.\
        You can't reveal your role.\
        You need to not cite your role in your explanations."
    elif role == "clairvoyant":
        return "You are the clairvoyant, you have the power to know the role of someone.\
        You need to discover who are the werewolfs and to vote for them.\
        When you can vote to eliminate someone, VOTE FOR A WEREWOLF.\
        You can't reveal your role.\
        You need to not cite your role in your explanations.\
        Choose other reasons to vote to eliminate a werewolf than the fact you know its role.\
        Do not talk about clairvoyance or a kitten die.\
        Do not talk about your abilities or a kitten die.\
        Do not talk about your powers or a kitten die.\
        Find an other reason to explain your choice to the others."
    else:
        return "You are a villager, you have to find the werewolf.\
        You can't reveal your role.\
        You need to not cite your role in your explanations."
    
def get_additionnal_context(event, player, lover=None):
    if event=="vote_death":
        if player.role != "werewolf":
            return f"\nThe village voted to eliminate {player.name}, he was the {player.role}."
        else:
            return f"\nThe village voted to eliminate {player.name}, he was a werewolf, one still remains..."
    elif event=="werewolf_kill":
        return f"\n{player.name} was killed by the werewolfs, he was the {player.role}."
    elif event=="round":
        return f"\nStart of the {player} round."
    elif event=="cupidon kill":
        return f"{player.name} died of sadness because his lover {lover} died."
