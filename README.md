# Adaptive Artemis News Recommendation

Adaptive Artemis is an advanced news recommendation system that personalizes content based on user preferences and reading history. This project is a comprehensive system that involves a web crawler, a backend server, and a user interface for seamless interaction.

## Features

- Personalized news articles recommendation.
- User registration and authentication.
- Article read history tracking.
- User profile management including preference settings.
- Dynamic updating of user preferences based on browsing history.

## Getting Test
- 1 Sign up(success and fail)
- username: lily
- email: lily@gmail.com
- password: P@ssword123
- 
- 2 Login(success and fail)
- 
- 3. Select the initial preferences
- 
- 4. Navigate to News recommendations
- 5. Clicking the news link will take you to the news content and store your browsing history
- 6. Go to the profile screen and see your current preferences and browsing history
- 7. Simulate the execution of a scheduled task in the terminal to crawl new news and update the user list
- 8. Log in again
- 9. Go straight to the news page and see new recommendations
- 10. Go to profile to see the updated preferences


### Prerequisites

- Python 3.8+
- Django 3.2+
- Scrapy 2.5+
- Celery 5.3+
- RabbitMQ as the message broker

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository/AdaptiveArtemisNewsRecommendation.git
2. Setup:
- To run this project, install it locally using venv and pip:
```bash
- Step1: Configure the python interpreter, version is python 3.12.0

- Step2: Configuring the virtual environment in a virtual project

$ python -m venv venv
$ .\venv\Scripts\activate  # On Windows
$ source venv/bin/activate  # On macOS or Linux
$ pip install -r requirements.txt   # Various configuration environment packages
 
