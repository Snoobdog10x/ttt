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

{{ENUMS}}

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
    return Column(
        children: [],
    );
  }

  @override
  void onDispose() {
    
  }
  
  @override
  void onReady() {
    // TODO: implement onReady
  }
}
"""

ABSTRACT_PROVIDER = """
import 'package:flutter/material.dart';
import 'package:reel_t/screens/abstracts/abstract_state.dart';

abstract class AbstractProvider extends ChangeNotifier {
  late AbstractState state;
  void notifyDataChanged() {
    notifyListeners();
  }
}
"""

ABSTRACT_SCREEN = """
import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:reel_t/shared_product/services/app_store.dart';
import 'abstract_provider.dart';

abstract class AbstractState<T extends StatefulWidget> extends State<T> {
  AppStore appStore = AppStore();
  late AbstractProvider _provider;
  late BuildContext _context;
  ConnectivityResult _previousConnectionStatus = ConnectivityResult.wifi;
  ConnectivityResult _connectionStatus = ConnectivityResult.wifi;
  final Connectivity _connectivity = Connectivity();
  late double _topPadding;
  late double _screenHeight;
  late double _screenWidth;
  void onCreate();
  void onDispose();
  void onReady();
  AbstractProvider initProvider();
  BuildContext initContext();
  Widget buildScreen({
    bool isSafe = true,
    Widget? appBar,
    Widget? bottomNavBar,
    Widget? body,
    EdgeInsets? padding,
  }) {
    List<Widget> layout = [];
    if (_previousConnectionStatus == ConnectivityResult.wifi &&
        _connectionStatus == ConnectivityResult.none) {
      layout.add(_buildConnectionStatus(false));
    }

    if (_previousConnectionStatus == ConnectivityResult.none &&
        _connectionStatus == ConnectivityResult.wifi) {
      layout.add(_buildConnectionStatus(true));
      Future.delayed(Duration(seconds: 3), () {
        _updateConnectionStatus(ConnectivityResult.wifi);
      });
    }

    if (appBar != null) {
      layout.add(appBar);
    }
    layout.add(body ?? Container());
    if (isSafe) {
      return Scaffold(
        bottomNavigationBar: bottomNavBar,
        body: Container(
          padding: EdgeInsets.only(
            top: paddingTop(),
            left: padding?.left ?? 0,
            right: padding?.right ?? 0,
            bottom: paddingBottom(),
          ),
          child: Column(
            children: layout,
          ),
        ),
      );
    }
    return Scaffold(
      bottomNavigationBar: bottomNavBar,
      body: Container(
        padding: padding ?? EdgeInsets.zero,
        child: Column(
          children: layout,
        ),
      ),
    );
  }

  Widget _buildConnectionStatus(bool isConnected) {
    return Container(
      height: 40,
      width: double.infinity,
      alignment: Alignment.center,
      color: isConnected ? Colors.green : Colors.red,
      child: Text(isConnected ? "Connected" : "Disconnected"),
    );
  }

  @override
  void initState() {
    super.initState();
    onCreate();
    _provider = initProvider();
    _provider.state = this;
    _context = initContext();
    initConnectivity();
    onReady();
  }

  void notifyDataChanged() {
    _provider?.notifyDataChanged();
  }

  double screenHeight() {
    if (_context == null) {
      return 0;
    }
    return MediaQuery.of(_context!).size.height;
  }

  double screenWidth() {
    if (_context == null) {
      return 0;
    }
    return MediaQuery.of(_context!).size.width;
  }

  double screenRatio() {
    if (_context == null) {
      return 0;
    }
    return MediaQuery.of(_context!).size.aspectRatio;
  }

  double paddingTop() {
    if (_context == null) {
      return 0;
    }
    return MediaQuery.of(_context!).padding.top;
  }

  double paddingBottom() {
    if (_context == null) {
      return 0;
    }
    return MediaQuery.of(_context!).padding.bottom;
  }

  @override
  Widget build(BuildContext context);
  @override
  void dispose() {
    super.dispose();
    onDispose();
  }

  void _updateConnectionStatus(ConnectivityResult result) {
    _previousConnectionStatus = _connectionStatus;
    _connectionStatus = result;
    notifyDataChanged();
  }

  Future<void> initConnectivity() async {
    late ConnectivityResult result;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      result = await _connectivity.checkConnectivity();
      _connectivity.onConnectivityChanged.listen(_updateConnectionStatus);
    } on PlatformException catch (e) {
      print("connect");
      return;
    }

    return _updateConnectionStatus(result);
  }

  bool _isLoading = false;
  void stopLoading() {
    if (!_isLoading) return;
    Navigator.pop(_context);
    _isLoading = false;
  }

  void showAlertDialog({
    String? title,
    String? content,
    Function? confirm,
    Function? cancel,
    bool isLockOutsideTap = false,
  }) {
    List<CupertinoDialogAction> actions = [];
    if (confirm != null) {
      actions.add(
        CupertinoDialogAction(
          isDefaultAction: true,
          onPressed: () {
            confirm();
            Navigator.pop(_context);
          },
          child: const Text('OK'),
        ),
      );
    }

    if (cancel != null) {
      actions.add(
        CupertinoDialogAction(
          isDefaultAction: true,
          onPressed: () {
            cancel();
            Navigator.pop(_context);
          },
          child: const Text('NO'),
        ),
      );
    }
    showCupertinoModalPopup<void>(
      context: _context,
      builder: (BuildContext context) => CupertinoAlertDialog(
        title: Text(title ?? ""),
        content: Text(content ?? ""),
        actions: actions,
      ),
    );
  }

  void startLoading() {
    if (_isLoading) return;

    AlertDialog alert = AlertDialog(
      backgroundColor: Colors.transparent,
      shadowColor: Colors.transparent,
      content: new Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CupertinoActivityIndicator(
            radius: 20,
            color: Colors.grey,
          ),
        ],
      ),
    );
    showDialog(
      barrierDismissible: false,
      context: _context,
      builder: (BuildContext context) {
        return alert;
      },
    );
    _isLoading = true;
    Future.delayed(Duration(seconds: 10), () {
      if (_isLoading) {
        stopLoading();
      }
    });
  }

  void popTopDisplay() {
    Navigator.pop(_context);
  }
}
"""