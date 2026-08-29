# Music Streaming Analytics & Decision Support System

An end-to-end data engineering, OLAP, and business intelligence project for analyzing music streaming behaviour using **Python, SQL Server, SSIS, SSAS Multidimensional, MDX, and Power BI**.

The project transforms raw music-streaming data into a structured analytical environment: data is profiled and prepared in Python, modeled in a multidimensional data warehouse, processed through ETL workflows, exposed through an SSAS OLAP cube, queried using MDX, and finally presented through interactive Power BI dashboards.

---

## Project Overview

Music streaming data contains information about songs, artists, releases, lyrical characteristics, categories, time, geography, and streaming performance.

The objective of this project was to transform this data into a complete **Decision Support System (DSS)** capable of answering analytical questions such as:

- Which artists, songs, and song categories generate the most streams?
- How has streaming activity evolved over time?
- Which song categories are growing or declining?
- How does an artist's geographic origin relate to streaming performance?
- How are explicit and non-explicit lyrics distributed?
- How has explicit lyrical content evolved over time?
- Is artist performance associated with releasing many songs or with a smaller number of high-performing songs?
- How do current streaming patterns compare with previous periods?
- What trends can be identified using multidimensional analysis?

The project covers the complete analytical pipeline rather than only visualization.

---

## End-to-End Architecture

```text
Raw Music Streaming Data
          │
          ▼
┌─────────────────────────────┐
│ Python Data Preparation     │
│ Profiling • Cleaning        │
│ Transformation             │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ SQL Server Data Warehouse   │
│ Facts • Dimensions          │
│ Analytical Schema          │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ SSIS ETL                    │
│ Extraction • Transformation│
│ Loading • Derived Features │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ SSAS Multidimensional Cube  │
│ Measures • Dimensions       │
│ Hierarchies • OLAP Model    │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ MDX Analytical Layer        │
│ Trends • Rankings • Growth  │
│ Time & Category Analysis    │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Power BI                    │
│ Interactive Dashboards      │
│ Decision Support            │
└─────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Data Preparation | Python | Profiling, cleaning and transformation |
| Data Storage | SQL Server | Relational analytical data storage |
| Data Warehousing | SQL / SQL Server | Fact and dimension modeling |
| ETL | SQL Server Integration Services (SSIS) | Data integration and analytical transformations |
| OLAP | SQL Server Analysis Services (SSAS) | Multidimensional analytical model |
| Query Language | MDX | Multidimensional querying and calculations |
| Visualization | Power BI | Interactive dashboards and decision support |
| Version Control | GitHub | Project organization and portfolio documentation |

---

# Project Workflow

## 1. Data Preparation

The first stage investigates and prepares the source music-streaming data before it enters the analytical system.

The work includes:

- initial data inspection;
- attribute and schema analysis;
- missing-value investigation;
- duplicate and consistency checks;
- data-type validation;
- cleaning and preprocessing;
- song-level profiling;
- preparation of data for downstream warehouse and analytical processes.

The goal of this stage is to ensure that the data entering the warehouse is sufficiently structured and consistent for reliable analysis.

Relevant material is available in:

```text
data-preparation/
├── assignment-01/
├── assignment-02/
└── assignment-03/
```

Processed project data is maintained separately under:

```text
data/processed/
```

---

## 2. Data Warehouse

After preparation, the data is organized into a warehouse-oriented analytical structure.

The warehouse separates measurable streaming activity from the descriptive dimensions used to analyze it.

The dimensional model supports analysis involving concepts such as:

- artists;
- tracks;
- time;
- streaming activity;
- song characteristics;
- categories;
- geographical attributes.

This separation allows streaming measures to be aggregated across multiple analytical perspectives.

Relevant implementation material is available in:

```text
data-warehouse/
├── assignment-04/
├── assignment-05/
└── assignment-06/
```

### Warehouse workflow

```text
Prepared Data
     │
     ├──► Dimensions
     │      ├── Artist
     │      ├── Track
     │      └── Time
     │
     └──► Streaming Facts
                │
                ▼
        Analytical Warehouse
