"""
Hand-written travel guide content for 10 cities.

Each city has exactly 5 sections -> each section becomes one PDF page.
The text deliberately mentions links BETWEEN cities (trains, flights,
shared history) so that GraphRAG has interesting relationships to find.
"""

CITIES = {
    # ------------------------------------------------------------------ PARIS
    "Paris": {
        "country": "France",
        "tagline": "The City of Light on the River Seine",
        "sections": [
            ("Overview and History", [
                "Paris is the capital of France and sits on the River Seine in the north of the country. "
                "The city began as a settlement of a Celtic tribe called the Parisii, and after the Roman "
                "conquest it became the Roman town of Lutetia. Like London, Barcelona and Istanbul, Paris "
                "was once part of the Roman Empire, whose capital was Rome.",
                "During the Middle Ages Paris grew into one of the largest cities in Europe, and the Gothic "
                "cathedral of Notre-Dame was built on the Ile de la Cite. The French Revolution began here in "
                "1789 with the storming of the Bastille. In the nineteenth century Baron Haussmann redesigned "
                "the city with the wide boulevards and cream-coloured apartment buildings that visitors see today.",
                "Paris is nicknamed the City of Light because it was an early adopter of street lighting and a "
                "centre of the Enlightenment. Today it is famous for art, fashion, food and romance, and it hosted "
                "the Summer Olympic Games in 1900, 1924 and 2024. The city is divided into 20 numbered districts "
                "called arrondissements that spiral outwards from the centre like a snail shell.",
                "Paris has a special link with New York: the Statue of Liberty was a gift from France to the "
                "United States. It was designed by the French sculptor Frederic Auguste Bartholdi, and its internal "
                "iron framework was engineered by Gustave Eiffel, the same engineer whose company built the "
                "Eiffel Tower. A smaller replica of the statue stands on the Ile aux Cygnes in Paris.",
            ]),
            ("Top Attractions", [
                "The Eiffel Tower is the symbol of Paris. It was built by the company of Gustave Eiffel for the "
                "Exposition Universelle (World's Fair) of 1889 and is about 330 metres tall. Visitors can climb the "
                "stairs to the second floor or take lifts to the summit. The tower sparkles with lights for five "
                "minutes every hour after dark. The Tokyo Tower in Japan was later inspired by its design.",
                "The Louvre is the most visited museum in the world and a former royal palace. Its collection "
                "includes the Mona Lisa by Leonardo da Vinci, the Venus de Milo and the Winged Victory of "
                "Samothrace. The glass pyramid entrance was designed by the architect I. M. Pei and opened in 1989. "
                "The Louvre also lent its name to the Louvre Abu Dhabi near Dubai, which opened in 2017.",
                "Notre-Dame Cathedral was badly damaged by a fire in April 2019 and reopened to visitors in "
                "December 2024 after a huge restoration. The Musee d'Orsay, housed in a former railway station, "
                "holds the world's greatest collection of Impressionist art, including works by Monet, Renoir "
                "and Van Gogh.",
                "Other highlights include the Arc de Triomphe at the top of the Champs-Elysees, the white "
                "Sacre-Coeur Basilica on the hill of Montmartre, the stained glass of Sainte-Chapelle, and the "
                "Luxembourg Gardens. A boat cruise on the Seine is a relaxing way to see many monuments in one hour.",
            ]),
            ("Neighborhoods and Food", [
                "Le Marais is a historic district of narrow medieval streets, elegant mansions and the Place des "
                "Vosges, the oldest planned square in Paris. Rue des Rosiers in the Marais is famous for falafel. "
                "Montmartre, on a hill in the north, was home to artists such as Picasso and Van Gogh, and painters "
                "still work in the Place du Tertre.",
                "Saint-Germain-des-Pres on the Left Bank is known for literary cafes such as Cafe de Flore and "
                "Les Deux Magots, where writers like Jean-Paul Sartre and Simone de Beauvoir worked. The Latin "
                "Quarter, around the Sorbonne university, is lively with students, bookshops and cheap restaurants.",
                "French food is a highlight of any visit. Start the day with a buttery croissant or pain au chocolat "
                "and a cafe creme. Lunch might be a jambon-beurre sandwich on a fresh baguette, and dinner at a "
                "bistro could be steak frites, duck confit or French onion soup. Paris is also famous for crepes, "
                "cheese, and colourful macarons from patisseries such as Laduree and Pierre Herme.",
                "Food markets such as the Marche des Enfants Rouges, the oldest covered market in Paris, are great "
                "places for lunch. In France a service charge is included in restaurant bills ('service compris'), "
                "so tipping is optional; leaving small change for good service is appreciated.",
            ]),
            ("Getting Around and Practical Tips", [
                "The Paris Metro is one of the densest subway networks in the world, with 16 lines and over 300 "
                "stations, so almost every address is within a short walk of a station. A single Metro ticket costs "
                "around 2.50 euros, and visitors staying a week can buy a Navigo weekly pass. The RER suburban trains "
                "connect the centre with the airports and with Versailles.",
                "Paris has two main airports. Charles de Gaulle Airport (CDG) is linked to the city centre by the "
                "RER B train in about 35 minutes, and Orly Airport is served by the Orlyval shuttle and Metro line 14. "
                "The currency in Paris is the euro (EUR), and cards are accepted almost everywhere.",
                "The Eurostar high-speed train connects Paris Gare du Nord with London St Pancras International "
                "through the Channel Tunnel in about 2 hours and 15 minutes. High-speed TGV trains also run from "
                "Paris Gare de Lyon to Barcelona in about six and a half hours, making Paris a great base for a "
                "multi-city European trip.",
                "The best time to visit Paris is in spring, from April to June, when the parks bloom, or in early "
                "autumn in September and October. July and August are hot and crowded, and many small shops close "
                "in August. Museums are often closed on Monday or Tuesday, so check before you go.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Start at the Eiffel Tower in the morning, walk across the Seine to the Trocadero for the "
                "classic photo, then take a Seine river cruise. In the evening walk up the Champs-Elysees to the "
                "Arc de Triomphe. Day 2: Spend the morning in the Louvre, have lunch in the Marais, then visit "
                "Notre-Dame and Sainte-Chapelle on the Ile de la Cite.",
                "Day 3: Explore Montmartre and the Sacre-Coeur in the morning, then visit the Musee d'Orsay in the "
                "afternoon, and finish with dinner in Saint-Germain-des-Pres.",
                "The most popular day trip is the Palace of Versailles, the lavish home of King Louis XIV, which is "
                "about 40 minutes away on the RER C train. Art lovers can visit Giverny to see Claude Monet's house "
                "and water-lily garden. Fast TGV trains reach Reims, the heart of the Champagne region, in about "
                "45 minutes, and the island abbey of Mont-Saint-Michel can be reached on a long day trip.",
                "Travellers on a bigger European adventure often combine Paris with London by Eurostar, or with "
                "Barcelona by TGV.",
            ]),
        ],
    },

    # ----------------------------------------------------------------- LONDON
    "London": {
        "country": "United Kingdom",
        "tagline": "Royal history and modern culture on the River Thames",
        "sections": [
            ("Overview and History", [
                "London is the capital of England and the United Kingdom and sits on the River Thames. The Romans "
                "founded the city as Londinium around AD 47, making London, like Paris and Barcelona, a former "
                "town of the Roman Empire ruled from Rome. Parts of the old Roman wall can still be seen near "
                "Tower Hill.",
                "In 1666 the Great Fire of London destroyed much of the medieval city. The architect Sir Christopher "
                "Wren then rebuilt dozens of churches, including the famous St Paul's Cathedral with its great dome. "
                "In the nineteenth century London became the capital of the British Empire and the largest city in "
                "the world.",
                "British traders also founded cities far away. In 1819 Sir Stamford Raffles of the British East "
                "India Company established a trading post that became Singapore, and in 1788 the British First Fleet "
                "arrived in Sydney. London therefore has historical links with both Singapore and Sydney.",
                "Today London is a global centre of finance, theatre, music and museums. It hosted the Summer "
                "Olympic Games three times, in 1908, 1948 and 2012, more than any other city.",
            ]),
            ("Top Attractions", [
                "The Tower of London, founded by William the Conqueror in 1066, has served as a royal palace, prison "
                "and treasury. It still guards the Crown Jewels, watched over by the Yeoman Warders known as "
                "Beefeaters. Next to it, Tower Bridge opens to let tall ships pass along the Thames.",
                "Buckingham Palace is the London home of the British monarch. The Changing of the Guard ceremony "
                "takes place outside the palace on several mornings each week. Nearby, Westminster Abbey has hosted "
                "coronations since 1066, and the Houses of Parliament are crowned by the clock tower known as Big Ben "
                "(officially the Elizabeth Tower).",
                "Many of London's best museums are free. The British Museum displays the Rosetta Stone and the "
                "Egyptian mummies, the Natural History Museum has a giant blue whale skeleton, and Tate Modern shows "
                "modern art inside a former power station on the South Bank.",
                "For views, ride the London Eye, a giant observation wheel opposite Parliament, or go up The Shard, "
                "the tallest building in the UK. In the West End you can see world-famous musicals and plays.",
            ]),
            ("Neighborhoods and Food", [
                "Covent Garden is known for its market hall, street performers and the Royal Opera House. Nearby Soho "
                "is full of restaurants, bars and nightlife. Camden is famous for its alternative fashion stalls and "
                "Camden Market, while Notting Hill is known for its colourful houses and the Portobello Road antiques "
                "market.",
                "Shoreditch in East London is a creative district of street art, galleries and coffee shops. "
                "Brick Lane, close by, is the centre of London's Bangladeshi community and is famous for curry and "
                "for bagel bakeries that are open 24 hours.",
                "Classic British dishes include fish and chips, the full English breakfast, and the Sunday roast "
                "with Yorkshire pudding, served in traditional pubs. Afternoon tea with scones, clotted cream and jam "
                "is a famous London treat in grand hotels such as The Ritz.",
                "Borough Market, near London Bridge, is one of the oldest and best food markets in the city, with "
                "stalls selling cheese, street food and baked goods. In restaurants a service charge of 12.5 percent "
                "is often added to the bill.",
            ]),
            ("Getting Around and Practical Tips", [
                "The London Underground, known as the Tube, opened in 1863 and is the oldest underground railway in "
                "the world. Visitors can tap in and out with a contactless bank card or an Oyster card, and daily "
                "fares are automatically capped. Red double-decker buses are a cheap way to see the city.",
                "Heathrow Airport is the busiest airport in the UK. The Heathrow Express train reaches Paddington "
                "station in about 15 minutes, and the Elizabeth line is a cheaper option. London also has Gatwick, "
                "Stansted, Luton and London City airports. Emirates flies from Dubai to Heathrow and Gatwick, and "
                "flights from New York to London take about 7 hours.",
                "The Eurostar train leaves from St Pancras International and reaches Paris Gare du Nord in about "
                "2 hours and 15 minutes, so a trip to Paris is easy to add.",
                "The currency in London is the pound sterling (GBP). The best time to visit is from May to September "
                "when days are long and parks are green, but it can rain at any time of year, so carry an umbrella.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit Westminster Abbey, Big Ben and the Houses of Parliament, walk through St James's Park "
                "to Buckingham Palace, and ride the London Eye at sunset. Day 2: Explore the Tower of London and "
                "Tower Bridge, walk along the South Bank to Tate Modern, and finish at Borough Market.",
                "Day 3: Spend the morning at the British Museum, shop in Covent Garden, and see a West End show in the "
                "evening.",
                "Popular day trips include Windsor Castle, the oldest occupied castle in the world, about an hour away. "
                "The university city of Oxford is about one hour by train. Bath is famous for its Roman Baths, and "
                "Stonehenge is a prehistoric stone circle on Salisbury Plain.",
                "Thanks to the Eurostar, London is easily combined with Paris, and its large airports make it a "
                "convenient stopover between New York, Dubai and Singapore.",
            ]),
        ],
    },

    # ------------------------------------------------------------------- ROME
    "Rome": {
        "country": "Italy",
        "tagline": "The Eternal City of emperors, art and pasta",
        "sections": [
            ("Overview and History", [
                "Rome is the capital of Italy and lies on the River Tiber. According to legend it was founded in "
                "753 BC by the twins Romulus and Remus, who were raised by a she-wolf. Rome is called the Eternal City "
                "because it has been an important city for nearly three thousand years.",
                "Rome was the capital of the Roman Empire, which at its peak stretched from Britain to the Middle East. "
                "The Romans founded or ruled many cities in this guide series, including Londinium (London), Lutetia "
                "(Paris) and Barcino (Barcelona). In AD 330 the Emperor Constantine moved the capital to a new city "
                "called Constantinople, today's Istanbul.",
                "Rome later became the centre of the Catholic Church. Vatican City, the smallest country in the world, "
                "is located inside Rome and is ruled by the Pope. During the Renaissance, artists such as Michelangelo "
                "and Raphael created masterpieces here.",
                "Today Rome is a lively modern capital where ancient ruins, baroque fountains and busy cafes sit side "
                "by side. Its historic centre is a UNESCO World Heritage Site.",
            ]),
            ("Top Attractions", [
                "The Colosseum is the largest amphitheatre ever built. It was completed in AD 80 and could hold about "
                "50,000 spectators who came to watch gladiator fights. A combined ticket also gives entry to the Roman "
                "Forum, the centre of public life in ancient Rome, and the Palatine Hill, where emperors built their "
                "palaces.",
                "The Pantheon was rebuilt by the Emperor Hadrian around AD 125. Its huge concrete dome, with an open "
                "hole called the oculus at the top, is still the largest unreinforced concrete dome in the world.",
                "In Vatican City, St Peter's Basilica is one of the largest churches in the world, and its dome was "
                "designed by Michelangelo. The Vatican Museums lead to the Sistine Chapel, where Michelangelo painted "
                "the ceiling and The Last Judgment.",
                "The Trevi Fountain is the most famous fountain in Rome. Tradition says that if you throw a coin over "
                "your shoulder into the fountain you will return to Rome. The Spanish Steps and the Piazza Navona, "
                "with Bernini's Fountain of the Four Rivers, are also must-see sights.",
            ]),
            ("Neighborhoods and Food", [
                "Trastevere, across the Tiber, is a charming neighbourhood of cobbled lanes, ivy-covered buildings and "
                "family-run trattorias. Monti, near the Colosseum, is a trendy area with vintage shops and wine bars. "
                "Testaccio is known as the home of traditional Roman cooking and has a popular covered food market.",
                "Roman cuisine is simple and delicious. The four classic Roman pasta dishes are carbonara (egg, "
                "pecorino cheese, guanciale and black pepper), cacio e pepe (cheese and pepper), amatriciana (tomato "
                "and guanciale) and gricia.",
                "Street food favourites include suppli, fried rice balls with melted mozzarella inside, and pizza al "
                "taglio, rectangular pizza sold by weight. Gelato is eaten all year round; look for shops that store "
                "it in covered metal tins rather than bright, fluffy mountains.",
                "Romans drink espresso standing at the bar, and cappuccino is usually only ordered in the morning. "
                "Dinner starts late, often after 8 pm. A small cover charge called 'coperto' is common in restaurants.",
            ]),
            ("Getting Around and Practical Tips", [
                "Much of central Rome is best explored on foot. The Rome Metro has three lines, A, B and C, which are "
                "useful for reaching the Colosseum, the Vatican area and Termini, the main railway station. Buses and "
                "trams fill the gaps.",
                "Rome's main airport is Fiumicino (Leonardo da Vinci Airport). The Leonardo Express train reaches Roma "
                "Termini in about 32 minutes. The smaller Ciampino Airport is used by low-cost airlines. Turkish "
                "Airlines connects Rome with Istanbul in about two and a half hours.",
                "Fast Frecciarossa trains link Rome with Naples in about 1 hour 10 minutes, Florence in about 1 hour "
                "30 minutes and Venice in under 4 hours. The currency in Rome is the euro (EUR).",
                "The best time to visit Rome is in spring, April and May, or in autumn, September and October, when "
                "the weather is warm but not too hot. In August it is very hot and many Romans leave the city for the "
                "Ferragosto holiday. Cover your shoulders and knees when entering churches.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit the Colosseum, the Roman Forum and the Palatine Hill, then have dinner in Monti. "
                "Day 2: Spend the morning in the Vatican Museums, the Sistine Chapel and St Peter's Basilica, then "
                "cross the river to Trastevere for the evening.",
                "Day 3: Walk from the Pantheon to Piazza Navona, the Trevi Fountain and the Spanish Steps, and enjoy "
                "gelato along the way.",
                "Ostia Antica, the ancient port city of Rome, is a large archaeological site only about 30 minutes "
                "away by train from Piramide station. Tivoli is home to the Renaissance gardens of Villa d'Este and "
                "the ruins of Hadrian's Villa.",
                "On a longer day trip, take the fast train to Naples and continue to Pompeii, the Roman town buried "
                "by the eruption of Mount Vesuvius in AD 79.",
            ]),
        ],
    },

    # -------------------------------------------------------------- BARCELONA
    "Barcelona": {
        "country": "Spain",
        "tagline": "Gaudi, beaches and tapas on the Mediterranean",
        "sections": [
            ("Overview and History", [
                "Barcelona is the capital of Catalonia, a region in north-east Spain, and lies on the Mediterranean "
                "Sea. The Romans founded the town of Barcino here in the first century BC, and remains of its Roman "
                "walls can still be seen in the Gothic Quarter. Like London and Paris, Barcelona was once part of the "
                "Roman Empire ruled from Rome.",
                "In the Middle Ages Barcelona became a powerful trading port. In the nineteenth century the city grew "
                "rapidly and the engineer Ildefons Cerda designed the Eixample district, a grid of wide streets with "
                "cut-off corners at each block.",
                "At the end of the nineteenth century, the Catalan Modernisme movement transformed the city. Its most "
                "famous architect, Antoni Gaudi, created fantastic buildings with curving shapes and colourful "
                "mosaics. Barcelona hosted the Summer Olympic Games in 1992, which brought new beaches and a modern "
                "waterfront.",
                "Two languages are spoken in Barcelona: Catalan and Spanish. Signs are usually in Catalan first.",
            ]),
            ("Top Attractions", [
                "The Sagrada Familia is Gaudi's masterpiece, a giant basilica begun in 1882 that is still under "
                "construction more than 140 years later. Its interior columns branch like trees and its stained glass "
                "fills the space with coloured light. Tickets should be booked in advance.",
                "Park Guell is a hillside park designed by Gaudi with a famous mosaic lizard, a serpentine bench and "
                "views over the city. On the Passeig de Gracia avenue you can visit two more Gaudi houses: Casa "
                "Batllo, with a roof like a dragon's back, and Casa Mila, also known as La Pedrera.",
                "La Rambla is a long tree-lined pedestrian street leading down to the sea. Halfway along is La "
                "Boqueria, a famous food market. The Gothic Quarter (Barri Gotic) is a maze of medieval streets around "
                "Barcelona Cathedral.",
                "Montjuic hill offers museums, gardens and the 1992 Olympic stadium, and Barceloneta beach is the most "
                "popular city beach. Football fans can visit Camp Nou, the home stadium of FC Barcelona.",
            ]),
            ("Neighborhoods and Food", [
                "El Born is a stylish area with boutiques, cocktail bars and the Picasso Museum, which holds many works "
                "from the artist's early years. Gracia feels like a village, with small squares full of cafes and "
                "a big neighbourhood festival in August. The Eixample is home to many Modernisme buildings and "
                "elegant shops.",
                "Barceloneta, the old fishermen's quarter by the beach, is the place for seafood restaurants. Poble "
                "Sec is known for its street of tapas bars, Carrer de Blai, where small snacks called pintxos are "
                "sold at low prices.",
                "Catalan food is a highlight. Pa amb tomaquet is bread rubbed with ripe tomato, olive oil and salt. "
                "Tapas such as patatas bravas, croquetas and jamon iberico are perfect for sharing. Paella, originally "
                "from Valencia, is popular by the sea, and crema catalana is a local custard dessert similar to creme "
                "brulee.",
                "Locals enjoy vermouth before lunch on weekends and cava, Catalan sparkling wine. Meals are eaten late: "
                "lunch at around 2 pm and dinner at 9 or 10 pm.",
            ]),
            ("Getting Around and Practical Tips", [
                "Barcelona has an efficient Metro run by TMB, plus buses and trams. The T-casual card gives ten "
                "journeys, and the Hola Barcelona travel card offers unlimited travel for visitors. The city centre "
                "is also easy to explore on foot or by bicycle.",
                "Barcelona-El Prat Airport is about 15 kilometres from the centre. The Aerobus shuttle reaches Placa "
                "de Catalunya in about 35 minutes, and Metro line L9 also serves the airport.",
                "High-speed AVE trains connect Barcelona Sants with Madrid in about 2 hours 30 minutes, and TGV trains "
                "run to Paris Gare de Lyon in about six and a half hours. The currency is the euro (EUR).",
                "The best time to visit Barcelona is late spring, May and June, or September, when the sea is warm "
                "and the big La Merce festival takes place in late September. July and August are hot and very busy. "
                "Watch out for pickpockets on La Rambla and in the Metro.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit the Sagrada Familia in the morning, then walk along the Passeig de Gracia to see Casa "
                "Batllo and Casa Mila. Spend the evening in the Gothic Quarter. Day 2: Explore Park Guell in the "
                "morning, have lunch at La Boqueria, and relax on Barceloneta beach.",
                "Day 3: Visit the Picasso Museum and El Born, then take the cable car up Montjuic for sunset views.",
                "The mountain monastery of Montserrat, home of the Black Madonna, is about one hour away by train and "
                "rack railway. Sitges is a pretty beach town 40 minutes south. The medieval city of Girona and the "
                "Dali Theatre-Museum in Figueres, created by the surrealist artist Salvador Dali, make a great day out.",
                "Barcelona is often combined with Paris on a rail trip, or with Rome by flight or overnight ferry.",
            ]),
        ],
    },

    # --------------------------------------------------------------- ISTANBUL
    "Istanbul": {
        "country": "Turkey",
        "tagline": "Where Europe meets Asia across the Bosphorus",
        "sections": [
            ("Overview and History", [
                "Istanbul is the largest city in Turkey and the only major city in the world that spans two "
                "continents, Europe and Asia. The two sides are separated by the Bosphorus strait, which links the "
                "Black Sea with the Sea of Marmara.",
                "The city was founded by Greek colonists as Byzantium. In AD 330 the Roman Emperor Constantine made it "
                "the new capital of the Roman Empire and named it Constantinople. For more than a thousand years it was "
                "the capital of the Eastern Roman, or Byzantine, Empire, linking its history closely with Rome.",
                "In 1453 the Ottoman Sultan Mehmed II conquered Constantinople, and the city became the capital of the "
                "Ottoman Empire. The sultans built magnificent mosques, palaces and bazaars. After the Republic of "
                "Turkey was founded in 1923, the capital moved to Ankara, but Istanbul remained the country's economic "
                "and cultural heart.",
                "The historic areas of Istanbul are a UNESCO World Heritage Site.",
            ]),
            ("Top Attractions", [
                "Hagia Sophia was completed in AD 537 under the Byzantine Emperor Justinian. It was a cathedral for "
                "nearly a thousand years, then a mosque, then a museum, and is now a mosque again. Its enormous dome "
                "and golden mosaics are breathtaking.",
                "Facing it, the Blue Mosque, officially the Sultan Ahmed Mosque, was finished in 1616 and has six "
                "minarets and walls covered in blue Iznik tiles. Topkapi Palace was the home of the Ottoman sultans for "
                "about 400 years and displays treasures such as the Topkapi Dagger.",
                "The Grand Bazaar is one of the oldest and largest covered markets in the world, with around 4,000 "
                "shops selling carpets, lamps, jewellery and ceramics. The Spice Bazaar near Eminonu is full of the "
                "scents of spices, teas and Turkish delight.",
                "The Basilica Cistern is a vast underground water reservoir with hundreds of columns, built in the "
                "sixth century. Galata Tower offers panoramic views, and a cruise on the Bosphorus passes palaces such "
                "as Dolmabahce Palace and wooden mansions along the shore.",
            ]),
            ("Neighborhoods and Food", [
                "Sultanahmet is the historic old city with Hagia Sophia, the Blue Mosque and Topkapi Palace. Across the "
                "Golden Horn, Beyoglu is the modern heart of the city, centred on the busy pedestrian Istiklal Avenue "
                "and its historic red tram. Karakoy, by the water, is full of cafes and galleries.",
                "On the Asian side, Kadikoy has a lively food market and a relaxed local atmosphere; it is reached by "
                "a short ferry ride. Balat is a colourful historic neighbourhood with steep streets and painted houses.",
                "Istanbul is a paradise for street food. Simit is a ring of bread covered in sesame seeds, sold from "
                "red carts on every corner. Balik ekmek is a grilled fish sandwich served from boats at Eminonu. Doner "
                "kebab, lahmacun and many kinds of kebab are everywhere.",
                "In restaurants, start with meze, small dishes such as hummus and stuffed vine leaves. For dessert, try "
                "baklava and Turkish delight (lokum). Turkish tea (cay) is served in small tulip-shaped glasses, and "
                "Turkish coffee is thick and strong.",
            ]),
            ("Getting Around and Practical Tips", [
                "Buy an Istanbulkart, a rechargeable card used on trams, metro, buses, funiculars and ferries. The T1 "
                "tram connects Sultanahmet with Eminonu and Karakoy. The Marmaray rail tunnel runs under the Bosphorus "
                "between Europe and Asia, and public ferries are a cheap and beautiful way to cross.",
                "Istanbul Airport (IST) is one of the largest airports in the world and the main hub of Turkish "
                "Airlines, which flies to more countries than any other airline, including direct flights to Rome, "
                "London, Paris, Tokyo, Singapore and New York. Sabiha Gokcen Airport (SAW) is on the Asian side.",
                "The currency is the Turkish lira (TRY). Bargaining is normal in the Grand Bazaar but not in shops with "
                "fixed prices. When visiting mosques, women should cover their hair, and everyone should cover their "
                "shoulders and knees and remove their shoes.",
                "The best time to visit Istanbul is spring, April and May, when the Istanbul Tulip Festival fills parks "
                "such as Emirgan Park with flowers, or autumn, September to November. Summers are hot and winters are "
                "cool and rainy.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit Hagia Sophia, the Blue Mosque and the Basilica Cistern in Sultanahmet, then explore "
                "Topkapi Palace. Day 2: Shop in the Grand Bazaar and the Spice Bazaar, eat balik ekmek at Eminonu, and "
                "take a Bosphorus cruise in the afternoon.",
                "Day 3: Cross the Galata Bridge, climb Galata Tower, walk along Istiklal Avenue, and take the ferry to "
                "Kadikoy for dinner on the Asian side.",
                "The Princes' Islands in the Sea of Marmara are a popular day trip by ferry. On Buyukada, the largest "
                "island, there are no private cars, so visitors walk or cycle past old wooden mansions. The city of "
                "Bursa, the first Ottoman capital, is famous for its green mosque and Iskender kebab.",
                "Many visitors also fly about one hour and fifteen minutes to Cappadocia to see its fairy chimneys and "
                "hot-air balloons.",
            ]),
        ],
    },

    # ------------------------------------------------------------------ DUBAI
    "Dubai": {
        "country": "United Arab Emirates",
        "tagline": "Skyscrapers, desert adventures and a global airline hub",
        "sections": [
            ("Overview and History", [
                "Dubai is one of the seven emirates of the United Arab Emirates (UAE) and lies on the Persian Gulf. For "
                "centuries it was a small fishing and pearl-diving village built around Dubai Creek, a natural "
                "saltwater inlet.",
                "Oil was discovered in Dubai in 1966, and in 1971 Dubai joined other emirates to form the United Arab "
                "Emirates. Rulers of the Al Maktoum family used oil money to build ports, airports and tourism, "
                "turning Dubai into a global business and travel hub.",
                "Today Dubai is famous for record-breaking architecture, luxury shopping and desert experiences. The "
                "city hosted the world's fair Expo 2020, which took place from 2021 to 2022. Its home airline, "
                "Emirates, connects Dubai with cities on every inhabited continent, including London, Sydney, "
                "Singapore, New York and Tokyo.",
                "Arabic is the official language, but English is widely spoken. The weekend in Dubai is Saturday and "
                "Sunday, and Friday is a half working day.",
            ]),
            ("Top Attractions", [
                "The Burj Khalifa is the tallest building in the world at 828 metres. It opened in 2010 and its "
                "observation decks, called At the Top, are on levels 124, 125 and 148. At its foot, the Dubai "
                "Fountain puts on a free show of water, music and lights every evening.",
                "The Dubai Mall is one of the largest shopping centres in the world, with an aquarium, an ice rink and "
                "hundreds of shops. The sail-shaped Burj Al Arab hotel and the palm-shaped artificial island of Palm "
                "Jumeirah are iconic sights along the coast.",
                "The Museum of the Future, opened in 2022, is a striking ring-shaped building covered in Arabic "
                "calligraphy. The Dubai Frame is a giant golden picture frame with views of old and new Dubai.",
                "For history, visit the Al Fahidi Historical Neighbourhood, with its wind-tower houses, and take a "
                "traditional wooden abra boat across Dubai Creek to the Gold Souk and the Spice Souk in Deira. A "
                "desert safari with dune driving and dinner at a desert camp is a favourite evening activity.",
            ]),
            ("Neighborhoods and Food", [
                "Downtown Dubai is home to the Burj Khalifa and Dubai Mall. Dubai Marina is a forest of residential "
                "towers around a canal, with a waterfront walk and many restaurants, next to the beach at JBR. Deira "
                "and Bur Dubai, on either side of the creek, are the old trading districts with busy souks.",
                "Jumeirah is a residential beach area with relaxed cafes, and Alserkal Avenue in Al Quoz is the centre "
                "of the contemporary art scene.",
                "Emirati food reflects the Gulf's trading history. Al machboos is spiced rice with meat or fish, and "
                "luqaimat are sweet fried dumplings with date syrup. Arabic coffee, called gahwa, is flavoured with "
                "cardamom and served with dates as a sign of hospitality.",
                "Dubai's huge expatriate population means you can find food from almost every country, from shawarma "
                "and Indian biryani to world-class fine dining. During the holy month of Ramadan, visitors should avoid "
                "eating or drinking in public during daylight hours.",
            ]),
            ("Getting Around and Practical Tips", [
                "The Dubai Metro has two driverless lines, the Red Line and the Green Line, and is clean and air "
                "conditioned. Pay with a rechargeable Nol card. Taxis and ride-hailing apps are affordable, and the "
                "abra boats across the creek cost only a few dirhams.",
                "Dubai International Airport (DXB) is the world's busiest airport for international passengers and the "
                "hub of Emirates. The Red Line Metro connects the airport with the city centre. From Dubai, Emirates "
                "flies non-stop to Sydney in about 14 hours and to London in about 7 hours.",
                "The currency is the UAE dirham (AED), which is pegged to the US dollar. Dress modestly in public places "
                "such as malls and souks, covering shoulders and knees.",
                "The best time to visit Dubai is from November to March, when the weather is warm and sunny. From June "
                "to September temperatures often rise above 40 degrees Celsius, so outdoor sightseeing is uncomfortable.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit the Burj Khalifa at sunset and watch the Dubai Fountain show, then explore Dubai Mall. "
                "Day 2: Explore old Dubai: the Al Fahidi neighbourhood, an abra ride across the creek, and the Gold and "
                "Spice Souks. In the afternoon go on a desert safari.",
                "Day 3: Visit the Museum of the Future, relax on Jumeirah beach with a view of the Burj Al Arab, and "
                "walk around Dubai Marina in the evening.",
                "Abu Dhabi, the capital of the UAE, is about 90 minutes away by road. There you can visit the Sheikh "
                "Zayed Grand Mosque, one of the largest mosques in the world, and the Louvre Abu Dhabi, a museum created "
                "in partnership with the Louvre in Paris. The mountain town of Hatta offers kayaking and hiking.",
                "Because Emirates connects Dubai with so many cities, many travellers make Dubai a stopover on the way "
                "between London and Sydney or between Europe and Asia.",
            ]),
        ],
    },

    # ------------------------------------------------------------------ TOKYO
    "Tokyo": {
        "country": "Japan",
        "tagline": "Ancient temples and neon streets in the world's largest metropolis",
        "sections": [
            ("Overview and History", [
                "Tokyo is the capital of Japan and, with its surrounding region, the most populous metropolitan area in "
                "the world. It was originally a fishing village called Edo, which became the seat of the Tokugawa "
                "shoguns in 1603.",
                "In 1868, during the Meiji Restoration, the emperor moved to Edo and the city was renamed Tokyo, which "
                "means Eastern Capital. Tokyo was badly damaged by the Great Kanto Earthquake in 1923 and by bombing in "
                "the Second World War, and both times it was rebuilt.",
                "Tokyo hosted the Summer Olympic Games in 1964 and again in 2021 (the Tokyo 2020 Games). Today it is a "
                "city of contrasts, where quiet shrines and traditional gardens sit next to neon-lit streets, "
                "high-tech shops and some of the world's best restaurants.",
                "Tokyo is a very safe and clean city, and its public transport is famous for being punctual.",
            ]),
            ("Top Attractions", [
                "Senso-ji in Asakusa is Tokyo's oldest temple. Visitors enter through the Kaminarimon (Thunder Gate) "
                "with its giant red lantern, then walk along Nakamise Street, lined with snack and souvenir stalls. "
                "Meiji Jingu is a peaceful Shinto shrine surrounded by forest near Harajuku.",
                "Shibuya Crossing is famous as one of the busiest pedestrian crossings in the world. Next to Shibuya "
                "Station stands the statue of Hachiko, the loyal dog. The Shibuya Sky observation deck gives views of "
                "the crossing from above.",
                "Tokyo Skytree, at 634 metres, is the tallest tower in Japan. The older Tokyo Tower, painted red and "
                "white and completed in 1958, was inspired by the Eiffel Tower in Paris. On clear days you can see "
                "Mount Fuji from both towers.",
                "Other highlights include the gardens of the Imperial Palace, the teamLab digital art museums, the "
                "Tsukiji Outer Market for fresh seafood, and Ueno Park, which has several museums and is one of the "
                "most popular places for cherry blossom viewing.",
            ]),
            ("Neighborhoods and Food", [
                "Shinjuku is a giant entertainment district with skyscrapers, department stores, the tiny bars of "
                "Golden Gai and the smoky yakitori alley Omoide Yokocho. Harajuku is the centre of youth fashion, "
                "especially along Takeshita Street.",
                "Akihabara is known as Electric Town and is the heart of anime, manga and gaming culture. Ginza is an "
                "upscale shopping district, and Shimokitazawa is a relaxed area of vintage shops and small theatres.",
                "Tokyo has more Michelin-starred restaurants than any other city in the world. Classic dishes to try "
                "include sushi, ramen, tempura, tonkatsu (breaded pork cutlet) and yakitori (grilled chicken skewers). "
                "An izakaya is a casual Japanese pub serving small dishes with drinks.",
                "Convenience stores, called konbini, sell surprisingly good onigiri rice balls, sandwiches and hot "
                "meals at any hour. Tipping is not customary in Japan and can even cause confusion.",
            ]),
            ("Getting Around and Practical Tips", [
                "Tokyo has one of the best public transport systems in the world. The JR Yamanote Line runs in a loop "
                "around the city centre, connecting Tokyo Station, Shinjuku, Shibuya, Harajuku and Ueno. Tokyo Metro and "
                "Toei subway lines cover the rest. Pay with a rechargeable IC card such as Suica or PASMO.",
                "Tokyo has two airports. Narita Airport is about an hour from the centre by the Narita Express or the "
                "Keisei Skyliner. Haneda Airport is much closer and connected by the Keikyu Line and the Tokyo Monorail. "
                "Singapore Airlines and Japan Airlines fly between Tokyo and Singapore in about 7 hours.",
                "Shinkansen bullet trains leave from Tokyo Station; the Nozomi reaches Kyoto in about 2 hours and 15 "
                "minutes. The currency in Tokyo is the Japanese yen (JPY). Some small restaurants and shops only "
                "accept cash, and convenience store ATMs accept foreign cards.",
                "The best times to visit Tokyo are spring, from late March to early April, when the cherry blossoms "
                "(sakura) bloom, and autumn, October and November, when the leaves turn red and gold. Summer is hot "
                "and humid, and June is the rainy season.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Visit Senso-ji in Asakusa, take a river boat or walk to Tokyo Skytree, and spend the evening in "
                "Akihabara. Day 2: Walk through Meiji Jingu to Harajuku, shop on Takeshita Street, cross Shibuya "
                "Crossing and see Hachiko, then enjoy dinner in Shinjuku.",
                "Day 3: Have a sushi breakfast at the Tsukiji Outer Market, stroll through the Imperial Palace East "
                "Gardens and Ginza, and visit a teamLab museum.",
                "Kamakura, about one hour by train, is famous for its Great Buddha statue and seaside temples. Nikko "
                "is home to the richly decorated Toshogu Shrine. Hakone offers hot springs (onsen) and views of Mount "
                "Fuji, as does Lake Kawaguchiko.",
                "Many visitors continue by Shinkansen to Kyoto, or fly onwards to Singapore or Sydney.",
            ]),
        ],
    },

    # -------------------------------------------------------------- SINGAPORE
    "Singapore": {
        "country": "Singapore",
        "tagline": "A garden city-state of food, culture and futuristic design",
        "sections": [
            ("Overview and History", [
                "Singapore is an island city-state at the southern tip of the Malay Peninsula in South-East Asia. In "
                "1819 Sir Stamford Raffles of the British East India Company established a trading post here, and "
                "Singapore grew into a busy port of the British Empire, ruled from London.",
                "Singapore became independent in 1965 after separating from Malaysia. Under its first Prime Minister, "
                "Lee Kuan Yew, the small nation quickly developed into one of the richest and most modern countries "
                "in the world.",
                "Singapore has four official languages: English, Malay, Mandarin and Tamil, reflecting its Chinese, "
                "Malay and Indian communities. It is known as a garden city because of its many parks and green "
                "buildings.",
                "The city is famous for being very clean and safe. Strict rules include fines for littering, and the "
                "sale of chewing gum is banned.",
            ]),
            ("Top Attractions", [
                "Gardens by the Bay is a futuristic park next to Marina Bay. Its giant tree-like structures, the "
                "Supertrees, light up during the free Garden Rhapsody show every evening. The Cloud Forest and Flower "
                "Dome are huge cooled glass conservatories filled with plants from around the world.",
                "Marina Bay Sands is a hotel with three towers joined at the top by the SkyPark, which has an "
                "observation deck and a famous infinity pool for hotel guests. Across the bay, the Merlion statue, "
                "half lion and half fish, is the symbol of Singapore.",
                "The Singapore Botanic Gardens are a UNESCO World Heritage Site and include the National Orchid Garden. "
                "The Singapore Zoo and the Night Safari are among the best wildlife parks in the world. Sentosa Island "
                "has beaches, Universal Studios Singapore and other attractions.",
                "Jewel Changi Airport features the Rain Vortex, the world's tallest indoor waterfall at about 40 metres. "
                "The historic Raffles Hotel, named after the city's founder, is where the Singapore Sling cocktail was "
                "invented.",
            ]),
            ("Neighborhoods and Food", [
                "Chinatown has temples, shophouses and street markets, including the Buddha Tooth Relic Temple. Little "
                "India is full of colour, spice shops and the Sri Veeramakaliamman Temple. Kampong Glam, the Malay and "
                "Arab quarter, is home to the golden-domed Sultan Mosque and the trendy Haji Lane.",
                "Tiong Bahru is an older residential area with art deco flats and cafes, and Clarke Quay is a riverside "
                "nightlife area.",
                "Food is a national passion. Hawker centres are open-air food courts with dozens of stalls selling "
                "cheap and delicious meals, and Singapore's hawker culture was added to the UNESCO list of Intangible "
                "Cultural Heritage in 2020. Popular hawker centres include Maxwell Food Centre and Lau Pa Sat, famous "
                "for its evening satay street.",
                "Must-try dishes include Hainanese chicken rice, laksa (spicy coconut noodle soup), chilli crab, char "
                "kway teow (fried noodles) and kaya toast with soft-boiled eggs for breakfast.",
            ]),
            ("Getting Around and Practical Tips", [
                "Singapore's MRT metro system is clean, fast and easy to use. You can tap in with a contactless bank "
                "card or an EZ-Link card. Buses cover the whole island, and taxis and Grab ride-hailing cars are "
                "affordable.",
                "Changi Airport is regularly voted the best airport in the world. To get from Changi Airport to the "
                "city, take the MRT East West Line, changing at Tanah Merah; the journey to the centre takes about 30 "
                "to 40 minutes. Taxis take about 20 minutes.",
                "Changi is the hub of Singapore Airlines, which flies to Tokyo, Sydney, London and New York. Its "
                "non-stop flight from Singapore to New York is one of the longest flights in the world, at around 18 "
                "hours. The currency is the Singapore dollar (SGD).",
                "Singapore is hot and humid all year, with temperatures around 30 degrees Celsius. February to April is "
                "usually the driest and sunniest period, while the north-east monsoon brings heavy rain from November "
                "to January. Carry an umbrella and expect strong air conditioning indoors.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Explore Marina Bay, see the Merlion, go up to the Marina Bay Sands SkyPark and watch the Garden "
                "Rhapsody light show at Gardens by the Bay. Day 2: Walk through Chinatown, have lunch at Maxwell Food "
                "Centre, then explore Little India and Kampong Glam.",
                "Day 3: Visit the Singapore Botanic Gardens in the morning, spend the afternoon on Sentosa Island, and "
                "end with the Night Safari.",
                "Pulau Ubin is a rustic island reached by bumboat, where visitors cycle past old villages and "
                "mangroves. Ferries go to the Indonesian island of Bintan for beach resorts, and Johor Bahru in "
                "Malaysia is just across the causeway.",
                "Singapore is a popular stopover between Europe and Australia, linking London with Sydney, and a short "
                "flight from Tokyo and other Asian cities.",
            ]),
        ],
    },

    # ----------------------------------------------------------------- SYDNEY
    "Sydney": {
        "country": "Australia",
        "tagline": "Harbour icons, golden beaches and outdoor living",
        "sections": [
            ("Overview and History", [
                "Sydney is the largest city in Australia and the capital of the state of New South Wales. For tens of "
                "thousands of years the area has been home to Aboriginal people; the Gadigal people of the Eora Nation "
                "are the traditional custodians of the land around Sydney Harbour.",
                "In 1788 the British First Fleet, led by Captain Arthur Phillip, arrived from England and set up a "
                "penal colony. The settlement grew into a major port and, like Singapore, kept strong ties with London "
                "and the British Empire.",
                "Sydney hosted the Summer Olympic Games in 2000. Today it is a multicultural city known for its "
                "beautiful harbour, beaches and relaxed outdoor lifestyle.",
                "Because Sydney is in the Southern Hemisphere, its seasons are the opposite of Europe's: summer is from "
                "December to February and winter from June to August.",
            ]),
            ("Top Attractions", [
                "The Sydney Opera House is one of the most famous buildings of the twentieth century. It was designed "
                "by the Danish architect Jorn Utzon, opened in 1973 and became a UNESCO World Heritage Site in 2007. Its "
                "white roof shells look like sails on the harbour. Guided tours and performances are available every "
                "day.",
                "The Sydney Harbour Bridge, nicknamed the Coathanger, opened in 1932. You can walk across it for free, "
                "or join BridgeClimb to climb to the top of its arch. Every New Year's Eve the bridge is the centre of a "
                "spectacular fireworks show.",
                "Bondi Beach is Australia's most famous beach. The Bondi to Coogee coastal walk is about 6 kilometres "
                "long and passes cliffs, ocean pools and smaller beaches. A ferry from Circular Quay to Manly is a "
                "cheap way to enjoy harbour views.",
                "The Royal Botanic Garden sits next to the Opera House, and Taronga Zoo, reached by ferry, has "
                "Australian animals such as koalas and kangaroos with views of the city skyline.",
            ]),
            ("Neighborhoods and Food", [
                "The Rocks is Sydney's oldest neighbourhood, with sandstone buildings, historic pubs and a weekend "
                "market, right next to the Harbour Bridge. Darling Harbour and Barangaroo are waterfront areas with "
                "restaurants, museums and the SEA LIFE aquarium.",
                "Surry Hills and Newtown are creative inner-city suburbs with cafes, bars and vintage shops, while "
                "Paddington is known for its terrace houses and boutiques. Manly is a relaxed beach suburb.",
                "Sydney has a world-class cafe culture. Order a flat white coffee and a smashed avocado on toast for "
                "brunch. Seafood is excellent: try Sydney rock oysters, barramundi, and fish and chips by the beach. The "
                "Sydney Fish Market is one of the largest in the Southern Hemisphere.",
                "Classic Australian treats include the meat pie, the pavlova meringue dessert, lamingtons and Tim Tam "
                "biscuits. Thanks to immigration, Sydney also has great Thai, Vietnamese, Chinese and Lebanese food.",
            ]),
            ("Getting Around and Practical Tips", [
                "Sydney's public transport includes trains, buses, light rail, the new driverless Metro and the much "
                "loved harbour ferries from Circular Quay. Pay with an Opal card or tap on with a contactless bank card; "
                "there are daily and weekly fare caps.",
                "Sydney Airport (SYD) is close to the city. The Airport Link train reaches Central station in about 13 "
                "minutes. Emirates flies non-stop between Sydney and Dubai in about 14 hours, and Qantas and Singapore "
                "Airlines connect Sydney with London via Singapore or other stopovers.",
                "The currency is the Australian dollar (AUD). Tipping is not expected but is appreciated for good "
                "service. The Australian sun is very strong, so always wear sunscreen and swim between the red and "
                "yellow flags on patrolled beaches.",
                "The best times to visit Sydney are spring, September to November, and autumn, March to May, when the "
                "weather is warm but not too hot. The Vivid Sydney festival of light takes place in May and June, and "
                "New Year's Eve fireworks draw huge crowds.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Tour the Sydney Opera House, stroll through the Royal Botanic Garden to Mrs Macquarie's Chair, "
                "then explore The Rocks and walk across the Harbour Bridge. Day 2: Spend the day at Bondi Beach and do "
                "the Bondi to Coogee coastal walk.",
                "Day 3: Take the ferry to Taronga Zoo in the morning and the ferry to Manly in the afternoon, then have "
                "dinner in Surry Hills or Newtown.",
                "The Blue Mountains are about two hours west by train. At Katoomba you can see the famous Three Sisters "
                "rock formation and walk through eucalyptus forest. The Hunter Valley is Australia's oldest wine region, "
                "and the Royal National Park, south of the city, has cliffs, beaches and walking trails.",
                "Long-haul travellers often break the journey to Sydney with a stopover in Dubai or Singapore.",
            ]),
        ],
    },

    # --------------------------------------------------------------- NEW YORK
    "New York": {
        "country": "United States",
        "tagline": "The city that never sleeps",
        "sections": [
            ("Overview and History", [
                "New York City is the largest city in the United States and is made up of five boroughs: Manhattan, "
                "Brooklyn, Queens, The Bronx and Staten Island. The area was originally the homeland of the Lenape "
                "people.",
                "In the 1620s the Dutch founded a colony called New Amsterdam at the southern tip of Manhattan. The "
                "English took control in 1664 and renamed it New York. Between 1892 and 1954 millions of immigrants "
                "entered the United States through Ellis Island in New York Harbor.",
                "The Statue of Liberty, a gift from France and the people of Paris to the United States, was dedicated "
                "in 1886. It was designed by the French sculptor Frederic Auguste Bartholdi, and its iron framework was "
                "engineered by Gustave Eiffel, who later built the Eiffel Tower in Paris.",
                "Today New York is a world capital of finance, media, art, fashion and theatre, and the headquarters of "
                "the United Nations.",
            ]),
            ("Top Attractions", [
                "The Statue of Liberty stands on Liberty Island and can be visited by ferry, together with the Ellis "
                "Island National Museum of Immigration. Central Park, designed by Frederick Law Olmsted and Calvert "
                "Vaux, covers 843 acres in the middle of Manhattan.",
                "The Empire State Building, completed in 1931, has observation decks on the 86th and 102nd floors. "
                "Other great viewpoints include Top of the Rock at Rockefeller Center and the observatory of One World "
                "Trade Center, the tallest building in the Western Hemisphere at 1,776 feet (541 metres). The 9/11 "
                "Memorial and Museum honours the victims of the 2001 attacks.",
                "The Metropolitan Museum of Art is one of the largest art museums in the world, and the Museum of "
                "Modern Art (MoMA) holds famous works such as Van Gogh's The Starry Night.",
                "Times Square is famous for its giant digital billboards and is the heart of the Broadway theatre "
                "district. Walking across the Brooklyn Bridge, opened in 1883, and along the High Line, a park built on "
                "an old elevated railway, are free and memorable experiences.",
            ]),
            ("Neighborhoods and Food", [
                "SoHo is known for its cast-iron buildings and shopping, and Greenwich Village for its jazz clubs and "
                "Washington Square Park. Harlem is the historic centre of African-American culture and home of the "
                "Apollo Theater.",
                "In Brooklyn, DUMBO offers classic views of the Manhattan skyline beneath the Brooklyn Bridge, and "
                "Williamsburg is a hip area of bars, music venues and markets. Chinatown, Little Italy and Flushing in "
                "Queens offer some of the best Asian and Italian food in the city.",
                "New York is famous for its foldable thin-crust New York-style pizza slices and for bagels with cream "
                "cheese and lox (smoked salmon). Katz's Delicatessen, open since 1888, serves a legendary pastrami on "
                "rye sandwich.",
                "Other classics include New York cheesecake, hot dogs from street carts, and halal cart chicken over "
                "rice. Tipping 18 to 20 percent is expected in restaurants.",
            ]),
            ("Getting Around and Practical Tips", [
                "The New York City Subway runs 24 hours a day, every day. Pay by tapping a contactless card or phone at "
                "the OMNY readers; a single ride costs about 3 dollars. Yellow taxis, buses and Citi Bike bicycles are "
                "also available, and the Staten Island Ferry is free and passes the Statue of Liberty.",
                "New York has three major airports. JFK International Airport is the main airport for international "
                "flights and is connected to the subway by the AirTrain. LaGuardia serves mostly domestic flights, and "
                "Newark Airport is in New Jersey. Flights from New York to London take about 7 hours, and Singapore "
                "Airlines flies non-stop between Newark and Singapore.",
                "The currency is the US dollar (USD). Sales tax is added at the till, so prices on tags are lower than "
                "what you pay.",
                "The best times to visit New York are spring, April to June, and autumn, September to November. The "
                "holiday season in December is magical, with the Rockefeller Center Christmas tree and ice skating, "
                "but it is cold. Summers are hot and humid.",
            ]),
            ("Sample Itinerary and Day Trips", [
                "Day 1: Take the ferry to the Statue of Liberty and Ellis Island, visit the 9/11 Memorial and walk "
                "across the Brooklyn Bridge to DUMBO. Day 2: Visit the Metropolitan Museum of Art, walk through Central "
                "Park, and see a Broadway show near Times Square in the evening.",
                "Day 3: Walk the High Line, explore Greenwich Village and SoHo, and watch the sunset from the Empire "
                "State Building or Top of the Rock.",
                "The Hudson Valley, north of the city, offers historic estates, art museums and autumn colours. Amtrak "
                "trains reach Philadelphia in about 1 hour 20 minutes and Washington DC in about 3 hours. In summer, "
                "the beaches of Long Island and the Hamptons are popular escapes.",
                "New York is a natural starting point for a transatlantic trip to London or Paris.",
            ]),
        ],
    },
}
