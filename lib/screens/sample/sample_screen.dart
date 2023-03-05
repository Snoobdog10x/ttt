
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:reel_t/screens/abstracts/abstract_provider.dart';
import 'package:reel_t/screens/abstracts/abstract_state.dart';
import 'package:reel_t/screens/sample/sample_provider.dart';
import 'package:reel_t/shared_product/widgets/default_appbar.dart';

class SampleScreen extends StatefulWidget {
  const SampleScreen ({super.key});

  @override
  State<SampleScreen> createState() => _SampleScreenState();
}

class _SampleScreenState extends AbstractState<SampleScreen> {
  late SampleProvider provider;
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
    provider = SampleProvider();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => provider,
      builder: (context, child) {
        return Consumer<SampleProvider>(
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
  void onDispose() {
    
  }
  
  @override
  void onReady() {
    // TODO: implement onReady
  }
}