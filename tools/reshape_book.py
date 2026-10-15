#!/usr/bin/env python3
import html
import re
from pathlib import Path

ROOT = Path("/Users/thomaspetersen/GIT/ser_jura")

EXTRA = {
    "Afbestilling": "Det er ikke det samme som fortrydelsesrettens 14 dage.",
    "Afhjælpning": "Gæsten skal ikke vente ugevis, hvis du kan bytte med det samme.",
    "Afslag": "Prisen sættes ned, men aftalen fortsætter.",
    "Aftale": "Før klikket er det markedsføring. Efter klikket er det en aftale.",
    "Booking": "Bekræftelsen skal vise pris, dato og afbestilling.",
    "Bindende periode": "Opsigelse skal kunne ske på mail eller i appen, når bindingen er slut.",
    "Erstatning": "Gæsten skal kunne vise et tab. Et almindeligt skuffet ophold er ikke nok.",
    "Erhvervsdrivende": "Du handler i erhverv, også når gæsten er privat.",
    "Forbrugerkøb": "Købelovens forbrugerregler gælder varen, ikke hotelnatten.",
    "Forbrugerombudsmanden": "En klage kan starte hos Forbrugerombudsmanden, også uden en retssag.",
    "Fortrydelsesret": "En fast dato på hotel, bord eller billet falder ofte udenfor.",
    "Fra-pris": "Gæsten skal kunne købe til den pris, opslaget fremhæver.",
    "Garanti": "Garantien lægges oven i reklamationsretten. Den erstatter den ikke.",
    "God markedsføringsskik": "Det gælder både opslag, booking og den måde, du taler til gæsten på.",
    "Handelskøb": "Reklamér samme dag. Grossisten kan afvise en sen klage.",
    "Influencer": "Et tag er ikke en tydelig reklamemarkering. Skriv Reklame.",
    "Klage": "Skriv klagen ned med tidspunkt, værelsesnummer og hvad du tilbød.",
    "Køb": "En hotelnat er ikke et køb. Flasken i minibaren er.",
    "Købeloven": "Loven gælder varer. Se kapitel 2.",
    "Kvittering": "Bed om den, før du afviser en reklamation.",
    "Levering": "Når gæsten har varen, går risikoen normalt over.",
    "Løsøre": "Løsøre er en vare, du kan flytte. En overnatning er det ikke.",
    "Mangel": "En proppet vin er en mangel ved en vare. Et beskidt værelse er en mangel ved en ydelse.",
    "Mangelsbeføjelser": "Du får først chancen for at rette fejlen.",
    "Markedsføring": "Opslaget skal være sandt, også når det kun ligger på Instagram.",
    "Markedsføringsloven": "Loven styrer reklamen, prisen og den skjulte reklame. Se kapitel 1.",
    "Omlevering": "Gæsten skal have den vare, du aftalte, uden at vente urimeligt længe.",
    "Ophævelse": "Pengene går tilbage, og gæsten afleverer varen.",
    "Opsigelse": "Bekræft opsigelsen på samme måde, som gæsten skrev.",
    "Pakkerejse": "Tog, hotel og cykel til én samlet pris kan være en pakkerejse.",
    "Præceptiv": "Et skilt om ingen reklamation gælder ikke i et forbrugerkøb.",
    "Reklamation": "Foto og dato gør klagen lettere at behandle.",
    "Reklamationsfrist": "I forbrugerkøb er fristen to år fra leveringen.",
    "Risikoovergang": "Går tasken i stykker bagefter ved normal brug, kan det stadig være en mangel.",
    "Samtykke": "Et forudkrydset felt er ikke et ja.",
    "Skjult reklame": "Skriv ordet Reklame, så læseren ser det med det samme.",
    "Spam": "Praktisk mail om den konkrete booking er ikke reklame.",
    "Standardvilkår": "Gæsten skal kunne læse vilkårene, før han siger ja.",
    "Udeladelse": "Du skal sige det, gæsten har brug for at vide, før han booker.",
    "Urimeligt vilkår": "Et vilkår, der altid lader hotellet beholde pengene, holder sjældent.",
    "Vare": "Varen kan du lægge i en pose. Ydelsen kan du ikke.",
    "Varigt medium": "Et mundtligt vilkår i telefonen er ikke nok, når loven kræver mail eller pdf.",
    "Vildledning": "Billedet og prisen skal ligne det, gæsten kan købe.",
    "Ydelse": "Købeloven gælder ikke ydelsen. Aftalen og markedsføringen gør.",
    "Culpa": "Ansvaret kommer på tale, når du kunne have undgået skaden.",
    "Nyhedsbrev": "Uden samtykke må du kun skrive om lignende varer, gæsten selv har købt.",
}