```

The resulting warehouse provides the relational foundation for both ETL processing and multidimensional analysis.

---

## 3. SSIS ETL & Analytical Transformation

SQL Server Integration Services was used to construct the ETL and transformation workflows required by the analytical system.

The SSIS stage goes beyond simple file loading. It performs transformations required for later analytical questions.

The workflows include operations such as:

- extracting source data;
- transforming and standardizing fields;
- joining related datasets;
- sorting and aggregating records;
- deriving analytical columns;
- preparing song and artist measures;
- generating features required by subsequent analyses;
- producing transformed datasets suitable for warehouse/OLAP consumption.

Relevant material is available in:

```text
ssis-etl/
├── assignment-09/
├── assignment-10/
├── assignment-11/
├── assignment-12/
└── assignment-13/
```

These packages demonstrate the movement from raw operational-style data toward analytics-ready information.

---

## 4. SSAS Multidimensional OLAP Model

The analytical warehouse is exposed through a **SQL Server Analysis Services multidimensional model**.

The SSAS project defines the dimensions, cube structure, relationships, and measures required for multidimensional analysis.

Major analytical dimensions include:

### Artist

Used to analyze streaming behaviour according to artist-related attributes, including geographical information.

### Track

Provides song-level analytical information and supports analysis across track characteristics and song categories.

### Time

Enables temporal analysis across multiple levels and supports trend, historical, and period-comparison calculations.

### Streaming Measures

Streaming activity is represented through measures that can be aggregated across dimensions and hierarchies.

The SSAS model is available under:

```text
ssas-cube/
```

It includes the multidimensional project definitions required to describe the analytical cube.

---

## 5. MDX Analysis

Once the OLAP model was available, **MDX (Multidimensional Expressions)** was used to perform advanced analysis directly against the cube.

The MDX layer demonstrates analytical operations that go beyond basic relational queries, including:

- multidimensional slicing;
- calculated members;
- ranking;
- contribution analysis;
- time-based comparison;
- year-over-year analysis;
- category comparison;
- growth calculations;
- regional analysis;
- market-share-style analysis.

Relevant MDX work is available under:

```text
mdx-analysis/
```

### Examples of analytical tasks

#### Geographic and Regional Analysis

Streaming performance can be analyzed across artist locations and geographical hierarchies to understand where streaming activity is concentrated.

#### Artist Contribution Analysis

Weighted contribution measures were used to distinguish different artist roles when evaluating streaming performance.

For example, analytical logic can assign different weights to main and featured artist contributions rather than treating every appearance identically.

#### Year-over-Year Growth

Previous-period values are obtained through multidimensional time navigation and compared with current performance.

Conceptually:

```text
Growth % =
(Current Period Streams - Previous Period Streams)
-------------------------------------------------- × 100
              Previous Period Streams
