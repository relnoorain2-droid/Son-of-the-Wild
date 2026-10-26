"""Localize audible words only; keep production instructions and screen text English."""

import re

from hindi_dialogue_catalog import NARRATION

DEVANAGARI = re.compile(r'[\u0900-\u097f]')
LATIN = re.compile(r'[A-Za-z]')
QUOTED = re.compile(r'"([^"\n]+)"|(?<![A-Za-z])\x27([^\x27\n]+)\x27(?![A-Za-z])')
SPEECH = re.compile(
    r'(?m)^(?P<indent>[ \t]*)DIALOGUE (?P<start>\d+)[-\u2013](?P<end>\d+)s: '
    r'(?P<speaker>[^(:\n]+) \((?P<voice>[^)\n]+)\):\s*(?P<payload>[^\n]+)$')

VOICES = {
    'NARRATOR': 'clear, cinematic Hindi story voice',
    'Lily': 'young emotional woman speaking natural Hindi',
    'Frost': 'deep, young heroic Hindi voice; match the age in this scene',
    'Bruno': 'very deep, gentle Hindi voice; short simple sentences',
    'Martha': 'warm, lively older woman speaking Hindi',
    'King Magnus': 'deep, rough, commanding Hindi king voice',
    'Hank': 'rough but kind rural man speaking Hindi',
    'Prince Damian': 'smooth, cold young prince speaking Hindi',
    'Old Joe': 'slow, wise older man speaking Hindi',
    'Rose': 'quiet, nervous older woman speaking Hindi',
    'Captain Vex': 'harsh, forceful Hindi soldier voice',
    'Tommy': 'excited Hindi voice; match the age in this scene',
    'Sarah': 'clear, natural Hindi voice; match the age in this scene',
    'Grace': 'worried, loving mother speaking Hindi',
    'Dark Bigfoot': 'very deep, savage Hindi voice',
    'Elder Orin': 'ancient, calm, resonant Hindi elder voice',
}

# These quotes describe visible writing, place cards, musical labels or sound
# effects. They are not spoken lines and remain English under the user's rule.
SILENT_QUOTES = {
    'FROST: SON OF THE WILD', 'Directed by Noorul Ain', 'MOM', 'RUN', 'NO MORE.',
    'CEDAR HOLLOW, WASHINGTON', 'CEDAR HOLLOW, OREGON', 'MILLBROOK, OREGON',
    'Emily', 'Sarah', 'Kate', 'Deep Wild', 'boing', 'bonk', 'BONK', 'roar',
    'Frost theme', 'lumberjack games',
}

# The source also implies speech inside English action descriptions. Supply
# those audible words explicitly while leaving the surrounding direction English.
SPOKEN_ACTIONS = {
    'Two maids whisper behind the curtain.':
        'Two maids whisper behind the curtain in Hindi: "यहाँ कुछ ठीक नहीं है।"',
    'A guard politely blocks her and says the prince wants her rested.':
        'A guard politely blocks her and says in Hindi: "राजकुमार ने आपको आराम करने को कहा है।"',
    'because King Magnus says no one there can challenge the crown.':
        'because King Magnus believes those families cannot challenge the crown.',
    'Lily says the words with fear while Damian smiles for the crowd.':
        'Lily says fearfully in Hindi: "मुझे मंज़ूर है।" Damian smiles for the crowd.',
    'He says he can take Lily home.':
        'Bruno says in Hindi: "ब्रूनो तुम्हें घर पहुँचा देगा।"',
    'Lily says the forest is frightening but beautiful with him.':
        'Lily says in Hindi: "डर लगता है, पर तुम्हारे साथ जंगल सुंदर है।"',
    'Lily sings a small song Grace taught her while Bruno listens quietly.':
        'In pauses between timed dialogue, Lily softly sings the short Hindi line Grace taught her: '
        '"माँ का आँचल, घर की छाँव।" Bruno listens quietly.',
    'She says she trusts him.':
        'Lily says in Hindi: "मुझे तुम पर भरोसा है।"',
    'Lily says it almost feels like home.':
        'Lily says in Hindi: "यह जगह घर जैसी लगती है।"',
    'Lily says only that her husband is gone.':
        'Lily says only this in Hindi: "मेरे पति अब नहीं रहे।"',
    'A shout comes from the wagon road.':
        'A shout comes from the wagon road in Hindi: "बचाओ!"',
    "Tommy says the king's men are worse than bandits.":
        'Tommy says in Hindi: "राजा के आदमी डाकुओं से बदतर हैं।"',
    'Lily cannot tell him yet and says Bruno was brave.':
        'Lily cannot tell him everything yet and says in Hindi: "ब्रूनो बहुत बहादुर थे।"',
    'Frost says he cannot watch people suffer.':
        'Frost says in Hindi: "दूसरों का दुख नहीं देख सकता।"',
    "She says his father's name: Bruno.":
        'Lily says in Hindi: "तुम्हारे पिता का नाम ब्रूनो था।"',
    "He says Elder Orin's power sleeps in Frost.":
        'Old Joe says in Hindi: "ओरिन की शक्ति तुम्हारे भीतर सोई है।"',
    'Orin says Frost must carry both strength and mercy.':
        'Orin says in Hindi: "शक्ति और करुणा साथ रखना।"',
    'Lily stands firm and says she is not his bride anymore.':
        'Lily stands firm and says in Hindi: "मैं अब तुम्हारी दुल्हन नहीं हूँ।"',
}

