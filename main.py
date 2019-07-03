from app import init_db, create_app


def main():
    init_db()
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()