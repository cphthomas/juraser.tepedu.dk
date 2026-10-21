#!/usr/bin/env python3
"""Byg quizzer i quiz/ og læg linkblokke sidst i kapitlerne."""
import html
import re
from pathlib import Path

ROOT = Path("/Users/thomaspetersen/GIT/ser_jura")

TEMPLATE = """<!DOCTYPE html>
<html lang="da">

<head>
     <meta charset="UTF-8">
     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
     <meta http-equiv="Content-Language" content="da">
     <title>{title}</title>
     <link rel="preconnect" href="https://fonts.googleapis.com">
     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@100;300;400;500&family=Roboto:ital,wght@0,100;0,300;0,400;1,100;1,300;1,400&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
     <link rel="stylesheet" href="https://quiz.tepedu.dk/styles.css">
     <link rel="icon" href="https://quiz.tepedu.dk/favicon.svg">
     <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>

<body data-formål="{formaal}" data-forudsætning-url="{chapter_url}" data-forudsætning-text="{chapter_label}" data-forudsætning="">
     <header> <a href="../index.html" target="_blank"><img src="../tepedulogoanim.svg" alt="Logo" width="8%"></a>
          <h2>Quiz Jura for serviceøkonomer</h2>
     </header>

     <div class="container">
          <div class="row justify-content-center">
               <div class="col-12 col-md-12 col-lg-12">
                    <div class="card mt-5">
                         <div class="card-body">
                              <div id="postProgressContent" class="mt-4" style="color: rgb(255, 255, 255);">
                                   <div>
                                        <h1>{heading}</h1>
                                   </div>
                              </div>
                              <h1 id="question" class="card-title"></h1>
                              <div id="options" class="mt-4"></div>
                              <div id="progress-bar" class="progress-bar-container"></div>
                              <div id="quiz-data" style="display: none;">
{questions}
                              </div>
                         </div>
                    </div>
                </div>
            </div>
        </div>
    <script src="https://quiz.tepedu.dk/script.js"></script>
</body>
</html>
"""


def qblock(index, question, answer, explanation, options):
    opts = "\n".join(
        f'                                        <div class="option" data-option="{html.escape(opt, quote=True)}"></div>'
        for opt in options
    )
    return f"""                                   <!-- {index} -->
                                   <div class="question"
                                        data-question="{html.escape(question, quote=True)}"
                                        data-answer="{answer}"
                                        data-explanation="{html.escape(explanation, quote=True)}">
{opts}
                                   </div>
"""


def render(slug, title, heading, formaal, chapter, questions):
    body = "\n".join(qblock(i, *item) for i, item in enumerate(questions))
    page = TEMPLATE.format(
        title=html.escape(title),
        heading=html.escape(heading),
        formaal=html.escape(formaal, quote=True),
        chapter_url=f"https://juraser.tepedu.dk/{chapter}",
        chapter_label=html.escape(f"Online-bog Jura for serviceøkonomer, {chapter}", quote=True),
        questions=body,
    )
    path = ROOT / "quiz" / slug
    path.write_text(page)
    if len(questions) < 10:
        raise SystemExit(f"{slug} har kun {len(questions)} spørgsmål")


