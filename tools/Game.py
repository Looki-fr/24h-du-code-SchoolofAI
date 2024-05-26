import random
from tools.Joueur import *
from tools.IA import IA
from tools.prompts import *
from tools.InquireHelper import InquireHelper

DEBUG=False
USE_AI = True
HUMAN_PLAYER=True
class Game:
    def __init__(self, current_path):
        
        self.inquire_helper = InquireHelper()
        self._init_joueurs()

        self.finish=False
        self.round=1
        self.president=""

        if USE_AI:
            self.ia = IA(current_path, short_answers=True)

    def update(self):
        # compter werewolf et si 0 on gagne
        # si nbr werewolf > nbr autres gagnent
        if USE_AI:
            self.ia.add_context(get_additionnal_context("round", self.round))

        if self.round==1:
            self._add_random_context()
            self._stealer_round()
            if HUMAN_PLAYER and Joueur.find_player(self.list_joueur, "", human=True).role=="werewolf":
                self.inquire_helper.print("\nYou will be in team with "+ self.list_joueur[1].name+", the other werewolf.", "blue")
            self._cupidon_round()
            self._vote_president()


        # tour des personnages : 
        self._werewolf_round()
        self._witch_round()
        self._clairvoyant_round()

        self._check_end()

        if not self.finish:
            if self.president=="":
                self._vote_president()

            self._vote_kill(blabla=True)

            self._check_end(end=True)

            self.round+=1

    def _witch_round(self):
        witch=Joueur.find_player(self.list_joueur, "witch", role=True)
        if witch and witch.kill:
            if not witch.is_ai:
                choice=Joueur.safe_input(f"Do you want to use your potion to kill someone ? (yes/no) : ",self.inquire_helper, contains=["yes", "no"], or_=True)
                if choice=="no":
                    return
            else:
                if random.randint(1,3)==1:
                    return
            witch.kill=False
            self._temp_kill_simple(witch, get_prompt_tuer_joueur(self._get_new_list_kill(witch), self.round, witch.role), "Who do you want to kill ? ")
            
    def _cupidon_round(self):
        j=Joueur.find_player(self.list_joueur, "cupidon", role=True)
        if not j.is_ai:
            choice=Joueur.safe_input("Choose the first person to fall in love between "+" ; ".join([p for p in self._get_new_list_president(j)]) + " : ",self.inquire_helper, contains=[p for p in self._get_new_list_president(j)], or_=True)
            choice2=Joueur.safe_input("Choose the second person to fall in love between "+" ; ".join([p for p in self._get_new_list_president(j) if p!=choice]) + " : ",self.inquire_helper, contains=[p for p in self._get_new_list_president(j) if p!=choice], or_=True)
            choice=Joueur.find_player(self.list_joueur, choice)
            choice2=Joueur.find_player(self.list_joueur, choice2)
        else:
            choice=random.choice(self.list_joueur)
            l=self._get_random_list_joueur()
            l.remove(choice)
            choice2=random.choice(l)

        if not choice.is_ai:
            self.inquire_helper.print(f"\nYou are now in love with {choice2.name}.\n", "blue")
        if not choice2.is_ai:
            self.inquire_helper.print(f"\nYou are now in love with {choice.name}.\n", "blue")
        
        choice.in_love=choice2.name
        choice2.in_love=choice.name

        #print(f"\n{choice.name} and {choice2.name} are now in love.")

    def _stealer_round(self):
        j=Joueur.find_player(self.list_joueur, "stealer", role=True)
        if not j.is_ai:
            choice=Joueur.safe_input("Choose someone to steal his role between "+" ; ".join([p for p in self._get_new_list_president(j)]) + " : ",self.inquire_helper, contains=[p for p in self._get_new_list_president(j)], or_=True)
            j2=Joueur.find_player(self.list_joueur, choice)
        else:
            j2=random.choice(self._get_new_list_president(j))
            j2=Joueur.find_player(self.list_joueur, j2)
        if not j2.is_ai:
            self.inquire_helper.print(f"\nYour role got stolen, you are now a villager !\n", "blue")
        self._temp_init_joueur(j2.name, "villager", ai=j2.is_ai)
        j2.name=j.name
        j2.is_ai=j.is_ai
        if j2.role=="clairvoyant":
            j2.knowed=[]
        self.list_joueur.remove(j)
        j2.got_stolen=True
        if not j.is_ai:
            self.inquire_helper.print(f"\nYou are now the {j2.role}.\n", "blue")

    def _add_random_context(self):
        if USE_AI:
            if random.randint(1,4)==1:
                player=random.choice(self.list_joueur)
                adding_context=f"\nThe village could hear some noise last night in {player.name}'s house... You should be carefull and think twice before voting, is {player.name} a werewolf ?"
                self.inquire_helper.print(adding_context, "blue")
                self.ia.add_context(adding_context)
            if random.randint(1,4)==1:
                player=random.choice(self.list_joueur)
                adding_context=f"\nSomeone saw {player.name} in the forest last night... You should be carefull and think twice before voting, is {player.name} a werewolf ?"
                self.inquire_helper.print(adding_context, "blue")
                self.ia.add_context(adding_context)

    def _clairvoyant_round(self):
        j=Joueur.find_player(self.list_joueur, "clairvoyant", role=True)
        if j==None:
            return
        if not j.is_ai:
            choice=Joueur.safe_input("Choose someone to discover his role between "+" ; ".join([p for p in self._get_new_list_president(j) if p not in [v.name for v in j.knowed]]) + " : ",self.inquire_helper, contains=[p for p in self._get_new_list_president(j) if p not in [v.name for v in j.knowed]], or_=True)
        else:
            choice=j.choose_player(self.list_joueur)
        #print("\n",j.name, "chose to know the role of", choice.name,"\n")
        if choice==None:
            return
        if j.is_ai:
            j.add_context(f"You discovered that {choice.name} is a {choice.role}.")
            if choice.role=="werewolf":
                j.add_context("You have to eliminate him. You have to vote for him at the end of the round to eliminate him.")
        else:
            choice=Joueur.find_player(self.list_joueur, choice)
            self.inquire_helper.print(f'{choice.name} is a {choice.role}.', "magenta")    

    def _werewolf_round(self):
        if HUMAN_PLAYER:
            j=Joueur.find_player(self.list_joueur, "", human=True)
            if j and j.role=="werewolf":
                new_lst=self._get_new_list_kill(j)
                choice=None
                while choice==None:
                    choice=Joueur.safe_input("Choose somebody to eat between "+" ; ".join(new_lst) + " : ",self.inquire_helper, contains=new_lst, or_=True)
                    choice=Joueur.find_player(self.list_joueur, choice)
                    print()
                    if choice==None:
                        self.inquire_helper.print("Error reading your vote, please try again.", "red")
            else:
                choice=Joueur.werewolf_choice(self.list_joueur)
        else:
            choice=Joueur.werewolf_choice(self.list_joueur)
        print_=False

 
        bool_=self._kill_player(choice, werewolf=True)
        if not bool_:
            if choice.in_love:
                self.inquire_helper.print(f"\n{choice.name} was killed by the werewolfs, he was the {choice.role}.\n", "blue" if choice.is_ai else "red")  
                print_=True  
            if not print_:
                self.inquire_helper.print(f"\n{choice.name} was killed by the werewolfs, he was the {choice.role}.\n", "blue" if choice.is_ai else "red")  
            if USE_AI:
                self.ia.add_context(get_additionnal_context("werewolf_kill", choice))      

    def _check_end(self, end=False):
        werewolf, human=Joueur.count_werefolf(self.list_joueur, end=end)
        
        if werewolf==0:
            self.inquire_helper.print("\nThe village won, all werewolfs are dead !", "blue")
            self.finish=True
        elif werewolf>=human:
            self.inquire_helper.print("\nThe werewolfs won, they are more than the villagers !", "blue")
            self.finish=True

    def _get_new_list_president(self, player):
        new_lst=[]
        for p in self.list_joueur:
            if p.name != player.name:
                new_lst.append(p.name)
        random.shuffle(new_lst)
        return new_lst

    def _get_new_list_kill(self, player):
        if player.role=="clairvoyant":
            new_lst=[p.name for p in player.knowed if p.role=="werewolf" and player.in_love!=p.name]
            if new_lst!=[]:
                return new_lst
        new_lst=[]
        for p in self.list_joueur:
            # wereworf dont kill werewolf
            if p.role != player.role and player.in_love!=p.name:
                new_lst.append(p.name)
        random.shuffle(new_lst)
        return new_lst

    def display_votes(self, votes):
        for key, value in votes.items():
            self.inquire_helper.print(f"{key} was accused by : {', '.join(value)}", "blue")

    def _vote_kill(self, blabla=True):
        self.inquire_helper.print("\nThe village will now vote for the elimination of someone...\n", "blue")
        votes=self._get_votes_kill_discussion()
        self.display_votes(votes)
        maxi=self._get_maxi(votes)

        if len(maxi)==1:
            unlucky=maxi[0]
            j=Joueur.find_player(self.list_joueur, unlucky)
            self.inquire_helper.print("\nThe village decided to eliminate : "+ unlucky+ ",he was the "+ j.role+ "\n", "blue")
        else:
            self.inquire_helper.print("The village couldn't decide on who to eliminate, so the vote of the president will be the deciding vote.", "blue")
            unlucly=""
            for key, value in votes.items():
                if self.president in value:
                    unlucky=key
                    break
            j=Joueur.find_player(self.list_joueur, unlucky)
            self.inquire_helper.print("The president decided to eliminate : "+ unlucky+ ",he was the "+ j.role+ "\n", "blue")

        while True:
            if USE_AI and blabla :
                j=Joueur.find_player(self.list_joueur, unlucky)
                res=self.ia.generate(get_prompt_get_eliminated(j.role), temperature=0.85)
                if res == "":
                    if DEBUG : print("error in _vote_kill : continue 1")
                    continue
                break
            else:
                res= "I am sad"
                break

        j.speak(self.inquire_helper,res)   
        if USE_AI:
            self.ia.add_context(get_additionnal_context("vote_death", j))

        self._kill_player(j)

    def _temp_kill_simple(self,player,prompt__, prompt):
        while True:
            if not player.is_ai:
                result=Joueur.safe_input(prompt,self.inquire_helper, contains=[":"] if player.role!="witch" else [])
            else:
                result=self.ia.generate(prompt__, temperature=0.75, additionnal_context=player.additionnal_context)
            if result == "" or ":" not in result:
                if player.role=="witch":
                    result+=":blabla"
                else:
                    continue

            temp = result.split(":")

            joueur, raison = temp[0].strip(), temp[1].strip()
            if joueur.lower() not in [p.name.lower() for p in self.list_joueur if p.in_love.lower() != player.name.lower()]:
                if not player.is_ai:
                    print([p.name.lower() for p in self.list_joueur if p.in_love.lower() != player.name.lower()])
                    print(self.list_joueur)
                    self.inquire_helper.print(f"Erreur lors de la lecture de votre réponse, le joueur '{joueur}' n'existe pas, veuillez re-essayer.", 'red')
                continue

            j=Joueur.find_player(self.list_joueur, joueur)
            if player.role=="hunter":
                l=raison.split(".")
                l[-1]=l[-1].upper()
                raison=".".join(l)
                player.speak(self.inquire_helper,raison,murdering=joueur)
                self.inquire_helper.print(f"{joueur} as died, he was a {j.role}", "blue")
            elif player.role=="witch":
                joueur=Joueur.find_player(self.list_joueur,joueur)
                self._kill_player(j)
                self.inquire_helper.print(f"\n{joueur.name} has died to the witch, he was the {joueur.role}.\n", "blue" if joueur.is_ai else "red")
                return
            self._kill_player(j)
            return

    def _kill_player(self, player, werewolf=False):

        if werewolf:
            witch=Joueur.find_player(self.list_joueur, "witch", role=True)
            if witch and witch.heal:
                if not witch.is_ai:
                    choice=Joueur.safe_input(f"{player.name+' is' if player.name != witch.name else 'You are'} about to die because of the werewolfs, do you want to use your potion to save {'him' if player.name != witch.name else 'you'} ? ('yes' or 'no') : ",self.inquire_helper, contains=["yes", "no"], or_=True)
                else:
                    if player.in_love==witch.name:
                        choice="yes"
                    else:
                        if random.randint(1,3)==1:
                            choice="yes"
                        else:
                            choice="no"
                    
                if choice=="yes":
                    self.inquire_helper.print(f"\nThe witch used his potion to save {player.name}, who was dying to werewolfs.\n", "blue")
                    witch.heal=False
                    return True

        if player.in_love:
            lover=Joueur.find_player(self.list_joueur, player.in_love)
            player.in_love=""
        else:
            lover=None

        self.list_joueur.remove(player) 

        if player.role=="hunter":
            if USE_AI or not player.is_ai:
                self._temp_kill_simple(player, get_prompt_vengeance_hunter(self._get_new_list_kill(player)), "As the hunter, you will get your revenche and kill somebody before dying.\nVotre réponse sera du format suivant : <Nom de celui que vous souhaitez éliminer> : <raison de votre vote>\n")
            else:
                choice=random.choice(self.list_joueur)
                self.inquire_helper.print("VENGEANCE : i kill"+choice.name, "green")
                self._kill_player(choice)
        if self.president==player.name:
            self.president=""

        if lover:
            if lover.is_ai and USE_AI:
                while True:
                    result=self.ia.generate(get_prompt_cry_death(player.name), temperature=0.85, additionnal_context=lover.additionnal_context)
                    if result == "":
                        if DEBUG : print("error in _kill_player : continue 1")
                        continue
                    break
                lover.speak(self.inquire_helper,"\n"+result)
            elif not lover.is_ai:
                self.inquire_helper.print(f"\nYou are really sad, you is gonna die of sadness because your lover {player.name} is dead.\n", "red")
            lover.in_love=""
            self._kill_player(lover)
            self.inquire_helper.print(f"\n{lover.name} died of sadness, he was a {lover.role}.\n", "blue")
            self.ia.add_context(get_additionnal_context("cupidon kill", lover, lover=player.name))   

    def _get_random_list_joueur(self):
        new_lst=[]
        for p in self.list_joueur:
            new_lst.append(p)
        random.shuffle(new_lst)
        return new_lst

    def _get_accusations_context(self, accusations, player_name):
        if len(accusations)==0:
            return ""
        discussion_context=""
        for acc in accusations:
            accused, accuser, raison = acc
            if accused.lower() == player_name.lower():
                discussion_context+=f"\n-{accuser} accused you, HE WANTS TO KILL YOU, defends yourself and deny what he said ! His explanation is : \"{raison}\"."
        
        return discussion_context

    def _get_accusations_to_others(self, accusations, player_name):
        if len(accusations)==0:
            return []
        new_lst=[]
        for acc in accusations:
            accused, accuser, raison = acc
            if accused != player_name:
                new_lst.append(acc)
        return new_lst

    def _temp_get_votes_kill_discussion(self, player, votes, seen, accusations, debug=False):
        
        if USE_AI and player.is_ai:
            accusation_context=self._get_accusations_context(accusations, player.name)
            if accusation_context != "":
                result_defense=""
                while result_defense=="":
                    result_defense=self.ia.generate(get_prompt_defending_accusation(), temperature=0.85, additionnal_context=player.additionnal_context+accusation_context, debug=debug)
                player.speak(self.inquire_helper,result_defense)
        
        if not player.is_ai:
            accusation_context=self._get_accusations_context(accusations, player.name)
            if accusation_context != "":
                res=Joueur.safe_input("You have been accused, defend yourself !\n",self.inquire_helper)
                player.speak(self.inquire_helper,res)

        agree=False
        while True:
            if not player.is_ai:
                self.inquire_helper.print("now vote for the elimination of someone...", "magenta")
                result=Joueur.safe_input("Votre réponse sera du format suivant : <Nom de celui que vous souhaitez éliminer> : <raison de votre vote>\n",self.inquire_helper, contains=[":"], or_=True)
                result[0].upper()
                print()
            else:
                if USE_AI :
                    accs=self._get_accusations_to_others(accusations, player.name)
                        #
                    if len(accs)>0 and random.randint(1,2)==1:
                        agree=True
                        choice=random.choice(accs)
                        result=self.ia.generate(get_prompt_agree(choice, self.round), temperature=0.5, additionnal_context=player.additionnal_context, debug=debug)
                    else:
                        result=self.ia.generate(get_prompt_tuer_joueur(self._get_new_list_kill(player), self.round, player.role), temperature=0.75, additionnal_context=player.additionnal_context, debug=debug)
                else:
                    result = f"{player.name} : because no ai"
            if result == "" or ":" not in result:
                if DEBUG : print("error rendering _temp_get_votes_kill_discussion : continue 1", result)
                continue

            temp = result.split(":")

            joueur, raison = temp[0].strip(), temp[1].strip()
            if joueur.lower() not in [p.name.lower() for p in self.list_joueur if p.in_love.lower() != player.name.lower()]:
                if not player.is_ai:
                    print(f"Erreur lors de la lecture de votre réponse, le joueur '{joueur}' n'existe pas, veuillez re-essayer.")
                elif DEBUG:print(f"(_temp_get_votes_kill_discussion)ERROR WHILE VOTING, <joueur>:<{joueur}> is not in the list of players. It was voted by {player.name} which is {player.role}")
                continue

            player.speak(self.inquire_helper,raison, voting_for=joueur)
            votes[joueur]=votes.get(joueur, []) + [player.name]
            seen.append(player.name.lower())
            if not agree:
                accusations.append([joueur, player.name, raison])
            break

        if joueur.lower() not in seen:
            self._temp_get_votes_kill_discussion(Joueur.find_player(self.list_joueur, joueur), votes, seen, accusations, debug=debug)

    def _get_votes_kill_discussion(self):
        votes={}
        seen=[]
        accusations = []
        for player in self._get_random_list_joueur():
            if player.name.lower() not in seen:
                self._temp_get_votes_kill_discussion(player, votes, seen, accusations)
        return votes

    def _get_votes(self, function, matter):
        votes={}
        for player in self._get_random_list_joueur():
            while True:
                if not player.is_ai:
                    if matter=="president":
                        result=Joueur.safe_input("Votre réponse sera du format suivant : <Nom du futur président> : <raison de votre vote>\n",self.inquire_helper, contains=[":"])
                        print()
                    elif matter=="kill":
                        result=Joueur.safe_input("Votre réponse sera du format suivant : <Nom de celui que vous souhaitez éliminer> : <raison de votre vote>\n",self.inquire_helper, contains=[":"])
                        print()
                else:
                    if USE_AI :
                        if matter=="president":
                            result=self.ia.generate(function(self._get_new_list_president(player), self.round), temperature=0.75, additionnal_context=player.additionnal_context, debug=True)
                        elif matter=="kill":
                            result=self.ia.generate(function(self._get_new_list_kill(player), self.round), temperature=0.75, additionnal_context=player.additionnal_context, debug=True)
                    else:
                        result = f"{player.name} : because debug"
                if result == "" or ":" not in result:
                    #print("error reading vote, continue in _get_votes : ", result)
                    continue
                temp = result.split(":")
                joueur, raison = temp[0].strip(), temp[1].strip()
                if joueur.lower() not in [p.name.lower() for p in self.list_joueur]:
                    if not player.is_ai:
                        print(f"Erreur lors de la lecture de votre réponse, le joueur '{joueur}' n'existe pas, veuillez re-essayer.")
                    #print(f"ERROR WHILE VOTING, <joueur>:<{joueur}> is not in the list of players. It was voted by {player.name} which is {player.role}")
                    continue

                votes[joueur]=votes.get(joueur, []) + [player.name]
                player.speak(self.inquire_helper,raison, voting_for=joueur)
                break
        return votes

    def _get_maxi(self, votes):
        maxi=[]
        for key, value in votes.items():
            if maxi == [] or len(value) > len(votes[maxi[0]]):
                maxi=[key]
            elif len(value)==len(votes[maxi[0]]):
                maxi.append(key)
        return maxi

    def _vote_president(self):
        self.inquire_helper.print("\nThe village will now vote for a president...\n", "blue")
        # self.president=self.list_joueur[0].name
        # print("The village decided to vote for :", self.president,"\n")
        # return
        votes=self._get_votes(get_prompt_voter_president, "president")
        maxi=self._get_maxi(votes)
        if len(maxi)==1:
            self.president=maxi[0]
            self.inquire_helper.print("\nThe village decided to vote for : "+ self.president+"\n", "blue")
        else:
            if maxi==[]:
                print("Error in vote_president, maxi==[] ??")
                maxi=self.list_joueur()
            self.president=random.choice(maxi)
            self.inquire_helper.print(f"\nThe village couldn't choose a president, so {self.president} were randomly chosen."+"\n", "blue")    

    def _temp_init_joueur(self, name, role, ai=True):
        if role=="witch":
            self.list_joueur.append(Witch(name, role, ai))
        elif role=="clairvoyant":
            self.list_joueur.append(Clairvoyant(name, role, ai))
        else:
            self.list_joueur.append(Joueur(name, role, ai))
        self.list_joueur[-1].additionnal_context+=get_additionnal_context_by_role(role)

    def _is_in(self,names, name, remove_=False):
        for i in names:
            if i.lower()==name.lower():
                names.remove(i)
                return True
        return False

    def _init_joueurs(self):
        _roles=["werewolf", "werewolf", "stealer", "cupidon", "clairvoyant", "little girl", "witch", "hunter", "villager"]
        _names=["Louis", "Paul", "Axel", "Quentin", "Antoine", "Joseph", "Matis", "Guillaume", "Romain"]
        if HUMAN_PLAYER:
            role_human=Joueur.safe_input("What do you want to play ? \nyou have the choice between "+" ; ".join(list(set(_roles))) + " : ",self.inquire_helper, contains=_roles, or_=True)
            name_human=Joueur.safe_input("What is your name  ? : ",self.inquire_helper)
            if not self._is_in(_names, name_human, remove_=True):
                _names.pop(-1)
            _roles.remove(role_human.lower())
        
        random.shuffle(_names)
        
        self.list_joueur=[]
        if HUMAN_PLAYER and role_human=="werewolf":
            self._temp_init_joueur(name_human, role_human, False)

        for i in range(len(_roles)):
            self._temp_init_joueur(_names[i], _roles[i])
        
        if HUMAN_PLAYER and role_human!="werewolf":
            self._temp_init_joueur(name_human, role_human, False)

        self.inquire_helper.print("\nAll the players are : "+ ", ".join(_names)+"\n", "blue")