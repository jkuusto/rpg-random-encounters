--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: biomes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.biomes (
    id integer NOT NULL,
    name character varying(30) NOT NULL
);


--
-- Name: biomes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.biomes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: biomes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.biomes_id_seq OWNED BY public.biomes.id;


--
-- Name: encounter_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.encounter_types (
    id integer NOT NULL,
    name character varying(30) NOT NULL
);


--
-- Name: encounter_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.encounter_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: encounter_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.encounter_types_id_seq OWNED BY public.encounter_types.id;


--
-- Name: encounters_biome; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.encounters_biome (
    id integer NOT NULL,
    game_id integer NOT NULL,
    biome_id integer NOT NULL,
    roll_range integer DEFAULT 1 NOT NULL,
    description text NOT NULL,
    preset boolean DEFAULT false NOT NULL
);


--
-- Name: encounters_biome_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.encounters_biome_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: encounters_biome_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.encounters_biome_id_seq OWNED BY public.encounters_biome.id;


--
-- Name: encounters_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.encounters_general (
    id integer NOT NULL,
    game_id integer NOT NULL,
    roll_range integer DEFAULT 1 NOT NULL,
    description text NOT NULL,
    preset boolean DEFAULT false NOT NULL
);


--
-- Name: encounters_general_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.encounters_general_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: encounters_general_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.encounters_general_id_seq OWNED BY public.encounters_general.id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.games (
    id integer NOT NULL,
    user_id integer NOT NULL,
    biome_id integer NOT NULL,
    name character varying NOT NULL
);


--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: main_probability; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.main_probability (
    id integer NOT NULL,
    game_id integer NOT NULL,
    encounter_type_id integer NOT NULL,
    roll_range integer,
    preset boolean DEFAULT false NOT NULL
);


--
-- Name: main_probability_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.main_probability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: main_probability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.main_probability_id_seq OWNED BY public.main_probability.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    password text NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: biomes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biomes ALTER COLUMN id SET DEFAULT nextval('public.biomes_id_seq'::regclass);


--
-- Name: encounter_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounter_types ALTER COLUMN id SET DEFAULT nextval('public.encounter_types_id_seq'::regclass);


--
-- Name: encounters_biome id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_biome ALTER COLUMN id SET DEFAULT nextval('public.encounters_biome_id_seq'::regclass);


