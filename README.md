# Real-Estate Scraper: btnproperti

[btnproperti](https://www.btnproperti.co.id/) is an online platform that focuses on real estate services, primarily in Indonesia. It serves as a marketplace for property listings, connecting buyers, sellers, and real estate agents.

This project efficiently processed over 8,700 URLs in less than an hour, utilising multi-threading, retry mechanisms and robust logging.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Application Flow](#application-flow)
- [Technical Highlights](#technical-highlights)
- [Data Processing](#data-processing)
- [License](#license)

## Project Structure

```
project-root/
├── scraper/              # Contains all scraping logic
│   ├── scraper.py        # Main scraping functions
│   └── ...
├── data_handler/         # Data preprocessing scripts
│   ├── data_cleaning.py  # Functions for data cleaning and formatting
│   └── ...
├── DATA.json             # Initial real-estate developer profiles
├── HEADERS.json          # Request header data (updated daily)
└── main.py               # Entry point to run the scraper
```

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/rianaditro/btnproperti.git
   cd real-estate-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open the website using your profile and copy your headers into `HEADERS.json` to ensure successful requests.

## Application Flow

1. **Run the Scraping Script**
   - Execute the command:
     ```bash
     python main.py
     ```
   - This command initiates the scraping process, targeting all available developer data from the specified URLs.

2. **Check for Errors**
   - After the scraping completes, review the `scraper.log` file for any failed requests. This log is essential for debugging and verifying the scraping success.

3. **Generate Output Files**
   - The scraper produces two output files:
     - `developer_profiles.xlsx`: Contains details of each developer.
     - `developer_projects.xlsx`: Lists all projects associated with each developer.

4. **Data Cleaning and Manipulation**
   - Utilize the provided Jupyter Notebook or Google Colab file to interactively clean and manipulate the scraped data:
      - **Validation Step**: Before finalizing, compare the `jml_prpt` column from the developer profiles with the count of `ID_DEV` in the developer projects. Both values should match for data integrity.

     - **Data Cleaning**: Ensures entries meet quality standards.
     - **Reformatting**: Adjusts the data structure for consistency.
     - **Column Selection**: Chooses relevant columns for analysis.
     - **Renaming Columns**: Updates column names for clarity.



5. **Export Cleaned Data**
   - Once the data is cleaned and formatted, export the final dataset as a single file for client deliverables.

## Technical Highlights

- **Retry Mechanism**: Implements a robust retry mechanism to handle temporary errors during HTTP requests, ensuring higher success rates in scraping.
  
- **Logging**: Utilizes logging throughout the scraping process to monitor progress and record any failed URLs, aiding in troubleshooting and debugging.

- **ThreadPoolExecutor**: Leverages `ThreadPoolExecutor` to execute scraping operations concurrently, significantly improving performance and allowing for efficient processing of a large number of URLs.

## Data Processing

The data processing file is provided in `.ipynb` format, making it easier to handle various data processing tasks through an interactive environment like Jupyter Notebook or Google Colab.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