# Preserve the source intent without awkwardly reading a chapter title aloud.
# Short lines leave time for reactions, effects and the full 30-second action.
TEMPLATES = {
    'This is <TITLE>, and my heart knows the danger is real.': 'मुझे खतरा महसूस हो रहा है।',
    'This is <TITLE>, and my heart finally knows peace is real.': 'अब सचमुच मन को शांति मिली।',
    'I will not let <TITLE> break the people I love.': 'अपनों को कुछ नहीं होने दूँगा।',
    'I have to survive <TITLE> without losing myself.': 'हिम्मत रखकर यहाँ से निकलना होगा।',
    '<TITLE> is where I stand for my family.': 'मैं परिवार के साथ हूँ।',
    'Bruno will protect Lily through <TITLE>.': 'लिली, ब्रूनो तुम्हारी रक्षा करेगा।',
    'Let the kingdom remember <TITLE>.': 'यह दिन पूरा राज्य याद रखेगा।',
    'Breathe first; <TITLE> can wait one second.': 'पहले साँस लो, फिर देखेंगे।',
    'Bruno hears fear in <TITLE>, but Bruno stays calm.': 'डर है, मगर ब्रूनो शांत रहेगा।',
    'After <TITLE>, I cannot ignore the truth anymore.': 'अब सच नहीं छिपा सकती।',
    'Father, guide me through <TITLE>.': 'पिताजी, मुझे सही राह दिखाइए।',
    'Hold steady until <TITLE> passes.': 'डटे रहो, यह वक्त भी गुज़रेगा।',
    '<TITLE> means Bruno must stay gentle and close.': 'ब्रूनो यहीं है, तुम्हारे पास।',
    'Nobody panics during <TITLE> while I am here.': 'मैं हूँ न, घबराना मत।',
    'Smile through <TITLE>; the court is watching.': 'मुस्कुराओ, दरबार देख रहा है।',
    '<TITLE> needs work, not talk.': 'बातें छोड़ो, अब काम करो।',
    'By tomorrow, <TITLE> will feel like destiny.': 'कल तक यही तुम्हारी तकदीर होगी।',
    'I have seen what comes after <TITLE>.': 'आगे क्या होगा, जानता हूँ।',
    '<TITLE> needs steady hands, honey.': 'बेटी, हाथ सँभालकर काम करो।',
    'Listen close before <TITLE> chooses you.': 'ध्यान से सुनो, वक्त कम है।',
    'We fix what <TITLE> broke before dark.': 'अँधेरे से पहले सब सुधारना है।',
    'If <TITLE> begins, you must be ready to run.': 'खतरा दिखे तो तुरंत भाग जाना।',
    'I have heard old stories about <TITLE>.': 'इसकी पुरानी कहानियाँ सुनी हैं।',
    'No one defies me after <TITLE>.': 'मेरी हुक्मउदूली कोई नहीं करेगा।',
    '<TITLE> belongs under my crown.': 'यह सब मेरी हुकूमत में है।',
    '<TITLE> will look like kindness if you obey.': 'बात मानोगी तो तकलीफ नहीं होगी।',
    'Hold the line until <TITLE> is finished.': 'मोर्चा मत छोड़ना, डटे रहो।',
    'Remember <TITLE>, child. It is your warning.': 'बेटी, इसे चेतावनी समझो।',
    'The king wants <TITLE> before dawn.': 'राजा को सुबह तक जवाब चाहिए।',
    '<TITLE> means the forest is answering.': 'जंगल तुम्हें जवाब दे रहा है।',
    '<TITLE> does not feel ordinary.': 'यह कोई मामूली बात नहीं।',
    'Your soft heart will lose during <TITLE>.': 'तेरी दया ही तुझे हराएगी।',
    'Tell me someone else saw <TITLE>.': 'यह तुमने भी देखा, है न?',
    'I saw <TITLE> with my own eyes.': 'अपनी आँखों से देखा है।',
    'By the crown, <TITLE> begins now.': 'राजा का हुक्म है, शुरू करो।',
    'Lily, stay close until <TITLE> passes.': 'लिली, मेरे पास ही रहना।',
    'The town has to understand <TITLE>.': 'पूरी बस्ती को सच जानना होगा।',
    '<TITLE> begins when anger ends.': 'क्रोध छोड़ो, तभी रास्ता खुलेगा।',
    'I will not let <TITLE> take my child quietly.': 'अपने बच्चे को नहीं खोऊँगी।',
    '<TITLE> ends under the dark pack.': 'हमारे झुंड से कोई नहीं बचेगा।',
    '<TITLE> is going to change this town.': 'अब यह बस्ती बदलने वाली है।',
    'Be still, or <TITLE> will break you.': 'शांत रहो, वरना खुद टूट जाओगे।',
    '<TITLE> is the sound I feared at our door.': 'दरवाज़े पर वही डर आ पहुँचा।',
    'We will crush anyone standing in <TITLE>.': 'रास्ते में आए तो कुचल देंगे।',
}