--
-- Name: encounters_general id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_general ALTER COLUMN id SET DEFAULT nextval('public.encounters_general_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: main_probability id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.main_probability ALTER COLUMN id SET DEFAULT nextval('public.main_probability_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: biomes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.biomes (id, name) FROM stdin;
1	Plains
2	Forest
3	Foothills
\.


--
-- Data for Name: encounter_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.encounter_types (id, name) FROM stdin;
1	General encounter
2	Biome encounter
\.


--
-- Data for Name: encounters_biome; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.encounters_biome (id, game_id, biome_id, roll_range, description, preset) FROM stdin;
1	1	1	1	As you traverse the seemingly endless sea of grass, the earth begins to quiver, escalating to a violent tremor. Raising your eyes to the horizon, you witness an awe-inspiring and terrifying sight: a vast herd of bison, thundering across the plains in a frenzied stampede. The herd's path intersects with your own, threatening to overrun you in moments. A DC 12 Strength (Athletics) or a DC 17 Dexterity (Acrobatics) check may carry you to safety, be it through a daring sprint or a desperate leap. Failure to escape the path of the stampede results in the loss of a random non-magical item and a story of survival against the wild fury of nature.	t
2	1	1	1	In a rare display of color on the endless plains, you find yourselves amidst a field of strikingly beautiful flowers. Their scent fills the air, sweet but overpowering, hinting at the hidden danger of their allure. Breathing in the pollen tests your body's resilience, as you must resist its toxic effects. A successful DC 14 Constitution save means you recognize the danger in time, holding your breath and escaping the field unharmed and with 1d4 common poisonous reagents worth 10 gp each to any alchemist. Failure, however, results in no reagents and one level of Exhaustion as your head swims with dizziness and nausea.	t
3	1	2	1	As you push your way through the dense underbrush, a clearing opens before you, revealing the weathered stones of an ancient structure. The base of what was once a wizard's tower stands silent, its history etched into the moss-covered ruins. Magical runes, faded with time, promise knowledge and power to those who can decipher their meanings. A DC 16 Intelligence (Arcana) check allows you to understand the arcane symbols, revealing the wizard's research into elemental magic and pointing to a hidden compartment somewhere nearby. Among the rubble, you find the compartment containing 1d6 x 30 electrum pieces and a mysterious, faintly glowing crystal that pulses with elemental energy. As you pick up the gem, its energy dissipates into the air as if you had inadvertently set something free, leaving the gem in your hands dim and worthless. Failure to decode the writings leaves their secrets undiscovered, but the ruins still stand as a testament to the arcane arts, waiting for the next curious mind to unlock their mysteries	t
4	1	2	1	Emerging from the shadows, the guardian of the forest confronts you, a bear of immense size, its fur a living tapestry of the forest itself. It watches you, intelligence gleaming in its eyes, the weight of its duty palpable in the air. Convincing the guardian of your peaceful intentions through a DC 13 Charisma (Persuasion) check allows you safe passage and, if you beat the DC by 5, it even imparts wisdom about the forest's hidden paths granting advantage to navigation checks for the duration of your current visit in the forest. Attempting to retreat with a DC 15 Wisdom (Animal Handling) ensures a tense but uneventful withdrawal. Failure in either approach risks the guardian's wrath, interpreting your presence as a threat, imposing a disadvantage to all navigation checks made during your current stay in the forest as the guardian creates supernatural alterations to the environment.	t
5	1	3	1	As you navigate a narrow pass between the sloping hills, a low rumble underfoot sends a jolt of alarm through you. The hillsides tremble, and you realize a rockslide is imminent. Your eyes catch glimpses of loose stones above, ready to cascade down upon you. Quick action is needed to find shelter or protect yourselves from the oncoming barrage of stones. If you have Portable Rams or Shields you can use them to create makeshift barriers for two people each against the falling rocks. Huddled together under these protections, you hear the thunderous sound of rocks crashing down around you. After a moment that feels like an eternity, the noise subsides, and you emerge unscathed. Otherwise, you brace as best you can. Make a DC 12 Dexterity Saving Throw. Failure means you're caught by the slide, battered by rocks and debris, suffering 1 level of Exhaustion and find yourselves momentarily disoriented but alive.	t
6	1	3	1	In a quiet dell among the foothills, you discover a circle of ancient stones, each carved with worn symbols that seem to pulsate with a forgotten power. The air thrums with energy, suggesting that unlocking the stones' secrets could grant boons or reveal hidden knowledge. But understanding these relics of the past will take a keen intellect. With a successful DC 17 Intelligence (Arcana or History) check your intellectual prowess shines as you translate the symbols, connecting them to arcane rituals of power and protection. The stones emit a soft glow, bathing the party in a welcoming light. Each party member gains the benefit of a Warding Bond spell for the next 24 hours, offering protection as you continue your journey. On a failure the symbols remain a mystery, their secrets locked away by time and decay. Perhaps with more knowledge or another key, their magic would reveal itself. For now, they stand silent, a reminder of your limitations and the mysteries that still wait to be uncovered.	t
\.


--
-- Data for Name: encounters_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.encounters_general (id, game_id, roll_range, description, preset) FROM stdin;
1	1	1	Without warning, a dense fog envelops you, obscuring the way ahead and muffling the sounds of the surrounding area. Navigating through this could lead you off course or into danger. Should you decide to travel further, the party's navigator must succeed on a DC 15 Wisdom (Survival) check or the party becomes lost for 1d6 hours.	t
2	1	1	As you journey, the air fills with the ethereal sounds of music and merriment, as if a grand celebration is taking place just out of sight. The source of these phantom sounds eludes your gaze, dancing away whenever you believe you're drawing near. A DC 20 Wisdom (Perception) check will help you track down the origin of this ghostly gala, or a DC 15 Charisma (Persuasion) combined with the Speak with Animal spell or similiar effect will help you to communicate with nearby wildlife, persuading them to reveal the source of the sounds. Success leads you to a spectral party, where the spirits bestow a boon for joining their revelry for 1d4 hours, granting an inspiration point for each party memeber. Failure, however, leaves you wandering, the enchanting sounds fading away, leaving only the whisper of what might have been.	t
3	1	1	As you advance, an unsettling sight catches your eye: a lifeless form lies a little over hundred feet away from where you're standing. Curiously, the ground around it seems undisturbed, as if the body was placed there by unseen hands. No wounds mar the corpse's visage, offering no hints of the tragedy that befell this poor soul.	t
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.games (id, user_id, biome_id, name) FROM stdin;
1	1	1	Preset Game
\.


--
-- Data for Name: main_probability; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.main_probability (id, game_id, encounter_type_id, roll_range, preset) FROM stdin;
1	1	1	70	t
2	1	2	30	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, username, password) FROM stdin;
1	preset	scrypt:32768:8:1$5Nzguso4TdNEqgBX$19e32bf9e53c5a21e8592c7aedac6762ca09762384256005fc6d6bea6b70cd8d3ede173c141e3a396cc07bd0ad605b900e24f556312d4ea8b732198baa480f9a
\.


