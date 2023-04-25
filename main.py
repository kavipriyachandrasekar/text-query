import spacy
import gradio as gr

import warnings
warnings.filterwarnings("ignore")
# print("Enter two words")
# words = input()

# Load a pre-trained spaCy model
model_name = "en_core_web_lg"
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
tags_final = 'belief,motherhood,simplicity,chorus,amazement,sensual,festive,mantra,flying,witness,chennai,loyalty,rain,care,symbolic,contemplative,seasons,summer,heroism,mystical,bravado,finger,ballad,habit,city,empowerment,inequality,sparrow,playful,consent,tension,separation,timelessness,screen,soul,cultural,sound,fire,reunion,oneness,hopeful,electricity,worship,existential,rivalry,meditation,superiority,adventure,dissolution,uncertainty,friendship,rap,difficulty,confusion,proletariat,winter,irrational,joyful,queen,protection,nostalgia,ally,unknown,lightning,auspicious,website,hopelessness,sun,hopefulness,fishes,honey,atoms,healing,mistakes,teasing,positivity,unity,wonder,transcendentalism,night,hunger,determined,torture,materialism,swagger,science,supreme,rebirth,absurdity,desire,indian,deities,street,valour,freedom,reconciliation,temptation,trees,dress,robots,emotion,heart,light,wealth,flower,smell,honesty,presence,chaotic,pleading,idealistic,mysticism,joyous,transcendence,poverty,impermanence,celebration,temple,womanhood,sensations,memories,socialising,deception,community,escapism,flirting,sea,achievement,tingling,aggression,hammer,reflection,sentimental,romantic,laughter,knowledge,ascent,fashion,lyricism,suspense,control,dolphin,reverential,attachment,imaginative,nonverbal,instruments,motivation,heaven,perception,sorrow,victory,transience,loneliness,running,attraction,education,enchantment,touch,enchanting,umbrella,forgiveness,blood,metaphor,soulful,butterflies,imagery,trust,defiance,feminism,intense,pleasure,virility,folklore,springtime,fulfilment,vulnerability,acupuncture,rebellion,satire,sarcasm,impossibility,reward,devotion,cheek,surrealism,death,power,viral,connection,triumph,bitterness,lighthearted,earth,pop,electrons,ghost,travel,playfulness,vacation,introspective,birds,dreaming,gamble,kidnapping,enigmatic,mythology,fun,optimism,pensive,movement,explosion,consequences,intensity,spiritual,saxophone,flight,supernatural,arrival,intoxication,fantasy,grief,sword,childhood,morality,sadness,sky,upbeat,disorientation,memory,tooth,romance,stars,comfort,affection,woman,request,anxiety,reality,illusion,acceptance,humility,countryside,god,journey,marriage,creative,individualism,wet,expression,innocence,excitement,boasting,silence,relaxation,pain,elements,beauty,butterfly,solitude,experimental,bhakti,hope,sorrowful,disco,meaning,warning,fear,passionate,nonsense,humorous,encouragement,campaigning,election,anguish,leadership,desperation,seductive,mesmerising,corruption,creativity,understanding,possessions,roots,nations,struggle,chanting,despair,chaos,battle,futuristic,fox,peace,prisoner,rights,man,regret,ambiguity,3d,resilience,cannibalism,blessing,identity,expressive,whimsical,gangsters,depth,prosperity,wanderlust,youthful,painting,surrender,contentment,ether,personification,philosophical,heartbreak,inspiration,apology,sensory,universe,exploitation,sacrifice,entertainment,fate,treasure,wind,challenge,sincerity,wisdom,political,remorse,mindfulness,directionless,ai,game,ambiguous,burden,failure,pursuit,inspiring,einstein,wings,tiger,divine,singing,sculpture,space,epic,colloquial,strength,detachment,lamp,selflessness,faith,mind,mercy,performance,survival,tears,values,traditions,longing,suppression,fearlessness,chariot,drums,determination,repetition,destiny,hardware,bloodshed,cheating,questioning,perseverance,optimistic,sports,reflective,lyrical,smile,rainbow,girl,transformation,software,destruction,mobilisation,speech,righteousness,river,permission,search,appreciation,food,masculinity,enlightenment,moon,thought,mystery,positive,shakespeare,revelry,cloud,reincarnation,horror,diversity,droplets,admiring,past,conquest,aromas,change,girlfriend,intellect,disjointed,fleeting,family,betrayal,accountability,confrontation,kisses,wildlife,technology,poster,energetic,life,inevitability,joy,propaganda,consumerism,companionship,infatuation,metaphysical,vocals,companion,patriotic,flirtatious,conflict,deep,time,language,disney,harvest,relationship,greed,mirage,japan,haiku,enthusiastic,degree,femininity,serenity,thriller,husain,hypnotic,fever,lively,nonsensical,melting,philosophy,validation,metaphorical,fight,growth,breeze,admiration,humour,competition,modelling,harmony,seed,festival,lust,seduction,creation,revolution,anticipation,catchy,art,rhythmic,trap,miracles,melancholic,poetry,eyes,energy,love,poetic,nature,foot,unconventional,darkness,wordplay,magic,youth,blooming,cooking,gentleness,brotherhood,prayer,jasmine,panic,cleansing,cruelty,togetherness,innovation,peacock,distance,plea,madness,support,yearning,sweetness,exotic,curve,shame,courage,dancing,loss,obsession,absurd,dreamy,redemption,melody,wedding,happiness,senses,random,revenge,future,truth,scenes,commitment,abstract,duality,communication,success,irreverent,pride,war,tantra,danger,swami,sad,uplifting,dance,robotic,bravery,goddess,ethereal,justice,flag,spring,tamil,sensuous,frustration,colour,gratitude,beach,intimacy,fishing,colourful,denial,violence,anger,persistence,window,party,radio,clock,crown,nightlife,leader,confidence,euphoria,dominance,computer,culture'

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

def get_tags(sentence):
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
            if nlp(tag).similarity(token) >= 0.8:
                if token.text not in tags:
                    tags.append(token.text)
                    # print(tag, token.text, nlp(tag).similarity(token))
    return tags


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