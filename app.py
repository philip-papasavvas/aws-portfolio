"""
Created on: 12 Dec 2023
Run the app
"""
from portfolio_tracker import create_app

app = create_app()

if __name__ == '__main__':
    # only run if the script is executed correctly
    app.run(debug=True)
