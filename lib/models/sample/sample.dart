
import 'dart:convert';

enum TestEnum { ONE,TWO,THREE }	
enum EnumTwo { TEST,B,A }

class Sample {
  String name;
	double fieldA;
	int fieldB;
	bool isTest;

  Sample({
    this.name = "",
		this.fieldA = 0,
		this.fieldB = 0,
		this.isTest = false,
  });

  Sample.fromJson(Map<dynamic, dynamic> json) {
    name = json["name"] ?? "";
		fieldA = json["fieldA"] ?? 0;
		fieldB = json["fieldB"] ?? 0;
		isTest = json["isTest"] ?? false;
  }

  Sample.fromStringJson(String stringJson) {
    Map valueMap = json.decode(stringJson);
    Sample.fromJson(valueMap);
  }

  String toStringJson() {
    return json.encode(this.toJson());
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data["name"] = this.name;
		data["fieldA"] = this.fieldA;
		data["fieldB"] = this.fieldB;
		data["isTest"] = this.isTest;
    return data;
  }
}