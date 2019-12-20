from modules.client.http import HTTPClient, HTTPClientConfiguration
import yaml

def main():
    with open("configuration.yaml") as configuration_file:
        configuration = yaml.full_load(configuration_file)
    client_configuration = HTTPClientConfiguration(configuration['connection'])
    print(client_configuration)
    client = HTTPClient(client_configuration)
    response = client.request("GET", "/cart/")
    print(response.headers)
    print(client.local_store)

if __name__ == "__main__":
    main()