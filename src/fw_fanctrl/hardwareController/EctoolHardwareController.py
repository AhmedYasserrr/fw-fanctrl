import re
import subprocess
from abc import ABC
import pyectool
from fw_fanctrl.hardwareController.HardwareController import HardwareController


class EctoolHardwareController(HardwareController, ABC):
    noBatterySensorMode = False
    nonBatterySensors = None

    def __init__(self, no_battery_sensor_mode=False):
       self.noBatterySensorMode = no_battery_sensor_mode

    def get_temperature(self):
        if self.noBatterySensorMode:
            max_temp = pyectool.get_max_non_battery_temperature()
        else:
            max_temp = pyectool.get_max_temperature()
 
        # safety fallback to avoid damaging hardware
        if max_temp < 0:
            return 50
        return float(round(max_temp, 2))

    def set_speed(self, speed):
        pyectool.set_fan_duty(speed)

    def is_on_ac(self):
        return pyectool.is_on_ac()

    def pause(self):
        pyectool.auto_fan_control()

    def resume(self):
        # Empty for ectool, as setting an arbitrary speed disables the automatic fan control
        pass
