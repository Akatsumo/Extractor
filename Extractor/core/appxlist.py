import string

a_to_zList = {
    f"appxSection_{letter}": {"name": letter}
    for letter in string.ascii_uppercase
}


appxapis = [
    {
        "name": "A4Agricos",
        "api": "a4agricosapi.classx.co.in"
    },
    {
        "name": "A4Shub",
        "api": "a4shubapi.classx.co.in"
    },
    {
        "name": "Aacharyaayurveda",
        "api": "aacharyaayurvedaapi.classx.co.in"
    },
    {
        "name": "Aadarshonlineeducation",
        "api": "aadarshonlineeducationapi.classx.co.in"
    },
    {
        "name": "Aadharclasses",
        "api": "aadharclassesjhunjhunuapi.classx.co.in"
    },
    {
        "name": "Aadiwasikritisamiti",
        "api": "aadiwasikritisamitiapi.classx.co.in"
    },
    {
        "name": "Aagaazinstitution",
        "api": "aagaazinstitutionapi.classx.co.in"
    },
    {
        "name": "Aagamclasses",
        "api": "aagamclassesapi.classx.co.in"
    },
    {
        "name": "Aakarlearningapp",
        "api": "aakarlearningapi.classx.co.in"
    },
    {
        "name": "Aakartutorials",
        "api": "aakartutorialsapi.classx.co.in"
    },
    {
        "name": "Aakashkrishnaacademy",
        "api": "aakashkrishnaacademyapi.classx.co.in"
    },
    {
        "name": "Aalphaglobalinstitute",
        "api": "aalphaglobalinstituteapi.classx.co.in"
    },
    {
        "name": "Aaonlinesolution",
        "api": "aaonlinesolutionapi.classx.co.in"
    },
    {
        "name": "Aapkipathshala",
        "api": "aapkipathshalaapi.classx.co.in"
    },
    {
        "name": "Aapnipadhai",
        "api": "aapnipadhaiapi.classx.co.in"
    },
    {
        "name": "Aarambhacademy",
        "api": "aarambhacademyapi.classx.co.in"
    },
    {
        "name": "Aarambhvidyapith",
        "api": "aarambhvidyapithapi.classx.co.in"
    },
    {
        "name": "Aarohacademy",
        "api": "aarohacademyapi.classx.co.in"
    },
    {
        "name": "Aash",
        "api": "aashapi.appx.co.in"
    },
    {
        "name": "Aasthabhavthramayan",
        "api": "aasthabhavathramayanapi.classx.co.in"
    },
    {
        "name": "Aatmnirmanacademy",
        "api": "aatmnirmanacademyapi.classx.co.in"
    },
    {
        "name": "Abhigyaias",
        "api": "abhigyaiasapi.classx.co.in"
    },
    {
        "name": "Abhimanyuacademyindore",
        "api": "abhimanyuacademyindoreapi.classx.co.in"
    },
    {
        "name": "Abhinanadanclasseskotputali",
        "api": "abhinanadanclasseskotputaliapi.classx.co.in"
    },
    {
        "name": "Abhinavmotordrivingschoolapp",
        "api": "abhinavmotordrivingschoolapi.classx.co.in"
    },
    {
        "name": "Abhishektehanguriyaclasses",
        "api": "abhishektehanguriyaclassesapi.classx.co.in"
    },
    {
        "name": "Abhiyaanacademyforiasips",
        "api": "abhiyaanacademyiasipsapi.classx.co.in"
    },
    {
        "name": "Abhyaasagriacademy",
        "api": "abhyaasagriacademyapi.classx.co.in"
    },
    {
        "name": "Abhyaasagriacademy20",
        "api": "abhyaasagriacademy20api.classx.co.in"
    },
    {
        "name": "Abhyasa",
        "api": "abhyasaapi.classx.co.in"
    },
    {
        "name": "Abhyasmitra",
        "api": "abhyasmitraapi.classx.co.in"
    },
    {
        "name": "Abjeetenge",
        "api": "abjeetengeapi.classx.co.in"
    },
    {
        "name": "Ablazeacademy",
        "api": "ablazeacademyapi.classx.co.in"
    },
    {
        "name": "Abplearning",
        "api": "abplearningapi.classx.co.in"
    },
    {
        "name": "Academiczoneclassbuddy",
        "api": "academiczoneapi.classx.co.in"
    },
    {
        "name": "Academiyaofficialliveclassesquizpdf",
        "api": "academiyaofficialapi.classx.co.in"
    },
    {
        "name": "Academy99Byanoopjain",
        "api": "academyanoopjainapi.classx.co.in"
    },
    {
        "name": "Academycommerce",
        "api": "academycommerceapi.classx.co.in"
    },
    {
        "name": "Academyofclinicalresearch",
        "api": "academyclinicalresearchapi.classx.co.in"
    },
    {
        "name": "Acewithease",
        "api": "acewitheaseapi.classx.co.in"
    },
    {
        "name": "Acfofficial",
        "api": "acfofficialapi.classx.co.in"
    },
    {
        "name": "Acharyakulambiharnaveensir",
        "api": "acharyakulambiharnaveenapi.classx.co.in"
    },
    {
        "name": "Achievecapf",
        "api": "achievecapfapi.classx.co.in"
    },
    {
        "name": "Achiever",
        "api": "achieversacademyapi.appx.co.in"
    },
    {
        "name": "Achieverpoint",
        "api": "achieverpointapi.classx.co.in"
    },
    {
        "name": "Achieversacademy",
        "api": "achieversacademyapi.classx.co.in"
    },
    {
        "name": "Achieversadda247",
        "api": "achieversadda247api.classx.co.in"
    },
    {
        "name": "Achiverseducation",
        "api": "achiverseducationapi.classx.co.in"
    },
    {
        "name": "Aclasseducation",
        "api": "aclasseducationapi.classx.co.in"
    },
    {
        "name": "Acmecommerceclasses",
        "api": "acmecommerceclassesapi.classx.co.in"
    },
    {
        "name": "Acracademy",
        "api": "acracademyapi.classx.co.in"
    },
    {
        "name": "Adarmypoint",
        "api": "adarmypointapi.classx.co.in"
    },
    {
        "name": "Adarshacademys20",
        "api": "adarshacademyapi.classx.co.in"
    },
    {
        "name": "Adarshiasacademy",
        "api": "adarshiasacademyapi.classx.co.in"
    },
    {
        "name": "Adconcept",
        "api": "adconceptapi.classx.co.in"
    },
    {
        "name": "Adhigamclassesjaipur",
        "api": "adhigamclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Adhijayclasses",
        "api": "adhijayclassesapi.classx.co.in"
    },
    {
        "name": "Adhyayan",
        "api": "adhyayanmantraapi.appx.co.in"
    },
    {
        "name": "Adhyayankendra",
        "api": "adhyayankendraapi.classx.co.in"
    },
    {
        "name": "Adinarayanaacademy2",
        "api": "adinarayanaacademytwoapi.classx.co.in"
    },
    {
        "name": "Adityanareshmathsclasses",
        "api": "adityanareshmathsclassesapi.classx.co.in"
    },
    {
        "name": "Adityaschoolofbanking",
        "api": "adityaschoolbankingapi.classx.co.in"
    },
    {
        "name": "Adlive",
        "api": "adliveapi.classx.co.in"
    },
    {
        "name": "Advancempsc",
        "api": "advancempscapi.classx.co.in"
    },
    {
        "name": "Agastyasacademy",
        "api": "agastyasacademyapi.classx.co.in"
    },
    {
        "name": "Agentsuvidha",
        "api": "agentsuvidhaapi.classx.co.in"
    },
    {
        "name": "Agkrishnaspokenhindi",
        "api": "agkrishnaspokenhindiapi.classx.co.in"
    },
    {
        "name": "Agnihotriclasses",
        "api": "agnihotriclassesapi.classx.co.in"
    },
    {
        "name": "Agnitutor",
        "api": "agnitutorapi.classx.co.in"
    },
    {
        "name": "Agniveerguruji",
        "api": "agniveergurujiapi.classx.co.in"
    },
    {
        "name": "Agniveerstudyarmynavyairforce",
        "api": "agniveerstudyarmynavyairforceapi.classx.co.in"
    },
    {
        "name": "Agogeclassesacharyagram",
        "api": "agogeclassesapi.classx.co.in"
    },
    {
        "name": "Agradeclasses",
        "api": "agradeclassesapi.classx.co.in"
    },
    {
        "name": "Agriacademyhisar",
        "api": "agriacademyhisarapi.classx.co.in"
    },
    {
        "name": "Agriaware",
        "api": "agriawareapi.classx.co.in"
    },
    {
        "name": "Agricoaching",
        "api": "agricoachingapi.appx.co.in"
    },
    {
        "name": "Agricoaching",
        "api": "agricoachingapi.classx.co.in"
    },
    {
        "name": "Agricultureacademyjaipur",
        "api": "agricultureacademyjaipurapi.classx.co.in"
    },
    {
        "name": "Agricultureadda",
        "api": "agricultureaddaapi.classx.co.in"
    },
    {
        "name": "Agricultureexpert",
        "api": "agricultureexpertapi.classx.co.in"
    },
    {
        "name": "Agriculturegk",
        "api": "agriculturegkapi.classx.co.in"
    },
    {
        "name": "Agriculturepadhaiexamprep",
        "api": "agriculturepadhaiexamprepapi.classx.co.in"
    },
    {
        "name": "Agrieducators",
        "api": "agrieducatorsapi.classx.co.in"
    },
    {
        "name": "Agriexamlibrary",
        "api": "agriexamlibraryapi.classx.co.in"
    },
    {
        "name": "Agrimentors",
        "api": "agrimentorsapi.classx.co.in"
    },
    {
        "name": "Agrimshiksha",
        "api": "agrimshikshaapi.classx.co.in"
    },
    {
        "name": "Agripathclassesudaipur",
        "api": "agripathclassesudaipurapi.classx.co.in"
    },
    {
        "name": "Agripmfqualityagriculture",
        "api": "agripmfqualityagricultureapi.classx.co.in"
    },
    {
        "name": "Agripowerjaipurcoaching",
        "api": "agripowerjaipurcoachingapi.classx.co.in"
    },
    {
        "name": "Agrirevolution",
        "api": "agrirevolutionapi.classx.co.in"
    },
    {
        "name": "Agriselectionpoint",
        "api": "agriselectionpointapi.classx.co.in"
    },
    {
        "name": "Agritubeplus",
        "api": "agritubeplusapi.classx.co.in"
    },
    {
        "name": "Agriyug",
        "api": "agriyugapi.classx.co.in"
    },
    {
        "name": "Agrizoneclasses",
        "api": "agrizoneclassesapi.classx.co.in"
    },
    {
        "name": "Aiapgetpocketapp",
        "api": "aiapgetpocketappapi.classx.co.in"
    },
    {
        "name": "Aifmeducation",
        "api": "aifmeducationapi.classx.co.in"
    },
    {
        "name": "Aimers",
        "api": "aimersapi.classx.co.in"
    },
    {
        "name": "Aimersacademy",
        "api": "aimersacademyapi.classx.co.in"
    },
    {
        "name": "Aiminghigh",
        "api": "aiminghighapi.classx.co.in"
    },
    {
        "name": "Ajaybeniwalmaths",
        "api": "ajaybeniwalmathsapi.classx.co.in"
    },
    {
        "name": "Ajaygurukul",
        "api": "ajaygurukulapi.classx.co.in"
    },
    {
        "name": "Ajaynyolmathematics",
        "api": "ajaynyolmathematicsapi.classx.co.in"
    },
    {
        "name": "Ajitchahalschallengersacademy",
        "api": "ajitchahalchallengersacademyapi.classx.co.in"
    },
    {
        "name": "Akashlectureonline",
        "api": "akashlectureonlineapi.classx.co.in"
    },
    {
        "name": "Akashtalks",
        "api": "akashtalksapi.classx.co.in"
    },
    {
        "name": "Akb",
        "api": "akbpublicationeducationapi.classx.co.in"
    },
    {
        "name": "Akdubeytutorials",
        "api": "akdubeytutorialsapi.classx.co.in"
    },
    {
        "name": "Akeduspot",
        "api": "akeduspotapi.classx.co.in"
    },
    {
        "name": "Akengineeringacademy",
        "api": "akengineeringacademyapi.classx.co.in"
    },
    {
        "name": "Akfoundation",
        "api": "akfoundationapi.classx.co.in"
    },
    {
        "name": "Akihimselfschoolofmusic",
        "api": "akihimselfschoolmusicapi.classx.co.in"
    },
    {
        "name": "Aksgroup",
        "api": "aksgroupapi.classx.co.in"
    },
    {
        "name": "Akshaybhise",
        "api": "akshaybhiseapi.classx.co.in"
    },
    {
        "name": "Akstechnicalclasses",
        "api": "akstechnicalclassesapi.classx.co.in"
    },
    {
        "name": "Akstudy",
        "api": "akstudyapi.classx.co.in"
    },
    {
        "name": "Alakclasses",
        "api": "alakclassesapi.classx.co.in"
    },
    {
        "name": "Alkamedicalclasses",
        "api": "alkamedicalclassesapi.classx.co.in"
    },
    {
        "name": "Allexamadda",
        "api": "allexamaddaapi.classx.co.in"
    },
    {
        "name": "Allexamguru",
        "api": "allexamguruapi.classx.co.in"
    },
    {
        "name": "Allexamlive",
        "api": "allexamapi.classx.co.in"
    },
    {
        "name": "Allexamplace",
        "api": "allexamplaceapi.classx.co.in"
    },
    {
        "name": "Allfintalk",
        "api": "allfintalkapi.classx.co.in"
    },
    {
        "name": "Alliedias",
        "api": "alliediasapi.classx.co.in"
    },
    {
        "name": "Allindiafoundation",
        "api": "allindiafoundationapi.classx.co.in"
    },
    {
        "name": "Alltimetoppers",
        "api": "alltimetoppersapi.classx.co.in"
    },
    {
        "name": "Aloft",
        "api": "aloftpreparationapi.classx.co.in"
    },
    {
        "name": "Alphainstitutepro",
        "api": "alphainstituteproapi.classx.co.in"
    },
    {
        "name": "Alphaplus",
        "api": "alphaplusapi.classx.co.in"
    },
    {
        "name": "Alphaspokenenglish",
        "api": "alphaspokenenglishapi.classx.co.in"
    },
    {
        "name": "Amajawan",
        "api": "amajawanapi.classx.co.in"
    },
    {
        "name": "Amanpathshala",
        "api": "amanpathshalaapi.classx.co.in"
    },
    {
        "name": "Amansir",
        "api": "amansirenglishapi.classx.co.in"
    },
    {
        "name": "Amarnadhsirclasses",
        "api": "amarnadhsirclassesapi.classx.co.in"
    },
    {
        "name": "Amazoncampus",
        "api": "amazoncampusapi.classx.co.in"
    },
    {
        "name": "Amitsacademy",
        "api": "amitsacademyapi.classx.co.in"
    },
    {
        "name": "Amitsilani",
        "api": "amitsilaniapi.classx.co.in"
    },
    {
        "name": "Amittaldamentorship",
        "api": "amittaldamentorshipapi.classx.co.in"
    },
    {
        "name": "Amlearning",
        "api": "amlearningapi.classx.co.in"
    },
    {
        "name": "Amolandhalea2Talk",
        "api": "amolandhalea2talkapi.classx.co.in"
    },
    {
        "name": "Amolpatil",
        "api": "amolpatilapi.classx.co.in"
    },
    {
        "name": "Amolpatilmathsreasoning",
        "api": "amolpatilmathsreasoningapi.classx.co.in"
    },
    {
        "name": "Ampledigital",
        "api": "ampledigitalapi.classx.co.in"
    },
    {
        "name": "Amplitudeclassesjaipur",
        "api": "amplitudeclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Amruthaiasacademy",
        "api": "amruthaiasacademyapi.classx.co.in"
    },
    {
        "name": "Amsacademy",
        "api": "amsacademyapi.classx.co.in"
    },
    {
        "name": "Analysiseclasses",
        "api": "analysiseclassesapi.classx.co.in"
    },
    {
        "name": "Analystias",
        "api": "analystiasapi.classx.co.in"
    },
    {
        "name": "Analyticaledupointlive",
        "api": "analyticaledupointliveapi.classx.co.in"
    },
    {
        "name": "Angelacademy",
        "api": "angelacademyapi.classx.co.in"
    },
    {
        "name": "Angrezimitra",
        "api": "angrezimitraapi.classx.co.in"
    },
    {
        "name": "Anilsacademy",
        "api": "anilsacademyapi.classx.co.in"
    },
    {
        "name": "Anilsiriti",
        "api": "anilsiritiapi.classx.co.in"
    },
    {
        "name": "Animateme",
        "api": "animatemeapi.classx.co.in"
    },
    {
        "name": "Anjaneyacademy",
        "api": "anjaneyacademyapi.classx.co.in"
    },
    {
        "name": "Ankitsingh",
        "api": "ankitsinghapi.classx.co.in"
    },
    {
        "name": "Ankuramtv",
        "api": "ankuramtvapi.classx.co.in"
    },
    {
        "name": "Ankurias",
        "api": "ankuriasapi.classx.co.in"
    },
    {
        "name": "Annadatabydrrschoudhary",
        "api": "annadatadrrschoudharyapi.classx.co.in"
    },
    {
        "name": "Anrlogics",
        "api": "anrlogicsapi.classx.co.in"
    },
    {
        "name": "Anugrahaacademy",
        "api": "anugrahaacademyapi.classx.co.in"
    },
    {
        "name": "Anuragtyagiclasses",
        "api": "anuragtyagiclassesapi.classx.co.in"
    },
    {
        "name": "Anushasanclasseswhiteboardacademy",
        "api": "anushasanclassesapi.classx.co.in"
    },
    {
        "name": "Anushastudycentre",
        "api": "anushastudycentreapi.classx.co.in"
    },
    {
        "name": "Anveshangroup",
        "api": "anveshangroupapi.classx.co.in"
    },
    {
        "name": "Apexartsacademy",
        "api": "apexartsacademyapi.classx.co.in"
    },
    {
        "name": "Apexgpat",
        "api": "apexgpatapi.classx.co.in"
    },
    {
        "name": "Apinstitute",
        "api": "apinstituteapi.classx.co.in"
    },
    {
        "name": "Apnaambition",
        "api": "apnaambitionapi.classx.co.in"
    },
    {
        "name": "Apnanotes",
        "api": "apnanotesapi.classx.co.in"
    },
    {
        "name": "Apnavidyalaya",
        "api": "apnavidyalayaapi.classx.co.in"
    },
    {
        "name": "Apnipathsala",
        "api": "apnipathshalaapi.classx.co.in"
    },
    {
        "name": "Apnischool",
        "api": "apnischoolapi.classx.co.in"
    },
    {
        "name": "Apnishiksha",
        "api": "apnishikshaapi.classx.co.in"
    },
    {
        "name": "Apniuniversity",
        "api": "apniuniversityapi.classx.co.in"
    },
    {
        "name": "Appsc",
        "api": "appscapi.classx.co.in"
    },
    {
        "name": "Appxhybrid",
        "api": "appxhybridapi.classx.co.in"
    },
    {
        "name": "Appxstore",
        "api": "appxstoreapi.classx.co.in"
    },
    {
        "name": "Arex",
        "api": "arexapi.classx.co.in"
    },
    {
        "name": "Armystudy",
        "api": "armystudyliveclassesapi.classx.co.in"
    },
    {
        "name": "Arnavsir",
        "api": "arnavsirapi.classx.co.in"
    },
    {
        "name": "Arresearchpoint",
        "api": "arresearchpointapi.classx.co.in"
    },
    {
        "name": "Arshacademy",
        "api": "arshacademyapi.classx.co.in"
    },
    {
        "name": "Artshala",
        "api": "artshalaapi.classx.co.in"
    },
    {
        "name": "Arunstudies",
        "api": "arunstudiesapi.classx.co.in"
    },
    {
        "name": "Aryaninstitute",
        "api": "aryaninstituteapi.classx.co.in"
    },
    {
        "name": "Aryen",
        "api": "aryenapi.classx.co.in"
    },
    {
        "name": "Asaeducation",
        "api": "asaeducationapi.classx.co.in"
    },
    {
        "name": "Asastuti",
        "api": "asastutiapi.classx.co.in"
    },
    {
        "name": "Aseclive",
        "api": "asecliveapi.classx.co.in"
    },
    {
        "name": "Ashaacademy",
        "api": "ashaacademyapi.classx.co.in"
    },
    {
        "name": "Ashavahi",
        "api": "ashavahiapi.classx.co.in"
    },
    {
        "name": "Ashishsingh",
        "api": "ashishsinghlecturesapi.teachx.in"
    },
    {
        "name": "Ashishsinghlecturespro",
        "api": "ashishsinghlecturesapi.classx.co.in"
    },
    {
        "name": "Ashishsirphysics",
        "api": "ashishsirphysicsapi.classx.co.in"
    },
    {
        "name": "Ashokacivilservices",
        "api": "ashokacivilservicesapi.classx.co.in"
    },
    {
        "name": "Ashokagyanguru",
        "api": "ashokagyanguruapi.classx.co.in"
    },
    {
        "name": "Ashokaonlineclasses",
        "api": "ashokaonlineclassesapi.classx.co.in"
    },
    {
        "name": "Ashokatheexamguru",
        "api": "ashokaexamguruapi.classx.co.in"
    },
    {
        "name": "Ashoktechhub",
        "api": "ashoktechhubapi.classx.co.in"
    },
    {
        "name": "Ashwinclasses",
        "api": "ashwinclasseslucknowapi.classx.co.in"
    },
    {
        "name": "Ashwinpandey",
        "api": "ashwinpandeyapi.classx.co.in"
    },
    {
        "name": "Asiannursingacademy",
        "api": "asiannursingacademyapi.classx.co.in"
    },
    {
        "name": "Aspectvision",
        "api": "aspectvisionapi.classx.co.in"
    },
    {
        "name": "Aspirantjunction",
        "api": "aspirantjunctionapi.classx.co.in"
    },
    {
        "name": "Aspirantslive",
        "api": "aspirantsliveapi.classx.co.in"
    },
    {
        "name": "Aspirationstudycentre",
        "api": "aspirationstudycentreapi.classx.co.in"
    },
    {
        "name": "Aspiredefence",
        "api": "aspiredefenceapi.classx.co.in"
    },
    {
        "name": "Aspiringteachers20",
        "api": "aspiringteachersapi.classx.co.in"
    },
    {
        "name": "Asrocareers",
        "api": "asrocareersapi.classx.co.in"
    },
    {
        "name": "Assamedu",
        "api": "assameduapi.classx.co.in"
    },
    {
        "name": "Astechnic",
        "api": "astechnicapi.classx.co.in"
    },
    {
        "name": "Asthaias",
        "api": "asthaiasacademyapi.classx.co.in"
    },
    {
        "name": "Astitvaacademy",
        "api": "astitvaacademyapi.classx.co.in"
    },
    {
        "name": "Astroaauraworld",
        "api": "astroaauraworldapi.classx.co.in"
    },
    {
        "name": "Atfirsttechnologies",
        "api": "atfirsttechnologiesapi.classx.co.in"
    },
    {
        "name": "Atharvaaggarwalofficial",
        "api": "atharvaagarwalapi.classx.co.in"
    },
    {
        "name": "Atstudycentre",
        "api": "atstudycentreapi.classx.co.in"
    },
    {
        "name": "Atulyalokmanch",
        "api": "atulyalokmanchapi.classx.co.in"
    },
    {
        "name": "Augustulearning",
        "api": "augustulearningapi.classx.co.in"
    },
    {
        "name": "Aveducationalacademy",
        "api": "aveducationalacademyapi.classx.co.in"
    },
    {
        "name": "Avinashparandeshirurpattern",
        "api": "avinashparandeshirurpatternapi.classx.co.in"
    },
    {
        "name": "Avinashsharma",
        "api": "avinashsharmaapi.classx.co.in"
    },
    {
        "name": "Avishkaracademy",
        "api": "avishkaracademyapi.classx.co.in"
    },
    {
        "name": "Avp",
        "api": "avpapi.classx.co.in"
    },
    {
        "name": "Avp247",
        "api": "avp247api.classx.co.in"
    },
    {
        "name": "Awstrainingcenter",
        "api": "awstrainingcenterapi.classx.co.in"
    },
    {
        "name": "Ayurprashna",
        "api": "ayurprashnaapi.classx.co.in"
    },
    {
        "name": "Ayurvedabeingvaidya",
        "api": "ayurvedabeingvaidyaapi.classx.co.in"
    },
    {
        "name": "Ayurvedalibrary",
        "api": "ayurvedalibraryapi.classx.co.in"
    },
    {
        "name": "Ayurvedapocketapp",
        "api": "ayurvedapocketappapi.classx.co.in"
    },
    {
        "name": "Ayurvedaprakrutivikruti",
        "api": "ayurvedaprakrutivikrutiapi.classx.co.in"
    },
    {
        "name": "Azadiasacademy",
        "api": "azadiasacademyapi.classx.co.in"
    },
    {
        "name": "Azucation",
        "api": "azucationapi.classx.co.in"
    },
    {
        "name": "Babhopalacademy",
        "api": "babhopalacademyapi.classx.co.in"
    },
    {
        "name": "Backtoeducation",
        "api": "backeducationapi.classx.co.in"
    },
    {
        "name": "Badamsinghclasses",
        "api": "badamsinghclassesapi.classx.co.in"
    },
    {
        "name": "Badesirclasses",
        "api": "badesirclassesapi.classx.co.in"
    },
    {
        "name": "Balasahebbhilareacademy",
        "api": "balasahebbhilareacademyapi.classx.co.in"
    },
    {
        "name": "Baluiq",
        "api": "baluiqapi.classx.co.in"
    },
    {
        "name": "Bandhanpathshala",
        "api": "bandhanpathshalaapi.classx.co.in"
    },
    {
        "name": "Bankerspoint",
        "api": "bankerspointapi.classx.co.in"
    },
    {
        "name": "Bankerspointmaharashtra",
        "api": "bankerspointmaharastraapi.classx.co.in"
    },
    {
        "name": "Bankerszoneapp",
        "api": "bankerszoneappapi.classx.co.in"
    },
    {
        "name": "Bansallive",
        "api": "bansalliveapi.classx.co.in"
    },
    {
        "name": "Basarainstitute",
        "api": "basarainstituteapi.classx.co.in"
    },
    {
        "name": "Basicsiksha",
        "api": "basicsikshaapi.classx.co.in"
    },
    {
        "name": "Bbaacademy",
        "api": "bbaacademyapi.classx.co.in"
    },
    {
        "name": "Bbcstudy",
        "api": "bbcstudyapi.classx.co.in"
    },
    {
        "name": "Bbn",
        "api": "bbnapi.classx.co.in"
    },
    {
        "name": "Be10X",
        "api": "be10xapi.classx.co.in"
    },
    {
        "name": "Beastlearners",
        "api": "beastlearnersapi.classx.co.in"
    },
    {
        "name": "Beatexams",
        "api": "beatexamsapi.classx.co.in"
    },
    {
        "name": "Bebankersanreetiacademy",
        "api": "bebankerapi.classx.co.in"
    },
    {
        "name": "Beeclassesbyghogaresir",
        "api": "beeclassesbyghogaresirapi.classx.co.in"
    },
    {
        "name": "Beepublication",
        "api": "beepublicationapi.classx.co.in"
    },
    {
        "name": "Beetaacademy",
        "api": "beetaacademyapi.classx.co.in"
    },
    {
        "name": "Beforebiology",
        "api": "beforebiologyapi.classx.co.in"
    },
    {
        "name": "Beingaspirant",
        "api": "beingaspirantapi.classx.co.in"
    },
    {
        "name": "Beingdoctor",
        "api": "beingdoctorapi.classx.co.in"
    },
    {
        "name": "Beparwahiacademy",
        "api": "beparwahiacademyapi.classx.co.in"
    },
    {
        "name": "Bepecexperiencetherealtime",
        "api": "bepecexperiencerealtimeapi.classx.co.in"
    },
    {
        "name": "Bestacad",
        "api": "bestacadapi.classx.co.in"
    },
    {
        "name": "Betterenroll",
        "api": "betterenrollapi.classx.co.in"
    },
    {
        "name": "Bhagirathiasacademy",
        "api": "bhagirathiasacademyapi.classx.co.in"
    },
    {
        "name": "Bhambhusirhindi",
        "api": "bhambhusirhindiapi.classx.co.in"
    },
    {
        "name": "Bharariacademy",
        "api": "bharariacademyapi.classx.co.in"
    },
    {
        "name": "Bharatiasacademy",
        "api": "bharatiasacademyapi.classx.co.in"
    },
    {
        "name": "Bharatjobs",
        "api": "bharatjobsapi.classx.co.in"
    },
    {
        "name": "Bharatsikshaacademy",
        "api": "bharatsikshaacademyapi.classx.co.in"
    },
    {
        "name": "Bharti",
        "api": "bhartilearningapi.appx.co.in"
    },
    {
        "name": "Bhashmiacademy",
        "api": "bhashmiacademyapi.classx.co.in"
    },
    {
        "name": "Bhavishyaacademy",
        "api": "bhavishyaacademyapi.classx.co.in"
    },
    {
        "name": "Bhavishyabhartiranchi",
        "api": "bhavishyabhartiranchiapi.classx.co.in"
    },
    {
        "name": "Bhavyainstitution",
        "api": "bhavyainstitutionapi.classx.co.in"
    },
    {
        "name": "Bhawanisinghchundawathindi",
        "api": "bhawanisinghchundawathindiapi.classx.co.in"
    },
    {
        "name": "Bhualumnismartsolution",
        "api": "bhualumnismartsolutionapi.classx.co.in"
    },
    {
        "name": "Bhupendrasinghdinkar",
        "api": "bhupendrasinghdinkarapi.classx.co.in"
    },
    {
        "name": "Bhushanmpscacademy",
        "api": "bhushanmpscacademyapi.classx.co.in"
    },
    {
        "name": "Bicebiswasinstitute",
        "api": "bicebiswasinstituteapi.classx.co.in"
    },
    {
        "name": "Big20",
        "api": "big20appapi.classx.co.in"
    },
    {
        "name": "Bigbangbogan",
        "api": "bigbangboganapi.classx.co.in"
    },
    {
        "name": "Biharboardeducation",
        "api": "biharboardeducationapi.classx.co.in"
    },
    {
        "name": "Biharsmartclasses",
        "api": "biharsmartclassesapi.classx.co.in"
    },
    {
        "name": "Biologyinhindi",
        "api": "biologyinhindiapi.classx.co.in"
    },
    {
        "name": "Biplawstudycentrebsc",
        "api": "biplawstudycentreapi.classx.co.in"
    },
    {
        "name": "Birensirodia",
        "api": "birensirodiaapi.classx.co.in"
    },
    {
        "name": "Biswaniclasses",
        "api": "biswaniclassesapi.classx.co.in"
    },
    {
        "name": "Bitsyuva",
        "api": "bitsyuvaapi.classx.co.in"
    },
    {
        "name": "Bookmyvideo",
        "api": "bookmyvideoapi.classx.co.in"
    },
    {
        "name": "Bookrox",
        "api": "bookroxapi.classx.co.in"
    },
    {
        "name": "Bookup",
        "api": "bookupapi.classx.co.in"
    },
    {
        "name": "Bookwormacademy",
        "api": "bookwormacademyapi.classx.co.in"
    },
    {
        "name": "Boosteracademy",
        "api": "boosteracademyapi.classx.co.in"
    },
    {
        "name": "Bpnmath",
        "api": "bpnmathapi.classx.co.in"
    },
    {
        "name": "Bpscacademy",
        "api": "bpscacademyapi.classx.co.in"
    },
    {
        "name": "Bpscadda247",
        "api": "bpscadda247api.classx.co.in"
    },
    {
        "name": "Bpscscore",
        "api": "bpscscoreapi.classx.co.in"
    },
    {
        "name": "Bpsczone",
        "api": "bpsczoneapi.classx.co.in"
    },
    {
        "name": "Brahmasmi",
        "api": "brahmasmiapi.classx.co.in"
    },
    {
        "name": "Brahmieducation",
        "api": "brahmieducationapi.classx.co.in"
    },
    {
        "name": "Brainbulb",
        "api": "brainbulbapi.classx.co.in"
    },
    {
        "name": "Brainerygroupvod",
        "api": "brainerygroupvodapi.classx.co.in"
    },
    {
        "name": "Brainq",
        "api": "brainqapi.classx.co.in"
    },
    {
        "name": "Brclasses",
        "api": "brclassesapi.classx.co.in"
    },
    {
        "name": "Brightacademy",
        "api": "brightacademyapi.classx.co.in"
    },
    {
        "name": "Brightpublication",
        "api": "brightpublicationapi.classx.co.in"
    },
    {
        "name": "Brilliantcommerceclassespune",
        "api": "brilliantcommerceclassespuneapi.classx.co.in"
    },
    {
        "name": "Brilliantguru",
        "api": "brilliantguruapi.classx.co.in"
    },
    {
        "name": "Brillianttestseries",
        "api": "brillianttestseriesapi.classx.co.in"
    },
    {
        "name": "Brotherhooddefence",
        "api": "brotherhooddefenceapi.classx.co.in"
    },
    {
        "name": "Bsclearningapp",
        "api": "bsclearningappapi.classx.co.in"
    },
    {
        "name": "Bscproclasses",
        "api": "bscproclassesapi.classx.co.in"
    },
    {
        "name": "Bscwithrambabusir",
        "api": "bscrambabusirapi.classx.co.in"
    },
    {
        "name": "Bsgurukul",
        "api": "bsgurukulapi.classx.co.in"
    },
    {
        "name": "Bsppharmacyofficial",
        "api": "bsppharmacyapi.classx.co.in"
    },
    {
        "name": "Bualbuleslive",
        "api": "bualbulesliveapi.classx.co.in"
    },
    {
        "name": "Bumbexfull",
        "api": "bumbexfullapi.classx.co.in"
    },
    {
        "name": "Bypradipbodhale",
        "api": "paripurnmarathivyakaranapi.classx.co.in"
    },
    {
        "name": "Bystudy",
        "api": "bystudyapi.classx.co.in"
    },
    {
        "name": "Cadetsdefencacademy",
        "api": "cadetsdefenceacademyapi.classx.co.in"
    },
    {
        "name": "Cadetspointlearningapp",
        "api": "cadetspointlearningappapi.classx.co.in"
    },
    {
        "name": "Canonline",
        "api": "canonlineapi.classx.co.in"
    },
    {
        "name": "Canvasclasses",
        "api": "canvasclassesapi.classx.co.in"
    },
    {
        "name": "Capfacmentors",
        "api": "capfacmentorsapi.classx.co.in"
    },
    {
        "name": "Caramanluthraclasses",
        "api": "caramanluthraclassesapi.classx.co.in"
    },
    {
        "name": "Carbacademy",
        "api": "carbacademyapi.classx.co.in"
    },
    {
        "name": "Careerado",
        "api": "careeradoapi.classx.co.in"
    },
    {
        "name": "Careerbooster",
        "api": "careerboosterapi.classx.co.in"
    },
    {
        "name": "Careerclassesjaipur",
        "api": "careerclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Careerhub",
        "api": "careerhubapi.classx.co.in"
    },
    {
        "name": "Careermirror",
        "api": "careermirrorapi.classx.co.in"
    },
    {
        "name": "Careernow",
        "api": "careernowapi.classx.co.in"
    },
    {
        "name": "Careerstudy",
        "api": "careerstudyapi.classx.co.in"
    },
    {
        "name": "Careerupdatebyengineer",
        "api": "careerupdatebyengineerapi.classx.co.in"
    },
    {
        "name": "Careerupshillong",
        "api": "careerupshillongapi.classx.co.in"
    },
    {
        "name": "Careervijay",
        "api": "careervijayapi.classx.co.in"
    },
    {
        "name": "Careerwave",
        "api": "careerwaveapi.classx.co.in"
    },
    {
        "name": "Careerwin",
        "api": "careerwinapi.classx.co.in"
    },
    {
        "name": "Careerwitharun",
        "api": "careerarunapi.classx.co.in"
    },
    {
        "name": "Carrierkatta",
        "api": "carrierkattaapi.classx.co.in"
    },
    {
        "name": "Casepage",
        "api": "casepageapi.classx.co.in"
    },
    {
        "name": "Catalystsoni",
        "api": "catalystsoniapi.classx.co.in"
    },
    {
        "name": "Cayatra",
        "api": "cayatraapi.classx.co.in"
    },
    {
        "name": "Cccwifistudy",
        "api": "cccwifistudyapi.classx.co.in"
    },
    {
        "name": "Cdacareerdishariacademy",
        "api": "cdacareerdishariacademyapi.classx.co.in"
    },
    {
        "name": "Cdacpreparation",
        "api": "cdacpreparationapi.classx.co.in"
    },
    {
        "name": "Cdpmastilearningapp",
        "api": "cdpmastilearningappapi.classx.co.in"
    },
    {
        "name": "Ceadclasses",
        "api": "ceadclassesapi.classx.co.in"
    },
    {
        "name": "Centuriondefenceacademy",
        "api": "centuriondefenceacademyapi.classx.co.in"
    },
    {
        "name": "Centurionstudypoint",
        "api": "centurionstudypointapi.classx.co.in"
    },
    {
        "name": "Cetqualifiers",
        "api": "cetqualifiersapi.classx.co.in"
    },
    {
        "name": "Cgpscknowledgehubpscwala",
        "api": "cgpscknowledgehubapi.classx.co.in"
    },
    {
        "name": "Cgpscmapology",
        "api": "cgpscmapologyapi.classx.co.in"
    },
    {
        "name": "Cgpscwiseup",
        "api": "cgpscwiseupapi.classx.co.in"
    },
    {
        "name": "Chaloseekho",
        "api": "chaloseekhoapi.classx.co.in"
    },
    {
        "name": "Champcircle",
        "api": "champcircleapi.classx.co.in"
    },
    {
        "name": "Championsiitmedical",
        "api": "championsiitmedicalapi.classx.co.in"
    },
    {
        "name": "Champsacademy",
        "api": "champsacademyapi.classx.co.in"
    },
    {
        "name": "Champsclassesprepjeet",
        "api": "champsclassesapi.classx.co.in"
    },
    {
        "name": "Chanakyachamps",
        "api": "chanakyachampsapi.classx.co.in"
    },
    {
        "name": "Chanakyadefenceacademy",
        "api": "chanakyadefenceacademyapi.classx.co.in"
    },
    {
        "name": "Chanakyaphysicalacademy",
        "api": "chanakyaphysicalacademyapi.classx.co.in"
    },
    {
        "name": "Chandanclasses",
        "api": "chandanclassesapi.classx.co.in"
    },
    {
        "name": "Chandanlogic",
        "api": "newchandanlogicsapi.classx.co.in"
    },
    {
        "name": "Chandanmishrabusinesscoach",
        "api": "chandanmishrabusinesscoachapi.classx.co.in"
    },
    {
        "name": "Chankshyamandalforupscandmpsc",
        "api": "chankshyamandalupscmpscapi.classx.co.in"
    },
    {
        "name": "Charikrishnasirclasses",
        "api": "charikrishnasirclassesapi.classx.co.in"
    },
    {
        "name": "Charteredcommerce",
        "api": "charteredcommerceapi.classx.co.in"
    },
    {
        "name": "Chauhanlawacademy",
        "api": "chauhanlawacademyapi.classx.co.in"
    },
    {
        "name": "Chemacademy",
        "api": "chemacademyapi.classx.co.in"
    },
    {
        "name": "Chemistrybyanilsir",
        "api": "chemistryanilsirapi.classx.co.in"
    },
    {
        "name": "Chemistryforyou",
        "api": "chemistryforyouapi.classx.co.in"
    },
    {
        "name": "Chemistryguruji",
        "api": "chemistrygurujiapi.classx.co.in"
    },
    {
        "name": "Chemistrypro",
        "api": "chemistryproapi.classx.co.in"
    },
    {
        "name": "Chemistrywallahvvr",
        "api": "chemistrywallahvvrapi.classx.co.in"
    },
    {
        "name": "Chemphy",
        "api": "chemphyapi.classx.co.in"
    },
    {
        "name": "Chengdedohipode",
        "api": "chengdedohipodeapi.classx.co.in"
    },
    {
        "name": "Chhoteiasthelearningapp",
        "api": "chhoteiaslearningapi.classx.co.in"
    },
    {
        "name": "Chinmayacademy",
        "api": "chinmayacademyapi.classx.co.in"
    },
    {
        "name": "Chiralacademy",
        "api": "chiralacademyapi.classx.co.in"
    },
    {
        "name": "Choutiseconomy",
        "api": "choutiseconomyapi.classx.co.in"
    },
    {
        "name": "Chrisedutech",
        "api": "chrisedutechapi.classx.co.in"
    },
    {
        "name": "Christopher",
        "api": "christopherapi.classx.co.in"
    },
    {
        "name": "Chunchunstudyacademy",
        "api": "chunchunstudyacademyapi.classx.co.in"
    },
    {
        "name": "Cityeducation",
        "api": "cityeducationapi.classx.co.in"
    },
    {
        "name": "Civilanalystcareer",
        "api": "civilanalystcareerapi.classx.co.in"
    },
    {
        "name": "Civilservices",
        "api": "studycivilservicesapi.classx.co.in"
    },
    {
        "name": "Civilsguruias",
        "api": "civilsguruiasapi.classx.co.in"
    },
    {
        "name": "Civiltaiyari",
        "api": "civiltaiyariapi.classx.co.in"
    },
    {
        "name": "Civiltechsolution",
        "api": "civiltechsolutionapi.classx.co.in"
    },
    {
        "name": "Cjclasses",
        "api": "cjclassesapi.classx.co.in"
    },
    {
        "name": "Clarifyknowledge",
        "api": "clarifyknowledgeapi.classx.co.in"
    },
    {
        "name": "Class24Byparwezsir",
        "api": "class24parwezsirapi.classx.co.in"
    },
    {
        "name": "Classhour",
        "api": "classhourapi.classx.co.in"
    },
    {
        "name": "Classtest",
        "api": "classtestappxapi.classx.co.in"
    },
    {
        "name": "Clatiansaguideforlawaspirants",
        "api": "clatiansapi.classx.co.in"
    },
    {
        "name": "Clearvisionclasses",
        "api": "clearvisionclassesapi.classx.co.in"
    },
    {
        "name": "Cloudtech",
        "api": "cloudtechapi.classx.co.in"
    },
    {
        "name": "Cmccareer",
        "api": "cmccareerapi.classx.co.in"
    },
    {
        "name": "Cmcindore",
        "api": "cmcindoreapi.classx.co.in"
    },
    {
        "name": "Cmpforupscmpsc",
        "api": "chanakyamandalpariwarapi.classx.co.in"
    },
    {
        "name": "Cnachievers",
        "api": "cnachieversapi.classx.co.in"
    },
    {
        "name": "Cnreddyacademy",
        "api": "cnreddyacademyapi.classx.co.in"
    },
    {
        "name": "Coachify",
        "api": "coachifyapi.classx.co.in"
    },
    {
        "name": "Coachingwithradhesir",
        "api": "coachingradhesirapi.classx.co.in"
    },
    {
        "name": "Coceducation",
        "api": "coceducationapi.classx.co.in"
    },
    {
        "name": "Codegenie",
        "api": "codegenieapi.classx.co.in"
    },
    {
        "name": "Codewithanurag",
        "api": "codewithanuragapi.classx.co.in"
    },
    {
        "name": "Codewithashhad",
        "api": "codeashhadapi.classx.co.in"
    },
    {
        "name": "Codingcontentcreator",
        "api": "codingcontentcreatorapi.classx.co.in"
    },
    {
        "name": "Codingseekho",
        "api": "codingseekhoapi.classx.co.in"
    },
    {
        "name": "Codingwallahsir",
        "api": "codingwallahsirapi.classx.co.in"
    },
    {
        "name": "Combinecrux",
        "api": "combinecruxapi.classx.co.in"
    },
    {
        "name": "Commerceassetsinstitute",
        "api": "commerceassetsinstituteapi.classx.co.in"
    },
    {
        "name": "Commerceinsightselearning",
        "api": "commerceinsightselearningapi.classx.co.in"
    },
    {
        "name": "Commercenation",
        "api": "commercenationapi.classx.co.in"
    },
    {
        "name": "Commercenationpro",
        "api": "commercenationproapi.classx.co.in"
    },
    {
        "name": "Commercewaleguruji",
        "api": "commercewalegurujiapi.classx.co.in"
    },
    {
        "name": "Commercewithvinay",
        "api": "commercevinayapi.classx.co.in"
    },
    {
        "name": "Competishun",
        "api": "competishunapi.classx.co.in"
    },
    {
        "name": "Competitionacademydigitalclasses",
        "api": "competitionacademydigitalclassesapi.classx.co.in"
    },
    {
        "name": "Competitionguru",
        "api": "competitionguruapi.classx.co.in"
    },
    {
        "name": "Competitionmaterialharyana",
        "api": "competitionmaterialharayanaapi.classx.co.in"
    },
    {
        "name": "Competitionmathpoint",
        "api": "competitionmathpointapi.classx.co.in"
    },
    {
        "name": "Competitionprobymkmishra",
        "api": "competitionpromkmishraapi.classx.co.in"
    },
    {
        "name": "Competitivepharma",
        "api": "competitivepharmaapi.classx.co.in"
    },
    {
        "name": "Computech",
        "api": "computechapi.classx.co.in"
    },
    {
        "name": "Comrcio",
        "api": "comercioapi.classx.co.in"
    },
    {
        "name": "Conceptclaritywala",
        "api": "conceptclaritywalaapi.classx.co.in"
    },
    {
        "name": "Conceptclasses",
        "api": "conceptclassesapi.classx.co.in"
    },
    {
        "name": "Conceptseekho",
        "api": "conceptseekhoapi.classx.co.in"
    },
    {
        "name": "Conceptup",
        "api": "conceptupapi.classx.co.in"
    },
    {
        "name": "Constantguide",
        "api": "constantguideapi.classx.co.in"
    },
    {
        "name": "Cosmosclasses",
        "api": "cosmosclassesapi.classx.co.in"
    },
    {
        "name": "Cosmossikaraninstituteofgeography",
        "api": "cosmossikarapi.classx.co.in"
    },
    {
        "name": "Coursee",
        "api": "courseeapi.classx.co.in"
    },
    {
        "name": "Cpyadavclasses",
        "api": "cpyadavclassesapi.classx.co.in"
    },
    {
        "name": "Crackcuetexam",
        "api": "crackcuetexamapi.classx.co.in"
    },
    {
        "name": "Crackerexamhub",
        "api": "crackerexamhubapi.classx.co.in"
    },
    {
        "name": "Crackexampurvi",
        "api": "crackexampurviapi.classx.co.in"
    },
    {
        "name": "Crackparikshachandanlogicsold",
        "api": "chandanlogicsapi.classx.co.in"
    },
    {
        "name": "Crackvision",
        "api": "crackvisionapi.classx.co.in"
    },
    {
        "name": "Createu",
        "api": "createuapi.classx.co.in"
    },
    {
        "name": "Creativechemistry",
        "api": "creativechemistryapi.classx.co.in"
    },
    {
        "name": "Creativecomputer",
        "api": "creativecomputerapi.classx.co.in"
    },
    {
        "name": "Crisscrossclasses",
        "api": "crisscrossclassesapi.classx.co.in"
    },
    {
        "name": "Cropcosagriedutech",
        "api": "cropcosagriapi.classx.co.in"
    },
    {
        "name": "Csacivilservicesacademy",
        "api": "civilservicesacademyapi.classx.co.in"
    },
    {
        "name": "Csatbykabirsir",
        "api": "csatkabirsirapi.classx.co.in"
    },
    {
        "name": "Csclassroom",
        "api": "csclassroomapi.classx.co.in"
    },
    {
        "name": "Csmaths",
        "api": "csmathsapi.classx.co.in"
    },
    {
        "name": "Cstutorugcnetgyan",
        "api": "cstutorapi.classx.co.in"
    },
    {
        "name": "Ctcclasses",
        "api": "ctcclassesapi.classx.co.in"
    },
    {
        "name": "Cuetechratneshpandey",
        "api": "cuetechapi.classx.co.in"
    },
    {
        "name": "Cuetprep",
        "api": "cuetprepapi.classx.co.in"
    },
    {
        "name": "Currentaffairsbyshrikanttayade",
        "api": "currentaffairsbyshrikanttayadeapi.classx.co.in"
    },
    {
        "name": "D2Techlab",
        "api": "d2techlabapi.classx.co.in"
    },
    {
        "name": "Dabrasirscience",
        "api": "dabrasirscienceapi.classx.co.in"
    },
    {
        "name": "Dagdushethupscacademy",
        "api": "dagdushethupscacademyapi.classx.co.in"
    },
    {
        "name": "Dagur",
        "api": "daguracademyapi.teachx.in"
    },
    {
        "name": "Dagursacademy",
        "api": "daguracademyapi.classx.co.in"
    },
    {
        "name": "Dailypractice",
        "api": "dailypracticeapi.classx.co.in"
    },
    {
        "name": "Darshanikias",
        "api": "darshanikiasapi.classx.co.in"
    },
    {
        "name": "Dazzlingcareer",
        "api": "dazzlingcareerapi.classx.co.in"
    },
    {
        "name": "Dbmcimdslive",
        "api": "dbmcimdsliveapi.classx.co.in"
    },
    {
        "name": "Dbstudyhub",
        "api": "dbstudyhubapi.classx.co.in"
    },
    {
        "name": "Dccinstitute",
        "api": "dccinstituteapi.classx.co.in"
    },
    {
        "name": "Dcclasses",
        "api": "dcclassesapi.classx.co.in"
    },
    {
        "name": "Dcjantabysarvantsir",
        "api": "dcjantasarvantsirapi.classx.co.in"
    },
    {
        "name": "Deargurujiofficial",
        "api": "gurujiofficialapi.classx.co.in"
    },
    {
        "name": "Dearlearners",
        "api": "dearlearnersapi.classx.co.in"
    },
    {
        "name": "Dearsirbarisir",
        "api": "dearsirbarisirapi.classx.co.in"
    },
    {
        "name": "Deccanias",
        "api": "deccaniasapi.classx.co.in"
    },
    {
        "name": "Decodingsports",
        "api": "decodingsportsapi.classx.co.in"
    },
    {
        "name": "Deebha",
        "api": "deebhaapi.classx.co.in"
    },
    {
        "name": "Deepakclasses",
        "api": "deepakclassesapi.classx.co.in"
    },
    {
        "name": "Deepakeducationhub",
        "api": "deepakeducationhubapi.classx.co.in"
    },
    {
        "name": "Deepeducation",
        "api": "deepeducationapi.classx.co.in"
    },
    {
        "name": "Deepikaclasses",
        "api": "deepikaclassesapi.classx.co.in"
    },
    {
        "name": "Deeptisinghacademy",
        "api": "deeptisinghacademyapi.classx.co.in"
    },
    {
        "name": "Defencedarling",
        "api": "defencedarlingapi.classx.co.in"
    },
    {
        "name": "Defencefighter",
        "api": "defencefighterapi.classx.co.in"
    },
    {
        "name": "Defencemania",
        "api": "defencemania2api.classx.co.in"
    },
    {
        "name": "Defencesadhanacdscapfacndaafcat",
        "api": "defencesadhanaapi.classx.co.in"
    },
    {
        "name": "Defencezonekanpur",
        "api": "defencezoneapi.classx.co.in"
    },
    {
        "name": "Degreemathstutorialdmtlogics",
        "api": "degreemathstutorialapi.classx.co.in"
    },
    {
        "name": "Dehradunclasses",
        "api": "dehradunclassesapi.classx.co.in"
    },
    {
        "name": "Delhipoliceconstable2023",
        "api": "delhipoliceconstableapi.classx.co.in"
    },
    {
        "name": "Delhisecrets",
        "api": "delhisecretsapi.classx.co.in"
    },
    {
        "name": "Deserveias",
        "api": "deserveiasapi.classx.co.in"
    },
    {
        "name": "Desiretolearn",
        "api": "desiretolearnapi.classx.co.in"
    },
    {
        "name": "Destinationias",
        "api": "destinationiasapi.classx.co.in"
    },
    {
        "name": "Devgktricks",
        "api": "devgktricksapi.classx.co.in"
    },
    {
        "name": "Dfglory",
        "api": "dfgloryapi.classx.co.in"
    },
    {
        "name": "Dgscaps",
        "api": "dgscapsapi.classx.co.in"
    },
    {
        "name": "Dhaapps",
        "api": "dhaappsapi.classx.co.in"
    },
    {
        "name": "Dhakadcoachingrameshwarsir",
        "api": "dhakadcoachingrameshwarsirapi.classx.co.in"
    },
    {
        "name": "Dhakadconcept",
        "api": "dhakadconceptapi.classx.co.in"
    },
    {
        "name": "Dhananjayias",
        "api": "dhananjayiasacademyapi.classx.co.in"
    },
    {
        "name": "Dhanbadmathsacademy",
        "api": "dhanbadmathsacademyapi.classx.co.in"
    },
    {
        "name": "Dhangarchemistrylecturepro",
        "api": "dhangarchemistrylectureproapi.classx.co.in"
    },
    {
        "name": "Dhankharclasses",
        "api": "dhankharclassesapi.classx.co.in"
    },
    {
        "name": "Dharmendrasociology",
        "api": "dharmendrasociologyapi.classx.co.in"
    },
    {
        "name": "Dharoharclasses",
        "api": "dharoharclassesapi.classx.co.in"
    },
    {
        "name": "Dharteeeducation",
        "api": "dharteeeducationapi.classx.co.in"
    },
    {
        "name": "Dhasusir",
        "api": "dhasusiracademyapi.teachx.in"
    },
    {
        "name": "Dhasusiracademy",
        "api": "dhasusiracademyapi.classx.co.in"
    },
    {
        "name": "Dhaygudeacademy",
        "api": "dhaygudeacademysataraapi.classx.co.in"
    },
    {
        "name": "Dheyapurtifoundation",
        "api": "dheyapurtifoundationapi.classx.co.in"
    },
    {
        "name": "Dhoraclasses",
        "api": "dhoraclassesapi.classx.co.in"
    },
    {
        "name": "Dhyeyinstitute",
        "api": "dhyeyinstituteapi.classx.co.in"
    },
    {
        "name": "Dhyeyliveapplication",
        "api": "dhyeyliveapplicationapi.classx.co.in"
    },
    {
        "name": "Diacmpscfullcourses",
        "api": "diacmpscfullcoursesapi.classx.co.in"
    },
    {
        "name": "Dictionenglishclasses",
        "api": "dictionenglishclassesapi.classx.co.in"
    },
    {
        "name": "Digicateias",
        "api": "digicateiasapi.classx.co.in"
    },
    {
        "name": "Digilearn",
        "api": "digilearnapi.classx.co.in"
    },
    {
        "name": "Diginest",
        "api": "diginestapi.classx.co.in"
    },
    {
        "name": "Digitech",
        "api": "digitechapi.classx.co.in"
    },
    {
        "name": "Digvijaysirgs",
        "api": "digvijaysirgsapi.classx.co.in"
    },
    {
        "name": "Dikshantias",
        "api": "dikshantiasapi.classx.co.in"
    },
    {
        "name": "Diligentsscian",
        "api": "diligentsscianapi.classx.co.in"
    },
    {
        "name": "Dilipkhatekar",
        "api": "dilipkhatekarapi.classx.co.in"
    },
    {
        "name": "Dimplekaushikenglishclasses",
        "api": "dimplekaushikenglishclassesapi.classx.co.in"
    },
    {
        "name": "Dineshacademy20",
        "api": "dineshacademyapi.classx.co.in"
    },
    {
        "name": "Directionacademy",
        "api": "directionacademyapi.classx.co.in"
    },
    {
        "name": "Directionrojgaracademy",
        "api": "directionrojgaracademyapi.classx.co.in"
    },
    {
        "name": "Discoveryiasacademy",
        "api": "discoveryiasacademyapi.classx.co.in"
    },
    {
        "name": "Dishaacademy",
        "api": "dishaacademyapi.classx.co.in"
    },
    {
        "name": "Dishaonlineclasses",
        "api": "dishaonlineclassesapi.classx.co.in"
    },
    {
        "name": "Divijatutorials",
        "api": "divijatutorialsapi.classx.co.in"
    },
    {
        "name": "Divinestudy",
        "api": "divinestudyapi.classx.co.in"
    },
    {
        "name": "Divyadrishticlasses",
        "api": "divyadrishticlassesapi.classx.co.in"
    },
    {
        "name": "Dixitsir",
        "api": "dixitsirapi.classx.co.in"
    },
    {
        "name": "Djmcforyou",
        "api": "djmcforyouapi.classx.co.in"
    },
    {
        "name": "Dkshiksha",
        "api": "dkshikshaapi.classx.co.in"
    },
    {
        "name": "Dnanursing",
        "api": "dnanursingapi.classx.co.in"
    },
    {
        "name": "Dnyanadeepacademypune",
        "api": "dnyanadeepacademypuneapi.classx.co.in"
    },
    {
        "name": "Dnyanaiacademy",
        "api": "dnyanaiacademyapi.classx.co.in"
    },
    {
        "name": "Dnyanankuracademypune",
        "api": "dnyanankuracademypuneapi.classx.co.in"
    },
    {
        "name": "Dnyanarnavonlineacademy",
        "api": "dnyanarnavonlineacademyapi.classx.co.in"
    },
    {
        "name": "Dnyandeepallin1",
        "api": "dnyandeepallapi.classx.co.in"
    },
    {
        "name": "Dnyandeepwallah",
        "api": "dnyandeepwallahapi.classx.co.in"
    },
    {
        "name": "Dnyaneshwarpatilsgurukulprabodhinipune",
        "api": "dnyaneshwarpatilgurukulprabodhiniapi.classx.co.in"
    },
    {
        "name": "Dnyanpeethacademyamravati",
        "api": "dnyanpeethacademyamravatiapi.classx.co.in"
    },
    {
        "name": "Dnyanrajacademy",
        "api": "dnyanrajacademyapi.classx.co.in"
    },
    {
        "name": "Dnyanvisharadbykamlakarsir",
        "api": "dnyanvisharadkamlakarsirapi.classx.co.in"
    },
    {
        "name": "Dnyndeepacademyambajogai",
        "api": "dnyndeepacademyambajogaiapi.classx.co.in"
    },
    {
        "name": "Dobhaifreepadhai",
        "api": "dobhaifreepadhaiapi.classx.co.in"
    },
    {
        "name": "Dobook",
        "api": "dobookapi.classx.co.in"
    },
    {
        "name": "Doeduadphycinstitute",
        "api": "doeduadphycinstituteapi.classx.co.in"
    },
    {
        "name": "Doonlawmentor",
        "api": "doonlawmentorapi.classx.co.in"
    },
    {
        "name": "Drajayyawaleacademy",
        "api": "drajayyawaleacademyapi.classx.co.in"
    },
    {
        "name": "Dramarjagtap",
        "api": "dramarjagtapapi.classx.co.in"
    },
    {
        "name": "Dramitsias",
        "api": "dramitsiasapi.classx.co.in"
    },
    {
        "name": "Dranandmani",
        "api": "dranandmaniapi.classx.co.in"
    },
    {
        "name": "Drdkkaushiksenglish",
        "api": "drdkkaushikenglishapi.classx.co.in"
    },
    {
        "name": "Dreamexam",
        "api": "dreamexamapi.classx.co.in"
    },
    {
        "name": "Dreamkhaki",
        "api": "dreamkhakiapi.classx.co.in"
    },
    {
        "name": "Dreamsewakiasthelearningapp",
        "api": "dreamsewakiasapi.classx.co.in"
    },
    {
        "name": "Dreamteam",
        "api": "dreamteamapi.classx.co.in"
    },
    {
        "name": "Dreducationofficial",
        "api": "dreducationofficialapi.classx.co.in"
    },
    {
        "name": "Drgoswamiacademy",
        "api": "goswamiacademyapi.classx.co.in"
    },
    {
        "name": "Drgreenagroclassesudaipur",
        "api": "drgreenagroclassesudaipurapi.classx.co.in"
    },
    {
        "name": "Drishta",
        "api": "drishtaapi.classx.co.in"
    },
    {
        "name": "Drishtipedia",
        "api": "drishtipediaapi.classx.co.in"
    },
    {
        "name": "Dronacharyaacademybyudaysir",
        "api": "dronacharyaacademyudaysirapi.classx.co.in"
    },
    {
        "name": "Drsachin",
        "api": "drsachinbhaskesshardaacademyapi.classx.co.in"
    },
    {
        "name": "Drsachinkapur",
        "api": "drsachinkapurapi.classx.co.in"
    },
    {
        "name": "Drsahilclasses",
        "api": "drsahilclassesapi.classx.co.in"
    },
    {
        "name": "Drsanjayatrieducation",
        "api": "drsanjayatrieducationapi.classx.co.in"
    },
    {
        "name": "Drsgoswamiclasses",
        "api": "drsgoswamiclassesapi.classx.co.in"
    },
    {
        "name": "Dryokesharul",
        "api": "dryokesharulapi.classx.co.in"
    },
    {
        "name": "Dslclassesjind",
        "api": "dslclassesjindapi.classx.co.in"
    },
    {
        "name": "Dteach",
        "api": "dteachapi.classx.co.in"
    },
    {
        "name": "Dts",
        "api": "dtsapi.classx.co.in"
    },
    {
        "name": "Dufferadda",
        "api": "dufferaddaapi.classx.co.in"
    },
    {
        "name": "Dvstechgovtjobskillprep",
        "api": "dvstechgovtjobskillprepapi.classx.co.in"
    },
    {
        "name": "Dyasvardicha",
        "api": "dyasvardichaapi.classx.co.in"
    },
    {
        "name": "Dynamiccoachingcentre",
        "api": "dynamiccoachingcentreapi.classx.co.in"
    },
    {
        "name": "Dzklive",
        "api": "dzkliveapi.classx.co.in"
    },
    {
        "name": "E1Coaching",
        "api": "e1coachingcenterapi.classx.co.in"
    },
    {
        "name": "E2Academy",
        "api": "e2academyapi.classx.co.in"
    },
    {
        "name": "E3Lacademy",
        "api": "e3lacademyapi.classx.co.in"
    },
    {
        "name": "Eabhyasu",
        "api": "eabhyasuapi.classx.co.in"
    },
    {
        "name": "Easy2Learning20",
        "api": "easy2learning2api.classx.co.in"
    },
    {
        "name": "Easyagriculture",
        "api": "easyagricultureapi.classx.co.in"
    },
    {
        "name": "Easyenglish",
        "api": "easyenglishapi.classx.co.in"
    },
    {
        "name": "Easyreasoningclassesbyrahulsir",
        "api": "easyreasoningclassesrahulsirapi.classx.co.in"
    },
    {
        "name": "Ebsexcellentbookstore",
        "api": "excellentbookstoreapi.classx.co.in"
    },
    {
        "name": "Ecacademy",
        "api": "ecacademyapi.classx.co.in"
    },
    {
        "name": "Ecomath",
        "api": "ecomathapi.classx.co.in"
    },
    {
        "name": "Economicsbyshrikantkalaskar",
        "api": "economicsshrikantkalaskarapi.classx.co.in"
    },
    {
        "name": "Economicspreparation",
        "api": "economicspreparationapi.classx.co.in"
    },
    {
        "name": "Economybydhananjaymate",
        "api": "dhananjaymatesswarajyaacademyapi.classx.co.in"
    },
    {
        "name": "Ecopathshala",
        "api": "ecopathshalaapi.classx.co.in"
    },
    {
        "name": "Ecotutorialsbymandeep",
        "api": "ecotutorialsmandeepapi.classx.co.in"
    },
    {
        "name": "Edgeias",
        "api": "edgeiasapi.classx.co.in"
    },
    {
        "name": "Edu4Tech",
        "api": "edu4techapi.classx.co.in"
    },
    {
        "name": "Educaptain",
        "api": "educaptainapi.classx.co.in"
    },
    {
        "name": "Educateindia",
        "api": "educateindiaapi.classx.co.in"
    },
    {
        "name": "Educationaddaplus",
        "api": "educationaddaplusapi.classx.co.in"
    },
    {
        "name": "Educationgalaxy",
        "api": "educationgalaxyapi.classx.co.in"
    },
    {
        "name": "Educationpathshala",
        "api": "educationpathshalaapi.classx.co.in"
    },
    {
        "name": "Educationpointharidwar",
        "api": "educationpointharidwarapi.classx.co.in"
    },
    {
        "name": "Educationwithsv",
        "api": "educationsvapi.classx.co.in"
    },
    {
        "name": "Educatorsplus",
        "api": "educatorsplusapi.classx.co.in"
    },
    {
        "name": "Educracy",
        "api": "educracyapi.classx.co.in"
    },
    {
        "name": "Eduexcellence",
        "api": "eduexcellenceapi.classx.co.in"
    },
    {
        "name": "Edukrishnaofficial",
        "api": "edukrishnapi.classx.co.in"
    },
    {
        "name": "Edukunjprime",
        "api": "edukunjprimeapi.classx.co.in"
    },
    {
        "name": "Edulogy",
        "api": "edulogyapi.classx.co.in"
    },
    {
        "name": "Edumedhbymahipalsir",
        "api": "edumedhmahipalsirapi.classx.co.in"
    },
    {
        "name": "Eduparcham",
        "api": "eduapi.classx.co.in"
    },
    {
        "name": "Eduzonin",
        "api": "eduzoninapi.classx.co.in"
    },
    {
        "name": "Eeeclive",
        "api": "eeecliveapi.classx.co.in"
    },
    {
        "name": "Effectivestudy",
        "api": "effectivestudyapi.classx.co.in"
    },
    {
        "name": "Ekalavya",
        "api": "ekalavyaapi.classx.co.in"
    },
    {
        "name": "Ekdantamclasses",
        "api": "ekdantamclassesapi.classx.co.in"
    },
    {
        "name": "Ekdumbasic",
        "api": "ekdumbasicapi.classx.co.in"
    },
    {
        "name": "Ekprayas",
        "api": "ekprayasapi.classx.co.in"
    },
    {
        "name": "Elearningstudyadda",
        "api": "elearningstudyaddaapi.classx.co.in"
    },
    {
        "name": "Electricaldost",
        "api": "electricaldostapi.classx.co.in"
    },
    {
        "name": "Electricaleng",
        "api": "electricenglishapi.classx.co.in"
    },
    {
        "name": "Electricalengineeringmcq",
        "api": "electricalengineeringmcqapi.classx.co.in"
    },
    {
        "name": "Eliteiasacademy",
        "api": "eliteiasacademyapi.classx.co.in"
    },
    {
        "name": "Endeavoracademy",
        "api": "endeavoracademyapi.classx.co.in"
    },
    {
        "name": "Engineeringfunda",
        "api": "engineeringfundaapi.classx.co.in"
    },
    {
        "name": "Engineersgroup",
        "api": "engineersgroupapi.classx.co.in"
    },
    {
        "name": "Engineerswala",
        "api": "engineerswalaapi.classx.co.in"
    },
    {
        "name": "Engineerswaveinstitute",
        "api": "engineerswaveinstituteapi.classx.co.in"
    },
    {
        "name": "Englishbyamysir",
        "api": "englishbyamysirapi.classx.co.in"
    },
    {
        "name": "Englishbydksir",
        "api": "englishdksirapi.classx.co.in"
    },
    {
        "name": "Englishbyjaisir",
        "api": "englishjaisirapi.classx.co.in"
    },
    {
        "name": "Englishbyroshansir",
        "api": "englishroshansirapi.classx.co.in"
    },
    {
        "name": "Englishbyvijender",
        "api": "englishvijenderapi.classx.co.in"
    },
    {
        "name": "Englishdiscovery",
        "api": "englishdiscoveryapi.classx.co.in"
    },
    {
        "name": "Englishdriveonline",
        "api": "englishdriveonlineapi.classx.co.in"
    },
    {
        "name": "Englishforall",
        "api": "englishforallapi.classx.co.in"
    },
    {
        "name": "Englishfromzero",
        "api": "englishfromzeroapi.classx.co.in"
    },
    {
        "name": "Englishgrammarbyrahulaute",
        "api": "englishgrammarrahulauteapi.classx.co.in"
    },
    {
        "name": "Englishnotebook",
        "api": "englishnotebookapi.classx.co.in"
    },
    {
        "name": "Englishramesh",
        "api": "englishrameshapi.classx.co.in"
    },
    {
        "name": "Englishwithashutoshsir",
        "api": "englishashutoshsirapi.classx.co.in"
    },
    {
        "name": "Englishwithbalasaheb",
        "api": "englishwithbalasahebapi.classx.co.in"
    },
    {
        "name": "Englishwithheman",
        "api": "englishwithhemantapi.classx.co.in"
    },
    {
        "name": "Englishwithnitinsir",
        "api": "englishnitinsirapi.classx.co.in"
    },
    {
        "name": "Englishwithrajesh",
        "api": "englishrajeshapi.classx.co.in"
    },
    {
        "name": "Englishwithsanjeevsir",
        "api": "englishsanjeevsirapi.classx.co.in"
    },
    {
        "name": "Englishworld",
        "api": "englishworldapi.classx.co.in"
    },
    {
        "name": "Englisio",
        "api": "englisioapi.classx.co.in"
    },
    {
        "name": "Envisionjeeneet",
        "api": "envisionjeeneetapi.classx.co.in"
    },
    {
        "name": "Erdr",
        "api": "erdrapi.classx.co.in"
    },
    {
        "name": "Ervkguptacampusexammantra",
        "api": "ervkguptacampusapi.classx.co.in"
    },
    {
        "name": "Et",
        "api": "etapi.classx.co.in"
    },
    {
        "name": "Etcenglishtrainingcentre",
        "api": "englishtrainingcentreapi.classx.co.in"
    },
    {
        "name": "Etechpathashala",
        "api": "etechpathashalaapi.classx.co.in"
    },
    {
        "name": "Etestseriestestbook",
        "api": "etestseriescompetitiveexamstestbookapi.classx.co.in"
    },
    {
        "name": "Ethicaedutech",
        "api": "ethicaedutechapi.classx.co.in"
    },
    {
        "name": "Eurekaacademylive",
        "api": "eurekaacademyliveapi.classx.co.in"
    },
    {
        "name": "Exam",
        "api": "examjunctionapi.classx.co.in"
    },
    {
        "name": "Exama2Z",
        "api": "exama2zapi.classx.co.in"
    },
    {
        "name": "Examadda360",
        "api": "examadda360api.classx.co.in"
    },
    {
        "name": "Examania",
        "api": "examaniaapi.classx.co.in"
    },
    {
        "name": "Examaspirants",
        "api": "examaspirantsapi.classx.co.in"
    },
    {
        "name": "Examboardhsscssccet",
        "api": "examboardhsscssccetapi.classx.co.in"
    },
    {
        "name": "Exambulls9",
        "api": "exambulls9api.classx.co.in"
    },
    {
        "name": "Examchase",
        "api": "examchaseapi.classx.co.in"
    },
    {
        "name": "Examchip",
        "api": "examchipapi.classx.co.in"
    },
    {
        "name": "Examcoach",
        "api": "examcoachapi.classx.co.in"
    },
    {
        "name": "Examdost",
        "api": "examdostapi.classx.co.in"
    },
    {
        "name": "Examdrishti",
        "api": "examdrishtiapi.classx.co.in"
    },
    {
        "name": "Exameducation",
        "api": "exameducationapi.classx.co.in"
    },
    {
        "name": "Exameducator",
        "api": "exameducatorapi.classx.co.in"
    },
    {
        "name": "Examfactacademy",
        "api": "examfactacademyapi.classx.co.in"
    },
    {
        "name": "Examfirst",
        "api": "englishallinoneapi.classx.co.in"
    },
    {
        "name": "Examgravity",
        "api": "examgravityapi.classx.co.in"
    },
    {
        "name": "Examguideapp",
        "api": "examguideappapi.classx.co.in"
    },
    {
        "name": "Examguruji",
        "api": "examgurujiapi.classx.co.in"
    },
    {
        "name": "Examgurutipsandtricks",
        "api": "examgurutipstricksapi.classx.co.in"
    },
    {
        "name": "Examhelpline",
        "api": "examhelplineapi.classx.co.in"
    },
    {
        "name": "Examindia",
        "api": "examindiaapi.classx.co.in"
    },
    {
        "name": "Examjn",
        "api": "examjnapi.classx.co.in"
    },
    {
        "name": "Exammanch",
        "api": "exammanchapi.classx.co.in"
    },
    {
        "name": "Exammantra",
        "api": "exammantraapi.classx.co.in"
    },
    {
        "name": "Exammaster",
        "api": "exammasterapi.classx.co.in"
    },
    {
        "name": "Examnagari",
        "api": "examnagariapi.classx.co.in"
    },
    {
        "name": "Examnity",
        "api": "examnityapi.classx.co.in"
    },
    {
        "name": "Examo",
        "api": "examoapi.classx.co.in"
    },
    {
        "name": "Exampathikclasses",
        "api": "exampathikclassesapi.classx.co.in"
    },
    {
        "name": "Exampoll",
        "api": "exampollapi.classx.co.in"
    },
    {
        "name": "Examprep",
        "api": "examprepapi.classx.co.in"
    },
    {
        "name": "Examprodigital",
        "api": "examprodigitalapi.classx.co.in"
    },
    {
        "name": "Exampunjabi",
        "api": "exampunjabiapi.classx.co.in"
    },
    {
        "name": "Exampur",
        "api": "exampurappapi.classx.co.in"
    },
    {
        "name": "Examqualifier",
        "api": "examqualifierapi.classx.co.in"
    },
    {
        "name": "Examscalegovtjobsexamprep",
        "api": "examscalegovtjobsexamprepapi.classx.co.in"
    },
    {
        "name": "Examscentre247",
        "api": "examscentre247api.classx.co.in"
    },
    {
        "name": "Examsquadprofessionalhub",
        "api": "examsquadprofessionalhubapi.classx.co.in"
    },
    {
        "name": "Examsrank",
        "api": "examsrankapi.classx.co.in"
    },
    {
        "name": "Examstrong",
        "api": "examstrongapi.classx.co.in"
    },
    {
        "name": "Examstudyengineering",
        "api": "examstudyengineeringapi.classx.co.in"
    },
    {
        "name": "Examtarkash",
        "api": "examtarkashapi.classx.co.in"
    },
    {
        "name": "Examtopper",
        "api": "examtopperappapi.classx.co.in"
    },
    {
        "name": "Examtopper9",
        "api": "examtopper9api.classx.co.in"
    },
    {
        "name": "Examtricks",
        "api": "examtricksapi.classx.co.in"
    },
    {
        "name": "Examvidhi",
        "api": "examvidhiapi.classx.co.in"
    },
    {
        "name": "Examwadi",
        "api": "examwadiapi.classx.co.in"
    },
    {
        "name": "Examyug24",
        "api": "examyug24api.classx.co.in"
    },
    {
        "name": "Examzila",
        "api": "examzilaapi.classx.co.in"
    },
    {
        "name": "Examzygovtjobsexamprep",
        "api": "examzygovtjobsexamprepapi.classx.co.in"
    },
    {
        "name": "Excellencestudy",
        "api": "excellencestudyapi.classx.co.in"
    },
    {
        "name": "Expertphysics20",
        "api": "expertphysicsapi.classx.co.in"
    },
    {
        "name": "Exploringgoals",
        "api": "exploringgoalsapi.classx.co.in"
    },
    {
        "name": "Expresstrainingservices",
        "api": "expresstrainingservicesapi.classx.co.in"
    },
    {
        "name": "Faibs",
        "api": "fabisinstituteofmathematicsapi.classx.co.in"
    },
    {
        "name": "Farmeducation",
        "api": "farmeducationapi.classx.co.in"
    },
    {
        "name": "Farmeducon",
        "api": "farmeduconapi.classx.co.in"
    },
    {
        "name": "Fastrackmathsreasoning",
        "api": "fastrackandmathsreasoningapi.classx.co.in"
    },
    {
        "name": "Fatehkar",
        "api": "fatehkarapi.classx.co.in"
    },
    {
        "name": "Feelthephysics",
        "api": "feelphysicsapi.classx.co.in"
    },
    {
        "name": "Finaltouchacademy",
        "api": "finaltouchacademyapi.classx.co.in"
    },
    {
        "name": "Fipinactive",
        "api": "funpathshalaapi.classx.co.in"
    },
    {
        "name": "Fittiti",
        "api": "fittitiapi.classx.co.in"
    },
    {
        "name": "Focusacademy",
        "api": "focusacademyapi.classx.co.in"
    },
    {
        "name": "Fojicircle",
        "api": "fojicircleapi.classx.co.in"
    },
    {
        "name": "Forcegalaxy",
        "api": "forcegalaxyapi.classx.co.in"
    },
    {
        "name": "Formulator",
        "api": "formulatorapi.classx.co.in"
    },
    {
        "name": "Foundationlearning",
        "api": "foundationlearningapi.classx.co.in"
    },
    {
        "name": "Foundationmathsexam",
        "api": "foundationmathsexamapi.classx.co.in"
    },
    {
        "name": "Fourhandsedusys",
        "api": "fourhandsedusysapi.classx.co.in"
    },
    {
        "name": "Freejobsinformation",
        "api": "freejobsinformationapi.classx.co.in"
    },
    {
        "name": "Freetest",
        "api": "freetestapi.classx.co.in"
    },
    {
        "name": "Freshernowtelugu",
        "api": "freshernowteluguapi.classx.co.in"
    },
    {
        "name": "Ftiiandsrfti",
        "api": "ftiiandsrftiapi.classx.co.in"
    },
    {
        "name": "Fullscore",
        "api": "fullscoreapi.classx.co.in"
    },
    {
        "name": "Fume",
        "api": "fumeappapi.classx.co.in"
    },
    {
        "name": "Funinpathsala",
        "api": "fipapi.classx.co.in"
    },
    {
        "name": "Futurekulcollege",
        "api": "futurekulcollegeapi.classx.co.in"
    },
    {
        "name": "Futurerojgar",
        "api": "futurerojgarapi.classx.co.in"
    },
    {
        "name": "Futurewillacademy",
        "api": "futurewillacademyapi.classx.co.in"
    },
    {
        "name": "G9Studybypatelsir",
        "api": "g9studypatelsirapi.classx.co.in"
    },
    {
        "name": "Gabypiyushsir",
        "api": "gabypiyushsirapi.classx.co.in"
    },
    {
        "name": "Gadgetsonemalayalam",
        "api": "gadgetsonemalayalamapi.classx.co.in"
    },
    {
        "name": "Gaganpratapmaths",
        "api": "gaganpratapmathsapi.classx.co.in"
    },
    {
        "name": "Galaxyonlineworld",
        "api": "galaxyonlineworldapi.classx.co.in"
    },
    {
        "name": "Gamepgapp",
        "api": "gamepgappapi.classx.co.in"
    },
    {
        "name": "Gammyanirdesha",
        "api": "gammyanirdeshaapi.classx.co.in"
    },
    {
        "name": "Ganeshaglobal",
        "api": "ganeshaglobalapi.classx.co.in"
    },
    {
        "name": "Ganeshkadsacademy",
        "api": "ganeshkadacademyapi.classx.co.in"
    },
    {
        "name": "Ganeshkawaneacademy",
        "api": "ganeshkawaneacademyapi.classx.co.in"
    },
    {
        "name": "Ganpatgurukulphulera",
        "api": "ganpatgurukulphuleraapi.classx.co.in"
    },
    {
        "name": "Garvitpublications",
        "api": "garvitpublicationsapi.classx.co.in"
    },
    {
        "name": "Gateacademyvod",
        "api": "gateacademyvodapi.classx.co.in"
    },
    {
        "name": "Gatecsebyamitkhurana",
        "api": "gatecseamitkhuranaapi.classx.co.in"
    },
    {
        "name": "Gauravjunction",
        "api": "gauravjunctionapi.classx.co.in"
    },
    {
        "name": "Gauravkaushal",
        "api": "gauravkaushalapi.classx.co.in"
    },
    {
        "name": "Gauravmadhu",
        "api": "gauravmadhuapi.classx.co.in"
    },
    {
        "name": "Gauravsuthar",
        "api": "gauravsutharapi.classx.co.in"
    },
    {
        "name": "Gaurshorthandclasses",
        "api": "gaurshorthandclassesapi.classx.co.in"
    },
    {
        "name": "Gccampusbygcjakhar",
        "api": "gccampusgcjakharapi.classx.co.in"
    },
    {
        "name": "Gccniosclasses",
        "api": "gccniosclassesapi.classx.co.in"
    },
    {
        "name": "Gcentrick",
        "api": "gcentrickapi.classx.co.in"
    },
    {
        "name": "Gchemclasses",
        "api": "gchemclassesapi.classx.co.in"
    },
    {
        "name": "Gdcacademy",
        "api": "gdcacademyapi.classx.co.in"
    },
    {
        "name": "Gearinstitute",
        "api": "gearinstituteapi.classx.co.in"
    },
    {
        "name": "Geetanjaliras",
        "api": "geetanjalirasapi.classx.co.in"
    },
    {
        "name": "Genique",
        "api": "geniqueapi.classx.co.in"
    },
    {
        "name": "Geniuselearning",
        "api": "geniuselearningapi.classx.co.in"
    },
    {
        "name": "Geniusias",
        "api": "geniusiasapi.classx.co.in"
    },
    {
        "name": "Geniusinstitute",
        "api": "geniusinstituteapi.classx.co.in"
    },
    {
        "name": "Geniusmaker",
        "api": "geniusmakerapi.classx.co.in"
    },
    {
        "name": "Geniusmaths",
        "api": "geniusmathsapi.classx.co.in"
    },
    {
        "name": "Geniusstudycircle",
        "api": "geniusstudycircleapi.classx.co.in"
    },
    {
        "name": "Geniusvidyarthi",
        "api": "geniusvidyarthiapi.classx.co.in"
    },
    {
        "name": "Gennextcareeracademy",
        "api": "gennextcareeracademyapi.classx.co.in"
    },
    {
        "name": "Genomicmedical",
        "api": "genomicmedicalapi.teachx.in"
    },
    {
        "name": "Genomicmedicalandnursing",
        "api": "genomicmedicalapi.classx.co.in"
    },
    {
        "name": "Geobyavdhutsir",
        "api": "geoavbhutsirapi.classx.co.in"
    },
    {
        "name": "Geographyacademy",
        "api": "geographyacademyapi.classx.co.in"
    },
    {
        "name": "Geographyandagriculturebypvsir",
        "api": "geographyagriculturepvsirapi.classx.co.in"
    },
    {
        "name": "Geographybydrvikaschoudhary",
        "api": "geographyvikaschoudharyapi.classx.co.in"
    },
    {
        "name": "Geographybyjanaiahsir",
        "api": "geographyjanaiahsirapi.classx.co.in"
    },
    {
        "name": "Geographybysachinshinde",
        "api": "geographysachinshindeapi.classx.co.in"
    },
    {
        "name": "Geographybyyogeshsir",
        "api": "geographyyogeshsirapi.classx.co.in"
    },
    {
        "name": "Geologywala",
        "api": "geologywalaapi.classx.co.in"
    },
    {
        "name": "Geopixelacademy",
        "api": "geopixelacademyapi.classx.co.in"
    },
    {
        "name": "Getapt",
        "api": "getaptapi.classx.co.in"
    },
    {
        "name": "Ggtfit",
        "api": "ggtfitapi.classx.co.in"
    },
    {
        "name": "Gkbysatishshindelatur",
        "api": "gksatishshindelaturapi.classx.co.in"
    },
    {
        "name": "Gkcafe",
        "api": "gkcafeapi.classx.co.in"
    },
    {
        "name": "Gkgsmasti",
        "api": "gkgsmastiapi.classx.co.in"
    },
    {
        "name": "Gkhouseexams",
        "api": "gkhouseexamsapi.classx.co.in"
    },
    {
        "name": "Gkmathsreasoning",
        "api": "gkmathsreasoningapi.classx.co.in"
    },
    {
        "name": "Gknagri",
        "api": "gknagriapi.classx.co.in"
    },
    {
        "name": "Gksacademyudaipur",
        "api": "gksacademyudaipurapi.classx.co.in"
    },
    {
        "name": "Gkstudygovtexamspreparation",
        "api": "gkstudygovtexamspreparationapi.classx.co.in"
    },
    {
        "name": "Gkwalesonusir",
        "api": "gkwalesonusirapi.classx.co.in"
    },
    {
        "name": "Gkwithvikassuthar",
        "api": "gkvikassutharapi.classx.co.in"
    },
    {
        "name": "Globalclasses",
        "api": "globalclassesapi.classx.co.in"
    },
    {
        "name": "Gmacademympsc",
        "api": "gmacademympscapi.classx.co.in"
    },
    {
        "name": "Gmade",
        "api": "gmadeapi.classx.co.in"
    },
    {
        "name": "Gnceducare",
        "api": "gnceducareapi.classx.co.in"
    },
    {
        "name": "Goalinstitute",
        "api": "goalinstituteapi.classx.co.in"
    },
    {
        "name": "Goalyaan",
        "api": "goalyaanapi.classx.co.in"
    },
    {
        "name": "Goforeducation",
        "api": "goforeducationapi.classx.co.in"
    },
    {
        "name": "Gogreen",
        "api": "gogreenapi.classx.co.in"
    },
    {
        "name": "Goldencareer",
        "api": "goldencareersapi.classx.co.in"
    },
    {
        "name": "Gonagannareddypublications",
        "api": "gonagannareddypublicationsapi.classx.co.in"
    },
    {
        "name": "Gonitchorcha",
        "api": "gonitchorchaapi.classx.co.in"
    },
    {
        "name": "Gopalgirisirmathsreasoning",
        "api": "gopalgirisirmathsreasoningapi.classx.co.in"
    },
    {
        "name": "Govidya",
        "api": "govidyaapi.classx.co.in"
    },
    {
        "name": "Govtjobs",
        "api": "govtjobswalaapi.classx.co.in"
    },
    {
        "name": "Gradeupstudy",
        "api": "gradeupstudyapi.classx.co.in"
    },
    {
        "name": "Greatconcept",
        "api": "greatconceptapi.classx.co.in"
    },
    {
        "name": "Greatgeniuses",
        "api": "greatgeniusesapi.classx.co.in"
    },
    {
        "name": "Greenboard",
        "api": "greenboardapi.classx.co.in"
    },
    {
        "name": "Groskill",
        "api": "groskillapi.classx.co.in"
    },
    {
        "name": "Growacademy",
        "api": "growacademyapi.classx.co.in"
    },
    {
        "name": "Gsbymanojsir",
        "api": "gsmanojsirapi.classx.co.in"
    },
    {
        "name": "Gsbyuttamgore",
        "api": "gsuttamgoreapi.classx.co.in"
    },
    {
        "name": "Gsforum",
        "api": "gsforumapi.classx.co.in"
    },
    {
        "name": "Gsforumofficial",
        "api": "gsforumofficialapi.classx.co.in"
    },
    {
        "name": "Gsmedicalacademy",
        "api": "gsmedicalacademyapi.classx.co.in"
    },
    {
        "name": "Gsmlive",
        "api": "gsmliveapi.classx.co.in"
    },
    {
        "name": "Gsplanetinstitute",
        "api": "gsplanetinstituteapi.classx.co.in"
    },
    {
        "name": "Gswithsandeeptyagi",
        "api": "gswithsandeeptyagiapi.classx.co.in"
    },
    {
        "name": "Gsworldonline",
        "api": "gsworldonlineapi.classx.co.in"
    },
    {
        "name": "Gtdefenceacademy",
        "api": "gtdefenceacademyapi.classx.co.in"
    },
    {
        "name": "Guardeer",
        "api": "guardeerapi.classx.co.in"
    },
    {
        "name": "Gulshanbeldarsacademy",
        "api": "gulshanbeldarsacademyapi.classx.co.in"
    },
    {
        "name": "Gupteshsiryudhhabhyasiasacademy",
        "api": "gupteshsiryudhhabhyasiasacademyapi.classx.co.in"
    },
    {
        "name": "Guruclassesjaipur",
        "api": "guruclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Gurudakshina",
        "api": "gurudakshinaapi.classx.co.in"
    },
    {
        "name": "Gurueducationhub",
        "api": "gurueducationhubapi.classx.co.in"
    },
    {
        "name": "Guruelearning",
        "api": "guruonlineclassesapi.classx.co.in"
    },
    {
        "name": "Gurujikags",
        "api": "gurujikagsapi.classx.co.in"
    },
    {
        "name": "Gurujiworldexamstudy",
        "api": "gurujiworldexamstudyapi.classx.co.in"
    },
    {
        "name": "Gurukulacademy",
        "api": "gurukulacademyapi.classx.co.in"
    },
    {
        "name": "Gurukulaenglishtestseries",
        "api": "gurukulaenglishtestseriesapi.classx.co.in"
    },
    {
        "name": "Gurukularmy",
        "api": "gurukularmyapi.classx.co.in"
    },
    {
        "name": "Gurukulplus",
        "api": "gurukulplusapi.classx.co.in"
    },
    {
        "name": "Gurukulprabhodhiniinstitute",
        "api": "gurukulprabodhinipuneapi.classx.co.in"
    },
    {
        "name": "Gururehman",
        "api": "gururehmanapi.classx.co.in"
    },
    {
        "name": "Gururehmansirliveclasses",
        "api": "gururehmansirliveclassesapi.classx.co.in"
    },
    {
        "name": "Gurushalateachersacademy",
        "api": "gurushalateachersacademyapi.classx.co.in"
    },
    {
        "name": "Gvkaksha",
        "api": "gvkakshaapi.classx.co.in"
    },
    {
        "name": "Gyanaj",
        "api": "gyanajapi.classx.co.in"
    },
    {
        "name": "Gyanbindu",
        "api": "gyanbinduapi.appx.co.in"
    },
    {
        "name": "Gyanbindu",
        "api": "gyanbinduapi.classx.co.in"
    },
    {
        "name": "Gyanbook",
        "api": "gyanbookapi.classx.co.in"
    },
    {
        "name": "Gyanbooster",
        "api": "gyanboosterapi.classx.co.in"
    },
    {
        "name": "Gyangangaofficial",
        "api": "gyangangaofficialapi.classx.co.in"
    },
    {
        "name": "Gyanhub",
        "api": "gyanhubapi.classx.co.in"
    },
    {
        "name": "Gyanias",
        "api": "gyaniasapi.classx.co.in"
    },
    {
        "name": "Gyanjyoti",
        "api": "gyanjyotiapi.classx.co.in"
    },
    {
        "name": "Gyankunjacademy",
        "api": "gyankunjacademyapi.classx.co.in"
    },
    {
        "name": "Gyankurfoundation",
        "api": "gyankurfoundationapi.classx.co.in"
    },
    {
        "name": "Gyanmadeias",
        "api": "gyanmadeiasapi.classx.co.in"
    },
    {
        "name": "Gyannidhiclasses",
        "api": "gyannidhiclassesapi.classx.co.in"
    },
    {
        "name": "Gyanodaykeguruji",
        "api": "gyanodaygurujiapi.classx.co.in"
    },
    {
        "name": "Gyansootra",
        "api": "gyansootraapi.classx.co.in"
    },
    {
        "name": "Gyansthalicommerceclasses",
        "api": "gyansthalicommerceclassesapi.classx.co.in"
    },
    {
        "name": "Gyanxp",
        "api": "gyanxpapi.classx.co.in"
    },
    {
        "name": "H2Sonlineclasses",
        "api": "h2sonlineclassesapi.classx.co.in"
    },
    {
        "name": "Haacademy",
        "api": "haacademyapi.classx.co.in"
    },
    {
        "name": "Hadacompetition",
        "api": "hadacompetitionapi.classx.co.in"
    },
    {
        "name": "Hamaraplatformlearningapp",
        "api": "hamaraplatformlearningappapi.classx.co.in"
    },
    {
        "name": "Hamariacademyofficial",
        "api": "hamariacademyofficialapi.classx.co.in"
    },
    {
        "name": "Hamaripariksha",
        "api": "hamariparikshaapi.classx.co.in"
    },
    {
        "name": "Handbookacademy",
        "api": "handbookacademyapi.classx.co.in"
    },
    {
        "name": "Hanumanshindesprashasancareeracademy",
        "api": "hanumanshindesprashasancareeracademyapi.classx.co.in"
    },
    {
        "name": "Happyacademy",
        "api": "happyacademyapi.classx.co.in"
    },
    {
        "name": "Harishtiwariclasses",
        "api": "harishtiwariclassesapi.classx.co.in"
    },
    {
        "name": "Harkiratsingh",
        "api": "harkiratapi.classx.co.in"
    },
    {
        "name": "Harshithinstitute",
        "api": "harshithinstituteapi.classx.co.in"
    },
    {
        "name": "Haryanajobcity",
        "api": "haryanajobcityapi.classx.co.in"
    },
    {
        "name": "Hcverma",
        "api": "hcvermaapi.classx.co.in"
    },
    {
        "name": "Hellorajasthan",
        "api": "hellorajasthanapi.classx.co.in"
    },
    {
        "name": "Hellosahitya",
        "api": "hellosahityaapi.classx.co.in"
    },
    {
        "name": "Hellosirexampreparationapp",
        "api": "hellosirexampreparationapi.classx.co.in"
    },
    {
        "name": "Helloworldbyprince",
        "api": "helloworldprinceapi.classx.co.in"
    },
    {
        "name": "Hexamathsbyranjitsinhrajput",
        "api": "hexamathsranjitsinhrajputapi.classx.co.in"
    },
    {
        "name": "Hgaurclassespro",
        "api": "hgaurclassesproapi.classx.co.in"
    },
    {
        "name": "Highlandparamedicalinstitute",
        "api": "highlandparamedicalinstituteapi.classx.co.in"
    },
    {
        "name": "Himalayacoachingclasses",
        "api": "himalayacoachingclassesapi.classx.co.in"
    },
    {
        "name": "Himalayaeduhub",
        "api": "himalayaeduhubapi.classx.co.in"
    },
    {
        "name": "Himankclasses",
        "api": "himankclassesapi.classx.co.in"
    },
    {
        "name": "Himanshusirclasses",
        "api": "himanshusirclassesapi.classx.co.in"
    },
    {
        "name": "Himveer",
        "api": "himveerapi.classx.co.in"
    },
    {
        "name": "Hinddefenceacademy",
        "api": "hinddefenceacademyapi.classx.co.in"
    },
    {
        "name": "Hindiadhyapak",
        "api": "hindiadhyapakapi.classx.co.in"
    },
    {
        "name": "Hindiclasses",
        "api": "hindiclassesapi.classx.co.in"
    },
    {
        "name": "Hindijoshisir",
        "api": "hindijoshisirapi.classx.co.in"
    },
    {
        "name": "Hindimaster",
        "api": "hindimasterapi.classx.co.in"
    },
    {
        "name": "Hindipoint",
        "api": "hindipointapi.classx.co.in"
    },
    {
        "name": "Hindustanclasses",
        "api": "hindustanclassesapi.classx.co.in"
    },
    {
        "name": "Historicaacademy",
        "api": "historicaacademyapi.classx.co.in"
    },
    {
        "name": "History360",
        "api": "history360api.classx.co.in"
    },
    {
        "name": "Historybychanchalsir",
        "api": "historychanchalsirapi.classx.co.in"
    },
    {
        "name": "Historybypawansir",
        "api": "historypawanapi.classx.co.in"
    },
    {
        "name": "Historybysachingulig",
        "api": "historysachinguligapi.classx.co.in"
    },
    {
        "name": "Historylok",
        "api": "historylokapi.classx.co.in"
    },
    {
        "name": "Historywithrohitsir",
        "api": "historywithrohitsirapi.classx.co.in"
    },
    {
        "name": "Hitechlearningacademy",
        "api": "hitechlearningacademyapi.classx.co.in"
    },
    {
        "name": "Hiteshsirgyankosh",
        "api": "hiteshsirgyankoshapi.classx.co.in"
    },
    {
        "name": "Homesciencehub",
        "api": "homesciencehubapi.classx.co.in"
    },
    {
        "name": "Hopeeducationjmk",
        "api": "hopeeducationjmkapi.classx.co.in"
    },
    {
        "name": "Horizoniasacademy",
        "api": "horizoniasacademyapi.classx.co.in"
    },
    {
        "name": "Hornbill",
        "api": "hornbillclassesapi.classx.co.in"
    },
    {
        "name": "Hpsuccessclasses",
        "api": "hpsuccessclassesapi.classx.co.in"
    },
    {
        "name": "Hrjprep",
        "api": "hrjprepapi.classx.co.in"
    },
    {
        "name": "Htcclassesbysksir",
        "api": "htcclassessksirapi.classx.co.in"
    },
    {
        "name": "Hundredsxdevs",
        "api": "100xdevsapi.classx.co.in"
    },
    {
        "name": "Iace",
        "api": "iaceapi.classx.co.in"
    },
    {
        "name": "Iaceonlineclasses",
        "api": "iaceonlineclassesapi.classx.co.in"
    },
    {
        "name": "Iasbabuji",
        "api": "iasbabujiapi.classx.co.in"
    },
    {
        "name": "Iasplus",
        "api": "iasplusapi.classx.co.in"
    },
    {
        "name": "Iceonline",
        "api": "iceonlineapi.classx.co.in"
    },
    {
        "name": "Icoaching",
        "api": "icoachingapi.classx.co.in"
    },
    {
        "name": "Ics",
        "api": "icsapi.classx.co.in"
    },
    {
        "name": "Icseconnect",
        "api": "icseconnectapi.classx.co.in"
    },
    {
        "name": "Idealachiever",
        "api": "idealachieverapi.classx.co.in"
    },
    {
        "name": "Idealnursingclasses",
        "api": "idealnursingclassesapi.classx.co.in"
    },
    {
        "name": "Idealonlineschool",
        "api": "idealonlineschoolapi.classx.co.in"
    },
    {
        "name": "Ignite247",
        "api": "ignite247api.classx.co.in"
    },
    {
        "name": "Ignitetuition",
        "api": "ignitetuitionapi.classx.co.in"
    },
    {
        "name": "Iitguide",
        "api": "iitguideapi.classx.co.in"
    },
    {
        "name": "Iitianconcept",
        "api": "iitianconceptapi.classx.co.in"
    },
    {
        "name": "Iitiansacademyonline",
        "api": "iitiansacademyonlineapi.classx.co.in"
    },
    {
        "name": "Ilearncenter",
        "api": "ilearncenterapi.classx.co.in"
    },
    {
        "name": "Ilmitms",
        "api": "ilmitmsapi.classx.co.in"
    },
    {
        "name": "Imfsstudyabroad",
        "api": "imfsstudyabroadapi.classx.co.in"
    },
    {
        "name": "Impetusedutech",
        "api": "impetusedutechapi.classx.co.in"
    },
    {
        "name": "Imransirmaths",
        "api": "imransirmathsapi.classx.co.in"
    },
    {
        "name": "Incredibleacademy",
        "api": "incredibleacademyapi.classx.co.in"
    },
    {
        "name": "Indiabiology",
        "api": "indiabiologyapi.classx.co.in"
    },
    {
        "name": "Indianeducator",
        "api": "indianeducatorapi.classx.co.in"
    },
    {
        "name": "Indiannews20",
        "api": "indiannews20api.classx.co.in"
    },
    {
        "name": "Indianrojgar",
        "api": "indianrojgarapi.classx.co.in"
    },
    {
        "name": "Indiashastralearningapp",
        "api": "indiashastralearningappapi.classx.co.in"
    },
    {
        "name": "Indorecscacademy",
        "api": "indorecscacademyapi.classx.co.in"
    },
    {
        "name": "Indorephysicalacademy",
        "api": "indorephysicalacademyapi.classx.co.in"
    },
    {
        "name": "Indused",
        "api": "indusedapi.classx.co.in"
    },
    {
        "name": "Infinimix",
        "api": "infinimixapi.classx.co.in"
    },
    {
        "name": "Infinityclassesjaipur",
        "api": "infinityclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Infiqueclasses",
        "api": "infiqueclassesapi.classx.co.in"
    },
    {
        "name": "Informativeinstitute",
        "api": "informativeinstituteapi.classx.co.in"
    },
    {
        "name": "Infotrade",
        "api": "infotradeapi.appx.co.in"
    },
    {
        "name": "Infotrade",
        "api": "infotradeapi.classx.co.in"
    },
    {
        "name": "Ingliaacademy",
        "api": "ingliaacademyapi.classx.co.in"
    },
    {
        "name": "Inspireindiaacademy",
        "api": "inspireindiaacademyapi.classx.co.in"
    },
    {
        "name": "Inspirerasacademy",
        "api": "inspirerasacademyapi.classx.co.in"
    },
    {
        "name": "Inspiresoftskills",
        "api": "inspiresoftskillsapi.classx.co.in"
    },
    {
        "name": "Instacademy",
        "api": "instacademyapi.classx.co.in"
    },
    {
        "name": "Instituteofcomputereducation",
        "api": "institutecomputereducationapi.classx.co.in"
    },
    {
        "name": "Intelectoin",
        "api": "intelectoinapi.classx.co.in"
    },
    {
        "name": "Investaajforkal",
        "api": "investaajforkalapi.classx.co.in"
    },
    {
        "name": "Investschool",
        "api": "investschoolapi.classx.co.in"
    },
    {
        "name": "Iosreview",
        "api": "iosreviewapi.classx.co.in"
    },
    {
        "name": "Ipaperclasses",
        "api": "ipaperclassesapi.classx.co.in"
    },
    {
        "name": "Ipbuddy",
        "api": "ipbuddyapi.classx.co.in"
    },
    {
        "name": "Iqacademy",
        "api": "iqacademyapi.classx.co.in"
    },
    {
        "name": "Iqhike",
        "api": "iqhikeapi.classx.co.in"
    },
    {
        "name": "Iraias",
        "api": "iraiasapi.classx.co.in"
    },
    {
        "name": "Iriseacademy",
        "api": "iriseacademyapi.classx.co.in"
    },
    {
        "name": "Irshatech",
        "api": "irshatechapi.classx.co.in"
    },
    {
        "name": "Ischool24",
        "api": "ischool24api.classx.co.in"
    },
    {
        "name": "Itcorner",
        "api": "itcornerapi.classx.co.in"
    },
    {
        "name": "Itihasinstitution",
        "api": "itihasinstitutionapi.classx.co.in"
    },
    {
        "name": "Itpathshala",
        "api": "itpathshalaapi.classx.co.in"
    },
    {
        "name": "Itshaala",
        "api": "itshaalaapi.classx.co.in"
    },
    {
        "name": "Itspiderspune",
        "api": "itspiderspuneapi.classx.co.in"
    },
    {
        "name": "Ivaclasses",
        "api": "ivaclassesapi.classx.co.in"
    },
    {
        "name": "Jagrutawaaz",
        "api": "jagrutawaazapi.classx.co.in"
    },
    {
        "name": "Jagrutiacademy",
        "api": "jagrutiacademyapi.classx.co.in"
    },
    {
        "name": "Jaibharatonlineclasses",
        "api": "jaibharatapi.classx.co.in"
    },
    {
        "name": "Jaihostudy",
        "api": "jaihostudyapi.classx.co.in"
    },
    {
        "name": "Jaipalvishwakarma",
        "api": "jaipalvishwakarmaapi.classx.co.in"
    },
    {
        "name": "Jaipurcoachingcentre",
        "api": "jaipurcoachingcentreapi.classx.co.in"
    },
    {
        "name": "Javatechie",
        "api": "javatechieapi.classx.co.in"
    },
    {
        "name": "Jawaharnavodyavidhalaya",
        "api": "jawaharnavodayvidhalayapraveshparikshaapi.classx.co.in"
    },
    {
        "name": "Jayacademyfornursing",
        "api": "jayacademyfornursingapi.classx.co.in"
    },
    {
        "name": "Jaydurgamechanical",
        "api": "jaydurgamechanicalapi.classx.co.in"
    },
    {
        "name": "Jayramclasses",
        "api": "jayramclassesapi.classx.co.in"
    },
    {
        "name": "Jeeone",
        "api": "jeeoneapi.classx.co.in"
    },
    {
        "name": "Jeesankalplive",
        "api": "jeesankalpliveapi.classx.co.in"
    },
    {
        "name": "Jeeskool",
        "api": "jeeskoolapi.classx.co.in"
    },
    {
        "name": "Jeetendrakumar",
        "api": "jeetendrakumarapi.classx.co.in"
    },
    {
        "name": "Jeewithajay",
        "api": "jeewithajayapi.classx.co.in"
    },
    {
        "name": "Jescorer",
        "api": "jescorerapi.classx.co.in"
    },
    {
        "name": "Jhansiinstituteofcommerce",
        "api": "jhansiinstitutecommerceapi.classx.co.in"
    },
    {
        "name": "Jharpathshala",
        "api": "jharpathshalaapi.classx.co.in"
    },
    {
        "name": "Jhguru",
        "api": "jhguruapi.classx.co.in"
    },
    {
        "name": "Jiddpolicetrainingbymaheshsir",
        "api": "jiddpolicetrainingapi.classx.co.in"
    },
    {
        "name": "Jittisirclasses",
        "api": "jittisirclassesapi.classx.co.in"
    },
    {
        "name": "Jittuclasses",
        "api": "jittuclassesapi.classx.co.in"
    },
    {
        "name": "Jkcivilservices",
        "api": "jkcivilservicesapi.classx.co.in"
    },
    {
        "name": "Jkssbstudyfast",
        "api": "jkssbstudyfastapi.classx.co.in"
    },
    {
        "name": "Jkssbstudypoint",
        "api": "jkssbstudypointapi.classx.co.in"
    },
    {
        "name": "Jnanadegula",
        "api": "jnanadegulaapi.classx.co.in"
    },
    {
        "name": "Jobbadi",
        "api": "jobbadiapi.classx.co.in"
    },
    {
        "name": "Jobstarget",
        "api": "jobstargetapi.classx.co.in"
    },
    {
        "name": "Joshonlineexams",
        "api": "joshonlineexamsapi.classx.co.in"
    },
    {
        "name": "Jpiasacademy",
        "api": "jpiasacademyapi.classx.co.in"
    },
    {
        "name": "Jpmathsolutions",
        "api": "jpmathsolutionsapi.classx.co.in"
    },
    {
        "name": "Jrtutorials",
        "api": "jrtutorialsapi.classx.co.in"
    },
    {
        "name": "Jscafe",
        "api": "jscafeapi.classx.co.in"
    },
    {
        "name": "Jscivil",
        "api": "jscivilapi.classx.co.in"
    },
    {
        "name": "Jsyatra",
        "api": "jsyatraapi.classx.co.in"
    },
    {
        "name": "Jtc",
        "api": "jtcapi.classx.co.in"
    },
    {
        "name": "Jtcthelearningapp",
        "api": "jawalateachingclassesapi.classx.co.in"
    },
    {
        "name": "Judicialaddaexamprep",
        "api": "judicialaddaexamprepapi.classx.co.in"
    },
    {
        "name": "Jugalsirclasses",
        "api": "jugalsirclassesapi.classx.co.in"
    },
    {
        "name": "Junoon",
        "api": "junoonapi.classx.co.in"
    },
    {
        "name": "Juristest",
        "api": "juristestapi.classx.co.in"
    },
    {
        "name": "Justwellclasses",
        "api": "justwellclassesapi.classx.co.in"
    },
    {
        "name": "Jyotinagpal",
        "api": "jyotinagpalapi.classx.co.in"
    },
    {
        "name": "Kagr",
        "api": "kagrapi.classx.co.in"
    },
    {
        "name": "Kaivalyathewisdom",
        "api": "kaivalyathewisdomapi.classx.co.in"
    },
    {
        "name": "Kaizenacademy",
        "api": "kaizenacademyapi.classx.co.in"
    },
    {
        "name": "Kalamacademy",
        "api": "kalamacademyapi.classx.co.in"
    },
    {
        "name": "Kalamkranti",
        "api": "kalamkrantiapi.classx.co.in"
    },
    {
        "name": "Kalpenglishacademy",
        "api": "kalpenglishacademyapi.classx.co.in"
    },
    {
        "name": "Kalyanipublication",
        "api": "kalyanipublicationapi.classx.co.in"
    },
    {
        "name": "Kalyansenglishworld",
        "api": "kalyansenglishworldapi.classx.co.in"
    },
    {
        "name": "Kannadaacademy",
        "api": "kannadaacademyapi.classx.co.in"
    },
    {
        "name": "Kapilpahuja",
        "api": "kapilpahujaapi.classx.co.in"
    },
    {
        "name": "Karadcoachingclasses",
        "api": "karadcoachingclassesapi.classx.co.in"
    },
    {
        "name": "Karlapudikrishna",
        "api": "karlapudikrishnaapi.classx.co.in"
    },
    {
        "name": "Karnomatics",
        "api": "karnomaticsapi.classx.co.in"
    },
    {
        "name": "Kataralearning",
        "api": "kataralearningapi.classx.co.in"
    },
    {
        "name": "Katariaclassesnarnaul",
        "api": "katariaclassesnarnaulapi.classx.co.in"
    },
    {
        "name": "Kathaayurveda",
        "api": "kathaayurvedaapi.classx.co.in"
    },
    {
        "name": "Kauserclasses",
        "api": "kauserclassesapi.classx.co.in"
    },
    {
        "name": "Kautilyaacademy",
        "api": "kautilyaacademyapi.classx.co.in"
    },
    {
        "name": "Kautilyaacademysatara",
        "api": "kautilyaacademysataraapi.classx.co.in"
    },
    {
        "name": "Kautilyaalp",
        "api": "kautilyaalpjeapi.classx.co.in"
    },
    {
        "name": "Kautilyans",
        "api": "kautilyansapi.classx.co.in"
    },
    {
        "name": "Kaydepanditlawacademy",
        "api": "kaydepanditlawacademyapi.classx.co.in"
    },
    {
        "name": "Kazisironlinecoaching",
        "api": "kazisironlinecoachingapi.classx.co.in"
    },
    {
        "name": "Kccoaching",
        "api": "kccoachingapi.classx.co.in"
    },
    {
        "name": "Keertipurswani",
        "api": "keertipurswaniapi.classx.co.in"
    },
    {
        "name": "Kelvinlive",
        "api": "kelvinliveapi.classx.co.in"
    },
    {
        "name": "Kelwinthelearningapp",
        "api": "kelwinlearningapi.classx.co.in"
    },
    {
        "name": "Kendretestseries",
        "api": "kendretestseriesapi.classx.co.in"
    },
    {
        "name": "Keyofsuccess",
        "api": "keyofsuccessapi.classx.co.in"
    },
    {
        "name": "Kgf",
        "api": "kgfapi.classx.co.in"
    },
    {
        "name": "Kgmmission",
        "api": "kgmmissionapi.classx.co.in"
    },
    {
        "name": "Kgskautilyagroupofstudies",
        "api": "kgskautilyagroupstudiesapi.classx.co.in"
    },
    {
        "name": "Khantimethod",
        "api": "khantimethodapi.classx.co.in"
    },
    {
        "name": "Kharatacademy",
        "api": "kharatacademyapi.classx.co.in"
    },
    {
        "name": "Khuranastudyofficial",
        "api": "khuranastudyofficialapi.classx.co.in"
    },
    {
        "name": "Kico",
        "api": "kicoappapi.classx.co.in"
    },
    {
        "name": "Kinjallearning",
        "api": "kinjallearningapi.classx.co.in"
    },
    {
        "name": "Kiranacademy",
        "api": "kiranacademyapi.classx.co.in"
    },
    {
        "name": "Kiranguruji",
        "api": "kirangurujiapi.classx.co.in"
    },
    {
        "name": "Kiroshaacademy",
        "api": "kiroshaacademyapi.classx.co.in"
    },
    {
        "name": "Kiswacareeracademy",
        "api": "kiswacareeracademyapi.akamai.net.in"
    },
    {
        "name": "Kjwisdomclasses",
        "api": "kjwisdomclassesapi.classx.co.in"
    },
    {
        "name": "Kmdsaharanpur",
        "api": "kmdsaharanpurapi.classx.co.in"
    },
    {
        "name": "Kmenglishclasses",
        "api": "kmenglishclassesapi.classx.co.in"
    },
    {
        "name": "Knowledgeaccount",
        "api": "knowledgeaccountapi.classx.co.in"
    },
    {
        "name": "Knowledgebeam",
        "api": "knowledgebeamapi.classx.co.in"
    },
    {
        "name": "Knowledgebox",
        "api": "knowledgeboxapi.classx.co.in"
    },
    {
        "name": "Knowledgetopking20",
        "api": "knowledgetopkingapi.classx.co.in"
    },
    {
        "name": "Knrlogics",
        "api": "knrlogicsapi.classx.co.in"
    },
    {
        "name": "Komyaeducation",
        "api": "komyaeducationapi.classx.co.in"
    },
    {
        "name": "Konsacollegecollegesetu",
        "api": "konsacollegeapi.classx.co.in"
    },
    {
        "name": "Kotputlilaweducation",
        "api": "kotputlilaweducationapi.classx.co.in"
    },
    {
        "name": "Kpsirsbiologyclasses",
        "api": "kpsirbiologyclassesapi.classx.co.in"
    },
    {
        "name": "Kredozthelearningapp",
        "api": "kredozlearningapi.classx.co.in"
    },
    {
        "name": "Kreduhub",
        "api": "kreduhubapi.classx.co.in"
    },
    {
        "name": "Krishinteducation",
        "api": "krishinteducationapi.classx.co.in"
    },
    {
        "name": "Krishiparikshaicaribpsupsccuetexametc",
        "api": "krishiparikshaapi.classx.co.in"
    },
    {
        "name": "Krishnaclasses",
        "api": "krishnaclassesapi.classx.co.in"
    },
    {
        "name": "Krishnacoachingcentre",
        "api": "krishnacoachingcentreapi.classx.co.in"
    },
    {
        "name": "Krishnamindset",
        "api": "krishnamindsetapi.classx.co.in"
    },
    {
        "name": "Krisshhnachemistryclasses",
        "api": "krisshnachemistryclassesapi.classx.co.in"
    },
    {
        "name": "Krushikingsagriacademy",
        "api": "krushikingsagriacademyapi.classx.co.in"
    },
    {
        "name": "Krushnamacedmyrajkot",
        "api": "krushnamacedmyrajkotapi.classx.co.in"
    },
    {
        "name": "Kskeducare",
        "api": "kskeducareapi.classx.co.in"
    },
    {
        "name": "Ksquare",
        "api": "ksquareapi.classx.co.in"
    },
    {
        "name": "Ktdtonline",
        "api": "ktdtonlineeducationapi.teachx.in"
    },
    {
        "name": "Ktdtonlineeducation",
        "api": "ktdtonlineeducationapi.classx.co.in"
    },
    {
        "name": "Kumaredutainment",
        "api": "kumaredutainmentapi.classx.co.in"
    },
    {
        "name": "Kumawatgs",
        "api": "kumawatgsapi.classx.co.in"
    },
    {
        "name": "Kumawattarunsir",
        "api": "kumawattarunsirapi.classx.co.in"
    },
    {
        "name": "Kundankishore",
        "api": "kundankishoreapi.classx.co.in"
    },
    {
        "name": "Kvclasses",
        "api": "kvclassesapi.classx.co.in"
    },
    {
        "name": "Kvkfoundation",
        "api": "kvkfoundationapi.classx.co.in"
    },
    {
        "name": "Lakshacademy",
        "api": "lakshacademyapi.classx.co.in"
    },
    {
        "name": "Lakshmimaths",
        "api": "lakshmimathsapi.classx.co.in"
    },
    {
        "name": "Lakshya",
        "api": "lakshyaclassesapi.appx.co.in"
    },
    {
        "name": "Lakshyaacademyahmednagar",
        "api": "lakshyaacademyahmednagarapi.classx.co.in"
    },
    {
        "name": "Lakshyaacademyjharkand",
        "api": "lakshyaacademyjharkhandapi.classx.co.in"
    },
    {
        "name": "Lakshyaclasses",
        "api": "lakshyaclassesapi.classx.co.in"
    },
    {
        "name": "Lakshyaclassesofficial",
        "api": "lakshyaclassesofficialapi.classx.co.in"
    },
    {
        "name": "Lakshyaclassesold",
        "api": "lakshyaclassesapi.classx.co.in"
    },
    {
        "name": "Lakshyagyananant",
        "api": "lakshyagyananantapi.classx.co.in"
    },
    {
        "name": "Lakshyaias",
        "api": "lakshyagscrackerapi.classx.co.in"
    },
    {
        "name": "Lakshyaias",
        "api": "lakshyaiasapi.classx.co.in"
    },
    {
        "name": "Lakshyamarathi",
        "api": "lakshyamarathiapi.classx.co.in"
    },
    {
        "name": "Lakshyaras",
        "api": "lakshyarasapi.classx.co.in"
    },
    {
        "name": "Lastexam",
        "api": "lastexamapi.classx.co.in"
    },
    {
        "name": "Lastmomentpadhai",
        "api": "lastmomentpadhaiapi.classx.co.in"
    },
    {
        "name": "Lawchamps",
        "api": "lawchampsapi.classx.co.in"
    },
    {
        "name": "Lawislife",
        "api": "lawlifeapi.classx.co.in"
    },
    {
        "name": "Lawlectures",
        "api": "lawlecturesapi.classx.co.in"
    },
    {
        "name": "Lawshalabyhalfpacelearnatyourownpace",
        "api": "lawshalaapi.classx.co.in"
    },
    {
        "name": "Laxaneducation",
        "api": "laxaneducationapi.classx.co.in"
    },
    {
        "name": "Learn247",
        "api": "learn247api.classx.co.in"
    },
    {
        "name": "Learn4Exam",
        "api": "learn4examapi.classx.co.in"
    },
    {
        "name": "Learnamanbarkhastudylab",
        "api": "learnamanbarkhaapi.classx.co.in"
    },
    {
        "name": "Learnandshare",
        "api": "learnshareapi.classx.co.in"
    },
    {
        "name": "Learnbyinvestt",
        "api": "learninvesttapi.classx.co.in"
    },
    {
        "name": "Learncodewithtechnicalsuneja",
        "api": "learncodetechnicalsunejaapi.classx.co.in"
    },
    {
        "name": "Learnhistorybychauhansir",
        "api": "learnhistorychauhansirapi.classx.co.in"
    },
    {
        "name": "Learnindia",
        "api": "learnindiaapi.classx.co.in"
    },
    {
        "name": "Learningadda",
        "api": "learningaddaapi.classx.co.in"
    },
    {
        "name": "Learningclasses",
        "api": "learningclassesapi.classx.co.in"
    },
    {
        "name": "Learningloop",
        "api": "learningloopapi.classx.co.in"
    },
    {
        "name": "Learningpocket",
        "api": "learningpocketapi.classx.co.in"
    },
    {
        "name": "Learningtimetelugu",
        "api": "learningtimeteluguapi.classx.co.in"
    },
    {
        "name": "Learningzone",
        "api": "learningzoneapi.classx.co.in"
    },
    {
        "name": "Learnmantra",
        "api": "learnmantraapi.classx.co.in"
    },
    {
        "name": "Learnwithchirag",
        "api": "learnchiragapi.classx.co.in"
    },
    {
        "name": "Learnwithnatarajupsc",
        "api": "learnwithnatarajupscapi.classx.co.in"
    },
    {
        "name": "Learnwithpts",
        "api": "learnwithptsapi.classx.co.in"
    },
    {
        "name": "Learnwithsumit",
        "api": "learnwithsumitapi.classx.co.in"
    },
    {
        "name": "Learnwithsweety",
        "api": "learnsweetyapi.classx.co.in"
    },
    {
        "name": "Learnwithvipul",
        "api": "learnwithvipulapi.classx.co.in"
    },
    {
        "name": "Leaverageconsultants",
        "api": "leverageconsultantsapi.classx.co.in"
    },
    {
        "name": "Legalpathshalabykaransangwan",
        "api": "legalpathshalakaransangwanapi.classx.co.in"
    },
    {
        "name": "Lernax",
        "api": "learnxapi.classx.co.in"
    },
    {
        "name": "Letsimprove",
        "api": "letsimproveapi.classx.co.in"
    },
    {
        "name": "Letslearn",
        "api": "letslearnappapi.classx.co.in"
    },
    {
        "name": "Letslearnwithajaysir",
        "api": "letslearnajaysirapi.classx.co.in"
    },
    {
        "name": "Levelup",
        "api": "levelupapi.classx.co.in"
    },
    {
        "name": "Levelupenglishwithramani",
        "api": "levelupenglishramaniapi.classx.co.in"
    },
    {
        "name": "Librsclasses",
        "api": "librsclassesapi.classx.co.in"
    },
    {
        "name": "Lifeguru",
        "api": "lifeguruapi.classx.co.in"
    },
    {
        "name": "Lifeskillsbyalmost",
        "api": "lifeskillsalmostapi.classx.co.in"
    },
    {
        "name": "Lifetimecourses",
        "api": "lifetimecoursesapi.classx.co.in"
    },
    {
        "name": "Lifexcareer",
        "api": "lifexcareerapi.classx.co.in"
    },
    {
        "name": "Linkinglaws",
        "api": "linkinglawsapi.classx.co.in"
    },
    {
        "name": "Liso",
        "api": "lisoclassesapi.classx.co.in"
    },
    {
        "name": "Listenup",
        "api": "listenupapi.classx.co.in"
    },
    {
        "name": "Littlecodershub",
        "api": "littlecodershubapi.classx.co.in"
    },
    {
        "name": "Livedoubts",
        "api": "livedoubtsapi.classx.co.in"
    },
    {
        "name": "Livereasoningbyshobhitsir",
        "api": "samarpanliveapi.classx.co.in"
    },
    {
        "name": "Lngeducation",
        "api": "lngeducationapi.classx.co.in"
    },
    {
        "name": "Logicalmindeducation",
        "api": "logicalmindapi.classx.co.in"
    },
    {
        "name": "Loginstudy",
        "api": "loginstudyapi.classx.co.in"
    },
    {
        "name": "Lokmanyaias",
        "api": "lokmanyaiasapi.classx.co.in"
    },
    {
        "name": "Loksevaacademypublicationbook",
        "api": "loksevaacademypublicationbookapi.classx.co.in"
    },
    {
        "name": "Lol",
        "api": "learnonlineapi.classx.co.in"
    },
    {
        "name": "Lovebabbar",
        "api": "lovebabarapi.classx.co.in"
    },
    {
        "name": "Ltrammanoharsinghintercollege",
        "api": "rammanoharsinghintercollegeapi.classx.co.in"
    },
    {
        "name": "Lucidacademy",
        "api": "lucidacademyapi.classx.co.in"
    },
    {
        "name": "Luckyenglish",
        "api": "luckyenglishapi.classx.co.in"
    },
    {
        "name": "Lvclasses",
        "api": "lvclassesapi.classx.co.in"
    },
    {
        "name": "Lvclasseslive",
        "api": "lvclassesapi.classx.co.in"
    },
    {
        "name": "Lvias",
        "api": "lviasapi.classx.co.in"
    },
    {
        "name": "Maarulaclasses",
        "api": "maarulaclassesapi.classx.co.in"
    },
    {
        "name": "Madhuramhindipro",
        "api": "madhuramhindiproapi.classx.co.in"
    },
    {
        "name": "Madhurikhedekar",
        "api": "madhurikhedekarapi.classx.co.in"
    },
    {
        "name": "Madlearning",
        "api": "madlearningapi.classx.co.in"
    },
    {
        "name": "Magadhsciencecoaching",
        "api": "magadhsciencecoachingapi.classx.co.in"
    },
    {
        "name": "Maggamworks",
        "api": "maggamworksapi.classx.co.in"
    },
    {
        "name": "Mahabharti",
        "api": "mahabhartiapi.classx.co.in"
    },
    {
        "name": "Mahajyotidnyanjyoti",
        "api": "mahajyotidnyanjyotiapi.classx.co.in"
    },
    {
        "name": "Maharanapratapacademypune",
        "api": "maharanapratapacademypuneapi.classx.co.in"
    },
    {
        "name": "Maharanapratapdefenceacademy",
        "api": "maharanapratapdefenceacademyapi.classx.co.in"
    },
    {
        "name": "Maharashtraacademy",
        "api": "maharashtraacademypuneapi.classx.co.in"
    },
    {
        "name": "Maharashtraayurvedaacademy",
        "api": "maharashtraayurvedaacademyapi.classx.co.in"
    },
    {
        "name": "Maharashtraprabodhini",
        "api": "maharashtraprabodhiniapi.classx.co.in"
    },
    {
        "name": "Maharshiacademy",
        "api": "maharshiacademyapi.classx.co.in"
    },
    {
        "name": "Mahateacher",
        "api": "mahateacherapi.classx.co.in"
    },
    {
        "name": "Mahatestmpsc",
        "api": "mahatestmpscapi.classx.co.in"
    },
    {
        "name": "Mahatmajieducator",
        "api": "mahatmajieducatorapi.classx.co.in"
    },
    {
        "name": "Mahatmajitechnical",
        "api": "mahatmajitechnicalapi.classx.co.in"
    },
    {
        "name": "Mahaveersanskrit",
        "api": "mahaveersanskritapi.classx.co.in"
    },
    {
        "name": "Mahavirpublisheranddistributors",
        "api": "mahavirpublisherdistributorsapi.classx.co.in"
    },
    {
        "name": "Maheshpatil",
        "api": "maheshpatilshashwatacademyapi.classx.co.in"
    },
    {
        "name": "Maheshramharichobe",
        "api": "maheshramharichobeapi.classx.co.in"
    },
    {
        "name": "Maheshstudies",
        "api": "maheshstudiesapi.classx.co.in"
    },
    {
        "name": "Mahiyapathsala",
        "api": "mahiyapathshalaapi.classx.co.in"
    },
    {
        "name": "Mahiyapathshalaschool",
        "api": "mahiyapathshalaschoolapi.classx.co.in"
    },
    {
        "name": "Maithilboy",
        "api": "maithilboyapi.classx.co.in"
    },
    {
        "name": "Maitreyaupscmpsc",
        "api": "maitreyaupscmpscapi.classx.co.in"
    },
    {
        "name": "Majesticacademy",
        "api": "majesticacademyapi.classx.co.in"
    },
    {
        "name": "Makecareer",
        "api": "makecareerapi.classx.co.in"
    },
    {
        "name": "Makeiasofficial",
        "api": "makeiasapi.classx.co.in"
    },
    {
        "name": "Makeiteasy",
        "api": "makeiteasyapi.classx.co.in"
    },
    {
        "name": "Makeiteasyskills",
        "api": "makeiteasyskillsapi.classx.co.in"
    },
    {
        "name": "Malikdefenseacademy",
        "api": "malikdefenseacademyapi.classx.co.in"
    },
    {
        "name": "Malindatech",
        "api": "malindatechapi.classx.co.in"
    },
    {
        "name": "Mallamcreations",
        "api": "mallamcreationsapi.classx.co.in"
    },
    {
        "name": "Malukaias",
        "api": "malukaiasapi.classx.co.in"
    },
    {
        "name": "Mamtatechnicalclasses",
        "api": "mamtatechnicalclassesapi.classx.co.in"
    },
    {
        "name": "Manaacademy",
        "api": "manaacademyapi.classx.co.in"
    },
    {
        "name": "Manapatashala",
        "api": "manapatashalaapi.classx.co.in"
    },
    {
        "name": "Manasacademy",
        "api": "manasacademyapi.classx.co.in"
    },
    {
        "name": "Manasurjaayurveda",
        "api": "manasurjaayurvedaapi.classx.co.in"
    },
    {
        "name": "Manekshawofficersacademy",
        "api": "manekshawofficersacademyapi.classx.co.in"
    },
    {
        "name": "Mangaranilessons",
        "api": "kmangaranilessonsapi.classx.co.in"
    },
    {
        "name": "Mangilalchoudharysir",
        "api": "mangilalchoudharysirapi.classx.co.in"
    },
    {
        "name": "Manishacademylive",
        "api": "manishacademyliveapi.classx.co.in"
    },
    {
        "name": "Manishvermaclasses",
        "api": "manishvermaclassesapi.classx.co.in"
    },
    {
        "name": "Manojacademy",
        "api": "manojacademyapi.classx.co.in"
    },
    {
        "name": "Manojstudycentre",
        "api": "manojstudycentreapi.classx.co.in"
    },
    {
        "name": "Mansimahilaaudyogikutpadak",
        "api": "mansimahilaaudyogikutpadaksahakarisocietyldtapi.classx.co.in"
    },
    {
        "name": "Marathuvyakaran",
        "api": "marathivyakarnapi.classx.co.in"
    },
    {
        "name": "Margdarshanpathshala",
        "api": "margdarshanpathshalaapi.classx.co.in"
    },
    {
        "name": "Marshalcareeracademy",
        "api": "marshalcareeracademyapi.classx.co.in"
    },
    {
        "name": "Maryadaqualityeducation",
        "api": "maryadaqualityeducationapi.classx.co.in"
    },
    {
        "name": "Masterclassesiaspcs",
        "api": "masterclassesiaspcsapi.classx.co.in"
    },
    {
        "name": "Masterji",
        "api": "masterjiapi.classx.co.in"
    },
    {
        "name": "Mastermindsforcaandcma",
        "api": "mastermindsforcaandcmaapi.classx.co.in"
    },
    {
        "name": "Mastersahab",
        "api": "mastersahabapi.classx.co.in"
    },
    {
        "name": "Mathematicsstarclasses",
        "api": "mathematicsstarclassesapi.classx.co.in"
    },
    {
        "name": "Mathematicswithvishalkumar",
        "api": "mathematicsvishalkumarapi.classx.co.in"
    },
    {
        "name": "Mathreasoningbykadamsir",
        "api": "mathreasoningkadamsirapi.classx.co.in"
    },
    {
        "name": "Mathsbazaar",
        "api": "mathsbazaarapi.classx.co.in"
    },
    {
        "name": "Mathsbymrksir",
        "api": "mathsmrksirapi.classx.co.in"
    },
    {
        "name": "Mathsbynitinsir",
        "api": "mathsnitinsirapi.classx.co.in"
    },
    {
        "name": "Mathscare",
        "api": "mathscareapi.classx.co.in"
    },
    {
        "name": "Mathscaredigital",
        "api": "mathscaredigitalapi.classx.co.in"
    },
    {
        "name": "Mathsfied",
        "api": "mathsfiedapi.classx.co.in"
    },
    {
        "name": "Mathsguru",
        "api": "mathsguruapi.classx.co.in"
    },
    {
        "name": "Mathsimpact",
        "api": "mathsimpactapi.classx.co.in"
    },
    {
        "name": "Mathsjugadsemjs",
        "api": "mathsjugadapi.classx.co.in"
    },
    {
        "name": "Mathskiduniyavivekchoudhary",
        "api": "mathskiduniyavivekchoudharyapi.classx.co.in"
    },
    {
        "name": "Mathsmantra",
        "api": "mathsmantraapi.classx.co.in"
    },
    {
        "name": "Mathsmastibyvipinsir",
        "api": "mathsmastivipinsirapi.classx.co.in"
    },
    {
        "name": "Mathsmirror",
        "api": "mathsmirrorapi.classx.co.in"
    },
    {
        "name": "Mathsmrinmoysir",
        "api": "mathsmrinmoysirapi.classx.co"
    },
    {
        "name": "Mathsphobia",
        "api": "mathsphobiaapi.classx.co.in"
    },
    {
        "name": "Mathsvalaashishkumar",
        "api": "mathsvalaashishkumarapi.classx.co.in"
    },
    {
        "name": "Mathsvatika20",
        "api": "mathsvatikaappapi.classx.co.in"
    },
    {
        "name": "Mathswalamaster",
        "api": "mathswalamasterapi.classx.co.in"
    },
    {
        "name": "Mathswithgajanand",
        "api": "mathsgajanandapi.classx.co.in"
    },
    {
        "name": "Mathswithmrinmoysir",
        "api": "mathsmrinmoysirapi.classx.co.in"
    },
    {
        "name": "Mathswithvivek",
        "api": "mathsvivekapi.classx.co.in"
    },
    {
        "name": "Mathwithpraveenbajpai",
        "api": "mathpraveenbajpaiapi.classx.co.in"
    },
    {
        "name": "Matsciodia",
        "api": "matsciodiaapi.classx.co.in"
    },
    {
        "name": "Maviacademy",
        "api": "maviacademyapi.classx.co.in"
    },
    {
        "name": "Mawanaclasses",
        "api": "mawanaclassesapi.classx.co.in"
    },
    {
        "name": "Maxenglishpoint",
        "api": "maxenglishpointapi.classx.co.in"
    },
    {
        "name": "Mayastheschoolofbeauty",
        "api": "mayasschoolbeautyapi.classx.co.in"
    },
    {
        "name": "Mayboliprabodhinipune",
        "api": "mayboliprabodhiniapi.classx.co.in"
    },
    {
        "name": "Mbnbyneerajkukreja",
        "api": "mbnbyneerajkukrejaapi.classx.co.in"
    },
    {
        "name": "Mcmaworldofengineering",
        "api": "mcmaworldengineeringapi.classx.co.in"
    },
    {
        "name": "Mcmpatna",
        "api": "mcmpatnaapi.classx.co.in"
    },
    {
        "name": "Mcsiasmissioncivilservices",
        "api": "mcsiasapi.classx.co.in"
    },
    {
        "name": "Md",
        "api": "mdclassesapi.appx.co.in"
    },
    {
        "name": "Mdclasses",
        "api": "mdclassesapi.classx.co.in"
    },
    {
        "name": "Mdsir",
        "api": "mdsirapi.classx.co.in"
    },
    {
        "name": "Medicalandnurseshub",
        "api": "medicalnurseshubapi.classx.co.in"
    },
    {
        "name": "Medicalpathshala",
        "api": "medicalpathshalaapi.classx.co.in"
    },
    {
        "name": "Medinotes",
        "api": "medinotesapi.classx.co.in"
    },
    {
        "name": "Medsynapse",
        "api": "medsynapseapi.classx.co.in"
    },
    {
        "name": "Mehtaclasses",
        "api": "mehraclassesapi.classx.co.in"
    },
    {
        "name": "Mendesuresh",
        "api": "mendesureshapi.classx.co.in"
    },
    {
        "name": "Mentor365",
        "api": "mentor365api.classx.co.in"
    },
    {
        "name": "Mentormee",
        "api": "mentormeeapi.classx.co.in"
    },
    {
        "name": "Mentormeein",
        "api": "mentormeeinapi.classx.co.in"
    },
    {
        "name": "Mentorseduserve",
        "api": "mentorseduserveapi.classx.co.in"
    },
    {
        "name": "Menttifyin",
        "api": "menttifyinapi.classx.co.in"
    },
    {
        "name": "Meomadeeasy",
        "api": "meomadeeasyapi.classx.co.in"
    },
    {
        "name": "Meramentor",
        "api": "meramentorapi.classx.co.in"
    },
    {
        "name": "Meritova",
        "api": "meritovaapi.classx.co.in"
    },
    {
        "name": "Mgacademy",
        "api": "mgacademyapi.classx.co.in"
    },
    {
        "name": "Mgclasses",
        "api": "mgclassesapi.classx.co.in"
    },
    {
        "name": "Mgcollegemahwadausa",
        "api": "mgcollegemahwadausaapi.classx.co.in"
    },
    {
        "name": "Mgconcept",
        "api": "mgconceptapi.classx.co.in"
    },
    {
        "name": "Mgics",
        "api": "mgicsappapi.classx.co.in"
    },
    {
        "name": "Mgieducation",
        "api": "mgieducationapi.classx.co.in"
    },
    {
        "name": "Mgumangstudy",
        "api": "mgumangstudyapi.classx.co.in"
    },
    {
        "name": "Mheducationlab",
        "api": "mheducationlabapi.classx.co.in"
    },
    {
        "name": "Mheducationlablite",
        "api": "mheducationlabliteapi.classx.co.in"
    },
    {
        "name": "Mias",
        "api": "miasappapi.classx.co.in"
    },
    {
        "name": "Militaryjawan",
        "api": "militaryjawanapi.classx.co.in"
    },
    {
        "name": "Mindacademy",
        "api": "mindacademyapi.classx.co.in"
    },
    {
        "name": "Mindexam",
        "api": "mindexamapi.classx.co.in"
    },
    {
        "name": "Mindmentors",
        "api": "mindmentorsapi.classx.co.in"
    },
    {
        "name": "Mindsetfitness",
        "api": "mindsetfitnessapi.classx.co.in"
    },
    {
        "name": "Mindyourmathbykona",
        "api": "mindyourmathbykonaapi.classx.co.in"
    },
    {
        "name": "Minilibrary",
        "api": "minilibraryapi.classx.co.in"
    },
    {
        "name": "Mishthiclassesjaipur",
        "api": "mishthiclassesjaipurapi.classx.co.in"
    },
    {
        "name": "Mission",
        "api": "missionapi.appx.co.in"
    },
    {
        "name": "Mission",
        "api": "missionapi.classx.co.in"
    },
    {
        "name": "Missionbadlav",
        "api": "missionbadlavapi.classx.co.in"
    },
    {
        "name": "Missiondreameducation",
        "api": "missiondreameducationapi.classx.co.in"
    },
    {
        "name": "Missionhigh",
        "api": "missionhighapi.classx.co.in"
    },
    {
        "name": "Missionkhakionlinelearningapp",
        "api": "missionkhakiapi.classx.co.in"
    },
    {
        "name": "Mitexa",
        "api": "mitexaapi.classx.co.in"
    },
    {
        "name": "Mjshaikhsenglishacademy",
        "api": "mjshaikhsenglishacademyapi.classx.co.in"
    },
    {
        "name": "Mkeducare",
        "api": "mkeducareapi.classx.co.in"
    },
    {
        "name": "Mkgyankendra",
        "api": "mkgyankendraapi.classx.co.in"
    },
    {
        "name": "Mkmadhavmaths",
        "api": "mkmadhavmathsapi.classx.co.in"
    },
    {
        "name": "Mkphysicsclasses",
        "api": "mkphysicsclassesapi.classx.co.in"
    },
    {
        "name": "Mksir",
        "api": "mksirapi.classx.co.in"
    },
    {
        "name": "Mme",
        "api": "missionmillionenglishapi.classx.co.in"
    },
    {
        "name": "Mobileparschool",
        "api": "mobileparschoolapi.classx.co.in"
    },
    {
        "name": "Mobishiksha",
        "api": "mobishikshaapi.classx.co.in"
    },
    {
        "name": "Mockopedia",
        "api": "mockopediaapi.classx.co.in"
    },
    {
        "name": "Mocksadda",
        "api": "mocksaddaapi.classx.co.in"
    },
    {
        "name": "Mocksguru",
        "api": "mocksguruapi.classx.co.in"
    },
    {
        "name": "Modelmaths",
        "api": "modelmathsapi.classx.co.in"
    },
    {
        "name": "Modulationdigital",
        "api": "modulationdigitalapi.classx.co.in"
    },
    {
        "name": "Mohandrivezone",
        "api": "mohandrivezoneapi.classx.co.in"
    },
    {
        "name": "Moneyfundas",
        "api": "moneyfundasapi.classx.co.in"
    },
    {
        "name": "Mpscbyeknathpatiltatya",
        "api": "mpscbyeknathpatiltatyaapi.classx.co.in"
    },
    {
        "name": "Mpscguru",
        "api": "mpscguruapi.classx.co.in"
    },
    {
        "name": "Mpsclakshya",
        "api": "mpsclakshyaapi.classx.co.in"
    },
    {
        "name": "Mpscmadesimple",
        "api": "mpscmadesimpleapi.classx.co.in"
    },
    {
        "name": "Mpscmaza",
        "api": "mpscmazaapi.classx.co.in"
    },
    {
        "name": "Mpscmentor",
        "api": "mpscmentorapi.classx.co.in"
    },
    {
        "name": "Mpscpocketapp",
        "api": "mpscpocketappapi.classx.co.in"
    },
    {
        "name": "Mpscstudypoint",
        "api": "mpscstudypointapi.classx.co.in"
    },
    {
        "name": "Mrcompetitiveeasylearning",
        "api": "mrcompetitiveeasylearningapi.classx.co.in"
    },
    {
        "name": "Mreducare",
        "api": "mreducareapi.classx.co.in"
    },
    {
        "name": "Msaclasses",
        "api": "msaclassesapi.classx.co.in"
    },
    {
        "name": "Mschool",
        "api": "mschoolapi.classx.co.in"
    },
    {
        "name": "Msclasses",
        "api": "msclassesapi.classx.co.in"
    },
    {
        "name": "Mseducations",
        "api": "mseducationsapi.classx.co.in"
    },
    {
        "name": "Msgurustudy",
        "api": "msgurustudyapi.classx.co.in"
    },
    {
        "name": "Mssscnotes",
        "api": "mseducationapi.classx.co.in"
    },
    {
        "name": "Mssuccess",
        "api": "mssuccessapi.classx.co.in"
    },
    {
        "name": "Mtphysicsclasses",
        "api": "mtphysicsclassesapi.classx.co.in"
    },
    {
        "name": "Muditguptaupscprepplatform",
        "api": "muditguptaprepplatformapi.classx.co.in"
    },
    {
        "name": "Mukeshpancholiacharyaclasses",
        "api": "acharyaclassesapi.classx.co.in"
    },
    {
        "name": "Mukulagrawal",
        "api": "mukulagrawalapi.classx.co.in"
    },
    {
        "name": "Murthysenglish",
        "api": "murthyenglishapi.classx.co.in"
    },
    {
        "name": "Mvrsuccess",
        "api": "mvrsuccessapi.classx.co.in"
    },
    {
        "name": "Mybizkid",
        "api": "mybizkidapi.classx.co.in"
    },
    {
        "name": "Myclass",
        "api": "myclassapi.classx.co.in"
    },
    {
        "name": "Mycoachingofficialapp",
        "api": "mycoachingofficialappapi.classx.co.in"
    },
    {
        "name": "Myenglishiqacademy",
        "api": "myenglishiqacademyapi.classx.co.in"
    },
    {
        "name": "Myexam",
        "api": "myexamappapi.classx.co.in"
    },
    {
        "name": "Myexamdiary",
        "api": "myexamdiaryapi.classx.co.in"
    },
    {
        "name": "Mymentor",
        "api": "mymentorappapi.classx.co.in"
    },
    {
        "name": "Mynotes",
        "api": "mynotesapi.classx.co.in"
    },
    {
        "name": "Mysaksham",
        "api": "mysakshamapi.classx.co.in"
    },
    {
        "name": "Myschool",
        "api": "myschoolapi.classx.co.in"
    },
    {
        "name": "Mytestlibrary",
        "api": "mytestlibraryapi.classx.co.in"
    },
    {
        "name": "Myupscclass",
        "api": "myupscclassapi.classx.co.in"
    },
    {
        "name": "Myvidyarthi",
        "api": "myvidyarthiapi.classx.co.in"
    },
    {
        "name": "Naiduexamwarriors",
        "api": "naiduexamwarriorsapi.classx.co.in"
    },
    {
        "name": "Naiyapaareducation",
        "api": "naiyapaareducationapi.classx.co.in"
    },
    {
        "name": "Nalandaclasses",
        "api": "nalandaclassesapi.classx.co.in"
    },
    {
        "name": "Nallurirajeshsirclasses",
        "api": "nallurirajeshsirclassesapi.classx.co.in"
    },
    {
        "name": "Namanneducation",
        "api": "namanneducationapi.classx.co.in"
    },
    {
        "name": "Namansirmaths",
        "api": "namansirmathsapi.classx.co.in"
    },
    {
        "name": "Namastelearning",
        "api": "namastelearningapi.classx.co.in"
    },
    {
        "name": "Namasteneetjee",
        "api": "namasteneetjeeapi.classx.co.in"
    },
    {
        "name": "Namastesql",
        "api": "namastesqlapi.classx.co.in"
    },
    {
        "name": "Namisha",
        "api": "nimishabansalapi.appx.co.in"
    },
    {
        "name": "Namoabcacademy",
        "api": "namoabcacademyapi.classx.co.in"
    },
    {
        "name": "Nannampoleclimbing",
        "api": "nannampoleclimbingapi.classx.co.in"
    },
    {
        "name": "Narayanansirstudycircles",
        "api": "narayanansirstudycirclesapi.classx.co.in"
    },
    {
        "name": "Narendrasirsacademy",
        "api": "narendrasiracademyapi.classx.co.in"
    },
    {
        "name": "Nareshonlineacademy",
        "api": "nareshonlineacademyapi.classx.co.in"
    },
    {
        "name": "Nathpublication",
        "api": "nathpublicationapi.classx.co.in"
    },
    {
        "name": "Natrajeducation",
        "api": "natrajeducationapi.classx.co.in"
    },
    {
        "name": "Naukriaspirants",
        "api": "naukriaspirantsapi.classx.co.in"
    },
    {
        "name": "Naukrijunction",
        "api": "naukrijunctionapi.classx.co.in"
    },
    {
        "name": "Naveenreddymath",
        "api": "naveenreddymathapi.classx.co.in"
    },
    {
        "name": "Naveentanwaracademy",
        "api": "naveentanwaracademyapi.classx.co.in"
    },
    {
        "name": "Navjeevanonlinecampus",
        "api": "navjeevanonlinecampusapi.classx.co.in"
    },
    {
        "name": "Navtutor",
        "api": "navtutorapi.classx.co.in"
    },
    {
        "name": "Navyugstudyforum",
        "api": "navyugstudyforumapi.classx.co.in"
    },
    {
        "name": "Nawala",
        "api": "nawalaapi.classx.co.in"
    },
    {
        "name": "Nayanclasses20",
        "api": "nayanclassesapi.classx.co.in"
    },
    {
        "name": "Ndcampusthelearningapp",
        "api": "ndcampuslearningapi.classx.co.in"
    },
    {
        "name": "Neelamnaidustudycircle",
        "api": "neelamnaidustudycircleapi.classx.co.in"
    },
    {
        "name": "Neerajsharmaenglishnew",
        "api": "neerajsharmaenglishapi.classx.co.in"
    },
    {
        "name": "Neerajsharmaenglishold",
        "api": "sharmasapi.classx.co.in"
    },
    {
        "name": "Neeteasy",
        "api": "neeteasyapi.classx.co.in"
    },
    {
        "name": "Neetkakajee",
        "api": "neetkakajeeapi.classx.co.in"
    },
    {
        "name": "Neetpathshala",
        "api": "neetpathshalaapi.classx.co.in"
    },
    {
        "name": "Neetshastraneetcounselling",
        "api": "neetshastraneetcounsellingapi.classx.co.in"
    },
    {
        "name": "Neocollege",
        "api": "neocollegeapi.classx.co.in"
    },
    {
        "name": "Neospark",
        "api": "neosparkapi.classx.co.in"
    },
    {
        "name": "Newatulyaacademy",
        "api": "newatulyaacademyapi.classx.co.in"
    },
    {
        "name": "Newlightclasses",
        "api": "newlightclassesapi.classx.co.in"
    },
    {
        "name": "Newutkarshiaspcscoaching",
        "api": "newutkarshcoachingapi.classx.co.in"
    },
    {
        "name": "Nexteducation",
        "api": "nexteducationapi.classx.co.in"
    },
    {
        "name": "Nglearner",
        "api": "nglearnersapi.classx.co.in"
    },
    {
        "name": "Nglearner",
        "api": "nglearnersapi.classx.co.in"
    },
    {
        "name": "Nhmiracleacademy",
        "api": "nhmiracleacademyapi.classx.co.in"
    },
    {
        "name": "Niceacademyhaveri",
        "api": "niceacademyhaveriapi.classx.co.in"
    },
    {
        "name": "Nicevidyapeeth",
        "api": "nicevidyapeethapi.classx.co.in"
    },
    {
        "name": "Nileshclasses",
        "api": "nileshclassesapi.classx.co.in"
    },
    {
        "name": "Nirakt",
        "api": "niraktapi.classx.co.in"
    },
    {
        "name": "Nirdeshiasclasses",
        "api": "nirdeshiasclassesapi.classx.co.in"
    },
    {
        "name": "Nirmanias",
        "api": "nirmaniasapi.classx.co.in"
    },
    {
        "name": "Niseeducationhub",
        "api": "niseeducationhubapi.classx.co.in"
    },
    {
        "name": "Nishanteacademyeducation",
        "api": "nishanteacademyeducationapi.classx.co.in"
    },
    {
        "name": "Nishantsenglish",
        "api": "nishantsenglishapi.classx.co.in"
    },
    {
        "name": "Nishchayacademy",
        "api": "nishchayacademyapi.classx.co.in"
    },
    {
        "name": "Nishchayiasacademy",
        "api": "nishchayiasacademyapi.classx.co.in"
    },
    {
        "name": "Nishtha",
        "api": "nishthaapi.classx.co.in"
    },
    {
        "name": "Nishthainstitute",
        "api": "nishthainstituteapi.classx.co.in"
    },
    {
        "name": "Niteshsir",
        "api": "niteshsirapi.classx.co.in"
    },
    {
        "name": "Nitinsharmamaths",
        "api": "nitinsharmamathsapi.classx.co.in"
    },
    {
        "name": "Nobelforensics",
        "api": "nobelforensicsapi.classx.co.in"
    },
    {
        "name": "Notebook",
        "api": "notebookapi.classx.co.in"
    },
    {
        "name": "Notebookacademy",
        "api": "d1ftpn76h259sr.cloudfront.net"
    },
    {
        "name": "Nscareeracademy",
        "api": "nscareeracademyapi.classx.co.in"
    },
    {
        "name": "Nskp",
        "api": "nskpapi.classx.co.in"
    },
    {
        "name": "Nst",
        "api": "nstapi.classx.co.in"
    },
    {
        "name": "Numbersacademy",
        "api": "numbersacademyapi.classx.co.in"
    },
    {
        "name": "Nurseasy",
        "api": "nurseasyapi.classx.co.in"
    },
    {
        "name": "Nursingtest",
        "api": "nursingtestapi.classx.co.in"
    },
    {
        "name": "Nurtureclassesjeeneetboard",
        "api": "nurtureclassesapi.classx.co.in"
    },
    {
        "name": "Ocean",
        "api": "oceangurukulsapi.classx.co.in"
    },
    {
        "name": "Odiaspacegovtexampreparationapp",
        "api": "odiaspaceapi.classx.co.in"
    },
    {
        "name": "Odinsacademy",
        "api": "odinsacademyapi.classx.co.in"
    },
    {
        "name": "Odishaexam",
        "api": "odishaexamapi.classx.co.in"
    },
    {
        "name": "Odishaexamnew",
        "api": "newodishaexamapi.classx.co.in"
    },
    {
        "name": "Olympiadwinner",
        "api": "olympiadwinnerapi.classx.co.in"
    },
    {
        "name": "Olympicstudy",
        "api": "olympicstudyapi.classx.co.in"
    },
    {
        "name": "Omeducation",
        "api": "omeducationapi.classx.co.in"
    },
    {
        "name": "Omtrivediclassesotc",
        "api": "omtrivediclassesapi.classx.co.in"
    },
    {
        "name": "Omvisionacademy",
        "api": "omvisionacademyapi.classx.co.in"
    },
    {
        "name": "Onedayghar",
        "api": "onedaygharapi.classx.co.in"
    },
    {
        "name": "Onekstudy",
        "api": "onekstudyapi.classx.co.in"
    },
    {
        "name": "Onlineagriculture",
        "api": "onlineagricultureapi.classx.co.in"
    },
    {
        "name": "Onlineclassacademy",
        "api": "onlineclassacademyapi.classx.co.in"
    },
    {
        "name": "Onlineeducationapp",
        "api": "onlineeducationapi.classx.co.in"
    },
    {
        "name": "Onlinelearning",
        "api": "onlinelearningapi.classx.co.in"
    },
    {
        "name": "Onlineolearnonline",
        "api": "onlineolearnonlineanytimeapi.classx.co.in"
    },
    {
        "name": "Onlineprep",
        "api": "onlineprepapi.classx.co.in"
    },
    {
        "name": "Onlinestudyplatform",
        "api": "onlinestudyplatformapi.classx.co.in"
    },
    {
        "name": "Onlinestudypoint",
        "api": "onlinestudypointapi.classx.co.in"
    },
    {
        "name": "Onlinestudyzone",
        "api": "onlinestudyzoneapi.classx.co.in"
    },
    {
        "name": "Onlinetestbook",
        "api": "onlinetestbookapi.classx.co.in"
    },
    {
        "name": "Onlykhakimission",
        "api": "onlykhakimissionapi.classx.co.in"
    },
    {
        "name": "Onlystudy",
        "api": "onlystudyapi.classx.co.in"
    },
    {
        "name": "Onlytopstudy",
        "api": "onlytopstudyapi.classx.co.in"
    },
    {
        "name": "Ooacademypune",
        "api": "ooacademypuneapi.classx.co.in"
    },
    {
        "name": "Openstudy",
        "api": "openstudyapi.teachx.in"
    },
    {
        "name": "Openstudy",
        "api": "openstudyapi.classx.co.in"
    },
    {
        "name": "Optimum",
        "api": "optimumapi.classx.co.in"
    },
    {
        "name": "Oraontvjh",
        "api": "oraontvjhapi.classx.co.in"
    },
    {
        "name": "Orjaat",
        "api": "orjaatapi.classx.co.in"
    },
    {
        "name": "Osnacademy",
        "api": "osnacademyapi.classx.co.in"
    },
    {
        "name": "Ourdreammerry",
        "api": "ourdreammerryapi.classx.co.in"
    },
    {
        "name": "Ourseducation",
        "api": "ourseducationapi.classx.co.in"
    },
    {
        "name": "Ovimet",
        "api": "ovimetapi.classx.co.in"
    },
    {
        "name": "Oxfordgsaacademyjaipur",
        "api": "oxfordgsaacademyjaipurapi.classx.co.in"
    },
    {
        "name": "Pacificmarineacademy",
        "api": "pacificmarineacademyapi.classx.co.in"
    },
    {
        "name": "Padhle",
        "api": "padhleapi.classx.co.in"
    },
    {
        "name": "Padhleakshay",
        "api": "padhleakshayapi.classx.co.in"
    },
    {
        "name": "Padhoabhiyan",
        "api": "padhoabhiyanapi.classx.co.in"
    },
    {
        "name": "Padhreclasses",
        "api": "padhreclassesapi.classx.co.in"
    },
    {
        "name": "Padhreiitjam",
        "api": "padhreiitjamapi.classx.co.in"
    },
    {
        "name": "Pahelieduplus",
        "api": "pahelieduplusapi.classx.co.in"
    },
    {
        "name": "Paidefenceacademy",
        "api": "paidefenceacademyapi.classx.co.in"
    },
    {
        "name": "Palakiasacademy",
        "api": "palakiasacademyapi.classx.co.in"
    },
    {
        "name": "Panaceaforssc",
        "api": "panaceaforsscapi.classx.co.in"
    },
    {
        "name": "Pancholi",
        "api": "acharyaclassesapi.appx.co.in"
    },
    {
        "name": "Panchrishiclasses",
        "api": "panchrishiclassesapi.classx.co.in"
    },
    {
        "name": "Pandeyjitechnical",
        "api": "pandeyjitechnicalapi.classx.co.in"
    },
    {
        "name": "Pankajstudycentre",
        "api": "pankajstudycentreapi.classx.co.in"
    },
    {
        "name": "Panoramabykamleshsir",
        "api": "panoramakamleshsirapi.classx.co.in"
    },
    {
        "name": "Pantheonedu",
        "api": "pantheoneduapi.classx.co.in"
    },
    {
        "name": "Paperhacker",
        "api": "paperhackerapi.classx.co.in"
    },
    {
        "name": "Papertickacademy",
        "api": "papertickacademyapi.classx.co.in"
    },
    {
        "name": "Parakramacademy",
        "api": "parakramacademyapi.classx.co.in"
    },
    {
        "name": "Paramedicalclasses",
        "api": "paramedicalclassesapi.classx.co.in"
    },
    {
        "name": "Pareeksharthi",
        "api": "pareeksharthiapi.classx.co.in"
    },
    {
        "name": "Pariksha247",
        "api": "pariksha247api.classx.co.in"
    },
    {
        "name": "Parikshadham",
        "api": "parikshadhamapi.classx.co.in"
    },
    {
        "name": "Parikshagyan",
        "api": "parikshagyanapi.classx.co.in"
    },
    {
        "name": "Parikshamunch",
        "api": "parikshamunchapi.classx.co.in"
    },
    {
        "name": "Parikshaone",
        "api": "parikshaoneapi.classx.co.in"
    },
    {
        "name": "Parikshaplus",
        "api": "parikshaplusapi.classx.co.in"
    },
    {
        "name": "Parikshaportal",
        "api": "parikshaportalapi.classx.co.in"
    },
    {
        "name": "Parishramupscgpsc",
        "api": "parishramupscgpscapi.classx.co.in"
    },
    {
        "name": "Pariskhastudy24",
        "api": "pariskhastudy24api.classx.co.in"
    },
    {
        "name": "Parivartanmpscupsc",
        "api": "parivartanmpscupscapi.classx.co.in"
    },
    {
        "name": "Parmaracademy",
        "api": "parmaracademyapi.classx.co.in"
    },
    {
        "name": "Pashaseconomy20",
        "api": "pashaseconomy20api.classx.co.in"
    },
    {
        "name": "Passionenglishstudy",
        "api": "passionenglishstudyapi.classx.co.in"
    },
    {
        "name": "Patanjaliiasacademy",
        "api": "patanjaliiasacademyapi.classx.co.in"
    },
    {
        "name": "Pathakclasses",
        "api": "pathakclassesapi.classx.co.in"
    },
    {
        "name": "Pathshala247Examprep",
        "api": "pathshala247examprepapi.classx.co.in"
    },
    {
        "name": "Patiya",
        "api": "patiyaapi.classx.co.in"
    },
    {
        "name": "Pavandeshpandesacademy",
        "api": "pavandeshpandeacademyapi.classx.co.in"
    },
    {
        "name": "Pawansirbettiah",
        "api": "pawansirbettiahapi.classx.co.in"
    },
    {
        "name": "Pcdigital",
        "api": "pcdigitalapi.classx.co.in"
    },
    {
        "name": "Pcepanacea",
        "api": "panaceacompetitiveexaminationsapi.classx.co.in"
    },
    {
        "name": "Pcmbacademy",
        "api": "pcmbacademyapi.classx.co.in"
    },
    {
        "name": "Pcsmantra",
        "api": "pcsmantraapi.teachx.in"
    },
    {
        "name": "Pcsmantra",
        "api": "pcsmantraapi.classx.co.in"
    },
    {
        "name": "Pdsharmaclasses",
        "api": "pdsharmaclassesapi.classx.co.in"
    },
    {
        "name": "Pearlnirmaanclassespnc",
        "api": "pearlnirmaanclassesapi.classx.co.in"
    },
    {
        "name": "Pediatricsbydranand",
        "api": "pediatricsdranandapi.classx.co.in"
    },
    {
        "name": "Perainstitutepune",
        "api": "perainstitutepuneapi.classx.co.in"
    },
    {
        "name": "Perfectcomputerengineer",
        "api": "perfectcomputerengineerapi.classx.co.in"
    },
    {
        "name": "Perfectioniasacademy",
        "api": "perfectioniasacademyapi.classx.co.in"
    },
    {
        "name": "Perfectswing",
        "api": "perfectswingapi.classx.co.in"
    },
    {
        "name": "Perspectiveacademy",
        "api": "perspectiveacademyapi.classx.co.in"
    },
    {
        "name": "Pesphankareducationservices",
        "api": "pesphankareducationservicesapi.classx.co.in"
    },
    {
        "name": "Pgcambd",
        "api": "pgcambdapi.classx.co.in"
    },
    {
        "name": "Pgpointlive",
        "api": "pgpointliveapi.classx.co.in"
    },
    {
        "name": "Pharmacadgpatnipermba",
        "api": "pharmacadapi.classx.co.in"
    },
    {
        "name": "Pharmacyindia",
        "api": "pharmacyindiaapi.classx.co.in"
    },
    {
        "name": "Pharmacypoint",
        "api": "pharmacypointapi.classx.co.in"
    },
    {
        "name": "Phoenixacademy",
        "api": "phoenixacademyapi.classx.co.in"
    },
    {
        "name": "Phonefixhyd",
        "api": "phonefixhydapi.classx.co.in"
    },
    {
        "name": "Phonixacadmy",
        "api": "studypiapi.appx.co.in"
    },
    {
        "name": "Photonclasses",
        "api": "photonclassesapi.classx.co.in"
    },
    {
        "name": "Physicasingh",
        "api": "physicsasinghsirapi.classx.co.in"
    },
    {
        "name": "Physicsbyniteshsir",
        "api": "physicsniteshsirapi.classx.co.in"
    },
    {
        "name": "Physicsbypankajsir",
        "api": "physicspankajsirapi.classx.co.in"
    },
    {
        "name": "Physicsbysanjaysir",
        "api": "physicssanjaysirapi.classx.co.in"
    },
    {
        "name": "Physicsbyshubhamtyagi",
        "api": "physicsshubhamtyagiapi.classx.co.in"
    },
    {
        "name": "Physicsfakira",
        "api": "physicsfakiraapi.classx.co.in"
    },
    {
        "name": "Physicsgravity",
        "api": "physicsgravityapi.classx.co.in"
    },
    {
        "name": "Physicsguru",
        "api": "physicsguruapi.classx.co.in"
    },
    {
        "name": "Physicsheistbyprofessor",
        "api": "physicsheistprofessorapi.classx.co.in"
    },
    {
        "name": "Physicsmagician",
        "api": "physicsmagicianapi.classx.co.in"
    },
    {
        "name": "Physicsmagicianweb",
        "api": "physicsmagicianwebapi.classx.co.in"
    },
    {
        "name": "Physicsprobyaksir",
        "api": "physicsproaksirapi.classx.co.in"
    },
    {
        "name": "Physicstour",
        "api": "physicstourapi.classx.co.in"
    },
    {
        "name": "Physicswithumeshrajoria",
        "api": "physicsumeshrajoriaapi.classx.co.in"
    },
    {
        "name": "Pioneeracademy",
        "api": "pioneeracademyapi.classx.co.in"
    },
    {
        "name": "Pkagriacademy",
        "api": "pkagriacademyapi.classx.co.in"
    },
    {
        "name": "Pksirmaths",
        "api": "pksirmathsapi.classx.co.in"
    },
    {
        "name": "Plaintospeak",
        "api": "plaintospeakapi.classx.co.in"
    },
    {
        "name": "Planetspike",
        "api": "planetspikeapi.classx.co.in"
    },
    {
        "name": "Platform",
        "api": "d2zv7casldjvbj.cloudfront.net"
    },
    {
        "name": "Pnextlive",
        "api": "pnextliveapi.classx.co.in"
    },
    {
        "name": "Policefactory",
        "api": "policefactoryapi.classx.co.in"
    },
    {
        "name": "Polytechnicacademy",
        "api": "polytechnicacademyapi.classx.co.in"
    },
    {
        "name": "Polytechnicpathshala",
        "api": "polytechnicpathshalaapi.classx.co.in"
    },
    {
        "name": "Powerofprotrading",
        "api": "powerofprotradingapi.classx.co.in"
    },
    {
        "name": "Powl",
        "api": "powlapi.classx.co.in"
    },
    {
        "name": "Prabalprofessionalacademy",
        "api": "prabalprofessionalacademyapi.classx.co.in"
    },
    {
        "name": "Prabhav",
        "api": "prabhavapi.classx.co.in"
    },
    {
        "name": "Prabodhfoundation",
        "api": "prabodhfoundationapi.classx.co.in"
    },
    {
        "name": "Pracademy",
        "api": "pracademyapi.classx.co.in"
    },
    {
        "name": "Prachandprayaspvtltd",
        "api": "prachandprayaspvtltdapi.classx.co.in"
    },
    {
        "name": "Practicebook",
        "api": "practicebookapi.classx.co.in"
    },
    {
        "name": "Pradeepgirisir",
        "api": "pradeepgiriapi.classx.co.in"
    },
    {
        "name": "Pradeepkagat",
        "api": "pradeepkagatapi.classx.co.in"
    },
    {
        "name": "Pradhitclassesliveclassespdf",
        "api": "pradhitclassesliveclassespdfapi.classx.co.in"
    },
    {
        "name": "Pragaticlassesudaipur",
        "api": "pragaticlassesudaipurapi.classx.co.in"
    },
    {
        "name": "Pragaticoaching",
        "api": "pragaticoachingapi.classx.co.in"
    },
    {
        "name": "Pragyaeducation",
        "api": "pragyaeducationapi.classx.co.in"
    },
    {
        "name": "Prajadefence",
        "api": "prajadefenceapi.classx.co.in"
    },
    {
        "name": "Prakashinstitute",
        "api": "prakashinstituteapi.classx.co.in"
    },
    {
        "name": "Prakashsirmaths",
        "api": "prakashsirmathsapi.classx.co.in"
    },
    {
        "name": "Prakhar",
        "api": "prakharapi.classx.co.in"
    },
    {
        "name": "Pramakhilclasses",
        "api": "pramakhilclassesapi.classx.co.in"
    },
    {
        "name": "Pramodsarangclasses",
        "api": "pramodsarangclassesapi.classx.co.in"
    },
    {
        "name": "Prasadacademyofficial",
        "api": "prasadacademyofficialapi.classx.co.in"
    },
    {
        "name": "Prashantchaturvedi",
        "api": "prashantchaturvediapi.classx.co.in"
    },
    {
        "name": "Prashareducare",
        "api": "prashareducareapi.classx.co.in"
    },
    {
        "name": "Pratapacademy",
        "api": "pratapacademyapi.classx.co.in"
    },
    {
        "name": "Pratapcampus",
        "api": "pratapcampusapi.classx.co.in"
    },
    {
        "name": "Prathamacademy",
        "api": "prathamacademyapi.classx.co.in"
    },
    {
        "name": "Pratigyaclasses",
        "api": "pratigyaclassesapi.classx.co.in"
    },
    {
        "name": "Pratigyaclassesjodhpur",
        "api": "pratigyaclassesjodhpurapi.classx.co.in"
    },
    {
        "name": "Pratigyalearningapp",
        "api": "pratigyalearningappapi.classx.co.in"
    },
    {
        "name": "Pratikbhad",
        "api": "pratikbhadapi.classx.co.in"
    },
    {
        "name": "Pratiyogitaghatnachakra",
        "api": "pratiyogitaghatnachakraapi.classx.co.in"
    },
    {
        "name": "Pravinchormalesmasterclass",
        "api": "pravinchormalesmasterclassapi.classx.co.in"
    },
    {
        "name": "Pravinkadsclasses",
        "api": "pravinkadsclassesapi.classx.co.in"
    },
    {
        "name": "Prayagfoundationindore",
        "api": "prayagfoundationindoreapi.classx.co.in"
    },
    {
        "name": "Prayagiasacademy",
        "api": "prayagiasacademyapi.classx.co.in"
    },
    {
        "name": "Prayagrajgsresearchcenter",
        "api": "prayagrajgsresearchcenterapi.classx.co.in"
    },
    {
        "name": "Prayasinstitute",
        "api": "prayasinstituteapi.classx.co.in"
    },
    {
        "name": "Prayasinstituteofagriculture",
        "api": "prayasinstituteofagricultureapi.classx.co.in"
    },
    {
        "name": "Prbankingadda",
        "api": "prbankingaddaapi.classx.co.in"
    },
    {
        "name": "Prepfusion",
        "api": "prepfusionapi.classx.co.in"
    },
    {
        "name": "Prepgyan",
        "api": "prepgyanapi.classx.co.in"
    },
    {
        "name": "Prepkar",
        "api": "prepkarapi.classx.co.in"
    },
    {
        "name": "Primepostalacademy",
        "api": "primepostalacademyapi.classx.co.in"
    },
    {
        "name": "Primeprofessionalclassesppc",
        "api": "primeprofessionalclassesppcapi.classx.co.in"
    },
    {
        "name": "Princedefenceacademy",
        "api": "princedefenceacademyapi.classx.co.in"
    },
    {
        "name": "Prishaias",
        "api": "prishaiasapi.classx.co.in"
    },
    {
        "name": "Priyeshsirvidyapeeth",
        "api": "priyeshsirvidyapeethapi.classx.co.in"
    },
    {
        "name": "Proeduhut",
        "api": "proeduhutapi.classx.co.in"
    },
    {
        "name": "Professionalcommerce",
        "api": "professionalcommerceapi.classx.co.in"
    },
    {
        "name": "Profinserv",
        "api": "profinservapi.classx.co.in"
    },
    {
        "name": "Proggapon",
        "api": "proggaponapi.classx.co.in"
    },
    {
        "name": "Provekarexam",
        "api": "provekarexamapi.classx.co.in"
    },
    {
        "name": "Psc",
        "api": "pscmantraapi.classx.co.in"
    },
    {
        "name": "Psibaba",
        "api": "psibabaapi.classx.co.in"
    },
    {
        "name": "Psychologytrading",
        "api": "psychologytradingapi.classx.co.in"
    },
    {
        "name": "Ptech",
        "api": "ptechapi.classx.co.in"
    },
    {
        "name": "Ptscadexpert",
        "api": "ptscadexpertapi.classx.co.in"
    },
    {
        "name": "Pulseaiims",
        "api": "pulseaiimsapi.classx.co.in"
    },
    {
        "name": "Puneetsirreasoning",
        "api": "puneetsirreasoningapi.classx.co.in"
    },
    {
        "name": "Purnaeducare",
        "api": "purnaeducareapi.classx.co.in"
    },
    {
        "name": "Purplehat",
        "api": "purplehatapi.classx.co.in"
    },
    {
        "name": "Qualitypluseducation",
        "api": "qualitypluseducationapi.classx.co.in"
    },
    {
        "name": "Quantachemistry",
        "api": "quantachemistryapi.teachx.in"
    },
    {
        "name": "Quantachemistryofficial",
        "api": "quantachemistryapi.classx.co.in"
    },
    {
        "name": "Quantapoint",
        "api": "quantapointapi.classx.co.in"
    },
    {
        "name": "Quantezy",
        "api": "quantezyapi.classx.co.in"
    },
    {
        "name": "Quickermaths",
        "api": "quickermathsapi.classx.co.in"
    },
    {
        "name": "Quizmaster",
        "api": "quizmasterapi.classx.co.in"
    },
    {
        "name": "R2Cacademy",
        "api": "r2cacademyapi.classx.co.in"
    },
    {
        "name": "Radhekrishnaacademyeducationapp",
        "api": "radhekrishnaacademyeducationappapi.classx.co.in"
    },
    {
        "name": "Radhinaquants",
        "api": "radhinaquantsapi.classx.co.in"
    },
    {
        "name": "Raghuramsacademy",
        "api": "raghuramsacademyapi.classx.co.in"
    },
    {
        "name": "Rahi",
        "api": "rahiappapi.classx.co.in"
    },
    {
        "name": "Rahmaniayurveda",
        "api": "rahmaniayurvedaapi.classx.co.in"
    },
    {
        "name": "Rahmanpathan",
        "api": "rahmanpathanapi.classx.co.in"
    },
    {
        "name": "Rahuldeshwalacademytoptak",
        "api": "rahuldeshwalacademyapi.classx.co.in"
    },
    {
        "name": "Rahulscienceacademy",
        "api": "rahulscienceacademyapi.classx.co.in"
    },
    {
        "name": "Railwayadda24",
        "api": "railwayadda24api.classx.co.in"
    },
    {
        "name": "Raithan",
        "api": "raithanapi.classx.co.in"
    },
    {
        "name": "Rajasthan360",
        "api": "rajasthan360api.classx.co.in"
    },
    {
        "name": "Rajclassesbansur",
        "api": "rajclassesbansurapi.classx.co.in"
    },
    {
        "name": "Rajeevacademy",
        "api": "rajeevacademyapi.classx.co.in"
    },
    {
        "name": "Rajeshbharate",
        "api": "rajeshbharateapi.classx.co.in"
    },
    {
        "name": "Rajfashionmaker",
        "api": "rajfashionmakerapi.classx.co.in"
    },
    {
        "name": "Rajhansshorthandclasses",
        "api": "rajhansshorthandclassesapi.classx.co.in"
    },
    {
        "name": "Rajkumarbandalsacademy",
        "api": "rajkumarbandalsacademyapi.classx.co.in"
    },
    {
        "name": "Rajmudraiasacademy",
        "api": "rajmudraiasacademyapi.classx.co.in"
    },
    {
        "name": "Rajmudralatur",
        "api": "rajmudralaturapi.classx.co.in"
    },
    {
        "name": "Rajnishsharmaclasses",
        "api": "rajnishsharmaclassesapi.classx.co.in"
    },
    {
        "name": "Rajpootananotes",
        "api": "rajpootananotesapi.classx.co.in"
    },
    {
        "name": "Rajsevaclasses",
        "api": "rajsevaclassesapi.classx.co.in"
    },
    {
        "name": "Rakeshsirmathsclasses",
        "api": "rakeshsirmathsclassesapi.classx.co.in"
    },
    {
        "name": "Rakshitsingh",
        "api": "rakshitsinghapi.classx.co.in"
    },
    {
        "name": "Ramaiahcoaching",
        "api": "ramaiahcoachingapi.classx.co.in"
    },
    {
        "name": "Ramanshugs",
        "api": "ramanshugsclassesapi.classx.co.in"
    },
    {
        "name": "Ramasgurukul",
        "api": "ramasgurukulapi.classx.co.in"
    },
    {
        "name": "Rambanacademy",
        "api": "rambanacademyapi.classx.co.in"
    },
    {
        "name": "Ramdasshrikrushnawaghaakarupscmpsc",
        "api": "ramdasshrikrushnawaghapi.classx.co.in"
    },
    {
        "name": "Ramdevcareerclasses",
        "api": "ramdevcareerclassesapi.classx.co.in"
    },
    {
        "name": "Ramjikipathshala",
        "api": "ramjikipathshalaapi.classx.co.in"
    },
    {
        "name": "Ramnarayan",
        "api": "ramnarayanapi.classx.co.in"
    },
    {
        "name": "Ramnivassirmaths",
        "api": "ramnivassirmathsapi.classx.co.in"
    },
    {
        "name": "Ramsirstudy",
        "api": "ramsirstudyapi.classx.co.in"
    },
    {
        "name": "Ranjitmathematicsclasses",
        "api": "ranjitmathematicsclassesapi.classx.co.in"
    },
    {
        "name": "Rankers",
        "api": "rankersapi.appx.co.in"
    },
    {
        "name": "Rankers",
        "api": "rankersapi.classx.co.in"
    },
    {
        "name": "Rankersdefenceacademy",
        "api": "rankerdefenceapi.classx.co.in"
    },
    {
        "name": "Rankersiq",
        "api": "rankersiqapi.classx.co.in"
    },
    {
        "name": "Rankupeducation",
        "api": "rankupeducationapi.classx.co.in"
    },
    {
        "name": "Raoscareerinstitute",
        "api": "raocareerinstituteapi.classx.co.in"
    },
    {
        "name": "Rasbabadeepaksir",
        "api": "rasbabadeepaksirapi.classx.co.in"
    },
    {
        "name": "Rathodonlineacademy",
        "api": "rathodonlineacademyapi.classx.co.in"
    },
    {
        "name": "Rationalacademy",
        "api": "rationalacademyupapi.classx.co.in"
    },
    {
        "name": "Ratnaifoundation",
        "api": "ratnaifoundationapi.classx.co.in"
    },
    {
        "name": "Rattaeducation",
        "api": "rattaeducationapi.classx.co.in"
    },
    {
        "name": "Rautsiruniqueacademyyavatmal",
        "api": "rautsiruniqueacademyyavatmalapi.classx.co.in"
    },
    {
        "name": "Ravacademyformpscupsc",
        "api": "ravacademyapi.classx.co.in"
    },
    {
        "name": "Ravideduplus",
        "api": "ravideduplusapi.classx.co.in"
    },
    {
        "name": "Ravidfmaudiobooklearning",
        "api": "ravidfmaudiobooklearningapi.classx.co.in"
    },
    {
        "name": "Ravindrababuravula",
        "api": "ravindrababuravulaapi.classx.co.in"
    },
    {
        "name": "Ravinkipathshala",
        "api": "ravinpathshalaapi.classx.co.in"
    },
    {
        "name": "Rayalanandagopalonlineacademy",
        "api": "rayalanandagopalonlineacademyapi.classx.co.in"
    },
    {
        "name": "Rayatprabodhiniofficial",
        "api": "rayatprabodhiniofficialapi.classx.co.in"
    },
    {
        "name": "Rbe",
        "api": "revolutioneducationapi.teachx.in"
    },
    {
        "name": "Rcmathematics",
        "api": "rcmathematicsapi.classx.co.in"
    },
    {
        "name": "Rdmglobalstudies",
        "api": "rdmglobalstudiesapi.classx.co.in"
    },
    {
        "name": "Realknowledgeworld",
        "api": "realknowledgeworldapi.classx.co.in"
    },
    {
        "name": "Realstudy",
        "api": "realstudyapi.classx.co.in"
    },
    {
        "name": "Reasoningbypulkitsir",
        "api": "reasoningpulkitapi.classx.co.in"
    },
    {
        "name": "Reasoningbypuransir",
        "api": "reasoningpuransirapi.classx.co.in"
    },
    {
        "name": "Reasoningguru",
        "api": "reasoningguruapi.classx.co.in"
    },
    {
        "name": "Reasoninglife",
        "api": "reasoninglifeapi.classx.co.in"
    },
    {
        "name": "Reasoningrunway",
        "api": "reasoningrunwayrspailwarapi.classx.co.in"
    },
    {
        "name": "Reasoningwallah",
        "api": "reasoningwallahapi.classx.co.in"
    },
    {
        "name": "Recevaacademy",
        "api": "racevaacademyapi.classx.co.in"
    },
    {
        "name": "Reliableacademyhigher",
        "api": "reliableacademyhigherapi.classx.co.in"
    },
    {
        "name": "Reliableofficer",
        "api": "reliableofficerapi.classx.co.in"
    },
    {
        "name": "Resonanceias",
        "api": "resonanceiasapi.classx.co.in"
    },
    {
        "name": "Restartias",
        "api": "restartiasapi.classx.co.in"
    },
    {
        "name": "Resultguru",
        "api": "resultguruapi.classx.co.in"
    },
    {
        "name": "Resultmitra",
        "api": "resultmitraapi.classx.co.in"
    },
    {
        "name": "Revisersacademy",
        "api": "revisersacademyapi.classx.co.in"
    },
    {
        "name": "Revolutionbyeducation",
        "api": "revolutioneducationapi.classx.co.in"
    },
    {
        "name": "Rglectures",
        "api": "rglecturesapi.classx.co.in"
    },
    {
        "name": "Rgvikramjeet",
        "api": "rgvikramjeetapi.classx.co.in"
    },
    {
        "name": "Rhchemistry",
        "api": "rhchemistryapi.classx.co.in"
    },
    {
        "name": "Riseacademy",
        "api": "riseacademyapi.classx.co.in"
    },
    {
        "name": "Rishamamlearningcentre",
        "api": "rishamamlearningcentreapi.classx.co.in"
    },
    {
        "name": "Ritustudypoint",
        "api": "ritustudypointapi.classx.co.in"
    },
    {
        "name": "Rjcbtnursing",
        "api": "rjcbtnursingapi.classx.co.in"
    },
    {
        "name": "Rjinstitute",
        "api": "rjinstituteapi.classx.co.in"
    },
    {
        "name": "Rjstudypoint",
        "api": "rjstudypointapi.classx.co.in"
    },
    {
        "name": "Rkracademy",
        "api": "rkracademyapi.classx.co.in"
    },
    {
        "name": "Rksirenglish",
        "api": "rksirenglishapi.classx.co.in"
    },
    {
        "name": "Rksirofficial",
        "api": "rksirofficialapi.classx.co.in"
    },
    {
        "name": "Rktutorialofficial",
        "api": "rktutorialofficialapi.classx.co.in"
    },
    {
        "name": "Rlc",
        "api": "rlcapi.classx.co.in"
    },
    {
        "name": "Rmc",
        "api": "rmcapi.classx.co.in"
    },
    {
        "name": "Rmcprofithouse",
        "api": "rmcprofithouseapi.classx.co.in"
    },
    {
        "name": "Rnsstudies",
        "api": "rnsstudiesapi.classx.co.in"
    },
    {
        "name": "Robustlearning",
        "api": "robustlearningapi.classx.co.in"
    },
    {
        "name": "Rohitnegi",
        "api": "rohitnegiapi.classx.co.in"
    },
    {
        "name": "Rohitvaidwannotes",
        "api": "rohitvaidwannotesapi.classx.co.in"
    },
    {
        "name": "Rojgarrunwaycareerinstitute",
        "api": "rojgarrunwaycareerinstituteapi.classx.co.in"
    },
    {
        "name": "Rojgarsagar",
        "api": "rojgarsagarapi.classx.co.in"
    },
    {
        "name": "Rojgarsetu",
        "api": "rojgarsetuapi.classx.co.in"
    },
    {
        "name": "Rojgarwithankit",
        "api": "rozgarapinew.teachx.in"
    },
    {
        "name": "Rojgarwithsubhash",
        "api": "rojgarwithsubhashapi.classx.co.in"
    },
    {
        "name": "Roshangaurgsclasses",
        "api": "roshangaurgsclassesapi.classx.co.in"
    },
    {
        "name": "Roydsircareerhit",
        "api": "roydsircareerhitapi.classx.co.in"
    },
    {
        "name": "Rpconcept",
        "api": "rpconceptapi.classx.co.in"
    },
    {
        "name": "Rpscnotes",
        "api": "rpscnotesapi.classx.co.in"
    },
    {
        "name": "Rracademy",
        "api": "rracademyapi.classx.co.in"
    },
    {
        "name": "Rrcampus",
        "api": "rrcampusapi.classx.co.in"
    },
    {
        "name": "Rsbrailwayexams",
        "api": "rsbrailwayexamsapi.classx.co.in"
    },
    {
        "name": "Rsclasses",
        "api": "rsclassesapi.classx.co.in"
    },
    {
        "name": "Rslearningplatform",
        "api": "rslearningplatformapi.classx.co.in"
    },
    {
        "name": "Rssdigital",
        "api": "rssdigitalapi.classx.co.in"
    },
    {
        "name": "Rudraacademy",
        "api": "rudraacademyapi.classx.co.in"
    },
    {
        "name": "Rukminieducationcenter",
        "api": "rukminieducationcenterapi.classx.co.in"
    },
    {
        "name": "Rvmanushistudy",
        "api": "rvmanushistudyapi.classx.co.in"
    },
    {
        "name": "Saarthieducation",
        "api": "saarthieducationapi.classx.co.in"
    },
    {
        "name": "Saarthimentor",
        "api": "saarthimentorapi.classx.co.in"
    },
    {
        "name": "Saarthispk",
        "api": "saarthispkapi.classx.co.in"
    },
    {
        "name": "Sachin",
        "api": "sachinacademyapi.classx.co.in"
    },
    {
        "name": "Sachindhawalesmathsandreasoningacademy",
        "api": "sachindhawaleapi.classx.co.in"
    },
    {
        "name": "Sachingaikwadte",
        "api": "sachingaikwadteamapi.classx.co.in"
    },
    {
        "name": "Sachinwarulkar",
        "api": "sachinwarulkarapi.classx.co.in"
    },
    {
        "name": "Sadhyaacademy",
        "api": "sadhyaacademyapi.classx.co.in"
    },
    {
        "name": "Safalacademyforgpsc",
        "api": "safalacademyforgpscapi.classx.co.in"
    },
    {
        "name": "Safalsteps",
        "api": "safalstepsapi.classx.co.in"
    },
    {
        "name": "Safaltabyprashantsir",
        "api": "safaltaprashantsirapi.classx.co.in"
    },
    {
        "name": "Safaltaexpress",
        "api": "safaltaexpressapi.classx.co.in"
    },
    {
        "name": "Safaltamanthan247",
        "api": "safaltamanthan247api.classx.co.in"
    },
    {
        "name": "Safaltaschool",
        "api": "safaltaschoolapi.classx.co.in"
    },
    {
        "name": "Safaltatestseriesacademy",
        "api": "safaltatestseriesacademyapi.classx.co.in"
    },
    {
        "name": "Sagarcompetitiveacademy",
        "api": "sagarcompetitiveacademyapi.classx.co.in"
    },
    {
        "name": "Sagarmathematics",
        "api": "sagarmathematicsapi.classx.co.in"
    },
    {
        "name": "Sagarsindhuridlc",
        "api": "sagarsindhuridlcapi.classx.co.in"
    },
    {
        "name": "Sagaryadavmathsindore",
        "api": "sagaryadavmathsindoreapi.classx.co.in"
    },
    {
        "name": "Sahadevchoudhary",
        "api": "hindisahadevchoudharyapi.classx.co.in"
    },
    {
        "name": "Sahilsir",
        "api": "quicktrickssahilsirapi.classx.co.in"
    },
    {
        "name": "Sahityaacademy",
        "api": "sahityaacademyapi.classx.co.in"
    },
    {
        "name": "Sahityasangamonlineclasses",
        "api": "sahityasangamonlineclassesapi.classx.co.in"
    },
    {
        "name": "Sahityatheliterature",
        "api": "sahityatheliteratureapi.classx.co.in"
    },
    {
        "name": "Sahyadriacademybaramati",
        "api": "sahyadriacademybaramatiapi.classx.co.in"
    },
    {
        "name": "Sahyadriias",
        "api": "sahyadriiasapi.classx.co.in"
    },
    {
        "name": "Sahyadritestseriesbaramati",
        "api": "sahyadritestseriesbaramatiapi.classx.co.in"
    },
    {
        "name": "Saiacademy",
        "api": "saiacademyapi.classx.co.in"
    },
    {
        "name": "Saigangabooks",
        "api": "saigangaapi.classx.co.in"
    },
    {
        "name": "Saimedhaecet",
        "api": "saimedhaecetapi.classx.co.in"
    },
    {
        "name": "Saimedhagate",
        "api": "saimedhagateapi.classx.co.in"
    },
    {
        "name": "Saimedhajlm",
        "api": "saimedhajlmapi.classx.co.in"
    },
    {
        "name": "Saimedhaunity",
        "api": "saimedhaunityapi.classx.co.in"
    },
    {
        "name": "Sakarforum",
        "api": "sakarforumapi.classx.co.in"
    },
    {
        "name": "Salesforceandinterviews",
        "api": "salesforceandinterviewsapi.classx.co.in"
    },
    {
        "name": "Salesforcegeek",
        "api": "salesforcegeekapi.classx.co.in"
    },
    {
        "name": "Samadhankokate",
        "api": "samadhankokatepolityapi.classx.co.in"
    },
    {
        "name": "Samarthacademy",
        "api": "samarthacademyapi.classx.co.in"
    },
    {
        "name": "Samayak",
        "api": "samyakapi.teachx.in"
    },
    {
        "name": "Samikshainstitute",
        "api": "samikshainstituteapi.classx.co.in"
    },
    {
        "name": "Samyak",
        "api": "samyakapi.classx.co.in"
    },
    {
        "name": "Sandeepjyani",
        "api": "sandeepjyanicivilengineeringapi.classx.co.in"
    },
    {
        "name": "Sandeepsirclasses",
        "api": "sandeepsirclassesapi.classx.co.in"
    },
    {
        "name": "Sandeshwithravisir",
        "api": "sandeshravisirapi.classx.co.in"
    },
    {
        "name": "Sandipargadesinstitute",
        "api": "sandipargadeinstituteapi.classx.co.in"
    },
    {
        "name": "Sangarshparivar",
        "api": "sangharshparivarapi.classx.co.in"
    },
    {
        "name": "Sangharshacademyapppbn",
        "api": "sangharshacademyapppbnapi.classx.co.in"
    },
    {
        "name": "Sangharshindia",
        "api": "sangharshindiaapi.classx.co.in"
    },
    {
        "name": "Sanjaychemtutorial",
        "api": "sanjaychemtutorialapi.classx.co.in"
    },
    {
        "name": "Sanjaypahadesmathsreasoningacademy",
        "api": "sanjaypahademathsreasoningacademyapi.classx.co.in"
    },
    {
        "name": "Sanjayvighnefutureofficer",
        "api": "sanjayvighnefutureofficerapi.classx.co.in"
    },
    {
        "name": "Sanjeevkijani",
        "api": "sanjeevkijaniapi.classx.co.in"
    },
    {
        "name": "Sankalp",
        "api": "sankalpcoachingganganagarapi.classx.co.in"
    },
    {
        "name": "Sankalp",
        "api": "sankalpclassesapi.appx.co.in"
    },
    {
        "name": "Sankalp2447",
        "api": "sankalp2447api.classx.co.in"
    },
    {
        "name": "Sankalpacademy",
        "api": "sankalpacademyapi.classx.co.in"
    },
    {
        "name": "Sankalpclasses",
        "api": "sankalpclassesapi.classx.co.in"
    },
    {
        "name": "Sankalpclassesmsp",
        "api": "sankalpclassesmspapi.classx.co.in"
    },
    {
        "name": "Sankalptrinity",
        "api": "sankalptrinityapi.classx.co.in"
    },
    {
        "name": "Sanketsirgs",
        "api": "sanketsirgscentreapi.classx.co.in"
    },
    {
        "name": "Sankhokun",
        "api": "sankhokunapi.classx.co.in"
    },
    {
        "name": "Sanskritganga",
        "api": "sanskritganganewapi.classx.co.in"
    },
    {
        "name": "Sanskritsamriddhi",
        "api": "sanskritsamriddhiapi.appx.co.in"
    },
    {
        "name": "Sanskritsannidhyam",
        "api": "sanskritsannidhyamapi.classx.co.in"
    },
    {
        "name": "Sanskrutiaryagurukulam",
        "api": "sanskrutiaryagurukulamapi.classx.co.in"
    },
    {
        "name": "Santsirclasses",
        "api": "santsirclassesapi.classx.co.in"
    },
    {
        "name": "Saptrangnursecarrieracademy",
        "api": "saptrangnursecarrieracademyapi.classx.co.in"
    },
    {
        "name": "Saraakash",
        "api": "saraakashapi.classx.co.in"
    },
    {
        "name": "Saraswatacademy",
        "api": "saraswatacademyapi.classx.co.in"
    },
    {
        "name": "Sarkarigurukul",
        "api": "sarkarigurukulapi.classx.co.in"
    },
    {
        "name": "Sarkarimasterofficial",
        "api": "sarkarimasterofficialapi.classx.co.in"
    },
    {
        "name": "Sarkarinaukari",
        "api": "sarkarinaukariapi.classx.co.in"
    },
    {
        "name": "Sarkarinaukriwale",
        "api": "sarkarinaukriwaleapi.classx.co.in"
    },
    {
        "name": "Sarokarshikshansansthan",
        "api": "sarokarshikshansansthanapi.classx.co.in"
    },
    {
        "name": "Sartazclasses",
        "api": "sartazclassesapi.classx.co.in"
    },
    {
        "name": "Sarthakclassespaota",
        "api": "sarthakclassespaotaapi.classx.co.in"
    },
    {
        "name": "Sarthiacademyakns",
        "api": "sarthiacademyaknsapi.classx.co.in"
    },
    {
        "name": "Sarthidigitalclassroom",
        "api": "sarthidigitalclassroomapi.classx.co.in"
    },
    {
        "name": "Sarthisupportdigitalclass",
        "api": "sarthisupportdigitalclassapi.classx.co.in"
    },
    {
        "name": "Sarvodayaacademy",
        "api": "sarvodayaacademyschoolcompetitiveexamapi.classx.co.in"
    },
    {
        "name": "Sarvodayaacademyrajasthan",
        "api": "sarvodayaacademyrajasthanapi.classx.co.in"
    },
    {
        "name": "Sarvodayaonline",
        "api": "sarvodayaonlineapi.classx.co.in"
    },
    {
        "name": "Sateeshenglishmethodologylogics",
        "api": "sateeshenglishmethodologylogicsapi.classx.co.in"
    },
    {
        "name": "Satendrasiasacademy",
        "api": "satendraiasapi.classx.co.in"
    },
    {
        "name": "Satendrasir",
        "api": "satendrasirclassesapi.classx.co.in"
    },
    {
        "name": "Satishscienceacademy",
        "api": "satishscienceacademyapi.classx.co.in"
    },
    {
        "name": "Satvalearningapp",
        "api": "satvalearningappapi.classx.co.in"
    },
    {
        "name": "Satyadisharma",
        "api": "satyadhisharmaclassesapi.classx.co.in"
    },
    {
        "name": "Satyamclassesgorakhpur",
        "api": "satyamclassesgorakhpurapi.classx.co.in"
    },
    {
        "name": "Satyarthinstitute",
        "api": "satyarthinstituteapi.classx.co.in"
    },
    {
        "name": "Saurabhsirclasses",
        "api": "saurabhsirclassesapi.classx.co.in"
    },
    {
        "name": "Savarncoaching",
        "api": "savarncoachingapi.classx.co.in"
    },
    {
        "name": "Savijayiasdelhi",
        "api": "savijayiasapi.classx.co.in"
    },
    {
        "name": "Sbexamexamscrackapp",
        "api": "sbexamexamscrackappapi.classx.co.in"
    },
    {
        "name": "Sbsuccessbymallikarjunasir",
        "api": "sbsuccessbymallikarjunasirapi.classx.co.in"
    },
    {
        "name": "Sbsuccesspoint",
        "api": "sbsuccesspointapi.classx.co.in"
    },
    {
        "name": "Sbtechmathacademy",
        "api": "sbtechmathapi.classx.co.in"
    },
    {
        "name": "Scholarscareeracademy",
        "api": "scholarscareeracademyapi.classx.co.in"
    },
    {
        "name": "Schoolingmantra",
        "api": "schoolingmantraapi.classx.co.in"
    },
    {
        "name": "Scienceacademy",
        "api": "scienceacademyapi.classx.co.in"
    },
    {
        "name": "Scienceacademybyaarifsir",
        "api": "scienceacademyaarifsirapi.classx.co.in"
    },
    {
        "name": "Sciencebyanilkotle",
        "api": "scienceanilkotleapi.classx.co.in"
    },
    {
        "name": "Sciencebypriya",
        "api": "sciencepriyamaamapi.classx.co.in"
    },
    {
        "name": "Sciencefun",
        "api": "sciencefunapi.classx.co.in"
    },
    {
        "name": "Scienceplus",
        "api": "scienceplusapi.classx.co.in"
    },
    {
        "name": "Sciencesamrajya",
        "api": "sciencesamrajyaapi.classx.co.in"
    },
    {
        "name": "Sciencesangrah",
        "api": "sciencesangrahapi.classx.co.in"
    },
    {
        "name": "Sciencetechnologybydrsantosh",
        "api": "sciencetechnologydrsantoshapi.classx.co.in"
    },
    {
        "name": "Scmagnet",
        "api": "sciencemagnetapi.classx.co.in"
    },
    {
        "name": "Sctacademy",
        "api": "sctacademyapi.classx.co.in"
    },
    {
        "name": "Sdcampus",
        "api": "sdcampusapi.classx.co.in"
    },
    {
        "name": "Sdcareer",
        "api": "sdcareerapi.classx.co.in"
    },
    {
        "name": "Selection",
        "api": "selectionguruapi.classx.co.in"
    },
    {
        "name": "Selectionacademy",
        "api": "selectionacademyapi.classx.co.in"
    },
    {
        "name": "Selectionboardacademy",
        "api": "selectionboardacademyapi.classx.co.in"
    },
    {
        "name": "Selectionboardjaipur",
        "api": "selectionboardjaipurapi.classx.co.in"
    },
    {
        "name": "Selectiondarbar",
        "api": "selectiondarbarapi.classx.co.in"
    },
    {
        "name": "Selectiondunia",
        "api": "selectionduniaapi.classx.co.in"
    },
    {
        "name": "Selectiongurukul",
        "api": "selectiongurukulapi.classx.co.in"
    },
    {
        "name": "Selectionhub",
        "api": "selectionhubapi.classx.co.in"
    },
    {
        "name": "Selectionshala",
        "api": "selectionshalaapi.classx.co.in"
    },
    {
        "name": "Selectiontak",
        "api": "selectiontakapi.classx.co.in"
    },
    {
        "name": "Selectiontaknew",
        "api": "selectiontakmpapi.classx.co.in"
    },
    {
        "name": "Selectionwarrior",
        "api": "selectionwarriorapi.classx.co.in"
    },
    {
        "name": "Serenepathsala",
        "api": "serenepathshalaapi.classx.co.in"
    },
    {
        "name": "Sgacademy",
        "api": "sgacademyapi.classx.co.in"
    },
    {
        "name": "Sgcommerceclasses",
        "api": "sgcommerceclassesapi.classx.co.in"
    },
    {
        "name": "Shahidsirseducationpoint",
        "api": "shahidsirseducationpointapi.classx.co.in"
    },
    {
        "name": "Shaileshclasses",
        "api": "shaileshclassesapi.classx.co.in"
    },
    {
        "name": "Sharadcoachingclasses",
        "api": "sharadcoachingclassesapi.classx.co.in"
    },
    {
        "name": "Sharadsenglishclubpune",
        "api": "sharadsenglishclubpuneapi.classx.co.in"
    },
    {
        "name": "Shardaexam",
        "api": "shardaexamapi.classx.co.in"
    },
    {
        "name": "Shardeclassesnokha",
        "api": "shardeclassesnokhaapi.classx.co.in"
    },
    {
        "name": "Sharmaclassesjodhpurshikshaguru",
        "api": "sharmaclassesjodhpurapi.classx.co.in"
    },
    {
        "name": "Shashankdefenceacademy",
        "api": "shashankdefenceacademyapi.classx.co.in"
    },
    {
        "name": "Shikharclassroom",
        "api": "shikharclassroomapi.classx.co.in"
    },
    {
        "name": "Shikhareducation",
        "api": "shikhareducationapi.classx.co.in"
    },
    {
        "name": "Shikhareducationresearchcentre",
        "api": "shikhareducationresearchcentreapi.classx.co.in"
    },
    {
        "name": "Shikharsthelearningapp",
        "api": "shikharslearningapi.classx.co.in"
    },
    {
        "name": "Shiksha",
        "api": "shikshapathapi.classx.co.in"
    },
    {
        "name": "Shikshadham",
        "api": "shikshadhamdelhiapi.classx.co.in"
    },
    {
        "name": "Shikshadhamofficialwinning",
        "api": "shikshadhamofficialapi.classx.co.in"
    },
    {
        "name": "Shikshakul",
        "api": "shikshakulapi.classx.co.in"
    },
    {
        "name": "Shikshasamagam",
        "api": "shikshasamagamapi.classx.co.in"
    },
    {
        "name": "Shikshayuglive",
        "api": "shikshayugliveapi.classx.co.in"
    },
    {
        "name": "Shineindiagroupsacademy",
        "api": "shineindiagroupsacademyapi.classx.co.in"
    },
    {
        "name": "Shinusingh",
        "api": "shinusinghapi.classx.co.in"
    },
    {
        "name": "Shivaclassesbiharagriculture",
        "api": "shivaclassesbiharagricultureapi.classx.co.in"
    },
    {
        "name": "Shivajinimat",
        "api": "shivajinimatapi.classx.co.in"
    },
    {
        "name": "Shivcoachingclasses",
        "api": "shivcoachingclassesapi.classx.co.in"
    },
    {
        "name": "Shivikakipathshala",
        "api": "shivikakipathshalaapi.classx.co.in"
    },
    {
        "name": "Shivzmusic",
        "api": "shivzmusicapi.classx.co.in"
    },
    {
        "name": "Shomusbiology",
        "api": "shomusbiologyapi.classx.co.in"
    },
    {
        "name": "Shreeacademy",
        "api": "shreeacademyapi.classx.co.in"
    },
    {
        "name": "Shreebalajinursingacademy",
        "api": "shreebalajinursingacademyapi.classx.co.in"
    },
    {
        "name": "Shreeclasses",
        "api": "shreeclassesapi.classx.co.in"
    },
    {
        "name": "Shreeenglish",
        "api": "shreeenglishapi.classx.co.in"
    },
    {
        "name": "Shreeganeshclasses",
        "api": "shreeganeshclassesapi.classx.co.in"
    },
    {
        "name": "Shreejipratyekam",
        "api": "shreejipratyekamapi.classx.co.in"
    },
    {
        "name": "Shreejistudycentre",
        "api": "shreejistudycentreapi.classx.co.in"
    },
    {
        "name": "Shreejitraders",
        "api": "shreejitradersapi.classx.co.in"
    },
    {
        "name": "Shreeramclasses",
        "api": "shreeramclassesapi.classx.co.in"
    },
    {
        "name": "Shreeramedumitra",
        "api": "shreeramedumitraapi.classx.co.in"
    },
    {
        "name": "Shrenikjainengineeringsimplified",
        "api": "engineeringsimplifiedapi.classx.co.in"
    },
    {
        "name": "Shreshthclasses",
        "api": "shreshthclassesapi.classx.co.in"
    },
    {
        "name": "Shreyajeeacademy",
        "api": "shreyajeeacademyapi.classx.co.in"
    },
    {
        "name": "Shubhamclasses",
        "api": "shubhamclassesapi.classx.co.in"
    },
    {
        "name": "Shubhameclasses",
        "api": "shubhameclassesapi.classx.co.in"
    },
    {
        "name": "Shubhamjagdish",
        "api": "shubhamjagdishapi.classx.co.in"
    },
    {
        "name": "Shubhiasacademy",
        "api": "shubhiasacademyapi.classx.co.in"
    },
    {
        "name": "Shuklaclassesdelhi",
        "api": "shuklaclassesdelhiapi.classx.co.in"
    },
    {
        "name": "Siddhantuedutech",
        "api": "siddhantuedutechapi.classx.co.in"
    },
    {
        "name": "Sigmaacademybyhemant",
        "api": "sigmaacademyhemantapi.classx.co.in"
    },
    {
        "name": "Sigmaclassesedutube",
        "api": "sigmaclassesapi.classx.co.in"
    },
    {
        "name": "Sigmaias",
        "api": "sigmaiasapi.classx.co.in"
    },
    {
        "name": "Sikarclasses",
        "api": "sikarclassesapi.classx.co.in"
    },
    {
        "name": "Sikhwalonlinehubjaipur",
        "api": "sikhwalonlinehubapi.classx.co.in"
    },
    {
        "name": "Simplifysuccess",
        "api": "simplifysuccessapi.classx.co.in"
    },
    {
        "name": "Simplifyuppsc",
        "api": "simplifyuppscapi.classx.co.in"
    },
    {
        "name": "Simplifyupscmpsc",
        "api": "simplifyupscmpscapi.classx.co.in"
    },
    {
        "name": "Simsnapclinic",
        "api": "simsnapclinicapi.classx.co.in"
    },
    {
        "name": "Singhinusa",
        "api": "singhusaapi.classx.co.in"
    },
    {
        "name": "Singhkorieducation",
        "api": "singhkorieducationapi.classx.co.in"
    },
    {
        "name": "Singhsahab",
        "api": "singhsahabapi.classx.co.in"
    },
    {
        "name": "Sirodiatestseriesapp",
        "api": "sirodiatestseriesappapi.classx.co.in"
    },
    {
        "name": "Sitachoudharyhistory",
        "api": "sitachoudharyhistoryapi.classx.co.in"
    },
    {
        "name": "Sivapallipsychology",
        "api": "sivapallipsychologyapi.classx.co.in"
    },
    {
        "name": "Siwalclasses",
        "api": "siwalclassesapi.classx.co.in"
    },
    {
        "name": "Sjnacademy",
        "api": "sjnacademyapi.classx.co.in"
    },
    {
        "name": "Skanclasses",
        "api": "skanclassesapi.classx.co.in"
    },
    {
        "name": "Skclass",
        "api": "skclassappapi.classx.co.in"
    },
    {
        "name": "Skeducationlive",
        "api": "skeducationliveapi.classx.co.in"
    },
    {
        "name": "Skilladda",
        "api": "skilladdaapi.classx.co.in"
    },
    {
        "name": "Skillupacademy",
        "api": "skillupacademyapi.classx.co.in"
    },
    {
        "name": "Skilluptech",
        "api": "skilluptechapi.classx.co.in"
    },
    {
        "name": "Skillverse",
        "api": "skillverseapi.classx.co.in"
    },
    {
        "name": "Skmathreasoning",
        "api": "skmathreasoningapi.classx.co.in"
    },
    {
        "name": "Skmstudy",
        "api": "skmstudyapi.classx.co.in"
    },
    {
        "name": "Sknayakclasses",
        "api": "sknayakclassesapi.classx.co.in"
    },
    {
        "name": "Skpatelsiasacademy",
        "api": "skpatelsiasacademyapi.classx.co.in"
    },
    {
        "name": "Skpolity",
        "api": "skpolityapi.classx.co.in"
    },
    {
        "name": "Sksrivastava",
        "api": "sksrivastavaapi.classx.co.in"
    },
    {
        "name": "Skyeducare",
        "api": "skyeducareapi.classx.co.in"
    },
    {
        "name": "Smartbookstore",
        "api": "smartbookstoreapi.classx.co.in"
    },
    {
        "name": "Smarteducationcenter",
        "api": "smarteducationcenterapi.classx.co.in"
    },
    {
        "name": "Smartmpscwala",
        "api": "smartmpscwalaapi.classx.co.in"
    },
    {
        "name": "Smartnotes",
        "api": "smartnotesapi.classx.co.in"
    },
    {
        "name": "Smartrankers",
        "api": "smartrankersapi.classx.co.in"
    },
    {
        "name": "Smartstudyclassespro",
        "api": "smartstudyclassesproapi.classx.co.in"
    },
    {
        "name": "Smartstudyfoundation",
        "api": "smartstudyfoundationapi.classx.co.in"
    },
    {
        "name": "Smartstudyras",
        "api": "smartstudyrasapi.classx.co.in"
    },
    {
        "name": "Smbis",
        "api": "smbisapi.classx.co.in"
    },
    {
        "name": "Smsinstitute",
        "api": "smsinstituteapi.classx.co.in"
    },
    {
        "name": "Sneakclub",
        "api": "sneakclubapi.classx.co.in"
    },
    {
        "name": "Softstudy",
        "api": "softstudyapi.classx.co.in"
    },
    {
        "name": "Solusacademy",
        "api": "solusacademyapi.classx.co.in"
    },
    {
        "name": "Sonuarmyclasses",
        "api": "sonuarmyclassesapi.classx.co.in"
    },
    {
        "name": "Sonusirclasses",
        "api": "sonusirclassesapi.classx.co.in"
    },
    {
        "name": "Soonyaacademylearnerapp",
        "api": "soonyaacademylearnerapi.classx.co.in"
    },
    {
        "name": "Spaceclasses",
        "api": "spaceclassesapi.classx.co.in"
    },
    {
        "name": "Spaceias",
        "api": "spaceiasapi.teachx.in"
    },
    {
        "name": "Spaceiasacademy",
        "api": "spaceiasapi.classx.co.in"
    },
    {
        "name": "Spacetutor",
        "api": "spacetutorapi.classx.co.in"
    },
    {
        "name": "Spandanias",
        "api": "spandaniasapi.classx.co.in"
    },
    {
        "name": "Spaneducation",
        "api": "spaneducationapi.classx.co.in"
    },
    {
        "name": "Spardhagram",
        "api": "spardhagramapi.classx.co.in"
    },
    {
        "name": "Spardhalines",
        "api": "spardhalinesapi.classx.co.in"
    },
    {
        "name": "Spardhaniti",
        "api": "spardhanitiapi.classx.co.in"
    },
    {
        "name": "Spardhapariksha",
        "api": "spardhaparikshaapi.classx.co.in"
    },
    {
        "name": "Spardhaparikshaupdate",
        "api": "spardhaparikshaupdateapi.classx.co.in"
    },
    {
        "name": "Sparkleeducation",
        "api": "sparkleeducationapi.classx.co.in"
    },
    {
        "name": "Sparkleeducationwithgaurav",
        "api": "sparkleeducationgauravapi.classx.co.in"
    },
    {
        "name": "Speakfluentlyankushpare",
        "api": "speakfluentlyankushpareapi.classx.co.in"
    },
    {
        "name": "Speakingchalks",
        "api": "speakingchalksapi.classx.co.in"
    },
    {
        "name": "Spectrumacademy",
        "api": "spectrumacademyapi.classx.co.in"
    },
    {
        "name": "Speedycurrentaffairsgk",
        "api": "speedycurrentaffairsgkapi.classx.co.in"
    },
    {
        "name": "Speedystudy",
        "api": "speedstudyapi.classx.co.in"
    },
    {
        "name": "Spguruagriculture",
        "api": "spguruagricultureapi.classx.co.in"
    },
    {
        "name": "Spmiasacademy",
        "api": "spmiasacademyapi.classx.co.in"
    },
    {
        "name": "Squaredice",
        "api": "squarediceapi.classx.co.in"
    },
    {
        "name": "Sreedharsstudies",
        "api": "sreedharsstudiesapi.classx.co.in"
    },
    {
        "name": "Sricompetitiveforum",
        "api": "sricompetitiveforumapi.classx.co.in"
    },
    {
        "name": "Sridhi",
        "api": "sridhiapi.classx.co.in"
    },
    {
        "name": "Srigayatriteluguacademy",
        "api": "srigayatriteluguacademyapi.classx.co.in"
    },
    {
        "name": "Srihanacademyneetjee",
        "api": "srihanacademyapi.classx.co.in"
    },
    {
        "name": "Srinivasmech",
        "api": "srinivasmechapi.classx.co.in"
    },
    {
        "name": "Srisaiacademy",
        "api": "srisaiacademyapi.classx.co.in"
    },
    {
        "name": "Srisaitutorial",
        "api": "srisaitutorialapi.classx.co.in"
    },
    {
        "name": "Srisatyaacademy",
        "api": "srisatyaacademyapi.classx.co.in"
    },
    {
        "name": "Srishailinypublications",
        "api": "srishailinyapi.classx.co.in"
    },
    {
        "name": "Sristiedu",
        "api": "sristieduapi.classx.co.in"
    },
    {
        "name": "Srkt",
        "api": "srktacademyapi.teachx.in"
    },
    {
        "name": "Srktacademy",
        "api": "srktacademyapi.classx.co.in"
    },
    {
        "name": "Srmacademy",
        "api": "srmacademyapi.classx.co.in"
    },
    {
        "name": "Ss",
        "api": "sandsappapi.classx.co.in"
    },
    {
        "name": "Ssacademy",
        "api": "ssacademyapi.classx.co.in"
    },
    {
        "name": "Ssbguide",
        "api": "ssbguideapi.classx.co.in"
    },
    {
        "name": "Ssbworld",
        "api": "ssbworldapi.classx.co.in"
    },
    {
        "name": "Sscgurukul",
        "api": "ssggurukulapi.appx.co.in"
    },
    {
        "name": "Sschsczone",
        "api": "sschsczoneapi.classx.co.in"
    },
    {
        "name": "Sscmakerexampreparation",
        "api": "sscmakerexampreparationapi.classx.co.in"
    },
    {
        "name": "Ssctelugu",
        "api": "sscteluguapi.classx.co.in"
    },
    {
        "name": "Sspathshala",
        "api": "sspathshalaapi.classx.co.in"
    },
    {
        "name": "Ssrganeshtelugu",
        "api": "ssrganeshteluguapi.classx.co.in"
    },
    {
        "name": "Sstbyanupamsir",
        "api": "sstanupamsirapi.classx.co.in"
    },
    {
        "name": "Sstpoint",
        "api": "sstpointapi.classx.co.in"
    },
    {
        "name": "Stariqeducation",
        "api": "stariqeducationapi.classx.co.in"
    },
    {
        "name": "Starmathematics",
        "api": "starmathematicsapi.classx.co.in"
    },
    {
        "name": "Stashokparwar",
        "api": "sciencetechnologyenvironmentashokpawarapi.classx.co.in"
    },
    {
        "name": "Stbgofficial",
        "api": "stbgofficialapi.classx.co.in"
    },
    {
        "name": "Stenoshala",
        "api": "stenoshalaapi.classx.co"
    },
    {
        "name": "Stenoshala",
        "api": "stenoshalaapi.classx.co.in"
    },
    {
        "name": "Stenoshalalearnshorthand",
        "api": "stenoshalalearnshorthandeaseapi.classx.co.in"
    },
    {
        "name": "Stiravindramane",
        "api": "stiravindramaneapi.classx.co.in"
    },
    {
        "name": "Stockburner",
        "api": "stockburnerapi.classx.co.in"
    },
    {
        "name": "Studento",
        "api": "studentoapi.classx.co.in"
    },
    {
        "name": "Studentscampus",
        "api": "studentscampusapi.classx.co.in"
    },
    {
        "name": "Study2Achieve",
        "api": "study2achieveapi.classx.co.in"
    },
    {
        "name": "Study8Home",
        "api": "study8homeapi.classx.co.in"
    },
    {
        "name": "Studyadda",
        "api": "studyaddaapi.classx.co.in"
    },
    {
        "name": "Studybharat",
        "api": "studybharatapi.classx.co.in"
    },
    {
        "name": "Studybypathaksir",
        "api": "studypathaksirapi.classx.co.in"
    },
    {
        "name": "Studycapitalcuetschoolprep",
        "api": "studycapitalcuetschoolprepapi.classx.co.in"
    },
    {
        "name": "Studychampionacademy",
        "api": "studychampionacademyapi.classx.co.in"
    },
    {
        "name": "Studycomofficial",
        "api": "studycomofficialapi.classx.co.in"
    },
    {
        "name": "Studydotcom",
        "api": "studydotcomapi.classx.co.in"
    },
    {
        "name": "Studyexamacademy",
        "api": "studyexamacademyapi.classx.co.in"
    },
    {
        "name": "Studyforcareer",
        "api": "studyforcareerapi.classx.co.in"
    },
    {
        "name": "Studygurupathshala",
        "api": "studygurupathshalaapi.classx.co.in"
    },
    {
        "name": "Studyhubkuchamancity",
        "api": "studyhubkuchamancityapi.classx.co.in"
    },
    {
        "name": "Studyhubpune",
        "api": "studyhubpuneapi.classx.co.in"
    },
    {
        "name": "Studyindiaadda",
        "api": "studyindiaaddaapi.classx.co.in"
    },
    {
        "name": "Studykar",
        "api": "studykarapi.classx.co.in"
    },
    {
        "name": "Studylab",
        "api": "learnamanbarkhaapi.appx.co.in"
    },
    {
        "name": "Studylive",
        "api": "studyliveapi.classx.co.in"
    },
    {
        "name": "Studylivenavnathsir",
        "api": "studylivenavnathsirapi.classx.co.in"
    },
    {
        "name": "Studyloverveer",
        "api": "studyloverveerapi.classx.co.in"
    },
    {
        "name": "Studymantra",
        "api": "studymantraapi.classx.co.in"
    },
    {
        "name": "Studymantramns",
        "api": "studymantramnsapi.classx.co.in"
    },
    {
        "name": "Studynitijaiibcaiib",
        "api": "studynitiapi.classx.co.in"
    },
    {
        "name": "Studynow",
        "api": "studynowapi.classx.co.in"
    },
    {
        "name": "Studyofeducation",
        "api": "studyofeducationapi.classx.co.in"
    },
    {
        "name": "Studyonacademy",
        "api": "studyonacademyapi.classx.co.in"
    },
    {
        "name": "Studyonline",
        "api": "studyonlineapi.classx.co.in"
    },
    {
        "name": "Studypanel",
        "api": "studypanelapi.classx.co.in"
    },
    {
        "name": "Studypass",
        "api": "studypassapi.classx.co.in"
    },
    {
        "name": "Studypie",
        "api": "studypieapi.classx.co.in"
    },
    {
        "name": "Studypillar",
        "api": "studypillarapi.classx.co.in"
    },
    {
        "name": "Studyplanet",
        "api": "studyplanetapi.classx.co.in"
    },
    {
        "name": "Studypoint",
        "api": "dheryastudypointapi.classx.co.in"
    },
    {
        "name": "Studypointwithnigamsir",
        "api": "studypointwithnigamsirapi.classx.co.in"
    },
    {
        "name": "Studyshala20",
        "api": "studyshala20api.classx.co.in"
    },
    {
        "name": "Studysyllabus",
        "api": "studysyllabusapi.classx.co.in"
    },
    {
        "name": "Studytimebangla",
        "api": "studytimebanglaapi.classx.co.in"
    },
    {
        "name": "Studytricks",
        "api": "studytricksapi.classx.co.in"
    },
    {
        "name": "Studyupacademypune",
        "api": "studyupacademypuneapi.classx.co.in"
    },
    {
        "name": "Studyvikram",
        "api": "studyvikramapi.classx.co.in"
    },
    {
        "name": "Studywadi",
        "api": "studywadiapi.classx.co.in"
    },
    {
        "name": "Studyway",
        "api": "studywayapi.classx.co.in"
    },
    {
        "name": "Studywithbhai",
        "api": "mathswithsumitbhaiapi.classx.co.in"
    },
    {
        "name": "Studywithdedicationswd",
        "api": "studywithdedicationapi.classx.co.in"
    },
    {
        "name": "Studywithiclm",
        "api": "studyiclmapi.classx.co.in"
    },
    {
        "name": "Studywithjs",
        "api": "studywithjsapi.classx.co.in"
    },
    {
        "name": "Studywithmanita",
        "api": "studymanitaapi.classx.co.in"
    },
    {
        "name": "Studywithmk",
        "api": "studymkapi.classx.co.in"
    },
    {
        "name": "Studywithritesh",
        "api": "studyriteshapi.classx.co.in"
    },
    {
        "name": "Studywithsmriti",
        "api": "studysmritiapi.classx.co.in"
    },
    {
        "name": "Successacademyjamkhandi",
        "api": "successacademyjamkhandiapi.classx.co.in"
    },
    {
        "name": "Successcareer",
        "api": "successcareerapi.classx.co.in"
    },
    {
        "name": "Successcentresikar",
        "api": "successcentresikarapi.classx.co.in"
    },
    {
        "name": "Successforum",
        "api": "successforumapi.classx.co.in"
    },
    {
        "name": "Successgyanclasses",
        "api": "successgyanclassesapi.classx.co.in"
    },
    {
        "name": "Successicon",
        "api": "successiconapi.classx.co.in"
    },
    {
        "name": "Successmantrabydeepakrai",
        "api": "successmantraapi.classx.co.in"
    },
    {
        "name": "Successmathematics",
        "api": "successmathematicsapi.classx.co.in"
    },
    {
        "name": "Successplanet20",
        "api": "successplanet20api.classx.co.in"
    },
    {
        "name": "Successpoint",
        "api": "successpointapi.classx.co.in"
    },
    {
        "name": "Successseries",
        "api": "successseriesmumbaiapi.classx.co.in"
    },
    {
        "name": "Successseries",
        "api": "successseriesapi.classx.co.in"
    },
    {
        "name": "Successsquare",
        "api": "successsquareapi.classx.co.in"
    },
    {
        "name": "Successstenotyping",
        "api": "successstenotypingapi.classx.co.in"
    },
    {
        "name": "Sumitacademy",
        "api": "sumitacademyapi.classx.co.in"
    },
    {
        "name": "Sumitjhambclasses",
        "api": "sumitjhambclassesapi.classx.co.in"
    },
    {
        "name": "Sumitsirclasseslive",
        "api": "sumitsirclassesapi.classx.co.in"
    },
    {
        "name": "Sunlight",
        "api": "sunlightapi.classx.co.in"
    },
    {
        "name": "Sunyapcs",
        "api": "sunyapcsapi.classx.co.in"
    },
    {
        "name": "Supercenturyacademy",
        "api": "supercenturyacademyapi.classx.co.in"
    },
    {
        "name": "Superclimaxacademysca",
        "api": "superclimaxacademyapi.classx.co.in"
    },
    {
        "name": "Supernotes",
        "api": "supernotesapi.classx.co.in"
    },
    {
        "name": "Sureias",
        "api": "sureiasapi.classx.co.in"
    },
    {
        "name": "Sureshbabusir",
        "api": "sureshbabusirapi.classx.co.in"
    },
    {
        "name": "Sureshbanking20",
        "api": "sureshbankingapi.classx.co.in"
    },
    {
        "name": "Sureshsirclasses",
        "api": "sureshsirclassesapi.classx.co.in"
    },
    {
        "name": "Sureshsirscompetitiveclasses",
        "api": "sureshsirscompetitiveclassesapi.classx.co.in"
    },
    {
        "name": "Surgerydada",
        "api": "surgerydadaapi.classx.co.in"
    },
    {
        "name": "Suryainstitute",
        "api": "suryainstituteapi.classx.co.in"
    },
    {
        "name": "Suryanagriuniquelawclasses",
        "api": "suryanagriuniquelawclassesapi.classx.co.in"
    },
    {
        "name": "Suryaschool",
        "api": "suryaschoolapi.classx.co.in"
    },
    {
        "name": "Suryavanshamgurukul",
        "api": "suryavanshamgurukulapi.classx.co.in"
    },
    {
        "name": "Sushenmaharajnaikawade",
        "api": "sushenmaharajnaikawadeapi.classx.co.in"
    },
    {
        "name": "Svijharkhand",
        "api": "svijharkhandapi.classx.co.in"
    },
    {
        "name": "Swadhyayacademy",
        "api": "swadhyayacademyapi.classx.co.in"
    },
    {
        "name": "Swadhyayprabodhini",
        "api": "swadhyayprabodhiniapi.classx.co.in"
    },
    {
        "name": "Swaeducation",
        "api": "swaeducationapi.classx.co.in"
    },
    {
        "name": "Swaminathanagriinstitute",
        "api": "swaminathanagriinstitutejaipurapi.classx.co.in"
    },
    {
        "name": "Swamivivekanandainschool",
        "api": "swamivivekanandainternationalschoolapi.classx.co.in"
    },
    {
        "name": "Swamivivekanandinstitute",
        "api": "swamivivekanandinstituteapi.classx.co.in"
    },
    {
        "name": "Swapnastudies",
        "api": "swapnastudiesapi.classx.co.in"
    },
    {
        "name": "Swarajyaacademyomsir",
        "api": "swarajyaacademyomsirapi.classx.co.in"
    },
    {
        "name": "Swarajyacareeracademy",
        "api": "swarajyacareeracademyapi.classx.co.in"
    },
    {
        "name": "Swastikclasses",
        "api": "swastikclassesapi.classx.co.in"
    },
    {
        "name": "Taksh",
        "api": "takshappapi.classx.co.in"
    },
    {
        "name": "Talent",
        "api": "talentplusapi.classx.co.in"
    },
    {
        "name": "Talentacademyliscentre",
        "api": "talentacademyliscentreapi.classx.co.in"
    },
    {
        "name": "Tallyclass",
        "api": "tallyclassapi.classx.co.in"
    },
    {
        "name": "Tamilsolaiacademy",
        "api": "tamilsolaiacademyapi.classx.co.in"
    },
    {
        "name": "Tandavclasses",
        "api": "tandavclassesapi.classx.co.in"
    },
    {
        "name": "Tapasyapcs",
        "api": "tapasyapcsapi.classx.co.in"
    },
    {
        "name": "Targetcombine",
        "api": "targetcombineapi.classx.co.in"
    },
    {
        "name": "Targetdefenceacademy",
        "api": "targetdefenceacademyapi.classx.co.in"
    },
    {
        "name": "Targetforiq",
        "api": "targetforiqapi.classx.co.in"
    },
    {
        "name": "Targetgpat",
        "api": "targetgpatapi.classx.co.in"
    },
    {
        "name": "Targetgurukul",
        "api": "targetgurukulapi.classx.co.in"
    },
    {
        "name": "Targetplus",
        "api": "targetplusapi.classx.co.in"
    },
    {
        "name": "Targetsarkarinaukari",
        "api": "targetsarkarinaukriapi.classx.co.in"
    },
    {
        "name": "Targetstudyiq",
        "api": "targetstudyiqapi.classx.co.in"
    },
    {
        "name": "Targetupsc",
        "api": "targetupscapi.classx.co.in"
    },
    {
        "name": "Targetwill",
        "api": "targetwillapi.classx.co.in"
    },
    {
        "name": "Targetwithajaysir",
        "api": "targetwithajaysirapi.classx.co.in"
    },
    {
        "name": "Targetwithankit",
        "api": "targetwithankitapi.classx.co.in"
    },
    {
        "name": "Targetwithbhavikmaru",
        "api": "targetbhavikmaruapi.classx.co.in"
    },
    {
        "name": "Targetwithbhavikmarunew",
        "api": "targetwithbhavikmaruapi.classx.co.in"
    },
    {
        "name": "Tathagatgsprep",
        "api": "tathagatgsprepapi.classx.co.in"
    },
    {
        "name": "Tcsexam",
        "api": "tcsexamzoneapi.classx.co.in"
    },
    {
        "name": "Teacheracademy",
        "api": "teacheracademyapi.classx.co.in"
    },
    {
        "name": "Teachersacademykng",
        "api": "teachersacademykngapi.classx.co.in"
    },
    {
        "name": "Teachersachievers",
        "api": "teachersachieversapi.classx.co.in"
    },
    {
        "name": "Teacherselectacademy",
        "api": "teacherselectacademyapi.classx.co.in"
    },
    {
        "name": "Teachersexpressofficial",
        "api": "teachersexpressofficialapi.classx.co.in"
    },
    {
        "name": "Teachersgurukul",
        "api": "teachersgurukulapi.classx.co.in"
    },
    {
        "name": "Teachersmantra",
        "api": "teachersmantraapi.classx.co.in"
    },
    {
        "name": "Teachersway",
        "api": "teacherswayapi.classx.co.in"
    },
    {
        "name": "Teachextra",
        "api": "teachextraapi.classx.co.in"
    },
    {
        "name": "Teachingoriented",
        "api": "teachingorientedapi.classx.co.in"
    },
    {
        "name": "Teachingpariksha",
        "api": "teachingparikshaapi.classx.co.in"
    },
    {
        "name": "Techcapsule",
        "api": "techcapsuleapi.classx.co.in"
    },
    {
        "name": "Techelitelive",
        "api": "techeliteliveapi.classx.co.in"
    },
    {
        "name": "Techhubclasses",
        "api": "techhubclassesapi.classx.co.in"
    },
    {
        "name": "Techiesms",
        "api": "techiesmsapi.classx.co.in"
    },
    {
        "name": "Techmechanicalelectrical",
        "api": "techmechanicalelectricalapi.classx.co.in"
    },
    {
        "name": "Technicaljobgyan",
        "api": "technicaljobgyanapi.classx.co.in"
    },
    {
        "name": "Technogateeducation",
        "api": "technogateeducationapi.classx.co.in"
    },
    {
        "name": "Techstudyiti",
        "api": "techstudyitiapi.classx.co.in"
    },
    {
        "name": "Techtech",
        "api": "techtechapi.classx.co.in"
    },
    {
        "name": "Teejanshpathshala",
        "api": "teejanshpathshalaapi.classx.co.in"
    },
    {
        "name": "Tegonity",
        "api": "tegonityapi.classx.co.in"
    },
    {
        "name": "Tejaswigovernmentexams",
        "api": "tejaswigovernmentexamsapi.classx.co.in"
    },
    {
        "name": "Telugurailways",
        "api": "telugurailwaysapi.classx.co.in"
    },
    {
        "name": "Tempdb",
        "api": "tempapi.classx.co.in"
    },
    {
        "name": "Test247",
        "api": "test247api.classx.co.in"
    },
    {
        "name": "Testcreds",
        "api": "testcredsapi.classx.co.in"
    },
    {
        "name": "Testfactory",
        "api": "testfactoryapi.classx.co.in"
    },
    {
        "name": "Testingmigration",
        "api": "testingmigrationapi.classx.co.in"
    },
    {
        "name": "Testpaper",
        "api": "testpaperapi.classx.co.in"
    },
    {
        "name": "Testpass",
        "api": "thetestpassapi.classx.co.in"
    },
    {
        "name": "Testplace",
        "api": "testplaceapi.classx.co.in"
    },
    {
        "name": "Testprep",
        "api": "thetestprepapi.classx.co.in"
    },
    {
        "name": "Testpur",
        "api": "testpurapi.classx.co.in"
    },
    {
        "name": "Testwala",
        "api": "testwalaapi.classx.co.in"
    },
    {
        "name": "Testyourtaiyarimind4Academy",
        "api": "testyourtaiyariapi.classx.co.in"
    },
    {
        "name": "Tharunspeaks",
        "api": "tharunspeaksapi.classx.co.in"
    },
    {
        "name": "Theachievesmentorship",
        "api": "theachievesmentorshipapi.classx.co.in"
    },
    {
        "name": "Theakacademy",
        "api": "akacademyapi.classx.co.in"
    },
    {
        "name": "Theananteducation",
        "api": "ananteducationapi.classx.co.in"
    },
    {
        "name": "Theapronboy",
        "api": "apronboyapi.classx.co.in"
    },
    {
        "name": "Thearmyboy",
        "api": "thearmyboyapi.classx.co.in"
    },
    {
        "name": "Theboardsacademy",
        "api": "theboardsacademyapi.classx.co.in"
    },
    {
        "name": "Thecivilindiaofficial",
        "api": "civilindiaofficialapi.classx.co.in"
    },
    {
        "name": "Thecivilsclub",
        "api": "civilsclubapi.classx.co.in"
    },
    {
        "name": "Thecoach",
        "api": "thecoachapi.classx.co.in"
    },
    {
        "name": "Thecodeskool",
        "api": "thecodeskoolapi.classx.co.in"
    },
    {
        "name": "Thecodingbus",
        "api": "codingbusapi.classx.co.in"
    },
    {
        "name": "Theconceptualias",
        "api": "theconceptualiasapi.classx.co.in"
    },
    {
        "name": "Thecoreacademy",
        "api": "coreacademyapi.classx.co.in"
    },
    {
        "name": "Thedepartment",
        "api": "thedepartmentapi.classx.co.in"
    },
    {
        "name": "Theeducationadda",
        "api": "educationaddaapi.classx.co.in"
    },
    {
        "name": "Thegrmacademy",
        "api": "grmacademyapi.classx.co.in"
    },
    {
        "name": "Thehistoricaias",
        "api": "historicaiasapi.classx.co.in"
    },
    {
        "name": "Theimaiasras",
        "api": "imaiasrasapi.classx.co.in"
    },
    {
        "name": "Thekpsharmaexamsprep",
        "api": "kpsharmaexamsprepapi.classx.co.in"
    },
    {
        "name": "Thelastexam",
        "api": "lastexamapi.teachx.in"
    },
    {
        "name": "Thelifistudy",
        "api": "lifistudyapi.classx.co.in"
    },
    {
        "name": "Thelionacademy",
        "api": "lionacademyapi.classx.co.in"
    },
    {
        "name": "Thelyceum",
        "api": "lyceumapi.classx.co.in"
    },
    {
        "name": "Themathscafe",
        "api": "mathscafeapi.classx.co.in"
    },
    {
        "name": "Thembbsplanet",
        "api": "mbbsplanetapi.classx.co.in"
    },
    {
        "name": "Thementors",
        "api": "thementorsapi.classx.co.in"
    },
    {
        "name": "Themotionclasses",
        "api": "themotionclassesapi.classx.co.in"
    },
    {
        "name": "Thenayakacademyamravati",
        "api": "nayakacademyamravatiapi.classx.co.in"
    },
    {
        "name": "Thenpibuxar",
        "api": "npibuxarapi.classx.co.in"
    },
    {
        "name": "Theofficersacadem",
        "api": "theofficersacademyapi.classx.co.in"
    },
    {
        "name": "Theofficersacademy",
        "api": "theofficersacademyapi.appx.co.in"
    },
    {
        "name": "Theoryofphysics",
        "api": "theoryphysicsapi.classx.co.in"
    },
    {
        "name": "Theparikshanitiacademy",
        "api": "parikshanitiacademyapi.classx.co.in"
    },
    {
        "name": "Thephidiasacademy",
        "api": "phidiasacademyapi.classx.co.in"
    },
    {
        "name": "Thephoenixacademypune",
        "api": "phoenixacademypuneapi.classx.co.in"
    },
    {
        "name": "Theplatform",
        "api": "platformapi.classx.co.in"
    },
    {
        "name": "Theplatform2O",
        "api": "theplatformapi.classx.co.in"
    },
    {
        "name": "Thepremieracademy",
        "api": "thepremieracademyapi.classx.co.in"
    },
    {
        "name": "Theprimeacademy",
        "api": "theprimeacademyapi.classx.co.in"
    },
    {
        "name": "Therasayanam",
        "api": "therasayanamapi.classx.co.in"
    },
    {
        "name": "Thesamarthacademy",
        "api": "thesamarthacademyapi.classx.co.in"
    },
    {
        "name": "Theschooleducationadda",
        "api": "schooleducationaddaapi.classx.co.in"
    },
    {
        "name": "Thesciencelaserbysumitshukla",
        "api": "sciencelasersumitshuklaapi.classx.co.in"
    },
    {
        "name": "Theselectionguru",
        "api": "theselectionguruapi.classx.co.in"
    },
    {
        "name": "Thesmartstudy",
        "api": "thesmartstudyapi.classx.co.in"
    },
    {
        "name": "Thespeed",
        "api": "speedcoachingapi.teachx.in"
    },
    {
        "name": "Thespeedcoaching",
        "api": "speedcoachingapi.classx.co.in"
    },
    {
        "name": "Thestudyline",
        "api": "thestudylineapi.classx.co.in"
    },
    {
        "name": "Thetargetdreamitchaseit",
        "api": "thetargetapi.classx.co.in"
    },
    {
        "name": "Theteacher",
        "api": "theteacherapi.classx.co.in"
    },
    {
        "name": "Thevectoracademy",
        "api": "vectoracademyapi.classx.co.in"
    },
    {
        "name": "Thevijeeshacademy",
        "api": "vijeeshacademyapi.classx.co.in"
    },
    {
        "name": "Thewinnersacademy",
        "api": "thewinnersacademyapi.classx.co.in"
    },
    {
        "name": "Thinkias",
        "api": "thinkiasapi.classx.co.in"
    },
    {
        "name": "Thinkssc",
        "api": "thinksscapi.classx.co.in"
    },
    {
        "name": "Tikkarmarathi",
        "api": "tikkarmarathiapi.classx.co.in"
    },
    {
        "name": "Timeforgreatness",
        "api": "timegreatnessapi.classx.co.in"
    },
    {
        "name": "Timelineeducation",
        "api": "timelineeducationapi.classx.co.in"
    },
    {
        "name": "Tirupatiiasbhopal",
        "api": "tirupatiiasbhopalapi.classx.co.in"
    },
    {
        "name": "Tiwaricampus",
        "api": "tiwaricampusapi.classx.co.in"
    },
    {
        "name": "Tkpacademy",
        "api": "tkpacademyapi.classx.co.in"
    },
    {
        "name": "Tnacademylearningapp",
        "api": "tnacademylearningapi.classx.co.in"
    },
    {
        "name": "Tnicollegeofcompetitions",
        "api": "tnicollegecompetitionsapi.classx.co.in"
    },
    {
        "name": "Toc",
        "api": "toclearningapi.teachx.in"
    },
    {
        "name": "Toclearningapp",
        "api": "toclearningapi.classx.co.in"
    },
    {
        "name": "Toothpracto",
        "api": "toothpractoapi.classx.co.in"
    },
    {
        "name": "Toppers24",
        "api": "toppers24inapi.classx.co.in"
    },
    {
        "name": "Toppersadda",
        "api": "studymateapi.classx.co.in"
    },
    {
        "name": "Toppersinitiative",
        "api": "toppersinitiativeapi.classx.co.in"
    },
    {
        "name": "Topperstest",
        "api": "topperstestapi.classx.co.in"
    },
    {
        "name": "Toppertemple",
        "api": "toppertempleapi.classx.co.in"
    },
    {
        "name": "Topsthan",
        "api": "topsthanapi.classx.co.in"
    },
    {
        "name": "Toptak",
        "api": "rahuldeshwalacademyapi.appx.co.in"
    },
    {
        "name": "Totallearning",
        "api": "totallearningapi.classx.co.in"
    },
    {
        "name": "Tradingkulture",
        "api": "tradingkultureapi.classx.co.in"
    },
    {
        "name": "Trendtutor",
        "api": "trendtutorapi.classx.co.in"
    },
    {
        "name": "Trickyacademyno1",
        "api": "trickyacademyno1api.classx.co.in"
    },
    {
        "name": "Trinetraias",
        "api": "trinetraiasapi.classx.co.in"
    },
    {
        "name": "Trinity",
        "api": "trinityapi.classx.co.in"
    },
    {
        "name": "Tripbohemia",
        "api": "tripbohemiaapi.classx.co.in"
    },
    {
        "name": "Triplingphysic",
        "api": "triplingphysicsapi.classx.co.in"
    },
    {
        "name": "Trishakti",
        "api": "trishaktiapi.classx.co.in"
    },
    {
        "name": "Trueiq",
        "api": "trueiqapi.classx.co.in"
    },
    {
        "name": "Tsbaditetdsc",
        "api": "tsbaditetdscapi.classx.co.in"
    },
    {
        "name": "Tsironlineclasses",
        "api": "tsironlineclassesapi.classx.co.in"
    },
    {
        "name": "Tslnursingcoaching",
        "api": "tslnursingcoachingapi.classx.co.in"
    },
    {
        "name": "Tubeenglish",
        "api": "tubeenglishapi.classx.co.in"
    },
    {
        "name": "Tuitiongharofficial",
        "api": "tuitiongharofficialapi.classx.co.in"
    },
    {
        "name": "Turningpointvijayamcompetitiveexams",
        "api": "turningpointapi.classx.co.in"
    },
    {
        "name": "Tutoralearningapp",
        "api": "tutoralearningappapi.classx.co.in"
    },
    {
        "name": "Tutorizeacademy",
        "api": "tutorizeacademyapi.classx.co.in"
    },
    {
        "name": "Tutorsadda",
        "api": "tutorsaddaapi.classx.co.in"
    },
    {
        "name": "Tutosadda",
        "api": "tutorsaddaapi.teachx.in"
    },
    {
        "name": "Twelthplus",
        "api": "plus12thapi.classx.co.in"
    },
    {
        "name": "Twelveminutestoclat",
        "api": "minutes12toclatapi.classx.co.in"
    },
    {
        "name": "Twentyfourhrsstudycentre",
        "api": "24hrsstudycentreapi.classx.co.in"
    },
    {
        "name": "Twsacademy",
        "api": "twsacademyapi.classx.co.in"
    },
    {
        "name": "Uascareerinstitute",
        "api": "uascareerinstituteapi.classx.co.in"
    },
    {
        "name": "Ucananenglishacademy",
        "api": "ucanenglishacademyapi.classx.co.in"
    },
    {
        "name": "Uclive",
        "api": "ucliveapi.classx.co.in"
    },
    {
        "name": "Udaaninstitute",
        "api": "udaaninstituteapi.classx.co.in"
    },
    {
        "name": "Udaaninstituteofexcellence",
        "api": "udaaninstituteexcellencenandedapi.classx.co.in"
    },
    {
        "name": "Udaicareeracademy",
        "api": "udaicareeracademyapi.classx.co.in"
    },
    {
        "name": "Udaipurclasses",
        "api": "udaipurclassesapi.classx.co.in"
    },
    {
        "name": "Udaykadamsmarathiacademy",
        "api": "udaykadamsmarathiacademyapi.classx.co.in"
    },
    {
        "name": "Udbhavaacademy",
        "api": "udbhavaacademyapi.classx.co.in"
    },
    {
        "name": "Ufjapp",
        "api": "ufjappapi.classx.co.in"
    },
    {
        "name": "Ujjwalclasses",
        "api": "ujjwalclassesapi.classx.co.in"
    },
    {
        "name": "Ujjwalclassesrajasthan",
        "api": "ujjwalclassesrajasthanapi.classx.co.in"
    },
    {
        "name": "Umaiiasacademy",
        "api": "umaiiasacademyapi.classx.co.in"
    },
    {
        "name": "Umangcareeracademy",
        "api": "umangcareeracademyapi.classx.co.in"
    },
    {
        "name": "Umangstudy",
        "api": "umangstudyapi.classx.co.in"
    },
    {
        "name": "Umaudaanmasteracademy",
        "api": "umaudaanmasteracademyapi.classx.co.in"
    },
    {
        "name": "Umediasacademy",
        "api": "umediasacademyapi.classx.co.in"
    },
    {
        "name": "Umedmpsc",
        "api": "umedmpscapi.classx.co.in"
    },
    {
        "name": "Umeshsharmaacademy",
        "api": "umeshsharmaacademyapi.classx.co.in"
    },
    {
        "name": "Uniexamsshiksha",
        "api": "uniexamsshikshaapi.classx.co.in"
    },
    {
        "name": "Unifoxconnected",
        "api": "unifoxconnectedapi.classx.co.in"
    },
    {
        "name": "Unifystudy",
        "api": "unifystudyapi.classx.co.in"
    },
    {
        "name": "Uniqueacademy",
        "api": "uniqueacademyapi.classx.co.in"
    },
    {
        "name": "Uniquecivil",
        "api": "uniquecivilapi.classx.co.in"
    },
    {
        "name": "Uniquegyanofficial",
        "api": "uniquegyanofficialapi.classx.co.in"
    },
    {
        "name": "Uniqueonlineclasses",
        "api": "uniqueonlineclassesapi.classx.co.in"
    },
    {
        "name": "Uniquephysics",
        "api": "uniquephysicsapi.classx.co.in"
    },
    {
        "name": "Uniquescienceacademy",
        "api": "uniquescienceacademyapi.classx.co.in"
    },
    {
        "name": "Unnatieducation",
        "api": "unnatieducationapi.classx.co.in"
    },
    {
        "name": "Unskillseducationlearnskill",
        "api": "unskillseducationlearnskillapi.classx.co.in"
    },
    {
        "name": "Upastapanainsititute",
        "api": "upastapanainsitituteapi.classx.co.in"
    },
    {
        "name": "Upclassesprayagraj",
        "api": "upclassesprayagrajapi.classx.co.in"
    },
    {
        "name": "Upgradeeducationofficial",
        "api": "upgradeeducationapi.classx.co.in"
    },
    {
        "name": "Upscalecode",
        "api": "upscalecodeapi.classx.co.in"
    },
    {
        "name": "Upsckaadda",
        "api": "upsckaaddaapi.classx.co.in"
    },
    {
        "name": "Upsckit",
        "api": "upsckitapi.classx.co.in"
    },
    {
        "name": "Upscmitra",
        "api": "upscmitraapi.classx.co.in"
    },
    {
        "name": "Upscsupersimplified",
        "api": "upscsupersimplifiedapi.classx.co.in"
    },
    {
        "name": "Upscvidyalaya",
        "api": "upscvidyalayaapi.classx.co.in"
    },
    {
        "name": "Urdubyirfan",
        "api": "urdubyirfanapi.classx.co.in"
    },
    {
        "name": "Utkarshclasses",
        "api": "utkarshclassesapi.classx.co.in"
    },
    {
        "name": "Uttamsacademy2",
        "api": "uttamsacademy2api.classx.co.in"
    },
    {
        "name": "Vaijanathdhendulesacademy",
        "api": "vaijanathdhendulesacademyapi.classx.co.in"
    },
    {
        "name": "Vaishnaviharkirat",
        "api": "vyshnaviapi.classx.co.in"
    },
    {
        "name": "Vajacademy",
        "api": "vajacademyapi.classx.co.in"
    },
    {
        "name": "Vakeelacademy",
        "api": "vakeelacademyapi.classx.co.in"
    },
    {
        "name": "Vamjaeducation",
        "api": "vamjaeducationapi.classx.co.in"
    },
    {
        "name": "Varunawasthi",
        "api": "examenginevarunawasthiapi.classx.co.in"
    },
    {
        "name": "Vasuconcept",
        "api": "vasuconceptapi.classx.co.in"
    },
    {
        "name": "Vaticaninstitute",
        "api": "vaticaninstituteapi.classx.co.in"
    },
    {
        "name": "Vcan24",
        "api": "vcan24api.classx.co.in"
    },
    {
        "name": "Vconlineclasses",
        "api": "vconlineclassesapi.classx.co.in"
    },
    {
        "name": "Vdemy",
        "api": "vdemyapi.classx.co.in"
    },
    {
        "name": "Vedakshiclasses",
        "api": "vedakshiclassesapi.classx.co.in"
    },
    {
        "name": "Vedamclassesstudyguardian",
        "api": "vedamclassesapi.classx.co.in"
    },
    {
        "name": "Vedanteducation",
        "api": "vedanteducationapi.classx.co.in"
    },
    {
        "name": "Vedantgurukul",
        "api": "vedantgurukulapi.classx.co.in"
    },
    {
        "name": "Vedantstudy",
        "api": "vedantstudyapi.classx.co.in"
    },
    {
        "name": "Veddigitaleducation",
        "api": "veddigitaleducationapi.classx.co.in"
    },
    {
        "name": "Vedicias",
        "api": "vediciasapi.classx.co.in"
    },
    {
        "name": "Vedpathshala",
        "api": "vedpathshalaapi.classx.co.in"
    },
    {
        "name": "Vedprep",
        "api": "vedprepapi.classx.co.in"
    },
    {
        "name": "Veertejango",
        "api": "veertejangoapi.classx.co.in"
    },
    {
        "name": "Venkatagirienglish",
        "api": "venkatagirienglishapi.classx.co.in"
    },
    {
        "name": "Venusshorthandclasses",
        "api": "venusshorthandclassesapi.classx.co.in"
    },
    {
        "name": "Verbalistlearning",
        "api": "verbalistlearningapi.classx.co.in"
    },
    {
        "name": "Veteran",
        "api": "veteranapi.classx.co.in"
    },
    {
        "name": "Vfirst",
        "api": "vfirstapi.classx.co.in"
    },
    {
        "name": "Vibrantelearning",
        "api": "vibrantelearningapi.classx.co.in"
    },
    {
        "name": "Vicsindore",
        "api": "vicsindoreapi.classx.co.in"
    },
    {
        "name": "Vidhanlawclasses",
        "api": "vidhanlawclassesapi.classx.co.in"
    },
    {
        "name": "Vidhigurukul",
        "api": "vidhigurukulapi.classx.co.in"
    },
    {
        "name": "Vidhyaagricultureacademy",
        "api": "vidhyaagricultureacademykanpurapi.classx.co.in"
    },
    {
        "name": "Vidhyakendra",
        "api": "vidhyakendraapi.classx.co.in"
    },
    {
        "name": "Vidwancompetition",
        "api": "vidwancompetitionapi.classx.co.in"
    },
    {
        "name": "Vidyabihar",
        "api": "vidyabiharapi.teachx.in"
    },
    {
        "name": "Vidyabihar",
        "api": "vidyabiharapi.classx.co.in"
    },
    {
        "name": "Vidyadarpan",
        "api": "vidyadarpanapi.classx.co.in"
    },
    {
        "name": "Vidyaguruschoolprep",
        "api": "vidyaguruschoolprepapi.classx.co.in"
    },
    {
        "name": "Vidyanjalipoint",
        "api": "vidyanjalipointapi.classx.co.in"
    },
    {
        "name": "Vidyapeethrajasthan",
        "api": "vidyapeethrajasthanapi.classx.co.in"
    },
    {
        "name": "Vidyapower",
        "api": "vidyapowerapi.classx.co.in"
    },
    {
        "name": "Vidyasagaracademypune",
        "api": "vidyasagaracademypuneapi.classx.co.in"
    },
    {
        "name": "Vidyashreemanthan",
        "api": "vidyashreemanthanapi.classx.co.in"
    },
    {
        "name": "Vigyanvriksha",
        "api": "vigyanvrikshaapi.classx.co.in"
    },
    {
        "name": "Vijayacademy",
        "api": "vijayacademyapi.classx.co.in"
    },
    {
        "name": "Vijayacademyindore",
        "api": "vijayacademyindoreapi.classx.co.in"
    },
    {
        "name": "Vijayclasses",
        "api": "vijayclassesapi.classx.co.in"
    },
    {
        "name": "Vijaykantsirofficial",
        "api": "vijaykantsirofficialapi.classx.co.in"
    },
    {
        "name": "Vijaypathacademy",
        "api": "vijaypathacademyapi.classx.co.in"
    },
    {
        "name": "Vijaypathdefence",
        "api": "vijaypathdefenceapi.classx.co.in"
    },
    {
        "name": "Vijendrasirstudyhub",
        "api": "vijendrasirstudyhubapi.classx.co.in"
    },
    {
        "name": "Vikalpkotwal",
        "api": "vikalpkotwalapi.classx.co.in"
    },
    {
        "name": "Vikascoaching",
        "api": "vikascoachingapi.classx.co.in"
    },
    {
        "name": "Vikasshuklaenglish",
        "api": "vikasshuklaenglishapi.classx.co.in"
    },
    {
        "name": "Vineettutorials",
        "api": "vineettutorialsapi.classx.co.in"
    },
    {
        "name": "Vipgurugofficial",
        "api": "vipgurugofficialapi.classx.co.in"
    },
    {
        "name": "Virajnationalacademy",
        "api": "virajnationalapi.classx.co.in"
    },
    {
        "name": "Vishalkhodifad",
        "api": "vishalkhodifadapi.classx.co.in"
    },
    {
        "name": "Vishwamarathi",
        "api": "vishwamarathiapi.classx.co.in"
    },
    {
        "name": "Vishwasacademy",
        "api": "vishwasacademyapi.classx.co.in"
    },
    {
        "name": "Visionacademyofficial",
        "api": "visionacademyofficialapi.classx.co.in"
    },
    {
        "name": "Visioncoachingclassesakole",
        "api": "visioncoachingclassesakoleapi.classx.co.in"
    },
    {
        "name": "Visionkhaki",
        "api": "visionkhakiapi.classx.co.in"
    },
    {
        "name": "Visionscience",
        "api": "visionscienceapi.classx.co.in"
    },
    {
        "name": "Visionupdate",
        "api": "visionupdateapi.classx.co.in"
    },
    {
        "name": "Visionupsc",
        "api": "visionupscapi.classx.co.in"
    },
    {
        "name": "Vitaneducation",
        "api": "vitaneducationapi.classx.co.in"
    },
    {
        "name": "Vitthalkangane",
        "api": "vitthalkanganeapi.classx.co.in"
    },
    {
        "name": "Vivanta",
        "api": "vivantaapi.classx.co.in"
    },
    {
        "name": "Vivekanandlearningappvla",
        "api": "vivekanandlearningappapi.classx.co.in"
    },
    {
        "name": "Vivekanandpublicintercollege",
        "api": "vivekanandpublicintercollegeapi.classx.co.in"
    },
    {
        "name": "Vivekpawaracademy",
        "api": "vivekacademyapi.classx.co.in"
    },
    {
        "name": "Vj",
        "api": "vjeducationapi.appx.co.in"
    },
    {
        "name": "Vjeducvation",
        "api": "vjeducationapi.classx.co.in"
    },
    {
        "name": "Vlrtraining",
        "api": "vlrtrainingapi.classx.co.in"
    },
    {
        "name": "Vmrlogics",
        "api": "vmrlogicsapi.classx.co.in"
    },
    {
        "name": "Vnrclasses",
        "api": "vnrclassesapi.classx.co.in"
    },
    {
        "name": "Voraclasses",
        "api": "voraclassesapi.classx.co.in"
    },
    {
        "name": "Vseducationofficial",
        "api": "vseducationapi.classx.co.in"
    },
    {
        "name": "Vsmpscacademy",
        "api": "vsmpscacademyapi.classx.co.in"
    },
    {
        "name": "Vvsias",
        "api": "vvsiasapi.classx.co.in"
    },
    {
        "name": "Warriorofficer",
        "api": "warriorofficerapi.classx.co.in"
    },
    {
        "name": "Wealthsagalearn",
        "api": "wealthsagalearnapi.classx.co.in"
    },
    {
        "name": "Webcityitgk",
        "api": "webcityitgkapi.classx.co.in"
    },
    {
        "name": "Webdemybysaunaksir",
        "api": "webdemysaunaksirapi.classx.co.in"
    },
    {
        "name": "Webinar",
        "api": "webinarapi.classx.co.in"
    },
    {
        "name": "Websankulcivilengineering",
        "api": "websankulcivilengineeringapi.classx.co.in"
    },
    {
        "name": "Websankullive",
        "api": "websankulliveapi.classx.co.in"
    },
    {
        "name": "Wewonacademy",
        "api": "wewonacademyapi.classx.co.in"
    },
    {
        "name": "Whatzbehind",
        "api": "whatzbehindapi.classx.co.in"
    },
    {
        "name": "Whiteboardacademy",
        "api": "whiteboardacademyapi.classx.co.in"
    },
    {
        "name": "Wingsekudaan",
        "api": "wingsekudaanapi.classx.co.in"
    },
    {
        "name": "Winias",
        "api": "winiasapi.classx.co.in"
    },
    {
        "name": "Winnerhubclasses",
        "api": "winnerhubclassesapi.classx.co.in"
    },
    {
        "name": "Winners",
        "api": "winnersinstituteapi.classx.co.in"
    },
    {
        "name": "Winnersclasses",
        "api": "winnersclassesapi.classx.co.in"
    },
    {
        "name": "Winnerspublications",
        "api": "winnerspublicationsapi.classx.co.in"
    },
    {
        "name": "Winnerstest",
        "api": "winnerstestapi.classx.co.in"
    },
    {
        "name": "Winnersworld",
        "api": "winnersworldapi.classx.co.in"
    },
    {
        "name": "Winningways",
        "api": "winningwaysapi.classx.co.in"
    },
    {
        "name": "Winrrb",
        "api": "winrrbapi.classx.co.in"
    },
    {
        "name": "Xambites",
        "api": "xambitesapi.classx.co.in"
    },
    {
        "name": "Xploreacademy",
        "api": "xploracademyapi.classx.co.in"
    },
    {
        "name": "Yashadaacademypune",
        "api": "yashadaacademypuneapi.classx.co.in"
    },
    {
        "name": "Yashashriiacademy",
        "api": "yashashriiacademyapi.classx.co.in"
    },
    {
        "name": "Yashmaheshwari",
        "api": "yashmaheshwariapi.classx.co.in"
    },
    {
        "name": "Yashpatelknowledge",
        "api": "yashpatelknowledgeapi.classx.co.in"
    },
    {
        "name": "Yashwantacademypune",
        "api": "yashwantacademypuneapi.classx.co.in"
    },
    {
        "name": "Ybdacademy",
        "api": "ybdacademyapi.classx.co.in"
    },
    {
        "name": "Yctfastbook",
        "api": "yctfastbookapi.classx.co.in"
    },
    {
        "name": "Yesandyesexamsadda",
        "api": "yesexamsaddaapi.classx.co.in"
    },
    {
        "name": "Yescompetitiveexamslibrary",
        "api": "yescompetitiveexamslibraryapi.classx.co.in"
    },
    {
        "name": "Yesofficer",
        "api": "yesofficerapi.classx.co.in"
    },
    {
        "name": "Yespoliceacademy",
        "api": "yespoliceacademyapi.classx.co.in"
    },
    {
        "name": "Yodha",
        "api": "yodhaapi.classx.co.in"
    },
    {
        "name": "Yodhaapp",
        "api": "yodhaappapi.classx.co.in"
    },
    {
        "name": "Yogenderkadyansacademy",
        "api": "yogenderkadyanapi.classx.co.in"
    },
    {
        "name": "Yourstudy",
        "api": "yourstudyapi.classx.co.in"
    },
    {
        "name": "Yoursuccessmate",
        "api": "yoursuccessmateapi.classx.co.in"
    },
    {
        "name": "Yspliveclass",
        "api": "yspliveclassapi.classx.co.in"
    },
    {
        "name": "Yugandharacademy",
        "api": "yugandharacademyapi.classx.co.in"
    },
    {
        "name": "Yugantaracademyupsc",
        "api": "yugantaracademyapi.classx.co.in"
    },
    {
        "name": "Yuktipublication",
        "api": "yuktipublicationapi.classx.co.in"
    },
    {
        "name": "Yuvaiasacademyofficial",
        "api": "yuvaiasacademyofficialapi.classx.co.in"
    },
    {
        "name": "Yuvaupnishadfoundation",
        "api": "yuvaupnishadfoundationonlineapi.classx.co.in"
    },
    {
        "name": "Zidacademyhisar",
        "api": "zidacademyhisarapi.classx.co.in"
    },
    {
        "name": "Zinmatt",
        "api": "zinmattapi.classx.co.in"
    },
    {
        "name": "Zitaenglishacademy",
        "api": "zitaenglishacademyapi.classx.co.in"
    },
    {
        "name": "Zscore",
        "api": "zscoreapi.classx.co.in"
    }
]








PER_PAGE = 15

def get_AppxPage(page: int, appNameDict=a_to_zList, appx: bool = False):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE

    # ✅ Agar start >= len(keys), matlab ek bhi button bacha hi nahi
    if start >= len(keys):
        return InlineKeyboardMarkup([[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]])

    buttons = []

    # ✅ Fixed Appx button top pe har page par
    if appx:
        buttons.append([InlineKeyboardButton("🌿 Appx Manual", callback_data="appx_manual")])

    # Normal app buttons
    row = []
    for i, key in enumerate(keys[start:end], 1):
        row.append(InlineKeyboardButton(appNameDict[key]["name"], callback_data=key))
        if i % 3 == 0:  
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Navigation buttons
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("＜ ᴘʀᴇᴠ", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("↺ ʙ ᴀ ᴄ ᴋ ↻", callback_data="home_"))
    if end < len(keys):  
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ＞", callback_data=f"page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(buttons)