PHRASES = {
    'FROST: SON OF THE WILD': 'फ्रॉस्ट: जंगल का बेटा',
    'Directed by Noorul Ain': 'निर्देशन: नूरुल ऐन',
    'She will do.': 'यही ठीक रहेगी।',
    'Tomorrow I will show you our private forest.': 'कल तुम्हें अपना निजी जंगल दिखाऊँगा।',
    'Come. I want to show you my favorite place.': 'आओ, तुम्हें अपनी पसंदीदा जगह दिखाऊँ।',
    'Not another one.': 'फिर एक और नहीं।',
    'Beyond this gate, no one asks questions.': 'इस फाटक के पार कोई सवाल नहीं पूछता।',
    'When is the next selection?': 'अगला चुनाव कब होगा?',
    'Lily Carter.': 'लिली कार्टर।',
    'You are the one.': 'तुम्हें ही चुना गया है।',
    'Not again.': 'फिर से नहीं।',
    'I cannot go back.': 'मैं वापस नहीं जा सकती।',
    'Bruno stay.': 'ब्रूनो यहीं रहेगा।',
    'Home is where Lily safe.': 'जहाँ लिली सुरक्षित, वहीं घर।',
    'Run. Save our child.': 'भागो। हमारे बच्चे को बचाओ।',
    'Monster!': 'राक्षस!',
    'To Frost!': 'फ्रॉस्ट के नाम!',
    'What did he do to us?': 'उसने हमारा क्या हाल कर दिया?',
    'Bruno also sing. Badly.': 'ब्रूनो भी गाएगा। बेसुरा।',
    'BRUNO WILL BE PAPA!': 'ब्रूनो पापा बनेगा!',
    'NO MORE.': 'अब और नहीं।',
    'Finally!': 'आखिरकार!',
    'MOM': 'माँ',
    'RUN': 'भागो',
    'CEDAR HOLLOW, WASHINGTON': 'सीडर हॉलो, ओरेगन',
    'CEDAR HOLLOW, OREGON': 'सीडर हॉलो, ओरेगन',
    'MILLBROOK, OREGON': 'मिलब्रुक, ओरेगन',
    'Emily': 'एमिली', 'Sarah': 'सारा', 'Kate': 'केट',
    'Deep Wild': 'घना वन',
    'follow me': 'मेरे पीछे आओ',
    'boing': 'बोइंग', 'bonk': 'ठक', 'BONK': 'ठक', 'roar': 'गर्जना',
    'Frost theme': 'फ्रॉस्ट की धुन',
    'lumberjack games': 'लकड़ी काटने वालों के खेल',
    'No castle walls, no golden crown, just a river song and the stars come down.':
        'न महल की दीवार, न सोने का ताज, नदी गाए संग, तारे हैं पास।',
    "It's you and me and the wild, running free like a child...":
        'तुम हो, मैं हूँ, जंगल के संग, बचपन-सा आज़ाद ये मन...',
    '...no one can find us here, you and me and the wild.':
        '...दुनिया से दूर, जंगल के संग, बस तुम और मैं।',
    "Big old hands and a gentle heart, the forest knew we'd never be apart.":
        'बड़े से हाथ, कोमल-सा मन, जंगल जाने अपना बंधन।',
    "Porch lights on and the kettle's warm, we stand together through every storm.":
        'चौखट रोशन, चाय तैयार, हर तूफान में साथ है प्यार।',
    "Oh Cedar Hollow, you're my home, never gonna walk this road alone...":
        'सीडर हॉलो, मेरा घर, अब अकेला नहीं ये सफर...',
    "...big or small, we're family, here in Cedar Hollow... home.":
        '...छोटे-बड़े, सब अपने यहाँ, सीडर हॉलो, अपना जहाँ।',
    'Muddy boots and a fiddle tune, dancing under a harvest moon.':
        'मिट्टी के जूते, सारंगी की तान, चाँद तले नाचे सारा जहान।',
}


