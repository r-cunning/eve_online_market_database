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

### Getting Started:

#### Set up Docker
#### Prerequisites

Before you begin, ensure that Docker Desktop is installed on your system. If not, you can download and install it from the following links:
- [Docker Desktop: The #1 Containerization Tool for Developers | Docker](https://www.docker.com/products/docker-desktop/)

### Installation Steps

#### 1. Pull the TimescaleDB Docker Image

First, we need to pull the latest TimescaleDB image from Docker Hub. Open your terminal or command prompt and execute the following command:

```bash
docker pull timescale/timescaledb:latest-pg14
```

#### 2. Run docker container
With the Docker image pulled, the next step is to run a container instance of TimescaleDB. Use the command below, ensuring to replace mysecretpassword with your chosen password and D:/eve_db/timescaledb with your preferred data storage path on your host machine.

``` bash
docker run -d --name timescaledb -e POSTGRES_PASSWORD=mysecretpassword -v D:/eve_db/timescaledb:/var/lib/postgresql/data -p 5432:5432 timescale/timescaledb:latest-pg14
```
This command starts a detached (background) container named timescaledb, sets the database password, maps port 5432 on your host to the container, and sets up a mounted volume for data persistence.

#### 3. Run psql within the docker container:

``` bash
docker exec -it timescaledb psql -U postgres
```

Data Acquisition: 
Use the example bash scripts to download (using wget) and unpack the raw EVE Online data using Linux or the Windows Subsystem for Linux.
I have used historical data hosted on data.everef.net and adam4eve.com to populate my database.

Data Loading: Utilize the provided Python scripts and Jupyter Notebooks to populate the database with the acquired data.
- Database credentials are held in a config.py file (excluded here).
Data Analysis and Forecasting: Refer to the EVE Online Forecasting repository for instructions on how to use the data for training machine learning models.




License
This project is open-source and available under the MIT License.
