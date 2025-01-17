# Spotify Playlist Creator

This project scrapes the Billboard Hot 100 chart for a specified date and creates a Spotify playlist with the top songs from that day.

## Features
- Scrape the Billboard Hot 100 chart using BeautifulSoup.
- Authenticate with Spotify using OAuth.
- Create and populate a Spotify playlist with the scraped songs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:
   ```bash
   cd your-repository
   ```

3. Create a virtual environment and activate it (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your `.env` file with your Spotify credentials:
   ```env
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   REDIRECT_URI=your_redirect_uri
   ```

## Usage

1. Run the script and follow the prompts to scrape the Billboard Hot 100 and create a Spotify playlist:
   ```bash
   python script_name.py
   ```

## License
This project is licensed under the MIT License.