NEW = {
    "Accept": (
        "Gæstens ja til dit tilbud.",
        "Gæsten klikker Book og betaler 1.890 kr. for to nætter. Accepten gør tilbuddet til en aftale. Et like på Instagram er ikke en accept.",
    ),
    "Ankenævn": (
        "Uafhængigt nævn, der afgør forbrugerklager.",
        "En hotelklage kan gå til Ankenævnet for Hotel, Restaurant og Turisme. En pakkerejse kan gå til Pakkerejse-Ankenævnet. Nævnet er ikke en domstol.",
    ),
    "Bekræftelse": (
        "Skriftligt bevis for bookingen.",
        "Mailen viser værelse, pris og afbestilling. Til et event viser billetmailen plads og vilkår. Mundtligt tilsagn i receptionen bør følges af en mail.",
    ),
    "Depositum": (
        "Beløb, gæsten betaler forud som sikkerhed.",
        "Et depositum på en suite eller et mødelokale skal stå i bekræftelsen. Skriv, hvornår beløbet kommer retur, og hvornår det kan beholdes.",
    ),
    "Force majeure": (
        "Ekstraordinær hindring uden for din kontrol.",
        "En strejke eller en naturkatastrofe kan være force majeure. Et almindeligt travlt køkken er det ikke. Brug ikke begrebet som en generel undskyldning i vilkårene.",
    ),
    "Formidler": (
        "Den, der formidler aftalen, uden selv at være leverandør.",
        "En bookingplatform mellem gæst og hotel er formidler. En portal, der sælger andres oplevelser, er det også. Sig tydeligt, hvem gæsten indgår aftalen med.",
    ),
    "Gebyr": (
        "Ekstra betaling ud over grundprisen.",
        "Et ekstra hotelgebyr, sen udtjekning eller et servicegebyr på billetten skal stå i totalprisen tidligt. Et gebyr, der først dukker op på sidste side, vildleder.",
    ),
    "Kreditnota": (
        "Dokument, der trækker en tidligere faktura ned.",
        "Proppet vin giver kredit på restaurantregningen. Et aflyst kursus kan give kredit på fakturaen. Skriv beløb og den faktura, kreditnotaen hører til.",
    ),
    "Overbooking": (
        "Flere bookinger end der er plads til.",
        "Flyt gæsten til et andet hotel og dæk merudgiften, når du har lovet et værelse. Til et show kan du flytte til en anden forestilling eller give pengene tilbage.",
    ),
    "Rabatkode": (
        "Kode, der sænker prisen.",
        "Koden må ikke skabe en falsk før-pris. Hvis alle betaler 800 kr. med koden, må du ikke skilte med 1.400 kr. som den normale pris.",
    ),
    "Refundering": (
        "Penge tilbage.",
        "Pengene kan komme retur efter en aftalt afbestilling, en aflysning eller en mangel, du ikke kan rette. Skriv beløb og tidspunkt i mailen.",
    ),
    "Tilbud": (
        "Det, du foreslår, at gæsten siger ja til.",
        "Prisen på værelset eller billetpakken er tilbuddet. Gæstens ja er accepten. Et opslag er ofte kun markedsføring, indtil gæsten kan sige ja til en bestemt pris.",
    ),
    "Udenretlig løsning": (
        "Løsning uden domstol.",
        "Du tilbyder et andet værelse og et afslag, eller du ombooker til næste show. De fleste gæstesager stopper her, hvis du handler hurtigt og skriver det ned.",
    ),
    "Udeblivelse": (
        "Gæsten møder ikke op og har ikke afbestilt. Branchen siger også no-show.",
        "Værelset står tomt, eller stolen til koncerten er tom. Vilkårene afgør, om gæsten stadig skal betale. Skriv reglen i bekræftelsen.",
    ),
    "Væsentlig mangel": (
        "Fejl, der betyder noget for aftalen.",
        "Intet vand på badeværelset er væsentligt. En aflyst hovednavn på plakaten er det også. En lille ridse, du har oplyst, er det ikke.",
    ),
}


