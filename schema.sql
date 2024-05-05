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
    name character varying(30) NOT NULL
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

