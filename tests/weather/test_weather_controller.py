from app.weather.controller import WeatherController

def test_insertWeatherData(monkeypatch):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called = False

    def fake_insertWeatherData(self, type):
        Recorder.called = True

    monkeypatch.setattr(
        'app.weather.dao.WeatherDAO.insertWeatherData', fake_insertWeatherData)


    # Act
    weatherController = WeatherController()
    weatherController.insertWeatherData()

    # Assert
    assert Recorder.called

def test_getWeatherData(monkeypatch):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called = False

    def fake_getWeatherData(self):
        Recorder.called = True

    monkeypatch.setattr(
        'app.weather.dao.WeatherDAO.getWeatherData', fake_getWeatherData)

    # Act
    weatherController = WeatherController()
    weatherController.getWeatherData()

    # Assert
    assert Recorder.called

