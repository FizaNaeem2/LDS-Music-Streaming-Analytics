# SSAS / OLAP Multidimensional Model

Portfolio-safe Analysis Services project for the music-streaming data warehouse.

## Contents
- Artist, Track, and Time dimensions
- Cube definition and partitions
- Data source and data source view
- Analysis Services database/project/solution definitions

## Security
Server, database, user, machine, and local-path identifiers were sanitized.
The user-specific `.dwproj.user` deployment file and Visual Studio upgrade logs are intentionally excluded.

## Pipeline
Relational data warehouse → SSAS data source/view → dimensions → cube/partitions → OLAP and MDX analysis.
