
import 'dart:async';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:reel_t/shared_product/first_init.dart';
import 'package:reel_t/shared_product/services/app_store.dart';
import 'abstract_provider.dart';

abstract class AbstractState<T extends StatefulWidget> extends State<T> {
  AppStore appStore = SetUp.firstInit.appStore;
  late AbstractProvider _provider;
  late BuildContext _context;
  late double _topPadding;
  late double _screenHeight;
  late double _screenWidth;
  void onCreate();
  void onDispose();
  void onReady();
  bool hasDisplayConnected = true;
  AbstractProvider initProvider();
  BuildContext initContext();
  Widget buildScreen({
    bool isSafe = true,
    Widget? appBar,
    Widget? bottomNavBar,
    Widget? body,
    EdgeInsets? padding,
    Color background = Colors.white,
  }) {
    List<Widget> child = [];
    List<Widget> layout = [];
    if (!appStore.isConnected()) {
      layout.add(_buildConnectionStatus(false));
      hasDisplayConnected = false;
    }

    if (hasDisplayConnected == false && appStore.isConnected()) {
      layout.add(_buildConnectionStatus(true));
      Future.delayed(Duration(seconds: 2), () {
        hasDisplayConnected = true;
        notifyDataChanged();
      });
    }

    if (appBar != null) {
      child.add(appBar);
    }
    child.add(Expanded(child: body ?? Container()));

    Widget childWidget;
    if (isSafe) {
      childWidget = Container(
        padding: EdgeInsets.only(
          top: paddingTop(),
          left: padding?.left ?? 0,
          right: padding?.right ?? 0,
          bottom: paddingBottom(),
        ),
        child: Column(
          children: child,
        ),
      );
    } else {
      childWidget = Container(
        padding: padding ?? EdgeInsets.zero,
        child: Column(
          children: child,
        ),
      );
    }
    layout.add(Expanded(child: childWidget));

    return Scaffold(
      backgroundColor: background,
      bottomNavigationBar: bottomNavBar,
      body: Column(
        children: layout,
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
    appStore.setNotify(notifyDataChanged);
    WidgetsBinding.instance.addPostFrameCallback(
      (_) async {
        onReady();
      },
    );
  }

  void notifyDataChanged() {
    _provider.notifyDataChanged();
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
