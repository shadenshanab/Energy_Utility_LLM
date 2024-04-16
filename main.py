import create_database
from app import app


def main():
    print("Starting database creation...")
    create_database.main()

    print("Database created successfully.")

    print("Launching the bot GUI...")
    app.run(debug=True, port=8080)


if __name__ == '__main__':
    main()
