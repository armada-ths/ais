--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO ais;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO ais;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO ais;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO ais;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO ais;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO ais;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO ais;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO ais;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO ais;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO ais;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO ais;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO ais;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: banquet_banquettable; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.banquet_banquettable (
    id integer NOT NULL,
    table_name character varying(60),
    number_of_seats integer,
    fair_id integer NOT NULL
);


ALTER TABLE public.banquet_banquettable OWNER TO ais;

--
-- Name: banquet_banquettable_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.banquet_banquettable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banquet_banquettable_id_seq OWNER TO ais;

--
-- Name: banquet_banquettable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.banquet_banquettable_id_seq OWNED BY public.banquet_banquettable.id;


--
-- Name: banquet_banquetteattendant; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.banquet_banquetteattendant (
    id integer NOT NULL,
    first_name character varying(200) NOT NULL,
    last_name character varying(200) NOT NULL,
    gender character varying(100) NOT NULL,
    phone_number character varying(200) NOT NULL,
    allergies character varying(1000) NOT NULL,
    student_ticket boolean NOT NULL,
    wants_alcohol boolean NOT NULL,
    wants_lactose_free_food boolean NOT NULL,
    wants_gluten_free_food boolean NOT NULL,
    exhibitor_id integer,
    job_title character varying(200) NOT NULL,
    linkedin_url character varying(200) NOT NULL,
    user_id integer,
    email character varying(200) NOT NULL,
    wants_vegan_food boolean NOT NULL,
    seat_number smallint,
    ignore_from_placement boolean NOT NULL,
    fair_id integer NOT NULL,
    confirmed boolean NOT NULL,
    table_id integer,
    ticket_id integer
);


ALTER TABLE public.banquet_banquetteattendant OWNER TO ais;

--
-- Name: banquet_banquetticket; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.banquet_banquetticket (
    id integer NOT NULL,
    name character varying(120)
);


ALTER TABLE public.banquet_banquetticket OWNER TO ais;

--
-- Name: banquet_banquetticket_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.banquet_banquetticket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banquet_banquetticket_id_seq OWNER TO ais;

--
-- Name: banquet_banquetticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.banquet_banquetticket_id_seq OWNED BY public.banquet_banquetticket.id;


--
-- Name: companies_company; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.companies_company (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    organisation_number character varying(100) NOT NULL,
    website character varying(300) NOT NULL,
    phone_number character varying(300) NOT NULL,
    address_city character varying(200) NOT NULL,
    address_country character varying(200) NOT NULL,
    address_street character varying(200) NOT NULL,
    address_zip_code character varying(200) NOT NULL,
    organisation_type character varying(30),
    additional_address_information character varying(200) NOT NULL
);


ALTER TABLE public.companies_company OWNER TO ais;

--
-- Name: companies_company_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.companies_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_company_id_seq OWNER TO ais;

--
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.companies_company_id_seq OWNED BY public.companies_company.id;


--
-- Name: companies_company_related_programme; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.companies_company_related_programme (
    id integer NOT NULL,
    company_id integer NOT NULL,
    programme_id integer NOT NULL
);


ALTER TABLE public.companies_company_related_programme OWNER TO ais;

--
-- Name: companies_company_related_programme_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.companies_company_related_programme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_company_related_programme_id_seq OWNER TO ais;

--
-- Name: companies_company_related_programme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.companies_company_related_programme_id_seq OWNED BY public.companies_company_related_programme.id;


--
-- Name: companies_contact; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.companies_contact (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(200) NOT NULL,
    title character varying(200) NOT NULL,
    cell_phone character varying(200) NOT NULL,
    work_phone character varying(200) NOT NULL,
    active boolean NOT NULL,
    phone_switchboard character varying(200),
    alternative_email character varying(200),
    belongs_to_id integer,
    user_id integer,
    confirmed boolean NOT NULL
);


ALTER TABLE public.companies_contact OWNER TO ais;

--
-- Name: companies_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.companies_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_contact_id_seq OWNER TO ais;

--
-- Name: companies_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.companies_contact_id_seq OWNED BY public.companies_contact.id;


