import requests
import hashlib
import sys


def main():
    def hash_password_sha1():
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    def pwned_api_check():
        def request_data(query_characters):
            url = 'https://api.pwnedpasswords.com/range/' + query_characters
            response = requests.get(url)
            if response.status_code != 200:
                raise RuntimeError(
                    f'There was an error fetching from the API. Check the API documentation and try again. '
                    f'error status code: {response.status_code}')
            return response

        def get_password_breach_count(hash_to_be_checked):
            hashes_from_api = (line.split(':') for line in api_response.text.splitlines())
            for hash, breaches_count in hashes_from_api:
                if hash_to_be_checked == hash:
                    return breaches_count
            return 0

        sha1password_first_five_characters = sha1password[:5]  # query characters for API are first five characters
        sha1password_tail = sha1password[5:]  # API returns tails of all hashes matching first five characters
        api_response = request_data(sha1password_first_five_characters)
        return get_password_breach_count(sha1password_tail)

    with open(sys.argv[1]) as passwords_file:
        passwords_list = passwords_file.read().splitlines()
        for password in passwords_list:
            asterisks = (len(password) - 2) * '*'
            sha1password = hash_password_sha1()
            breach_count = pwned_api_check()
            if breach_count:
                print(f'The password "{password[:2]}{asterisks}" was found {breach_count} times '
                      f'in the haveibeenpwned.com database. If this is your password, you should change it.')
            else:
                print(f'The password "{password[:2]}{asterisks}" was not found in the haveibeenpwned.com database.')


if __name__ == '__main__':
    main()