```

This allows categories with increasing or decreasing streaming performance to be identified.

#### Seasonal Analysis

Streaming behaviour is also compared across seasonal/time periods to determine whether categories outperform historical benchmarks.

#### Growth-Share Analysis

Growth and relative streaming contribution are combined to support portfolio-style evaluation of song categories.

The MDX layer therefore acts as the analytical bridge between the OLAP cube and the final decision-support visualizations.

---

# 6. Power BI Decision Support Dashboards

The final stage transforms the analytical model into interactive Power BI dashboards.

Rather than displaying only basic totals, the dashboards address specific decision-support questions.

Power BI material is located under:

```text
power-bi/
├── assignment-20/
├── assignment-21/
└── assignment-22/
```

Each public portfolio folder contains:

```text
dashboard image
sanitized PBIX file
README.md
```

---

## Dashboard 1 — Geographic Streaming Analysis

**Assignment 20**

This dashboard investigates how streaming activity is distributed geographically according to artist birthplace and song category.

### Main analyses

- global distribution of streams by artist birthplace;
- geographical concentration of streaming activity;
- stream totals for individual birthplaces;
- comparison between song categories across locations.

### Key question

> Where do high-performing artists originate, and how does song-category performance differ geographically?

The combination of map and ranked bar visualization makes both global patterns and individual locations visible.

See:

```text
power-bi/assignment-20/
```

---

## Dashboard 2 — Lyrical Content Analysis

**Assignment 21**

This dashboard explores the relationship between lyrical characteristics and streaming activity.

### Main analyses

- explicit vs non-explicit lyrical content;
- song-category distribution according to lyric length;
- swear-word frequency;
- evolution of explicit content over time;
- top songs by streams within the lyrics-based analysis.

### Explicit vs Non-Explicit Content

The dashboard compares the streaming share associated with explicit and non-explicit lyrics.

This provides a direct view of how lyrical classification relates to total streaming activity.

### Lyric Length

Song categories are compared according to lyric length, allowing differences in lyrical structure to be examined.

### Swear-Word Distribution

The dashboard also investigates the distribution of detected swear-word counts.

### Evolution Over Time

Explicit content is analyzed historically to determine how its presence within streaming activity changes across years.

### Top Streaming Songs

High-performing tracks are ranked to connect lyrical characteristics with actual streaming outcomes.

See:

```text
power-bi/assignment-21/
```

---

## Dashboard 3 — Streaming & Song Category Trends

**Assignment 22**

The final dashboard focuses on long-term streaming behaviour, release activity, category growth, and artist output.

### Main analyses

- artist quantity versus streaming performance;
- streaming growth by song category;
- song-release trends over time;
- individual category growth trajectories.

### Quantity vs Quality

A scatter analysis compares:

```text
Number of songs / observations
              vs
        Streaming performance
```

This addresses the question:

> Do artists achieve high streaming performance by producing more songs, or can a smaller catalogue generate stronger results?

The visualization shows that artist output and streaming performance are not simply equivalent measures.

### Streaming Growth by Song Category

Historical streaming activity is separated across:

- Energetic/Emotional
- Energetic/Party
- Mellow/Bright
- Soft/Chill

This allows periods of acceleration, decline, and category-specific behaviour to be identified.

### Song Release Trends

Release activity is also analyzed over time to distinguish growth in the number of songs from growth in actual streaming consumption.

### Individual Category Trends

Separate category views make it possible to inspect each trajectory without larger categories visually dominating smaller ones.

See:

```text
power-bi/assignment-22/
```

---

# Analytical Story

The complete project can be understood as a progression from **data to decisions**.

### Stage 1 — What data do we have?

Python profiling and preparation establish the structure and quality of the source data.

### Stage 2 — How should it be organized?

The data warehouse separates measurable streaming activity from dimensions such as Artist, Track, and Time.

### Stage 3 — How do we transform it?

SSIS pipelines perform the integration and transformations required for analysis.

### Stage 4 — How can it be explored multidimensionally?

SSAS exposes the warehouse through an OLAP cube containing dimensions, hierarchies, relationships, and measures.

### Stage 5 — What analytical questions can we calculate?

MDX provides multidimensional calculations for trends, growth, contribution, geography, time comparisons, and category performance.

### Stage 6 — How can the results support decisions?

Power BI translates these analytical structures into dashboards that allow users to explore geographical, lyrical, temporal, artist, and category-level streaming behaviour.

---

# Repository Structure

```text
LDS-Music-Streaming-Analytics/
│
├── data-preparation/
│   ├── assignment-01/
│   ├── assignment-02/
│   └── assignment-03/
│
├── data-warehouse/
│   ├── assignment-04/
│   ├── assignment-05/
│   └── assignment-06/
│
├── data/
│   └── processed/
│
├── ssis-etl/
│   ├── assignment-09/
│   ├── assignment-10/
│   ├── assignment-11/
│   ├── assignment-12/
│   └── assignment-13/
│
├── ssas-cube/
│   └── multidimensional OLAP model
│
├── mdx-analysis/
│   └── multidimensional analytical queries
│
├── power-bi/
│   ├── assignment-20/
│   ├── assignment-21/
│   └── assignment-22/
│
├── report/
│   └── project documentation
│
└── README.md
```

---

# How the Components Connect

One important aspect of this repository is that the technologies are **not independent exercises**.

They form one analytical system.

```text
Python
  │
  │ cleans and prepares
  ▼
