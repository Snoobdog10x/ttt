
import 'dart:convert';



class Test {
  

  Test({
    
  });

  Test.fromJson(Map<dynamic, dynamic> json) {
    
  }

  Test.fromStringJson(String stringJson) {
    Map valueMap = json.decode(stringJson);
    Test.fromJson(valueMap);
  }

  String toStringJson() {
    return json.encode(this.toJson());
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    
    return data;
  }
}