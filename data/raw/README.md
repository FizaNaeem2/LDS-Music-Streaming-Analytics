# Raw Data

This directory documents the original source datasets used in the Music Streaming Analytics & Decision Support System.

## Included Dataset

### `artists.xml`

Contains the original artist-related source data used throughout the project, including artist attributes required for data preparation, warehouse construction, geographic analysis, and multidimensional analytics.

This file is included in the public repository as part of the reproducible project data.

## Additional Source Data

The original project also used a track-level JSON source dataset containing music and streaming-related information.

That source file is **not included in the public repository**. Processed and derived outputs required to demonstrate the analytical workflow are retained within the relevant assignment directories and project artifacts.

## Data Flow

The source data was progressively processed through the project pipeline:

`Raw Data → Python Preparation → SQL Server → SSIS ETL → SSAS Cube → MDX Analysis → Power BI`

The raw datasets should therefore be understood as the starting point of the analytical workflow rather than standalone analytical outputs.
