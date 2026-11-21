# Ethics, provenance and implementation limitations

1. The dashboard uses the CSV supplied for the project. The source report describes the data as recorded/synthetic as supplied and does not establish collection from a deployed home.
2. No physical sensor, ESP32/Arduino controller, relay, MQTT broker, or Blynk dashboard connection is included in this software bundle.
3. Dashboard charts and metrics are descriptive summaries of the supplied dataset only.
4. `alert_flag` is treated as a pre-existing label. Its generation rule and independent ground truth are not known; alert accuracy must not be claimed.
5. The generic `value` column has no common unit documented. Interpret it only after defining its meaning per `sensor_type`.
6. Avoid adding personal identifiers, audio/video, or detailed occupancy histories. Protect any credentials if a real IoT integration is later added.
7. For electrical safety, begin with low-voltage demonstration loads. Mains switching must be designed and checked by a qualified supervisor.
8. Disclose any AI assistance and verify programme-specific declaration requirements with the mentor before signing.
