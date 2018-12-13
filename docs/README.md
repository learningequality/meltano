# Meltano Docs

## Prerequisites

- [NodeJS 8+](https://nodejs.org/en/)

## Getting Started

1. Navigate to project root directory in terminal
1. Run `npm install` or `yarn`
1. Run `npm run dev` or `yarn dev`

## Resources

- [VuePress](https://vuepress.vuejs.org)

## Terminology (temp location)

### MELTANO
- "Meltano is the market (data science) lifecycle, just like GitLab is the product (DevOps) lifecycle."
    - Single application for managing the data lifecycle (https://gitlab.com/meltano/meltano#approach)

### MELTANO Acronym

#### *E*xtract
- Extract data from one or more sources where a built-in listener kicks off the *Load* step once extraction is complete.
    - Typically an API call or DB pull > get data > spit it out in a preferred/expected format (the schema) at one record at a time vs a dump
        - "discovery step" to determine schema

#### *L*oad
- Using the *Model* definitions create a database using the *Extract*ed data.
    - Listen for extractor dispatches and load to DB based on extractor schema
        - incremental w/concurrency ideal for speed

#### *T*ransform
- Update the database fields to encourage human-friendly use of data in *Model* step.
    - currently using DBT for transformations

#### *M*odel
- Define the data model empowering the *Load*, *Transform*, and *Analyze* steps.
    - inform the *Analyze* step (dimensions - db column and measures - computed values)

#### *A*nalyze
- UX friendly rich and interactive data visualization tooling levageging *Model* data.
    - 'dashboarding' as part of this step

#### *N*otebook
- like Jupyter Notebooks
    - GUI live REPL for exploration of data - useful for saving and version controlled

#### *O*rchestrate
- Data lifecycle facilitator (Meltano itself?).
    - Airflow - automates and schedules (DAG), ELT jobs as pipelines with dependencies

### Related (more proprietiery?) Terminology

- Tap
    - an extractor of a specific dataset
- Target
    - the type of database
- Dimensions
    - db column
- View
    - table containing dimension
- Explore
    - one or more views
- Measure
    - computed values
- DAG
    - directed acyclic graph

