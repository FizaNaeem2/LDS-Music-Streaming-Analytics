-- 1. For Cleanup
DROP TABLE IF EXISTS Fact_Streams;
DROP TABLE IF EXISTS Dim_Track;
DROP TABLE IF EXISTS Dim_Artist;
DROP TABLE IF EXISTS Dim_Time;

-- 2. Dimension Tables

-- Create Dimension Artist
CREATE TABLE Dim_Artist (
    id_artist NVARCHAR(50) PRIMARY KEY,
    name NVARCHAR(255),
    gender NVARCHAR(50),
    birth_place NVARCHAR(255),
    country NVARCHAR(100),
    region NVARCHAR(100),
    h3_index NVARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);

-- 3. Create Dimension Track
CREATE TABLE Dim_Track (
    id_track VARCHAR(50) PRIMARY KEY,    
    title NVARCHAR(400),
    song_category VARCHAR(100),
    featured_artists NVARCHAR(MAX),       -- Can be long lists
    explicit VARCHAR(10),                 
    duration_ms INT,
    bpm FLOAT,
    n_tokens INT,
    language VARCHAR(10),
    n_sentences INT,
    char_per_tok FLOAT,
    avg_token_per_clause FLOAT,
    swear_IT INT,
    swear_EN INT
);

CREATE TABLE Dim_Time (
    id_time INT PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    quarter INT,
    season NVARCHAR(20)
);

-- 3. Create Fact Table
CREATE TABLE Fact_Streams (
    id_track NVARCHAR(50),
    id_artist NVARCHAR(50),
    id_time INT,
    streams BIGINT,       
    popularity INT,
    
    CONSTRAINT FK_Track FOREIGN KEY (id_track) REFERENCES Dim_Track(id_track),
    CONSTRAINT FK_Artist FOREIGN KEY (id_artist) REFERENCES Dim_Artist(id_artist),
    CONSTRAINT FK_Time FOREIGN KEY (id_time) REFERENCES Dim_Time(id_time),
    
    CONSTRAINT PK_Fact PRIMARY KEY (id_track, id_artist, id_time)
);