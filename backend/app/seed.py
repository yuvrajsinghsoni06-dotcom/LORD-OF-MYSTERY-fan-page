from app.database import SessionLocal, engine, Base
from app.models import Pathway, Beyonder, Potion, Commission, Claim


def seed_database(force=False):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded with all 22 pathways
        pathway_count = db.query(Pathway).count()
        if pathway_count >= 22 and not force:
            print("Database already contains all 22 Pathways and complete organizations data. Skipping initial seeding.")
            return

        if force or pathway_count > 0:
            print("Refreshing and expanding database with all 22 Divine Pathways and organizations...")
            # If refreshing, remove old records to reseed cleanly
            db.query(Claim).delete()
            db.query(Commission).delete()
            db.query(Beyonder).delete()
            db.query(Potion).delete()
            db.query(Pathway).delete()
            db.commit()

        print("Seeding all 22 Pathways to the Divine into Tarot Command Center...")

        # =========================================================================
        # 1. ALL 22 PATHWAYS TO THE DIVINE
        # =========================================================================
        pathways_data = [
            {"name": "Fool", "sequence_0_title": "The Fool"},
            {"name": "Door", "sequence_0_title": "Key of Stars"},
            {"name": "Error", "sequence_0_title": "Error (Marauder)"},
            {"name": "Visionary", "sequence_0_title": "Visionary (Spectator)"},
            {"name": "Hanged Man", "sequence_0_title": "The Hanged Man (Secrets Supplicant)"},
            {"name": "Tyrant", "sequence_0_title": "Tyrant (Lord of Storms)"},
            {"name": "Sun", "sequence_0_title": "Eternal Blazing Sun"},
            {"name": "Darkness", "sequence_0_title": "Darkness (Evernight Goddess)"},
            {"name": "Death", "sequence_0_title": "Death"},
            {"name": "Twilight Giant", "sequence_0_title": "Twilight Giant (God of Combat)"},
            {"name": "Red Priest", "sequence_0_title": "Red Priest (Hunter)"},
            {"name": "Demoness", "sequence_0_title": "Primordial Demoness"},
            {"name": "Paragon", "sequence_0_title": "Paragon (God of Steam & Machinery)"},
            {"name": "Hermit", "sequence_0_title": "Hermit (Mystery Pryer)"},
            {"name": "Wheel of Fortune", "sequence_0_title": "Wheel of Fortune (Monster)"},
            {"name": "Moon", "sequence_0_title": "Moon (Apothecary / Lilith)"},
            {"name": "Mother", "sequence_0_title": "Mother (Earth Mother / Planter)"},
            {"name": "Black Emperor", "sequence_0_title": "Black Emperor (Lawyer)"},
            {"name": "Justiciar", "sequence_0_title": "Justiciar (Arbiter)"},
            {"name": "Chained", "sequence_0_title": "The Chained (Prisoner)"},
            {"name": "Abyss", "sequence_0_title": "Abyss (Father of Devils / Criminal)"},
            {"name": "White Tower", "sequence_0_title": "White Tower (God of Knowledge & Wisdom)"},
        ]

        pathway_objs = {}
        for item in pathways_data:
            p = Pathway(name=item["name"], sequence_0_title=item["sequence_0_title"])
            db.add(p)
            db.flush()
            pathway_objs[item["name"]] = p

        # =========================================================================
        # 2. BEYONDERS ACROSS ALL MAJOR ORGANIZATIONS & FACTIONS
        # =========================================================================
        beyonders_data = [
            # ----------------- TAROT CLUB -----------------
            {
                "pathway": "Fool",
                "codename": "The Fool (Klein Moretti)",
                "sequence_level": 0,
                "sequence_name": "The Fool",
                "sanity_percentage": 94.0,
                "affiliation": "Tarot Club",
                "characteristics": "Master of Sefirah Castle. Controls Spirit Body Threads, historical projections from the Fog of History, miracle granting, grafting concepts, and paper figurine substitutes. Accompanied by Creeping Hunger and Death Kneel."
            },
            {
                "pathway": "Fool",
                "codename": "The World (Gehrman Sparrow)",
                "sequence_level": 4,
                "sequence_name": "Bizarro Sorcerer",
                "sanity_percentage": 88.5,
                "affiliation": "Tarot Club",
                "characteristics": "Klein's premier adventurer persona. Puppeteer who manipulates spirit threads within 100 meters, swapping places instantly with marionettes and paper figures. Cold, ruthless, and deadly precise."
            },
            {
                "pathway": "Visionary",
                "codename": "Justice (Audrey Hall)",
                "sequence_level": 3,
                "sequence_name": "Manipulator",
                "sanity_percentage": 97.0,
                "affiliation": "Tarot Club",
                "characteristics": "The Miss Justice of the Tarot Club. Can manipulate emotional currents, implant psychological cues, weave mental plagues, soothe corrupted minds, and perceive the Sea of Collective Subconscious."
            },
            {
                "pathway": "Tyrant",
                "codename": "The Hanged Man (Alger Wilson)",
                "sequence_level": 3,
                "sequence_name": "Cataclysmic Intercessor",
                "sanity_percentage": 76.5,
                "affiliation": "Tarot Club",
                "characteristics": "Command of hurricane tempests, divine lightning smites, deep ocean acoustic navigation, and aquatic respiration. Cunning strategist wielding sealed pirate artifacts."
            },
            {
                "pathway": "Sun",
                "codename": "The Sun (Derrick Berg)",
                "sequence_level": 3,
                "sequence_name": "Light Seeker",
                "sanity_percentage": 92.0,
                "affiliation": "Tarot Club",
                "characteristics": "Champion from the Forsaken Land of the Gods. Radiates pure unshadowed sunlight, purges wraiths, dispels ancient curses, heals necrotic corruption, and wields the Thunder God's Hammer."
            },
            {
                "pathway": "Door",
                "codename": "The Magician (Fors Wall)",
                "sequence_level": 3,
                "sequence_name": "Wanderer",
                "sanity_percentage": 84.0,
                "affiliation": "Tarot Club",
                "characteristics": "Interstellar and spatial teleportation, door manifestation through conceptual boundaries, record and replicate other Beyonders' mystical spells using her notebook."
            },
            {
                "pathway": "Moon",
                "codename": "The Moon (Emlyn White)",
                "sequence_level": 4,
                "sequence_name": "Shaman King",
                "sanity_percentage": 82.0,
                "affiliation": "Tarot Club",
                "characteristics": "Sanguine nobleman turned Tarot Club attendee. Masters moonlight potions, nature beast summoning, life vitality restoration, and high-tier darkness biological curses."
            },
            {
                "pathway": "Hermit",
                "codename": "The Hermit (Cattleya)",
                "sequence_level": 3,
                "sequence_name": "Clairvoyant",
                "sanity_percentage": 89.0,
                "affiliation": "Tarot Club",
                "characteristics": "Admiral of the Stars and Tarot Club pillar. Deciphers mystical knowledge, casts fairy tale reality distortions, star astrology divination, and eye of mystery prying."
            },
            {
                "pathway": "Darkness",
                "codename": "The Star (Leonard Mitchell)",
                "sequence_level": 4,
                "sequence_name": "Nightwatcher",
                "sanity_percentage": 83.5,
                "affiliation": "Tarot Club",
                "characteristics": "Poetic soul harboring the parasitic Worm of Time (Pallez Zoroast). Pacifies spirits with slumber poetry, manipulates soul dreams, and conceals reality behind night curtains."
            },
            {
                "pathway": "Justiciar",
                "codename": "Judgement (Xio Derecha)",
                "sequence_level": 4,
                "sequence_name": "Imperative Mage",
                "sanity_percentage": 91.0,
                "affiliation": "Tarot Club",
                "characteristics": "Establishes binding order domains: 'Prohibited', 'Imprisonment', and 'Execution'. Subdues chaotic lawbreakers and wields the Law-Enforcing Golden Stave."
            },

            # ----------------- CHURCH OF THE EVERNIGHT GODDESS -----------------
            {
                "pathway": "Darkness",
                "codename": "Amanises (The Evernight Goddess)",
                "sequence_level": 0,
                "sequence_name": "Darkness",
                "sanity_percentage": 99.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "Empress of Horror and Misfortune, Lady of Crimson and Mother of Concealment. Absolute control over night dreams, perpetual serenity, concealment of cosmic secrets, and soul slumber."
            },
            {
                "pathway": "Darkness",
                "codename": "Captain Dunn Smith",
                "sequence_level": 7,
                "sequence_name": "Nightmare",
                "sanity_percentage": 71.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "Captain of the Tingen Nighthawks. Pulls targets into realistic dreams, forces interrogation while sleeping, and consumes characteristics of fallen comrades causing memory lapses."
            },
            {
                "pathway": "Death",
                "codename": "Madam Daly Simone",
                "sequence_level": 6,
                "sequence_name": "Spirit Medium",
                "sanity_percentage": 79.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "High-tier medium of the Nighthawks. Direct communion with wandering spirits and underworld corpses, potion brewing, and spirit dance exorcism."
            },
            {
                "pathway": "Darkness",
                "codename": "Anthony Stevenson",
                "sequence_level": 3,
                "sequence_name": "Horror Bishop",
                "sanity_percentage": 86.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "Archbishop of the Backlund Diocese. Emits dread terror auras, summons deep darkness domains, and invokes the Goddess's holy moon artifact."
            },
            {
                "pathway": "Death",
                "codename": "Frye (Corpse Collector)",
                "sequence_level": 8,
                "sequence_name": "Gravedigger",
                "sanity_percentage": 75.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "Nighthawk specialist who handles decaying cadavers, detects lingering necrotic grudges, possesses chilling frost touch and resistance to spectral venom."
            },
            {
                "pathway": "Darkness",
                "codename": "Crestet Cesario",
                "sequence_level": 4,
                "sequence_name": "Nightwatcher",
                "sanity_percentage": 87.0,
                "affiliation": "Church of Evernight Goddess",
                "characteristics": "Senior Commander of the Red Gloves elite strike force. Master of shadow infiltration, concealment barriers, and rapid containment of high-tier supernatural anomalies."
            },

            # ----------------- CHURCH OF THE LORD OF STORMS -----------------
            {
                "pathway": "Tyrant",
                "codename": "Lord of Storms (Leodero)",
                "sequence_level": 0,
                "sequence_name": "Tyrant",
                "sanity_percentage": 93.0,
                "affiliation": "Church of Lord of Storms",
                "characteristics": "God of Seas, Storms, and Thunder. Total dominion over the planet's atmospheric currents, summoning world-ending tempests, oceanic maelstroms, and blinding lightning judgements."
            },
            {
                "pathway": "Tyrant",
                "codename": "Archbishop Spinnat",
                "sequence_level": 3,
                "sequence_name": "Cataclysmic Intercessor",
                "sanity_percentage": 74.0,
                "affiliation": "Church of Lord of Storms",
                "characteristics": "Commander of the Mandated Punishers in Backlund. Chants lightning bolts capable of shattering warships, creates tidal whirlpools, and leads punitive maritime inquisitions."
            },
            {
                "pathway": "Tyrant",
                "codename": "Captain Sharon (Mandated Punisher)",
                "sequence_level": 7,
                "sequence_name": "Seafarer",
                "sanity_percentage": 80.0,
                "affiliation": "Church of Lord of Storms",
                "characteristics": "Commands wind propulsion for gunboats, underwater combat prowess, acoustic navigation, and electrical shock punches."
            },

            # ----------------- CHURCH OF GOD OF STEAM AND MACHINERY -----------------
            {
                "pathway": "Paragon",
                "codename": "God of Steam and Machinery",
                "sequence_level": 0,
                "sequence_name": "Paragon",
                "sanity_percentage": 96.0,
                "affiliation": "Church of God of Steam and Machinery",
                "characteristics": "The divine inventor of industrial civilization. Omniscient mastery over all physical laws, mechanical apparatuses, metallurgy, steam golems, and technological innovation."
            },
            {
                "pathway": "Paragon",
                "codename": "Archbishop Horamick Haydn",
                "sequence_level": 3,
                "sequence_name": "Arcane Scholar",
                "sanity_percentage": 88.0,
                "affiliation": "Church of God of Steam and Machinery",
                "characteristics": "Backlund Diocese Archbishop and chief scientist. Constructs hyper-advanced steam weaponry, mathematical ward lattices, and mechanized autonomous battle automatons."
            },
            {
                "pathway": "Paragon",
                "codename": "Ikers Sanchez",
                "sequence_level": 7,
                "sequence_name": "Astomizer",
                "sanity_percentage": 83.0,
                "affiliation": "Church of God of Steam and Machinery",
                "characteristics": "Machinery Hivemind Captain. Expert in dismantling sealed artifact traps, crafting precision steam revolvers, alchemy bullets, and structural detonation."
            },

            # ----------------- CHURCH OF THE EARTH MOTHER -----------------
            {
                "pathway": "Mother",
                "codename": "Earth Mother (Lilith)",
                "sequence_level": 0,
                "sequence_name": "Mother",
                "sanity_percentage": 98.0,
                "affiliation": "Church of Earth Mother",
                "characteristics": "Ancient deity holding the dual authorities of Life, Fertility, and the Crimson Moon. Supreme creation and mutation of biological lifeforms and bountiful natural harvest."
            },
            {
                "pathway": "Twilight Giant",
                "codename": "Father Utravsky",
                "sequence_level": 4,
                "sequence_name": "Demon Hunter",
                "sanity_percentage": 78.0,
                "affiliation": "Church of Earth Mother",
                "characteristics": "Giant priest of the Harvest Church in Backlund. Towering 3-meter physical stature, dawn aura sword projection, demonic weakness discernment, and repentant spiritual composure."
            },
            {
                "pathway": "Mother",
                "codename": "Frank Lee (Mad Botanist)",
                "sequence_level": 5,
                "sequence_name": "Druid",
                "sanity_percentage": 65.0,
                "affiliation": "Church of Earth Mother",
                "characteristics": "Infamous botanical alchemist. Crossbreeds cows with mushrooms, creates carnivorous wheat, self-reproducing fish, and terrifying chimeric organisms that frighten even pirate admirals."
            },

            # ----------------- CHURCH OF THE ETERNAL BLAZING SUN -----------------
            {
                "pathway": "Sun",
                "codename": "Eternal Blazing Sun (Aucuses)",
                "sequence_level": 0,
                "sequence_name": "Eternal Blazing Sun",
                "sanity_percentage": 95.0,
                "affiliation": "Church of Eternal Blazing Sun",
                "characteristics": "The pure manifestation of the sun. Purges all filth, corruption, unholy undead, and shadows. Casts Unshadowed Spears and absolute purifying holy halos."
            },
            {
                "pathway": "Sun",
                "codename": "Inquisitor Vaneuer",
                "sequence_level": 4,
                "sequence_name": "Unshadowed",
                "sanity_percentage": 82.0,
                "affiliation": "Church of Eternal Blazing Sun",
                "characteristics": "High Inquisitor of the Sun church. Exorcises heretical spirits, strips curses, commands purifying solar coronas, and conducts solemn heretic purges."
            },

            # ----------------- CHURCH OF THE GOD OF KNOWLEDGE & WISDOM -----------------
            {
                "pathway": "White Tower",
                "codename": "God of Knowledge and Wisdom (Herabergen)",
                "sequence_level": 0,
                "sequence_name": "White Tower",
                "sanity_percentage": 97.0,
                "affiliation": "Church of God of Knowledge and Wisdom",
                "characteristics": "Omniscient deity of truth, learning, and analysis. Can replicate, analyze, and counter any supernatural ability, predicting tactical outcomes through divine deduction."
            },
            {
                "pathway": "White Tower",
                "codename": "Edwina Edwards (Vice Admiral Iceberg)",
                "sequence_level": 5,
                "sequence_name": "Polymath",
                "sanity_percentage": 93.0,
                "affiliation": "Church of God of Knowledge and Wisdom",
                "characteristics": "Captain of the Golden Dream and honorary scholar. Imparts lessons to pirate crew, analyzes mystical texts, and casts mirrored ice and fiery spells using copied formulas."
            },

            # ----------------- PIRATES: FOUR KINGS & SEVEN ADMIRALS -----------------
            {
                "pathway": "Black Emperor",
                "codename": "Nast Salomon (King of Five Seas)",
                "sequence_level": 2,
                "sequence_name": "Duke of the Fallen",
                "sanity_percentage": 81.0,
                "affiliation": "Pirates (Five Seas)",
                "characteristics": "Supreme ruler of the pirate realm aboard the ghost flagship 'Black Emperor'. Exploits order loopholes, establishes distorted tyrannical laws, and dominates maritime trade."
            },
            {
                "pathway": "Death",
                "codename": "Agalgalos (King of Immortality)",
                "sequence_level": 2,
                "sequence_name": "Death Consul",
                "sanity_percentage": 68.0,
                "affiliation": "Pirates (Five Seas)",
                "characteristics": "Ancient immortal pirate monarch. Commands ghost fleets, summons skeleton legions from the underworld, and rots living flesh upon glance."
            },
            {
                "pathway": "Demoness",
                "codename": "Tracy (Vice Admiral Disease)",
                "sequence_level": 4,
                "sequence_name": "Despair Demoness",
                "sanity_percentage": 73.0,
                "affiliation": "Pirates (Five Seas)",
                "characteristics": "Captain of the Black Death. Spreads airborne black plagues, invisible thread strangulation, frost curses, and seductive charm magic."
            },
            {
                "pathway": "Red Priest",
                "codename": "Blazing Danitz",
                "sequence_level": 7,
                "sequence_name": "Pyromaniac",
                "sanity_percentage": 88.0,
                "affiliation": "Pirates (Five Seas)",
                "characteristics": "Golden Dream fourth mate and Gehrman Sparrow's reluctant attendant. Hurls blazing fireballs, magma jets, and possesses enhanced physical brawling."
            },
            {
                "pathway": "Red Priest",
                "codename": "Anderson Hood (Strongest Hunter)",
                "sequence_level": 5,
                "sequence_name": "Reaper",
                "sanity_percentage": 80.0,
                "affiliation": "Pirates (Five Seas)",
                "characteristics": "Top hunter of the Fog Sea. Can pinpoint and strike lethal anatomical weaknesses, wielding flame swords and an irrepressible provocative tongue."
            },

            # ----------------- CITY OF SILVER -----------------
            {
                "pathway": "Twilight Giant",
                "codename": "Colin Iliad (Chief of City of Silver)",
                "sequence_level": 4,
                "sequence_name": "Demon Hunter",
                "sanity_percentage": 85.0,
                "affiliation": "City of Silver",
                "characteristics": "Legendary Chief of the Six-Member Council. Dual-wields silver holy swords coated in exorcism oils, discerns mythological creature weak spots, and protects the cursed bastion."
            },
            {
                "pathway": "Hanged Man",
                "codename": "Lovia (Elder of the Council)",
                "sequence_level": 4,
                "sequence_name": "Black Knight",
                "sanity_percentage": 52.0,
                "affiliation": "City of Silver",
                "characteristics": "Elder grazing the souls of ancient spirits and demonic knights. Projects shadowy degradation swords and endures heavy mental whispers from the True Creator."
            },

            # ----------------- AURORA ORDER -----------------
            {
                "pathway": "Hanged Man",
                "codename": "The True Creator",
                "sequence_level": 0,
                "sequence_name": "The Hanged Man",
                "sanity_percentage": 25.0,
                "affiliation": "Aurora Order",
                "characteristics": "The Fallen Creator and source of madness. Extreme degradation flesh corruption, shadow depravity, listening ravings that drive mortals mad, and absolute soul grazing."
            },
            {
                "pathway": "Hanged Man",
                "codename": "Mr. A (Oracle)",
                "sequence_level": 5,
                "sequence_name": "Shepherd",
                "sanity_percentage": 42.0,
                "affiliation": "Aurora Order",
                "characteristics": "Backlund Oracle of the Aurora Order. Grazes multiple souls simultaneously to unleash diverse abilities (teleportation, holy light, shadow flesh), dressed in hooded blood robes."
            },
            {
                "pathway": "Hanged Man",
                "codename": "Mr. Z (Oracle)",
                "sequence_level": 5,
                "sequence_name": "Shepherd",
                "sanity_percentage": 46.0,
                "affiliation": "Aurora Order",
                "characteristics": "Southern Continent Oracle orchestrating heretical rituals and biological flesh sacrifices in service of the divine True Creator."
            },

            # ----------------- SECRET ORDER -----------------
            {
                "pathway": "Fool",
                "codename": "Zaratul (Leader of Secret Order)",
                "sequence_level": 1,
                "sequence_name": "Attendant of Mysteries",
                "sanity_percentage": 73.0,
                "affiliation": "Secret Order",
                "characteristics": "Ancient angel of the Zaratul family. Weaves vortexes of Spirit Body Threads, historical void summoning, transformation miracles, and wishes."
            },
            {
                "pathway": "Fool",
                "codename": "Rosago (Secret Order Operative)",
                "sequence_level": 5,
                "sequence_name": "Marionettist",
                "sanity_percentage": 68.0,
                "affiliation": "Secret Order",
                "characteristics": "Subversive operative who uses a Mutated Eye artifact to paralyze spirit body threads, turning targets into obedient wooden puppets within minutes."
            },

            # ----------------- ROSE SCHOOL OF THOUGHT -----------------
            {
                "pathway": "Chained",
                "codename": "Abomination Suah",
                "sequence_level": 1,
                "sequence_name": "Abomination",
                "sanity_percentage": 28.0,
                "affiliation": "Rose School of Thought - Indulgence Faction",
                "characteristics": "Son of the Chained God. Giant tree of rotten flesh, eyes, and bone spikes. Radiates intense corruption curses, malignant festering wounds, and extreme sadism."
            },
            {
                "pathway": "Chained",
                "codename": "Miss Sharron",
                "sequence_level": 4,
                "sequence_name": "Puppet",
                "sanity_percentage": 87.0,
                "affiliation": "Rose School of Thought - Temperance Faction",
                "characteristics": "Pale doll-like maiden advocating ascetic restraint. Can turn intangible like a wraith, possess enemy bodies, mirror leap, and construct cursed voodoo effigies."
            },
            {
                "pathway": "Chained",
                "codename": "Maric (Zombie)",
                "sequence_level": 5,
                "sequence_name": "Wraith",
                "sanity_percentage": 69.0,
                "affiliation": "Rose School of Thought - Temperance Faction",
                "characteristics": "Controls zombie corpses through playing cards, suppresses internal feral bloodlust through restraint, possesses freezing touch and supernatural resilience."
            },
            {
                "pathway": "Chained",
                "codename": "Reinette Tinekerr (Miss Messenger)",
                "sequence_level": 2,
                "sequence_name": "Ancient Bane",
                "sanity_percentage": 90.0,
                "affiliation": "Rose School of Thought - Temperance Faction",
                "characteristics": "Ancient spirit world angel appearing as a headless doll carrying four blonde heads. Casts dreadful curses, spirit thread manipulation, and demands gold coin delivery fees."
            },

            # ----------------- DEMONESS SECT -----------------
            {
                "pathway": "Demoness",
                "codename": "Primordial Demoness (Cheek)",
                "sequence_level": 0,
                "sequence_name": "Primordial Demoness",
                "sanity_percentage": 30.0,
                "affiliation": "Demoness Sect",
                "characteristics": "The source of apocalyptic disaster, petrification, pestilence, and corruption. Can turn entire continents into barren wastelands and freeze souls in agony."
            },
            {
                "pathway": "Demoness",
                "codename": "Panatiya (Saint of Disaster)",
                "sequence_level": 3,
                "sequence_name": "Unaging Demoness",
                "sanity_percentage": 64.0,
                "affiliation": "Demoness Sect",
                "characteristics": "Youthful beauty untouched by time. Spreads invisible airborne epidemics, poisonous spider silk, mirrors of petrification, and soul-draining charms."
            },
            {
                "pathway": "Demoness",
                "codename": "Madam Sharon",
                "sequence_level": 6,
                "sequence_name": "Pleasure Demoness",
                "sanity_percentage": 62.0,
                "affiliation": "Demoness Sect",
                "characteristics": "Backlund high-society socialite who ensnares noble politicians through aphrodisiacs, mirror substitution illusions, and necromantic soul sacrifices."
            },

            # ----------------- PSYCHOLOGY ALCHEMISTS -----------------
            {
                "pathway": "Visionary",
                "codename": "Hermes (Ancient Scholar)",
                "sequence_level": 2,
                "sequence_name": "Discerner",
                "sanity_percentage": 88.0,
                "affiliation": "Psychology Alchemists",
                "characteristics": "Creator of the Hermes language and founder of Psychology Alchemists. Manipulates world consciousness, psychological cue programming, and weaves collective dreams."
            },
            {
                "pathway": "Visionary",
                "codename": "Hevin Rambis",
                "sequence_level": 3,
                "sequence_name": "Manipulator",
                "sanity_percentage": 70.0,
                "affiliation": "Psychology Alchemists",
                "characteristics": "Backlund court counselor infiltrating the Loen royal family. Plants subconscious mental commands, incites emotional panic, and induces psychological hypnosis."
            },

            # ----------------- AMON FAMILY (TIME MARAUDERS) -----------------
            {
                "pathway": "Error",
                "codename": "Amon (Angel of Time)",
                "sequence_level": 0,
                "sequence_name": "Error",
                "sanity_percentage": 78.0,
                "affiliation": "Amon Family",
                "characteristics": "The Blasphemer wearing a crystal monocle on the right eye. Steals thoughts, memories, destiny, lifespan, abilities, and replicates countless avatar clones."
            },
            {
                "pathway": "Error",
                "codename": "Pallez Zoroast (Old Man)",
                "sequence_level": 1,
                "sequence_name": "Worm of Time",
                "sanity_percentage": 85.0,
                "affiliation": "Amon Family",
                "characteristics": "Grandpa parasitic angel residing inside Leonard Mitchell's emerald ring. Parasitizes souls, slows enemy time perception, steals distance, and provides ancient guidance."
            },

            # ----------------- ABRAHAM FAMILY -----------------
            {
                "pathway": "Door",
                "codename": "Bethel Abraham (Mr. Door)",
                "sequence_level": 0,
                "sequence_name": "Key of Stars",
                "sanity_percentage": 35.0,
                "affiliation": "Abraham Family",
                "characteristics": "King of Angels trapped in cosmic exile beyond the astral seal. Can open doors to any celestial coordinate, conceptual seal breaking, and cosmos replication."
            },
            {
                "pathway": "Door",
                "codename": "Dorian Gray Abraham",
                "sequence_level": 7,
                "sequence_name": "Astrologer",
                "sanity_percentage": 86.0,
                "affiliation": "Abraham Family",
                "characteristics": "Head of Pritz Harbor branch and Fors Wall's teacher. Skilled in unlocking wards, space displacement, astrological fortune reading, and family relic curation."
            },

            # ----------------- CHURCH OF GOD OF COMBAT -----------------
            {
                "pathway": "Twilight Giant",
                "codename": "God of Combat (Badheil)",
                "sequence_level": 0,
                "sequence_name": "Twilight Giant",
                "sanity_percentage": 91.0,
                "affiliation": "Church of God of Combat",
                "characteristics": "Patron deity of the Feysac Empire. Wields the Twilight Light of withering decay, absolute impenetrable armor, and colossal divine swordsmanship."
            },
            {
                "pathway": "Twilight Giant",
                "codename": "Archbishop Larrion",
                "sequence_level": 2,
                "sequence_name": "Glory Golem",
                "sanity_percentage": 84.0,
                "affiliation": "Church of God of Combat",
                "characteristics": "Feysac imperial high priest commanding heavy armored vanguard paladins, radiating twilight decaying radiance and fortress stone barriers."
            },

            # ----------------- IRON AND BLOOD CROSS ORDER -----------------
            {
                "pathway": "Red Priest",
                "codename": "Gardner Martin",
                "sequence_level": 4,
                "sequence_name": "Iron-blooded Knight",
                "sanity_percentage": 77.0,
                "affiliation": "Iron and Blood Cross Order",
                "characteristics": "Chief of the Iron and Blood Cross Order. Links soldier souls into an unyielding collective formation, throws devastating iron spears, and commands military arson."
            },

            # ----------------- MI9 & ROYAL FAMILIES -----------------
            {
                "pathway": "Black Emperor",
                "codename": "Qonas Kilgor",
                "sequence_level": 4,
                "sequence_name": "Earl of the Fallen",
                "sanity_percentage": 76.0,
                "affiliation": "MI9 & Royal Families",
                "characteristics": "Deputy Director of Military Intelligence 9. Enacts bribe distortion, magnifies enemy minor infractions into treason, and wields royal decree sealed artifacts."
            },

            # ----------------- LIFE SCHOOL OF THOUGHT -----------------
            {
                "pathway": "Wheel of Fortune",
                "codename": "Will Auceptin (Snake of Mercury)",
                "sequence_level": 1,
                "sequence_name": "Snake of Mercury",
                "sanity_percentage": 94.0,
                "affiliation": "Life School of Thought",
                "characteristics": "Currently reincarnating as a human infant who loves ice cream. Commands the river of probability, gives absolute good luck or fatal misfortune, and restarts local timelines."
            },
            {
                "pathway": "Wheel of Fortune",
                "codename": "Aaron Ceres (Surgeon Affiliate)",
                "sequence_level": 9,
                "sequence_name": "Monster",
                "sanity_percentage": 89.0,
                "affiliation": "Life School of Thought",
                "characteristics": "Surgeon in Backlund associated with Will Auceptin. Has eerie premonitions of danger, hears erratic whispers of fate, and senses anomalous luck fluctuations."
            },

            # ----------------- MOSES ASCETIC ORDER & ELEMENT DAWN -----------------
            {
                "pathway": "Hermit",
                "codename": "Bernadette Gustav (Queen Mystic)",
                "sequence_level": 2,
                "sequence_name": "Sage",
                "sanity_percentage": 92.0,
                "affiliation": "Moses Ascetic Order & Element Dawn",
                "characteristics": "Daughter of Emperor Roselle Gustav and founder of Element Dawn. Weaves reality from fairy tales ('Cinderella', 'Matchstick Girl'), wields the Sage's Eye and ancient sage wisdom."
            },

            # ----------------- DEVIL FAMILIES & BLOOD SANCTUM -----------------
            {
                "pathway": "Abyss",
                "codename": "Farbauti (Father of Devils)",
                "sequence_level": 0,
                "sequence_name": "Abyss",
                "sanity_percentage": 20.0,
                "affiliation": "Devil Families & Blood Sanctum",
                "characteristics": "Ancient evil deity dwelling in the Abyss. Embodies ultimate malice, demonic magma sulfur, bloodlust contagion, and irreversible soul damnation."
            },
            {
                "pathway": "Abyss",
                "codename": "Jason Beria (Backlund Serial Killer)",
                "sequence_level": 6,
                "sequence_name": "Devil",
                "sanity_percentage": 34.0,
                "affiliation": "Devil Families & Blood Sanctum",
                "characteristics": "Cold-blooded butcher in East Borough. Detects human hatred, exudes toxic sulfur breath, immune to cold and fire, and drinks sacrificial victim blood."
            }
        ]

        for item in beyonders_data:
            p_name = item["pathway"]
            if p_name in pathway_objs:
                b = Beyonder(
                    pathway_id=pathway_objs[p_name].id,
                    codename=item["codename"],
                    sequence_level=item["sequence_level"],
                    sequence_name=item["sequence_name"],
                    sanity_percentage=item["sanity_percentage"],
                    affiliation=item["affiliation"],
                    characteristics=item["characteristics"]
                )
                db.add(b)

        # =========================================================================
        # 3. POTION CODEX RECIPES FOR ALL 22 PATHWAYS (Rich Alchemy Details)
        # =========================================================================
        potions_data = [
            # 1. Fool (Seer)
            {
                "pathway": "Fool", "sequence_level": 9,
                "main_ingredients": "100ml Pure Water, 5 drops of Night Vanilla Juice, 1 Secret Seer Spirit Gland",
                "supplementary_ingredients": "3 drops of Mint Juice, 5g Coagulated Lavender Powder",
                "abilities": "Seer: Enhanced spiritual intuition, spirit vision, astromancy, tarot divination, danger premonition."
            },
            {
                "pathway": "Fool", "sequence_level": 7,
                "main_ingredients": "Crystal Gland of a Phantom Crystal Spider, 30ml Blood of a Faceless Hound",
                "supplementary_ingredients": "100ml Pure Water, 5g Star Crystal Powder",
                "abilities": "Magician: Damage transfer, paper figurine substitute, flame controlling, air bullets, bone softening."
            },
            {
                "pathway": "Fool", "sequence_level": 4,
                "main_ingredients": "Bizarro Demonic Spider Eye, Core of a Shape-shifter Tree",
                "supplementary_ingredients": "100ml Fog Essence, 5g Void Dust",
                "abilities": "Bizarro Sorcerer: Manipulation of Spirit Body Threads into puppets, instant spatial substitution with marionettes."
            },

            # 2. Door (Apprentice)
            {
                "pathway": "Door", "sequence_level": 9,
                "main_ingredients": "1 Core of a Wandering Spirit, 20ml Moon Flower Liquid",
                "supplementary_ingredients": "50ml Pure Water, 5g Star Silver Dust",
                "abilities": "Apprentice: Door opening trickery, phase through solid masonry walls, unlock physical mechanisms."
            },
            {
                "pathway": "Door", "sequence_level": 4,
                "main_ingredients": "Astral Hound Heart, Core Crystal of a Star Devourer",
                "supplementary_ingredients": "100ml Starlight Water, 5g Cosmic Dust",
                "abilities": "Secrets Sorcerer: Manifest conceptual doors across dimensions, banish enemies into void chasms."
            },

            # 3. Error (Marauder)
            {
                "pathway": "Error", "sequence_level": 9,
                "main_ingredients": "Single Eyeball of a Swift Shadow Fox, 10g Thieving Magpie Feather",
                "supplementary_ingredients": "50ml Pure Alcohol, 5 drops of Snake Oil",
                "abilities": "Marauder: Deft fingers, steal physical items effortlessly, detect weakness and structural flaws."
            },
            {
                "pathway": "Error", "sequence_level": 4,
                "main_ingredients": "Parasitic Worm Gland, Core of an Illusionary Clock",
                "supplementary_ingredients": "50ml Essence of Time, 10g Gold Leaf Powder",
                "abilities": "Parasite: Implant spirit worms into foreign souls, steal thoughts, memories, and short spans of time."
            },

            # 4. Visionary (Spectator)
            {
                "pathway": "Visionary", "sequence_level": 9,
                "main_ingredients": "Eye of a Mind Dragon, 10ml Dreamland Dew",
                "supplementary_ingredients": "50ml Pure Water, 3g Lavender Dust",
                "abilities": "Spectator: Keen observation of micro-expressions, body language, emotional aura reading."
            },
            {
                "pathway": "Visionary", "sequence_level": 4,
                "main_ingredients": "Heart of a Nightmare Dragon, Brain Fluid of a Dream Weaver",
                "supplementary_ingredients": "100ml Pure Dream Water, 10g Soothing Powder",
                "abilities": "Manipulator: Implant subconscious mental cues, weave dreamscapes, soothe madness, and project mental plagues."
            },

            # 5. Hanged Man (Secrets Supplicant)
            {
                "pathway": "Hanged Man", "sequence_level": 9,
                "main_ingredients": "Blood of a Deep Sea Eel, 1 Dried Flesh of a Murmuring Spectre",
                "supplementary_ingredients": "50ml Dark Spring Water, 5g Bone Ash",
                "abilities": "Secrets Supplicant: Hears ancient divine secrets, withstands corruption ravings, senses hidden occult dangers."
            },
            {
                "pathway": "Hanged Man", "sequence_level": 5,
                "main_ingredients": "Core Gland of an Aurora Predator, 50ml Flesh of a Devourer",
                "supplementary_ingredients": "100ml Rotten Holy Water, 10g Soul Powder",
                "abilities": "Shepherd: Grazes the souls of dead Beyonders inside body flesh, deploying their supernatural abilities at will."
            },

            # 6. Tyrant (Sailor)
            {
                "pathway": "Tyrant", "sequence_level": 9,
                "main_ingredients": "Scale of a Deep Sea Siren, 20ml Blood of a Blue Ring Octopus",
                "supplementary_ingredients": "100ml Seawater, 5g Kelp Salt",
                "abilities": "Sailor: Superhuman balance on stormy seas, aquatic swimming speed, night vision in murky water."
            },
            {
                "pathway": "Tyrant", "sequence_level": 4,
                "main_ingredients": "Thunder Dragon Feather, Heart of a Giant Sea Maelstrom Serpent",
                "supplementary_ingredients": "100ml Heavy Water, 10g Electric Ore Dust",
                "abilities": "Cataclysmic Intercessor: Summons massive thunderstorm smites, commands tidal waves, flies via storm winds."
            },

            # 7. Sun (Bard)
            {
                "pathway": "Sun", "sequence_level": 9,
                "main_ingredients": "Petal of a Sunflower of Light, 1 Feather of a Dawn Canary",
                "supplementary_ingredients": "50ml Pure Morning Dew, 3g Golden Sand",
                "abilities": "Bard: Sings uplifting holy hymns, boosts comrades' morale and vitality, dispels gloomy fatigue."
            },
            {
                "pathway": "Sun", "sequence_level": 4,
                "main_ingredients": "Crown of a Sun Phoenix, Liquid Heart of a Radiant Drake",
                "supplementary_ingredients": "100ml Holy Solar Water, 10g Gold Leaf Flakes",
                "abilities": "Unshadowed: Exorcises and incinerates all curses, unholy spectres, and demonic taint with blinding solar corona."
            },

            # 8. Darkness (Sleepless)
            {
                "pathway": "Darkness", "sequence_level": 9,
                "main_ingredients": "Tears of a Slumber Toad, 10g Herb of the Midnight Blossom",
                "supplementary_ingredients": "50ml Night Sky Dew, 5g Poppy Flower Dust",
                "abilities": "Sleepless: Needs only 2 hours of sleep, enhanced sensory perception and reflexes in darkness."
            },
            {
                "pathway": "Darkness", "sequence_level": 4,
                "main_ingredients": "Feather of an Underworld Falcon, Core of a Midnight Beast",
                "supplementary_ingredients": "100ml Holy Night Water, 10g Obsidian Dust",
                "abilities": "Nightwatcher: Casts darkness concealment domes, puts armies into deep hypnotic slumber, controls dreams."
            },

            # 9. Death (Corpse Collector)
            {
                "pathway": "Death", "sequence_level": 9,
                "main_ingredients": "Essence of a Grave Lily, 10ml Embalming Fluid of an Ancient Mummy",
                "supplementary_ingredients": "50ml Tomb Water, 5g Coffin Wood Ash",
                "abilities": "Corpse Collector: Immunity to corpse poison, detects residual grudges in dead bodies, senses undead entities."
            },
            {
                "pathway": "Death", "sequence_level": 4,
                "main_ingredients": "Soul Flame of an Underworld Lich, Bone of a Skeletal Dragon",
                "supplementary_ingredients": "100ml River of the Underworld, 10g Tomb Dust",
                "abilities": "Undying: Resurrects upon physical death after shedding a dead husk, commands legions of skeletons."
            },

            # 10. Twilight Giant (Warrior)
            {
                "pathway": "Twilight Giant", "sequence_level": 9,
                "main_ingredients": "Horn of a Rhinoceros Beast, 20ml Blood of an Iron Bear",
                "supplementary_ingredients": "50ml Pure Spring Water, 5g Iron Ore Powder",
                "abilities": "Warrior: Extreme physical constitution, mastery of all melee weaponry, skin as durable as leather."
            },
            {
                "pathway": "Twilight Giant", "sequence_level": 4,
                "main_ingredients": "Heart of a Twilight Demon, Core of a Silver Dawn Golem",
                "supplementary_ingredients": "100ml Molten Silver Liquid, 10g Dawn Ash",
                "abilities": "Demon Hunter: Crafts magical demon-bane oils, projects Dawn Light greatswords, detects mythological weak points."
            },

            # 11. Red Priest (Hunter)
            {
                "pathway": "Red Priest", "sequence_level": 9,
                "main_ingredients": "Scent Gland of a Red Fox, 1 Tooth of a Bloodhound",
                "supplementary_ingredients": "50ml Pure Spirit Alcohol, 5g Sulfur Powder",
                "abilities": "Hunter: Tracking footmarks, tactical trap setting, acute environmental survival and terrain reading."
            },
            {
                "pathway": "Red Priest", "sequence_level": 4,
                "main_ingredients": "Blood of a Magma Titan, Heart of an Iron-blooded Warhorse",
                "supplementary_ingredients": "100ml Volcanic Spring Water, 10g Steel Dust",
                "abilities": "Iron-blooded Knight: Telepathically links military formations, commands explosive firestorms and iron spears."
            },

            # 12. Demoness (Assassin)
            {
                "pathway": "Demoness", "sequence_level": 9,
                "main_ingredients": "Poison Gland of an Agate Spider, 10ml Night Shade Extract",
                "supplementary_ingredients": "50ml Distilled Water, 5g Silver Powder",
                "abilities": "Assassin: Shadow blending, silent stalking, lethal pressure point strikes, agile acrobatics."
            },
            {
                "pathway": "Demoness", "sequence_level": 4,
                "main_ingredients": "Eye of a Frost Medusa, Core Gland of a Plague Queen",
                "supplementary_ingredients": "100ml Ice Spring Water, 10g Black Silk Ash",
                "abilities": "Despair Demoness: Spreads fatal black airborne pestilence, petrifies living flesh via mirrors, weaves invisible silk."
            },

            # 13. Paragon (Savant)
            {
                "pathway": "Paragon", "sequence_level": 9,
                "main_ingredients": "1 Brain Gland of an Electric Owl, 10ml Copper Sulfate Liquid",
                "supplementary_ingredients": "50ml Mineral Oil, 5g Fine Brass Shavings",
                "abilities": "Savant: Photographic memory, mastery of mechanical structures, mathematical calculation and drafting."
            },
            {
                "pathway": "Paragon", "sequence_level": 4,
                "main_ingredients": "Core of a Steam Reactor golem, Brain of an Alchemical Chimera",
                "supplementary_ingredients": "100ml Liquid Mercury, 10g Platinum Dust",
                "abilities": "Alchemist / Arcane Scholar: Imbues inanimate mechanisms with magical logic, crafts steam automatons and energy wards."
            },

            # 14. Hermit (Mystery Pryer)
            {
                "pathway": "Hermit", "sequence_level": 9,
                "main_ingredients": "Eye of an Owl of Secrets, 10g Starlight Grass Powder",
                "supplementary_ingredients": "50ml Pure Water, 5g Amethyst Powder",
                "abilities": "Mystery Pryer: Sees magical emanations and spirit flows, studies ritualistic alchemy and hidden occult laws."
            },
            {
                "pathway": "Hermit", "sequence_level": 4,
                "main_ingredients": "Brain of a Dream Sphinx, Star Crystal of the Astral Sea",
                "supplementary_ingredients": "100ml Starlight Water, 10g Emerald Dust",
                "abilities": "Mysticologist: Manifests fairy tale laws into physical reality, crafts mystical scrolls, and prys cosmic secrets."
            },

            # 15. Wheel of Fortune (Monster)
            {
                "pathway": "Wheel of Fortune", "sequence_level": 9,
                "main_ingredients": "Eye of a Two-headed Viper, 10ml Clover Nectar",
                "supplementary_ingredients": "50ml River Water, 3g Quicksilver",
                "abilities": "Monster: Hears erratic whispers of fate, suffers involuntary premonitions, senses impending disasters."
            },
            {
                "pathway": "Wheel of Fortune", "sequence_level": 4,
                "main_ingredients": "Scale of a Mercury Dragon, Core of an Astral Dice",
                "supplementary_ingredients": "100ml Pure Liquid Silver, 10g Fortune Flower Ash",
                "abilities": "Misfortune Mage: Rewrites luck probability, bestowing catastrophic bad luck on enemies and miraculous survival on self."
            },

            # 16. Moon (Apothecary)
            {
                "pathway": "Moon", "sequence_level": 9,
                "main_ingredients": "Extract of Crimson Lily, 1 Horn of a Mandrake Root",
                "supplementary_ingredients": "50ml Moon Water, 5g Dried Blood Powder",
                "abilities": "Apothecary: Diagnoses diseases, brews curative potions, heals wounds, crafts mystical aphrodisiacs."
            },
            {
                "pathway": "Moon", "sequence_level": 4,
                "main_ingredients": "Heart of a Sanguine Elder, Core of a Moonlight Beast",
                "supplementary_ingredients": "100ml Crimson Moon Essence, 10g Silver Dust",
                "abilities": "Shaman King: Casts high-order darkness curses, summons spirit beasts, channels moonlight vitality regeneration."
            },

            # 17. Mother (Planter)
            {
                "pathway": "Mother", "sequence_level": 9,
                "main_ingredients": "Seed of a Giant World Tree, 10ml Sap of a Life Vine",
                "supplementary_ingredients": "100ml Rich Loam Water, 5g Compost Ash",
                "abilities": "Planter: Promotes plant germination, tames wild flora, detects soil vitality and toxic blights."
            },
            {
                "pathway": "Mother", "sequence_level": 4,
                "main_ingredients": "Heart of a Living Ent, Core Crystal of an Earth Spirit",
                "supplementary_ingredients": "100ml Vitality Sap, 10g Fertile Soil Powder",
                "abilities": "Classical Alchemist: Crossbreeds divergent biological species, accelerates mutations, creates chimeric lifeforms."
            },

            # 18. Black Emperor (Lawyer)
            {
                "pathway": "Black Emperor", "sequence_level": 9,
                "main_ingredients": "Tongue of a Silver Mockingbird, 10ml Venom of a Golden Scorpion",
                "supplementary_ingredients": "50ml Pure Water, 5g Red Sealing Wax Dust",
                "abilities": "Lawyer: Finds loopholes in laws, rules, and arguments; persuasive speech that disorients targets."
            },
            {
                "pathway": "Black Emperor", "sequence_level": 4,
                "main_ingredients": "Heart of a Tyrant Behemoth, Core of a Corrupted Law Stone",
                "supplementary_ingredients": "100ml Imperial Wine, 10g Gold Leaf",
                "abilities": "Earl of the Fallen: Magnifies minor faults into fatal errors, distorts enemy spells, commands bribe submissions."
            },

            # 19. Justiciar (Arbiter)
            {
                "pathway": "Justiciar", "sequence_level": 9,
                "main_ingredients": "Gland of a Golden Scales Lizard, 1 Feather of an Eagle of Order",
                "supplementary_ingredients": "50ml Spring Water, 5g Marble Dust",
                "abilities": "Arbiter: Commanding aura of authoritative presence, settles disputes, physically subdues chaotic brawlers."
            },
            {
                "pathway": "Justiciar", "sequence_level": 4,
                "main_ingredients": "Heart of a Judgement Gryphon, Core of an Oath Monument",
                "supplementary_ingredients": "100ml Holy Order Water, 10g Iron Dust",
                "abilities": "Imperative Mage: Decrees absolute binding territorial laws ('Prohibited', 'Execution', 'Imprisonment')."
            },

            # 20. Chained (Prisoner)
            {
                "pathway": "Chained", "sequence_level": 9,
                "main_ingredients": "Heart of a Cursed Wolf, 1 Chain Link soaked in Prisoner Tears",
                "supplementary_ingredients": "50ml Cold Spring Water, 5g Rusty Iron Shavings",
                "abilities": "Prisoner: Endures extreme pain and confinement, bursts into berserk supernatural physical strength."
            },
            {
                "pathway": "Chained", "sequence_level": 4,
                "main_ingredients": "Heart of a Shadow Wraith, Blood of a Petrified Effigy",
                "supplementary_ingredients": "100ml Gloomy Water, 10g Grave Soil",
                "abilities": "Puppet: Turns intangible, mirror leap traversal, possesses mortal bodies, constructs cursed voodoo puppets."
            },

            # 21. Abyss (Criminal)
            {
                "pathway": "Abyss", "sequence_level": 9,
                "main_ingredients": "Heart of a Rabid Hyena, 10ml Bile of a Venomous Toad",
                "supplementary_ingredients": "50ml Stagnant Swamp Water, 5g Charcoal Dust",
                "abilities": "Criminal: Extreme malice intuition, crafting cruel weapons, resistance to poisons and mental interrogation."
            },
            {
                "pathway": "Abyss", "sequence_level": 4,
                "main_ingredients": "Heart of an Infernal Demon, Molten Horn of a Balor",
                "supplementary_ingredients": "100ml Sulfur Spring Water, 10g Black Ash",
                "abilities": "Devil: Transforms into an armored demonic behemoth, spews toxic sulfur magma, senses hostility miles away."
            },

            # 22. White Tower (Reader)
            {
                "pathway": "White Tower", "sequence_level": 9,
                "main_ingredients": "Eye of an Insight Hawk, 10ml Ink of a Giant Memory Squid",
                "supplementary_ingredients": "50ml Pure Water, 5g Papyrus Ash",
                "abilities": "Reader: Phenomenal reading speed and textual comprehension, analytical deduction of supernatural relics."
            },
            {
                "pathway": "White Tower", "sequence_level": 4,
                "main_ingredients": "Brain of an Astral Sphinx, Core of a Divine Mirror of Truth",
                "supplementary_ingredients": "100ml Holy Scholar Water, 10g Crystal Dust",
                "abilities": "Polymath / Prophet: Replicates spells of other pathways, analyzes and exploits flaws in mystical formations."
            }
        ]

        for item in potions_data:
            pathway_name = item["pathway"]
            if pathway_name in pathway_objs:
                potion = Potion(
                    pathway_id=pathway_objs[pathway_name].id,
                    sequence_level=item["sequence_level"],
                    main_ingredients=item["main_ingredients"],
                    supplementary_ingredients=item["supplementary_ingredients"],
                    abilities=item["abilities"]
                )
                db.add(potion)

        # =========================================================================
        # 4. COMMISSIONS ACROSS WORLD ORGANIZATIONS & REGIONS
        # =========================================================================
        commissions_data = [
            {
                "title": "Investigate Antigonus Family Notebook",
                "hazard_rank": 4,
                "target": "Antigonus Relic & Secret Order Marionettes",
                "location": "Tingen Town, West District",
                "reward_gold": 350.0,
                "status": "OPEN"
            },
            {
                "title": "Purify Corrupted Spirit in Backlund Sewer",
                "hazard_rank": 7,
                "target": "Vagrant Wraiths & Toxic Slime",
                "location": "Backlund East Borough Underground",
                "reward_gold": 85.0,
                "status": "OPEN"
            },
            {
                "title": "Banish Devil Worshippers Ritual",
                "hazard_rank": 5,
                "target": "Desire Apostle Cult & Serial Slaughterers",
                "location": "Hillston District Abandoned Factory",
                "reward_gold": 180.0,
                "status": "OPEN"
            },
            {
                "title": "Escort Sealed Artifact 3-0782",
                "hazard_rank": 8,
                "target": "Sun-Emblem Purification Artifact",
                "location": "Raybibts Countryside Cathedral",
                "reward_gold": 50.0,
                "status": "OPEN"
            },
            {
                "title": "Exorcise Amon Avatar Sighting",
                "hazard_rank": 2,
                "target": "Monocle Marauder Avatar (Angel of Time clone)",
                "location": "Chernobyl Ruins Boundary / Forsaken Land",
                "reward_gold": 1500.0,
                "status": "OPEN"
            },
            {
                "title": "Contain Escaped Demoness Plague Source",
                "hazard_rank": 4,
                "target": "Pleasure Demoness Covens & Black Death vectors",
                "location": "Pritz Harbor Maritime Docks",
                "reward_gold": 400.0,
                "status": "OPEN"
            },
            {
                "title": "Suppress Berserk Steam Golem Protocol",
                "hazard_rank": 6,
                "target": "Defective Clockwork Automaton with Soul Core",
                "location": "Backlund Steam Machinery Works No. 4",
                "reward_gold": 120.0,
                "status": "OPEN"
            },
            {
                "title": "Intercept Pirate Raiding Squadron",
                "hazard_rank": 3,
                "target": "Admiral Hurricane Corsair Fleet",
                "location": "Sonia Sea Archipelago Shipping Route",
                "reward_gold": 650.0,
                "status": "OPEN"
            }
        ]

        for item in commissions_data:
            c = Commission(
                title=item["title"],
                hazard_rank=item["hazard_rank"],
                target=item["target"],
                location=item["location"],
                reward_gold=item["reward_gold"],
                status=item["status"]
            )
            db.add(c)

        db.commit()
        print("Database successfully seeded with all 22 Pathways, full organizations roster, and canonical characteristics!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database(force=True)
