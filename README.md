# AllePoints Dashboard

A dashboard application for searching and displaying member data from the Alle business site.

## Features

- Search for members by phone number
- Display detailed member information including points
- View summary statistics for all members
- Filter members by minimum points
- Interactive data visualization

## Requirements

- Python 3.8+
- Chrome browser (for Selenium WebDriver)
- Alle business account credentials
- Bluehost account credentials (for deployment)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AllePoints.git
   cd AllePoints
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your credentials:
   ```
   # Alle credentials
   ALLE_USERNAME=your_alle_username
   ALLE_PASSWORD=your_alle_password

   # Bluehost credentials
   BLUEHOST_USERNAME=your_bluehost_username
   BLUEHOST_PASSWORD=your_bluehost_password

   # Environment (development or production)
   ENVIRONMENT=development

   # Server configuration
   PORT=8050
   ```

## Usage

1. Run the application:
   ```
   python run.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8050
   ```

3. To search for a member, enter a phone number in the search box and click "Search".

## Deployment to Bluehost

1. Make sure your Bluehost credentials are set in the `.env` file.

2. Run the deployment script:
   ```
   python deploy.py
   ```

3. Access your dashboard at your Bluehost domain.

## Project Structure

- `src/`: Source code directory
  - `api/`: API clients and web scrapers
  - `data/`: Data processing modules
  - `dashboard/`: Dashboard layout and components
- `tests/`: Test cases
- `config/`: Configuration files
- `docs/`: Documentation
- `run.py`: Main entry point for running the application
- `requirements.txt`: Python dependencies

## Security Notes

- Never commit your `.env` file or any files containing credentials to version control.
- Use environment variables for sensitive information.
- Consider using a secrets manager for production deployments.

## License

This project is licensed under the MIT License - see the LICENSE file for details.