def translate_line(line, number, source_title, speaker=None, duration=None):
    if not LATIN.search(line):
        assert DEVANAGARI.search(line), (number, line)
        return line
    if line in PHRASES:
        return PHRASES[line]
    if speaker == 'NARRATOR':
        return NARRATION[number]['line']
    normalized = line
    for title in sorted({source_title, source_title.replace(':', '')}, key=len, reverse=True):
        normalized = normalized.replace(title, '<TITLE>')
    normalized = normalized.replace(' right now', '').replace('<TITLE> after the fall', '<TITLE>')
    normalized = normalized.replace('<TITLE> in the final battle', '<TITLE>')
    if normalized not in TEMPLATES:
        raise ValueError(f'Part {number:03}: untranslated quoted text: {line!r}')
    result = TEMPLATES[normalized]
    if duration == 1:
        result = {
            '<TITLE> means Bruno must stay gentle and close.': 'ब्रूनो यहीं है।',
            'Hold steady until <TITLE> passes.': 'डटे रहो।',
            '<TITLE> needs steady hands, honey.': 'बेटी, सँभलकर।',
        }.get(normalized, result)
    if speaker in {'Lily', 'Martha', 'Rose', 'Grace', 'Sarah'}:
        result = result.replace('दूँगा', 'दूँगी').replace('खड़ा हूँ', 'खड़ी हूँ').replace('जानता हूँ', 'जानती हूँ')
    elif speaker is not None:
        result = result.replace('छिपा सकती', 'छिपा सकता')
    return result


def localize_quotes(text, number, source_title):
    text = text.replace('as if saying "follow me"', 'silently gesturing for them to follow')
    for original, localized in SPOKEN_ACTIONS.items():
        text = text.replace(original, localized)
    def replace(match):
        line = match[1] if match[1] is not None else match[2]
        if line in SILENT_QUOTES:
            return match[0]
        return '"' + translate_line(line, number, source_title) + '"'
    return QUOTED.sub(replace, text)


def localize_body(text, number, source_title):
    def replace_speech(match):
        speaker = match['speaker'].strip()
        voice = VOICES[speaker]
        payloads = list(QUOTED.finditer(match['payload']))
        assert len(payloads) == 1, (number, match[0])
        original = payloads[0][1] if payloads[0][1] is not None else payloads[0][2]
        line = translate_line(original, number, source_title, speaker,
                              int(match['end']) - int(match['start']))
        return (f'{match["indent"]}DIALOGUE {match["start"]}-{match["end"]}s: '
                f'{speaker} ({voice}): "{line}"')

    text = SPEECH.sub(replace_speech, text)
    text = localize_quotes(text, number, source_title)
    # Source montage instructions must not reintroduce an English singing voice.
    text = text.replace('soft, sweet country-folk voice', 'soft, sweet Hindi singing voice over country-folk music')
    text = text.replace('young emotional American woman', 'young woman speaking natural Hindi')
    return text


def validate_native_payloads(text, source_title):
    quoted = [m[1] if m[1] is not None else m[2] for m in QUOTED.finditer(text)]
    assert quoted
    spoken_count = 0
    for payload in quoted:
        if payload in SILENT_QUOTES or payload == source_title:
            continue
        assert DEVANAGARI.search(payload) and not LATIN.search(payload), payload
        spoken_count += 1
    # Hindi belongs only inside the actual spoken/sung quoted payloads.
    assert not DEVANAGARI.search(QUOTED.sub('', text)), 'Hindi production directions found'
    return spoken_count
