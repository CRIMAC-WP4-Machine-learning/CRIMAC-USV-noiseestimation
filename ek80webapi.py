import requests
import argparse

# Testing the EK80 Web Api, documentation is available:
# http://localhost:12345/swagger/ui/index

# https://github.com/rhtowler/EK80_REST_Client/tree/main/ek80_param_client
# Could use Swagger CodeGen to generate this, too, probably. Just have to figure out how.
# https://goswagger.io/generate/client.html

# Joakim Skjefstad (joakim.skjefstad@hi.no) 13.11.2023

EK80_Hostname = "localhost"
EK80_CommandPort = "12345"

class EK80CommandApi:
    server = None
    server_command_port = None
    api_root = None

    def __init__(self, server = "localhost", command_port = "12345"):
        self.server = server
        self.server_command_port = command_port
        self.api_root = f'http://{self.server}:{self.server_command_port}/api/'

    def get_api_system(self):
        api_function = f'system'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_system_operational_state(self):
        api_function = f'system/operational-state'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def set_api_system_operation_mode(self, mode):
        api_function = f'system/operation-mode'
        api_payload = {'mode' : mode}
        api_url = f'{self.api_root}{api_function}'
        response = requests.put(api_url, data=api_payload)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_system_ping_mode(self):
        api_function = f'system/ping-mode'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_system_ping_interval(self):
        api_function = f'system/ping-interval'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_system_active_user_settings(self):
        api_function = f'system/active-user-settings'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_system_application_details(self):
        api_function = f'system/application-details'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_ownship(self):
        api_function = f'ownship'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_environment_WaterColumn(self):
        api_function = f'environment/WaterColumn'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_sensors(self):
        api_function = f'sensors'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_data_output(self):
        api_function = f'data-output'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_sounder_processing_channel_bottom_detection(self, channel_name):
        api_function = f'/sounder/processing/{channel_name}/bottom-detection'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
            print("NB: get_api_sounder_processing_channel_bottom_detection requires channel-name as parameter")
        return retval

    def get_api_sounder_ping_configuration_channel_list(self):
        api_function = f'/sounder/ping-configuration/channel-list'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
            print("NB: get_api_sounder_processing_channel_bottom_detection requires channel-name as parameter")
        
        return retval

    def get_api_sounder_ping_configuration_channel_pulse_settings(self, channel_id):
        api_function = f'/sounder/ping-configuration/{channel_id}/pulse-settings'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
            print("NB: get_api_sounder_ping_configuration_channel_pulse_settings requires channel-id as parameter")
        
        return retval

    def get_api_sounder_ping_configuration_channel_transmit_power(self, channel_id):
        api_function = f'/sounder/ping-configuration/{channel_id}/transmit-power'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
            print("NB: get_api_sounder_ping_configuration_channel_transmit_power requires channel-id as parameter")
        return retval

    def get_api_sounder_data_storage(self):
        api_function = f'/sounder/data-storage'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_sounder_data_storage_record_raw_active(self):
        api_function = f'/sounder/data-storage/record-raw-active'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval

    def get_api_sounder_ping_info(self):
        api_function = f'/sounder/ping-info'
        api_url = f'{self.api_root}{api_function}'
        response = requests.get(api_url)

        retval = None
        if response.status_code == 200:
            print(response.json())
            retval = response.json()
        else:
            print("Error code HTTP", response.status_code)
        return retval


def main():
    parser = argparse.ArgumentParser(description = "Try out the EK80 REST WebApi.")
    parser.add_argument("-ip", "--ip", help = "IP or hostname to EK80 Server, default is localhost")
    args = parser.parse_args()

    if args.ip:
        print(f'Using custom IP:{args.ip}')

    myApiInstance = EK80CommandApi(EK80_Hostname, EK80_CommandPort)

    print(f'Using EK80 WebServer {EK80_Hostname}:{EK80_CommandPort}. Change with -ip aaa.bbb.ccc.ddd; if not localhost, remember to set client IP in EK80 WebApi-settings!\n\n')
    
    print("# System:")
    ping_mode = myApiInstance.get_api_system_ping_mode()
    ping_interval = myApiInstance.get_api_system_ping_interval()
    active_user_settings = myApiInstance.get_api_system_active_user_settings()

    print("\n# Ownship:")
    ownship = myApiInstance.get_api_ownship()

    print("\n# Environment:")
    environment_WaterColumn = myApiInstance.get_api_environment_WaterColumn()

    print("\n# Sensors:")
    sensors = myApiInstance.get_api_sensors()

    print("\n# Data-output:")
    data_output = myApiInstance.get_api_data_output()

    print("\n# Ping-configuration:")
    channels = myApiInstance.get_api_sounder_ping_configuration_channel_list() # Output should be a list over transcievers (?)
    pulse_settings = myApiInstance.get_api_sounder_ping_configuration_channel_pulse_settings("channel-id") # Need to update this with a valid channel id!
    transmit_power = myApiInstance.get_api_sounder_ping_configuration_channel_transmit_power("channel-id") # Need to update this with a valid channel id!

    print("\n# Processing:")
    bottom_detection = myApiInstance.get_api_sounder_processing_channel_bottom_detection("channel-name") # Need to update this with a valid channel name!

    print("\n# Data-storage:")
    data_storage = myApiInstance.get_api_sounder_data_storage()
    record_raw_active = myApiInstance.get_api_sounder_data_storage_record_raw_active()

    print("\n# Ping-info")
    ping_info = myApiInstance.get_api_sounder_ping_info()

if __name__ == "__main__":
    main()