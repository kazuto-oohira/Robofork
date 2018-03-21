import os, sys, csv, time, json

# Shell起動, Background起動時もSIGINTをKeyboardInterruptで捕まえる
import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../robofork_app/libs')
import utility

test_data_file = '/Users/sngmr/Projects/NKC/RoboFork/sources/RoboforkWeb/robofork_bin/test/test_data/fork_route_data.tsv'

def create_test_data():
    try:
        with open(test_data_file) as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                data = (
                    utility.to_hex(utility.to_can_signed(int(row[0]))) +
                    utility.to_hex(utility.to_can_signed(int(row[1]))) +
                    utility.to_hex(utility.to_can_signed(1000)) +
                    utility.to_hex(utility.to_can_signed(77))
                )

                mqtt_data = {
                    "serial_number": "1",
                    "id": "402",
                    "data": utility.to_can_data(data),
                }
                print("Robofork/1/toS#" + json.dumps(mqtt_data))

                time.sleep(0.01)

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    create_test_data()
