def test_insertWeatherData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_insertWeatherData(self):
        Recorder.called = True

    monkeypatch.setattr(
        'app.weather.controller.WeatherController.insertWeatherData', fake_insertWeatherData)

    # Act
    response = client.get('/weather/fetch')

    # Assert
    assert response.status_code == 200
    assert b'inserted' in response.data
    assert Recorder.called