--
-- Name: biomes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.biomes_id_seq', 3, true);


--
-- Name: encounter_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.encounter_types_id_seq', 2, true);


--
-- Name: encounters_biome_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.encounters_biome_id_seq', 42, true);


--
-- Name: encounters_general_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.encounters_general_id_seq', 21, true);


--
-- Name: games_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.games_id_seq', 8, true);


--
-- Name: main_probability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.main_probability_id_seq', 16, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: biomes biomes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biomes
    ADD CONSTRAINT biomes_pkey PRIMARY KEY (id);


--
-- Name: encounter_types encounter_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounter_types
    ADD CONSTRAINT encounter_types_pkey PRIMARY KEY (id);


--
-- Name: encounters_biome encounters_biome_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_biome
    ADD CONSTRAINT encounters_biome_pkey PRIMARY KEY (id);


--
-- Name: encounters_general encounters_general_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_general
    ADD CONSTRAINT encounters_general_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: main_probability main_probability_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.main_probability
    ADD CONSTRAINT main_probability_pkey PRIMARY KEY (id);


--
-- Name: biomes unique_biome_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biomes
    ADD CONSTRAINT unique_biome_name UNIQUE (name);


--
-- Name: users unique_username; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: encounters_biome encounters_biome_biome_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_biome
    ADD CONSTRAINT encounters_biome_biome_id_fkey FOREIGN KEY (biome_id) REFERENCES public.biomes(id);


--
-- Name: encounters_biome encounters_biome_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_biome
    ADD CONSTRAINT encounters_biome_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(id) ON DELETE CASCADE;


--
-- Name: encounters_general encounters_general_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.encounters_general
    ADD CONSTRAINT encounters_general_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(id) ON DELETE CASCADE;


--
-- Name: games games_biome_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_biome_id_fkey FOREIGN KEY (biome_id) REFERENCES public.biomes(id);


--
-- Name: games games_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: main_probability main_probability_encounter_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.main_probability
    ADD CONSTRAINT main_probability_encounter_type_id_fkey FOREIGN KEY (encounter_type_id) REFERENCES public.encounter_types(id);


--
-- Name: main_probability main_probability_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.main_probability
    ADD CONSTRAINT main_probability_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

