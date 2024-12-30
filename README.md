# LinkedIn Outreach AI Bot for Lead Generation

An automated LinkedIn outreach tool designed to connect with early-career professionals from WITCH (Wipro, Infosys, TCS, Cognizant, HCL) companies.

## Features

- **Smart Profile Targeting**: Focuses on professionals with 0-5 years of experience in WITCH companies
- **Automated Connection Requests**: Sends personalized connection requests using OpenAI for message generation
- **Company-Specific Messaging**: Tailors messages based on the target's company and experience level
- **Safe Automation**: Implements rate limiting and delays to comply with LinkedIn's usage guidelines

## Prerequisites

- Python 3.12+
- Chrome Browser
- LinkedIn Account
- OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/outreach_bot_linkedin.git
cd outreach_bot_linkedin
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

## Project Structure

```
outreach_bot_linkedin/
├── config/
│   └── settings.py         # Configuration settings
├── src/
│   ├── messaging/
│   │   └── message_generator.py    # OpenAI-powered message generation
│   ├── scraper/
│   │   └── linkedin_bot.py        # LinkedIn automation
│   └── utils/
│       └── profile_analyzer.py     # Profile analysis and scoring
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── main.py               # Main entry point
```

## Usage

1. Ensure your LinkedIn credentials and OpenAI API key are set in the `.env` file
2. Run the bot:
```bash
python main.py
```

The bot will:
1. Log into your LinkedIn account
2. Search for professionals from WITCH companies
3. Analyze profiles based on experience and company
4. Send personalized connection requests

## Safety Features

- Rate limiting to avoid LinkedIn restrictions
- Random delays between actions
- Maximum daily connection limit
- Manual verification handling
- Error recovery mechanisms

## Configuration

Adjust settings in `config/settings.py`:
- Maximum connection requests per day
- Target companies list
- Experience range
- Delay between requests

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
