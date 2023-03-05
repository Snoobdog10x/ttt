EVENTS = """
abstract class {{NAMING}}Event {
  void send{{NAMING}}EventEvent() {
    try {
      on{{NAMING}}EventDone(null);
    } catch (e) {
      on{{NAMING}}EventDone(e);
    }
  }

  void on{{NAMING}}EventDone(dynamic e);
}
"""

MODELS = """
import 'dart:convert';

class {{NAMING}} {
  {{CLASS_FIELD}}

  {{NAMING}}({
    {{MAIN_CONSTRUCTOR}}
  });

  {{NAMING}}.fromJson(Map<dynamic, dynamic> json) {
    {{FORM_JSON_CONSTRUCTOR}}
  }

  {{NAMING}}.fromStringJson(String stringJson) {
    Map valueMap = json.decode(stringJson);
    {{NAMING}}.fromJson(valueMap);
  }

  String toStringJson() {
    return json.encode(this.toJson());
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    {{TO_JSON}}
    return data;
  }
}
"""

SCREENS_PROVIDER = """
import 'package:reel_t/screens/abstracts/abstract_provider.dart';

class {{NAMING}}Provider extends AbstractProvider {

}
"""

SCREENS = """
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:reel_t/screens/abstracts/abstract_provider.dart';
import 'package:reel_t/screens/abstracts/abstract_state.dart';
import 'package:reel_t/screens/{{PATH_NAMING}}/{{PATH_NAMING}}_provider.dart';
import 'package:reel_t/shared_product/widgets/default_appbar.dart';

class {{NAMING}}Screen extends StatefulWidget {
  const {{NAMING}}Screen ({super.key});

  @override
  State<{{NAMING}}Screen> createState() => _{{NAMING}}ScreenState();
}

class _{{NAMING}}ScreenState extends AbstractState<{{NAMING}}Screen> {
  late {{NAMING}}Provider provider;
  @override
  AbstractProvider initProvider() {
    return provider;
  }

  @override
  BuildContext initContext() {
    return context;
  }

  @override
  void onCreate() {
    provider = {{NAMING}}Provider();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => provider,
      builder: (context, child) {
        return Consumer<{{NAMING}}Provider>(
          builder: (context, value, child) {
            var body = buildBody();
            return buildScreen(
              appBar: DefaultAppBar(appBarTitle: "sample appbar"),
              body: body,
            );
          },
        );
      },
    );
  }

  Widget buildBody() {
    return Container(
      alignment: Alignment.center,
      child: Column(
        children: [

        ],
      ),
    );
  }

  @override
  void onDispose() {}
}
"""