import argparse
import time
import subprocess
import logging
from arm_controller import ArmControl


class ArmControlError(Exception):
    def __init__(self, error_code=None):
        self.error_code = error_code
        self.description = ["ERR_SUCC"
                            , "ERR_INVALID_HANDLER"
                            , "ERR_INVALID_PARAMETER"
                            , "ERR_COMMUNICATION_ERR"
                            , "ERR_KINE_INVERSE_ERR"
                            , "ERR_EMERGENCY_PRESSED"
                            , "ERR_NOT_POWERED"
                            , "ERR_NOT_ENABLED"
                            , "ERR_DISABLE_SERVOMODE"
                            , "ERR_NOT_OFF_ENABLE"
                            , "ERR_PROGRAM_IS_RUNNING"
                            , "ERR_CANNOT_OPEN_FILE"
                            , "ERR_MOTION_ABNORMAL"
                            , "ERR_FTP_PREFROM"]

    @property
    def msg(self):
        return self.description[-1 * self.error_code]


class NetWorkError(Exception):
    pass


def check_network_requirements(arm_ip):
    try:
        result = subprocess.run(['ping', '-c', '1', str(arm_ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if result.returncode == 0:
            logging.info(f"Successfully pinged {arm_ip}. Network requirements satisfied.")
        else:
            logging.warning(f"Failed to ping {arm_ip}. Check network connectivity.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while executing ping: {e}")
        raise NetWorkError("Error while executing ping: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise NetWorkError("Network requirements not satisfied")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip_right", type=str, help="ip address of left arm"
                        , default="172.16.9.17")
    args = parser.parse_args()
    ip_right = args.ip_right
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    try:
        check_network_requirements(ip_right)

        with ArmControl(ip_right) as robot:
            # while True:
            time.sleep(2)
            robot.stacking()

        logging.info("Stacking finish.")
                
    except NetWorkError as e:
        exit(1)
