
import 'package:flutter/material.dart';
abstract class AbstractProvider extends ChangeNotifier{
  void notifyDataChanged(){
    notifyListeners();
  }
}
