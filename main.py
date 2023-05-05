import spacy
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import warnings
warnings.filterwarnings("ignore")
# print("Enter two words")
# words = input()

# Load a pre-trained spaCy model
model_name = "en_core_web_md"
try:
    nlp = spacy.load(model_name)
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)")
    from spacy.cli import download
    download(model_name)
    nlp = spacy.load(model_name)

# Define a list of POS tags that correspond to "content" words
content_tags = ["ADJ", "NOUN", "VERB", "ADV"]
tags_final = 'abstract,absurd,absurdity,acceptance,accountability,acupuncture,admiration,adventure,affection,aggression,ally,amazement,ambiguity,ambiguous,anger,anticipation,anxiety,apology,appreciation,art,ascent,attachment,attraction,auspicious,ballad,battle,beach,beauty,belief,betrayal,bhakti,bitterness,blessing,blood,bloodshed,boasting,bravado,bravery,breeze,brotherhood,burden,butterflies,butterfly,campaigning,cannibalism,care,celebration,challenge,change,chanting,chaotic,chariot,cheating,cheek,childhood,chorus,city,cleansing,clock,cloud,colloquial,colour,commitment,communication,community,companion,companionship,competition,computer,confidence,conflict,confrontation,confusion,connection,conquest,consent,consequences,contemplative,contentment,control,corruption,countryside,courage,creation,creative,creativity,crown,cruelty,cultural,culture,curve,dance,dancing,danger,darkness,death,deception,deep,defiance,deities,denial,desire,despair,desperation,destiny,destruction,detachment,determination,determined,devotion,difficulty,directionless,disco,disjointed,dissolution,diversity,divine,dolphin,dominance,dreamy,dress,droplets,drums,duality,earth,election,electricity,elements,emotion,empowerment,enchanting,enchantment,encouragement,energetic,energy,enigmatic,enlightenment,enthusiastic,epic,escapism,ether,ethereal,euphoria,excitement,existential,exotic,experimental,exploitation,explosion,expression,expressive,eyes,failure,faith,family,fantasy,fashion,fate,fear,fearlessness,femininity,festival,finger,fire,fishes,fishing,fleeting,flirtatious,flirting,flower,folk,folklore,food,foot,forgiveness,fox,freedom,friendship,frustration,fulfilment,fun,futuristic,gamble,game,gangsters,gentleness,girlfriend,god,goddess,gratitude,greed,grief,growth,habit,haiku,hammer,happiness,hardware,harmony,harvest,healing,heart,heartbreak,heaven,heroism,honesty,honey,hope,hopeful,hopefulness,hopelessness,humility,humorous,humour,hunger,hypnotic,idealistic,identity,illusion,imagery,imaginative,impermanence,impossibility,individualism,inequality,inevitability,infatuation,innocence,innovation,inspiration,inspiring,instruments,intellect,intense,intimacy,intoxication,introspective,irrational,irreverent,journey,joy,joyful,joyous,justice,kidnapping,knowledge,lamp,language,laughter,leader,leadership,life,light,lighthearted,lightning,lively,loneliness,longing,loss,love,loyalty,lyrical,lyricism,madness,magic,mantra,marriage,masculinity,materialism,meaning,meditation,melancholic,melody,melting,memories,memory,mercy,mesmerising,metaphor,metaphorical,metaphysical,mindfulness,miracles,mistakes,mobilisation,modelling,moon,morality,motherhood,motivation,movement,mystery,mystical,mysticism,mythology,nations,nature,night,nonsense,nonsensical,nonverbal,nostalgia,obsession,oneness,optimism,optimistic,pain,painting,party,passionate,past,patriotic,peace,peacock,pensive,perception,performance,permission,perseverance,persistence,personification,philosophical,philosophy,playful,playfulness,plea,pleading,pleasure,poetic,poetry,political,pop,positive,positivity,possessions,poster,poverty,power,prayer,pride,prisoner,proletariat,propaganda,prosperity,protection,pursuit,queen,questioning,radio,rain,rainbow,random,rap,reality,rebellion,rebirth,reconciliation,redemption,reflection,reflective,regret,reincarnation,relationship,relaxation,remorse,repetition,request,resilience,reunion,revelry,revenge,reverential,revolution,reward,rhythmic,righteousness,rights,rivalry,river,robotic,robots,romance,romantic,roots,rural,sacrifice,sadness,sarcasm,saxophone,scenes,science,screen,sculpture,sea,search,seasons,seduction,seductive,seed,selflessness,sensations,senses,sensory,sensual,sensuous,sentimental,separation,shakespeare,shame,silence,simplicity,sincerity,singing,sky,smell,smile,socialising,software,solitude,sorrow,sorrowful,soul,soulful,sound,space,sparrow,speech,spiritual,spring,springtime,stars,street,strength,struggle,success,summer,sun,superiority,supernatural,support,suppression,surrealism,surrender,sweetness,sword,symbolic,tantra,tears,teasing,technology,temple,temptation,tension,thought,tiger,time,timelessness,tingling,togetherness,tooth,touch,traditions,transcendence,transcendentalism,transformation,transience,trap,travel,treasure,trees,triumph,trust,truth,umbrella,uncertainty,unconventional,understanding,unity,universe,upbeat,uplifting,vacation,validation,valour,values,victory,violence,viral,virility,vocals,vulnerability,wanderlust,war,warning,website,wet,whimsical,wildlife,wind,window,wings,winter,wisdom,witness,womanhood,wonder,wordplay,worship,yearning,youth,youthful'

# Define a function to extract keywords from a sentence
def extract_keywords(sentence):
    # Parse the sentence with spaCy
    doc = nlp(sentence)
    # Initialize a list to hold the extracted keywords
    keywords = []
    # Iterate over the tokens in the parsed sentence
    for token in doc:
        # If the token is a content word
        if token.pos_ in content_tags:
            # Add the token's lemma to the keywords list
            keywords.append(token.lemma_)
    # Return the list of keywords
    return keywords

def get_tags(sentence, similarity_index=0.4):
    # load tags.json and import the object into a dictionary
    # songs = json.load(codecs.open('tags.json', 'r', 'utf-8-sig'))

    # #  read from file tags-processed-final.txt and split into words
    # with open('tags-processed-final.txt', 'r') as file:
    #     words = file.read().replace(',', ' ')
    words = tags_final.replace(',', ' ')
    # Example usage
    # sentence = "i have review tomorrow and i am not ready"
    keywords = extract_keywords(sentence)
    # print(keywords)

    tokens = nlp(words)
    tags = []
    for tag in keywords:
        for token in tokens:
            if nlp(tag).similarity(token) >= similarity_index:
                if token.text not in tags:
                    tags.append(token.text)
                    # print(tag, token.text, nlp(tag).similarity(token))
    return list(set(tags))


app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()
def api():
    # get the query from the url sentence
    sentence = request.args.get('sentence')
    assert sentence == str(sentence)

    if sentence == None or len(sentence) == 0:
        return "Send query param ?sentence="

    # get the tags from the sentence
    tags = get_tags(sentence)
    # return the tags as json
    return jsonify(tags)

@app.route('/noob', methods=['GET'])
@cross_origin()
def test():
    # get the query from the url sentence
    sentence = request.args.get('sentence')
    assert sentence == str(sentence)

    # assert sentence == str(sentence)

    if sentence == None or len(sentence) == 0:
        return "Send query param ?sentence="

    print(type(sentence))
    return "mysteries to the universe"


if __name__ == '__main__':
    app.run(debug=True)