# Processed Data

This directory represents the processed and derived datasets produced throughout the Music Streaming Analytics & Decision Support System.

## Data Processing Strategy

The project does not maintain a second duplicate copy of every generated dataset in this directory.

Instead, processed datasets and analytical CSV outputs are stored alongside the assignment or processing stage that generated them. This preserves the relationship between:

- source data;
- transformation logic;
- generated dataset;
- analytical result.

Examples of these outputs can be found throughout:

- `data-preparation/`
- `data-warehouse/`
- `ssis-etl/`
- `mdx-analysis/`
- `power-bi/`

## Processing Flow

The general transformation pipeline is:

Raw source data  
→ Python profiling and preparation  
→ SQL Server dimensional warehouse  
→ SSIS transformations and derived features  
→ SSAS multidimensional model  
→ MDX analytical results  
→ Power BI visualizations

The original source datasets that are publicly included in the repository are documented under:

`data/raw/`

## Reproducibility

Where an assignment produces a CSV or other intermediate analytical result, that output is retained within the corresponding assignment directory rather than duplicated here.

This organization keeps the repository traceable while avoiding unnecessary duplication of derived data.
