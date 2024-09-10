import pytest
import toga


def test_take_gyro_reading(app):
    def callback(abc):
        assert abc == "asdfkjalsdgjhalksdfghj"
        
    """If permission has not been previously requested, it is requested before a photo
    is taken."""
    # Set permission to potentially allowed

   
    gyroscope = app.gyroscope
    print(gyroscope.start(callback))
    
    
    
    