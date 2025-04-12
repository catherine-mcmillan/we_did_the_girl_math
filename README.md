# We Did The Girl Math

A social financial justification app where users can share their "girl-math" expense justifications and get feedback from their social network.

## Features

- Create posts with financial justifications for purchases/expenses
- Vote on others' posts with options like "The math checks out", "Treat Yo Self", etc.
- Comment on posts and reply to comments
- Ask for help justifying an expense
- Hall of Fame for most popular posts
- Facebook integration for social connections

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Conda or another virtual environment manager

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/we_did_the_girl_math.git
   cd we_did_the_girl_math
   ```

2. Create and activate a conda environment:
   ```
   conda create -n girl_math python=3.9
   conda activate girl_math
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```
   
7. Open your browser and navigate to `http://127.0.0.1:5000`

## Testing

Run the test suite with pytest:
```
pytest
```

## Deployment

The application is configured for deployment on Fly.io. See the deployment section for instructions.

