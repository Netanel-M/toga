from java import dynamic_proxy
from android.hardware import SensorEventListener, SensorEvent
from android.content import Context
from android.hardware import SensorManager, Sensor

class GyroscopeListener(dynamic_proxy(SensorEventListener)):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def onSensorChanged(self, event):
        if event.sensor.getType() == Sensor.TYPE_GYROSCOPE:
            x, y, z = event.values
            self.callback(x, y, z)
            
    def onAccuracyChanged(self, sensor, accuracy):
        pass
        
class Gyroscope:
    def __init__(self, interface):
        self.interface = interface
        self.context = self.interface.app._impl.native.getApplicationContext()
        self.sensor_manager = self.context.getSystemService(Context.SENSOR_SERVICE)
        self.sensor = self.sensor_manager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        
    def start(self, callback):
        self.callback
        if self.sensor:
            self.listener = GyroscopeListener(callback=callback)
            self.sensor_manager.registerListener(self.listener, self.sensor, SensorManager.SENSOR_DELAY_NORMAL)

    def stop(self):
        self.sensor_manager.unregisterListener(self.listener)