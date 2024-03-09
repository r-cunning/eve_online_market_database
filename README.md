## EVE Online Database Repository
Welcome to the EVE Online Database Repository! This project is a hobby venture aimed at enhancing my database management skills and practicing data science concepts outside of my PhD work. Leveraging the rich universe of EVE Online, this repository hosts a database filled with in-game data that serves as a playground for various data science experiments, including but not limited to, forecasting the in-game economy using advanced machine learning techniques.

### Project Overview
At the core of this project is a database utilizing PostgreSQL with the TimescaleDB extension, optimized for time-series data. This setup allows for efficient storage, retrieval, and manipulation of time-based data points critical for analyzing and forecasting within the dynamic ecosystem of EVE Online. The database is run through a Docker container, ensuring a smooth and consistent setup across different environments.

Data populating this database is meticulously gathered and processed using a combination of Python scripts (.py files) and Jupyter Notebooks. The raw data is downloaded via the Windows Subsystem for Linux, showcasing a diverse toolset for data acquisition and management.

### Repository Structure

tables folder: contains a subfolder for each table in the database. Subfolders contain .py and juptyer notebook files for creating, populating and querying their respective tables.
Python Scripts: A series of .py files responsible for data extraction, transformation, and loading (ETL) processes.
Jupyter Notebooks: Used to call the functions in the .py files and populate the tables.

Docker: Configuration files and setup instructions for deploying the PostgreSQL + TimescaleDB environment within a Docker container.
Data: Though the raw data files are not stored within this repository due to size constraints, instructions on how to acquire and load the data into the database are provided.
Integrations
This database does not stand alone; it feeds into a larger ecosystem of data analysis and forecasting projects. Specifically, it integrates with my other project repository, EVE Online Forecasting, where Python scripts leverage the data stored here to train machine learning models.

### Key Features:
Player Activity Metrics: The database includes detailed metrics on player activities such as ship destructions and industrial output, offering a rich dataset to base forecasting models and market analysis on.

### Getting Started

#### To get started with this project:

Set up Docker: Follow the instructions in the Docker folder to deploy the PostgreSQL + TimescaleDB environment.
Data Acquisition: Use the guidelines provided to download the raw EVE Online data using Linux or the Windows Subsystem for Linux.
Data Loading: Utilize the provided Python scripts and Jupyter Notebooks to populate the database with the acquired data.
Data Analysis and Forecasting: Refer to the EVE Online Forecasting repository for instructions on how to use the data for training machine learning models.




License
This project is open-source and available under the MIT License.
