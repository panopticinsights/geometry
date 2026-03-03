import os

# Set the correct port and production settings for Render deployment
PORT = int(os.environ.get('PORT', 5000))

# Other production settings can be configured below
app.config['DEBUG'] = False  # Disable debug mode in production
app.config['ENV'] = 'production'  # Set the environment to production

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)