SQL Server Warehouse
  │
  │ stores facts and dimensions
  ▼
SSIS
  │
  │ integrates and transforms
  ▼
SSAS
  │
  │ provides multidimensional model
  ▼
MDX
  │
  │ performs OLAP calculations
  ▼
Power BI
  │
  ▼
Business / Analytical Insight
```

This integration is the central purpose of the project.

---

# Key Skills Demonstrated

## Data Engineering

- data profiling;
- data cleaning;
- transformation pipelines;
- ETL design;
- analytical data preparation.

## Data Warehousing

- dimensional modeling;
- fact and dimension structures;
- analytical schema design;
- SQL Server data management.

## Business Intelligence

- OLAP modeling;
- multidimensional dimensions and measures;
- analytical hierarchies;
- dashboard design;
- decision-support analysis.

## Analytical Querying

- MDX;
- calculated members;
- time intelligence;
- ranking;
- growth calculations;
- multidimensional filtering and aggregation.

## Visualization

- Power BI;
- geographic visualization;
- time-series analysis;
- category comparison;
- ranking;
- distribution analysis;
- interactive analytical dashboards.

---

# Security and Public Repository Sanitization

The original development environment used course/institutional infrastructure for SQL Server Analysis Services and related services.

For the public version of this repository, environment-specific connection information was intentionally removed or replaced.

Public Power BI artifacts use placeholders such as:

```text
YOUR_SSAS_ENDPOINT
YOUR_DATABASE
YOUR_CUBE
```

The original private development files are therefore not required to expose institutional server details in the public repository.

Users who want to reproduce the analytical environment should configure their own SQL Server / Analysis Services connection.

No credentials are intentionally included in this repository.

---

# Reproducibility Notes

Some components of the project depend on Microsoft SQL Server Business Intelligence tooling, including:

- SQL Server;
- SQL Server Integration Services;
- SQL Server Analysis Services Multidimensional;
- Power BI Desktop.

Because SSIS and SSAS projects depend on local/server configuration, reproducing the complete system requires configuring an equivalent Microsoft BI environment.

The repository is primarily structured to preserve:

1. the analytical workflow;
2. transformation logic;
3. multidimensional model;
4. MDX analysis;
5. dashboard implementation;
6. project documentation.

---

# How to Explore This Repository

For a quick overview, a recommended path is:

```text
1. README.md
      ↓
2. data-preparation/
      ↓
3. data-warehouse/
      ↓
4. ssis-etl/
      ↓
5. ssas-cube/
      ↓
6. mdx-analysis/
      ↓
7. power-bi/
      ↓
8. report/
```

For recruiters or reviewers primarily interested in analytics and visualization, start with:

```text
power-bi/
```

For data engineering and BI implementation, inspect:

```text
data-preparation/
data-warehouse/
ssis-etl/
ssas-cube/
```

For multidimensional analytics, inspect:

```text
mdx-analysis/
```

---

# Project Outcome

The final result is an end-to-end **music streaming analytics and decision support system** that demonstrates how raw data can be transformed into progressively more useful analytical structures.

The project integrates:

**data preparation → data warehousing → ETL → OLAP → multidimensional querying → business intelligence visualization**

within a single analytical workflow.

Rather than treating Python, SQL Server, SSIS, SSAS, MDX, and Power BI as isolated technologies, the project demonstrates how they can work together to transform raw streaming data into interpretable analytical information.

---

## Authors

**Fiza Naeem**  
**Zahra Hameed Khan**

MSc Data Science and Business Informatics  
University of Pisa

---

## Project Context

Academic project developed as part of work in **Laboratory of Data Science / Decision Support and Business Intelligence**, demonstrating an end-to-end Microsoft BI and data analytics workflow.
