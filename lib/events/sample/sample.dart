
abstract class SampleEvent {
  void sendSampleEventEvent() {
    try {
      onSampleEventDone(null);
    } catch (e) {
      onSampleEventDone(e);
    }
  }

  void onSampleEventDone(dynamic e);
}