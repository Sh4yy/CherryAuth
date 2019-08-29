from app import create_app, create_secret, create_db


def main():
    """
    initialize mongodb
    create jwt secret if does not exist
    run the webserver
    """

    create_db()
    create_secret()
    (create_app()
        .run(host="0.0.0.0", port=5001, debug=True))


if __name__ == '__main__':
    main()
