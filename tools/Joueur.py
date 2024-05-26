import random

class Joueur:
    def __init__(self, name, role, ai):
        self.name=name
        self.role=role
        self.is_ai=ai
        # reset dans compte
        self.additionnal_context=""
        self.in_love=""
        self._add_speaking_style()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return f"{self.name} | {self.role}"
    
    def speak(self, inquirepy, speach, voting_for="", murdering=""):
        if voting_for== "" and murdering=="":
            s=f"({self.name}) : {speach}"
        elif voting_for!="":
            s=f"({self.name}, voting for {voting_for}) : {speach}"
        else:
            s=f"({self.name}, murdering {murdering}) : {speach}"
        inquirepy.print(s+"\n", "green")
        return s

    def _add_speaking_style(self):
        if self.name=="Louis":
            self.additionnal_context+="You are Louis, a simple and idiot man. You have a lot of feelings and you are really expressive."
        elif self.name=="Paul":
            self.additionnal_context+="You are Paul, a smart lawyer. You are really formal and you have a lot of vocabulary, and a strong argumentation."
        elif self.name=="Axel":
            self.additionnal_context+="You are Axel, a shy and introverted young men, you are really discreet and you don't like to talk."
        elif self.name=="Quentin":
            self.additionnal_context+="You are Quentin, a funny and sarcastic old men, you are really ironic and you like to make jokes."
        elif self.name=="Antoine":
            self.additionnal_context+="You are Antoine, a strong and muscular men, you have a lot of confidence and you are really direct."
        elif self.name=="Joseph":
            self.additionnal_context+="You are Joseph, a wise and old men, you have a lot of experience and you are really calm."
        elif self.name=="Matis":
            self.additionnal_context+="You are Matis, a young men, you are really curious and you like to ask a lot of questions."
        elif self.name=="Guillaume":
            self.additionnal_context+="You are Guillaume, a really smart and intelligent student, you are really logical and you like to analyse."
        elif self.name=="Romain":
            self.additionnal_context+="You are Romain, a really kind and gentle men, you are really empathic and you like to help people."

    def add_context(self, context):
        self.additionnal_context+=context

    @staticmethod
    def safe_input(prompt,inquire_helper, contains=[], or_=False):
        choice=""
        while choice=="":
            choice=inquire_helper.input(prompt, "magenta")
            for i in contains:
                if or_:
                    if i.lower() in choice.lower():
                        return choice
                else:
                    if not i.lower() in choice.lower():
                        choice=""
                        inquire_helper.print("\nWrong input, your answer doesn't respect the format needed, please try again : ", "magenta")
                        break
            if or_:
                choice=""
                inquire_helper.print("\nWrong input, please choose at least one element of "+ " ; ".join(contains)+" : ", "magenta")
            else:
                return choice

    @staticmethod
    def find_player(liste_joueur, name, role=False, human=False):
        for player in liste_joueur:
            if human and not player.is_ai:
                return player
            if role:
                if player.role==name:
                    return player
            if player.name.lower()==name.lower():
                return player
        return None
    
    @staticmethod
    def count_werefolf(liste_joueur, end=False):
        werewolf=human=0
        for player in liste_joueur:
            if player.role=="werewolf":
                werewolf+=1
            else:
                human+=1
        return werewolf, human
    
    @staticmethod
    def werewolf_choice(liste_joueur):
        if liste_joueur[1].role=="werewolf":
            return random.choice(liste_joueur[2:])
        return random.choice(liste_joueur[1:])
        


class Witch(Joueur):
    def __init__(self, name, role, ai):
        super().__init__(name, role, ai)
        self.heal=True
        self.kill=True

class Clairvoyant(Joueur):
    def __init__(self, name, role, ai):
        super().__init__(name, role, ai)
        self.knowed=[self]

    def choose_player(self, liste_joueur):
        new_lst=[]
        for player in liste_joueur:
            if player not in self.knowed:
                new_lst.append(player)
        if len(new_lst)==0:
            return None
        #choice=new_lst[0]
        choice=random.choice(new_lst)
        self.knowed.append(choice)
        return choice