
import 'package:flutter/material.dart';
import 'package:reel_t/screens/abstracts/abstract_state.dart';

abstract class AbstractProvider extends ChangeNotifier {
  late AbstractState state;
  void notifyDataChanged() {
    notifyListeners();
  }
}
