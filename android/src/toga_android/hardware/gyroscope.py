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
    def __init__(self, context, callback):
        self.context = context
        self.callback = callback
        self.sensor_manager = context.getSystemService(Context.SENSOR_SERVICE)
        self.sensor = self.sensor_manager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        self.listener = GyroscopeListener(callback=self.callback)

    def start(self):
        if self.sensor:
            self.sensor_manager.registerListener(self.listener, self.sensor, SensorManager.SENSOR_DELAY_NORMAL)

    def stop(self):
        self.sensor_manager.unregisterListener(self.listener)