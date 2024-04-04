# Binance Trading History Dashboard

## Overview
This project provides a comprehensive dashboard for visualizing and analyzing trading history from Binance. It features data processing capabilities to clean and transform CSV exports from Binance, stores processed data in a PostgreSQL database, and presents insights through a Plotly Dash web application. Users can upload trading history files, view processed data, and analyze their trading performance over time with various interactive visualizations.

## Features
- **Data Processing:** Clean and transform Binance trading history CSV files using Pandas.
- **Database Storage:** Store and manage processed trading data in a PostgreSQL database.
- **Interactive Dashboard:** Visualize trading data with time series charts, profit distributions, asset allocations, and more using Plotly Dash.
- **Trading Journal:** Enter and track individual trades, including entry price, risk-to-reward ratios, and other trade-related metrics.

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pipenv (optional for virtual environment management)

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/binance-trading-history-dashboard.git
   cd binance-trading-history-dashboard

2. **Install Dependencies**
   - Using pip:
   ```bash
   pip install -r requirements.txt
   ```
   - Using pipenv:
     
   ```bash
   pipenv install
pipenv shell
   ```
3. **Database Configuration**
- Create a PostgreSQL database for storing the trading data.
- Update the database configuration in `database/db_config.py` with your database credentials.

2. **Environment Variables**
- Create a .env file in the project root directory.
- Add your database credentials:
```bash
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
### Usage

1. **Start the Dash App**

```bash
python app.py
```
This will start the Dash server, and the application will be accessible at http://127.0.0.1:8050/ by default.

2. **Uploading Trading History**

- Navigate to the Dash application in your web browser.
- Use the "Drag and Drop or Select Files" area to upload your Binance trading history CSV files.
3. **Viewing and Analyzing Data**

- Once uploaded, the data will be processed and stored in the database.
- Use the sidebar to navigate to different sections of the dashboard for data visualization and analysis.

   