def strip_inline(text):
    key = '<div class="book-quiz">'
    out = []
    i = 0
    while True:
        j = text.find(key, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        k = j
        depth = 0
        while k < len(text):
            if text.startswith("<div", k):
                depth += 1
                k = text.find(">", k) + 1
            elif text.startswith("</div>", k):
                depth -= 1
                k += len("</div>")
                if depth == 0:
                    break
            else:
                k += 1
        i = k
    text = "".join(out)
    text = text.replace('    <link rel="stylesheet" href="css/quiz.css?v=4">\n', "")
    text = text.replace('    <script src="js/quiz.js"></script>\n', "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def quiz_block(items):
    parts = ["\n                <h2>Quiz</h2>\n                <div class=\"quiz-container\">\n"]
    for href, label in items:
        start = "Start " + label
        parts.append(
            f'                    <a href="{href}" class="effectLinks"\n'
            f'                        data-replace="{html.escape(start, quote=True)}"\n'
            f'                        target="_blank">\n'
            f'                        <span>{html.escape(label)}</span> </a>\n'
            f'                    <br>\n'
        )
    parts.append("                </div>\n")
    return "".join(parts)


def insert_links(name, items):
    path = ROOT / name
    text = strip_inline(path.read_text())
    block = quiz_block(items)
    marker = "            </article>"
    if marker not in text:
        raise SystemExit(f"mangler article-slut i {name}")
    if 'class="quiz-container"' in text:
        raise SystemExit(f"quiz-container findes allerede i {name}")
    text = text.replace(marker, block + marker, 1)
    text = text.replace("?v=4", "?v=5")
    path.write_text(text)


QUIZZES = []

# --- Kapitel 1 ---
QUIZZES.append(("1-1.html", "Quiz 1.1 om Markedsføring: Reklame og aftale",
                "1. Reklame og aftale",
                "Kunne skelne reklame fra aftale og kende vildledning og skjult reklame.",
                "kapitel1.html", [
    ("Hvad er forskellen på reklame og aftale?", 1,
     "Reklamen lokker. Aftalen binder, når gæsten siger ja.",
     ["De er det samme", "Reklamen lokker. Aftalen binder, når gæsten siger ja", "Aftalen kommer altid før reklamen", "Reklame gælder kun aviser"]),
    ("Et opslag viser havudsigt, men værelset vender mod gården. Hvad er det?", 2,
     "Det er vildledning. Billedet skal ligne det, gæsten kan booke.",
     ["En gyldig garanti", "Force majeure", "Vildledning", "Et handelskøb"]),
    ("Du ved, at der er byggeri uden for værelset, men skriver det ikke. Hvad er det?", 0,
     "Du udelader noget, gæsten har brug for at vide, før han booker.",
     ["Udeladelse", "En mangel ved en vare", "Handelskøb", "Kreditnota"]),
    ("Hvad kræver markedsføringsloven, før du skriver «byens bedste brunch»?", 3,
     "Du skal kunne dokumentere udsagnet, jf. markedsføringslovens § 13.",
     ["Ingenting, det er salgssprog", "Kun et tag på Instagram", "Et samtykke fra gæsten", "Noget, du kan vise frem"]),
    ("Gæsten booker et stille værelse. Byggeriet starter om morgenen, og du vidste det. Hvad gør du?", 1,
     "Tilbyd flytning, og ret opslaget. Ellers er det vildledning eller udeladelse.",
     ["Henvis kun til købeloven", "Tilbyd flytning og ret opslaget", "Kræv et nyt depositum", "Sig, at gæsten må leve med det"]),
    ("Menuen siger hummer. Retten er jomfruhummer. Hvad kan gæsten kræve?", 2,
     "Gæsten kan klage over ydelsen. Træk forskellen fra, eller lav en ny ret.",
     ["Ingenting, fordi det er en vare", "14 dages fortrydelse", "Afslag eller en ny ret", "En kreditnota fra købeloven"]),
    ("Plakaten lover et bestemt navn. Navnet aflyses, og ændringen er væsentlig. Hvad tilbyder du?", 0,
     "Ombooking eller pengene tilbage. Et vilkår om, at programmet kan ændres, redder dig ikke ved en væsentlig ændring.",
     ["Ombooking eller pengene tilbage", "Ingenting, fordi vilkårene nævner ændringer", "Kun et nyt depositum", "Afhjælpning efter købeloven"]),
    ("Et vilkår siger, at hotellet kan ændre alt. Hvad er det kloge svar?", 3,
     "Skriv, hvad der sker ved en væsentlig ændring, og tilbyd en rimelig løsning i den konkrete sag.",
     ["Vilkåret står, så gæsten må leve med det", "Henvis kun til force majeure", "Slet bookingen uden mail", "Ret teksten og tilbyd en rimelig løsning"]),
    ("Hvem kan gå ind i en sag om skjult reklame og vildledende priser?", 1,
     "Forbrugerombudsmanden fører tilsyn med markedsføringen.",
     ["Pakkerejse-Ankenævnet i alle sager", "Forbrugerombudsmanden", "Kun politiet", "Kun købelovens mangelsregler"]),
    ("God markedsføringsskik betyder blandt andet, at du ikke må?", 0,
     "Du må ikke presse børn eller skjule vigtige vilkår.",
     ["Presse børn eller skjule vigtige vilkår", "Skrive prisen på hjemmesiden", "Sende en bookingbekræftelse", "Bøde en proppet vin"]),
]))

QUIZZES.append(("1-2.html", "Quiz 1.2 om Markedsføring: Pris, influencer og mail",
                "2. Pris, influencer og mail",
                "Kunne vise en ærlig pris, mærke reklame og håndtere samtykke.",
                "kapitel1.html", [
    ("En fra-pris på 998 kr. gælder kun søndag nat. Opslaget siger weekend. Holder det?", 0,
     "Nej. Gæsten skal kunne købe til den pris, du fremhæver.",
     ["Nej. Vis den pris, gæsten faktisk kan købe", "Ja, hvis én nat findes til prisen", "Ja, hvis prisen står i vilkårene", "Ja, hvis det er en pakkerejse"]),
    ("Hvornår skal gæsten kunne se totalprisen?", 2,
     "Tidligt i bookingen. Et gebyr på sidste side kommer for sent.",
     ["Først på fakturaen efter opholdet", "Kun hvis gæsten spørger", "Tidligt, før gæsten siger ja", "Kun i receptionen"]),
    ("Et ekstra hotelgebyr dukker op på sidste side i bookingen. Hvad er problemet?", 1,
     "Gebyret skulle have ligget i totalprisen fra start.",
     ["Ingenting, hvis gæsten kan afbestille", "Prisen er vildledende, fordi totalen kommer for sent", "Det er en mangel ved en vare", "Det er force majeure"]),
    ("En rabatkode giver alle gæster 800 kr. Du skilter med 1.400 kr. som normalpris. Må du det?", 3,
     "Nej. Koden må ikke skabe en falsk før-pris.",
     ["Ja, hvis koden står med småt", "Ja, i en weekend", "Ja, hvis én gæst har betalt 1.400 kr.", "Nej. Før-prisen skal være reel"]),
    ("Hvad skal der stå, når en influencer får opholdet betalt?", 1,
     "Skriv Reklame synligt. Et tag er ikke nok.",
     ["Kun hotellets navn", "Ordet Reklame, så det ses med det samme", "Ingenting, hvis opholdet var kort", "Kun prisen"]),
    ("Influenceren lover en suite, som hotellet ikke har lovet. Hvad gør du først?", 0,
     "Find opslaget. Se, om det var reklame, og hvad der faktisk blev lovet.",
     ["Find opslaget og se, hvad der blev lovet", "Afvis alle klager om influencere", "Henvis kun til købeloven", "Kræv et nyt depositum"]),
    ("Må du sende nyhedsbrev til alle på en bordplan?", 2,
     "Nej. Listen må bruges til middagen. Reklame kræver samtykke.",
     ["Ja, fordi de har været i huset", "Ja, hvis mailen har et afmeldingslink", "Nej, ikke uden samtykke", "Ja, hvis du skriver Reklame i emnefeltet"]),
    ("Må et ja-felt til nyhedsbrevet være krydset af på forhånd?", 0,
     "Nej. Gæsten skal selv sætte krydset.",
     ["Nej. Gæsten skal selv sætte krydset", "Ja, hvis afmelding er nem", "Ja, ved hotelbooking", "Ja, hvis mailen er til virksomheder"]),
    ("Gæsten skriver stop til nyhedsbrevet. Hvad gør du?", 1,
     "Afmeld med det samme, og bekræft det.",
     ["Vent til næste udsendelse", "Afmeld med det samme og bekræft", "Bed gæsten ringe i åbningstiden", "Slet kun navnet, hvis gæsten finder linket"]),
    ("En mail om den konkrete booking med værelsesnummer og tid er typisk?", 3,
     "Praktisk information om aftalen er ikke reklame.",
     ["Altid spam", "Skjult reklame", "En pakkerejse", "Ikke reklame, fordi den hører til aftalen"]),
]))

QUIZZES.append(("1-3.html", "Quiz 1.3 om Markedsføring: Booking, fortrydelse og abonnement",
                "3. Booking, fortrydelse og abonnement",
                "Kunne skelne fortrydelse, afbestilling og opsigelse i servicebranchen.",
                "kapitel1.html", [
    ("Er en hotelnat købeloven?", 2,
     "Nej. En hotelnat er en ydelse. Købeloven gælder varen.",
     ["Ja, altid", "Ja, hvis gæsten betaler med kort", "Nej. Det er en ydelse", "Ja, hvis opholdet varer under to nætter"]),
    ("Hvad er forskellen på fortrydelse og afbestilling?", 0,
     "Fortrydelse er lovens 14 dage i nogle netkøb. Afbestilling følger dine vilkår eller pakkerejseloven.",
     ["Fortrydelse er lovens 14 dage i nogle netkøb. Afbestilling følger vilkårene", "De betyder det samme", "Afbestilling gælder kun varer", "Fortrydelse gælder altid en hotelnat"]),
    ("Gæsten vil fortryde en hotelnat booket til lørdag. Hvilket ord passer?", 1,
     "En fast dato følger afbestillingsvilkårene. Fortrydelsesrettens 14 dage gælder sjældent her.",
     ["Ophævelse efter købeloven", "Afbestilling", "Formodningsregel", "Kreditnota"]),
    ("Du sælger cykel, to nætter og tog til én pris. Hvad ligner det?", 3,
     "En samlet rejse med transport og overnatning kan være en pakkerejse.",
     ["Et almindeligt løsøre", "Et handelskøb", "Kun markedsføring", "En pakkerejse"]),
    ("Hvor skal afbestillingsvilkårene stå, når loven kræver et varigt medium?", 0,
     "I mailen eller som pdf. Et mundtligt vilkår i telefonen er ikke nok.",
     ["I bookingmailen eller som pdf", "Kun mundtligt i telefonen", "Kun på et skilt i receptionen", "Kun i en story på Instagram"]),
    ("En gæst ringer og afbestiller. Hvad gør du ud over at følge vilkårene?", 2,
     "Notér samtalen. I pakkerejsesager kan en telefonopringning være en afbestilling.",
     ["Ingenting, mundtligt gælder aldrig", "Kræv, at gæsten møder op", "Notér samtalen og send vilkårene på mail", "Slet bookingen uden svar"]),
    ("Spa-kortet kan kun opsiges ved personligt fremmøde. Hvad er problemet?", 1,
     "Et vilkår, der gør det urimeligt svært at stoppe, holder sjældent. Mail eller app skal være nok.",
     ["Det er force majeure", "Det kan være et urimeligt vilkår", "Det er en mangel ved en vare", "Det er skjult reklame"]),
    ("Hvad gør du først ved et beskidt værelse?", 0,
     "Ret fejlen med det samme. Tilbyd et andet værelse.",
     ["Ret fejlen og tilbyd et andet værelse", "Bed gæsten vente til næste dag", "Henvis kun til købeloven", "Kræv et nyt depositum"]),
    ("Gæsten siger, at prisen var en anden online. Hvad spørger du om?", 3,
     "Hvilken side, og har gæsten et skærmbillede. Så tjekker du bookingen.",
     ["Kun gæstens humør", "Om gæsten er influencer", "Om værelset er en vare", "Hvilken side, og om der er et skærmbillede"]),
    ("Hvilken lov starter du med ved opslag, pris, influencer og spam?", 2,
     "Det er markedsføring. Start i kapitel 1 og markedsføringsloven.",
     ["Købelovens mangelsregler", "Kun pakkerejseloven", "Markedsføringsloven", "Kun aftalelovens § 36"]),
]))

# --- Kapitel 2 ---
QUIZZES.append(("2-1.html", "Quiz 2.1 om Købeloven: Vare eller ydelse",
                "1. Vare eller ydelse",
                "Kunne se, hvornår købeloven gælder i hotel, restaurant og butik.",
                "kapitel2.html", [
    ("En gæst klager over et beskidt værelse. Er det købeloven?", 0,
     "Nej. Det er en ydelse. Se kapitel 1.",
     ["Nej. Det er en ydelse", "Ja. Alt på hotellet er købeloven", "Ja, hvis gæsten har betalt", "Kun hvis værelset er en suite"]),
    ("Gæsten køber en flaske vin i butikken. Hvilken lov?", 1,
     "Flasken er en vare. Købeloven gælder.",
     ["Pakkerejseloven", "Købeloven", "Kun markedsføringsloven", "Ingen, fordi salget sker i lobbyen"]),
    ("Firmaet køber sal, frokost og AV. Hvad er det?", 2,
     "Sal, frokost og AV er ydelser. Købeloven gælder ikke dem.",
     ["Tre varer", "En pakkerejse", "Ydelser", "Handelskøb af løsøre"]),
    ("Samme firma køber 40 flasker vand med hjem. Hvad er flaskerne?", 3,
     "Flasker, de tager med, er varer. Hold dem adskilt fra ydelsen.",
     ["En del af ydelsen, så købeloven aldrig gælder", "Force majeure", "Standardvilkår", "Varer"]),
    ("Et digitalt gavekort til en booking. Er det automatisk købeloven?", 0,
     "En booking er ofte en ydelse. Hold dig til den konkrete aftale.",
     ["Nej. En booking er ofte en ydelse", "Ja, altid", "Ja, hvis beløbet er under 1.000 kr.", "Ja, hvis det sendes på mail"]),
    ("Hvad er løsøre i den her bog?", 1,
     "Løsøre er en vare, du kan flytte. En overnatning er det ikke.",
     ["En hotelnat", "Glas, linned, badekåbe og kuffert", "En billet", "Et abonnement"]),
    ("Hvornår er gæsten i butikken typisk forbruger?", 2,
     "Når en privat gæst køber varen til sig selv, er det forbrugerkøb.",
     ["Aldrig, fordi hotellet er erhverv", "Kun hvis varen koster over 5.000 kr.", "Når gæsten køber som privat", "Kun ved handelskøb"]),
    ("Hotellet køber 200 dynebetræk af en grossist. Hvilket køb?", 0,
     "Hotellet køber til erhverv. Det er handelskøb.",
     ["Handelskøb", "Forbrugerkøb", "Pakkerejse", "En ydelse"]),
    ("Skiltet siger 199 kr. Kassen trækker 249 kr. Hvad gør du?", 1,
     "Ret det med det samme. Prisen på skiltet og i kassen skal være den samme.",
     ["Bed gæsten betale differencen uden forklaring", "Ret prisen med det samme", "Henvis til force majeure", "Kræv et depositum"]),
    ("En proppet vin ved bordet. Hvor starter du?", 3,
     "Flasken er en vare. Købeloven gælder manglen.",
     ["Kun markedsføringsloven", "Pakkerejseloven", "Ingen lov, fordi det er service", "Købeloven"]),
]))

QUIZZES.append(("2-2.html", "Quiz 2.2 om Købeloven: Mangel og afhjælpning",
                "2. Mangel og afhjælpning",
                "Kunne se en mangel og vælge det rigtige første skridt.",
                "kapitel2.html", [
    ("Badekåbens søm går op efter tre uger ved normal brug. Hvad er første skridt?", 1,
     "Afhjælpning. Reparation eller en ny kåbe inden for rimelig tid.",
     ["Ophævelse med det samme", "Afhjælpning inden for rimelig tid", "Afvis, fordi der er gået over 48 timer", "Kræv et nyt køb til fuld pris"]),
    ("Gæsten fortryder farven på en T-shirt dagen efter. Er det en mangel?", 2,
     "Nej. Fortrydelse er ikke en mangel.",
     ["Ja, farve er altid en mangel", "Ja, i de første 14 dage", "Nej. Der er ingen fejl ved varen", "Ja, hvis T-shirten var på udsalg"]),
    ("Lampen på udsalg tænder ikke. Ridsen var oplyst. Hvad gælder?", 0,
     "Den oplyste ridse er ikke en mangel. En lampe, der ikke tænder, er en mangel.",
     ["Det, at lampen ikke tænder, er en mangel", "Hele købet er uden reklamation, fordi det er udsalg", "Kun ridsen kan påklages", "Gæsten skal vente to år, før du skal reagere"]),
    ("Et skilt siger ingen ombytning på udsalgsvarer. Gæsten køber en skjult defekt. Holder skiltet?", 3,
     "Nej. Du kan ikke fjerne reklamationsretten i et forbrugerkøb.",
     ["Ja, fordi gæsten så skiltet", "Ja, på alle udsalgsvarer", "Ja, hvis kvitteringen gentager skiltet", "Nej. Skiltet fjerner ikke reklamationsretten"]),
    ("Chokoladen i minibaren er en uge over dato. Hvad tilbyder du?", 1,
     "Det er en mangel ved en vare. Tilbyd pengene tilbage eller en ny vare.",
     ["Ingenting. Minibaren er en ydelse", "Pengene tilbage eller en ny vare", "Kun en undskyldning", "Et nyt værelse"]),
    ("Du kan ikke reparere kufferten inden for rimelig tid. Hvad kan gæsten?", 2,
     "Gæsten kan hæve købet. Pengene går tilbage, og gæsten afleverer varen.",
     ["Kun bede om rabat og beholde kufferten", "Vente i to år", "Hæve købet", "Ingenting, fordi du har påbegyndt en reparation"]),
    ("Reparationen af højttaleren har stået stille i otte dage, og reservedelen mangler. Kan gæsten hæve?", 0,
     "Ja, hvis det står klart, at reparationen ikke sker inden for rimelig tid.",
     ["Ja, hvis reparationen ikke sker inden for rimelig tid", "Nej. Du har altid ret til at reparere", "Nej, før der er gået to år", "Kun hvis varen kostede over 5.000 kr."]),
    ("Hvad er et afslag?", 1,
     "Gæsten beholder varen eller opholdet, men betaler mindre.",
     ["Aftalen rulles helt tilbage", "Prisen sættes ned, og aftalen fortsætter", "Gæsten skal købe en ny vare", "Du sender en reklame"]),
    ("Gaven er købt i butikken. Lynlåsen går i stykker efter en måned. Må gavemodtageren reklamere?", 3,
     "Ja, typisk. Bed om kvittering eller anden dokumentation.",
     ["Nej. Kun den, der betalte, må klage", "Nej. Gaver er uden for købeloven", "Kun hvis gaven kostede over 500 kr.", "Ja, typisk, med kvittering eller anden dokumentation"]),
    ("Hvad er forskellen på garanti og reklamationsret?", 2,
     "Reklamationsretten følger loven. Garantien er et ekstra løfte oveni.",
     ["Garantien fjerner reklamationsretten", "Kun garantien gælder i butikken", "Reklamationsretten følger loven. Garantien er et ekstra løfte", "Reklamationsret gælder kun ydelser"]),
]))

QUIZZES.append(("2-3.html", "Quiz 2.3 om Købeloven: Frist, bevis og handel",
                "3. Frist, bevis og handel",
                "Kunne reklamationsfrist, formodning og handelskøb.",
                "kapitel2.html", [
    ("Fejlen viser sig efter otte måneder i et forbrugerkøb. Hvem skal typisk bevise, at fejlen ikke var der ved købet?", 0,
     "Dig. Formodningen gælder det første år.",
     ["Dig, sælgeren", "Altid gæsten", "Grossisten, også når du solgte varen", "Ingen. Sagen er forældet efter seks måneder"]),
    ("Hvornår er reklamationsfristen typisk udløbet i et forbrugerkøb?", 1,
     "To år efter leveringen. Otte måneder er stadig inden for fristen.",
     ["Efter 48 timer", "To år efter leveringen", "Efter seks måneder", "Når garantien udløber, også hvis den er på tre måneder"]),
    ("Hotellet får 100 glas. Ti er flækkede i kassen. Hvad gør du?", 2,
     "Reklamér med det samme. Det er handelskøb.",
     ["Vent til næste måned", "Brug forbrugerkøbets toårsfrist over for gæsten", "Reklamér med det samme over for leverandøren", "Smid glassene ud uden besked"]),
    ("Du bestiller 50 hvide duge. Der kommer 50 råhvide, og arrangementet er i morgen. Hvad gør du først?", 0,
     "Reklamér med det samme og tag et billede. Det er handelskøb.",
     ["Reklamér med det samme og dokumentér fejlen", "Vent, til arrangementet er overstået", "Brug forbrugerkøbets formodningsregel", "Kald det en pakkerejse"]),
    ("Hvornår går risikoen normalt over i butikken?", 3,
     "Når gæsten har fået varen og betalt.",
     ["Først efter to år", "Når gæsten forlader hotellet", "Aldrig, hvis der er garanti", "Ved leveringen i butikken"]),
    ("Webshoppen lover en velkomstpakke på en bestemt dato. Pakken er tre dage forsinket. Hvad er nok?", 1,
     "Svar hurtigt, forklar hvorfor, og tilbyd en løsning.",
     ["En automatisk mail om travlhed", "Et hurtigt svar med forklaring og en løsning", "Ingenting, fordi tre dage er kort tid", "Et nyt depositum"]),
    ("Må du i et handelskøb aftale en kortere reklamationsfrist end i forbrugerkøb?", 2,
     "Ja. Reglerne er deklaratoriske mellem erhvervsdrivende. En sen klage kan blive afvist.",
     ["Nej, toårsfristen gælder altid", "Nej, kun hvis grossisten er forbruger", "Ja. Aftal fristen, og reklamér hurtigt", "Kun hvis varen er en ydelse"]),
    ("Gæsten vil have taxaen betalt, fordi en fejl i huset gjorde ham forsinket. Hvad skal der til, før det er erstatning?", 0,
     "Gæsten skal kunne vise et tab. Et almindeligt skuffet ophold er ikke nok.",
     ["Et konkret tab, som gæsten kan vise", "Altid, når gæsten er utilfreds", "Kun hvis det er en vare", "Kun hvis Forbrugerombudsmanden har dømt"]),
    ("Hvem står stærkest, når der er uenighed om, hvad der blev sagt?", 1,
     "Den, der kan dokumentere det. Gem kvittering, mail og billeder.",
     ["Altid gæsten", "Den, der kan dokumentere det", "Altid hotellet", "Den, der ringer først"]),
    ("En flaske, en souvenir, en T-shirt og linned. Hvor starter du?", 3,
     "Det er varer. Købeloven i kapitel 2.",
     ["Kun markedsføringsloven", "Pakkerejseloven", "Forbrugeraftalelovens spamregler", "Købeloven"]),
]))

# --- Kapitel 3 ---
QUIZZES.append(("3-1.html", "Quiz 3.1 om Ordliste: Ordene i receptionen",
                "1. Ordene i receptionen",
                "Kunne bruge de rigtige ord, når gæsten står foran dig.",
                "kapitel3.html", [
    ("Gæsten udebliver uden at afbestille. Hvad hedder det?", 0,
     "Udeblivelse. Branchen siger også no-show. Vilkårene afgør betalingen.",
     ["Udeblivelse", "Ophævelse", "Afhjælpning", "Formodningsregel"]),
    ("Hvad er et depositum?", 1,
     "Et beløb, gæsten betaler forud som sikkerhed. Skriv, hvornår det kommer retur.",
     ["En rabat", "Et beløb forud som sikkerhed", "En mangel", "En reklame"]),
    ("Hvad er en bekræftelse?", 2,
     "Det skriftlige bevis for bookingen: værelse, pris og afbestilling.",
     ["Et mundtligt løfte i receptionen", "Et like på Instagram", "Mail med værelse, pris og afbestilling", "En kreditnota"]),
    ("Hvad er force majeure?", 3,
     "En ekstraordinær hindring uden for din kontrol. Et travlt køkken er det ikke.",
     ["Et almindeligt travlt køkken", "En forkert pris", "En proppet vin", "En ekstraordinær hindring uden for din kontrol"]),
    ("Hvad er en formidler?", 0,
     "Den, der formidler aftalen, uden selv at være leverandør. Sig, hvem gæsten aftaler med.",
     ["En platform mellem gæst og hotel", "Altid hotellet selv", "Kun en ankenævn", "Kun køberen"]),
    ("Hvad er en kreditnota?", 1,
     "Et dokument, der trækker en tidligere faktura ned. Skriv beløb og hvilken faktura.",
     ["En ny reklame", "Et dokument, der sætter en faktura ned", "Et depositum", "Et samtykke"]),
    ("Hvad er overbooking?", 2,
     "Flere bookinger end der er plads til. Flyt gæsten, eller giv pengene tilbage.",
     ["Gæsten afbestiller i tide", "En mangel ved en vare", "Flere bookinger end der er plads til", "En skjult reklame"]),
    ("Hvad er en udenretlig løsning?", 0,
     "En løsning uden domstol. For eksempel et andet værelse og et afslag.",
     ["Et andet værelse og et afslag, uden domstol", "En dom fra byretten", "En bøde fra Forbrugerombudsmanden", "En ny lov"]),
    ("Hvad er en væsentlig mangel?", 3,
     "En fejl, der betyder noget for aftalen. Intet vand på badeværelset er væsentligt.",
     ["En oplyst ridse", "Et like", "En rabatkode", "En fejl, der betyder noget for aftalen"]),
    ("Hvornår er gæstens ja en accept?", 1,
     "Når gæsten siger ja til et tilbud, for eksempel ved at bestille og betale. At synes godt om et opslag er ikke en accept.",
     ["Når gæsten synes godt om opslaget", "Når gæsten bestiller og betaler", "Når du sender et nyhedsbrev", "Når gæsten går forbi hotellet"]),
]))

QUIZZES.append(("3-2.html", "Quiz 3.2 om Ordliste: Forvekslinger",
                "2. Forvekslinger",
                "Kunne holde de ord fra hinanden, som gæster blander sammen.",
                "kapitel3.html", [
    ("Hvad er forskellen på afbestilling og fortrydelse?", 0,
     "Afbestilling følger vilkår eller pakkerejse. Fortrydelse er lovens 14 dage i nogle netkøb.",
     ["Afbestilling følger vilkårene. Fortrydelse er lovens 14 dage i nogle netkøb", "De betyder det samme", "Fortrydelse gælder kun handelskøb", "Afbestilling gælder kun varer"]),
    ("Hvad er forskellen på mangel og fortrydelse?", 1,
     "En mangel er noget galt. Fortrydelse er omfortrydelse uden fejl.",
     ["De betyder det samme", "Mangel er en fejl. Fortrydelse er uden fejl", "Fortrydelse gælder kun ydelser", "Mangel gælder kun Instagram"]),
    ("Hvad er forskellen på afhjælpning og ophævelse?", 2,
     "Afhjælpning retter fejlen. Ophævelse ruller købet tilbage.",
     ["Ophævelse er altid første skridt", "Afhjælpning gælder kun ydelser", "Afhjælpning retter. Ophævelse ruller købet tilbage", "Ophævelse kræver en domstol"]),
    ("Hvad er forskellen på vildledning og udeladelse?", 3,
     "Vildledning er forkert information. Udeladelse er det, du glemmer at sige.",
     ["Udeladelse er altid strafbart, vildledning er det aldrig", "De gælder kun priser", "Udeladelse gælder kun pakkerejser", "Vildledning er forkert info. Udeladelse er det, du ikke siger"]),
    ("Hvad er forskellen på samtykke og en bookingmail?", 0,
     "Bookingmailen hører til aftalen. Reklame kræver samtykke eller undtagelsen om lignende varer.",
     ["Bookingmailen hører til aftalen. Reklame kræver samtykke", "De er begge spam", "Samtykke gælder kun varer", "Bookingmailen er altid skjult reklame"]),
    ("Hvad er forskellen på forbrugerkøb og handelskøb?", 1,
     "Gæsten i butikken er ofte forbruger. Grossistleverancen er handelskøb.",
     ["De har samme frister altid", "Butikken er ofte forbrugerkøb. Grossisten er handelskøb", "Handelskøb gælder kun ydelser", "Forbrugerkøb gælder kun pakkerejser"]),
    ("Hvad er forskellen på vare og ydelse?", 2,
     "Varen kan du lægge i en pose. Ydelsen kan du ikke. Købeloven gælder varen.",
     ["De styres af samme lov", "Ydelsen er altid købeloven", "Varen kan lægges i en pose. Ydelsen kan ikke", "En hotelnat er en vare"]),
    ("Hvad er forskellen på garanti og reklamationsret?", 0,
     "Reklamationsretten følger loven. Garantien er et ekstra løfte.",
     ["Reklamationsretten følger loven. Garantien er et ekstra løfte", "Garantien fjerner reklamationsretten", "Kun garantien gælder en souvenir", "Reklamationsret gælder kun abonnementer"]),
    ("Hvad er forskellen på tilbud og accept?", 3,
     "Tilbuddet er det, du foreslår. Accepten er gæstens ja.",
     ["Accepten kommer altid først", "De er begge reklame", "Tilbuddet er gæstens klage", "Tilbuddet er dit forslag. Accepten er gæstens ja"]),
    ("Hvad er forskellen på opsigelse og ophævelse?", 1,
     "Opsigelse stopper et abonnement efter reglerne. Ophævelse ruller et køb tilbage på grund af en mangel.",
     ["De betyder det samme", "Opsigelse stopper et abonnement. Ophævelse ruller et køb tilbage", "Ophævelse gælder kun nyhedsbreve", "Opsigelse kræver en domstol"]),
]))

QUIZZES.append(("3-3.html", "Quiz 3.3 om Ordliste: Hvilken lov",
                "3. Hvilken lov",
                "Kunne vælge den rigtige lov, før du svarer gæsten.",
                "kapitel3.html", [
    ("Opslag, pris, influencer og spam. Hvor starter du?", 0,
     "Markedsføringsloven i kapitel 1.",
     ["Markedsføringsloven", "Købelovens mangelsregler", "Kun pakkerejseloven", "Kun aftalelovens § 36"]),
    ("Flaske, souvenir, T-shirt og linned. Hvor starter du?", 2,
     "Købeloven i kapitel 2.",
     ["Kun markedsføringsloven", "Pakkerejseloven", "Købeloven", "Forbrugeraftalelovens spamregler"]),
    ("Fly, hotel og cykel til én samlet pris. Hvad ligner det?", 1,
     "En pakkerejse. Brug pakkerejselovens afbestillingsregler.",
     ["Almindeligt løsøre", "En pakkerejse", "Et handelskøb", "En kreditnota"]),
    ("Urimelige standardvilkår over for en forbruger. Hvor kigger du?", 3,
     "Aftalelovens § 36 og § 38 c.",
     ["Kun købelovens risikoovergang", "Kun markedsføringslovens § 11 om børn", "Kun EAL", "Aftalelovens regler om urimelige vilkår"]),
    ("Et løbende spa-kort, som gæsten vil stoppe. Hvilket regelsæt er relevant?", 0,
     "Forbrugeraftalelovens regler om opsigelse af løbende aftaler, sammen med kapitel 1.",
     ["Reglerne om opsigelse af løbende aftaler", "Købelovens toårsfrist", "Kun formodningsreglen", "Kun risikoovergangen"]),
    ("Grossisten leverer hullerede betræk. Hvilket køb?", 1,
     "Handelskøb. Reklamér samme dag.",
     ["Forbrugerkøb", "Handelskøb", "Pakkerejse", "Skjult reklame"]),
    ("En hotelklage, som du ikke kan løse. Hvor kan den ende?", 2,
     "Ankenævnet for Hotel, Restaurant og Turisme. En pakkerejse kan gå til Pakkerejse-Ankenævnet.",
     ["Altid i Højesteret først", "Kun hos politiet", "Et ankenævn", "Kun i købelovens § 1"]),
    ("Gæsten vil have en praktisk mail om bryllupsmiddagen. Kræver det samtykke?", 0,
     "Nej. Praktisk information om aftalen er ikke reklame.",
     ["Nej. Det hører til aftalen", "Ja, altid", "Ja, hvis der er over 10 gæster", "Ja, hvis mailen har et emnefelt"]),
    ("Gæsten vil på tilbudslisten til næste weekend. Kræver det samtykke?", 3,
     "Ja. Reklame for næste weekend kræver samtykke.",
     ["Nej, fordi gæsten har boet på hotellet", "Nej, hvis du skriver Reklame", "Nej, hvis afmelding findes", "Ja"]),
    ("Du kan ikke skaffe vand på værelset. Hvad er en udenretlig løsning?", 1,
     "Flyt gæsten og giv et afslag, før sagen ender i et nævn.",
     ["Bed gæsten vente til næste morgen uden alternativ", "Flyt gæsten og giv et afslag", "Slet bookingen uden besked", "Kræv et nyt depositum"]),
]))


LINKS = {
    "kapitel1.html": [
        ("quiz/1-1.html", "Quiz 1.1 om Markedsføring: Reklame og aftale"),
        ("quiz/1-2.html", "Quiz 1.2 om Markedsføring: Pris, influencer og mail"),
        ("quiz/1-3.html", "Quiz 1.3 om Markedsføring: Booking, fortrydelse og abonnement"),
    ],
    "kapitel2.html": [
        ("quiz/2-1.html", "Quiz 2.1 om Købeloven: Vare eller ydelse"),
        ("quiz/2-2.html", "Quiz 2.2 om Købeloven: Mangel og afhjælpning"),
        ("quiz/2-3.html", "Quiz 2.3 om Købeloven: Frist, bevis og handel"),
    ],
    "kapitel3.html": [
        ("quiz/3-1.html", "Quiz 3.1 om Ordliste: Ordene i receptionen"),
        ("quiz/3-2.html", "Quiz 3.2 om Ordliste: Forvekslinger"),
        ("quiz/3-3.html", "Quiz 3.3 om Ordliste: Hvilken lov"),
    ],
}


if __name__ == "__main__":
    (ROOT / "quiz").mkdir(exist_ok=True)
    for item in QUIZZES:
        render(*item)
    for name, links in LINKS.items():
        insert_links(name, links)
    index = ROOT / "index.html"
    index.write_text(index.read_text().replace("?v=4", "?v=5"))
    print("quizzer", len(QUIZZES))