def strip(value):
    text = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", text).strip()


def slugify(value):
    text = value.lower().replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def sort_key(term):
    return term.lower().translate(str.maketrans({"æ": "z1", "ø": "z2", "å": "z3"}))


def letter_of(term):
    first = term[0].upper()
    if first in "ÆØÅ":
        return first
    return first


def quiz(title, items):
    parts = [f'<div class="book-quiz">\n<h2>{html.escape(title)}</h2>\n<div hidden>']
    for question, answer, explanation, options in items:
        parts.append(
            f'<div class="question" data-question="{html.escape(question)}" data-answer="{answer}" data-explanation="{html.escape(explanation)}">'
        )
        for option in options:
            parts.append(f'<div class="option" data-option="{html.escape(option)}"></div>')
        parts.append("</div>")
    parts.append("</div>\n</div>")
    return "\n".join(parts)


def rebuild_glossary():
    path = ROOT / "kapitel3.html"
    text = path.read_text()
    start = text.index('<h2 class="letter-header" id="a">A</h2>')
    end = text.index("            </article>")
    chunk = text[start:end]
    cut = chunk.split("<h2>Sammenligningstabeller</h2>")[0]
    rows = re.findall(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", cut, re.S)
    terms = {}
    for raw_term, raw_def, raw_ex in rows:
        term = strip(raw_term)
        definition = strip(raw_def)
        example = strip(raw_ex)
        extra = EXTRA.get(term)
        if extra and extra not in example:
            example = example.rstrip(".") + ". " + extra
        terms[term] = (definition, example)
    for term, (definition, example) in NEW.items():
        terms[term] = (definition, example)

    grouped = {}
    for term in sorted(terms, key=sort_key):
        grouped.setdefault(letter_of(term), []).append(term)

    blocks = []
    for letter, names in grouped.items():
        body = []
        for term in names:
            definition, example = terms[term]
            slug = slugify(term)
            body.append(
                "                            <tr id=\"term-" + slug + "\">"
                f"<td><b>{html.escape(term)}</b></td>"
                f"<td>{html.escape(definition)}</td>"
                f"<td>{html.escape(example)}</td></tr>"
            )
        blocks.append(
            f"""                <h2 class="letter-header" id="{letter.lower()}">{letter}</h2>
                <div class="table-responsive mb-4">
                    <table class="table table-striped table-bordered glossary-table">
                        <colgroup><col class="col-ord"><col class="col-betydning"><col class="col-eksempel"></colgroup>
                        <thead><tr><th>Ord</th><th>Betydning</th><th>Eksempel</th></tr></thead>
                        <tbody>
{chr(10).join(body)}
                        </tbody>
                    </table>
                </div>"""
        )

    quizzes = "\n".join([
        quiz("Quiz: ordene i receptionen", [
            ("Gæsten vil fortryde en hotelnat booket til lørdag. Hvilket ord passer?", 0,
             "En fast dato følger afbestillingsvilkårene. Fortrydelsesrettens 14 dage gælder sjældent her.",
             ["Afbestilling", "Ophævelse", "Formodningsregel", "Kreditnota"]),
            ("Vinen er proppet. Hvilken lov starter du med?", 1,
             "Flasken er en vare. Købeloven gælder manglen.",
             ["Pakkerejseloven", "Købeloven", "Kun markedsføringsloven", "Ingen lov, fordi det er service"]),
            ("Influenceren tagger hotellet. Er det nok?", 2,
             "Et tag er ikke en tydelig reklamemarkering. Skriv Reklame, så det ses med det samme.",
             ["Ja, et tag er altid nok", "Ja, hvis opslaget har mange likes", "Nej. Skriv Reklame synligt", "Kun hvis Forbrugerombudsmanden har godkendt opslaget"]),
            ("Grossisten leverer hullerede betræk. Hvilket køb er det?", 0,
             "Hotellet køber til erhverv. Det er handelskøb, så du reklamerer samme dag.",
             ["Handelskøb", "Forbrugerkøb", "Pakkerejse", "Force majeure"]),
        ]),
        quiz("Quiz: forvekslinger", [
            ("Hvad er forskellen på mangel og fortrydelse?", 1,
             "En mangel er noget galt ved varen eller ydelsen. Fortrydelse er omfortrydelse uden fejl.",
             ["De betyder det samme", "Mangel er en fejl. Fortrydelse er uden fejl", "Fortrydelse gælder kun handelskøb", "Mangel gælder kun Instagram"]),
            ("Hvad er forskellen på garanti og reklamationsret?", 0,
             "Reklamationsretten følger loven. Garantien er et ekstra løfte oveni.",
             ["Reklamationsretten følger loven. Garantien er et ekstra løfte", "Garantien fjerner reklamationsretten", "Kun garantien gælder i shoppen", "Reklamationsret gælder kun ydelser"]),
            ("Hvad er forskellen på vildledning og udeladelse?", 2,
             "Vildledning er forkert information. Udeladelse er det, du glemmer at sige.",
             ["Udeladelse er altid strafbart. Vildledning er det aldrig", "De gælder kun priser", "Vildledning er forkert info. Udeladelse er det, du ikke siger", "Udeladelse gælder kun pakkerejser"]),
            ("Hvad er forskellen på afhjælpning og ophævelse?", 1,
             "Afhjælpning retter fejlen. Ophævelse ruller købet tilbage.",
             ["Ophævelse er altid første skridt", "Afhjælpning retter. Ophævelse ruller købet tilbage", "Afhjælpning gælder kun ydelser", "Ophævelse kræver en domstol"]),
        ]),
        quiz("Quiz: hvilken lov", [
            ("Opslag, pris, influencer og spam. Hvor starter du?", 0,
             "Det er markedsføring. Start i kapitel 1 og markedsføringsloven.",
             ["Markedsføringsloven", "Købelovens mangelsregler", "Kun pakkerejseloven", "Kun aftalelovens § 36"]),
            ("Flaske, souvenir, T-shirt og linned. Hvor starter du?", 2,
             "Det er varer. Købeloven i kapitel 2 er det rigtige sted.",
             ["Kun markedsføringsloven", "Pakkerejseloven", "Købeloven", "Forbrugeraftalelovens spamregler"]),
            ("Fly, hotel og cykel til én samlet pris. Hvad ligner det?", 1,
             "En samlet rejse med transport og overnatning kan være en pakkerejse.",
             ["Almindeligt løsøre", "En pakkerejse", "Et handelskøb", "En kreditnota"]),
            ("Spa-kortet kan kun opsiges ved personligt fremmøde. Hvad er problemet?", 3,
             "Et vilkår, der gør det urimeligt svært at stoppe, holder sjældent. Mail eller app skal være nok.",
             ["Det er force majeure", "Det er en mangel ved en vare", "Det er skjult reklame", "Det kan være et urimeligt vilkår"]),
        ]),
        quiz("Quiz: pris, samtykke og løsning", [
            ("Fra-prisen gælder kun søndag nat, men opslaget siger weekend. Hvad gør du?", 0,
             "Ret prisen, så gæsten kan købe det, opslaget lover.",
             ["Ret prisen og vis den typiske pris", "Behold teksten, hvis én gæst fik prisen", "Skriv prisen med småt nederst", "Kalder det force majeure"]),
            ("Må du sætte en hel bordplan på nyhedsbrevet?", 2,
             "Listen må bruges til middagen. Reklame for næste weekend kræver samtykke.",
             ["Ja, fordi de har været i huset", "Ja, hvis mailen har et afmeldingslink", "Nej. Reklame kræver samtykke", "Ja, hvis brylluppet er betalt"]),
            ("Gæsten udebliver uden at afbestille. Hvad styrer betalingen?", 1,
             "Vilkårene i bekræftelsen styrer udeblivelse. Skriv reglen, før gæsten booker.",
             ["Altid fuld refundering", "Vilkårene om udeblivelse", "Købelovens toårsfrist", "Automatisk 14 dages fortrydelse"]),
            ("Du kan ikke skaffe vand på værelset. Hvad er en udenretlig løsning?", 0,
             "Flyt gæsten og giv et afslag, før sagen ender i et nævn.",
             ["Flyt gæsten og giv et afslag", "Bed gæsten vente til næste morgen uden alternativ", "Slet bookingen uden besked", "Kræv et nyt depositum"]),
        ]),
    ])

    new_body = "\n".join(blocks) + "\n\n" + quizzes + "\n                <p>Kapitlet er en ordliste til undervisning. Det er ikke en fuld lovgennemgang. Slå den aktuelle lov op, eller spørg en jurist, før du ændrer vilkår eller afviser et større krav.</p>\n"
    path.write_text(text[:start] + new_body + text[end:])
    print("kapitel3 terms", len(terms))


KAP1_EXTRA = """
                <h2>Eksempler fra hotel, restaurant, event og turisme</h2>
                <div class="example-box">
                    <p><b>Hotel.</b> Gæsten booker et stille værelse. Byggeriet starter om morgenen. Det er vildledning eller udeladelse, hvis du vidste det. Tilbyd flytning. Ret opslaget.</p>
                </div>
                <div class="example-box">
                    <p><b>Restaurant.</b> Menuen siger hummer. Retten er jomfruhummer. Gæsten kan klage over ydelsen. Træk forskellen fra, eller lav en ny ret.</p>
                </div>
                <div class="example-box">
                    <p><b>Event.</b> Plakaten lover et bestemt navn. Navnet aflyses. Vilkårene siger, at programmet kan ændres. Er ændringen væsentlig, skal du tilbyde ombooking eller penge tilbage.</p>
                </div>
                <div class="example-box">
                    <p><b>Turisme.</b> Du sælger cykel, to nætter og tog til én pris. Det ligner en pakkerejse. Brug pakkerejselovens afbestillingsregler.</p>
                </div>
                <div class="example-box">
                    <p><b>Bryllup i huset.</b> Du har en bordplan med 80 mailadresser. Du må gerne bruge listen til middagen. Du må ikke sætte alle 80 på hotellets tilbudsliste. Praktisk information om brylluppet hører til aftalen. Reklame for næste weekend kræver samtykke.</p>
                </div>
                <h2>Sig det sådan</h2>
                <div class="table-responsive mb-4">
                    <table class="table table-striped table-bordered">
                        <thead><tr><th>Sig</th><th>Undgå</th></tr></thead>
                        <tbody>
                            <tr><td>Det er en afbestilling efter vores vilkår</td><td>Du har altid 14 dages fortrydelse</td></tr>
                            <tr><td>Flasken er et køb. Vi bytter den</td><td>Det er bare en oplevelse, så der er ikke noget at gøre</td></tr>
                            <tr><td>Jeg afmelder dig nu og sender en bekræftelse</td><td>Du må selv finde afmeldingslinket et sted</td></tr>
                            <tr><td>Jeg flytter dig til et andet værelse nu</td><td>Det må du leve med</td></tr>
                            <tr><td>Reklame skal stå synligt i opslaget</td><td>Et tag er fint nok</td></tr>
                        </tbody>
                    </table>
                </div>
                <h2>Hvilken lov starter du med</h2>
                <div class="table-responsive mb-4">
                    <table class="table table-striped table-bordered">
                        <thead><tr><th>Situation</th><th>Start her</th></tr></thead>
                        <tbody>
                            <tr><td>Opslag, pris, influencer, spam</td><td>Markedsføringsloven i dette kapitel</td></tr>
                            <tr><td>Booking, fortrydelse, abonnement, vilkår</td><td>Dette kapitel plus forbrugeraftaleloven og aftaleloven</td></tr>
                            <tr><td>Flaske, souvenir, T-shirt, linned</td><td>Købeloven i kapitel 2</td></tr>
                            <tr><td>Fly og hotel som én pakke</td><td>Pakkerejseloven, som dette kapitel også dækker</td></tr>
                        </tbody>
                    </table>
                </div>
"""

KAP1_QUIZ = "\n".join([
    quiz("Quiz: reklame og aftale", [
        ("Hvad er forskellen på reklame og aftale?", 1,
         "Reklamen lokker. Aftalen binder, når gæsten siger ja.",
         ["De er det samme", "Reklamen lokker. Aftalen binder, når gæsten siger ja", "Aftalen kommer altid før reklamen", "Reklame gælder kun aviser"]),
        ("Må du sende nyhedsbrev til alle på en bordplan?", 0,
         "Nej. Praktisk information om festen er i orden. Reklame kræver samtykke.",
         ["Nej, ikke uden samtykke", "Ja, hvis de sidder i restauranten", "Ja, hvis mailen er kort", "Ja, hvis du skriver Reklame i emnefeltet"]),
        ("Et opslag viser havudsigt, men værelset vender mod gården. Hvad er det?", 2,
         "Det er vildledning. Billedet skal ligne det, gæsten kan booke.",
         ["En gyldig garanti", "Force majeure", "Vildledning", "Et handelskøb"]),
        ("Hvad skal der stå, når en influencer får opholdet betalt?", 1,
         "Skriv Reklame synligt. Et tag er ikke nok.",
         ["Kun hotellets navn", "Ordet Reklame, så det ses med det samme", "Ingenting, hvis opholdet var kort", "Kun prisen"]),
    ]),
    quiz("Quiz: pris og mail", [
        ("En fra-pris på 998 kr. gælder kun søndag nat. Opslaget siger weekend. Holder det?", 0,
         "Nej. Gæsten skal kunne købe til den pris, du fremhæver.",
         ["Nej. Vis den pris, gæsten faktisk kan købe", "Ja, hvis én nat findes til prisen", "Ja, hvis prisen står i vilkårene", "Ja, hvis det er en pakkerejse"]),
        ("Hvornår skal gæsten kunne se totalprisen?", 2,
         "Tidligt i bookingen. Et gebyr på sidste side kommer for sent.",
         ["Først på fakturaen efter opholdet", "Kun hvis gæsten spørger", "Tidligt, før gæsten siger ja", "Kun i receptionen"]),
        ("Gæsten skriver stop til nyhedsbrevet. Hvad gør du?", 1,
         "Afmeld med det samme, og bekræft det.",
         ["Vent til næste udsendelse", "Afmeld med det samme og bekræft", "Bed gæsten ringe i åbningstiden", "Slet kun navnet, hvis gæsten finder linket"]),
        ("Må et ja-felt være krydset af på forhånd?", 0,
         "Nej. Gæsten skal selv sætte krydset.",
         ["Nej. Gæsten skal selv sætte krydset", "Ja, hvis afmelding er nem", "Ja, ved hotelbooking", "Ja, hvis mailen er til virksomheder"]),
    ]),
    quiz("Quiz: fortrydelse og ydelse", [
        ("Er en hotelnat købeloven?", 2,
         "Nej. En hotelnat er en ydelse. Købeloven gælder varen.",
         ["Ja, altid", "Ja, hvis gæsten betaler med kort", "Nej. Det er en ydelse", "Ja, hvis opholdet varer under to nætter"]),
        ("Hvad gør du først ved et beskidt værelse?", 1,
         "Ret fejlen med det samme. Tilbyd et andet værelse.",
         ["Bed gæsten vente til næste dag", "Ret fejlen og tilbyd et andet værelse", "Henvis kun til købeloven", "Kræv et nyt depositum"]),
        ("Hvad er forskellen på fortrydelse og afbestilling?", 0,
         "Fortrydelse er lovens 14 dage i nogle netkøb. Afbestilling følger dine vilkår eller pakkerejseloven.",
         ["Fortrydelse er lovens 14 dage i nogle netkøb. Afbestilling følger vilkårene", "De betyder det samme", "Afbestilling gælder kun varer", "Fortrydelse gælder altid en hotelnat"]),
        ("Et vilkår siger, at hotellet kan ændre alt. Hvad er det kloge svar?", 3,
         "Skriv, hvad der sker ved en væsentlig ændring, og tilbyd en rimelig løsning i den konkrete sag.",
         ["Vilgåret står, så gæsten må leve med det", "Henvis kun til force majeure", "Slet bookingen uden mail", "Ret teksten og tilbyd en rimelig løsning"]),
    ]),
])

KAP2_EXTRA = """
                <h2>Eksempler fra shop, konference og udsalg</h2>
                <div class="example-box">
                    <p><b>Hotelshop.</b> Skiltet siger 199 kr. Kassen trækker 249 kr. Ret det med det samme. Det er både prisskiltning og en forkert varepris.</p>
                </div>
                <div class="example-box">
                    <p><b>Konferencepakke.</b> Firmaet køber sal, frokost og AV. Det er ydelser. Køber de samtidig 40 flasker vand til at tage med hjem, er flaskerne varer. Hold regningerne adskilt, når der klages.</p>
                </div>
                <div class="example-box">
                    <p><b>Udsalg.</b> Du sælger en lampe med en synlig ridse og skiltet udsalg. Ridsen er oplyst og er ikke en mangel. At lampen ikke tænder, er en mangel. Skjul ikke den fejl, gæsten ikke kan se.</p>
                </div>
                <h2>Forvekslinger i shoppen</h2>
                <div class="table-responsive mb-4">
                    <table class="table table-striped table-bordered">
                        <thead><tr><th>Forveksling</th><th>Forskellen</th></tr></thead>
                        <tbody>
                            <tr><td>Mangel og fortrydelse</td><td>Mangel er noget galt. Fortrydelse er omfortrydelse uden fejl</td></tr>
                            <tr><td>Garanti og reklamationsret</td><td>Reklamationsretten følger loven. Garantien er et ekstra løfte</td></tr>
                            <tr><td>Afhjælpning og ophævelse</td><td>Afhjælpning retter. Ophævelse ruller købet tilbage</td></tr>
                            <tr><td>Forbrugerkøb og handelskøb</td><td>Gæsten i shoppen er ofte forbruger. Grossistleverancen er handelskøb</td></tr>
                        </tbody>
                    </table>
                </div>
"""

KAP2_QUIZ = "\n".join([
    quiz("Quiz: vare eller ydelse", [
        ("En gæst klager over et beskidt værelse. Er det købeloven?", 0,
         "Nej. Det er en ydelse. Se kapitel 1.",
         ["Nej. Det er en ydelse", "Ja. Alt på hotellet er købeloven", "Ja, hvis gæsten har betalt", "Kun hvis værelset er en suite"]),
        ("Gæsten køber en flaske vin i shoppen. Hvilken lov?", 1,
         "Flasken er en vare. Købeloven gælder.",
         ["Pakkerejseloven", "Købeloven", "Kun markedsføringsloven", "Ingen, fordi salget sker i lobbyen"]),
        ("Firmaet køber 40 flasker vand med hjem fra konferencen. Hvad er flaskerne?", 2,
         "Salen og frokosten er ydelser. Flaskerne, de tager med, er varer.",
         ["En pakkerejse", "Force majeure", "Varer", "Standardvilkår"]),
        ("Et digitalt gavekort til en booking. Er det automatisk købeloven?", 3,
         "En booking er ofte en ydelse. Hold dig til den konkrete aftale.",
         ["Ja, altid", "Ja, hvis beløbet er under 1.000 kr.", "Ja, hvis det sendes på mail", "Nej. En booking er ofte en ydelse"]),
    ]),
    quiz("Quiz: mangel og første skridt", [
        ("Badekåbens søm går op efter tre uger ved normal brug. Hvad er første skridt?", 1,
         "Afhjælpning. Reparation eller en ny kåbe inden for rimelig tid.",
         ["Ophævelse med det samme", "Afhjælpning inden for rimelig tid", "Afvis, fordi der er gået over 48 timer", "Kræv et nyt køb til fuld pris"]),
        ("Hotellet får 100 glas. Ti er flækkede i kassen. Hvad gør du?", 0,
         "Reklamér med det samme. Det er handelskøb.",
         ["Reklamér med det samme over for leverandøren", "Vent til næste måned", "Smid glassene ud uden besked", "Brug købelovens formodningsregel over for gæsten"]),
        ("Gæsten fortryder farven på en T-shirt dagen efter. Er det en mangel?", 2,
         "Nej. Fortrydelse er ikke en mangel.",
         ["Ja, farve er altid en mangel", "Ja, i de første 14 dage", "Nej. Der er ingen fejl ved varen", "Ja, hvis T-shirten var på udsalg"]),
        ("Lampen på udsalg tænder ikke. Ridsen var oplyst. Hvad gælder?", 1,
         "Den oplyste ridse er ikke en mangel. En lampe, der ikke tænder, er en mangel.",
         ["Hele købet er uden reklamation, fordi det er udsalg", "Det, at lampen ikke tænder, er en mangel", "Kun ridsen kan påklages", "Gæsten skal bevise fejlen i to år, før du skal reagere"]),
    ]),
    quiz("Quiz: frist, bevis og reparation", [
        ("Fejlen viser sig efter otte måneder. Hvem skal typisk bevise, at fejlen ikke var der ved købet?", 0,
         "Dig. I forbrugerkøb gælder formodningen det første år.",
         ["Dig, sælgeren", "Altid gæsten", "Grossisten, også når du solgte varen", "Ingen. Sagen er forældet efter seks måneder"]),
        ("Reparationen af højttaleren har stået stille i otte dage, og der er ingen reservedel. Kan gæsten hæve?", 1,
         "Ja, hvis det står klart, at reparationen ikke sker inden for rimelig tid.",
         ["Nej. Du har altid ret til at reparere", "Ja, hvis reparationen ikke sker inden for rimelig tid", "Nej, før der er gået to år", "Kun hvis varen kostede over 5.000 kr."]),
        ("Et skilt siger ingen ombytning på udsalgsvarer. Gæsten køber en defekt vare, og fejlen var ikke oplyst. Holder skiltet?", 2,
         "Nej. Du kan ikke fjerne reklamationsretten i et forbrugerkøb.",
         ["Ja, fordi gæsten så skiltet", "Ja, på alle udsalgsvarer", "Nej. Skiltet fjerner ikke reklamationsretten", "Ja, hvis kvitteringen gentager skiltet"]),
        ("Chokoladen i minibaren er en uge over dato. Hvad tilbyder du?", 3,
         "Det er en mangel ved en vare. Tilbyd pengene tilbage eller en ny vare.",
         ["Ingenting. Minibaren er en ydelse", "Kun en undskyldning", "Et nyt værelse", "Pengene tilbage eller en ny vare"]),
    ]),
    quiz("Quiz: handel og levering", [
        ("Du bestiller 50 hvide duge. Der kommer 50 råhvide, og arrangementet er i morgen. Hvad gør du først?", 0,
         "Reklamér med det samme. Det er handelskøb.",
         ["Reklamér med det samme med foto", "Vent, til arrangementet er overstået", "Brug forbrugerkøbets toårsfrist", "Kalder det en pakkerejse"]),
        ("Hvornår går risikoen normalt over i shoppen?", 1,
         "Når gæsten har fået varen i hånden og betalt.",
         ["Først efter to år", "Ved leveringen i shoppen", "Når gæsten forlader hotellet", "Aldrig, hvis der er garanti"]),
        ("Gaven er købt i shoppen. Lynlåsen går i stykker efter en måned. Må gavemodtageren reklamere?", 2,
         "Ja, typisk. Bed om kvittering eller anden dokumentation.",
         ["Nej. Kun den, der betalte, må klage", "Nej. Gaver er uden for købeloven", "Ja, typisk, med kvittering eller anden dokumentation", "Kun hvis gaven kostede over 500 kr."]),
        ("Webshoppen lover en velkomstpakke på en bestemt dato. Pakken er tre dage forsinket. Hvad er nok?", 1,
         "Svar hurtigt, forklar hvorfor, og tilbyd en løsning. En automatisk mail om travlhed er ikke nok.",
         ["En automatisk mail om travlhed", "Et hurtigt svar med forklaring og en løsning", "Ingenting, fordi tre dage er kort tid", "Et nyt depositum"]),
    ]),
])


def replace_tjek(path, quizzes, extra=""):
    text = path.read_text()
    text = re.sub(
        r"\n\s*<h2>Tjek dig selv</h2>\s*<div class=\"example-box\">.*?</div>\n",
        "\n" + quizzes + "\n",
        text,
        count=1,
        flags=re.S,
    )
    if extra:
        text = text.replace(
            "<p>Kapitlet er til undervisning.",
            extra + "\n                <p>Kapitlet er til undervisning.",
            1,
        )
    path.write_text(text)


def wire_assets():
    for name in ("index.html", "kapitel1.html", "kapitel2.html", "kapitel3.html"):
        path = ROOT / name
        text = path.read_text()
        text = text.replace("?v=3", "?v=4")
        if "css/quiz.css" not in text and name.startswith("kapitel"):
            text = text.replace(
                'css/square.css?v=4">',
                'css/square.css?v=4">\n    <link rel="stylesheet" href="css/quiz.css?v=4">',
            )
        if name.startswith("kapitel") and "js/quiz.js" not in text:
            text = text.replace(
                '<script src="js/theme-toggle.js"></script>',
                '<script src="js/theme-toggle.js"></script>\n    <script src="js/quiz.js"></script>',
            )
        path.write_text(text)


def language_fixes():
    path = ROOT / "kapitel2.html"
    text = path.read_text()
    text = text.replace("chocoladen", "chokoladen").replace("50 hvide dug", "50 hvide duge")
    path.write_text(text)


if __name__ == "__main__":
    rebuild_glossary()
    replace_tjek(ROOT / "kapitel1.html", KAP1_QUIZ, KAP1_EXTRA)
    replace_tjek(ROOT / "kapitel2.html", KAP2_QUIZ, KAP2_EXTRA)
    language_fixes()
    wire_assets()
    print("done")