--
-- Name: companies_invoicedetails; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.companies_invoicedetails (
    id integer NOT NULL,
    reference character varying(200) NOT NULL,
    purchase_order_number character varying(200) NOT NULL,
    reference_phone_number character varying(200) NOT NULL,
    organisation_name character varying(200) NOT NULL,
    address character varying(200) NOT NULL,
    address_po_box character varying(200) NOT NULL,
    address_zip_code character varying(100) NOT NULL,
    identification character varying(200) NOT NULL,
    additional_information character varying(500) NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.companies_invoicedetails OWNER TO ais;

--
-- Name: companies_invoicedetails_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.companies_invoicedetails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_invoicedetails_id_seq OWNER TO ais;

--
-- Name: companies_invoicedetails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.companies_invoicedetails_id_seq OWNED BY public.companies_invoicedetails.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO ais;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO ais;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO ais;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO ais;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO ais;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO ais;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO ais;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO ais;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO ais;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: events_event; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_event (
    id integer NOT NULL,
    name character varying(75) NOT NULL,
    event_start timestamp with time zone NOT NULL,
    event_end timestamp with time zone NOT NULL,
    capacity smallint NOT NULL,
    description text NOT NULL,
    registration_start timestamp with time zone NOT NULL,
    registration_end timestamp with time zone NOT NULL,
    registration_last_day_cancel timestamp with time zone,
    public_registration boolean NOT NULL,
    fair_id integer NOT NULL,
    attendence_description text NOT NULL,
    description_short text NOT NULL,
    send_submission_mail boolean NOT NULL,
    submission_mail_body text NOT NULL,
    submission_mail_subject character varying(78) NOT NULL,
    image character varying(100) NOT NULL,
    image_original character varying(100) NOT NULL,
    attendence_approvement_required boolean NOT NULL,
    registration_required boolean NOT NULL,
    location character varying(75) NOT NULL,
    published boolean NOT NULL,
    extra_field_id integer,
    confirmation_mail_body text NOT NULL,
    confirmation_mail_subject character varying(78) NOT NULL,
    rejection_mail_body text NOT NULL,
    rejection_mail_subject character varying(78) NOT NULL,
    external_signup_url character varying(200) NOT NULL,
    CONSTRAINT events_event_capacity_0788c01e_check CHECK ((capacity >= 0))
);


ALTER TABLE public.events_event OWNER TO ais;

--
-- Name: events_event_allowed_groups; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_event_allowed_groups (
    id integer NOT NULL,
    event_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.events_event_allowed_groups OWNER TO ais;

--
-- Name: events_event_allowed_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_event_allowed_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_allowed_groups_id_seq OWNER TO ais;

--
-- Name: events_event_allowed_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_event_allowed_groups_id_seq OWNED BY public.events_event_allowed_groups.id;


--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_id_seq OWNER TO ais;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events_event.id;


--
-- Name: events_event_tags; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_event_tags (
    id integer NOT NULL,
    event_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.events_event_tags OWNER TO ais;

--
-- Name: events_event_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_event_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_tags_id_seq OWNER TO ais;

--
-- Name: events_event_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_event_tags_id_seq OWNED BY public.events_event_tags.id;


--
-- Name: events_eventanswer; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_eventanswer (
    id integer NOT NULL,
    answer text NOT NULL,
    attendence_id integer NOT NULL,
    question_id integer NOT NULL
);


ALTER TABLE public.events_eventanswer OWNER TO ais;

--
-- Name: events_eventanswer_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_eventanswer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_eventanswer_id_seq OWNER TO ais;

--
-- Name: events_eventanswer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_eventanswer_id_seq OWNED BY public.events_eventanswer.id;


--
-- Name: events_eventattendence; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_eventattendence (
    id integer NOT NULL,
    status character varying(3) NOT NULL,
    event_id integer NOT NULL,
    user_id integer,
    submission_date timestamp with time zone NOT NULL,
    sent_email boolean NOT NULL
);


ALTER TABLE public.events_eventattendence OWNER TO ais;

--
-- Name: events_eventattendence_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_eventattendence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_eventattendence_id_seq OWNER TO ais;

--
-- Name: events_eventattendence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_eventattendence_id_seq OWNED BY public.events_eventattendence.id;


--
-- Name: events_eventquestion; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.events_eventquestion (
    id integer NOT NULL,
    question_text text NOT NULL,
    event_id integer NOT NULL,
    required boolean NOT NULL
);


ALTER TABLE public.events_eventquestion OWNER TO ais;

--
-- Name: events_eventquestion_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.events_eventquestion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_eventquestion_id_seq OWNER TO ais;

--
-- Name: events_eventquestion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.events_eventquestion_id_seq OWNED BY public.events_eventquestion.id;


--
-- Name: exhibitors_banquetteattendant_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_banquetteattendant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_banquetteattendant_id_seq OWNER TO ais;

--
-- Name: exhibitors_banquetteattendant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_banquetteattendant_id_seq OWNED BY public.banquet_banquetteattendant.id;


--
-- Name: exhibitors_cataloginfo; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo (
    id integer NOT NULL,
    display_name character varying(200) NOT NULL,
    slug character varying(50) NOT NULL,
    short_description character varying(200) NOT NULL,
    description text NOT NULL,
    employees_sweden integer NOT NULL,
    employees_world integer NOT NULL,
    countries integer NOT NULL,
    website_url character varying(300) NOT NULL,
    facebook_url character varying(300) NOT NULL,
    twitter_url character varying(300) NOT NULL,
    linkedin_url character varying(300) NOT NULL,
    exhibitor_id integer NOT NULL,
    main_work_field_id integer,
    ad character varying(100) NOT NULL,
    logo character varying(100) NOT NULL,
    logo_small character varying(100) NOT NULL,
    ad_original character varying(100) NOT NULL,
    logo_original character varying(100) NOT NULL,
    location_at_fair character varying(100) NOT NULL,
    location_at_fair_original character varying(100) NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_continents; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_continents (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    continent_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_continents OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_continents_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_continents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_continents_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_continents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_continents_id_seq OWNED BY public.exhibitors_cataloginfo_continents.id;


--
-- Name: exhibitors_cataloginfo_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_id_seq OWNED BY public.exhibitors_cataloginfo.id;


--
-- Name: exhibitors_cataloginfo_job_types; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_job_types (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    jobtype_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_job_types OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_job_types_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_job_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_job_types_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_job_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_job_types_id_seq OWNED BY public.exhibitors_cataloginfo_job_types.id;


--
-- Name: exhibitors_cataloginfo_programs; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_programs (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    programme_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_programs OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_programs_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_programs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_programs_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_programs_id_seq OWNED BY public.exhibitors_cataloginfo_programs.id;


--
-- Name: exhibitors_cataloginfo_tags; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_tags (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_tags OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_tags_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_tags_id_seq OWNED BY public.exhibitors_cataloginfo_tags.id;


--
-- Name: exhibitors_cataloginfo_values; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_values (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    value_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_values OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_values_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_values_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_values_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_values_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_values_id_seq OWNED BY public.exhibitors_cataloginfo_values.id;


--
-- Name: exhibitors_cataloginfo_work_fields; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_cataloginfo_work_fields (
    id integer NOT NULL,
    cataloginfo_id integer NOT NULL,
    workfield_id integer NOT NULL
);


ALTER TABLE public.exhibitors_cataloginfo_work_fields OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_work_fields_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_cataloginfo_work_fields_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_cataloginfo_work_fields_id_seq OWNER TO ais;

--
-- Name: exhibitors_cataloginfo_work_fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_cataloginfo_work_fields_id_seq OWNED BY public.exhibitors_cataloginfo_work_fields.id;


--
-- Name: exhibitors_continent; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_continent (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.exhibitors_continent OWNER TO ais;

--
-- Name: exhibitors_continent_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_continent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_continent_id_seq OWNER TO ais;

--
-- Name: exhibitors_continent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_continent_id_seq OWNED BY public.exhibitors_continent.id;


--
-- Name: exhibitors_exhibitor; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_exhibitor (
    id integer NOT NULL,
    company_id integer NOT NULL,
    fair_id integer NOT NULL,
    location_id integer,
    contact_id integer,
    status character varying(30),
    fair_location_id integer,
    logo character varying(100) NOT NULL,
    about_text text NOT NULL,
    facts_text text NOT NULL,
    accept_terms boolean NOT NULL,
    booth_number integer,
    comment text NOT NULL,
    location_at_fair character varying(100) NOT NULL,
    invoice_details_id integer,
    inbound_transportation_id integer,
    outbound_transportation_id integer,
    delivery_order_id integer,
    pickup_order_id integer
);


ALTER TABLE public.exhibitors_exhibitor OWNER TO ais;

--
-- Name: exhibitors_exhibitor_hosts; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_exhibitor_hosts (
    id integer NOT NULL,
    exhibitor_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.exhibitors_exhibitor_hosts OWNER TO ais;

--
-- Name: exhibitors_exhibitor_hosts_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitor_hosts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitor_hosts_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitor_hosts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitor_hosts_id_seq OWNED BY public.exhibitors_exhibitor_hosts.id;


--
-- Name: exhibitors_exhibitor_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitor_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitor_id_seq OWNED BY public.exhibitors_exhibitor.id;


--
-- Name: exhibitors_exhibitor_job_types; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_exhibitor_job_types (
    id integer NOT NULL,
    exhibitor_id integer NOT NULL,
    jobtype_id integer NOT NULL
);


ALTER TABLE public.exhibitors_exhibitor_job_types OWNER TO ais;

--
-- Name: exhibitors_exhibitor_job_types_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitor_job_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitor_job_types_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitor_job_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitor_job_types_id_seq OWNED BY public.exhibitors_exhibitor_job_types.id;


--
-- Name: exhibitors_exhibitor_tags; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_exhibitor_tags (
    id integer NOT NULL,
    exhibitor_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.exhibitors_exhibitor_tags OWNER TO ais;

--
-- Name: exhibitors_exhibitor_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitor_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitor_tags_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitor_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitor_tags_id_seq OWNED BY public.exhibitors_exhibitor_tags.id;


--
-- Name: exhibitors_location; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_location (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.exhibitors_location OWNER TO ais;

--
-- Name: exhibitors_exhibitorlocation_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitorlocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitorlocation_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitorlocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitorlocation_id_seq OWNED BY public.exhibitors_location.id;


--
-- Name: exhibitors_exhibitorview; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_exhibitorview (
    id integer NOT NULL,
    choices text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.exhibitors_exhibitorview OWNER TO ais;

--
-- Name: exhibitors_exhibitorview_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_exhibitorview_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_exhibitorview_id_seq OWNER TO ais;

--
-- Name: exhibitors_exhibitorview_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_exhibitorview_id_seq OWNED BY public.exhibitors_exhibitorview.id;


--
-- Name: exhibitors_jobtype; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_jobtype (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.exhibitors_jobtype OWNER TO ais;

--
-- Name: exhibitors_jobtype_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_jobtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_jobtype_id_seq OWNER TO ais;

--
-- Name: exhibitors_jobtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_jobtype_id_seq OWNED BY public.exhibitors_jobtype.id;


--
-- Name: exhibitors_transportationalternative; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_transportationalternative (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    transportation_type character varying(30),
    inbound boolean NOT NULL
);


ALTER TABLE public.exhibitors_transportationalternative OWNER TO ais;

--
-- Name: exhibitors_transportationalternative_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_transportationalternative_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_transportationalternative_id_seq OWNER TO ais;

--
-- Name: exhibitors_transportationalternative_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_transportationalternative_id_seq OWNED BY public.exhibitors_transportationalternative.id;


--
-- Name: exhibitors_value; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_value (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.exhibitors_value OWNER TO ais;

--
-- Name: exhibitors_value_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_value_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_value_id_seq OWNER TO ais;

--
-- Name: exhibitors_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_value_id_seq OWNED BY public.exhibitors_value.id;


--
-- Name: exhibitors_workfield; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.exhibitors_workfield (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.exhibitors_workfield OWNER TO ais;

--
-- Name: exhibitors_workfield_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.exhibitors_workfield_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exhibitors_workfield_id_seq OWNER TO ais;

--
-- Name: exhibitors_workfield_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.exhibitors_workfield_id_seq OWNED BY public.exhibitors_workfield.id;


--
-- Name: fair_fair; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.fair_fair (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    year integer NOT NULL,
    description text NOT NULL,
    registration_end_date timestamp with time zone,
    registration_start_date timestamp with time zone,
    current boolean NOT NULL,
    complete_registration_close_date timestamp with time zone,
    complete_registration_start_date timestamp with time zone
);


ALTER TABLE public.fair_fair OWNER TO ais;

--
-- Name: fair_fair_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.fair_fair_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fair_fair_id_seq OWNER TO ais;

--
-- Name: fair_fair_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.fair_fair_id_seq OWNED BY public.fair_fair.id;


--
-- Name: fair_partner; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.fair_partner (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    logo character varying(100) NOT NULL,
    url character varying(300) NOT NULL,
    main_partner boolean NOT NULL,
    fair_id integer NOT NULL
);


ALTER TABLE public.fair_partner OWNER TO ais;

--
-- Name: fair_partner_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.fair_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fair_partner_id_seq OWNER TO ais;

--
-- Name: fair_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.fair_partner_id_seq OWNED BY public.fair_partner.id;


--
-- Name: fair_tag; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.fair_tag (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.fair_tag OWNER TO ais;

--
-- Name: fair_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.fair_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fair_tag_id_seq OWNER TO ais;

--
-- Name: fair_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.fair_tag_id_seq OWNED BY public.fair_tag.id;


--
-- Name: locations_building; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.locations_building (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    map_image character varying(100) NOT NULL
);


ALTER TABLE public.locations_building OWNER TO ais;

--
-- Name: locations_building_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.locations_building_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_building_id_seq OWNER TO ais;

--
-- Name: locations_building_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.locations_building_id_seq OWNED BY public.locations_building.id;


--
-- Name: locations_location; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.locations_location (
    id integer NOT NULL,
    room_id integer NOT NULL,
    x_pos double precision NOT NULL,
    y_pos double precision NOT NULL
);


ALTER TABLE public.locations_location OWNER TO ais;

--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.locations_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_location_id_seq OWNER TO ais;

--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations_location.id;


--
-- Name: locations_room; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.locations_room (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    floor smallint NOT NULL,
    building_id integer NOT NULL,
    CONSTRAINT locations_room_floor_check CHECK ((floor >= 0))
);


ALTER TABLE public.locations_room OWNER TO ais;

--
-- Name: locations_room_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.locations_room_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_room_id_seq OWNER TO ais;

--
-- Name: locations_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.locations_room_id_seq OWNED BY public.locations_room.id;


--
-- Name: matching_answer; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_answer (
    id integer NOT NULL,
    question_id integer NOT NULL,
    response_id integer NOT NULL,
    polymorphic_ctype_id integer
);


ALTER TABLE public.matching_answer OWNER TO ais;

--
-- Name: matching_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_answer_id_seq OWNER TO ais;

--
-- Name: matching_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_answer_id_seq OWNED BY public.matching_answer.id;


--
-- Name: matching_booleanans; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_booleanans (
    answer_ptr_id integer NOT NULL,
    ans boolean
);


ALTER TABLE public.matching_booleanans OWNER TO ais;

--
-- Name: matching_category; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_category (
    id integer NOT NULL,
    name character varying(400) NOT NULL,
    "order" integer,
    description character varying(2000),
    survey_id integer NOT NULL
);


ALTER TABLE public.matching_category OWNER TO ais;

--
-- Name: matching_category_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_category_id_seq OWNER TO ais;

--
-- Name: matching_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_category_id_seq OWNED BY public.matching_category.id;


--
-- Name: matching_choiceans; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_choiceans (
    answer_ptr_id integer NOT NULL,
    ans integer
);


ALTER TABLE public.matching_choiceans OWNER TO ais;

--
-- Name: matching_continent; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_continent (
    id integer NOT NULL,
    name text NOT NULL,
    continent_id integer,
    survey_id integer
);


ALTER TABLE public.matching_continent OWNER TO ais;

--
-- Name: matching_continent_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_continent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_continent_id_seq OWNER TO ais;

--
-- Name: matching_continent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_continent_id_seq OWNED BY public.matching_continent.id;


--
-- Name: matching_country; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_country (
    id integer NOT NULL,
    name text NOT NULL,
    continent_id integer
);


ALTER TABLE public.matching_country OWNER TO ais;

--
-- Name: matching_country_exhibitor; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_country_exhibitor (
    id integer NOT NULL,
    country_id integer NOT NULL,
    exhibitor_id integer NOT NULL
);


ALTER TABLE public.matching_country_exhibitor OWNER TO ais;

--
-- Name: matching_country_exhibitor_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_country_exhibitor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_country_exhibitor_id_seq OWNER TO ais;

--
-- Name: matching_country_exhibitor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_country_exhibitor_id_seq OWNED BY public.matching_country_exhibitor.id;


--
-- Name: matching_country_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_country_id_seq OWNER TO ais;

--
-- Name: matching_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_country_id_seq OWNED BY public.matching_country.id;


--
-- Name: matching_integerans; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_integerans (
    answer_ptr_id integer NOT NULL,
    ans integer
);


ALTER TABLE public.matching_integerans OWNER TO ais;

--
-- Name: matching_jobtype; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_jobtype (
    id integer NOT NULL,
    job_type text NOT NULL,
    job_type_id integer NOT NULL,
    exhibitor_question_id integer
);


ALTER TABLE public.matching_jobtype OWNER TO ais;

--
-- Name: matching_jobtype_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_jobtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_jobtype_id_seq OWNER TO ais;

--
-- Name: matching_jobtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_jobtype_id_seq OWNED BY public.matching_jobtype.id;


--
-- Name: matching_question; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_question (
    id integer NOT NULL,
    text text NOT NULL,
    question_type character varying(256),
    name character varying(64),
    help_text text,
    category_id integer,
    survey_id integer,
    required boolean NOT NULL
);


ALTER TABLE public.matching_question OWNER TO ais;

--
-- Name: matching_question_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_question_id_seq OWNER TO ais;

--
-- Name: matching_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_question_id_seq OWNED BY public.matching_question.id;


--
-- Name: matching_response; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_response (
    id integer NOT NULL,
    exhibitor_id integer NOT NULL,
    survey_id integer
);


ALTER TABLE public.matching_response OWNER TO ais;

--
-- Name: matching_response_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_response_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_response_id_seq OWNER TO ais;

--
-- Name: matching_response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_response_id_seq OWNED BY public.matching_response.id;


--
-- Name: matching_studentanswerbase; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerbase (
    id integer NOT NULL,
    student_id integer NOT NULL,
    created timestamp with time zone,
    updated timestamp with time zone
);


ALTER TABLE public.matching_studentanswerbase OWNER TO ais;

--
-- Name: matching_studentanswerbase_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_studentanswerbase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_studentanswerbase_id_seq OWNER TO ais;

--
-- Name: matching_studentanswerbase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_studentanswerbase_id_seq OWNED BY public.matching_studentanswerbase.id;


--
-- Name: matching_studentanswerbase_survey; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerbase_survey (
    id integer NOT NULL,
    studentanswerbase_id integer NOT NULL,
    survey_id integer NOT NULL
);


ALTER TABLE public.matching_studentanswerbase_survey OWNER TO ais;

--
-- Name: matching_studentanswerbase_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_studentanswerbase_survey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_studentanswerbase_survey_id_seq OWNER TO ais;

--
-- Name: matching_studentanswerbase_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_studentanswerbase_survey_id_seq OWNED BY public.matching_studentanswerbase_survey.id;


--
-- Name: matching_studentanswercontinent; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswercontinent (
    studentanswerbase_ptr_id integer NOT NULL,
    continent_id integer NOT NULL
);


ALTER TABLE public.matching_studentanswercontinent OWNER TO ais;

--
-- Name: matching_studentanswergrading; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswergrading (
    studentanswerbase_ptr_id integer NOT NULL,
    answer integer NOT NULL,
    question_id integer NOT NULL
);


ALTER TABLE public.matching_studentanswergrading OWNER TO ais;

--
-- Name: matching_studentanswerjobtype; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerjobtype (
    studentanswerbase_ptr_id integer NOT NULL,
    job_type_id integer
);


ALTER TABLE public.matching_studentanswerjobtype OWNER TO ais;

--
-- Name: matching_studentanswerregion; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerregion (
    studentanswerbase_ptr_id integer NOT NULL,
    region_id integer NOT NULL
);


ALTER TABLE public.matching_studentanswerregion OWNER TO ais;

--
-- Name: matching_studentanswerslider; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerslider (
    studentanswerbase_ptr_id integer NOT NULL,
    answer_max double precision NOT NULL,
    question_id integer NOT NULL,
    answer_min double precision NOT NULL
);


ALTER TABLE public.matching_studentanswerslider OWNER TO ais;

--
-- Name: matching_studentanswerworkfield; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentanswerworkfield (
    studentanswerbase_ptr_id integer NOT NULL,
    answer boolean NOT NULL,
    work_field_id integer NOT NULL
);


ALTER TABLE public.matching_studentanswerworkfield OWNER TO ais;

--
-- Name: matching_studentquestionbase; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentquestionbase (
    id integer NOT NULL,
    question character varying(256) NOT NULL,
    question_type character varying(64) NOT NULL,
    company_question_id integer
);


ALTER TABLE public.matching_studentquestionbase OWNER TO ais;

--
-- Name: matching_studentquestionbase_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_studentquestionbase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_studentquestionbase_id_seq OWNER TO ais;

--
-- Name: matching_studentquestionbase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_studentquestionbase_id_seq OWNED BY public.matching_studentquestionbase.id;


--
-- Name: matching_studentquestionbase_survey; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentquestionbase_survey (
    id integer NOT NULL,
    studentquestionbase_id integer NOT NULL,
    survey_id integer NOT NULL
);


ALTER TABLE public.matching_studentquestionbase_survey OWNER TO ais;

--
-- Name: matching_studentquestionbase_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_studentquestionbase_survey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_studentquestionbase_survey_id_seq OWNER TO ais;

--
-- Name: matching_studentquestionbase_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_studentquestionbase_survey_id_seq OWNED BY public.matching_studentquestionbase_survey.id;


--
-- Name: matching_studentquestiongrading; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentquestiongrading (
    studentquestionbase_ptr_id integer NOT NULL,
    grading_size integer NOT NULL
);


ALTER TABLE public.matching_studentquestiongrading OWNER TO ais;

--
-- Name: matching_studentquestionslider; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_studentquestionslider (
    studentquestionbase_ptr_id integer NOT NULL,
    min_value double precision NOT NULL,
    max_value double precision NOT NULL,
    logarithmic boolean NOT NULL,
    units character varying(64)
);


ALTER TABLE public.matching_studentquestionslider OWNER TO ais;

--
-- Name: matching_survey; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_survey (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    description text NOT NULL,
    fair_id integer NOT NULL,
    relates_to_id integer
);


ALTER TABLE public.matching_survey OWNER TO ais;

--
-- Name: matching_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_survey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_survey_id_seq OWNER TO ais;

--
-- Name: matching_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_survey_id_seq OWNED BY public.matching_survey.id;


--
-- Name: matching_swedencity_exhibitor; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_swedencity_exhibitor (
    id integer NOT NULL,
    swedencity_id integer NOT NULL,
    exhibitor_id integer NOT NULL
);


ALTER TABLE public.matching_swedencity_exhibitor OWNER TO ais;

--
-- Name: matching_swedencities_exhibitor_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_swedencities_exhibitor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_swedencities_exhibitor_id_seq OWNER TO ais;

--
-- Name: matching_swedencities_exhibitor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_swedencities_exhibitor_id_seq OWNED BY public.matching_swedencity_exhibitor.id;


--
-- Name: matching_swedencity; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_swedencity (
    id integer NOT NULL,
    city text NOT NULL,
    region_id integer NOT NULL
);


ALTER TABLE public.matching_swedencity OWNER TO ais;

--
-- Name: matching_swedencities_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_swedencities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_swedencities_id_seq OWNER TO ais;

--
-- Name: matching_swedencities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_swedencities_id_seq OWNED BY public.matching_swedencity.id;


--
-- Name: matching_swedenregion; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_swedenregion (
    id integer NOT NULL,
    name text NOT NULL,
    survey_id integer,
    region_id integer
);


ALTER TABLE public.matching_swedenregion OWNER TO ais;

--
-- Name: matching_swedenregion_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_swedenregion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_swedenregion_id_seq OWNER TO ais;

--
-- Name: matching_swedenregion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_swedenregion_id_seq OWNED BY public.matching_swedenregion.id;


--
-- Name: matching_textans; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_textans (
    answer_ptr_id integer NOT NULL,
    ans character varying(4096)
);


ALTER TABLE public.matching_textans OWNER TO ais;

--
-- Name: matching_workfield; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_workfield (
    id integer NOT NULL,
    work_field text NOT NULL,
    work_area_id integer
);


ALTER TABLE public.matching_workfield OWNER TO ais;

--
-- Name: matching_workfield_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_workfield_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_workfield_id_seq OWNER TO ais;

--
-- Name: matching_workfield_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_workfield_id_seq OWNED BY public.matching_workfield.id;


--
-- Name: matching_workfield_survey; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_workfield_survey (
    id integer NOT NULL,
    workfield_id integer NOT NULL,
    survey_id integer NOT NULL
);


ALTER TABLE public.matching_workfield_survey OWNER TO ais;

--
-- Name: matching_workfield_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_workfield_survey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_workfield_survey_id_seq OWNER TO ais;

--
-- Name: matching_workfield_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_workfield_survey_id_seq OWNED BY public.matching_workfield_survey.id;


--
-- Name: matching_workfieldarea; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.matching_workfieldarea (
    id integer NOT NULL,
    work_area text NOT NULL
);


ALTER TABLE public.matching_workfieldarea OWNER TO ais;

--
-- Name: matching_workfieldarea_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.matching_workfieldarea_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matching_workfieldarea_id_seq OWNER TO ais;

--
-- Name: matching_workfieldarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.matching_workfieldarea_id_seq OWNED BY public.matching_workfieldarea.id;


--
-- Name: news_newsarticle; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.news_newsarticle (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    html_article_text text NOT NULL,
    publication_date timestamp with time zone NOT NULL,
    image character varying(100) NOT NULL,
    ingress text NOT NULL,
    author character varying(50) NOT NULL
);


ALTER TABLE public.news_newsarticle OWNER TO ais;

--
-- Name: news_newsarticle_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.news_newsarticle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.news_newsarticle_id_seq OWNER TO ais;

--
-- Name: news_newsarticle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.news_newsarticle_id_seq OWNED BY public.news_newsarticle.id;


--
-- Name: orders_electricityorder; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.orders_electricityorder (
    id integer NOT NULL,
    total_power integer NOT NULL,
    number_of_outlets integer NOT NULL,
    equipment_description character varying(150),
    exhibitor_id integer NOT NULL
);


ALTER TABLE public.orders_electricityorder OWNER TO ais;

--
-- Name: orders_electricityorder_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.orders_electricityorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_electricityorder_id_seq OWNER TO ais;

--
-- Name: orders_electricityorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.orders_electricityorder_id_seq OWNED BY public.orders_electricityorder.id;


--
-- Name: orders_order; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.orders_order (
    id integer NOT NULL,
    amount smallint NOT NULL,
    exhibitor_id integer NOT NULL,
    product_id integer NOT NULL,
    CONSTRAINT orders_order_amount_check CHECK ((amount >= 0))
);


ALTER TABLE public.orders_order OWNER TO ais;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_order_id_seq OWNER TO ais;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders_order.id;


--
-- Name: orders_product; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.orders_product (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description text NOT NULL,
    coa_number smallint NOT NULL,
    price integer NOT NULL,
    fair_id integer NOT NULL,
    product_type_id integer,
    display_in_product_list boolean NOT NULL,
    included_for_all boolean NOT NULL,
    CONSTRAINT orders_product_coa_number_check CHECK ((coa_number >= 0))
);


ALTER TABLE public.orders_product OWNER TO ais;

--
-- Name: orders_product_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.orders_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_product_id_seq OWNER TO ais;

--
-- Name: orders_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.orders_product_id_seq OWNED BY public.orders_product.id;


--
-- Name: orders_producttype; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.orders_producttype (
    id integer NOT NULL,
    name character varying(64),
    description text,
    selection_policy character varying(25) NOT NULL,
    display_in_product_list boolean NOT NULL
);


ALTER TABLE public.orders_producttype OWNER TO ais;

--
-- Name: orders_producttype_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.orders_producttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_producttype_id_seq OWNER TO ais;

--
-- Name: orders_producttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.orders_producttype_id_seq OWNED BY public.orders_producttype.id;


--
-- Name: orders_standarea; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.orders_standarea (
    product_ptr_id integer NOT NULL,
    width integer NOT NULL,
    depth integer NOT NULL,
    height integer NOT NULL
);


ALTER TABLE public.orders_standarea OWNER TO ais;

--
-- Name: people_programme; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.people_programme (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.people_programme OWNER TO ais;

--
-- Name: people_programme_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.people_programme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.people_programme_id_seq OWNER TO ais;

--
-- Name: people_programme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.people_programme_id_seq OWNED BY public.people_programme.id;


--
-- Name: profile; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.profile (
    user_id integer NOT NULL,
    birth_date date,
    gender character varying(10) NOT NULL,
    shirt_size character varying(3) NOT NULL,
    phone_number character varying(15),
    drivers_license character varying(10),
    allergy character varying(30),
    programme_id integer,
    registration_year integer,
    planned_graduation integer,
    linkedin_url character varying(200),
    picture character varying(100) NOT NULL,
    picture_original character varying(100) NOT NULL
);


ALTER TABLE public.profile OWNER TO ais;

--
-- Name: recruitment_customfield; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_customfield (
    id integer NOT NULL,
    question text NOT NULL,
    field_type character varying(20) NOT NULL,
    "position" integer NOT NULL,
    extra_field_id integer NOT NULL,
    required boolean NOT NULL
);


ALTER TABLE public.recruitment_customfield OWNER TO ais;

--
-- Name: recruitment_customfield_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_customfield_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_customfield_id_seq OWNER TO ais;

--
-- Name: recruitment_customfield_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_customfield_id_seq OWNED BY public.recruitment_customfield.id;


--
-- Name: recruitment_customfieldanswer; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_customfieldanswer (
    id integer NOT NULL,
    answer text NOT NULL,
    custom_field_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.recruitment_customfieldanswer OWNER TO ais;

--
-- Name: recruitment_customfieldanswer_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_customfieldanswer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_customfieldanswer_id_seq OWNER TO ais;

--
-- Name: recruitment_customfieldanswer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_customfieldanswer_id_seq OWNED BY public.recruitment_customfieldanswer.id;


--
-- Name: recruitment_customfieldargument; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_customfieldargument (
    id integer NOT NULL,
    value text NOT NULL,
    "position" integer NOT NULL,
    custom_field_id integer NOT NULL
);


ALTER TABLE public.recruitment_customfieldargument OWNER TO ais;

--
-- Name: recruitment_customfieldargument_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_customfieldargument_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_customfieldargument_id_seq OWNER TO ais;

--
-- Name: recruitment_customfieldargument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_customfieldargument_id_seq OWNED BY public.recruitment_customfieldargument.id;


--
-- Name: recruitment_extrafield; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_extrafield (
    id integer NOT NULL
);


ALTER TABLE public.recruitment_extrafield OWNER TO ais;

--
-- Name: recruitment_extrafield_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_extrafield_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_extrafield_id_seq OWNER TO ais;

--
-- Name: recruitment_extrafield_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_extrafield_id_seq OWNED BY public.recruitment_extrafield.id;


--
-- Name: recruitment_recruitmentapplication; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_recruitmentapplication (
    id integer NOT NULL,
    rating integer,
    interview_date timestamp with time zone,
    interview_location character varying(100),
    submission_date timestamp with time zone NOT NULL,
    status character varying(20),
    delegated_role_id integer,
    exhibitor_id integer,
    interviewer_id integer,
    recommended_role_id integer,
    recruitment_period_id integer NOT NULL,
    superior_user_id integer,
    user_id integer NOT NULL,
    scorecard character varying(300),
    drive_document character varying(300),
    interviewer2_id integer
);


ALTER TABLE public.recruitment_recruitmentapplication OWNER TO ais;

--
-- Name: recruitment_recruitmentapplication_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_recruitmentapplication_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_recruitmentapplication_id_seq OWNER TO ais;

--
-- Name: recruitment_recruitmentapplication_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_recruitmentapplication_id_seq OWNED BY public.recruitment_recruitmentapplication.id;


--
-- Name: recruitment_recruitmentapplicationcomment; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_recruitmentapplicationcomment (
    id integer NOT NULL,
    comment text,
    created_date timestamp with time zone NOT NULL,
    recruitment_application_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.recruitment_recruitmentapplicationcomment OWNER TO ais;

--
-- Name: recruitment_recruitmentapplicationcomment_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_recruitmentapplicationcomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_recruitmentapplicationcomment_id_seq OWNER TO ais;

--
-- Name: recruitment_recruitmentapplicationcomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_recruitmentapplicationcomment_id_seq OWNED BY public.recruitment_recruitmentapplicationcomment.id;


--
-- Name: recruitment_recruitmentperiod; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_recruitmentperiod (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL,
    interview_end_date timestamp with time zone NOT NULL,
    eligible_roles integer NOT NULL,
    application_questions_id integer,
    fair_id integer NOT NULL,
    interview_questions_id integer
);


ALTER TABLE public.recruitment_recruitmentperiod OWNER TO ais;

--
-- Name: recruitment_recruitmentperiod_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_recruitmentperiod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_recruitmentperiod_id_seq OWNER TO ais;

--
-- Name: recruitment_recruitmentperiod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_recruitmentperiod_id_seq OWNED BY public.recruitment_recruitmentperiod.id;


--
-- Name: recruitment_recruitmentperiod_recruitable_roles; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_recruitmentperiod_recruitable_roles (
    id integer NOT NULL,
    recruitmentperiod_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.recruitment_recruitmentperiod_recruitable_roles OWNER TO ais;

--
-- Name: recruitment_recruitmentperiod_recruitable_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_recruitmentperiod_recruitable_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_recruitmentperiod_recruitable_roles_id_seq OWNER TO ais;

--
-- Name: recruitment_recruitmentperiod_recruitable_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_recruitmentperiod_recruitable_roles_id_seq OWNED BY public.recruitment_recruitmentperiod_recruitable_roles.id;


--
-- Name: recruitment_role; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_role (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    parent_role_id integer,
    group_id integer,
    organization_group character varying(100)
);


ALTER TABLE public.recruitment_role OWNER TO ais;

--
-- Name: recruitment_role_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_role_id_seq OWNER TO ais;

--
-- Name: recruitment_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_role_id_seq OWNED BY public.recruitment_role.id;


--
-- Name: recruitment_roleapplication; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.recruitment_roleapplication (
    id integer NOT NULL,
    "order" integer NOT NULL,
    recruitment_application_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.recruitment_roleapplication OWNER TO ais;

--
-- Name: recruitment_roleapplication_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.recruitment_roleapplication_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recruitment_roleapplication_id_seq OWNER TO ais;

--
-- Name: recruitment_roleapplication_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.recruitment_roleapplication_id_seq OWNED BY public.recruitment_roleapplication.id;


--
-- Name: register_orderlog; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.register_orderlog (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    action character varying(30),
    products text NOT NULL,
    company_id integer NOT NULL,
    contact_id integer NOT NULL,
    fair_id integer NOT NULL
);


ALTER TABLE public.register_orderlog OWNER TO ais;

--
-- Name: register_orderlog_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.register_orderlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_orderlog_id_seq OWNER TO ais;

--
-- Name: register_orderlog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.register_orderlog_id_seq OWNED BY public.register_orderlog.id;


--
-- Name: register_signupcontract; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.register_signupcontract (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    contract character varying(100) NOT NULL,
    current boolean NOT NULL,
    fair_id integer NOT NULL
);


ALTER TABLE public.register_signupcontract OWNER TO ais;

--
-- Name: register_signupcontract_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.register_signupcontract_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_signupcontract_id_seq OWNER TO ais;

--
-- Name: register_signupcontract_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.register_signupcontract_id_seq OWNED BY public.register_signupcontract.id;


--
-- Name: register_signuplog; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.register_signuplog (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    contact_id integer NOT NULL,
    contract_id integer NOT NULL,
    company_id integer,
    type character varying(30)
);


ALTER TABLE public.register_signuplog OWNER TO ais;

--
-- Name: register_signuplog_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.register_signuplog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_signuplog_id_seq OWNER TO ais;

--
-- Name: register_signuplog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.register_signuplog_id_seq OWNED BY public.register_signuplog.id;


--
-- Name: sales_followup; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.sales_followup (
    id integer NOT NULL,
    status character varying(30),
    follow_up_date timestamp with time zone NOT NULL,
    sale_id integer NOT NULL
);


ALTER TABLE public.sales_followup OWNER TO ais;

--
-- Name: sales_followup_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.sales_followup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sales_followup_id_seq OWNER TO ais;

--
-- Name: sales_followup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.sales_followup_id_seq OWNED BY public.sales_followup.id;


--
-- Name: sales_sale; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.sales_sale (
    id integer NOT NULL,
    status character varying(30),
    responsible_id integer,
    company_id integer NOT NULL,
    fair_id integer,
    diversity_room boolean NOT NULL,
    events boolean NOT NULL,
    green_room boolean NOT NULL,
    nova boolean NOT NULL,
    contact_by_date date
);


ALTER TABLE public.sales_sale OWNER TO ais;

--
-- Name: sales_sale_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.sales_sale_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sales_sale_id_seq OWNER TO ais;

--
-- Name: sales_sale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.sales_sale_id_seq OWNED BY public.sales_sale.id;


--
-- Name: sales_salecomment; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.sales_salecomment (
    id integer NOT NULL,
    created_date timestamp with time zone NOT NULL,
    comment text,
    sale_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.sales_salecomment OWNER TO ais;

--
-- Name: sales_salecomment_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.sales_salecomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sales_salecomment_id_seq OWNER TO ais;

--
-- Name: sales_salecomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.sales_salecomment_id_seq OWNED BY public.sales_salecomment.id;


--
-- Name: student_profiles_matchingresult; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.student_profiles_matchingresult (
    id integer NOT NULL,
    score integer NOT NULL,
    created timestamp with time zone,
    updated timestamp with time zone,
    fair_id integer NOT NULL,
    student_id integer NOT NULL,
    exhibitor_id integer,
    CONSTRAINT student_profiles_matchingresult_score_check CHECK ((score >= 0))
);


ALTER TABLE public.student_profiles_matchingresult OWNER TO ais;

--
-- Name: student_profiles_matchingresult_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.student_profiles_matchingresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_profiles_matchingresult_id_seq OWNER TO ais;

--
-- Name: student_profiles_matchingresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.student_profiles_matchingresult_id_seq OWNED BY public.student_profiles_matchingresult.id;


--
-- Name: student_profiles_studentprofile; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.student_profiles_studentprofile (
    nickname character varying(512) NOT NULL,
    facebook_profile character varying(128),
    linkedin_profile character varying(128),
    phone_number character varying(32),
    id integer NOT NULL,
    id_string uuid NOT NULL
);


ALTER TABLE public.student_profiles_studentprofile OWNER TO ais;

--
-- Name: student_profiles_studentprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.student_profiles_studentprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_profiles_studentprofile_id_seq OWNER TO ais;

--
-- Name: student_profiles_studentprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.student_profiles_studentprofile_id_seq OWNED BY public.student_profiles_studentprofile.id;


--
-- Name: transportation_transportationorder; Type: TABLE; Schema: public; Owner: ais; Tablespace: 
--

CREATE TABLE public.transportation_transportationorder (
    id integer NOT NULL,
    number_of_packages integer NOT NULL,
    number_of_pallets integer NOT NULL,
    goods_description text NOT NULL,
    contact_name character varying(50) NOT NULL,
    contact_phone_number character varying(50) NOT NULL,
    delivery_city character varying(50) NOT NULL,
    delivery_street_address character varying(100) NOT NULL,
    delivery_zip_code character varying(10) NOT NULL,
    pickup_city character varying(50) NOT NULL,
    pickup_street_address character varying(100) NOT NULL,
    pickup_zip_code character varying(10) NOT NULL
);


ALTER TABLE public.transportation_transportationorder OWNER TO ais;

--
-- Name: transportation_transportationorder_id_seq; Type: SEQUENCE; Schema: public; Owner: ais
--

CREATE SEQUENCE public.transportation_transportationorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transportation_transportationorder_id_seq OWNER TO ais;

--
-- Name: transportation_transportationorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ais
--

ALTER SEQUENCE public.transportation_transportationorder_id_seq OWNED BY public.transportation_transportationorder.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquettable ALTER COLUMN id SET DEFAULT nextval('public.banquet_banquettable_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_banquetteattendant_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetticket ALTER COLUMN id SET DEFAULT nextval('public.banquet_banquetticket_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_company ALTER COLUMN id SET DEFAULT nextval('public.companies_company_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_company_related_programme ALTER COLUMN id SET DEFAULT nextval('public.companies_company_related_programme_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_contact ALTER COLUMN id SET DEFAULT nextval('public.companies_contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_invoicedetails ALTER COLUMN id SET DEFAULT nextval('public.companies_invoicedetails_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event ALTER COLUMN id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_allowed_groups ALTER COLUMN id SET DEFAULT nextval('public.events_event_allowed_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_tags ALTER COLUMN id SET DEFAULT nextval('public.events_event_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventanswer ALTER COLUMN id SET DEFAULT nextval('public.events_eventanswer_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventattendence ALTER COLUMN id SET DEFAULT nextval('public.events_eventattendence_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventquestion ALTER COLUMN id SET DEFAULT nextval('public.events_eventquestion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_continents ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_continents_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_job_types ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_job_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_programs ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_programs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_tags ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_values ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_values_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_work_fields ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_cataloginfo_work_fields_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_continent ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_continent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_hosts ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitor_hosts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_job_types ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitor_job_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_tags ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitor_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitorview ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitorview_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_jobtype ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_jobtype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_location ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_exhibitorlocation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_transportationalternative ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_transportationalternative_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_value ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_value_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_workfield ALTER COLUMN id SET DEFAULT nextval('public.exhibitors_workfield_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.fair_fair ALTER COLUMN id SET DEFAULT nextval('public.fair_fair_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.fair_partner ALTER COLUMN id SET DEFAULT nextval('public.fair_partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.fair_tag ALTER COLUMN id SET DEFAULT nextval('public.fair_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.locations_building ALTER COLUMN id SET DEFAULT nextval('public.locations_building_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.locations_location ALTER COLUMN id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.locations_room ALTER COLUMN id SET DEFAULT nextval('public.locations_room_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_answer ALTER COLUMN id SET DEFAULT nextval('public.matching_answer_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_category ALTER COLUMN id SET DEFAULT nextval('public.matching_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_continent ALTER COLUMN id SET DEFAULT nextval('public.matching_continent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_country ALTER COLUMN id SET DEFAULT nextval('public.matching_country_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_country_exhibitor ALTER COLUMN id SET DEFAULT nextval('public.matching_country_exhibitor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_jobtype ALTER COLUMN id SET DEFAULT nextval('public.matching_jobtype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_question ALTER COLUMN id SET DEFAULT nextval('public.matching_question_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_response ALTER COLUMN id SET DEFAULT nextval('public.matching_response_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerbase ALTER COLUMN id SET DEFAULT nextval('public.matching_studentanswerbase_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerbase_survey ALTER COLUMN id SET DEFAULT nextval('public.matching_studentanswerbase_survey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionbase ALTER COLUMN id SET DEFAULT nextval('public.matching_studentquestionbase_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionbase_survey ALTER COLUMN id SET DEFAULT nextval('public.matching_studentquestionbase_survey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_survey ALTER COLUMN id SET DEFAULT nextval('public.matching_survey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedencity ALTER COLUMN id SET DEFAULT nextval('public.matching_swedencities_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedencity_exhibitor ALTER COLUMN id SET DEFAULT nextval('public.matching_swedencities_exhibitor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedenregion ALTER COLUMN id SET DEFAULT nextval('public.matching_swedenregion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfield ALTER COLUMN id SET DEFAULT nextval('public.matching_workfield_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfield_survey ALTER COLUMN id SET DEFAULT nextval('public.matching_workfield_survey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfieldarea ALTER COLUMN id SET DEFAULT nextval('public.matching_workfieldarea_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.news_newsarticle ALTER COLUMN id SET DEFAULT nextval('public.news_newsarticle_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_electricityorder ALTER COLUMN id SET DEFAULT nextval('public.orders_electricityorder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_order ALTER COLUMN id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_product ALTER COLUMN id SET DEFAULT nextval('public.orders_product_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_producttype ALTER COLUMN id SET DEFAULT nextval('public.orders_producttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.people_programme ALTER COLUMN id SET DEFAULT nextval('public.people_programme_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfield ALTER COLUMN id SET DEFAULT nextval('public.recruitment_customfield_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfieldanswer ALTER COLUMN id SET DEFAULT nextval('public.recruitment_customfieldanswer_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfieldargument ALTER COLUMN id SET DEFAULT nextval('public.recruitment_customfieldargument_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_extrafield ALTER COLUMN id SET DEFAULT nextval('public.recruitment_extrafield_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication ALTER COLUMN id SET DEFAULT nextval('public.recruitment_recruitmentapplication_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplicationcomment ALTER COLUMN id SET DEFAULT nextval('public.recruitment_recruitmentapplicationcomment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod ALTER COLUMN id SET DEFAULT nextval('public.recruitment_recruitmentperiod_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod_recruitable_roles ALTER COLUMN id SET DEFAULT nextval('public.recruitment_recruitmentperiod_recruitable_roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_role ALTER COLUMN id SET DEFAULT nextval('public.recruitment_role_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_roleapplication ALTER COLUMN id SET DEFAULT nextval('public.recruitment_roleapplication_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_orderlog ALTER COLUMN id SET DEFAULT nextval('public.register_orderlog_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signupcontract ALTER COLUMN id SET DEFAULT nextval('public.register_signupcontract_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signuplog ALTER COLUMN id SET DEFAULT nextval('public.register_signuplog_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_followup ALTER COLUMN id SET DEFAULT nextval('public.sales_followup_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_sale ALTER COLUMN id SET DEFAULT nextval('public.sales_sale_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_salecomment ALTER COLUMN id SET DEFAULT nextval('public.sales_salecomment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.student_profiles_matchingresult ALTER COLUMN id SET DEFAULT nextval('public.student_profiles_matchingresult_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.student_profiles_studentprofile ALTER COLUMN id SET DEFAULT nextval('public.student_profiles_studentprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.transportation_transportationorder ALTER COLUMN id SET DEFAULT nextval('public.transportation_transportationorder_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 354, true);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 1, false);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$36000$CXe1p4ZcxNHd$+7lMENq+4x37pk0ICcdOz7ohqNHxlaLuceik2qzr9o0=	\N	t	admin				t	t	2018-03-20 11:34:42.347887+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 4559, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1155, true);


--
-- Data for Name: banquet_banquettable; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.banquet_banquettable (id, table_name, number_of_seats, fair_id) FROM stdin;
\.


--
-- Name: banquet_banquettable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.banquet_banquettable_id_seq', 1, false);


--
-- Data for Name: banquet_banquetteattendant; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.banquet_banquetteattendant (id, first_name, last_name, gender, phone_number, allergies, student_ticket, wants_alcohol, wants_lactose_free_food, wants_gluten_free_food, exhibitor_id, job_title, linkedin_url, user_id, email, wants_vegan_food, seat_number, ignore_from_placement, fair_id, confirmed, table_id, ticket_id) FROM stdin;
\.


--
-- Data for Name: banquet_banquetticket; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.banquet_banquetticket (id, name) FROM stdin;
\.


--
-- Name: banquet_banquetticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.banquet_banquetticket_id_seq', 1, false);


--
-- Data for Name: companies_company; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.companies_company (id, name, organisation_number, website, phone_number, address_city, address_country, address_street, address_zip_code, organisation_type, additional_address_information) FROM stdin;
\.


--
-- Name: companies_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.companies_company_id_seq', 1, false);


--
-- Data for Name: companies_company_related_programme; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.companies_company_related_programme (id, company_id, programme_id) FROM stdin;
\.


--
-- Name: companies_company_related_programme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.companies_company_related_programme_id_seq', 1, true);


--
-- Data for Name: companies_contact; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.companies_contact (id, name, email, title, cell_phone, work_phone, active, phone_switchboard, alternative_email, belongs_to_id, user_id, confirmed) FROM stdin;
\.


--
-- Name: companies_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.companies_contact_id_seq', 1, false);


--
-- Data for Name: companies_invoicedetails; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.companies_invoicedetails (id, reference, purchase_order_number, reference_phone_number, organisation_name, address, address_po_box, address_zip_code, identification, additional_information, company_id) FROM stdin;
\.


--
-- Name: companies_invoicedetails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.companies_invoicedetails_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 1, false);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2016-08-21 19:30:07.890697+00
2	auth	0001_initial	2016-08-21 19:30:08.064905+00
3	admin	0001_initial	2016-08-21 19:30:08.110799+00
4	admin	0002_logentry_remove_auto_add	2016-08-21 19:30:08.176141+00
5	contenttypes	0002_remove_content_type_name	2016-08-21 19:30:08.228237+00
6	auth	0002_alter_permission_name_max_length	2016-08-21 19:30:08.249531+00
7	auth	0003_alter_user_email_max_length	2016-08-21 19:30:08.273572+00
8	auth	0004_alter_user_username_opts	2016-08-21 19:30:08.294567+00
9	auth	0005_alter_user_last_login_null	2016-08-21 19:30:08.31597+00
10	auth	0006_require_contenttypes_0002	2016-08-21 19:30:08.320666+00
11	auth	0007_group_is_role	2016-08-21 19:30:08.357958+00
12	auth	0007_alter_validators_add_error_messages	2016-08-21 19:30:08.377688+00
13	auth	0008_merge	2016-08-21 19:30:08.381787+00
14	fair	0001_initial	2016-08-21 19:30:08.40985+00
15	companies	0001_initial	2016-08-21 19:30:08.480537+00
16	events	0001_initial	2016-08-21 19:30:08.517583+00
17	locations	0001_initial	2016-08-21 19:30:08.537524+00
18	news	0001_initial	2016-08-21 19:30:08.561452+00
19	people	0001_initial	2016-08-21 19:30:08.591442+00
20	people	0002_auto_20160820_1951	2016-08-21 19:30:08.660382+00
21	people	0003_profile_linkedin_url	2016-08-21 19:30:08.690957+00
22	people	0004_profile_image	2016-08-21 19:30:08.716098+00
23	people	0005_auto_20160820_2101	2016-08-21 19:30:08.741076+00
24	recruitment	0001_initial	2016-08-21 19:30:09.576573+00
25	recruitment	0002_recruitmentperiod_image	2016-08-21 19:30:09.627928+00
26	recruitment	0003_customfield_required	2016-08-21 19:30:09.708825+00
27	recruitment	0004_auto_20160820_1259	2016-08-21 19:30:09.820835+00
28	recruitment	0005_auto_20160821_0000	2016-08-21 19:30:09.914248+00
29	recruitment	0006_auto_20160821_0229	2016-08-21 19:30:09.982498+00
30	sessions	0001_initial	2016-08-21 19:30:10.008352+00
31	people	0006_auto_20160822_1051	2016-08-22 11:42:27.697988+00
32	recruitment	0007_auto_20160822_1051	2016-08-22 11:42:28.699574+00
33	recruitment	0008_auto_20160822_1102	2016-08-22 11:42:28.768967+00
34	recruitment	0009_auto_20160826_2253	2016-08-27 23:11:32.065368+00
35	recruitment	0010_auto_20160827_2110	2016-08-27 23:11:32.162134+00
36	recruitment	0011_auto_20160828_0108	2016-08-27 23:11:32.275741+00
37	recruitment	0012_auto_20160828_2054	2016-08-30 03:09:34.373063+00
38	recruitment	0013_auto_20160829_2316	2016-08-30 03:09:34.601948+00
39	recruitment	0014_remove_recruitmentperiod_image	2016-08-30 03:09:34.65583+00
40	recruitment	0015_auto_20160830_0250	2016-08-30 03:09:34.777878+00
41	events	0002_auto_20160811_1532	2016-09-01 02:00:39.615469+00
42	recruitment	0016_auto_20160831_2242	2016-09-01 02:00:40.989866+00
43	recruitment	0017_auto_20160901_1459	2016-09-01 13:03:09.461907+00
44	recruitment	0018_auto_20160904_0056	2016-09-04 00:34:23.77151+00
45	people	0007_auto_20160910_0109	2016-09-11 17:11:42.983816+00
53	auth	0008_alter_user_username_max_length	2016-09-12 07:41:37.588558+00
54	recruitment	0019_role_group	2016-09-12 07:41:37.676984+00
55	recruitment	0020_auto_20160910_0055	2016-09-12 07:41:37.730699+00
56	recruitment	0021_auto_20160910_0100	2016-09-12 07:41:37.785206+00
57	recruitment	0022_auto_20160910_0104	2016-09-12 07:41:37.836137+00
58	recruitment	0023_auto_20160910_0106	2016-09-12 07:41:37.885726+00
59	recruitment	0024_auto_20160910_0113	2016-09-12 07:41:37.948507+00
60	recruitment	0025_auto_20160911_1906	2016-09-12 07:41:38.069261+00
61	auth	0009_remove_group_is_role	2016-09-12 07:53:05.116352+00
62	recruitment	0026_auto_20160919_1036	2016-09-19 08:48:07.768888+00
63	events	0003_auto_20160914_2313	2016-10-02 22:18:35.898977+00
64	events	0004_auto_20160915_0052	2016-10-02 22:18:36.241697+00
65	events	0005_auto_20160915_1031	2016-10-02 22:18:36.34054+00
66	events	0006_event_allowed_groups	2016-10-02 22:18:36.418369+00
67	events	0007_event_fair	2016-10-02 22:26:54.966768+00
68	events	0008_auto_20160922_1117	2016-10-02 22:26:55.09878+00
69	events	0009_event_attendence_description	2016-10-02 22:26:55.164839+00
70	events	0010_event_description_short	2016-10-02 22:26:55.240545+00
71	exhibitors	0001_initial	2016-10-02 22:26:56.020073+00
72	exhibitors	0002_auto_20160921_1213	2016-10-02 22:26:56.024001+00
73	exhibitors	0003_auto_20160921_1222	2016-10-02 22:26:56.027529+00
74	exhibitors	0004_auto_20160921_1223	2016-10-02 22:26:56.03003+00
75	exhibitors	0001_squashed_0004_auto_20160921_1223	2016-10-02 22:26:56.035472+00
76	events	0011_auto_20161003_1046	2016-10-03 11:38:23.980967+00
77	exhibitors	0002_auto_20161004_2340	2016-10-05 10:11:35.569988+00
78	exhibitors	0003_exhibitor_location	2016-10-05 10:11:35.674296+00
79	companies	0002_auto_20160920_2202	2016-10-12 18:57:25.367586+00
80	companies	0003_auto_20160920_2213	2016-10-12 18:57:26.393472+00
81	companies	0004_exhibitor_responsible	2016-10-12 18:57:26.464561+00
82	companies	0005_auto_20161006_1147	2016-10-12 18:57:27.358523+00
83	companies	0006_auto_20161010_1922	2016-10-12 18:57:27.638906+00
84	companies	0007_auto_20161010_1923	2016-10-12 18:57:27.723514+00
85	companies	0008_auto_20161010_1927	2016-10-12 18:57:27.868037+00
86	companies	0009_auto_20161010_1930	2016-10-12 18:57:28.158092+00
87	companies	0010_auto_20161010_1939	2016-10-12 18:57:28.224198+00
88	companies	0011_auto_20161010_1941	2016-10-12 18:57:28.522466+00
89	companies	0012_company_organisation_type	2016-10-12 18:57:28.717307+00
90	companies	0013_company_additional_address_information	2016-10-12 18:57:28.803438+00
91	companies	0014_contact_phone_switchboard	2016-10-12 18:57:28.866162+00
92	companies	0015_contact_alternative_email	2016-10-12 18:57:28.932699+00
93	companies	0016_auto_20161012_1825	2016-10-12 18:57:29.002352+00
94	events	0012_auto_20161006_0840	2016-10-12 18:57:29.222376+00
95	events	0013_auto_20161007_1803	2016-10-12 18:57:29.370257+00
96	exhibitors	0004_auto_20161006_2020	2016-10-12 18:57:32.03699+00
97	exhibitors	0005_auto_20161010_1924	2016-10-12 18:57:32.177773+00
98	exhibitors	0006_auto_20161010_1925	2016-10-12 18:57:32.593334+00
99	exhibitors	0007_auto_20161010_1927	2016-10-12 18:57:32.910551+00
100	exhibitors	0008_auto_20161010_1928	2016-10-12 18:57:33.178428+00
101	exhibitors	0009_auto_20161010_1940	2016-10-12 18:57:33.271303+00
102	exhibitors	0010_exhibitor_status	2016-10-12 18:57:33.350852+00
103	exhibitors	0011_exhibitor_allergies	2016-10-12 18:57:33.432282+00
104	exhibitors	0012_exhibitor_requests_for_stand_placement	2016-10-12 18:57:33.538348+00
105	exhibitors	0013_exhibitor_heavy_duty_electric_equipment	2016-10-12 18:57:33.65734+00
106	exhibitors	0014_exhibitor_other_information_about_the_stand	2016-10-12 18:57:33.773468+00
107	exhibitors	0015_exhibitor_transport_to_fair_type	2016-10-12 18:57:33.870322+00
108	exhibitors	0016_auto_20161012_0105	2016-10-12 18:57:34.308732+00
109	exhibitors	0017_auto_20161012_0124	2016-10-12 18:57:34.387185+00
110	exhibitors	0018_exhibitor_transport_from_fair_type	2016-10-12 18:57:34.575524+00
111	exhibitors	0019_auto_20161012_0127	2016-10-12 18:57:34.670386+00
112	exhibitors	0020_exhibitor_estimated_arrival	2016-10-12 18:57:34.74827+00
113	exhibitors	0021_auto_20161012_0216	2016-10-12 18:57:35.094941+00
114	exhibitors	0022_auto_20161012_0235	2016-10-12 18:57:35.810125+00
115	exhibitors	0023_auto_20161012_0240	2016-10-12 18:57:35.991394+00
116	orders	0001_initial	2016-10-12 18:57:36.277931+00
117	orders	0002_auto_20161011_2252	2016-10-12 18:57:36.459277+00
118	exhibitors	0024_auto_20161014_2150	2016-10-14 21:33:50.662305+00
119	exhibitors	0025_auto_20161014_2157	2016-10-14 21:33:50.865768+00
120	exhibitors	0026_exhibitor_estimated_arrival_of_representatives	2016-10-15 00:23:23.482294+00
121	exhibitors	0027_banquetteattendant	2016-10-15 15:36:48.369792+00
122	events	0014_event_attendence_approvement_required	2016-10-15 16:19:37.228866+00
123	events	0015_auto_20161014_1936	2016-10-15 16:19:37.58832+00
124	exhibitors	0028_auto_20161015_1902	2016-10-15 17:09:45.12521+00
125	fair	0002_partner_tag	2016-10-19 14:03:30.561536+00
126	events	0014_auto_20161012_2055	2016-10-19 14:03:30.808122+00
127	events	0016_merge_20161018_2148	2016-10-19 14:03:30.812492+00
128	exhibitors	0024_cataloginfo_tags	2016-10-19 14:03:30.984319+00
129	exhibitors	0029_merge_20161018_2148	2016-10-19 14:03:30.988925+00
130	events	0017_event_location	2016-10-21 10:30:29.62169+00
131	news	0002_newsarticle_image	2016-10-21 14:43:05.321987+00
132	exhibitors	0030_auto_20161022_1835	2016-10-23 11:20:34.040503+00
133	exhibitors	0031_auto_20161023_2040	2016-10-24 11:26:36.288774+00
134	exhibitors	0032_auto_20161024_1320	2016-10-24 11:26:36.403726+00
135	exhibitors	0033_auto_20161025_1929	2016-10-25 20:36:11.844732+00
136	exhibitors	0034_auto_20161025_1930	2016-10-25 20:36:12.161536+00
137	exhibitors	0035_auto_20161025_2252	2016-10-25 21:50:59.689534+00
138	exhibitors	0036_auto_20161025_2257	2016-10-25 21:50:59.795225+00
139	exhibitors	0037_auto_20161025_2331	2016-10-25 21:50:59.878805+00
140	exhibitors	0038_auto_20161025_2358	2016-10-26 20:34:51.372558+00
141	people	0008_auto_20161019_1130	2016-10-26 20:34:51.708605+00
142	events	0018_auto_20161027_2101	2016-10-30 13:35:35.467804+00
143	events	0019_event_published	2016-11-01 00:28:12.898073+00
144	events	0020_auto_20161031_2226	2016-11-01 00:28:13.034279+00
145	events	0021_auto_20161031_2257	2016-11-01 00:28:13.138575+00
146	events	0022_auto_20161031_2330	2016-11-01 00:28:13.249158+00
147	events	0023_event_extra_field	2016-11-02 15:12:37.150851+00
148	exhibitors	0039_auto_20161106_1724	2016-11-06 17:15:01.499871+00
149	exhibitors	0040_banquetteattendant_ignore_from_placement	2016-11-06 17:15:01.805365+00
150	events	0024_auto_20161106_1830	2016-11-06 17:49:29.191707+00
151	exhibitors	0041_auto_20161109_1418	2016-11-09 14:48:12.08269+00
152	events	0025_eventattendence_submission_date	2016-11-09 19:09:05.920009+00
153	locations	0002_auto_20161109_2044	2016-11-09 21:17:34.107245+00
154	exhibitors	0042_exhibitor_fair_location	2016-11-09 21:17:34.286587+00
155	exhibitors	0042_auto_20161109_2235	2016-11-09 22:09:06.193008+00
156	exhibitors	0043_merge_20161109_2254	2016-11-09 22:09:06.196909+00
157	events	0026_event_external_signup_url	2016-11-11 15:14:14.830892+00
158	events	0027_auto_20161110_0028	2016-11-11 15:14:14.982747+00
159	exhibitors	0044_auto_20161115_1038	2016-11-15 09:59:56.552697+00
160	exhibitors	0045_auto_20161118_2007	2016-11-18 19:27:14.230833+00
161	orders	0003_auto_20161118_2007	2016-11-18 19:27:14.32769+00
162	exhibitors	0046_exhibitor_manual_invoice	2016-11-22 15:09:20.64718+00
163	companies	0017_contact_belongs_to	2017-03-17 15:30:01.798207+00
164	companies	0018_contact_user	2017-03-17 15:30:02.044788+00
165	companies	0019_move_company_contact	2017-03-17 15:30:03.180794+00
166	companies	0020_remove_company_contact	2017-03-17 15:30:03.550369+00
167	companies	0021_auto_20170304_1648	2017-03-17 15:30:03.823741+00
168	companies	0022_auto_20170306_1828	2017-03-17 15:30:04.354476+00
169	companies	0023_auto_20170306_2339	2017-03-17 15:30:04.896308+00
170	fair	0003_auto_20170218_2244	2017-03-17 15:30:05.217888+00
171	exhibitors	0047_banquetteattendant_fair	2017-03-17 15:30:05.464033+00
172	fair	0004_auto_20170305_1039	2017-03-17 15:30:05.976848+00
173	fair	0005_fair_current	2017-03-17 15:30:06.201297+00
174	register	0001_initial	2017-03-17 15:30:06.38479+00
175	register	0002_signuplog	2017-03-17 15:30:06.587067+00
176	register	0003_auto_20170305_1418	2017-03-17 15:30:07.004884+00
177	register	0004_auto_20170305_1442	2017-03-17 15:30:07.128358+00
178	register	0005_signuplog_company	2017-03-17 15:30:07.278309+00
179	sales	0001_initial	2017-03-17 15:30:07.500504+00
180	sales	0002_auto_20161026_2012	2017-03-17 15:30:08.881136+00
181	sales	0003_auto_20161026_2046	2017-03-17 15:30:10.111437+00
182	sales	0004_followup_sale	2017-03-17 15:30:10.262417+00
183	sales	0005_auto_20161109_1303	2017-03-17 15:30:10.520261+00
184	sales	0006_auto_20161118_1225	2017-03-17 15:30:10.75964+00
185	sales	0007_auto_20170218_2356	2017-03-17 15:30:11.287256+00
186	sales	0008_campaign_fair	2017-03-17 15:30:11.443186+00
187	sales	0009_auto_20170305_1025	2017-03-17 15:30:12.071966+00
188	sales	0010_auto_20170306_2339	2017-03-17 15:30:12.28436+00
189	sales	0011_sale_preliminary_registration	2017-03-17 15:30:12.472953+00
190	sales	0012_auto_20170306_2351	2017-03-17 15:30:12.778883+00
191	sales	0013_auto_20170308_0031	2017-03-17 15:30:13.788873+00
192	sales	0014_auto_20170323_0853	2017-03-23 14:11:10.207022+00
193	companies	0024_contact_confirmed	2017-03-27 13:49:27.761142+00
194	companies	0025_auto_20170410_1307	2017-04-10 12:54:24.044684+00
195	sales	0015_auto_20170330_1535	2017-04-10 12:54:24.245772+00
196	sales	0016_auto_20170330_1537	2017-04-10 12:54:25.005271+00
197	sales	0017_auto_20170330_1547	2017-04-10 12:54:25.719491+00
198	sales	0018_sale_nova	2017-04-25 17:26:31.749571+00
199	news	0003_auto_20170510_1039	2017-05-30 21:17:04.805307+00
200	news	0004_newsarticle_author	2017-05-30 21:17:04.843113+00
201	sales	0019_sale_contact_by_date	2017-06-12 15:49:41.774288+00
202	exhibitors	0048_auto_20170525_2050	2017-06-30 23:29:26.681292+00
203	exhibitors	0049_exhibitor_logo	2017-06-30 23:29:26.871913+00
204	exhibitors	0050_auto_20170526_1807	2017-06-30 23:29:27.294342+00
205	exhibitors	0051_auto_20170530_1348	2017-06-30 23:29:27.774259+00
206	exhibitors	0052_auto_20170530_1401	2017-06-30 23:29:28.158721+00
207	exhibitors	0053_auto_20170603_1718	2017-06-30 23:29:28.626357+00
208	exhibitors	0054_auto_20170607_1657	2017-06-30 23:29:28.863637+00
209	exhibitors	0055_auto_20170629_2041	2017-06-30 23:29:30.778021+00
210	exhibitors	0056_exhibitor_accept_terms	2017-06-30 23:29:31.022548+00
211	orders	0004_auto_20170516_2215	2017-06-30 23:29:31.230641+00
212	orders	0005_remove_producttype_formview	2017-06-30 23:29:31.366156+00
213	orders	0006_auto_20170525_1838	2017-06-30 23:29:31.577881+00
214	register	0006_signuplog_type	2017-07-06 18:15:38.911148+00
215	matching	0001_initial	2017-07-31 20:33:51.07935+00
216	matching	0002_auto_20170629_2347	2017-07-31 20:33:53.135135+00
217	matching	0003_remove_question_survey	2017-07-31 20:33:53.289974+00
218	matching	0004_survey_questions	2017-07-31 20:33:53.475436+00
219	matching	0005_question_category	2017-07-31 20:33:53.656014+00
220	matching	0006_auto_20170630_1616	2017-07-31 20:33:53.81047+00
221	matching	0007_auto_20170630_1957	2017-07-31 20:33:54.515672+00
222	matching	0008_auto_20170630_2142	2017-07-31 20:33:54.823634+00
223	matching	0009_auto_20170630_2319	2017-07-31 20:33:54.9687+00
224	matching	0010_auto_20170630_2322	2017-07-31 20:33:55.397586+00
225	matching	0011_auto_20170630_2334	2017-07-31 20:33:56.120503+00
226	matching	0012_question_help_text	2017-07-31 20:33:56.283286+00
227	matching	0013_auto_20170702_1649	2017-07-31 20:33:56.414156+00
228	matching	0014_auto_20170702_1927	2017-07-31 20:33:56.557913+00
229	matching	0015_auto_20170702_2052	2017-07-31 20:33:56.691804+00
230	matching	0016_auto_20170703_2140	2017-07-31 20:33:56.831353+00
231	matching	0017_auto_20170815_1710	2017-08-15 15:50:39.342488+00
232	exhibitors	0057_auto_20170828_2027	2017-08-28 20:01:03.956462+00
233	register	0007_orderlog	2017-09-01 07:26:36.559031+00
234	register	0008_auto_20170831_1353	2017-09-01 07:26:36.861362+00
235	fair	0006_auto_20170831_2211	2017-09-04 09:33:22.180881+00
236	recruitment	0027_recruitmentapplication_scorecard	2017-09-18 18:46:03.420994+00
237	recruitment	0028_recruitmentapplication_drive_document	2017-09-18 18:46:03.634779+00
238	exhibitors	0058_exhibitor_booth_number	2017-09-22 15:05:33.632664+00
239	people	0009_profile_portrait	2017-09-22 15:05:34.111489+00
240	exhibitors	0059_exhibitorview	2017-10-02 09:39:38.551941+00
241	exhibitors	0060_auto_20170927_1742	2017-10-02 09:39:38.683459+00
242	people	0010_remove_profile_portrait	2017-10-02 09:39:38.817827+00
243	exhibitors	0059_auto_20170926_2020	2017-10-05 08:41:08.223003+00
244	exhibitors	0060_auto_20170926_2021	2017-10-05 08:41:08.477382+00
245	banquet	0001_initial	2017-10-05 08:41:08.653441+00
246	exhibitors	0061_merge_20170930_2132	2017-10-05 08:41:08.660643+00
247	banquet	0002_auto_20171007_1144	2017-10-10 17:26:46.456587+00
248	banquet	0003_auto_20171007_1144	2017-10-10 17:26:46.636276+00
249	banquet	0004_banquetteattendant_confirmed	2017-10-10 17:26:46.904661+00
250	banquet	0005_banquetteattendant_ticket_type	2017-10-10 17:26:47.130743+00
251	banquet	0006_auto_20171007_1350	2017-10-10 17:26:47.964747+00
252	banquet	0007_auto_20171007_1355	2017-10-10 17:26:48.142689+00
253	banquet	0008_auto_20171007_1355	2017-10-10 17:26:48.306089+00
254	student_profiles	0001_initial	2017-10-11 10:52:36.453407+00
255	student_profiles	0002_auto_20170930_1718	2017-10-11 10:52:36.478507+00
256	banquet	0010_banquetticket	2017-10-13 10:04:13.205343+00
257	banquet	0011_auto_20171010_2205	2017-10-13 10:04:13.241547+00
258	banquet	0014_banquetteattendant_ticket	2017-10-13 10:04:13.509055+00
259	exhibitors	0062_auto_20171013_1616	2017-10-13 14:16:55.076536+00
260	exhibitors	0062_auto_20171012_1910	2017-10-15 13:57:00.701698+00
261	matching	0018_auto_20171015_1238	2017-10-20 07:07:00.085158+00
262	matching	0019_auto_20171016_1404	2017-10-20 07:07:02.387177+00
263	matching	0020_auto_20171016_1610	2017-10-20 07:07:02.872981+00
264	matching	0021_auto_20171016_2146	2017-10-20 07:07:03.858697+00
265	matching	0022_auto_20171017_1037	2017-10-20 07:07:04.524832+00
266	student_profiles	0003_matchingresult	2017-10-20 07:07:04.751273+00
267	exhibitors	0063_exhibitor_comment	2017-10-24 15:24:15.053+00
268	exhibitors	0064_exhibitor_location_at_fair	2017-10-26 11:22:39.76163+00
269	matching	0023_auto_20171023_2319	2017-10-26 11:22:41.753518+00
270	matching	0024_auto_20171024_1142	2017-10-26 11:22:42.27573+00
271	matching	0025_auto_20171024_1306	2017-10-26 11:22:43.52908+00
272	matching	0026_auto_20171024_1309	2017-10-26 11:22:43.899321+00
273	matching	0027_auto_20171024_1311	2017-10-26 11:22:44.627867+00
274	matching	0023_studentquestionbase_company_question	2017-10-26 11:22:44.936625+00
275	matching	0024_auto_20171017_1513	2017-10-26 11:22:45.791901+00
276	matching	0028_merge_20171024_1340	2017-10-26 11:22:45.799401+00
277	matching	0029_auto_20171025_1458	2017-10-26 11:22:48.23686+00
278	banquet	0015_auto_20171020_1132	2017-10-27 14:22:42.472095+00
279	banquet	0016_auto_20171024_2115	2017-10-27 14:22:42.748317+00
280	matching	0025_auto_20171019_1333	2017-10-27 14:22:43.63743+00
281	matching	0026_auto_20171019_1838	2017-10-27 14:22:44.864749+00
282	matching	0030_merge_20171027_1420	2017-10-27 14:22:44.869525+00
283	student_profiles	0004_auto_20171026_2249	2017-10-29 11:00:51.10552+00
284	matching	0031_auto_20171030_1602	2017-10-30 21:24:53.733585+00
285	exhibitors	0065_exhibitor_tags	2017-10-30 21:24:53.971876+00
286	exhibitors	0066_update_room_tags	2017-10-30 21:24:54.177861+00
287	exhibitors	0067_auto_20171030_1602	2017-10-30 21:24:54.344617+00
288	exhibitors	0068_auto_20171030_1619	2017-10-30 21:24:56.783612+00
289	exhibitors	0069_exhibitor_job_types	2017-10-30 21:24:57.010723+00
290	exhibitors	0070_exhibitor_job_types2	2017-10-30 21:24:59.610397+00
291	exhibitors	0071_auto_20171030_2040	2017-10-30 21:25:00.712633+00
292	matching	0032_auto_20171101_1227	2017-11-01 13:19:42.522326+00
293	matching	0033_auto_20171101_1239	2017-11-01 13:19:42.71538+00
294	matching	0034_jobtype_studentanswerjobtype	2017-11-02 17:15:13.248403+00
295	matching	0035_add_jobtypes	2017-11-02 17:15:13.287225+00
296	matching	0036_jobtype_exhibitor_question	2017-11-02 17:15:13.498387+00
297	student_profiles	0005_auto_20171101_1400	2017-11-02 22:49:54.906186+00
298	student_profiles	0006_auto_20171102_1045	2017-11-02 22:49:55.532015+00
300	matching	0037_survey_relates_to	2017-11-03 16:53:50.893369+00
301	matching	0038_auto_20171102_2058	2017-11-03 16:53:51.173878+00
308	student_profiles	0007_studentprofile_id_string	2017-11-05 18:03:54.561743+00
309	student_profiles	0008_auto_20171105_1902	2017-11-05 18:03:54.797087+00
310	banquet	0017_auto_20171109_1411	2017-11-09 13:38:10.302139+00
311	events	0028_eventattendence_sent_email	2017-11-09 22:28:21.559958+00
312	companies	0026_company_related_programme	2017-11-14 11:48:48.826103+00
313	banquet	0018_auto_20171115_0955	2017-11-19 15:42:45.945577+00
314	recruitment	0029_role_organization_group	2017-12-05 20:46:22.392974+00
315	sites	0001_initial	2018-01-03 16:58:12.756541+00
316	sites	0002_alter_domain_unique	2018-01-03 16:58:12.808475+00
317	fair	0007_auto_20180103_1813	2018-01-03 17:14:46.74778+00
318	fair	0007_auto_20180103_1814	2018-01-03 17:25:55.756558+00
319	companies	0027_invoicedetails	2018-02-01 17:52:33.365846+00
320	transportation	0001_initial	2018-02-01 17:52:33.47808+00
321	transportation	0002_auto_20180128_1443	2018-02-01 17:52:34.036245+00
322	transportation	0003_transportationorder_company	2018-02-01 17:52:34.714643+00
323	transportation	0004_remove_transportationorder_company	2018-02-01 17:52:35.014885+00
324	exhibitors	0072_exhibitor_invoice_details	2018-02-01 17:52:35.368888+00
325	exhibitors	0073_auto_20180121_1738	2018-02-04 13:57:07.214711+00
326	exhibitors	0074_auto_20180128_1326	2018-02-04 13:57:07.906639+00
327	exhibitors	0075_auto_20180128_1443	2018-02-04 13:57:08.613201+00
328	exhibitors	0076_auto_20180128_1506	2018-02-04 13:57:09.00073+00
329	exhibitors	0077_auto_20180128_2357	2018-02-04 13:57:14.957831+00
330	exhibitors	0078_auto_20180129_0012	2018-02-04 13:57:15.984298+00
331	exhibitors	0079_auto_20180131_1726	2018-02-04 13:57:18.11338+00
332	fair	0007_auto_20180110_1829	2018-02-04 13:57:19.258956+00
333	fair	0008_auto_20180110_1850	2018-02-04 13:57:19.653656+00
334	matching	0037_auto_20180119_1405	2018-02-04 13:57:31.104366+00
335	matching	0038_auto_20180119_1533	2018-02-04 13:57:33.687645+00
336	matching	0039_question_required	2018-02-04 13:57:34.527723+00
337	matching	0040_auto_20180119_1742	2018-02-04 14:04:49.608365+00
338	matching	0041_remove_response_question	2018-02-04 14:04:50.567211+00
339	orders	0007_standarea	2018-02-04 14:04:53.559021+00
340	orders	0008_auto_20180127_1433	2018-02-04 14:04:55.264617+00
341	orders	0009_producttype_selection_policy	2018-02-04 14:04:55.846055+00
342	orders	0010_producttype_display_in_product_list	2018-02-04 14:04:56.967939+00
343	orders	0011_product_display_in_product_list	2018-02-04 14:05:00.699725+00
344	orders	0012_auto_20180127_1906	2018-02-04 14:05:02.665557+00
345	orders	0013_electricityorder	2018-02-04 14:05:28.079581+00
346	orders	0014_product_included_for_all	2018-02-04 14:05:28.192322+00
347	recruitment	0030_recruitmentapplication_interviewer2	2018-02-04 14:05:28.408551+00
348	transportation	0005_auto_20180128_1843	2018-02-04 14:05:28.473789+00
349	transportation	0006_auto_20180131_1726	2018-02-04 14:05:28.543141+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 349, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Data for Name: events_event; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_event (id, name, event_start, event_end, capacity, description, registration_start, registration_end, registration_last_day_cancel, public_registration, fair_id, attendence_description, description_short, send_submission_mail, submission_mail_body, submission_mail_subject, image, image_original, attendence_approvement_required, registration_required, location, published, extra_field_id, confirmation_mail_body, confirmation_mail_subject, rejection_mail_body, rejection_mail_subject, external_signup_url) FROM stdin;
\.


--
-- Data for Name: events_event_allowed_groups; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_event_allowed_groups (id, event_id, group_id) FROM stdin;
\.


--
-- Name: events_event_allowed_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_event_allowed_groups_id_seq', 1, false);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);


--
-- Data for Name: events_event_tags; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_event_tags (id, event_id, tag_id) FROM stdin;
\.


--
-- Name: events_event_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_event_tags_id_seq', 2, true);


--
-- Data for Name: events_eventanswer; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_eventanswer (id, answer, attendence_id, question_id) FROM stdin;
\.


--
-- Name: events_eventanswer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_eventanswer_id_seq', 1, false);


--
-- Data for Name: events_eventattendence; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_eventattendence (id, status, event_id, user_id, submission_date, sent_email) FROM stdin;
\.


--
-- Name: events_eventattendence_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_eventattendence_id_seq', 1, false);


--
-- Data for Name: events_eventquestion; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.events_eventquestion (id, question_text, event_id, required) FROM stdin;
\.


--
-- Name: events_eventquestion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.events_eventquestion_id_seq', 1, false);


--
-- Name: exhibitors_banquetteattendant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_banquetteattendant_id_seq', 1, false);


--
-- Data for Name: exhibitors_cataloginfo; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo (id, display_name, slug, short_description, description, employees_sweden, employees_world, countries, website_url, facebook_url, twitter_url, linkedin_url, exhibitor_id, main_work_field_id, ad, logo, logo_small, ad_original, logo_original, location_at_fair, location_at_fair_original) FROM stdin;
\.


--
-- Data for Name: exhibitors_cataloginfo_continents; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_continents (id, cataloginfo_id, continent_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_continents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_continents_id_seq', 556, true);


--
-- Name: exhibitors_cataloginfo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_id_seq', 1, false);


--
-- Data for Name: exhibitors_cataloginfo_job_types; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_job_types (id, cataloginfo_id, jobtype_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_job_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_job_types_id_seq', 636, true);


--
-- Data for Name: exhibitors_cataloginfo_programs; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_programs (id, cataloginfo_id, programme_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_programs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_programs_id_seq', 1680, true);


--
-- Data for Name: exhibitors_cataloginfo_tags; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_tags (id, cataloginfo_id, tag_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_tags_id_seq', 35, true);


--
-- Data for Name: exhibitors_cataloginfo_values; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_values (id, cataloginfo_id, value_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_values_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_values_id_seq', 1055, true);


--
-- Data for Name: exhibitors_cataloginfo_work_fields; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_cataloginfo_work_fields (id, cataloginfo_id, workfield_id) FROM stdin;
\.


--
-- Name: exhibitors_cataloginfo_work_fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_cataloginfo_work_fields_id_seq', 1368, true);


--
-- Data for Name: exhibitors_continent; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_continent (id, name) FROM stdin;
\.


--
-- Name: exhibitors_continent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_continent_id_seq', 1, false);


--
-- Data for Name: exhibitors_exhibitor; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_exhibitor (id, company_id, fair_id, location_id, contact_id, status, fair_location_id, logo, about_text, facts_text, accept_terms, booth_number, comment, location_at_fair, invoice_details_id, inbound_transportation_id, outbound_transportation_id, delivery_order_id, pickup_order_id) FROM stdin;
\.


--
-- Data for Name: exhibitors_exhibitor_hosts; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_exhibitor_hosts (id, exhibitor_id, user_id) FROM stdin;
\.


--
-- Name: exhibitors_exhibitor_hosts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitor_hosts_id_seq', 409, true);


--
-- Name: exhibitors_exhibitor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitor_id_seq', 1, false);


--
-- Data for Name: exhibitors_exhibitor_job_types; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_exhibitor_job_types (id, exhibitor_id, jobtype_id) FROM stdin;
\.


--
-- Name: exhibitors_exhibitor_job_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitor_job_types_id_seq', 218, true);


--
-- Data for Name: exhibitors_exhibitor_tags; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_exhibitor_tags (id, exhibitor_id, tag_id) FROM stdin;
\.


--
-- Name: exhibitors_exhibitor_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitor_tags_id_seq', 28, true);


--
-- Name: exhibitors_exhibitorlocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitorlocation_id_seq', 1, false);


--
-- Data for Name: exhibitors_exhibitorview; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_exhibitorview (id, choices, user_id) FROM stdin;
\.


--
-- Name: exhibitors_exhibitorview_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_exhibitorview_id_seq', 1, false);


--
-- Data for Name: exhibitors_jobtype; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_jobtype (id, name) FROM stdin;
\.


--
-- Name: exhibitors_jobtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_jobtype_id_seq', 1, false);


--
-- Data for Name: exhibitors_location; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_location (id, name) FROM stdin;
\.


--
-- Data for Name: exhibitors_transportationalternative; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_transportationalternative (id, name, transportation_type, inbound) FROM stdin;
\.


--
-- Name: exhibitors_transportationalternative_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_transportationalternative_id_seq', 1, false);


--
-- Data for Name: exhibitors_value; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_value (id, name) FROM stdin;
\.


--
-- Name: exhibitors_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_value_id_seq', 1, false);


--
-- Data for Name: exhibitors_workfield; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.exhibitors_workfield (id, name) FROM stdin;
\.


--
-- Name: exhibitors_workfield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.exhibitors_workfield_id_seq', 1, false);


--
-- Data for Name: fair_fair; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.fair_fair (id, name, year, description, registration_end_date, registration_start_date, current, complete_registration_close_date, complete_registration_start_date) FROM stdin;
\.


--
-- Name: fair_fair_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.fair_fair_id_seq', 1, false);


--
-- Data for Name: fair_partner; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.fair_partner (id, name, logo, url, main_partner, fair_id) FROM stdin;
\.


--
-- Name: fair_partner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.fair_partner_id_seq', 1, false);


--
-- Data for Name: fair_tag; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.fair_tag (id, name, description) FROM stdin;
\.


--
-- Name: fair_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.fair_tag_id_seq', 1, false);


--
-- Data for Name: locations_building; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.locations_building (id, name, map_image) FROM stdin;
\.


--
-- Name: locations_building_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.locations_building_id_seq', 1, false);


--
-- Data for Name: locations_location; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.locations_location (id, room_id, x_pos, y_pos) FROM stdin;
\.


--
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.locations_location_id_seq', 1, false);


--
-- Data for Name: locations_room; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.locations_room (id, name, floor, building_id) FROM stdin;
\.


--
-- Name: locations_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.locations_room_id_seq', 1, false);


--
-- Data for Name: matching_answer; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_answer (id, question_id, response_id, polymorphic_ctype_id) FROM stdin;
\.


--
-- Name: matching_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_answer_id_seq', 1, false);


--
-- Data for Name: matching_booleanans; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_booleanans (answer_ptr_id, ans) FROM stdin;
\.


--
-- Data for Name: matching_category; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_category (id, name, "order", description, survey_id) FROM stdin;
\.


--
-- Name: matching_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_category_id_seq', 1, false);


--
-- Data for Name: matching_choiceans; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_choiceans (answer_ptr_id, ans) FROM stdin;
\.


--
-- Data for Name: matching_continent; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_continent (id, name, continent_id, survey_id) FROM stdin;
\.


--
-- Name: matching_continent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_continent_id_seq', 1, false);


--
-- Data for Name: matching_country; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_country (id, name, continent_id) FROM stdin;
\.


--
-- Data for Name: matching_country_exhibitor; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_country_exhibitor (id, country_id, exhibitor_id) FROM stdin;
\.


--
-- Name: matching_country_exhibitor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_country_exhibitor_id_seq', 1, false);


--
-- Name: matching_country_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_country_id_seq', 1, false);


--
-- Data for Name: matching_integerans; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_integerans (answer_ptr_id, ans) FROM stdin;
\.


--
-- Data for Name: matching_jobtype; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_jobtype (id, job_type, job_type_id, exhibitor_question_id) FROM stdin;
\.


--
-- Name: matching_jobtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_jobtype_id_seq', 1, false);


--
-- Data for Name: matching_question; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_question (id, text, question_type, name, help_text, category_id, survey_id, required) FROM stdin;
\.


--
-- Name: matching_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_question_id_seq', 1, false);


--
-- Data for Name: matching_response; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_response (id, exhibitor_id, survey_id) FROM stdin;
\.


--
-- Name: matching_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_response_id_seq', 1, false);


--
-- Data for Name: matching_studentanswerbase; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerbase (id, student_id, created, updated) FROM stdin;
\.


--
-- Name: matching_studentanswerbase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_studentanswerbase_id_seq', 1, false);


--
-- Data for Name: matching_studentanswerbase_survey; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerbase_survey (id, studentanswerbase_id, survey_id) FROM stdin;
\.


--
-- Name: matching_studentanswerbase_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_studentanswerbase_survey_id_seq', 180, true);


--
-- Data for Name: matching_studentanswercontinent; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswercontinent (studentanswerbase_ptr_id, continent_id) FROM stdin;
\.


--
-- Data for Name: matching_studentanswergrading; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswergrading (studentanswerbase_ptr_id, answer, question_id) FROM stdin;
\.


--
-- Data for Name: matching_studentanswerjobtype; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerjobtype (studentanswerbase_ptr_id, job_type_id) FROM stdin;
\.


--
-- Data for Name: matching_studentanswerregion; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerregion (studentanswerbase_ptr_id, region_id) FROM stdin;
\.


--
-- Data for Name: matching_studentanswerslider; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerslider (studentanswerbase_ptr_id, answer_max, question_id, answer_min) FROM stdin;
\.


--
-- Data for Name: matching_studentanswerworkfield; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentanswerworkfield (studentanswerbase_ptr_id, answer, work_field_id) FROM stdin;
\.


--
-- Data for Name: matching_studentquestionbase; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentquestionbase (id, question, question_type, company_question_id) FROM stdin;
\.


--
-- Name: matching_studentquestionbase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_studentquestionbase_id_seq', 1, false);


--
-- Data for Name: matching_studentquestionbase_survey; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentquestionbase_survey (id, studentquestionbase_id, survey_id) FROM stdin;
\.


--
-- Name: matching_studentquestionbase_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_studentquestionbase_survey_id_seq', 4, true);


--
-- Data for Name: matching_studentquestiongrading; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentquestiongrading (studentquestionbase_ptr_id, grading_size) FROM stdin;
\.


--
-- Data for Name: matching_studentquestionslider; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_studentquestionslider (studentquestionbase_ptr_id, min_value, max_value, logarithmic, units) FROM stdin;
\.


--
-- Data for Name: matching_survey; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_survey (id, name, description, fair_id, relates_to_id) FROM stdin;
\.


--
-- Name: matching_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_survey_id_seq', 1, false);


--
-- Name: matching_swedencities_exhibitor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_swedencities_exhibitor_id_seq', 1, false);


--
-- Name: matching_swedencities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_swedencities_id_seq', 1, false);


--
-- Data for Name: matching_swedencity; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_swedencity (id, city, region_id) FROM stdin;
\.


--
-- Data for Name: matching_swedencity_exhibitor; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_swedencity_exhibitor (id, swedencity_id, exhibitor_id) FROM stdin;
\.


--
-- Data for Name: matching_swedenregion; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_swedenregion (id, name, survey_id, region_id) FROM stdin;
\.


--
-- Name: matching_swedenregion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_swedenregion_id_seq', 1, false);


--
-- Data for Name: matching_textans; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_textans (answer_ptr_id, ans) FROM stdin;
\.


--
-- Data for Name: matching_workfield; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_workfield (id, work_field, work_area_id) FROM stdin;
\.


--
-- Name: matching_workfield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_workfield_id_seq', 1, false);


--
-- Data for Name: matching_workfield_survey; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_workfield_survey (id, workfield_id, survey_id) FROM stdin;
\.


--
-- Name: matching_workfield_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_workfield_survey_id_seq', 10, true);


--
-- Data for Name: matching_workfieldarea; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.matching_workfieldarea (id, work_area) FROM stdin;
\.


--
-- Name: matching_workfieldarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.matching_workfieldarea_id_seq', 1, false);


--
-- Data for Name: news_newsarticle; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.news_newsarticle (id, title, html_article_text, publication_date, image, ingress, author) FROM stdin;
\.


--
-- Name: news_newsarticle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.news_newsarticle_id_seq', 1, false);


--
-- Data for Name: orders_electricityorder; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.orders_electricityorder (id, total_power, number_of_outlets, equipment_description, exhibitor_id) FROM stdin;
\.


--
-- Name: orders_electricityorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.orders_electricityorder_id_seq', 1, false);


--
-- Data for Name: orders_order; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.orders_order (id, amount, exhibitor_id, product_id) FROM stdin;
\.


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 1, false);


--
-- Data for Name: orders_product; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.orders_product (id, name, description, coa_number, price, fair_id, product_type_id, display_in_product_list, included_for_all) FROM stdin;
\.


--
-- Name: orders_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.orders_product_id_seq', 1, false);


--
-- Data for Name: orders_producttype; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.orders_producttype (id, name, description, selection_policy, display_in_product_list) FROM stdin;
\.


--
-- Name: orders_producttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.orders_producttype_id_seq', 1, false);


--
-- Data for Name: orders_standarea; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.orders_standarea (product_ptr_id, width, depth, height) FROM stdin;
\.


--
-- Data for Name: people_programme; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.people_programme (id, name) FROM stdin;
\.


--
-- Name: people_programme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.people_programme_id_seq', 1, false);


--
-- Data for Name: profile; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.profile (user_id, birth_date, gender, shirt_size, phone_number, drivers_license, allergy, programme_id, registration_year, planned_graduation, linkedin_url, picture, picture_original) FROM stdin;
\.


--
-- Data for Name: recruitment_customfield; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_customfield (id, question, field_type, "position", extra_field_id, required) FROM stdin;
\.


--
-- Name: recruitment_customfield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_customfield_id_seq', 1, false);


--
-- Data for Name: recruitment_customfieldanswer; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_customfieldanswer (id, answer, custom_field_id, user_id) FROM stdin;
\.


--
-- Name: recruitment_customfieldanswer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_customfieldanswer_id_seq', 1, false);


--
-- Data for Name: recruitment_customfieldargument; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_customfieldargument (id, value, "position", custom_field_id) FROM stdin;
\.


--
-- Name: recruitment_customfieldargument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_customfieldargument_id_seq', 1, false);


--
-- Data for Name: recruitment_extrafield; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_extrafield (id) FROM stdin;
\.


--
-- Name: recruitment_extrafield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_extrafield_id_seq', 1, false);


--
-- Data for Name: recruitment_recruitmentapplication; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_recruitmentapplication (id, rating, interview_date, interview_location, submission_date, status, delegated_role_id, exhibitor_id, interviewer_id, recommended_role_id, recruitment_period_id, superior_user_id, user_id, scorecard, drive_document, interviewer2_id) FROM stdin;
\.


--
-- Name: recruitment_recruitmentapplication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_recruitmentapplication_id_seq', 1, false);


--
-- Data for Name: recruitment_recruitmentapplicationcomment; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_recruitmentapplicationcomment (id, comment, created_date, recruitment_application_id, user_id) FROM stdin;
\.


--
-- Name: recruitment_recruitmentapplicationcomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_recruitmentapplicationcomment_id_seq', 1, false);


--
-- Data for Name: recruitment_recruitmentperiod; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_recruitmentperiod (id, name, start_date, end_date, interview_end_date, eligible_roles, application_questions_id, fair_id, interview_questions_id) FROM stdin;
\.


--
-- Name: recruitment_recruitmentperiod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_recruitmentperiod_id_seq', 1, false);


--
-- Data for Name: recruitment_recruitmentperiod_recruitable_roles; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_recruitmentperiod_recruitable_roles (id, recruitmentperiod_id, role_id) FROM stdin;
\.


--
-- Name: recruitment_recruitmentperiod_recruitable_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_recruitmentperiod_recruitable_roles_id_seq', 170, true);


--
-- Data for Name: recruitment_role; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_role (id, name, description, parent_role_id, group_id, organization_group) FROM stdin;
\.


--
-- Name: recruitment_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_role_id_seq', 1, false);


--
-- Data for Name: recruitment_roleapplication; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.recruitment_roleapplication (id, "order", recruitment_application_id, role_id) FROM stdin;
\.


--
-- Name: recruitment_roleapplication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.recruitment_roleapplication_id_seq', 1, false);


--
-- Data for Name: register_orderlog; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.register_orderlog (id, "timestamp", action, products, company_id, contact_id, fair_id) FROM stdin;
\.


--
-- Name: register_orderlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.register_orderlog_id_seq', 1, false);


--
-- Data for Name: register_signupcontract; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.register_signupcontract (id, name, contract, current, fair_id) FROM stdin;
\.


--
-- Name: register_signupcontract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.register_signupcontract_id_seq', 1, false);


--
-- Data for Name: register_signuplog; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.register_signuplog (id, "timestamp", contact_id, contract_id, company_id, type) FROM stdin;
\.


--
-- Name: register_signuplog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.register_signuplog_id_seq', 1, false);


--
-- Data for Name: sales_followup; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.sales_followup (id, status, follow_up_date, sale_id) FROM stdin;
\.


--
-- Name: sales_followup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.sales_followup_id_seq', 1, false);


--
-- Data for Name: sales_sale; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.sales_sale (id, status, responsible_id, company_id, fair_id, diversity_room, events, green_room, nova, contact_by_date) FROM stdin;
\.


--
-- Name: sales_sale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.sales_sale_id_seq', 1, false);


--
-- Data for Name: sales_salecomment; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.sales_salecomment (id, created_date, comment, sale_id, user_id) FROM stdin;
\.


--
-- Name: sales_salecomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.sales_salecomment_id_seq', 1, false);


--
-- Data for Name: student_profiles_matchingresult; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.student_profiles_matchingresult (id, score, created, updated, fair_id, student_id, exhibitor_id) FROM stdin;
\.


--
-- Name: student_profiles_matchingresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.student_profiles_matchingresult_id_seq', 1, false);


--
-- Data for Name: student_profiles_studentprofile; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.student_profiles_studentprofile (nickname, facebook_profile, linkedin_profile, phone_number, id, id_string) FROM stdin;
\.


--
-- Name: student_profiles_studentprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.student_profiles_studentprofile_id_seq', 1, false);


--
-- Data for Name: transportation_transportationorder; Type: TABLE DATA; Schema: public; Owner: ais
--

COPY public.transportation_transportationorder (id, number_of_packages, number_of_pallets, goods_description, contact_name, contact_phone_number, delivery_city, delivery_street_address, delivery_zip_code, pickup_city, pickup_street_address, pickup_zip_code) FROM stdin;
\.


--
-- Name: transportation_transportationorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ais
--

SELECT pg_catalog.setval('public.transportation_transportationorder_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: banquet_banquettable_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.banquet_banquettable
    ADD CONSTRAINT banquet_banquettable_pkey PRIMARY KEY (id);


--
-- Name: banquet_banquetticket_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.banquet_banquetticket
    ADD CONSTRAINT banquet_banquetticket_pkey PRIMARY KEY (id);


--
-- Name: companies_company_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_company
    ADD CONSTRAINT companies_company_pkey PRIMARY KEY (id);


--
-- Name: companies_company_related_programme_company_id_b3476e16_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_company_related_programme
    ADD CONSTRAINT companies_company_related_programme_company_id_b3476e16_uniq UNIQUE (company_id, programme_id);


--
-- Name: companies_company_related_programme_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_company_related_programme
    ADD CONSTRAINT companies_company_related_programme_pkey PRIMARY KEY (id);


--
-- Name: companies_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_contact
    ADD CONSTRAINT companies_contact_pkey PRIMARY KEY (id);


--
-- Name: companies_contact_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_contact
    ADD CONSTRAINT companies_contact_user_id_key UNIQUE (user_id);


--
-- Name: companies_invoicedetails_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.companies_invoicedetails
    ADD CONSTRAINT companies_invoicedetails_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: events_event_allowed_groups_event_id_742a305c_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_event_allowed_groups
    ADD CONSTRAINT events_event_allowed_groups_event_id_742a305c_uniq UNIQUE (event_id, group_id);


--
-- Name: events_event_allowed_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_event_allowed_groups
    ADD CONSTRAINT events_event_allowed_groups_pkey PRIMARY KEY (id);


--
-- Name: events_event_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_pkey PRIMARY KEY (id);


--
-- Name: events_event_tags_event_id_b2716ce9_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_event_tags
    ADD CONSTRAINT events_event_tags_event_id_b2716ce9_uniq UNIQUE (event_id, tag_id);


--
-- Name: events_event_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_event_tags
    ADD CONSTRAINT events_event_tags_pkey PRIMARY KEY (id);


--
-- Name: events_eventanswer_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_eventanswer
    ADD CONSTRAINT events_eventanswer_pkey PRIMARY KEY (id);


--
-- Name: events_eventattendence_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_eventattendence
    ADD CONSTRAINT events_eventattendence_pkey PRIMARY KEY (id);


--
-- Name: events_eventquestion_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.events_eventquestion
    ADD CONSTRAINT events_eventquestion_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_banquetteattendant_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT exhibitors_banquetteattendant_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_continents_cataloginfo_id_3badc7e4_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_continents
    ADD CONSTRAINT exhibitors_cataloginfo_continents_cataloginfo_id_3badc7e4_uniq UNIQUE (cataloginfo_id, continent_id);


--
-- Name: exhibitors_cataloginfo_continents_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_continents
    ADD CONSTRAINT exhibitors_cataloginfo_continents_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_exhibitor_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo
    ADD CONSTRAINT exhibitors_cataloginfo_exhibitor_id_key UNIQUE (exhibitor_id);


--
-- Name: exhibitors_cataloginfo_job_types_cataloginfo_id_f8f9724c_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_job_types
    ADD CONSTRAINT exhibitors_cataloginfo_job_types_cataloginfo_id_f8f9724c_uniq UNIQUE (cataloginfo_id, jobtype_id);


--
-- Name: exhibitors_cataloginfo_job_types_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_job_types
    ADD CONSTRAINT exhibitors_cataloginfo_job_types_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo
    ADD CONSTRAINT exhibitors_cataloginfo_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_programs_cataloginfo_id_4c1f70b0_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_programs
    ADD CONSTRAINT exhibitors_cataloginfo_programs_cataloginfo_id_4c1f70b0_uniq UNIQUE (cataloginfo_id, programme_id);


--
-- Name: exhibitors_cataloginfo_programs_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_programs
    ADD CONSTRAINT exhibitors_cataloginfo_programs_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_tags_cataloginfo_id_8e89b683_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_tags
    ADD CONSTRAINT exhibitors_cataloginfo_tags_cataloginfo_id_8e89b683_uniq UNIQUE (cataloginfo_id, tag_id);


--
-- Name: exhibitors_cataloginfo_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_tags
    ADD CONSTRAINT exhibitors_cataloginfo_tags_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_values_cataloginfo_id_b26a6aea_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_values
    ADD CONSTRAINT exhibitors_cataloginfo_values_cataloginfo_id_b26a6aea_uniq UNIQUE (cataloginfo_id, value_id);


--
-- Name: exhibitors_cataloginfo_values_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_values
    ADD CONSTRAINT exhibitors_cataloginfo_values_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_cataloginfo_work_fields_cataloginfo_id_82d6d8e2_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_work_fields
    ADD CONSTRAINT exhibitors_cataloginfo_work_fields_cataloginfo_id_82d6d8e2_uniq UNIQUE (cataloginfo_id, workfield_id);


--
-- Name: exhibitors_cataloginfo_work_fields_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_work_fields
    ADD CONSTRAINT exhibitors_cataloginfo_work_fields_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_continent_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_continent
    ADD CONSTRAINT exhibitors_continent_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitor_fair_location_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_fair_location_id_key UNIQUE (fair_location_id);


--
-- Name: exhibitors_exhibitor_hosts_exhibitor_id_d9c97ced_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_hosts
    ADD CONSTRAINT exhibitors_exhibitor_hosts_exhibitor_id_d9c97ced_uniq UNIQUE (exhibitor_id, user_id);


--
-- Name: exhibitors_exhibitor_hosts_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_hosts
    ADD CONSTRAINT exhibitors_exhibitor_hosts_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitor_job_types_exhibitor_id_de8b59fb_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_job_types
    ADD CONSTRAINT exhibitors_exhibitor_job_types_exhibitor_id_de8b59fb_uniq UNIQUE (exhibitor_id, jobtype_id);


--
-- Name: exhibitors_exhibitor_job_types_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_job_types
    ADD CONSTRAINT exhibitors_exhibitor_job_types_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitor_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitor_tags_exhibitor_id_13e18904_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_tags
    ADD CONSTRAINT exhibitors_exhibitor_tags_exhibitor_id_13e18904_uniq UNIQUE (exhibitor_id, tag_id);


--
-- Name: exhibitors_exhibitor_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitor_tags
    ADD CONSTRAINT exhibitors_exhibitor_tags_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitorlocation_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_location
    ADD CONSTRAINT exhibitors_exhibitorlocation_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_exhibitorview_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_exhibitorview
    ADD CONSTRAINT exhibitors_exhibitorview_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_jobtype_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_jobtype
    ADD CONSTRAINT exhibitors_jobtype_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_transportationalternative_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_transportationalternative
    ADD CONSTRAINT exhibitors_transportationalternative_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_value_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_value
    ADD CONSTRAINT exhibitors_value_pkey PRIMARY KEY (id);


--
-- Name: exhibitors_workfield_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.exhibitors_workfield
    ADD CONSTRAINT exhibitors_workfield_pkey PRIMARY KEY (id);


--
-- Name: fair_fair_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.fair_fair
    ADD CONSTRAINT fair_fair_pkey PRIMARY KEY (id);


--
-- Name: fair_partner_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.fair_partner
    ADD CONSTRAINT fair_partner_pkey PRIMARY KEY (id);


--
-- Name: fair_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.fair_tag
    ADD CONSTRAINT fair_tag_pkey PRIMARY KEY (id);


--
-- Name: locations_building_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.locations_building
    ADD CONSTRAINT locations_building_pkey PRIMARY KEY (id);


--
-- Name: locations_location_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.locations_location
    ADD CONSTRAINT locations_location_pkey PRIMARY KEY (id);


--
-- Name: locations_room_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.locations_room
    ADD CONSTRAINT locations_room_pkey PRIMARY KEY (id);


--
-- Name: matching_answer_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_answer
    ADD CONSTRAINT matching_answer_pkey PRIMARY KEY (id);


--
-- Name: matching_booleanans_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_booleanans
    ADD CONSTRAINT matching_booleanans_pkey PRIMARY KEY (answer_ptr_id);


--
-- Name: matching_category_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_category
    ADD CONSTRAINT matching_category_pkey PRIMARY KEY (id);


--
-- Name: matching_choiceans_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_choiceans
    ADD CONSTRAINT matching_choiceans_pkey PRIMARY KEY (answer_ptr_id);


--
-- Name: matching_continent_continent_ee83ca7d_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_continent
    ADD CONSTRAINT matching_continent_continent_ee83ca7d_uniq UNIQUE (name);


--
-- Name: matching_continent_continent_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_continent
    ADD CONSTRAINT matching_continent_continent_id_key UNIQUE (continent_id);


--
-- Name: matching_continent_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_continent
    ADD CONSTRAINT matching_continent_pkey PRIMARY KEY (id);


--
-- Name: matching_country_exhibitor_country_id_3d954d65_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_country_exhibitor
    ADD CONSTRAINT matching_country_exhibitor_country_id_3d954d65_uniq UNIQUE (country_id, exhibitor_id);


--
-- Name: matching_country_exhibitor_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_country_exhibitor
    ADD CONSTRAINT matching_country_exhibitor_pkey PRIMARY KEY (id);


--
-- Name: matching_country_name_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_country
    ADD CONSTRAINT matching_country_name_key UNIQUE (name);


--
-- Name: matching_country_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_country
    ADD CONSTRAINT matching_country_pkey PRIMARY KEY (id);


--
-- Name: matching_integerans_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_integerans
    ADD CONSTRAINT matching_integerans_pkey PRIMARY KEY (answer_ptr_id);


--
-- Name: matching_jobtype_job_type_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_jobtype
    ADD CONSTRAINT matching_jobtype_job_type_id_key UNIQUE (job_type_id);


--
-- Name: matching_jobtype_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_jobtype
    ADD CONSTRAINT matching_jobtype_pkey PRIMARY KEY (id);


--
-- Name: matching_question_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_question
    ADD CONSTRAINT matching_question_pkey PRIMARY KEY (id);


--
-- Name: matching_response_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_response
    ADD CONSTRAINT matching_response_pkey PRIMARY KEY (id);


--
-- Name: matching_studentanswerbase_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerbase
    ADD CONSTRAINT matching_studentanswerbase_pkey PRIMARY KEY (id);


--
-- Name: matching_studentanswerbase_s_studentanswerbase_id_3acd85dd_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerbase_survey
    ADD CONSTRAINT matching_studentanswerbase_s_studentanswerbase_id_3acd85dd_uniq UNIQUE (studentanswerbase_id, survey_id);


--
-- Name: matching_studentanswerbase_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerbase_survey
    ADD CONSTRAINT matching_studentanswerbase_survey_pkey PRIMARY KEY (id);


--
-- Name: matching_studentanswercontinent_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswercontinent
    ADD CONSTRAINT matching_studentanswercontinent_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentanswergrading_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswergrading
    ADD CONSTRAINT matching_studentanswergrading_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentanswerjobtype_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerjobtype
    ADD CONSTRAINT matching_studentanswerjobtype_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentanswerregion_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerregion
    ADD CONSTRAINT matching_studentanswerregion_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentanswerslider_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerslider
    ADD CONSTRAINT matching_studentanswerslider_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentanswerworkfield_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentanswerworkfield
    ADD CONSTRAINT matching_studentanswerworkfield_pkey PRIMARY KEY (studentanswerbase_ptr_id);


--
-- Name: matching_studentquestionba_studentquestionbase_id_53930a28_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentquestionbase_survey
    ADD CONSTRAINT matching_studentquestionba_studentquestionbase_id_53930a28_uniq UNIQUE (studentquestionbase_id, survey_id);


--
-- Name: matching_studentquestionbase_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentquestionbase
    ADD CONSTRAINT matching_studentquestionbase_pkey PRIMARY KEY (id);


--
-- Name: matching_studentquestionbase_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentquestionbase_survey
    ADD CONSTRAINT matching_studentquestionbase_survey_pkey PRIMARY KEY (id);


--
-- Name: matching_studentquestiongrading_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentquestiongrading
    ADD CONSTRAINT matching_studentquestiongrading_pkey PRIMARY KEY (studentquestionbase_ptr_id);


--
-- Name: matching_studentquestionslider_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_studentquestionslider
    ADD CONSTRAINT matching_studentquestionslider_pkey PRIMARY KEY (studentquestionbase_ptr_id);


--
-- Name: matching_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_survey
    ADD CONSTRAINT matching_survey_pkey PRIMARY KEY (id);


--
-- Name: matching_swedencities_city_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedencity
    ADD CONSTRAINT matching_swedencities_city_key UNIQUE (city);


--
-- Name: matching_swedencities_exhibitor_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedencity_exhibitor
    ADD CONSTRAINT matching_swedencities_exhibitor_pkey PRIMARY KEY (id);


--
-- Name: matching_swedencities_exhibitor_swedencities_id_53d848f1_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedencity_exhibitor
    ADD CONSTRAINT matching_swedencities_exhibitor_swedencities_id_53d848f1_uniq UNIQUE (swedencity_id, exhibitor_id);


--
-- Name: matching_swedencities_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedencity
    ADD CONSTRAINT matching_swedencities_pkey PRIMARY KEY (id);


--
-- Name: matching_swedenregion_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedenregion
    ADD CONSTRAINT matching_swedenregion_pkey PRIMARY KEY (id);


--
-- Name: matching_swedenregion_region_id_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_swedenregion
    ADD CONSTRAINT matching_swedenregion_region_id_key UNIQUE (region_id);


--
-- Name: matching_textans_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_textans
    ADD CONSTRAINT matching_textans_pkey PRIMARY KEY (answer_ptr_id);


--
-- Name: matching_workfield_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfield
    ADD CONSTRAINT matching_workfield_pkey PRIMARY KEY (id);


--
-- Name: matching_workfield_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfield_survey
    ADD CONSTRAINT matching_workfield_survey_pkey PRIMARY KEY (id);


--
-- Name: matching_workfield_survey_workfield_id_8bab2a4b_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfield_survey
    ADD CONSTRAINT matching_workfield_survey_workfield_id_8bab2a4b_uniq UNIQUE (workfield_id, survey_id);


--
-- Name: matching_workfield_work_field_2b046ccb_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfield
    ADD CONSTRAINT matching_workfield_work_field_2b046ccb_uniq UNIQUE (work_field);


--
-- Name: matching_workfieldarea_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfieldarea
    ADD CONSTRAINT matching_workfieldarea_pkey PRIMARY KEY (id);


--
-- Name: matching_workfieldarea_work_area_ae8a7ff2_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.matching_workfieldarea
    ADD CONSTRAINT matching_workfieldarea_work_area_ae8a7ff2_uniq UNIQUE (work_area);


--
-- Name: news_newsarticle_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.news_newsarticle
    ADD CONSTRAINT news_newsarticle_pkey PRIMARY KEY (id);


--
-- Name: orders_electricityorder_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.orders_electricityorder
    ADD CONSTRAINT orders_electricityorder_pkey PRIMARY KEY (id);


--
-- Name: orders_order_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_pkey PRIMARY KEY (id);


--
-- Name: orders_product_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.orders_product
    ADD CONSTRAINT orders_product_pkey PRIMARY KEY (id);


--
-- Name: orders_producttype_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.orders_producttype
    ADD CONSTRAINT orders_producttype_pkey PRIMARY KEY (id);


--
-- Name: orders_standarea_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.orders_standarea
    ADD CONSTRAINT orders_standarea_pkey PRIMARY KEY (product_ptr_id);


--
-- Name: people_programme_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.people_programme
    ADD CONSTRAINT people_programme_pkey PRIMARY KEY (id);


--
-- Name: profile_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (user_id);


--
-- Name: recruitment_customfield_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_customfield
    ADD CONSTRAINT recruitment_customfield_pkey PRIMARY KEY (id);


--
-- Name: recruitment_customfieldanswer_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_customfieldanswer
    ADD CONSTRAINT recruitment_customfieldanswer_pkey PRIMARY KEY (id);


--
-- Name: recruitment_customfieldargument_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_customfieldargument
    ADD CONSTRAINT recruitment_customfieldargument_pkey PRIMARY KEY (id);


--
-- Name: recruitment_extrafield_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_extrafield
    ADD CONSTRAINT recruitment_extrafield_pkey PRIMARY KEY (id);


--
-- Name: recruitment_recruitmentapplication_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recruitmentapplication_pkey PRIMARY KEY (id);


--
-- Name: recruitment_recruitmentapplicationcomment_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_recruitmentapplicationcomment
    ADD CONSTRAINT recruitment_recruitmentapplicationcomment_pkey PRIMARY KEY (id);


--
-- Name: recruitment_recruitmentperio_recruitmentperiod_id_c417424c_uniq; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod_recruitable_roles
    ADD CONSTRAINT recruitment_recruitmentperio_recruitmentperiod_id_c417424c_uniq UNIQUE (recruitmentperiod_id, role_id);


--
-- Name: recruitment_recruitmentperiod_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod
    ADD CONSTRAINT recruitment_recruitmentperiod_pkey PRIMARY KEY (id);


--
-- Name: recruitment_recruitmentperiod_recruitable_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod_recruitable_roles
    ADD CONSTRAINT recruitment_recruitmentperiod_recruitable_roles_pkey PRIMARY KEY (id);


--
-- Name: recruitment_role_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_role
    ADD CONSTRAINT recruitment_role_pkey PRIMARY KEY (id);


--
-- Name: recruitment_roleapplication_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.recruitment_roleapplication
    ADD CONSTRAINT recruitment_roleapplication_pkey PRIMARY KEY (id);


--
-- Name: register_orderlog_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.register_orderlog
    ADD CONSTRAINT register_orderlog_pkey PRIMARY KEY (id);


--
-- Name: register_signupcontract_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.register_signupcontract
    ADD CONSTRAINT register_signupcontract_pkey PRIMARY KEY (id);


--
-- Name: register_signuplog_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.register_signuplog
    ADD CONSTRAINT register_signuplog_pkey PRIMARY KEY (id);


--
-- Name: sales_followup_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.sales_followup
    ADD CONSTRAINT sales_followup_pkey PRIMARY KEY (id);


--
-- Name: sales_sale_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.sales_sale
    ADD CONSTRAINT sales_sale_pkey PRIMARY KEY (id);


--
-- Name: sales_salecomment_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.sales_salecomment
    ADD CONSTRAINT sales_salecomment_pkey PRIMARY KEY (id);


--
-- Name: student_profiles_matchingresult_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.student_profiles_matchingresult
    ADD CONSTRAINT student_profiles_matchingresult_pkey PRIMARY KEY (id);


--
-- Name: student_profiles_studentprofile_id_string_key; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.student_profiles_studentprofile
    ADD CONSTRAINT student_profiles_studentprofile_id_string_key UNIQUE (id_string);


--
-- Name: student_profiles_studentprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.student_profiles_studentprofile
    ADD CONSTRAINT student_profiles_studentprofile_pkey PRIMARY KEY (id);


--
-- Name: transportation_transportationorder_pkey; Type: CONSTRAINT; Schema: public; Owner: ais; Tablespace: 
--

ALTER TABLE ONLY public.transportation_transportationorder
    ADD CONSTRAINT transportation_transportationorder_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: banquet_banquettable_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX banquet_banquettable_df5a2d4b ON public.banquet_banquettable USING btree (fair_id);


--
-- Name: banquet_banquetteattendant_649b92cd; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX banquet_banquetteattendant_649b92cd ON public.banquet_banquetteattendant USING btree (ticket_id);


--
-- Name: banquet_banquetteattendant_a15b1ede; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX banquet_banquetteattendant_a15b1ede ON public.banquet_banquetteattendant USING btree (table_id);


--
-- Name: companies_company_related_programme_447d3092; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX companies_company_related_programme_447d3092 ON public.companies_company_related_programme USING btree (company_id);


--
-- Name: companies_company_related_programme_82558bcc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX companies_company_related_programme_82558bcc ON public.companies_company_related_programme USING btree (programme_id);


--
-- Name: companies_contact_7de27a13; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX companies_contact_7de27a13 ON public.companies_contact USING btree (belongs_to_id);


--
-- Name: companies_invoicedetails_company_id_372c7b1a; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX companies_invoicedetails_company_id_372c7b1a ON public.companies_invoicedetails USING btree (company_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: events_event_25868659; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_25868659 ON public.events_event USING btree (extra_field_id);


--
-- Name: events_event_allowed_groups_0e939a4f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_allowed_groups_0e939a4f ON public.events_event_allowed_groups USING btree (group_id);


--
-- Name: events_event_allowed_groups_4437cfac; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_allowed_groups_4437cfac ON public.events_event_allowed_groups USING btree (event_id);


--
-- Name: events_event_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_df5a2d4b ON public.events_event USING btree (fair_id);


--
-- Name: events_event_tags_4437cfac; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_tags_4437cfac ON public.events_event_tags USING btree (event_id);


--
-- Name: events_event_tags_76f094bc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_event_tags_76f094bc ON public.events_event_tags USING btree (tag_id);


--
-- Name: events_eventanswer_7aa0f6ee; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_eventanswer_7aa0f6ee ON public.events_eventanswer USING btree (question_id);


--
-- Name: events_eventanswer_a8d1ad63; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_eventanswer_a8d1ad63 ON public.events_eventanswer USING btree (attendence_id);


--
-- Name: events_eventattendence_4437cfac; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_eventattendence_4437cfac ON public.events_eventattendence USING btree (event_id);


--
-- Name: events_eventattendence_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_eventattendence_e8701ad4 ON public.events_eventattendence USING btree (user_id);


--
-- Name: events_eventquestion_4437cfac; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX events_eventquestion_4437cfac ON public.events_eventquestion USING btree (event_id);


--
-- Name: exhibitors_banquetteattendant_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_banquetteattendant_d33742b2 ON public.banquet_banquetteattendant USING btree (exhibitor_id);


--
-- Name: exhibitors_banquetteattendant_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_banquetteattendant_df5a2d4b ON public.banquet_banquetteattendant USING btree (fair_id);


--
-- Name: exhibitors_banquetteattendant_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_banquetteattendant_e8701ad4 ON public.banquet_banquetteattendant USING btree (user_id);


--
-- Name: exhibitors_cataloginfo_8fafcd66; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_8fafcd66 ON public.exhibitors_cataloginfo USING btree (main_work_field_id);


--
-- Name: exhibitors_cataloginfo_continents_071e6d87; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_continents_071e6d87 ON public.exhibitors_cataloginfo_continents USING btree (continent_id);


--
-- Name: exhibitors_cataloginfo_continents_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_continents_7b0bb61e ON public.exhibitors_cataloginfo_continents USING btree (cataloginfo_id);


--
-- Name: exhibitors_cataloginfo_job_types_3fde09dd; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_job_types_3fde09dd ON public.exhibitors_cataloginfo_job_types USING btree (jobtype_id);


--
-- Name: exhibitors_cataloginfo_job_types_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_job_types_7b0bb61e ON public.exhibitors_cataloginfo_job_types USING btree (cataloginfo_id);


--
-- Name: exhibitors_cataloginfo_programs_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_programs_7b0bb61e ON public.exhibitors_cataloginfo_programs USING btree (cataloginfo_id);


--
-- Name: exhibitors_cataloginfo_programs_82558bcc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_programs_82558bcc ON public.exhibitors_cataloginfo_programs USING btree (programme_id);


--
-- Name: exhibitors_cataloginfo_tags_76f094bc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_tags_76f094bc ON public.exhibitors_cataloginfo_tags USING btree (tag_id);


--
-- Name: exhibitors_cataloginfo_tags_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_tags_7b0bb61e ON public.exhibitors_cataloginfo_tags USING btree (cataloginfo_id);


--
-- Name: exhibitors_cataloginfo_values_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_values_7b0bb61e ON public.exhibitors_cataloginfo_values USING btree (cataloginfo_id);


--
-- Name: exhibitors_cataloginfo_values_b0304493; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_values_b0304493 ON public.exhibitors_cataloginfo_values USING btree (value_id);


--
-- Name: exhibitors_cataloginfo_work_fields_78a3ad45; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_work_fields_78a3ad45 ON public.exhibitors_cataloginfo_work_fields USING btree (workfield_id);


--
-- Name: exhibitors_cataloginfo_work_fields_7b0bb61e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_cataloginfo_work_fields_7b0bb61e ON public.exhibitors_cataloginfo_work_fields USING btree (cataloginfo_id);


--
-- Name: exhibitors_exhibitor_447d3092; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_447d3092 ON public.exhibitors_exhibitor USING btree (company_id);


--
-- Name: exhibitors_exhibitor_6d82f13d; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_6d82f13d ON public.exhibitors_exhibitor USING btree (contact_id);


--
-- Name: exhibitors_exhibitor_delivery_order_id_e88ea52b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_delivery_order_id_e88ea52b ON public.exhibitors_exhibitor USING btree (delivery_order_id);


--
-- Name: exhibitors_exhibitor_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_df5a2d4b ON public.exhibitors_exhibitor USING btree (fair_id);


--
-- Name: exhibitors_exhibitor_e274a5da; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_e274a5da ON public.exhibitors_exhibitor USING btree (location_id);


--
-- Name: exhibitors_exhibitor_hosts_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_hosts_d33742b2 ON public.exhibitors_exhibitor_hosts USING btree (exhibitor_id);


--
-- Name: exhibitors_exhibitor_hosts_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_hosts_e8701ad4 ON public.exhibitors_exhibitor_hosts USING btree (user_id);


--
-- Name: exhibitors_exhibitor_inbound_transportation_id_35d43cef; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_inbound_transportation_id_35d43cef ON public.exhibitors_exhibitor USING btree (inbound_transportation_id);


--
-- Name: exhibitors_exhibitor_invoice_details_id_2bd4a77e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_invoice_details_id_2bd4a77e ON public.exhibitors_exhibitor USING btree (invoice_details_id);


--
-- Name: exhibitors_exhibitor_job_types_3fde09dd; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_job_types_3fde09dd ON public.exhibitors_exhibitor_job_types USING btree (jobtype_id);


--
-- Name: exhibitors_exhibitor_job_types_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_job_types_d33742b2 ON public.exhibitors_exhibitor_job_types USING btree (exhibitor_id);


--
-- Name: exhibitors_exhibitor_outbound_transportation_id_fb7765eb; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_outbound_transportation_id_fb7765eb ON public.exhibitors_exhibitor USING btree (outbound_transportation_id);


--
-- Name: exhibitors_exhibitor_pickup_order_id_4f4ac707; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_pickup_order_id_4f4ac707 ON public.exhibitors_exhibitor USING btree (pickup_order_id);


--
-- Name: exhibitors_exhibitor_tags_76f094bc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_tags_76f094bc ON public.exhibitors_exhibitor_tags USING btree (tag_id);


--
-- Name: exhibitors_exhibitor_tags_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitor_tags_d33742b2 ON public.exhibitors_exhibitor_tags USING btree (exhibitor_id);


--
-- Name: exhibitors_exhibitorview_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX exhibitors_exhibitorview_e8701ad4 ON public.exhibitors_exhibitorview USING btree (user_id);


--
-- Name: fair_partner_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX fair_partner_df5a2d4b ON public.fair_partner USING btree (fair_id);


--
-- Name: locations_location_room_id_6a63e06f_uniq; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX locations_location_room_id_6a63e06f_uniq ON public.locations_location USING btree (room_id);


--
-- Name: locations_room_4c63c6ae; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX locations_room_4c63c6ae ON public.locations_room USING btree (building_id);


--
-- Name: matching_answer_7aa0f6ee; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_answer_7aa0f6ee ON public.matching_answer USING btree (question_id);


--
-- Name: matching_answer_e122f817; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_answer_e122f817 ON public.matching_answer USING btree (response_id);


--
-- Name: matching_answer_polymorphic_ctype_id_69638c96; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_answer_polymorphic_ctype_id_69638c96 ON public.matching_answer USING btree (polymorphic_ctype_id);


--
-- Name: matching_category_survey_id_71bdc096; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_category_survey_id_71bdc096 ON public.matching_category USING btree (survey_id);


--
-- Name: matching_continent_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_continent_00b3bd7e ON public.matching_continent USING btree (survey_id);


--
-- Name: matching_continent_continent_ee83ca7d_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_continent_continent_ee83ca7d_like ON public.matching_continent USING btree (name text_pattern_ops);


--
-- Name: matching_country_071e6d87; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_country_071e6d87 ON public.matching_country USING btree (continent_id);


--
-- Name: matching_country_exhibitor_93bfec8a; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_country_exhibitor_93bfec8a ON public.matching_country_exhibitor USING btree (country_id);


--
-- Name: matching_country_exhibitor_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_country_exhibitor_d33742b2 ON public.matching_country_exhibitor USING btree (exhibitor_id);


--
-- Name: matching_country_name_1e397f76_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_country_name_1e397f76_like ON public.matching_country USING btree (name text_pattern_ops);


--
-- Name: matching_jobtype_b62a43bf; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_jobtype_b62a43bf ON public.matching_jobtype USING btree (exhibitor_question_id);


--
-- Name: matching_question_category_id_888854fb; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_question_category_id_888854fb ON public.matching_question USING btree (category_id);


--
-- Name: matching_question_survey_id_0a6cafbc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_question_survey_id_0a6cafbc ON public.matching_question USING btree (survey_id);


--
-- Name: matching_response_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_response_00b3bd7e ON public.matching_response USING btree (survey_id);


--
-- Name: matching_response_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_response_d33742b2 ON public.matching_response USING btree (exhibitor_id);


--
-- Name: matching_studentanswerbase_30a811f6; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerbase_30a811f6 ON public.matching_studentanswerbase USING btree (student_id);


--
-- Name: matching_studentanswerbase_survey_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerbase_survey_00b3bd7e ON public.matching_studentanswerbase_survey USING btree (survey_id);


--
-- Name: matching_studentanswerbase_survey_0fc2a17f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerbase_survey_0fc2a17f ON public.matching_studentanswerbase_survey USING btree (studentanswerbase_id);


--
-- Name: matching_studentanswercontinent_071e6d87; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswercontinent_071e6d87 ON public.matching_studentanswercontinent USING btree (continent_id);


--
-- Name: matching_studentanswergrading_7aa0f6ee; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswergrading_7aa0f6ee ON public.matching_studentanswergrading USING btree (question_id);


--
-- Name: matching_studentanswerjobtype_d1803079; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerjobtype_d1803079 ON public.matching_studentanswerjobtype USING btree (job_type_id);


--
-- Name: matching_studentanswerregion_0f442f96; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerregion_0f442f96 ON public.matching_studentanswerregion USING btree (region_id);


--
-- Name: matching_studentanswerslider_7aa0f6ee; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerslider_7aa0f6ee ON public.matching_studentanswerslider USING btree (question_id);


--
-- Name: matching_studentanswerworkfield_d52c60f4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentanswerworkfield_d52c60f4 ON public.matching_studentanswerworkfield USING btree (work_field_id);


--
-- Name: matching_studentquestionbase_f70f553c; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentquestionbase_f70f553c ON public.matching_studentquestionbase USING btree (company_question_id);


--
-- Name: matching_studentquestionbase_survey_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentquestionbase_survey_00b3bd7e ON public.matching_studentquestionbase_survey USING btree (survey_id);


--
-- Name: matching_studentquestionbase_survey_4a0ef7e0; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_studentquestionbase_survey_4a0ef7e0 ON public.matching_studentquestionbase_survey USING btree (studentquestionbase_id);


--
-- Name: matching_survey_af0c028a; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_survey_af0c028a ON public.matching_survey USING btree (relates_to_id);


--
-- Name: matching_survey_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_survey_df5a2d4b ON public.matching_survey USING btree (fair_id);


--
-- Name: matching_swedencities_0f442f96; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_swedencities_0f442f96 ON public.matching_swedencity USING btree (region_id);


--
-- Name: matching_swedencities_city_78e54839_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_swedencities_city_78e54839_like ON public.matching_swedencity USING btree (city text_pattern_ops);


--
-- Name: matching_swedencities_exhibitor_aa6645b5; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_swedencities_exhibitor_aa6645b5 ON public.matching_swedencity_exhibitor USING btree (swedencity_id);


--
-- Name: matching_swedencities_exhibitor_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_swedencities_exhibitor_d33742b2 ON public.matching_swedencity_exhibitor USING btree (exhibitor_id);


--
-- Name: matching_swedenregion_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_swedenregion_00b3bd7e ON public.matching_swedenregion USING btree (survey_id);


--
-- Name: matching_workfield_a99fe235; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_workfield_a99fe235 ON public.matching_workfield USING btree (work_area_id);


--
-- Name: matching_workfield_survey_00b3bd7e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_workfield_survey_00b3bd7e ON public.matching_workfield_survey USING btree (survey_id);


--
-- Name: matching_workfield_survey_78a3ad45; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_workfield_survey_78a3ad45 ON public.matching_workfield_survey USING btree (workfield_id);


--
-- Name: matching_workfield_work_field_2b046ccb_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_workfield_work_field_2b046ccb_like ON public.matching_workfield USING btree (work_field text_pattern_ops);


--
-- Name: matching_workfieldarea_work_area_ae8a7ff2_like; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX matching_workfieldarea_work_area_ae8a7ff2_like ON public.matching_workfieldarea USING btree (work_area text_pattern_ops);


--
-- Name: orders_electricityorder_exhibitor_id_28286d6b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX orders_electricityorder_exhibitor_id_28286d6b ON public.orders_electricityorder USING btree (exhibitor_id);


--
-- Name: orders_order_9bea82de; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX orders_order_9bea82de ON public.orders_order USING btree (product_id);


--
-- Name: orders_order_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX orders_order_d33742b2 ON public.orders_order USING btree (exhibitor_id);


--
-- Name: orders_product_d9862cd8; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX orders_product_d9862cd8 ON public.orders_product USING btree (product_type_id);


--
-- Name: orders_product_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX orders_product_df5a2d4b ON public.orders_product USING btree (fair_id);


--
-- Name: profile_programme_id_467b0fd7_uniq; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX profile_programme_id_467b0fd7_uniq ON public.profile USING btree (programme_id);


--
-- Name: recruitment_customfield_25868659; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_customfield_25868659 ON public.recruitment_customfield USING btree (extra_field_id);


--
-- Name: recruitment_customfieldanswer_a16ec6d0; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_customfieldanswer_a16ec6d0 ON public.recruitment_customfieldanswer USING btree (custom_field_id);


--
-- Name: recruitment_customfieldanswer_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_customfieldanswer_e8701ad4 ON public.recruitment_customfieldanswer USING btree (user_id);


--
-- Name: recruitment_customfieldargument_a16ec6d0; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_customfieldargument_a16ec6d0 ON public.recruitment_customfieldargument USING btree (custom_field_id);


--
-- Name: recruitment_recruitmentapplication_16067579; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_16067579 ON public.recruitment_recruitmentapplication USING btree (superior_user_id);


--
-- Name: recruitment_recruitmentapplication_5babbd82; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_5babbd82 ON public.recruitment_recruitmentapplication USING btree (recommended_role_id);


--
-- Name: recruitment_recruitmentapplication_bfe4cfac; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_bfe4cfac ON public.recruitment_recruitmentapplication USING btree (recruitment_period_id);


--
-- Name: recruitment_recruitmentapplication_cb0f7719; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_cb0f7719 ON public.recruitment_recruitmentapplication USING btree (interviewer_id);


--
-- Name: recruitment_recruitmentapplication_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_d33742b2 ON public.recruitment_recruitmentapplication USING btree (exhibitor_id);


--
-- Name: recruitment_recruitmentapplication_e72b116e; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_e72b116e ON public.recruitment_recruitmentapplication USING btree (delegated_role_id);


--
-- Name: recruitment_recruitmentapplication_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_e8701ad4 ON public.recruitment_recruitmentapplication USING btree (user_id);


--
-- Name: recruitment_recruitmentapplication_interviewer2_id_273dcc8d; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplication_interviewer2_id_273dcc8d ON public.recruitment_recruitmentapplication USING btree (interviewer2_id);


--
-- Name: recruitment_recruitmentapplicationcomment_c522f5e9; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplicationcomment_c522f5e9 ON public.recruitment_recruitmentapplicationcomment USING btree (recruitment_application_id);


--
-- Name: recruitment_recruitmentapplicationcomment_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentapplicationcomment_e8701ad4 ON public.recruitment_recruitmentapplicationcomment USING btree (user_id);


--
-- Name: recruitment_recruitmentperiod_0f55de3f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentperiod_0f55de3f ON public.recruitment_recruitmentperiod USING btree (interview_questions_id);


--
-- Name: recruitment_recruitmentperiod_d8eccb61; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentperiod_d8eccb61 ON public.recruitment_recruitmentperiod USING btree (application_questions_id);


--
-- Name: recruitment_recruitmentperiod_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentperiod_df5a2d4b ON public.recruitment_recruitmentperiod USING btree (fair_id);


--
-- Name: recruitment_recruitmentperiod_recruitable_roles_2b1e4c5a; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentperiod_recruitable_roles_2b1e4c5a ON public.recruitment_recruitmentperiod_recruitable_roles USING btree (recruitmentperiod_id);


--
-- Name: recruitment_recruitmentperiod_recruitable_roles_84566833; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_recruitmentperiod_recruitable_roles_84566833 ON public.recruitment_recruitmentperiod_recruitable_roles USING btree (role_id);


--
-- Name: recruitment_role_0e939a4f; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_role_0e939a4f ON public.recruitment_role USING btree (group_id);


--
-- Name: recruitment_role_d75d21fc; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_role_d75d21fc ON public.recruitment_role USING btree (parent_role_id);


--
-- Name: recruitment_roleapplication_84566833; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_roleapplication_84566833 ON public.recruitment_roleapplication USING btree (role_id);


--
-- Name: recruitment_roleapplication_c522f5e9; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX recruitment_roleapplication_c522f5e9 ON public.recruitment_roleapplication USING btree (recruitment_application_id);


--
-- Name: register_orderlog_447d3092; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_orderlog_447d3092 ON public.register_orderlog USING btree (company_id);


--
-- Name: register_orderlog_6d82f13d; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_orderlog_6d82f13d ON public.register_orderlog USING btree (contact_id);


--
-- Name: register_orderlog_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_orderlog_df5a2d4b ON public.register_orderlog USING btree (fair_id);


--
-- Name: register_signupcontract_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_signupcontract_df5a2d4b ON public.register_signupcontract USING btree (fair_id);


--
-- Name: register_signuplog_447d3092; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_signuplog_447d3092 ON public.register_signuplog USING btree (company_id);


--
-- Name: register_signuplog_567128e5; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_signuplog_567128e5 ON public.register_signuplog USING btree (contract_id);


--
-- Name: register_signuplog_6d82f13d; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX register_signuplog_6d82f13d ON public.register_signuplog USING btree (contact_id);


--
-- Name: sales_followup_2506e0ba; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_followup_2506e0ba ON public.sales_followup USING btree (sale_id);


--
-- Name: sales_sale_447d3092; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_sale_447d3092 ON public.sales_sale USING btree (company_id);


--
-- Name: sales_sale_4c66c5b6; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_sale_4c66c5b6 ON public.sales_sale USING btree (responsible_id);


--
-- Name: sales_sale_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_sale_df5a2d4b ON public.sales_sale USING btree (fair_id);


--
-- Name: sales_salecomment_2506e0ba; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_salecomment_2506e0ba ON public.sales_salecomment USING btree (sale_id);


--
-- Name: sales_salecomment_e8701ad4; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX sales_salecomment_e8701ad4 ON public.sales_salecomment USING btree (user_id);


--
-- Name: student_profiles_matchingresult_30a811f6; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX student_profiles_matchingresult_30a811f6 ON public.student_profiles_matchingresult USING btree (student_id);


--
-- Name: student_profiles_matchingresult_d33742b2; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX student_profiles_matchingresult_d33742b2 ON public.student_profiles_matchingresult USING btree (exhibitor_id);


--
-- Name: student_profiles_matchingresult_df5a2d4b; Type: INDEX; Schema: public; Owner: ais; Tablespace: 
--

CREATE INDEX student_profiles_matchingresult_df5a2d4b ON public.student_profiles_matchingresult USING btree (fair_id);


--
-- Name: D047a05b9185e584991cceccb1322fb4; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerregion
    ADD CONSTRAINT "D047a05b9185e584991cceccb1322fb4" FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D05971a65c231060b0621e65ad794428; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT "D05971a65c231060b0621e65ad794428" FOREIGN KEY (recruitment_period_id) REFERENCES public.recruitment_recruitmentperiod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D1e9fb33fe4cd9e7d135313b68975127; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerjobtype
    ADD CONSTRAINT "D1e9fb33fe4cd9e7d135313b68975127" FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D253f06965684b678cc76f3bf8609633; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswergrading
    ADD CONSTRAINT "D253f06965684b678cc76f3bf8609633" FOREIGN KEY (question_id) REFERENCES public.matching_studentquestiongrading(studentquestionbase_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D435d3cf0ef8d4674a27c15a5e730b5b; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerslider
    ADD CONSTRAINT "D435d3cf0ef8d4674a27c15a5e730b5b" FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D4a0f3f35426794d3cdb2b7781e66cf3; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerworkfield
    ADD CONSTRAINT "D4a0f3f35426794d3cdb2b7781e66cf3" FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D720fcb46f4c51933a327a61fd6dd293; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswergrading
    ADD CONSTRAINT "D720fcb46f4c51933a327a61fd6dd293" FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D83b388b74508f6be21708b901883384; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerslider
    ADD CONSTRAINT "D83b388b74508f6be21708b901883384" FOREIGN KEY (question_id) REFERENCES public.matching_studentquestionslider(studentquestionbase_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D8a7b3d8f26d2d0fe50caec6a8daba2f; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionslider
    ADD CONSTRAINT "D8a7b3d8f26d2d0fe50caec6a8daba2f" FOREIGN KEY (studentquestionbase_ptr_id) REFERENCES public.matching_studentquestionbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: a6c55549304cafa8a2530cbaf9522673; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestiongrading
    ADD CONSTRAINT a6c55549304cafa8a2530cbaf9522673 FOREIGN KEY (studentquestionbase_ptr_id) REFERENCES public.matching_studentquestionbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: application_questions_id_9a26254d_fk_recruitment_extrafield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod
    ADD CONSTRAINT application_questions_id_9a26254d_fk_recruitment_extrafield_id FOREIGN KEY (application_questions_id) REFERENCES public.recruitment_extrafield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: banquet_banquett_ticket_id_eae60723_fk_banquet_banquetticket_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT banquet_banquett_ticket_id_eae60723_fk_banquet_banquetticket_id FOREIGN KEY (ticket_id) REFERENCES public.banquet_banquetticket(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: banquet_banquettable_fair_id_f88d2d33_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquettable
    ADD CONSTRAINT banquet_banquettable_fair_id_f88d2d33_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: banquet_banquettea_table_id_6614fb4c_fk_banquet_banquettable_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT banquet_banquettea_table_id_6614fb4c_fk_banquet_banquettable_id FOREIGN KEY (table_id) REFERENCES public.banquet_banquettable(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cd66968569f1874aef1f3d804ddfe8df; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_roleapplication
    ADD CONSTRAINT cd66968569f1874aef1f3d804ddfe8df FOREIGN KEY (recruitment_application_id) REFERENCES public.recruitment_recruitmentapplication(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company__programme_id_137f85bb_fk_people_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_company_related_programme
    ADD CONSTRAINT companies_company__programme_id_137f85bb_fk_people_programme_id FOREIGN KEY (programme_id) REFERENCES public.people_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company_r_company_id_36969173_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_company_related_programme
    ADD CONSTRAINT companies_company_r_company_id_36969173_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_contac_belongs_to_id_96282225_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_contact
    ADD CONSTRAINT companies_contac_belongs_to_id_96282225_fk_companies_company_id FOREIGN KEY (belongs_to_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_contact_user_id_abef7e06_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_contact
    ADD CONSTRAINT companies_contact_user_id_abef7e06_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_invoicedet_company_id_372c7b1a_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.companies_invoicedetails
    ADD CONSTRAINT companies_invoicedet_company_id_372c7b1a_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: d2a5a2425cc644cced73b1f0054d5af5; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionbase_survey
    ADD CONSTRAINT d2a5a2425cc644cced73b1f0054d5af5 FOREIGN KEY (studentquestionbase_id) REFERENCES public.matching_studentquestionbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: daa8740e731bfe43c906483600b87db5; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswercontinent
    ADD CONSTRAINT daa8740e731bfe43c906483600b87db5 FOREIGN KEY (studentanswerbase_ptr_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ea4da3cdc3ba4900804d709aa3d7bd28; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplicationcomment
    ADD CONSTRAINT ea4da3cdc3ba4900804d709aa3d7bd28 FOREIGN KEY (recruitment_application_id) REFERENCES public.recruitment_recruitmentapplication(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_eve_extra_field_id_89c43469_fk_recruitment_extrafield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_eve_extra_field_id_89c43469_fk_recruitment_extrafield_id FOREIGN KEY (extra_field_id) REFERENCES public.recruitment_extrafield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_even_attendence_id_36e1930d_fk_events_eventattendence_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventanswer
    ADD CONSTRAINT events_even_attendence_id_36e1930d_fk_events_eventattendence_id FOREIGN KEY (attendence_id) REFERENCES public.events_eventattendence(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_allowed_group_event_id_76618db0_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_allowed_groups
    ADD CONSTRAINT events_event_allowed_group_event_id_76618db0_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_allowed_groups_group_id_7e945367_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_allowed_groups
    ADD CONSTRAINT events_event_allowed_groups_group_id_7e945367_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_fair_id_6d79fc55_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_fair_id_6d79fc55_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_tags_event_id_dbac01f5_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_tags
    ADD CONSTRAINT events_event_tags_event_id_dbac01f5_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_tags_tag_id_e0e734aa_fk_fair_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_event_tags
    ADD CONSTRAINT events_event_tags_tag_id_e0e734aa_fk_fair_tag_id FOREIGN KEY (tag_id) REFERENCES public.fair_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_eventans_question_id_d0421429_fk_events_eventquestion_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventanswer
    ADD CONSTRAINT events_eventans_question_id_d0421429_fk_events_eventquestion_id FOREIGN KEY (question_id) REFERENCES public.events_eventquestion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_eventattendence_event_id_09e624bf_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventattendence
    ADD CONSTRAINT events_eventattendence_event_id_09e624bf_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_eventattendence_user_id_a2d9a27f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventattendence
    ADD CONSTRAINT events_eventattendence_user_id_a2d9a27f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_eventquestion_event_id_03be7de8_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.events_eventquestion
    ADD CONSTRAINT events_eventquestion_event_id_03be7de8_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibito_main_work_field_id_f2dd40b4_fk_exhibitors_workfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo
    ADD CONSTRAINT exhibito_main_work_field_id_f2dd40b4_fk_exhibitors_workfield_id FOREIGN KEY (main_work_field_id) REFERENCES public.exhibitors_workfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_ban_exhibitor_id_f80193e1_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT exhibitors_ban_exhibitor_id_f80193e1_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_banquetteattendant_fair_id_e78ec06e_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT exhibitors_banquetteattendant_fair_id_e78ec06e_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_banquetteattendant_user_id_25123a77_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.banquet_banquetteattendant
    ADD CONSTRAINT exhibitors_banquetteattendant_user_id_25123a77_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cat_continent_id_9050835e_fk_exhibitors_continent_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_continents
    ADD CONSTRAINT exhibitors_cat_continent_id_9050835e_fk_exhibitors_continent_id FOREIGN KEY (continent_id) REFERENCES public.exhibitors_continent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cat_exhibitor_id_57337e2a_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo
    ADD CONSTRAINT exhibitors_cat_exhibitor_id_57337e2a_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cat_workfield_id_ec62e993_fk_exhibitors_workfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_work_fields
    ADD CONSTRAINT exhibitors_cat_workfield_id_ec62e993_fk_exhibitors_workfield_id FOREIGN KEY (workfield_id) REFERENCES public.exhibitors_workfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_catalog_jobtype_id_3e73354d_fk_exhibitors_jobtype_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_job_types
    ADD CONSTRAINT exhibitors_catalog_jobtype_id_3e73354d_fk_exhibitors_jobtype_id FOREIGN KEY (jobtype_id) REFERENCES public.exhibitors_jobtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_catalog_programme_id_9fbf729c_fk_people_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_programs
    ADD CONSTRAINT exhibitors_catalog_programme_id_9fbf729c_fk_people_programme_id FOREIGN KEY (programme_id) REFERENCES public.people_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_28bc18d1_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_tags
    ADD CONSTRAINT exhibitors_cataloginfo_id_28bc18d1_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_59c8ba45_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_values
    ADD CONSTRAINT exhibitors_cataloginfo_id_59c8ba45_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_6866d8d0_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_job_types
    ADD CONSTRAINT exhibitors_cataloginfo_id_6866d8d0_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_a3984f63_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_work_fields
    ADD CONSTRAINT exhibitors_cataloginfo_id_a3984f63_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_a5e0b912_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_continents
    ADD CONSTRAINT exhibitors_cataloginfo_id_a5e0b912_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_id_e5c83694_fk_exhibitors_cataloginfo_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_programs
    ADD CONSTRAINT exhibitors_cataloginfo_id_e5c83694_fk_exhibitors_cataloginfo_id FOREIGN KEY (cataloginfo_id) REFERENCES public.exhibitors_cataloginfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_tags_tag_id_c81b5519_fk_fair_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_tags
    ADD CONSTRAINT exhibitors_cataloginfo_tags_tag_id_c81b5519_fk_fair_tag_id FOREIGN KEY (tag_id) REFERENCES public.fair_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_cataloginfo_value_id_72a4e66e_fk_exhibitors_value_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_cataloginfo_values
    ADD CONSTRAINT exhibitors_cataloginfo_value_id_72a4e66e_fk_exhibitors_value_id FOREIGN KEY (value_id) REFERENCES public.exhibitors_value(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_e_fair_location_id_429c9f61_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_e_fair_location_id_429c9f61_fk_locations_location_id FOREIGN KEY (fair_location_id) REFERENCES public.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exh_exhibitor_id_013ae8a1_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_tags
    ADD CONSTRAINT exhibitors_exh_exhibitor_id_013ae8a1_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exh_exhibitor_id_d93cd31b_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_hosts
    ADD CONSTRAINT exhibitors_exh_exhibitor_id_d93cd31b_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exh_exhibitor_id_e258d381_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_job_types
    ADD CONSTRAINT exhibitors_exh_exhibitor_id_e258d381_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhib_location_id_dfcb3004_fk_exhibitors_location_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhib_location_id_dfcb3004_fk_exhibitors_location_id FOREIGN KEY (location_id) REFERENCES public.exhibitors_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibit_jobtype_id_ea3a9750_fk_exhibitors_jobtype_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_job_types
    ADD CONSTRAINT exhibitors_exhibit_jobtype_id_ea3a9750_fk_exhibitors_jobtype_id FOREIGN KEY (jobtype_id) REFERENCES public.exhibitors_jobtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibito_company_id_ca7b2be7_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibito_company_id_ca7b2be7_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibito_contact_id_bd4e0b15_fk_companies_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibito_contact_id_bd4e0b15_fk_companies_contact_id FOREIGN KEY (contact_id) REFERENCES public.companies_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_delivery_order_id_e88ea52b_fk_transport; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_delivery_order_id_e88ea52b_fk_transport FOREIGN KEY (delivery_order_id) REFERENCES public.transportation_transportationorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_fair_id_f2353bf5_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_fair_id_f2353bf5_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_hosts_user_id_94655829_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_hosts
    ADD CONSTRAINT exhibitors_exhibitor_hosts_user_id_94655829_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_inbound_transportati_35d43cef_fk_exhibitor; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_inbound_transportati_35d43cef_fk_exhibitor FOREIGN KEY (inbound_transportation_id) REFERENCES public.exhibitors_transportationalternative(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_invoice_details_id_2bd4a77e_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_invoice_details_id_2bd4a77e_fk_companies FOREIGN KEY (invoice_details_id) REFERENCES public.companies_invoicedetails(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_outbound_transportat_fb7765eb_fk_exhibitor; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_outbound_transportat_fb7765eb_fk_exhibitor FOREIGN KEY (outbound_transportation_id) REFERENCES public.exhibitors_transportationalternative(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_pickup_order_id_4f4ac707_fk_transport; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor
    ADD CONSTRAINT exhibitors_exhibitor_pickup_order_id_4f4ac707_fk_transport FOREIGN KEY (pickup_order_id) REFERENCES public.transportation_transportationorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitor_tags_tag_id_105b7b3a_fk_fair_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitor_tags
    ADD CONSTRAINT exhibitors_exhibitor_tags_tag_id_105b7b3a_fk_fair_tag_id FOREIGN KEY (tag_id) REFERENCES public.fair_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exhibitors_exhibitorview_user_id_eaee166e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.exhibitors_exhibitorview
    ADD CONSTRAINT exhibitors_exhibitorview_user_id_eaee166e_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: f99d425ff23407b80289638200ef506d; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod_recruitable_roles
    ADD CONSTRAINT f99d425ff23407b80289638200ef506d FOREIGN KEY (recruitmentperiod_id) REFERENCES public.recruitment_recruitmentperiod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fair_partner_fair_id_89ac5da1_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.fair_partner
    ADD CONSTRAINT fair_partner_fair_id_89ac5da1_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location_room_id_6a63e06f_fk_locations_room_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.locations_location
    ADD CONSTRAINT locations_location_room_id_6a63e06f_fk_locations_room_id FOREIGN KEY (room_id) REFERENCES public.locations_room(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_room_building_id_c1b2fd77_fk_locations_building_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.locations_room
    ADD CONSTRAINT locations_room_building_id_c1b2fd77_fk_locations_building_id FOREIGN KEY (building_id) REFERENCES public.locations_building(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_answer_polymorphic_ctype_id_69638c96_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_answer
    ADD CONSTRAINT matching_answer_polymorphic_ctype_id_69638c96_fk_django_co FOREIGN KEY (polymorphic_ctype_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_answer_question_id_e40503d7_fk_matching_question_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_answer
    ADD CONSTRAINT matching_answer_question_id_e40503d7_fk_matching_question_id FOREIGN KEY (question_id) REFERENCES public.matching_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_answer_response_id_56e3ed23_fk_matching_response_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_answer
    ADD CONSTRAINT matching_answer_response_id_56e3ed23_fk_matching_response_id FOREIGN KEY (response_id) REFERENCES public.matching_response(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_booleanan_answer_ptr_id_642295c6_fk_matching_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_booleanans
    ADD CONSTRAINT matching_booleanan_answer_ptr_id_642295c6_fk_matching_answer_id FOREIGN KEY (answer_ptr_id) REFERENCES public.matching_answer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_category_survey_id_71bdc096_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_category
    ADD CONSTRAINT matching_category_survey_id_71bdc096_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_choiceans_answer_ptr_id_473e57e6_fk_matching_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_choiceans
    ADD CONSTRAINT matching_choiceans_answer_ptr_id_473e57e6_fk_matching_answer_id FOREIGN KEY (answer_ptr_id) REFERENCES public.matching_answer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_continent_survey_id_b2bee442_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_continent
    ADD CONSTRAINT matching_continent_survey_id_b2bee442_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_count_exhibitor_id_9b2136d6_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_country_exhibitor
    ADD CONSTRAINT matching_count_exhibitor_id_9b2136d6_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_country_continent_id_53d3d406_fk_matching_continent_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_country
    ADD CONSTRAINT matching_country_continent_id_53d3d406_fk_matching_continent_id FOREIGN KEY (continent_id) REFERENCES public.matching_continent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_country_exh_country_id_178c470e_fk_matching_country_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_country_exhibitor
    ADD CONSTRAINT matching_country_exh_country_id_178c470e_fk_matching_country_id FOREIGN KEY (country_id) REFERENCES public.matching_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_exhibitor_question_id_998c84e9_fk_matching_question_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_jobtype
    ADD CONSTRAINT matching_exhibitor_question_id_998c84e9_fk_matching_question_id FOREIGN KEY (exhibitor_question_id) REFERENCES public.matching_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_integeran_answer_ptr_id_1c3e8a1f_fk_matching_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_integerans
    ADD CONSTRAINT matching_integeran_answer_ptr_id_1c3e8a1f_fk_matching_answer_id FOREIGN KEY (answer_ptr_id) REFERENCES public.matching_answer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_question_category_id_888854fb_fk_matching_category_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_question
    ADD CONSTRAINT matching_question_category_id_888854fb_fk_matching_category_id FOREIGN KEY (category_id) REFERENCES public.matching_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_question_survey_id_0a6cafbc_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_question
    ADD CONSTRAINT matching_question_survey_id_0a6cafbc_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_respo_exhibitor_id_07578fec_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_response
    ADD CONSTRAINT matching_respo_exhibitor_id_07578fec_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_response_survey_id_b5284f97_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_response
    ADD CONSTRAINT matching_response_survey_id_b5284f97_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_s_company_question_id_90a3dea4_fk_matching_question_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionbase
    ADD CONSTRAINT matching_s_company_question_id_90a3dea4_fk_matching_question_id FOREIGN KEY (company_question_id) REFERENCES public.matching_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_studen_work_field_id_c9c34bba_fk_matching_workfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerworkfield
    ADD CONSTRAINT matching_studen_work_field_id_c9c34bba_fk_matching_workfield_id FOREIGN KEY (work_field_id) REFERENCES public.matching_workfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_student_continent_id_bab90ff1_fk_matching_continent_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswercontinent
    ADD CONSTRAINT matching_student_continent_id_bab90ff1_fk_matching_continent_id FOREIGN KEY (continent_id) REFERENCES public.matching_continent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_student_region_id_d40ccc26_fk_matching_swedenregion_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerregion
    ADD CONSTRAINT matching_student_region_id_d40ccc26_fk_matching_swedenregion_id FOREIGN KEY (region_id) REFERENCES public.matching_swedenregion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_studentans_job_type_id_bac7d265_fk_matching_jobtype_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerjobtype
    ADD CONSTRAINT matching_studentans_job_type_id_bac7d265_fk_matching_jobtype_id FOREIGN KEY (job_type_id) REFERENCES public.matching_jobtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_studentanswer_survey_id_d5381434_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerbase_survey
    ADD CONSTRAINT matching_studentanswer_survey_id_d5381434_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_studentquesti_survey_id_0fbb0954_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentquestionbase_survey
    ADD CONSTRAINT matching_studentquesti_survey_id_0fbb0954_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_survey_fair_id_9eabc18a_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_survey
    ADD CONSTRAINT matching_survey_fair_id_9eabc18a_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_survey_relates_to_id_086e980d_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_survey
    ADD CONSTRAINT matching_survey_relates_to_id_086e980d_fk_matching_survey_id FOREIGN KEY (relates_to_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_swede_exhibitor_id_2fa6d8f5_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedencity_exhibitor
    ADD CONSTRAINT matching_swede_exhibitor_id_2fa6d8f5_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_swede_swedencity_id_2c42caeb_fk_matching_swedencity_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedencity_exhibitor
    ADD CONSTRAINT matching_swede_swedencity_id_2c42caeb_fk_matching_swedencity_id FOREIGN KEY (swedencity_id) REFERENCES public.matching_swedencity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_swedenc_region_id_275bb2f1_fk_matching_swedenregion_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedencity
    ADD CONSTRAINT matching_swedenc_region_id_275bb2f1_fk_matching_swedenregion_id FOREIGN KEY (region_id) REFERENCES public.matching_swedenregion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_swedenregion_survey_id_bc935c78_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_swedenregion
    ADD CONSTRAINT matching_swedenregion_survey_id_bc935c78_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_textans_answer_ptr_id_f9fcd426_fk_matching_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_textans
    ADD CONSTRAINT matching_textans_answer_ptr_id_f9fcd426_fk_matching_answer_id FOREIGN KEY (answer_ptr_id) REFERENCES public.matching_answer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_wor_work_area_id_5a02a53b_fk_matching_workfieldarea_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfield
    ADD CONSTRAINT matching_wor_work_area_id_5a02a53b_fk_matching_workfieldarea_id FOREIGN KEY (work_area_id) REFERENCES public.matching_workfieldarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_workfie_workfield_id_598f29d8_fk_matching_workfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfield_survey
    ADD CONSTRAINT matching_workfie_workfield_id_598f29d8_fk_matching_workfield_id FOREIGN KEY (workfield_id) REFERENCES public.matching_workfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matching_workfield_sur_survey_id_9ad80ee4_fk_matching_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_workfield_survey
    ADD CONSTRAINT matching_workfield_sur_survey_id_9ad80ee4_fk_matching_survey_id FOREIGN KEY (survey_id) REFERENCES public.matching_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_electricityor_exhibitor_id_28286d6b_fk_exhibitor; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_electricityorder
    ADD CONSTRAINT orders_electricityor_exhibitor_id_28286d6b_fk_exhibitor FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order_exhibitor_id_257debbf_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_exhibitor_id_257debbf_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order_product_id_096244de_fk_orders_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_product_id_096244de_fk_orders_product_id FOREIGN KEY (product_id) REFERENCES public.orders_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_produc_product_type_id_c8935e81_fk_orders_producttype_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_product
    ADD CONSTRAINT orders_produc_product_type_id_c8935e81_fk_orders_producttype_id FOREIGN KEY (product_type_id) REFERENCES public.orders_producttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_product_fair_id_0b2cf18a_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_product
    ADD CONSTRAINT orders_product_fair_id_0b2cf18a_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_standarea_product_ptr_id_44fc7afe_fk_orders_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.orders_standarea
    ADD CONSTRAINT orders_standarea_product_ptr_id_44fc7afe_fk_orders_product_id FOREIGN KEY (product_ptr_id) REFERENCES public.orders_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profile_programme_id_467b0fd7_fk_people_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_programme_id_467b0fd7_fk_people_programme_id FOREIGN KEY (programme_id) REFERENCES public.people_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profile_user_id_2aeb6f6b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_user_id_2aeb6f6b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: re_interview_questions_id_c191da66_fk_recruitment_extrafield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod
    ADD CONSTRAINT re_interview_questions_id_c191da66_fk_recruitment_extrafield_id FOREIGN KEY (interview_questions_id) REFERENCES public.recruitment_extrafield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitm_custom_field_id_bcb37f87_fk_recruitment_customfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfieldanswer
    ADD CONSTRAINT recruitm_custom_field_id_bcb37f87_fk_recruitment_customfield_id FOREIGN KEY (custom_field_id) REFERENCES public.recruitment_customfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitm_custom_field_id_f30acd2f_fk_recruitment_customfield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfieldargument
    ADD CONSTRAINT recruitm_custom_field_id_f30acd2f_fk_recruitment_customfield_id FOREIGN KEY (custom_field_id) REFERENCES public.recruitment_customfield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitmen_extra_field_id_5fc1904d_fk_recruitment_extrafield_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfield
    ADD CONSTRAINT recruitmen_extra_field_id_5fc1904d_fk_recruitment_extrafield_id FOREIGN KEY (extra_field_id) REFERENCES public.recruitment_extrafield(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_customfieldanswer_user_id_ad3710d2_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_customfieldanswer
    ADD CONSTRAINT recruitment_customfieldanswer_user_id_ad3710d2_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_r_delegated_role_id_7fd90f03_fk_recruitment_role_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_r_delegated_role_id_7fd90f03_fk_recruitment_role_id FOREIGN KEY (delegated_role_id) REFERENCES public.recruitment_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recommended_role_id_81235d7a_fk_recruitment_role_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recommended_role_id_81235d7a_fk_recruitment_role_id FOREIGN KEY (recommended_role_id) REFERENCES public.recruitment_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recru_exhibitor_id_9767ddf4_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recru_exhibitor_id_9767ddf4_fk_companies_company_id FOREIGN KEY (exhibitor_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitm_interviewer2_id_273dcc8d_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recruitm_interviewer2_id_273dcc8d_fk_auth_user FOREIGN KEY (interviewer2_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitme_superior_user_id_4f8860b1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recruitme_superior_user_id_4f8860b1_fk_auth_user_id FOREIGN KEY (superior_user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitment_interviewer_id_d7cec0cd_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recruitment_interviewer_id_d7cec0cd_fk_auth_user_id FOREIGN KEY (interviewer_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitment_role_id_7763fb40_fk_recruitment_role_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod_recruitable_roles
    ADD CONSTRAINT recruitment_recruitment_role_id_7763fb40_fk_recruitment_role_id FOREIGN KEY (role_id) REFERENCES public.recruitment_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitmentapplica_user_id_0e76df09_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplication
    ADD CONSTRAINT recruitment_recruitmentapplica_user_id_0e76df09_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitmentapplica_user_id_671136cb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentapplicationcomment
    ADD CONSTRAINT recruitment_recruitmentapplica_user_id_671136cb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_recruitmentperiod_fair_id_ff850707_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_recruitmentperiod
    ADD CONSTRAINT recruitment_recruitmentperiod_fair_id_ff850707_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_role_group_id_2481e7f5_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_role
    ADD CONSTRAINT recruitment_role_group_id_2481e7f5_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_role_parent_role_id_12cb2a1b_fk_recruitment_role_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_role
    ADD CONSTRAINT recruitment_role_parent_role_id_12cb2a1b_fk_recruitment_role_id FOREIGN KEY (parent_role_id) REFERENCES public.recruitment_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recruitment_roleapplica_role_id_5f74ae3c_fk_recruitment_role_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.recruitment_roleapplication
    ADD CONSTRAINT recruitment_roleapplica_role_id_5f74ae3c_fk_recruitment_role_id FOREIGN KEY (role_id) REFERENCES public.recruitment_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_orderlog_company_id_4d0a48b7_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_orderlog
    ADD CONSTRAINT register_orderlog_company_id_4d0a48b7_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_orderlog_contact_id_87bc2227_fk_companies_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_orderlog
    ADD CONSTRAINT register_orderlog_contact_id_87bc2227_fk_companies_contact_id FOREIGN KEY (contact_id) REFERENCES public.companies_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_orderlog_fair_id_28ae296e_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_orderlog
    ADD CONSTRAINT register_orderlog_fair_id_28ae296e_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_sig_contract_id_6dbb6974_fk_register_signupcontract_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signuplog
    ADD CONSTRAINT register_sig_contract_id_6dbb6974_fk_register_signupcontract_id FOREIGN KEY (contract_id) REFERENCES public.register_signupcontract(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_signupcontract_fair_id_96329418_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signupcontract
    ADD CONSTRAINT register_signupcontract_fair_id_96329418_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_signuplog_company_id_d503f025_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signuplog
    ADD CONSTRAINT register_signuplog_company_id_d503f025_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_signuplog_contact_id_b4c200f1_fk_companies_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.register_signuplog
    ADD CONSTRAINT register_signuplog_contact_id_b4c200f1_fk_companies_contact_id FOREIGN KEY (contact_id) REFERENCES public.companies_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_followup_sale_id_3c5f769a_fk_sales_sale_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_followup
    ADD CONSTRAINT sales_followup_sale_id_3c5f769a_fk_sales_sale_id FOREIGN KEY (sale_id) REFERENCES public.sales_sale(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_sale_company_id_6e88f52f_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_sale
    ADD CONSTRAINT sales_sale_company_id_6e88f52f_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_sale_fair_id_2185eb15_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_sale
    ADD CONSTRAINT sales_sale_fair_id_2185eb15_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_sale_responsible_id_e57acf5e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_sale
    ADD CONSTRAINT sales_sale_responsible_id_e57acf5e_fk_auth_user_id FOREIGN KEY (responsible_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_salecomment_sale_id_b89b19d9_fk_sales_sale_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_salecomment
    ADD CONSTRAINT sales_salecomment_sale_id_b89b19d9_fk_sales_sale_id FOREIGN KEY (sale_id) REFERENCES public.sales_sale(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sales_salecomment_user_id_1c3c4761_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.sales_salecomment
    ADD CONSTRAINT sales_salecomment_user_id_1c3c4761_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student_profil_exhibitor_id_37144048_fk_exhibitors_exhibitor_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.student_profiles_matchingresult
    ADD CONSTRAINT student_profil_exhibitor_id_37144048_fk_exhibitors_exhibitor_id FOREIGN KEY (exhibitor_id) REFERENCES public.exhibitors_exhibitor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student_profiles_matchingresul_fair_id_a25c495c_fk_fair_fair_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.student_profiles_matchingresult
    ADD CONSTRAINT student_profiles_matchingresul_fair_id_a25c495c_fk_fair_fair_id FOREIGN KEY (fair_id) REFERENCES public.fair_fair(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: studentanswerbase_id_e2ee7578_fk_matching_studentanswerbase_id; Type: FK CONSTRAINT; Schema: public; Owner: ais
--

ALTER TABLE ONLY public.matching_studentanswerbase_survey
    ADD CONSTRAINT studentanswerbase_id_e2ee7578_fk_matching_studentanswerbase_id FOREIGN KEY (studentanswerbase_id) REFERENCES public.matching_studentanswerbase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

